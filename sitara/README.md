# ⭐ Sitara — AI Companion Game for Non-Verbal Autistic Children

> *An agentic mobile game powered by Google Antigravity that adapts in real time to help non-verbal autistic children in Pakistan communicate, learn, and thrive.*

[![Challenge](https://img.shields.io/badge/Challenge-4%3A%20Agentic%20Mobile%20Game-purple)](.)
[![Platform](https://img.shields.io/badge/Platform-Android%20(Flutter)-blue)](.)
[![AI](https://img.shields.io/badge/AI-Google%20ADK%20%2B%20Gemini%202.0%20Flash-orange)](.)
[![Hackathon](https://img.shields.io/badge/Hackathon-%23AISeekho2026-green)](.)

---

## 🎯 Problem Statement

Pakistan has approximately **350,000 children diagnosed with autism**, the majority of whom are non-verbal. Existing AAC (Augmentative and Alternative Communication) tools are:

- Designed for English-speaking Western contexts — no Urdu, no Roman Urdu
- Expensive and inaccessible in rural Pakistan
- Static flashcard boards — no real-time adaptation to child behaviour
- Reliant on camera-based emotion detection (privacy invasive, unreliable in low light)

**Sitara solves all four problems** using Google Antigravity to drive real-time multi-agent adaptation based entirely on tap behaviour — no camera, no biometrics.

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────┐
│                   Flutter App (Android)                   │
│  ┌──────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │  Game Screen │  │ Parent Dashboard│  │ Agent Trace │  │
│  │ (card grid)  │  │ (weekly report) │  │ Panel (judge│  │
│  │  30s timer   │  │ baseline toggle │  │  overlay)   │  │
│  └──────┬───────┘  └────────┬────────┘  └──────┬──────┘  │
│         │  AntigravityService (Dart)            │         │
│         │  • Event collection → POST every 30s  │         │
│         │  • Local heuristic fallback (offline) │         │
│         │  • Trace log export for judges         │         │
└─────────┼──────────────────────────────────────-┘         │
          │ HTTP / FastAPI                                   │
┌─────────▼────────────────────────────────────────────────┐
│             Google ADK — FastAPI Backend (Cloud Run)      │
│                                                          │
│  Agent 1: Therapy Director (Orchestrator)                │
│    OBSERVE → INFER → DECIDE → ACT → LOG                  │
│    Tools: get_session_state, switch_category,            │
│           adjust_difficulty, trigger_reward,             │
│           send_break_prompt, log_insight,                │
│           generate_quest_via_story_weaver [A2A]          │
│                   │ A2A delegation                        │
│  Agent 2: Story Weaver (Sub-Agent)                       │
│    Generates Urdu/English quest JSON                     │
│    QC gate validates output before returning             │
│                                                          │
│  Agent 3: Progress Guardian (Independent)                │
│    Weekly parent reports from log_insight history        │
│                                                          │
│  Sovereign Baseline (FixedRuleEngine)                    │
│    Deterministic fallback — always available             │
└──────────────────────────────────────────────────────────┘
          │
┌─────────▼──────────────────────────────────┐
│  Local Storage (shared_preferences)         │
│  • Child profiles (flutter_secure_storage)  │
│  • Session events (500-event rolling window)│
│  • Agent insights for Progress Guardian     │
└────────────────────────────────────────────┘
```

### Agent-to-Agent (A2A) Flow

The Therapy Director is the **sole orchestrator**. When it detects a milestone, it calls `generate_quest_via_story_weaver()` — a tool that internally runs the Story Weaver sub-agent and returns structured quest JSON. This is true A2A delegation, visible in the ADK trace panel.

```
Therapy Director
  │
  ├─[frustration]──► switch_category() + trigger_reward()  [direct tools]
  ├─[engagement] ──► adjust_difficulty()                   [direct tool]
  ├─[milestone]  ──► generate_quest_via_story_weaver()     [A2A → Story Weaver]
  │                        └─► returns quest JSON with QC gate
  └─[always]     ──► log_insight()                         [feeds Progress Guardian]

Progress Guardian  ← triggered independently by parent dashboard
```

---

## 🤖 Google Antigravity Usage

Antigravity (Google ADK) is the **game engine**, not a decorator. Every adaptation decision is made by an LlmAgent.

### Agent 1: Therapy Director
**Trigger:** Every 30 seconds during active session  
**Protocol:** `OBSERVE → INFER → DECIDE → ACT → LOG` (visible in trace panel)

| Signal | Threshold | Agentic Response |
|--------|-----------|-----------------|
| Consecutive failures | ≥ 3 | `switch_category` to preferred/easier |
| Tap speed | > 3 taps/sec | `adjust_difficulty` + `trigger_reward` |
| Inactivity | > 30 seconds | `send_break_prompt` |
| Session + declining success | 15+ min, < 60% | `send_break_prompt` |
| Success rate | > 80% last 10 cards | `adjust_difficulty` (increase) |
| Milestone | 5 correct in a row | `generate_quest_via_story_weaver` |

**Max one adaptation per 60-second window** to avoid overwhelming the child.

### Agent 2: Story Weaver
**Trigger:** On A2A call from Therapy Director, or direct `POST /generate-quest` at session start

**Output schema:**
```json
{
  "quest_title": "Sitara's Lost Kitten",
  "story_text": "Mubarak ho, Zara! Sitara ki billi gum ho gayi...",
  "target_category": "animals",
  "character": "Sitara",
  "urdu_hook": "Mubarak ho, Zara!",
  "difficulty": "easy",
  "qc_status": "passed"
}
```

**QC Gate:** `_validate_quest()` checks title, story length (≥ 2 sentences), valid category, and valid difficulty before returning to Flutter. Rejected quests fall back to a safe static quest.

### Agent 3: Progress Guardian
**Trigger:** Weekly or on-demand from parent dashboard (`POST /weekly-report`)  
**Output:** 7-section warm parent report — wins, preferences, gentle observations, home activity, encouragement  
**Tone rule:** Never clinical. "Zara recognised 12 new symbols!" not "Zara failed 14 items."

### Sovereign Baseline (FixedRuleEngine)
Toggle in the game AppBar (🤖 AI / 📏 Rules) switches between agentic AI and deterministic heuristics. The Parent Dashboard shows average success rate per mode — measurable performance delta.

---

## 🎮 Game Design

### Symbol Cards — 57 cards across 6 categories
| Category | Cards | Notes |
|----------|-------|-------|
| Animals | 10 | Cat, Dog, Bird, Fish, Cow, Horse, Elephant, Rabbit, Butterfly, Lion |
| Food | 10 | Mango, Roti, Rice, Water, Apple, Banana, Milk, Egg, Bread, Orange |
| Family | 7 | Mother, Father, Grandmother, Grandfather, Brother, Sister, Baby |
| Emotions | 6 | Happy, Sad, Hungry, Angry, Scared, Tired — difficulty level 2 |
| Daily Routines | 8 | Sleep, Eat, Bath, Play, Walk, Study, Brush Teeth, Pray |
| Transport | 6 | Car, Bus, Bicycle, Airplane, Boat, Motorcycle |

Images: ARASAAC pictograms (CC BY-NC-SA 4.0). Emoji fallback if image fails to load.  
Labels: Urdu script + Roman Urdu + English on every card.  
Audio: flutter_tts speaks Urdu (ur-PK if installed) then Roman Urdu then English.

### Core Loop
```
Child hears card name (Urdu + English TTS)
    → Taps the matching card from 2×6 grid
    → Correct: star reward + praise ("Shabash!")
    → Wrong: card shake animation, retry
    → Every 30s: Therapy Director evaluates and adapts
    → Every 5 correct: Story Weaver generates a mini-quest
    → Weekly: Progress Guardian writes parent report
```

### Frustration Detection (Privacy-Safe)
No camera. No biometrics. Only tap behaviour:
- **Tap speed** (taps/second) — rapid tapping = frustration
- **Consecutive failures** — 3+ = high frustration
- **Inactivity duration** — 30+ seconds = disengagement
- **Success rate trend** — declining over last 10 taps = fatigue
- **Session length + declining success** — 15+ min = fatigue

---

## 📱 Technology Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| Mobile | Flutter 3.x (Android) | Provider state management |
| AI Orchestration | Google ADK (Antigravity) | LlmAgent, Runner, A2A pattern |
| Language Model | Gemini 2.0 Flash | Fast, low-latency, cost-effective |
| Backend API | FastAPI + uvicorn | Cloud Run deployable |
| Session DB | DatabaseSessionService (SQLite/aiosqlite) | InMemory fallback for local dev |
| Local Storage | shared_preferences | Offline-first, no native deps |
| Secure Storage | flutter_secure_storage | Child profiles in Android Keystore |
| TTS | flutter_tts | ur-PK → Roman Urdu → en-US fallback chain |
| HTTP | http ^1.2.0 | 10s timeout, local fallback on failure |

---

## ⚙️ Setup & Running

### Backend (adk_backend/)

```bash
cd adk_backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

# Required environment variable
set GOOGLE_API_KEY=your_gemini_api_key_here

# Run locally
uvicorn agent:app --reload --port 8000
```

**Deploy to Cloud Run:**
```powershell
.\deploy_cloud_run.ps1   # Windows
# or
bash deploy_cloud_run.sh  # Linux/Mac
```

### Flutter App (sitara_app/)

```bash
cd sitara_app
flutter pub get
flutter run                    # Debug on connected device
flutter build apk --release    # Build APK for submission

# Point to local backend during testing:
flutter run --dart-define=BACKEND_URL=http://10.0.2.2:8000
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_API_KEY` | ✅ Yes | Gemini API key (fails at startup if missing) |
| `GEMINI_API_KEY` | Fallback | Alternative key name |
| `BACKEND_URL` | Optional | Override Cloud Run URL for local dev |

---

## 🔒 Privacy & Data

- **No camera, no microphone, no location** — frustration detected via tap behaviour only
- **Child profiles** stored in Android Keystore via `flutter_secure_storage` (encrypted at rest)
- **Session events** stored in `shared_preferences` with 500-event rolling cap
- **No PII** transmitted to backend — only anonymised metrics (success_rate, tap_speed, consecutive_failures, category)
- **Offline-first** — app works fully without internet; agent calls are enhancement-only
- No raw personal data stored server-side in demo mode (SQLite session DB contains only session IDs and event counts)

---

## 🛡️ Robustness & Edge Cases

### Quota / 429 Handling
- 60-second per-child cooldown on `ResourceExhausted` errors
- Sliding-window rate limiter: max 3 `/evaluate-session` calls per child per 10 seconds
- Both `/evaluate-session` and `/weekly-report` check cooldown before calling the LLM
- `FixedRuleEngine` provides deterministic adaptation during cooldown
- Flutter falls back to `_localFallback()` (client-side heuristics) on any API failure

### Story Weaver QC Gate
- Every quest validated: non-empty title, ≥ 2 story sentences, valid category, valid difficulty
- Rejected quests logged with reason; safe static fallback returned
- Parse errors log raw LLM response (first 200 chars) for debugging

### Network Failures
- All Flutter API calls have 10-second timeout
- `TimeoutException` and any HTTP error trigger `_localFallback()` silently
- Child never sees an error — game continues with heuristic mode

### Session Continuity
- `_get_or_create_session()` handles `AlreadyExistsError` on concurrent requests
- `DatabaseSessionService` (SQLite) persists across Cloud Run restarts

### Demonstrated Failure Scenario
During development, Gemini 2.0 Flash returned 429 errors during burst testing. The quota cooldown + `FixedRuleEngine` fallback activated automatically — the Flutter app continued without interruption, showing "📏 Rules" mode in the trace panel. Cloud Run logs (`cloud_run_logs.txt`) contain real 429 recovery sequences.

---

## 📊 Baseline Comparison

| Feature | Sovereign Baseline (Heuristic) | Antigravity Agentic |
|---------|-------------------------------|---------------------|
| Adaptation trigger | Fixed thresholds (3 failures = reduce difficulty) | Contextual reasoning (frustration + category preference + session length) |
| Quest generation | None | Personalised Urdu/English narrative per child |
| Parent report | None | 7-section warm weekly letter with specific evidence |
| Difficulty logic | Boolean (if failures > 3) | Multi-signal inference with explanation |
| Trace visibility | None | Full OBSERVE→INFER→DECIDE→ACT→LOG in UI |

**Toggle:** 🤖 AI / 📏 Rules button in AppBar switches modes live.  
**Evidence:** Parent Dashboard "Mode Comparison" card shows average session success rate per mode across recorded sessions.  
**Expected delta:** ~40% longer session duration in agentic mode vs heuristic (tap-speed saturation occurs slower when difficulty adapts intelligently).

---

## 💰 Cost & Scalability

### Per-Session Cost (Gemini 2.0 Flash, May 2026)

| Item | Value |
|------|-------|
| Input tokens per `/evaluate-session` | ~500 tokens |
| Output tokens per `/evaluate-session` | ~200 tokens |
| Calls per 10-minute session | 20 (every 30s) |
| Tokens per quest generation | ~800 input / 300 output |
| **Cost per full session** | **~$0.002** |

Pricing basis: Gemini 2.0 Flash ~$0.075/1M input, ~$0.30/1M output tokens.

### Scaling

| Scale | Sessions/day | Est. daily cost | Infrastructure |
|-------|-------------|-----------------|----------------|
| MVP (hackathon) | 50 | $0.10 | Cloud Run free tier, SQLite session DB |
| 10× growth | 500 | $1.00 | Cloud Run auto-scales, SQLite sufficient |
| 100× growth | 5,000 | $10.00 | Cloud SQL for sessions, batch Progress Guardian |
| 1,000× (national) | 50,000 | $100.00 | Regional Cloud Run, Firestore, async report queue |

### Latency
- Gemini 2.0 Flash p50 response: ~800ms
- Flutter's 30-second evaluation window absorbs this with no visible latency to the child
- Quest generation (Story Weaver): ~1.2s — triggered only on milestone, not every cycle

---

## 🌍 Pakistan-Specific Design

| Decision | Rationale |
|---------|-----------|
| Urdu + Roman Urdu + English | Pakistan's linguistic reality — parents read all three |
| Offline-first | Unreliable connectivity in many Pakistani cities |
| Cultural symbols | Mango, chai, roti, Eid, dadi — familiar and engaging |
| Android-only MVP | 95%+ of Pakistani smartphone users are on Android |
| No camera | Privacy-appropriate for conservative households |
| Urdu TTS chain | Falls back to Roman Urdu (English engine) when ur-PK voice pack not installed |

---

## 🚧 Assumptions & Limitations

### Assumptions
- Child has 1-on-1 adult supervision during sessions
- Primary caregiver can read basic Urdu or Roman Urdu
- Android device with ≥ 2GB RAM
- Internet for initial agent session; offline fallback for subsequent use

### Current Limitations (Hackathon MVP)
- No audio asset files bundled — TTS used for all speech (pre-recorded audio is post-MVP)
- Single child profile per device (multi-child is post-hackathon)
- No cloud sync — session history is device-local
- English-only app chrome UI (Urdu content on cards; full Urdu UI is post-hackathon)
- Agent traces exported as JSON from the Agent Trace Panel — not auto-submitted to a server

---

## 📂 Data Schemas

### SessionEvent (Flutter → Backend)
```json
{
  "child_id": "child_001",
  "success_rate": 0.72,
  "consecutive_failures": 1,
  "tap_speed": 1.4,
  "category": "animals",
  "session_duration_mins": 4.5,
  "cards_attempted": 12
}
```

### AdaptationResponse (Backend → Flutter)
```json
{
  "mode": "agentic",
  "reasoning": "Success rate 72%, improving. Increasing difficulty...",
  "actions": [
    {"tool": "adjust_difficulty", "args": {"cards_per_round": 6, "card_size": "medium", "reason": "..."}}
  ]
}
```

### QuestJSON (Story Weaver Output)
```json
{
  "quest_title": "Sitara's Lost Kitten",
  "story_text": "Mubarak ho, Zara! Sitara ki billi gum ho gayi...",
  "target_category": "animals",
  "character": "Sitara",
  "urdu_hook": "Mubarak ho, Zara!",
  "difficulty": "easy",
  "qc_status": "passed"
}
```

---

## 📋 Submission Checklist

- [x] Working Android APK (Flutter, tested on Android 10+)
- [x] Demo video ~3 minutes (see `demo_script_readme.md`)
- [x] Antigravity trace/logs — export via Agent Trace Panel → "Export Traces" button
- [x] Architecture map — see Architecture section above + `Project_Architecture_Blueprint.md`
- [x] Agent definitions + tool schemas — `antigravity_agents.md`
- [x] README with architecture, schemas, tools, setup, privacy, cost, scalability, baseline, limitations
- [x] Baseline comparison — Sovereign Benchmarking toggle + Parent Dashboard mode stats
- [x] Robustness evidence — quota 429 recovery in `cloud_run_logs.txt`; offline fallback always active
- [x] Cost/latency estimate — see Cost & Scalability section above

---

## 🔓 Open Source Attribution

| Resource | License | Usage |
|---------|---------|-------|
| [ARASAAC Pictograms](https://arasaac.org) | CC BY-NC-SA 4.0 | Symbol card images |
| [flutter_tts](https://pub.dev/packages/flutter_tts) | MIT | Urdu + English TTS |
| [flutter_secure_storage](https://pub.dev/packages/flutter_secure_storage) | MIT | Encrypted child profiles |
| [Google ADK](https://google.github.io/adk-docs/) | Apache 2.0 | Agent orchestration framework |
| [Gemini 2.0 Flash](https://deepmind.google/technologies/gemini/) | Commercial | Language model |

---

## 👥 Team

| Role | Name | Contact |
|------|------|---------|
| Founder / Lead | Tahir Yamin | tahiryamin2050@gmail.com |

**Hackathon:** #AISeekho2026 — Challenge 4: Agentic Mobile Game  
**Submission deadline:** May 20, 2026

---

*"Sitara means 'star' in Urdu. Every child is one."*

**Built with ❤️ for Pakistan | Powered by Google Antigravity + Gemini 2.0 Flash**
