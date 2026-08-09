#!/usr/bin/env python3
"""EMG-JARVIS GoHighLevel live data bridge.

Python 3 standard library only. Runs a small HTTP server on port 8090 that
pulls real calendar/pipeline data from GoHighLevel (via a Private
Integration Token) and exposes it as agent status the viewer can poll.

If config.json's `ghl_token` is blank, every agent reports "standby" and
the viewer shows a banner prompting the user to connect GHL -- no network
calls are made in that case.
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
AGENT_MAP_PATH = os.path.join(BASE_DIR, "agent-map.json")

GHL_API_BASE = "https://services.leadconnectorhq.com"
GHL_API_VERSION = "2021-07-28"
DEFAULT_PORT = 8090
CACHE_TTL = 30  # seconds -- avoid hammering the GHL API on every poll

# agent name -> manually-pushed status override from POST /ghl/push
PUSH_OVERRIDES = {}

# short-lived cache of the raw GHL fetch: {"ts": float, "appointments": [...], "opportunities": [...]}
_CACHE = {"ts": 0, "appointments": [], "opportunities": [], "error": None}


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def load_agent_map():
    with open(AGENT_MAP_PATH, "r") as f:
        return json.load(f)


def ghl_configured(config):
    token = (config.get("ghl_token") or "").strip()
    return bool(token)


def ghl_request(config, path, query=None):
    token = config["ghl_token"].strip()
    url = f"{GHL_API_BASE}{path}"
    if query:
        url += "?" + urllib.parse.urlencode(query)
    req = urllib.request.Request(
        url,
        method="GET",
        headers={
            "Authorization": f"Bearer {token}",
            "Version": GHL_API_VERSION,
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (compatible; EMG-JARVIS-GHL-Bridge/1.0)",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_ghl_data(config, force=False):
    """Fetch (and cache) appointments + opportunities from GHL."""
    now = time.time()
    if not force and (now - _CACHE["ts"]) < CACHE_TTL and _CACHE["ts"] > 0:
        return _CACHE["appointments"], _CACHE["opportunities"], _CACHE["error"]

    location_id = (config.get("ghl_location_id") or "").strip()
    appointments = []
    opportunities = []
    error = None

    try:
        if location_id:
            start_ms = int((now - 86400) * 1000)
            end_ms = int((now + 14 * 86400) * 1000)

            # GHL requires one of calendarId/userId/groupId on /calendars/events,
            # so pull the location's calendars and query events per-calendar,
            # tagging each event with its calendar name for keyword matching.
            calendars = ghl_request(config, "/calendars/", {"locationId": location_id})
            for cal in calendars.get("calendars", []):
                cal_id = cal.get("id")
                if not cal_id:
                    continue
                try:
                    events = ghl_request(config, "/calendars/events", {
                        "locationId": location_id,
                        "calendarId": cal_id,
                        "startTime": start_ms,
                        "endTime": end_ms,
                    })
                except urllib.error.HTTPError:
                    continue
                for ev in events.get("events", events.get("appointments", [])):
                    ev = dict(ev)
                    ev["calendarName"] = cal.get("name", "")
                    appointments.append(ev)

            opps = ghl_request(config, "/opportunities/search", {
                "location_id": location_id,
                "limit": 100,
            })
            opportunities = opps.get("opportunities", [])
        else:
            # No location configured -- try to discover one from the token's
            # accessible locations so the bridge still works out of the box.
            locations = ghl_request(config, "/locations/search", {"limit": 1})
            found = locations.get("locations", [])
            if found:
                config = dict(config)
                config["ghl_location_id"] = found[0].get("id", "")
                return fetch_ghl_data(config, force=True)
            error = "No ghl_location_id configured and none discoverable from token."
    except urllib.error.HTTPError as e:
        error = f"GHL API error {e.code}: {e.read().decode('utf-8', errors='replace')[:200]}"
    except urllib.error.URLError as e:
        error = f"Could not reach GHL API: {e.reason}"
    except Exception as e:
        error = f"GHL fetch failed: {e}"

    _CACHE.update({"ts": now, "appointments": appointments, "opportunities": opportunities, "error": error})
    return appointments, opportunities, error


def _text_of(obj, *keys):
    return " ".join(str(obj.get(k, "")) for k in keys).lower()


def derive_agent_status(agent_map, appointments, opportunities):
    result = {}
    for label, mapping in agent_map.items():
        if label in PUSH_OVERRIDES:
            result[label] = PUSH_OVERRIDES[label]
            continue

        signal = mapping.get("ghl_signal", "none")
        words = mapping.get("match", [])

        if signal == "calendar" and words:
            matches = [
                a for a in appointments
                if any(w in _text_of(a, "title", "calendarName", "appointmentStatus") for w in words)
            ]
            if matches:
                last = matches[-1].get("startTime") or matches[-1].get("dateAdded")
                result[label] = {"status": "active", "tasks": len(matches), "last": last}
            else:
                result[label] = {"status": "idle", "tasks": 0, "last": None}
        elif signal == "pipeline" and words:
            matches = [
                o for o in opportunities
                if any(w in _text_of(o, "name", "pipelineStageName", "status") for w in words)
            ]
            if matches:
                last = matches[-1].get("updatedAt") or matches[-1].get("createdAt")
                result[label] = {"status": "active", "tasks": len(matches), "last": last}
            else:
                result[label] = {"status": "idle", "tasks": 0, "last": None}
        else:
            result[label] = {"status": "standby", "tasks": 0, "last": None}

    return result


def build_todos(opportunities):
    """Derive a lightweight action list from open pipeline opportunities."""
    todos = []
    for o in opportunities:
        status = (o.get("status") or "").lower()
        if status in ("won", "lost", "abandoned"):
            continue
        todos.append({
            "id": o.get("id"),
            "text": f"Follow up: {o.get('name', 'Untitled opportunity')}",
            "stage": o.get("pipelineStageName", ""),
            "updatedAt": o.get("updatedAt") or o.get("createdAt"),
        })
    return todos[:50]


class Handler(BaseHTTPRequestHandler):
    server_version = "EMG-JARVIS-GHL-Bridge/1.0"

    def log_message(self, fmt, *args):
        sys.stderr.write(f"[{self.log_date_time_string()}] {fmt % args}\n")

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _send_json(self, status, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {}

    def do_OPTIONS(self):
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/ghl/status"):
            self._handle_status()
        elif self.path.startswith("/ghl/panels"):
            self._handle_panels()
        else:
            self._send_json(404, {"error": "not found"})

    def do_POST(self):
        if self.path == "/ghl/push":
            self._handle_push()
        else:
            self._send_json(404, {"error": "not found"})

    def _handle_status(self):
        try:
            config = load_config()
            agent_map = load_agent_map()

            if not ghl_configured(config):
                agents = {
                    label: PUSH_OVERRIDES.get(label, {"status": "standby", "tasks": 0, "last": None})
                    for label in agent_map
                }
                self._send_json(200, {
                    "configured": False,
                    "banner": "Connect GHL: add ghl_token to config.json",
                    "agents": agents,
                })
                return

            appointments, opportunities, error = fetch_ghl_data(config)
            agents = derive_agent_status(agent_map, appointments, opportunities)
            self._send_json(200, {
                "configured": True,
                "error": error,
                "agents": agents,
            })
        except Exception as e:
            self._send_json(500, {"error": str(e)})

    def _handle_panels(self):
        try:
            config = load_config()
            if not ghl_configured(config):
                self._send_json(200, {
                    "configured": False,
                    "banner": "Connect GHL: add ghl_token to config.json",
                    "appointments": [],
                    "pipelines": [],
                    "todos": [],
                })
                return

            appointments, opportunities, error = fetch_ghl_data(config)
            self._send_json(200, {
                "configured": True,
                "error": error,
                "appointments": appointments,
                "pipelines": opportunities,
                "todos": build_todos(opportunities),
            })
        except Exception as e:
            self._send_json(500, {"error": str(e)})

    def _handle_push(self):
        try:
            body = self._read_json_body()
            agent = (body.get("agent") or "").strip()
            if not agent:
                self._send_json(400, {"error": "agent is required"})
                return

            PUSH_OVERRIDES[agent] = {
                "status": body.get("status", "active"),
                "tasks": body.get("tasks", 0),
                "last": body.get("last"),
            }
            self._send_json(200, {"status": "ok", "agent": agent})
        except Exception as e:
            self._send_json(500, {"error": str(e)})


def print_banner(config, port):
    configured = ghl_configured(config)
    banner = f"""
==============================================================
   E M G - J A R V I S  ::  G H L   B R I D G E
==============================================================
   GHL token:        {'connected' if configured else 'NOT SET (agents will report standby)'}
   URL:              http://localhost:{port}
   Endpoints:        GET /ghl/status  GET /ghl/panels  POST /ghl/push
==============================================================
"""
    print(banner)


def main():
    config = load_config()
    port = config.get("ghl_port", DEFAULT_PORT)
    print_banner(config, port)

    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nEMG-JARVIS GHL bridge shutting down.")
        server.shutdown()


if __name__ == "__main__":
    main()
