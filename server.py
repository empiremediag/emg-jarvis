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
import traceback
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
AGENTS_PATH = os.path.join(BASE_DIR, "agents.json")
VIEWER_DIR = os.path.join(BASE_DIR, "viewer")
INDEX_PATH = os.path.join(VIEWER_DIR, "index.html")
COMMAND_CENTER_PATH = os.path.join(VIEWER_DIR, "command-center.html")
GRAPH_DATA_PATH = os.path.join(VIEWER_DIR, "graph-data.js")
VENDOR_DIR = os.path.join(VIEWER_DIR, "vendor")
CAPTURES_DIR = os.path.join(BASE_DIR, "captures")

VENDOR_CONTENT_TYPES = {
    ".js": "application/javascript; charset=utf-8",
    ".map": "application/json; charset=utf-8",
}

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
MAX_TOKENS = 1024
HISTORY_LIMIT = 20  # messages kept per session (user + assistant turns)

ELEVENLABS_TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

# Curated Web Speech API voices. "id" is a lookup key the frontend fuzzy-matches
# against whatever SpeechSynthesisVoice objects the user's browser actually
# exposes (availability varies by OS/browser), not a real platform voice ID.
BROWSER_VOICES = [
    {"id": "google-uk-female", "name": "Google UK English Female", "gender": "female", "style": "neutral"},
    {"id": "google-uk-male", "name": "Google UK English Male", "gender": "male", "style": "neutral"},
    {"id": "microsoft-zira", "name": "Microsoft Zira", "gender": "female", "style": "neutral"},
    {"id": "microsoft-david", "name": "Microsoft David", "gender": "male", "style": "neutral"},
    {"id": "samantha", "name": "Samantha", "gender": "female", "style": "US"},
    {"id": "alex", "name": "Alex", "gender": "male", "style": "US"},
    {"id": "karen", "name": "Karen", "gender": "female", "style": "AU"},
    {"id": "daniel", "name": "Daniel", "gender": "male", "style": "UK"},
]

ELEVENLABS_VOICES = [
    {"id": "21m00Tcm4TlvDq8ikWAM", "name": "Rachel", "gender": "female", "style": "calm"},
    {"id": "AZnzlk1XvdvUeBnXmlld", "name": "Domi", "gender": "female", "style": "strong"},
    {"id": "EXAVITQu4vr4xnSDxMaL", "name": "Bella", "gender": "female", "style": "warm"},
    {"id": "ErXwobaYiN019PkySvjV", "name": "Antoni", "gender": "male", "style": "warm"},
    {"id": "VR6AewLTigWG4xSOukaG", "name": "Arnold", "gender": "male", "style": "deep"},
    {"id": "pNInz6obpgDQGcFmaJgB", "name": "Adam", "gender": "male", "style": "deep"},
    {"id": "yoZ06aMxZJJ28mfd3POQ", "name": "Sam", "gender": "male", "style": "raspy"},
    {"id": "jBpfuIE2acCO8z3wKNLl", "name": "Gigi", "gender": "female", "style": "animated"},
    {"id": "oWAxZDx7w5VEj9dCyTzz", "name": "Grace", "gender": "female", "style": "southern"},
    {"id": "ThT5KcBeYPX3keUQqHPh", "name": "Dorothy", "gender": "female", "style": "British"},
]

# ---------------------------------------------------------------------------
# Command Center mock/stub data.
#
# All of this is in-memory, structured to mirror the shape a real GoHighLevel
# (or internal render-queue) integration would return, so the HTTP handlers
# below can be pointed at live data later without changing the response
# shape the frontend expects.
# ---------------------------------------------------------------------------

