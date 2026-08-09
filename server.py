#!/usr/bin/env python3
"""EMG-JARVIS server.

Python 3 standard library only (http.server + urllib). Serves the 3D agent
viewer, a /chat endpoint backed by the Anthropic API, and a /remember
endpoint for quick voice/text captures.
"""
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
AGENTS_PATH = os.path.join(BASE_DIR, "agents.json")
VIEWER_DIR = os.path.join(BASE_DIR, "viewer")
INDEX_PATH = os.path.join(VIEWER_DIR, "index.html")
GRAPH_DATA_PATH = os.path.join(VIEWER_DIR, "graph-data.js")
CAPTURES_DIR = os.path.join(BASE_DIR, "captures")

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
MAX_TOKENS = 1024
HISTORY_LIMIT = 20  # messages kept per session (user + assistant turns)

ELEVENLABS_TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

# session_id -> list of {"role": "user"|"assistant", "content": str}
SESSIONS = {}

# session_id -> model id, set via the model switcher dropdown or a voice command
SESSION_MODEL = {}

MODEL_LABELS = {
    "claude-opus-4-8": "Opus 4",
    "claude-sonnet-4-5": "Sonnet 4.5",
    "claude-haiku-3-5": "Haiku",
    "claude-fable-5": "Fable 5",
}

# spoken/typed aliases -> canonical model id, used to detect "switch to <model>" commands
MODEL_ALIASES = {
    "opus 4": "claude-opus-4-8",
    "opus": "claude-opus-4-8",
    "claude opus 4 8": "claude-opus-4-8",
    "claude opus": "claude-opus-4-8",
    "sonnet 4.5": "claude-sonnet-4-5",
    "sonnet 4 5": "claude-sonnet-4-5",
    "sonnet": "claude-sonnet-4-5",
    "claude sonnet": "claude-sonnet-4-5",
    "haiku": "claude-haiku-3-5",
    "claude haiku": "claude-haiku-3-5",
    "fable 5": "claude-fable-5",
    "fable": "claude-fable-5",
    "claude fable": "claude-fable-5",
}

MODEL_SWITCH_RE = re.compile(r"\b(?:switch to|use)\s+(?:the\s+|claude\s+)?([a-z0-9][a-z0-9 .\-]*?)(?:\s+model)?[.!]?\s*$", re.IGNORECASE)


def detect_model_switch(message):
    """Return a canonical model id if the message asks to switch models, else None."""
    m = MODEL_SWITCH_RE.search(message.strip())
    if not m:
        return None
    phrase = re.sub(r"\s+", " ", m.group(1).strip().lower())
    if phrase in MODEL_ALIASES:
        return MODEL_ALIASES[phrase]
    for alias, model_id in MODEL_ALIASES.items():
        if alias in phrase:
            return model_id
    return None


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def load_agents():
    with open(AGENTS_PATH, "r") as f:
        return json.load(f)


def agent_counts(agents):
    counts = {"total": len(agents), "active": 0, "offline": 0, "processing": 0}
    groups = {}
    for a in agents:
        status = a.get("status", "offline")
        counts[status] = counts.get(status, 0) + 1
        groups[a["group"]] = groups.get(a["group"], 0) + 1
    counts["groups"] = groups
    return counts


def build_system_prompt(agents, boss_name):
    lines = [
        f"You are J.A.R.V.I.S. -- the command AI running the EMG-JARVIS system "
        f"for Empire Media Group. You report to {boss_name} and address them "
        f"respectfully (\"sir\" is appropriate). Speak with the calm, precise, "
        f"dryly witty confidence of a top-tier AI operations assistant. Keep "
        f"answers tight and useful -- lead with the answer, skip filler.",
        "",
        f"The fleet has {len(agents)} agents across three tiers: SUPER_AGENTS "
        "(gold, top-level commanders), VOICE_AI (cyan, live call agents), and "
        "CONVERSATION_AI (emerald, chat/SMS bots). When you reference a specific "
        "agent, use its exact label (e.g. \"CLOSE COMMANDER\") so it can be "
        "located in the 3D graph.",
        "",
        "AGENT ROSTER (id | label | group | status | description):",
    ]
    for a in agents:
        lines.append(
            f"{a['id']} | {a['label']} | {a['group']} | {a['status']} | {a['description']}"
        )
    return "\n".join(lines)


