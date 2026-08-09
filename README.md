# EMG-JARVIS

Empire Media Group's autonomous agent command system: an 85-agent fleet
(SUPER_AGENTS, VOICE_AI, CONVERSATION_AI) visualized as a live 3D glowing
mesh (Three.js), with a JARVIS-style chat/voice interface backed by Claude,
a swappable brain model, ElevenLabs-quality voice, and a live GoHighLevel
data bridge.

## Setup

1. **Install Python 3** (3.8+). No external packages are required — both
   `server.py` and `ghl_bridge.py` use only the Python standard library.

   ```bash
   python3 --version
   ```

2. **Add your Anthropic API key.** Open `config.json` and replace
   `PUT-YOUR-KEY-HERE` with a real key:

   ```json
   {
     "anthropic_api_key": "sk-ant-...",
     "model": "claude-opus-4-8",
     "port": 4700,
     "boss_name": "Able",
     "ghl_token": "",
     "elevenlabs_api_key": "",
     "elevenlabs_voice_id": "",
     "voice_backend": "browser"
   }
   ```

   You can also change `boss_name` (used in JARVIS's greetings) and `port`.

3. **Run the server:**

   ```bash
   python3 server.py
   ```

   This regenerates `viewer/graph-data.js` from `agents.json` on every
   startup (via `build.py`), then starts the server on `http://localhost:4700`.

4. **Open Chrome** (recommended for the Web Speech API) and go to:

   ```
   http://localhost:4700
   ```

   Allow microphone access if prompted, and wait for the boot sequence to
   finish — JARVIS will greet you out loud once the agent mesh has loaded.

## Regenerating the graph manually

If you edit `agents.json` directly, you can rebuild the viewer's graph data
without restarting the server:

```bash
python3 build.py
```

This reads `agents.json` and writes `viewer/graph-data.js`.

## Using the interface

- **Search** — type an agent name in the top-left search box and press
  Enter to fly the camera to it.
- **Click any node** — the sphere scales up and glows brighter, and the
  side panel opens with the agent's name, type, status, tool count,
  description, and linked agents (click a linked agent to jump straight
  to it).
- **Chat bar** — type a question and hit send (or Enter). JARVIS answers
  using the full agent roster as context, speaks the first sentence aloud,
  and flies the camera to any agents it mentions.
- **Mic button** — click to speak your question instead of typing (uses
  the browser's Web Speech API).
- **Escape** — closes the side panel, settings panel, and the chat answer
  overlay.
- **Gear icon** (top-right) — opens Settings: brain model, voice, voice
  type, GHL bridge status, and About.

### Voice / chat commands to try

- "How many agents are online right now?"
- "Tell me about CLOSE COMMANDER."
- "Which agents handle video production?"
- "What does KAREN do?"
- "Show me the reactivation pipeline."
- "remember Follow up with the Meridian account next week" — saves a
  timestamped note to `captures/` and adds a gold star node to the mesh.
- "switch to sonnet" / "use haiku" / "switch to fable 5" — swaps the
  active Claude model mid-conversation; JARVIS confirms out loud.

## v2: Voice selection & ElevenLabs

Open **Settings** (gear icon) → **Voice**. The dropdown lists every voice
your browser's Speech Synthesis API exposes, grouped **Female** / **Male**
(best-effort, since browsers don't expose gender directly) / **Other**,
plus an **ElevenLabs** group with six presets:

| Voice  | Gender | Tone    |
|--------|--------|---------|
| Rachel | female | calm    |
| Domi   | female | strong  |
| Bella  | female | warm    |
| Adam   | male   | deep    |
| Antoni | male   | warm    |
| Josh   | male   | natural |

Click **Preview** to hear "Good evening, sir. Empire Media Group OS
online." in the selected voice. Your choice is saved to `localStorage` and
reused on every visit.

### Enabling ElevenLabs

1. Get an API key from [elevenlabs.io](https://elevenlabs.io) and put it
   in `config.json`'s `elevenlabs_api_key`.
2. Optionally set a default `elevenlabs_voice_id` (falls back to Rachel's
   ID if left blank and ElevenLabs is selected).
3. Restart `server.py`. The ElevenLabs presets become selectable in the
   Voice dropdown (they're greyed out otherwise) and the **Voice Type**
   toggle in Settings switches between **Browser** and **ElevenLabs**.
4. All speech (boot greeting, chat replies, "remember" confirmations,
   Preview) now routes through `POST /tts` on the local server, which
   proxies to `https://api.elevenlabs.io/v1/text-to-speech/{voice_id}` —
   your API key never leaves the server.

If `elevenlabs_api_key` is blank, the app transparently falls back to the
browser's built-in speech synthesis.

## v2: Model switcher

Open **Settings** → **Brain Model** to pick which Claude model answers
your questions:

| Option              | Label                     |
|---------------------|---------------------------|
| `claude-opus-4-8`   | Opus 4 — Smartest (default) |
| `claude-sonnet-4-5` | Sonnet 4.5 — Balanced      |
| `claude-haiku-3-5`  | Haiku — Fastest            |
| `claude-fable-5`    | Fable 5 — Creative         |

The choice is saved to `localStorage` and sent as `model_override` with
every `/chat` request; `server.py` uses it in place of the `model` field
in `config.json` whenever it's non-empty.

You can also switch models by voice or text mid-conversation — say or
type **"switch to sonnet"**, **"use haiku"**, **"switch to opus 4"**, or
**"use fable 5"**. JARVIS detects the command server-side, switches the
session's active model, and replies with a spoken confirmation instead of
answering as a normal chat turn.

## v2: GoHighLevel live data bridge

`ghl_bridge.py` is a standalone server (port `8090` by default) that pulls
live calendar and pipeline data from GoHighLevel using a **Private
Integration Token** and derives a status (`active` / `idle` / `standby`)
for each agent via `agent-map.json`.

### Setup

1. In GoHighLevel, create a Private Integration Token with read access to
   calendars/appointments and opportunities.
2. Add it to `config.json`:

   ```json
   {
     "ghl_token": "pit-...",
     "ghl_location_id": "your-location-id"
   }
   ```

   (`ghl_location_id` is optional — if omitted, the bridge tries to
   auto-discover the first location visible to your token.)

3. Run the bridge alongside the main server:

   ```bash
   python3 ghl_bridge.py
   ```

4. In the Settings panel, **GHL Bridge** shows **Connected** once the
   bridge is reachable and configured, or **Standby** / **Unreachable**
   otherwise.

If `ghl_token` is left blank, every agent reports `standby` and a gold
banner appears under the status bar: *"Connect GHL: add ghl_token to
config.json."*

### Endpoints

- `GET /ghl/status` → `{"configured": bool, "agents": {AGENT_NAME: {status, tasks, last}}}`
- `GET /ghl/panels` → `{"appointments": [...], "pipelines": [...], "todos": [...]}`
- `POST /ghl/push` → body `{"agent": "...", "status": "...", "tasks": N, "last": "..."}`
  lets any external process push a manual status override for an agent,
  taking priority over the derived GHL signal.

`agent-map.json` maps each of the 85 agent labels to a GHL signal type
(`calendar`, `pipeline`, or `none`) and the keyword(s) used to match
GHL appointment titles / opportunity names to that agent.

## Project structure

```
agents.json          # source of truth: all 85 agents
agent-map.json        # agent name -> GHL calendar/pipeline signal mapping
build.py              # agents.json -> viewer/graph-data.js
server.py             # HTTP server: viewer, /status, /chat, /remember, /tts, /voice-config
ghl_bridge.py          # standalone GHL live-data bridge (port 8090)
config.json            # API keys, model, port, boss name, GHL/ElevenLabs config
viewer/
  index.html          # Three.js 3D mesh viewer + chat/voice UI + settings panel
  graph-data.js        # generated by build.py — do not edit by hand
captures/              # markdown notes created by "remember ..." commands
```