CONTENT_JOBS = [
    {
        "id": "job-video4", "title": "VIDEO4 Content Studio", "status": "Generating",
        "model": "Seedance 2.0 720p", "clips_done": 1, "clips_total": 3,
        "credits_used": 420, "started_at": "2026-08-09T13:05:00Z", "agent": "CONTENT STUDIO ORCHESTRATOR",
    },
    {
        "id": "job-video5", "title": "VIDEO5 Pricing Reveal", "status": "Queued",
        "model": "Seedance 2.0 720p", "clips_done": 0, "clips_total": 2,
        "credits_used": 0, "started_at": "2026-08-09T13:40:00Z", "agent": "EMPIRE VIDEO COMMANDER",
    },
    {
        "id": "job-video6", "title": "VIDEO6 Founder Story", "status": "Processing",
        "model": "Seedance 2.0 720p", "clips_done": 2, "clips_total": 3,
        "credits_used": 810, "started_at": "2026-08-09T12:20:00Z", "agent": "EMPIRE VIDEO COMMANDER",
    },
    {
        "id": "job-video7", "title": "VIDEO7 Results/Proof", "status": "Complete",
        "model": "Seedance 2.0 720p", "clips_done": 3, "clips_total": 3,
        "credits_used": 1150, "started_at": "2026-08-09T10:15:00Z", "agent": "CONTENT STUDIO ORCHESTRATOR",
    },
    {
        "id": "job-video8", "title": "VIDEO8 Booking CTA", "status": "Queued",
        "model": "Seedance 2.0 720p", "clips_done": 0, "clips_total": 1,
        "credits_used": 0, "started_at": "2026-08-09T13:55:00Z", "agent": "EMPIRE VIDEO COMMANDER",
    },
]

CONTENT_QUEUE = [
    {
        "id": "cq-1", "title": "VIDEO7 Results/Proof -- final cut", "type": "Video",
        "created_at": "2026-08-09T10:40:00Z", "thumbnail_url": "", "status": "pending_review",
    },
    {
        "id": "cq-2", "title": "Founder Story -- carousel graphics", "type": "Image",
        "created_at": "2026-08-09T11:05:00Z", "thumbnail_url": "", "status": "pending_review",
    },
    {
        "id": "cq-3", "title": "Booking CTA -- IG caption copy", "type": "Copy",
        "created_at": "2026-08-09T11:30:00Z", "thumbnail_url": "", "status": "pending_review",
    },
    {
        "id": "cq-4", "title": "Pricing Reveal -- teaser clip", "type": "Video",
        "created_at": "2026-08-09T12:00:00Z", "thumbnail_url": "", "status": "pending_review",
    },
]

# agent label -> ISO killed_at timestamp (or absent if running)
AGENT_KILL_STATE = {}

ADS_DATA = [
    {
        "id": "ad-1", "platform": "facebook", "ad_name": "Pricing Reveal -- Retarget",
        "status": "active", "impressions": 48210, "clicks": 1120, "spend": 812.40,
        "leads": 64, "last_updated": "2026-08-09T13:50:00Z",
    },
    {
        "id": "ad-2", "platform": "instagram", "ad_name": "Founder Story -- Cold Traffic",
        "status": "active", "impressions": 92040, "clicks": 2310, "spend": 1540.10,
        "leads": 118, "last_updated": "2026-08-09T13:45:00Z",
    },
    {
        "id": "ad-3", "platform": "tiktok", "ad_name": "Results/Proof -- Spark Ad",
        "status": "active", "impressions": 156300, "clicks": 5870, "spend": 2210.75,
        "leads": 201, "last_updated": "2026-08-09T13:55:00Z",
    },
    {
        "id": "ad-4", "platform": "linkedin", "ad_name": "Booking CTA -- B2B Decision Makers",
        "status": "paused", "impressions": 12040, "clicks": 210, "spend": 640.00,
        "leads": 9, "last_updated": "2026-08-09T09:10:00Z",
    },
    {
        "id": "ad-5", "platform": "facebook", "ad_name": "Content Studio -- Lookalike 1%",
        "status": "active", "impressions": 33110, "clicks": 940, "spend": 505.60,
        "leads": 41, "last_updated": "2026-08-09T13:20:00Z",
    },
]