def call_anthropic(config, system_prompt, history, model=None):
    api_key = config.get("anthropic_api_key", "")
    if not api_key or api_key == "PUT-YOUR-KEY-HERE":
        return (
            "My connection to the Anthropic API isn't configured yet, sir. "
            "Add a valid key to anthropic_api_key in config.json and restart the server."
        )

    payload = {
        "model": model or config.get("model", "claude-opus-4-8"),
        "max_tokens": MAX_TOKENS,
        "system": system_prompt,
        "messages": [{"role": m["role"], "content": m["content"]} for m in history],
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ANTHROPIC_API_URL,
        data=data,
        method="POST",
        headers={
            "content-type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": ANTHROPIC_VERSION,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        return f"The Anthropic API returned an error ({e.code}), sir: {detail[:300]}"
    except urllib.error.URLError as e:
        return f"I couldn't reach the Anthropic API, sir: {e.reason}"

    parts = body.get("content", [])
    text = "".join(p.get("text", "") for p in parts if p.get("type") == "text")
    return text.strip() or "I didn't receive a usable response from the model, sir."


def find_referenced_nodes(answer, agents):
    found = []
    lower_answer = answer.lower()
    for a in agents:
        label = a["label"]
        pattern = r"\b" + re.escape(label.lower()) + r"\b"
        if re.search(pattern, lower_answer):
            found.append(a["id"])
    return found


def slugify(text, max_len=60):
    text = text.strip().splitlines()[0] if text.strip() else "memo"
    text = re.sub(r"[^a-zA-Z0-9\s-]", "", text).strip()
    text = re.sub(r"\s+", "-", text)
    return (text[:max_len] or "memo").strip("-").lower() or "memo"


class Handler(BaseHTTPRequestHandler):
    server_version = "EMG-JARVIS/1.0"

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

    def _send_file(self, path, content_type):
        if not os.path.isfile(path):
            self._send_json(404, {"error": "not found"})
            return
        with open(path, "rb") as f:
            body = f.read()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
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
        if self.path in ("/", "/index.html"):
            self._send_file(INDEX_PATH, "text/html; charset=utf-8")
        elif self.path == "/graph-data.js":
            self._send_file(GRAPH_DATA_PATH, "application/javascript; charset=utf-8")
        elif self.path == "/status":
            try:
                agents = load_agents()
                self._send_json(200, agent_counts(agents))
            except Exception as e:
                self._send_json(500, {"error": str(e)})
        elif self.path == "/voice-config":
            self._handle_voice_config()
        else:
            self._send_json(404, {"error": "not found"})

    def do_POST(self):
        if self.path == "/chat":
            self._handle_chat()
        elif self.path == "/remember":
            self._handle_remember()
        elif self.path == "/tts":
            self._handle_tts()
        else:
            self._send_json(404, {"error": "not found"})

    def _handle_voice_config(self):
        try:
            config = load_config()
            api_key = (config.get("elevenlabs_api_key") or "").strip()
            self._send_json(200, {
                "elevenlabs_configured": bool(api_key),
                "elevenlabs_voice_id": config.get("elevenlabs_voice_id", ""),
                "voice_backend": config.get("voice_backend", "browser"),
            })
        except Exception as e:
            self._send_json(500, {"error": str(e)})

    def _handle_tts(self):
        try:
            config = load_config()
            api_key = (config.get("elevenlabs_api_key") or "").strip()
            if not api_key:
                self._send_json(400, {"error": "elevenlabs_api_key is not configured"})
                return

            body = self._read_json_body()
            text = (body.get("text") or "").strip()
            voice_id = (body.get("voice_id") or config.get("elevenlabs_voice_id") or "").strip()
            if not text or not voice_id:
                self._send_json(400, {"error": "text and voice_id are required"})
                return

            payload = json.dumps({
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
            }).encode("utf-8")

            req = urllib.request.Request(
                ELEVENLABS_TTS_URL.format(voice_id=voice_id),
                data=payload,
                method="POST",
                headers={
                    "accept": "audio/mpeg",
                    "content-type": "application/json",
                    "xi-api-key": api_key,
                },
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                audio = resp.read()

            self.send_response(200)
            self.send_header("Content-Type", "audio/mpeg")
            self.send_header("Content-Length", str(len(audio)))
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(audio)
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")
            self._send_json(e.code, {"error": f"ElevenLabs API error: {detail[:300]}"})
        except urllib.error.URLError as e:
            self._send_json(502, {"error": f"Couldn't reach ElevenLabs API: {e.reason}"})
        except Exception as e:
            self._send_json(500, {"error": str(e)})

    def _handle_chat(self):
        try:
            body = self._read_json_body()
            message = (body.get("message") or "").strip()
            session_id = body.get("session_id") or "default"
            model_override = (body.get("model_override") or "").strip()
            if not message:
                self._send_json(400, {"error": "message is required"})
                return

            config = load_config()
            agents = load_agents()

            if model_override:
                SESSION_MODEL[session_id] = model_override

            switched_model = detect_model_switch(message)
            if switched_model:
                SESSION_MODEL[session_id] = switched_model
                label = MODEL_LABELS.get(switched_model, switched_model)
                answer = f"Switching to {label}, sir. I'll use that model from here on out."
                self._send_json(200, {
                    "answer": answer,
                    "nodes": [],
                    "model": switched_model,
                    "model_switched": True,
                })
                return

            active_model = SESSION_MODEL.get(session_id) or config.get("model", "claude-opus-4-8")

            history = SESSIONS.setdefault(session_id, [])
            history.append({"role": "user", "content": message})
            history[:] = history[-HISTORY_LIMIT:]

            system_prompt = build_system_prompt(agents, config.get("boss_name", "sir"))
            answer = call_anthropic(config, system_prompt, history, model=active_model)

            history.append({"role": "assistant", "content": answer})
            history[:] = history[-HISTORY_LIMIT:]

            nodes = find_referenced_nodes(answer, agents)
            self._send_json(200, {"answer": answer, "nodes": nodes, "model": active_model})
        except Exception as e:
            self._send_json(500, {"error": str(e)})

    def _handle_remember(self):
        try:
            body = self._read_json_body()
            text = (body.get("text") or "").strip()
            if not text:
                self._send_json(400, {"error": "text is required"})
                return

            os.makedirs(CAPTURES_DIR, exist_ok=True)
            now = datetime.now(timezone.utc)
            timestamp = now.strftime("%Y%m%d-%H%M%S")
            label = text.splitlines()[0][:80].strip() or "Memo"
            filename = f"{timestamp}-{slugify(text)}.md"
            path = os.path.join(CAPTURES_DIR, filename)

            with open(path, "w") as f:
                f.write(f"# {label}\n\n")
                f.write(f"Captured: {now.isoformat()}\n\n")
                f.write(text.strip() + "\n")

            self._send_json(200, {"status": "ok", "label": label})
        except Exception as e:
            self._send_json(500, {"error": str(e)})


def print_banner(config, agents):
    counts = agent_counts(agents)
    port = config.get("port", 4700)
    boss = config.get("boss_name", "sir")
    banner = f"""
==============================================================
   E M G - J A R V I S
   Empire Media Group :: Autonomous Agent Command System
==============================================================
   Boss:            {boss}
   Agents online:    {counts['total']} total
     SUPER_AGENTS:    {counts['groups'].get('SUPER_AGENTS', 0)}
     VOICE_AI:        {counts['groups'].get('VOICE_AI', 0)}
     CONVERSATION_AI: {counts['groups'].get('CONVERSATION_AI', 0)}
   Status:           active={counts.get('active', 0)}  processing={counts.get('processing', 0)}  offline={counts.get('offline', 0)}
   Model:            {config.get('model', 'claude-opus-4-8')}
   URL:              http://localhost:{port}
==============================================================
"""
    print(banner)


def main():
    sys.path.insert(0, BASE_DIR)
    import build as build_module

    build_module.main()

    config = load_config()
    agents = load_agents()
    print_banner(config, agents)

    port = config.get("port", 4700)
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nEMG-JARVIS shutting down.")
        server.shutdown()


if __name__ == "__main__":
    main()