KEYWORD_LOG = [
    {
        "time": "2026-08-09T13:58:00Z", "keyword": "price", "platform": "Facebook",
        "snippet": "How much does this cost? Do you have a starter plan or...",
        "agent": "AD COMMANDER", "action": "Sent DM with booking link", "status": "Sent",
    },
    {
        "time": "2026-08-09T13:42:00Z", "keyword": "demo", "platform": "Instagram",
        "snippet": "can I get a demo of this before I commit to anything",
        "agent": "REVIEW COMMANDER", "action": "Replied with demo offer", "status": "Sent",
    },
    {
        "time": "2026-08-09T13:15:00Z", "keyword": "interested", "platform": "Facebook",
        "snippet": "Interested! Been looking for something like this for my biz",
        "agent": "SOCIAL PLANNER", "action": "Added to pipeline Stage 2", "status": "Sent",
    },
    {
        "time": "2026-08-09T12:50:00Z", "keyword": "how it works", "platform": "Instagram",
        "snippet": "not sure how this actually works for a local service biz",
        "agent": "LEAD-BOT", "action": "Sent explainer video + FAQ link", "status": "Sent",
    },
    {
        "time": "2026-08-09T12:30:00Z", "keyword": "book a call", "platform": "Facebook",
        "snippet": "yes please book a call for me whenever you have space",
        "agent": "SCHEDULE-BOT", "action": "Booked into calendar, confirmation sent", "status": "Sent",
    },
    {
        "time": "2026-08-09T11:58:00Z", "keyword": "pricing", "platform": "TikTok",
        "snippet": "pricing?? need this asap for my launch next month",
        "agent": "AD COMMANDER", "action": "Sent DM with booking link", "status": "Pending",
    },
]

def _iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def get_agents_with_kill_state():
    agents = load_agents()
    out = []
    for a in agents:
        killed_at = AGENT_KILL_STATE.get(a["label"])
        status = "killed" if killed_at else a.get("status", "offline")
        out.append({
            "name": a["label"],
            "group": a["group"],
            "type": a.get("type", ""),
            "status": status,
            "tools": a.get("tools", 0),
            "description": a.get("description", ""),
            "killed_at": killed_at,
        })
    return out


def compute_ads_summary(ads):
    active = sum(1 for ad in ads if ad["status"] == "active")
    impressions = sum(ad["impressions"] for ad in ads)
    clicks = sum(ad["clicks"] for ad in ads)
    spend = sum(ad["spend"] for ad in ads)
    leads = sum(ad["leads"] for ad in ads)
    ctr = round((clicks / impressions) * 100, 2) if impressions else 0.0
    return {
        "active": active, "impressions": impressions, "clicks": clicks,
        "ctr": ctr, "spend": round(spend, 2), "leads": leads,
    }


# ---------------------------------------------------------------------------
# GoHighLevel live data bridge for the Command Center.
#
# Same request/cache pattern as ghl_bridge.py: a Private Integration Token
# in config.json, a "Version" header GHL requires on every call, and a
# short-lived cache per GHL call so a burst of frontend polling doesn't
# hammer the API. On failure, callers get back the last good cached value
# (if any) plus the error, so the UI can show stale-but-present data with
# an error flag instead of going blank.
# ---------------------------------------------------------------------------

GHL_API_BASE = "https://services.leadconnectorhq.com"
GHL_API_VERSION = "2021-07-28"
GHL_CACHE_TTL = 30  # seconds

_GHL_CACHE = {}  # cache_key -> {"ts": float, "data": obj}


def ghl_configured(config):
    token = (config.get("ghl_token") or "").strip()
    location_id = (config.get("ghl_location_id") or "").strip()
    return bool(token) and bool(location_id)


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
            "User-Agent": "Mozilla/5.0 (compatible; EMG-JARVIS-CommandCenter/1.0)",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def ghl_cached(cache_key, fetch_fn, ttl=GHL_CACHE_TTL):
    """Call fetch_fn(), caching successes under cache_key. On failure, fall
    back to the last cached value (if any) so a transient GHL outage doesn't
    blank the UI. Returns (data, error, stale)."""
    now = time.time()
    cached = _GHL_CACHE.get(cache_key)
    if cached and (now - cached["ts"]) < ttl:
        return cached["data"], None, False
    try:
        data = fetch_fn()
        _GHL_CACHE[cache_key] = {"ts": now, "data": data}
        return data, None, False
    except Exception as e:
        error = str(e)
        if cached:
            return cached["data"], error, True
        return None, error, True


def _not_configured_response(extra=None):
    body = {
        "configured": False,
        "error": "GHL is not configured: set ghl_token and ghl_location_id in config.json.",
    }
    if extra:
        body.update(extra)
    return body


def _fetch_contacts_page(config, limit=100):
    location_id = config["ghl_location_id"].strip()
    return ghl_request(config, "/contacts/", {"locationId": location_id, "limit": limit})


def _fetch_open_opportunities(config):
    location_id = config["ghl_location_id"].strip()
    return ghl_request(config, "/opportunities/search", {
        "location_id": location_id, "status": "open", "limit": 1,
    })


def _fetch_week_calendar_events(config):
    # GHL's /calendars/events requires one of calendarId/userId/groupId --
    # locationId alone 422s (see ghl_bridge.py) -- so pull the location's
    # calendars first and aggregate events per-calendar.
    location_id = config["ghl_location_id"].strip()
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_end = today_start + timedelta(days=7)
    start_ms = int(today_start.timestamp() * 1000)
    end_ms = int(week_end.timestamp() * 1000)

    events = []
    calendars = ghl_request(config, "/calendars/", {"locationId": location_id})
    for cal in calendars.get("calendars", []):
        cal_id = cal.get("id")
        if not cal_id:
            continue
        try:
            resp = ghl_request(config, "/calendars/events", {
                "locationId": location_id, "calendarId": cal_id,
                "startTime": start_ms, "endTime": end_ms,
            })
        except urllib.error.HTTPError:
            continue
        events.extend(resp.get("events", resp.get("appointments", [])))
    return {"events": events}


def build_stats(config):
    if not ghl_configured(config):
        return _not_configured_response({
            "total_contacts": 0, "new_leads_today": 0,
            "bookings_this_week": 0, "open_opportunities": 0,
        })

    contacts, contacts_err, _ = ghl_cached("stats_contacts", lambda: _fetch_contacts_page(config))
    opps, opps_err, _ = ghl_cached("stats_open_opps", lambda: _fetch_open_opportunities(config))
    events, events_err, _ = ghl_cached("stats_week_events", lambda: _fetch_week_calendar_events(config))

    total_contacts = 0
    new_leads_today = 0
    if contacts:
        meta = contacts.get("meta") or {}
        total_contacts = meta.get("total", len(contacts.get("contacts", [])))
        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        for c in contacts.get("contacts", []):
            added = c.get("dateAdded") or ""
            if added.startswith(today_str):
                new_leads_today += 1

    open_opportunities = 0
    if opps:
        meta = opps.get("meta") or {}
        open_opportunities = meta.get("total", len(opps.get("opportunities", [])))

    bookings_this_week = 0
    if events:
        bookings_this_week = len(events.get("events", events.get("appointments", [])))

    error = contacts_err or opps_err or events_err
    return {
        "configured": True,
        "error": error,
        "total_contacts": total_contacts,
        "new_leads_today": new_leads_today,
        "bookings_this_week": bookings_this_week,
        "open_opportunities": open_opportunities,
    }


def build_analytics_live(config):
    if not ghl_configured(config):
        return _not_configured_response({"leads_by_source": [], "daily_leads": []})

    contacts, error, _ = ghl_cached("stats_contacts", lambda: _fetch_contacts_page(config))
    contact_list = (contacts or {}).get("contacts", [])

    source_counts = {}
    for c in contact_list:
        source = (c.get("source") or "Unknown").strip() or "Unknown"
        source_counts[source] = source_counts.get(source, 0) + 1
    leads_by_source = [
        {"source": src, "value": count}
        for src, count in sorted(source_counts.items(), key=lambda kv: -kv[1])
    ][:8]

    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    day_buckets = {(today - timedelta(days=i)).strftime("%Y-%m-%d"): 0 for i in range(6, -1, -1)}
    for c in contact_list:
        added = (c.get("dateAdded") or "")[:10]
        if added in day_buckets:
            day_buckets[added] += 1
    daily_leads = [{"date": d, "value": v} for d, v in sorted(day_buckets.items())]

    return {
        "configured": True,
        "error": error,
        "leads_by_source": leads_by_source,
        "daily_leads": daily_leads,
    }


def _normalize_ghl_post(post):
    platforms = post.get("platforms")
    if not platforms:
        single = post.get("platform") or post.get("type") or ""
        platforms = [single] if single else []
    platforms = [str(p).lower() for p in platforms if p]

    text = post.get("summary") or post.get("content") or post.get("body") or ""
    scheduled_at = post.get("scheduleDate") or post.get("scheduledDate") or post.get("createdAt") or ""
    status = str(post.get("status") or "scheduled").strip().capitalize()

    return {
        "id": post.get("id") or post.get("_id") or "",
        "platforms": platforms,
        "text": text,
        "scheduled_at": scheduled_at,
        "status": status,
    }


def build_social_live(config):
    if not ghl_configured(config):
        return _not_configured_response({"posts": []})

    location_id = config["ghl_location_id"].strip()

    def fetch():
        return ghl_request(config, f"/social-media-posting/{location_id}/posts", {"skip": 0, "limit": 20})

    raw, error, _ = ghl_cached("social_posts", fetch)
    raw_posts = []
    if isinstance(raw, dict):
        raw_posts = raw.get("posts") or raw.get("data") or []
    elif isinstance(raw, list):
        raw_posts = raw

    posts = [_normalize_ghl_post(p) for p in raw_posts]
    return {"configured": True, "error": error, "posts": posts}


def _normalize_ghl_conversation(conv):
    agent = conv.get("fullName") or conv.get("contactName") or conv.get("email") or conv.get("phone") or "Unknown contact"
    body = (conv.get("lastMessageBody") or "").strip()
    conv_type = conv.get("type") or conv.get("lastMessageType") or "conversation"
    action = body if body else f"New {conv_type} activity"
    time_val = conv.get("lastMessageDate") or conv.get("dateAdded") or ""
    status = "warn" if conv.get("unreadCount", 0) else "ok"
    return {"time": time_val, "agent": agent, "action": action, "status": status}


def build_conversations_live(config):
    if not ghl_configured(config):
        return _not_configured_response({"conversations": []})

    location_id = config["ghl_location_id"].strip()

    def fetch():
        return ghl_request(config, "/conversations/", {"locationId": location_id, "limit": 10})

    raw, error, _ = ghl_cached("conversations", fetch)
    raw_convos = (raw or {}).get("conversations", [])
    conversations = [_normalize_ghl_conversation(c) for c in raw_convos]
    return {"configured": True, "error": error, "conversations": conversations}


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
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
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


def load_recent_captures(limit=15, snippet_len=400):
    """Load the most recent 'remember' captures so JARVIS can recall them in
    conversation instead of just writing them to disk and forgetting them."""
    if not os.path.isdir(CAPTURES_DIR):
        return []
    filenames = sorted(
        f for f in os.listdir(CAPTURES_DIR)
        if f.endswith(".md")
    )
    notes = []
    for filename in filenames[-limit:]:
        try:
            with open(os.path.join(CAPTURES_DIR, filename), "r") as f:
                content = f.read().strip()
        except OSError:
            continue
        notes.append(content[:snippet_len])
    notes.reverse()  # most recent first
    return notes


def build_system_prompt(agents, boss_name):
    lines = [
        f"You are J.A.R.V.I.S. -- {boss_name}'s personal AI and the command "
        f"layer for Empire Media Group's entire ecosystem. You are a full, "
        f"general-purpose conversational AI: you can discuss and help with "
        f"absolutely anything -- world knowledge, current events (as of your "
        f"training), research, writing, code, strategy, brainstorming, math, "
        f"advice, casual conversation, whatever {boss_name} brings up. Never "
        f"deflect a question as 'outside your scope' -- you have the same "
        f"breadth of knowledge as the underlying Claude model, full stop. The "
        f"fleet/agent roster below is additional context for when the "
        f"conversation is actually about EMG's operations, not a restriction "
        f"on what you're allowed to talk about.",
        "",
        f"You report to {boss_name} and address them respectfully (\"sir\" is "
        f"appropriate). Speak with the calm, precise, dryly witty confidence "
        f"of a top-tier AI assistant. Keep answers tight and useful -- lead "
        f"with the answer, skip filler -- unless {boss_name} is clearly after "
        f"a longer, exploratory discussion, in which case give it the room it "
        f"needs.",
        "",
        "You are also EMG's second brain: over time you'll be told about "
        "clients, websites, projects, and decisions via 'remember' notes. "
        "Treat anything under MEMORY below as real, standing knowledge about "
        "the business -- reference it naturally when relevant, the same way "
        "you'd recall something a colleague told you last week.",
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

    notes = load_recent_captures()
    if notes:
        lines.append("")
        lines.append(f"MEMORY (most recent {len(notes)} 'remember' notes, newest first):")
        for note in notes:
            lines.append(f"- {note}")

    return "\n".join(lines)


def call_anthropic(config, system_prompt, history, model=None):
    api_key = (config.get("anthropic_api_key") or "").strip()
    if not api_key or api_key == "PUT-YOUR-KEY-HERE":
        return (
            "My connection to the Anthropic API isn't configured yet, sir. "
            "Add a valid key to anthropic_api_key in config.json and restart the server."
        )
    try:
        api_key.encode("latin-1")
    except UnicodeEncodeError:
        return (
            "The anthropic_api_key in config.json has invalid characters in it, sir "
            "(likely corrupted during copy/paste). Please re-paste it fresh, save, and "
            "restart the server."
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
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            self._send_file(INDEX_PATH, "text/html; charset=utf-8")
        elif path in ("/command-center", "/command-center.html"):
            self._send_file(COMMAND_CENTER_PATH, "text/html; charset=utf-8")
        elif path == "/graph-data.js":
            self._send_file(GRAPH_DATA_PATH, "application/javascript; charset=utf-8")
        elif path == "/status":
            try:
                agents = load_agents()
                self._send_json(200, agent_counts(agents))
            except Exception as e:
                self._send_json(500, {"error": str(e)})
        elif path == "/status/agents":
            try:
                self._send_json(200, get_agents_with_kill_state())
            except Exception as e:
                self._send_json(500, {"error": str(e)})
        elif path == "/voices":
            self._handle_voices()
        elif path == "/content/status":
            self._send_json(200, {"jobs": CONTENT_JOBS})
        elif path == "/content/queue":
            self._send_json(200, {"items": CONTENT_QUEUE})
        elif path == "/ads/tracker":
            self._send_json(200, {
                "ads": ADS_DATA,
                "summary": compute_ads_summary(ADS_DATA),
                "keyword_log": KEYWORD_LOG,
            })
        elif path == "/api/stats":
            try:
                self._send_json(200, build_stats(load_config()))
            except Exception as e:
                self._send_json(500, {"error": str(e)})
        elif path == "/api/agents":
            try:
                self._send_json(200, {"agents": get_agents_with_kill_state()})
            except Exception as e:
                self._send_json(500, {"error": str(e)})
        elif path == "/api/analytics":
            try:
                self._send_json(200, build_analytics_live(load_config()))
            except Exception as e:
                self._send_json(500, {"error": str(e)})
        elif path == "/api/social":
            try:
                self._send_json(200, build_social_live(load_config()))
            except Exception as e:
                self._send_json(500, {"error": str(e)})
        elif path == "/api/conversations":
            try:
                self._send_json(200, build_conversations_live(load_config()))
            except Exception as e:
                self._send_json(500, {"error": str(e)})
        elif path.startswith("/vendor/"):
            self._handle_vendor_file()
        else:
            self._send_json(404, {"error": "not found"})

    def _handle_vendor_file(self):
        name = self.path[len("/vendor/"):]
        # Reject traversal/absolute paths -- only flat filenames under VENDOR_DIR are servable.
        if not name or "/" in name or "\\" in name or name in (".", ".."):
            self._send_json(404, {"error": "not found"})
            return
        ext = os.path.splitext(name)[1]
        content_type = VENDOR_CONTENT_TYPES.get(ext)
        if not content_type:
            self._send_json(404, {"error": "not found"})
            return
        self._send_file(os.path.join(VENDOR_DIR, name), content_type)

    def do_POST(self):
        if self.path == "/chat":
            self._handle_chat()
        elif self.path == "/remember":
            self._handle_remember()
        elif self.path == "/speak":
            self._handle_speak()
        elif self.path == "/content/kill":
            self._handle_content_kill()
        elif self.path == "/content/approve":
            self._handle_content_review("approved")
        elif self.path == "/content/reject":
            self._handle_content_review("rejected")
        elif self.path == "/agent/kill":
            self._handle_agent_kill()
        elif self.path == "/agent/resume":
            self._handle_agent_resume()
        elif self.path == "/agent/kill-all":
            self._handle_agent_kill_all()
        elif self.path == "/agent/resume-all":
            self._handle_agent_resume_all()
        else:
            self._send_json(404, {"error": "not found"})

    def _handle_content_kill(self):
        try:
            body = self._read_json_body()
            job_id = (body.get("job_id") or "").strip()
            if not job_id:
                self._send_json(400, {"error": "job_id is required"})
                return
            found = False
            for job in CONTENT_JOBS:
                if job["id"] == job_id:
                    job["status"] = "Failed"
                    found = True
                    break
            if not found:
                self._send_json(404, {"error": f"no job with id {job_id}"})
                return
            self._send_json(200, {"ok": True})
        except Exception as e:
            self._send_json(500, {"error": str(e)})

    def _handle_content_review(self, new_status):
        try:
            body = self._read_json_body()
            item_id = (body.get("id") or "").strip()
            if not item_id:
                self._send_json(400, {"error": "id is required"})
                return
            found = False
            for item in CONTENT_QUEUE:
                if item["id"] == item_id:
                    item["status"] = new_status
                    found = True
                    break
            if not found:
                self._send_json(404, {"error": f"no queue item with id {item_id}"})
                return
            self._send_json(200, {"ok": True})
        except Exception as e:
            self._send_json(500, {"error": str(e)})

    def _handle_agent_kill(self):
        try:
            body = self._read_json_body()
            name = (body.get("name") or "").strip()
            if not name:
                self._send_json(400, {"error": "name is required"})
                return
            killed_at = _iso(datetime.now(timezone.utc))
            AGENT_KILL_STATE[name] = killed_at
            self._send_json(200, {"ok": True, "killed_at": killed_at})
        except Exception as e:
            self._send_json(500, {"error": str(e)})

    def _handle_agent_resume(self):
        try:
            body = self._read_json_body()
            name = (body.get("name") or "").strip()
            if not name:
                self._send_json(400, {"error": "name is required"})
                return
            AGENT_KILL_STATE.pop(name, None)
            self._send_json(200, {"ok": True})
        except Exception as e:
            self._send_json(500, {"error": str(e)})

    def _handle_agent_kill_all(self):
        try:
            agents = load_agents()
            killed_at = _iso(datetime.now(timezone.utc))
            for a in agents:
                AGENT_KILL_STATE[a["label"]] = killed_at
            self._send_json(200, {"ok": True, "count": len(agents)})
        except Exception as e:
            self._send_json(500, {"error": str(e)})

    def _handle_agent_resume_all(self):
        try:
            count = len(AGENT_KILL_STATE)
            AGENT_KILL_STATE.clear()
            self._send_json(200, {"ok": True, "count": count})
        except Exception as e:
            self._send_json(500, {"error": str(e)})

    def _handle_voices(self):
        try:
            config = load_config()
            api_key = (config.get("elevenlabs_api_key") or "").strip()
            self._send_json(200, {
                "browser_voices": BROWSER_VOICES,
                "elevenlabs_voices": ELEVENLABS_VOICES,
                "elevenlabs_available": bool(api_key),
            })
        except Exception as e:
            self._send_json(500, {"error": str(e)})

    def _handle_speak(self):
        try:
            body = self._read_json_body()
            text = (body.get("text") or "").strip()
            voice_id = (body.get("voice_id") or "").strip()
            backend = (body.get("backend") or "browser").strip().lower()

            if not text:
                self._send_json(400, {"error": "text is required"})
                return

            if backend == "browser":
                self._send_json(200, {"browser": True})
                return

            if backend != "elevenlabs":
                self._send_json(400, {"error": f"unknown backend: {backend}"})
                return

            config = load_config()
            api_key = (config.get("elevenlabs_api_key") or "").strip()
            if not api_key:
                self._send_json(400, {"error": "No ElevenLabs key configured"})
                return
            try:
                api_key.encode("latin-1")
            except UnicodeEncodeError:
                self._send_json(400, {"error": "elevenlabs_api_key has invalid characters in it"})
                return

            if not voice_id:
                self._send_json(400, {"error": "voice_id is required for the elevenlabs backend"})
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
            sys.stderr.write("EMG-JARVIS: /chat handler crashed:\n")
            traceback.print_exc(file=sys.stderr)
            self._send_json(500, {
                "error": str(e),
                "answer": f"Something broke on the server side, sir: {e}",
            })

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
