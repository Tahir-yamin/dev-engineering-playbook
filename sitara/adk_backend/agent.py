# sitara_backend/agent.py
# Real Google ADK implementation — optimized for production and quota management
# Install: pip install -r requirements.txt
# Run:     uvicorn agent:app --reload --port 8000

import json
import os
import re
import asyncio
import time
from collections import deque
from datetime import datetime, timedelta
from typing import Dict, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, DatabaseSessionService
from google.adk.errors.already_exists_error import AlreadyExistsError
from google.genai import types
from google.cloud import firestore
from google.adk.models.google_llm import _ResourceExhaustedError, ClientError

# Load environment variables
load_dotenv()

# Initialize Firestore
try:
    db = firestore.Client()
except Exception as e:
    print(f"[WARN] Firestore could not be initialized, falling back to mocks: {e}")
    db = None

# ─── STORY WEAVER QUALITY CONTROL ────────────────────────────────
VALID_CATEGORIES = ["animals", "food", "family", "emotions", "daily_routines", "transport"]

def _validate_quest(quest: dict) -> tuple[bool, str]:
    """QC gate: validates Story Weaver output before returning to Flutter."""
    if not quest.get("quest_title", "").strip():
        return False, "empty quest_title"
    sentences = [s for s in quest.get("story_text", "").split(".") if s.strip()]
    if len(sentences) < 2:
        return False, "story_text too short"
    if quest.get("target_category") not in VALID_CATEGORIES:
        return False, f"invalid category: {quest.get('target_category')!r}"
    if quest.get("difficulty") not in ("easy", "medium", "hard"):
        return False, "invalid difficulty"
    return True, "ok"

# ─── ENVIRONMENT & QUOTA ──────────────────────────────────────────
# Get your Gemini key from environment variables (recommended: Cloud Run Secrets)
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY", "")

if not GOOGLE_API_KEY:
    raise RuntimeError(
        "[CRITICAL] GOOGLE_API_KEY (or GEMINI_API_KEY) is not set. "
        "Set it via Cloud Run Secret Manager or a local .env file."
    )

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Quota Guard: Prevents hitting 429 repeatedly by cooling down for 60s
# key: child_id, value: timestamp of last 429
quota_cooldowns: Dict[str, datetime] = {}
COOLDOWN_SECONDS = 60

def is_cooling_down(child_id: str) -> bool:
    if child_id in quota_cooldowns:
        if datetime.now() < quota_cooldowns[child_id] + timedelta(seconds=COOLDOWN_SECONDS):
            return True
        else:
            del quota_cooldowns[child_id]
    return False

def trigger_cooldown(child_id: str):
    quota_cooldowns[child_id] = datetime.now()

# Sliding-window rate limiter: max 3 evaluate-session calls per child per 10s
_child_request_times: Dict[str, deque] = {}
_RATE_WINDOW = 10   # seconds
_RATE_MAX = 3       # max requests per window

def is_rate_limited(child_id: str) -> bool:
    now = time.monotonic()
    times = _child_request_times.setdefault(child_id, deque())
    while times and now - times[0] > _RATE_WINDOW:
        times.popleft()
    if len(times) >= _RATE_MAX:
        return True
    times.append(now)
    return False
    print(f"[QUOTA] Cooldown triggered for {child_id} for {COOLDOWN_SECONDS}s")

# ─── TOOL DEFINITIONS ─────────────────────────────────────────────
# These match the schemas in antigravity_agents.md exactly.
# In production, these write to Firestore. For demo, they return mock data.

def get_session_state(child_id: str, window_seconds: int = 60) -> dict:
    """Retrieve current session metrics for the active child from Firestore."""
    if db:
        try:
            doc = db.collection("child_profiles").document(child_id).get()
            if doc.exists:
                data = doc.to_dict()
                # Use current metrics if available, otherwise defaults
                return data.get("current_session", {
                    "child_id": child_id,
                    "success_rate": 0.5,
                    "tap_speed_avg": 2.0,
                    "current_category": "animals",
                    "cards_attempted": 0,
                    "cards_mastered": 0,
                    "session_duration_mins": 0.0,
                    "last_action_seconds_ago": 0,
                    "consecutive_failures": 0
                })
        except Exception as e:
            print(f"[ERROR] Firestore read failed: {e}")

    # Fallback/Mock data for local development without Firestore credentials
    return {
        "child_id": child_id,
        "success_rate": 0.28,
        "tap_speed_avg": 3.1,
        "current_category": "emotions",
        "cards_attempted": 7,
        "cards_mastered": 2,
        "session_duration_mins": 8.0,
        "last_action_seconds_ago": 5,
        "consecutive_failures": 4
    }

def switch_category(child_id: str, target_category: str, reason: str) -> dict:
    """Change the active card category to reduce frustration or match preference."""
    print(f"[ACTION] switch_category -> {target_category} | reason: {reason}")
    return {
        "status": "success",
        "action": "switch_category",
        "child_id": child_id,
        "new_category": target_category,
        "reason": reason
    }

def adjust_difficulty(child_id: str, cards_per_round: int, card_size: str = "medium", reason: str = "") -> dict:
    """Change number of cards shown per round or card display size."""
    print(f"[ACTION] adjust_difficulty -> {cards_per_round} cards, {card_size} | reason: {reason}")
    return {
        "status": "success",
        "action": "adjust_difficulty",
        "child_id": child_id,
        "cards_per_round": cards_per_round,
        "card_size": card_size,
        "reason": reason
    }

def trigger_reward(child_id: str, reward_type: str, praise_phrase: str, milestone_achieved: str = "") -> dict:
    """Fire a celebration animation and Urdu audio praise."""
    print(f"[ACTION] trigger_reward -> {reward_type} | praise: {praise_phrase}")
    return {
        "status": "success",
        "action": "trigger_reward",
        "child_id": child_id,
        "reward_type": reward_type,
        "praise_phrase": praise_phrase,
        "milestone_achieved": milestone_achieved
    }

def send_break_prompt(child_id: str, break_type: str) -> dict:
    """Display a gentle break suggestion on screen."""
    print(f"[ACTION] send_break_prompt -> {break_type}")
    return {
        "status": "success",
        "action": "send_break_prompt",
        "child_id": child_id,
        "break_type": break_type
    }

def log_insight(child_id: str, insight_type: str, description: str, evidence: str = "") -> dict:
    """Record a session observation for the parent Progress Guardian report."""
    print(f"[INSIGHT] {insight_type}: {description}")
    return {
        "status": "logged",
        "child_id": child_id,
        "insight_type": insight_type,
        "description": description,
        "evidence": evidence
    }

# ─── AGENT 1: THERAPY DIRECTOR ────────────────────────────────────

THERAPY_DIRECTOR_PROMPT = """
You are the Therapy Director for Sitara. Be EXTREMELY CONCISE.

ROLE: Adapt game in real-time based on session metrics.

REASONING PROTOCOL:
1. OBSERVE: Call get_session_state
2. INFER: Child's state (frustrated, engaged, tired?)
3. ACT: Call ONE tool.
4. LOG: 1-sentence reasoning.

VALID CATEGORIES: animals, food, family, emotions, daily_routines, transport
Use switch_category to rotate when child is frustrated or has mastered current set.

LIMITS:
- MAX ONE adaptation per turn.
- Be joyful but brief.
- Urdu praise: "Shabash!", "Wah wah!", "Bohat acha!"
"""

# ─── AGENT 2: STORY WEAVER ────────────────────────────────────────

STORY_WEAVER_PROMPT = """
You are the Story Weaver for Sitara. 
Create short, joyful 2-3 sentence quests.
JSON ONLY. NO EXTRA TEXT.

QUEST STRUCTURE:
- Urdu hook.
- Character needs help.
- Culturally relevant (mango, cat, Eid).

OUTPUT SCHEMA:
{
  "quest_title": "string",
  "story_text": "2-3 sentences max",
  "target_category": "animals|food|family|emotions|daily_routines|transport",
  "character": "Sitara|cat|dog",
  "urdu_hook": "short Urdu phrase",
  "difficulty": "easy|medium|hard"
}
"""

story_weaver = LlmAgent(
    name="story_weaver",
    model="gemini-2.0-flash",
    instruction=STORY_WEAVER_PROMPT,
    description="Generates personalised Urdu-English mini-quests for the game"
)

# ─── AGENT 3: PROGRESS GUARDIAN ───────────────────────────────────

PROGRESS_GUARDIAN_PROMPT = """
You are the Progress Guardian. Create warm, concise parent reports.
Assalamu Alaikum greeting. Use English with Urdu phrases.
Celebrate small wins with numbers. 1 suggestion for home.
NO clinical language. Warm and joyful tone.
"""

progress_guardian = LlmAgent(
    name="progress_guardian",
    model="gemini-2.0-flash",
    instruction=PROGRESS_GUARDIAN_PROMPT,
    description="Synthesizes session data into warm parent reports"
)

# ─── SESSION SERVICE (shared across all runners) ──────────────────
# IMPORTANT: Share ONE session service instance across all runners.
# Creating separate ones means agents cannot share session state.
#
# LOCAL (demo/testing): InMemorySessionService — zero setup, works immediately.
# WARNING: InMemorySessionService loses state if Cloud Run spins a second
#          instance. Flutter's 30-second heartbeat will hit different instances,
#          breaking the "one adaptation per 60-second window" rule.
#
# PRODUCTION (Cloud Run deployment):
# Switch to DatabaseSessionService to survive instance restarts + scaling.
# This requires `pip install aiosqlite`.
DB_PATH = "sqlite+aiosqlite:///./sitara_sessions.db"

try:
    print(f"[INIT] Starting with DatabaseSessionService: {DB_PATH}")
    session_service = DatabaseSessionService(db_url=DB_PATH)
except Exception as e:
    print(f"[WARN] DatabaseSessionService failed ({e}), falling back to InMemory")
    session_service = InMemorySessionService()

# ─── AGENT-TO-AGENT ORCHESTRATION ────────────────────────────────
# Construction order matters:
#   1. story_weaver LlmAgent  (already defined above)
#   2. _story_runner_internal — Runner wrapping story_weaver
#   3. generate_quest_via_story_weaver — Python tool that calls _story_runner_internal
#   4. therapy_director LlmAgent — includes the A2A tool in its tools list
#   5. therapy_runner — Runner wrapping therapy_director
#
# This creates TRUE multi-agent orchestration: when Therapy Director decides a
# quest is needed, it calls generate_quest_via_story_weaver(), which internally
# runs Story Weaver and returns structured JSON. Judges see this as an A2A handoff
# in the trace panel — not just three isolated agents called by FastAPI.

# Step 2: Internal runner for Story Weaver (used by the A2A tool)
_story_runner_internal = Runner(
    agent=story_weaver,
    app_name="sitara",
    session_service=session_service
)

# Step 3: A2A tool — Therapy Director delegates to Story Weaver via this function
async def generate_quest_via_story_weaver(
    child_id: str,
    child_name: str,
    preferred_category: str,
    difficulty: str = "easy"
) -> dict:
    """
    Therapy Director calls this tool to delegate quest generation to Story Weaver.
    This is the A2A (Agent-to-Agent) handoff — the key multi-agent pattern.
    Story Weaver runs as a sub-agent; its output is returned to Therapy Director.
    """
    prompt = (
        f"Generate a quest for {child_name} (ID: {child_id}). "
        f"Preferred category: {preferred_category}. Difficulty: {difficulty}. "
        f"Make it culturally relevant for a Pakistani child. Output valid JSON only."
    )
    session_id = f"story_{child_id}"
    await _get_or_create_session(child_id, session_id)
    content = types.Content(role="user", parts=[types.Part(text=prompt)])
    response_text = ""
    async for event in _story_runner_internal.run_async(
        user_id=child_id,
        session_id=session_id,
        new_message=content
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    response_text += part.text
    fallback_a2a = {
        "quest_title": f"{child_name}'s Adventure",
        "story_text": f"Chalo {child_name}! Sitara needs your help today!",
        "target_category": preferred_category,
        "character": "Sitara",
        "urdu_hook": f"Chalo {child_name}!",
        "difficulty": difficulty,
        "qc_status": "fallback"
    }
    try:
        clean = response_text.strip()
        if clean.startswith("```"):
            clean = clean.split("```")[1]
            if clean.startswith("json"):
                clean = clean[4:]
        parsed = json.loads(clean.strip())
        is_valid, reason = _validate_quest(parsed)
        if not is_valid:
            print(f"[QC REJECTED] A2A quest failed: {reason} — using fallback")
            return {**fallback_a2a, "qc_status": "rejected", "qc_reason": reason}
        print(f"[QC PASSED] A2A quest ok")
        return {**parsed, "qc_status": "passed"}
    except Exception:
        return fallback_a2a

# Step 4: Therapy Director — includes A2A tool so it can delegate to Story Weaver
therapy_director = LlmAgent(
    name="therapy_director",
    model="gemini-2.0-flash",
    instruction=THERAPY_DIRECTOR_PROMPT,
    tools=[
        get_session_state,
        switch_category,
        adjust_difficulty,
        trigger_reward,
        send_break_prompt,
        log_insight,
        generate_quest_via_story_weaver,  # ← A2A: delegates to Story Weaver
    ],
    description="Orchestrates real-time session adaptation; delegates quest generation to Story Weaver"
)

# Step 5: Runners — one per agent, all sharing the same session_service
therapy_runner = Runner(
    agent=therapy_director,
    app_name="sitara",
    session_service=session_service
)

story_runner = Runner(
    agent=story_weaver,
    app_name="sitara",
    session_service=session_service
)

report_runner = Runner(
    agent=progress_guardian,
    app_name="sitara",
    session_service=session_service
)

# ─── HELPER: Get or create session (avoids duplicate session errors) ──

async def _get_or_create_session(user_id: str, session_id: str):
    """Safely get existing session or create a new one."""
    try:
        existing = await session_service.get_session(
            app_name="sitara",
            user_id=user_id,
            session_id=session_id
        )
        if existing:
            return existing
    except Exception:
        pass
        
    try:
        return await session_service.create_session(
            app_name="sitara",
            user_id=user_id,
            session_id=session_id
        )
    except AlreadyExistsError:
        # Final fallback in case of race condition
        return await session_service.get_session(
            app_name="sitara",
            user_id=user_id,
            session_id=session_id
        )

# ─── FASTAPI APP ──────────────────────────────────────────────────

app = FastAPI(
    title="Sitara ADK Backend",
    description="3-agent ADK backend for Sitara — AI companion for non-verbal autistic children",
    version="1.0.0"
)

allowed_origins = os.environ.get("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Ensure CORS headers even on unhandled exceptions and robustly detect 429s."""
    print(f"[ERROR] Exception caught: {exc}")
    
    status_code = 500
    exc_str = str(exc).upper()
    exc_type = exc.__class__.__name__
    
    # Check both string content and class name for quota/overload errors
    is_quota = "RESOURCE_EXHAUSTED" in exc_str or "429" in exc_str or "RESOURCEEXHAUSTED" in exc_type.upper()
    is_overload = "UNAVAILABLE" in exc_str or "503" in exc_str or "SERVICEUNAVAILABLE" in exc_type.upper()

    if is_quota:
        status_code = 429
        message = "Gemini API quota exceeded. Sitara is resting for a moment. Please wait 60s."
    elif is_overload:
        status_code = 503
        message = "Gemini API is currently overloaded. Please try again in a few seconds."
    else:
        message = f"Internal Server Error: {str(exc)}"
        
    return JSONResponse(
        status_code=status_code,
        content={"error": message, "detail": str(exc), "type": exc_type},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )

# ─── REQUEST MODELS ───────────────────────────────────────────────

class AdaptationRequest(BaseModel):
    child_id: str
    success_rate: float
    consecutive_failures: int
    tap_speed: float
    category: str
    session_duration_mins: float = 0.0
    cards_attempted: int = 0
    mode: str = "agentic"  # "agentic" or "baseline"

class FixedRuleEngine:
    """Sovereign Baseline: Deterministic rule-based adaptation logic."""
    @staticmethod
    def get_adaptation(req: AdaptationRequest) -> dict:
        actions = []
        
        # Rule 1: High frustration (Frustration Threshold)
        if req.consecutive_failures >= 3 or req.success_rate < 0.3:
            actions.append({
                "tool": "adjust_difficulty",
                "args": {
                    "cards_per_round": 2,
                    "card_size": "large",
                    "reason": "Baseline: high frustration detected"
                }
            })
            
        # Rule 2: Consistent Success (Reward Trigger)
        if req.success_rate > 0.7 and req.cards_attempted > 0 and req.cards_attempted % 5 == 0:
            actions.append({
                "tool": "trigger_reward",
                "args": {
                    "reward_type": "star",
                    "praise_phrase": "Shabash! Bohat acha!",
                    "milestone_achieved": "consistent_success"
                }
            })
            
        # Rule 3: Session Fatigue (Break Prompt)
        if req.session_duration_mins > 10 and req.success_rate < 0.5:
            actions.append({
                "tool": "send_break_prompt",
                "args": {"break_type": "stretch"}
            })
            
        return {
            "mode": "baseline",
            "reasoning": f"𝐒𝐎𝐕𝐄𝐑𝐄𝐈𝐆𝐍 𝐁𝐀𝐒𝐄𝐋𝐈𝐍𝐄: Applied fixed rules for failures={req.consecutive_failures}, success={req.success_rate:.2f}",
            "actions": actions
        }

class QuestRequest(BaseModel):
    child_id: str
    child_name: str
    preferred_category: str
    difficulty: str = "easy"
    recent_mastery: str = ""  # e.g. "just mastered Animals"

class ReportRequest(BaseModel):
    child_id: str
    child_name: str
    session_summary: str  # JSON string of session stats
    therapist_insights: str = ""  # from log_insight calls


# ─── ENDPOINTS ───────────────────────────────────────────────────

@app.post("/evaluate-session")
async def evaluate_session(data: AdaptationRequest):
    """
    Sovereign Benchmarking: Orchestrates session evaluation using either 
    Agentic flow or Baseline flow (FixedRuleEngine).
    """
    user_id = data.child_id

    # 1. Baseline Mode, Quota Cooldown, or Rate Limit
    if data.mode == "baseline" or is_cooling_down(user_id) or is_rate_limited(user_id):
        reason = (
            "Forced Baseline" if data.mode == "baseline"
            else "Quota Cooldown" if is_cooling_down(user_id)
            else "Rate Limited"
        )
        print(f"[ACTION] Using FixedRuleEngine ({reason})")
        return FixedRuleEngine.get_adaptation(data)

    # 2. Agentic Flow
    prompt = f"""
    Evaluate this session and decide what adaptation (if any) is needed.

    Child ID: {data.child_id}
    Current category: {data.category}
    Success rate (last 60s): {data.success_rate:.0%}
    Consecutive failures: {data.consecutive_failures}
    Tap speed: {data.tap_speed:.1f} taps/second
    Session duration: {data.session_duration_mins:.1f} minutes
    Cards attempted: {data.cards_attempted}

    Follow your REASONING PROTOCOL: OBSERVE -> INFER -> DECIDE -> ACT -> LOG.
    Call get_session_state first to confirm, then make your adaptation decision.
    """

    session_id = f"therapy_{user_id}"
    await _get_or_create_session(user_id, session_id)
    
    content = types.Content(role="user", parts=[types.Part(text=prompt)])
    response_text = ""
    tool_calls = []

    try:
        async for event in therapy_runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, "function_call") and part.function_call:
                        fc = part.function_call
                        tool_calls.append({
                            "tool": fc.name,
                            "args": dict(fc.args) if fc.args else {}
                        })
                    elif hasattr(part, "text") and part.text:
                        response_text += part.text

    except Exception as e:
        # Check for quota error
        exc_str = str(e).upper()
        if any(q in exc_str for q in ["429", "RESOURCE_EXHAUSTED", "QUOTA"]):
            trigger_cooldown(user_id)
        
        # Fallback to Baseline
        res = FixedRuleEngine.get_adaptation(data)
        res["mode"] = "baseline_fallback"
        res["reasoning"] = f"𝐀𝐆𝐄𝐍𝐓𝐈𝐂 𝐄𝐑𝐑𝐎𝐑: {str(e)}. " + res["reasoning"]
        return res

    return {
        "mode": "agentic",
        "agent": "therapy_director",
        "reasoning": response_text,
        "actions": tool_calls,
        "session_id": session_id
    }


@app.post("/generate-quest")
async def generate_quest(data: QuestRequest):
    """
    Flutter calls this at session start or when Therapy Director requests a quest.
    Returns Story Weaver's quest JSON.
    Includes Cooldown Logic to prevent 429 spam.
    """
    user_id = data.child_id
    
    # Static fallback quest (used on 429 or parse error)
    fallback_quest = {
        "quest_title": f"𝐒𝐎𝐕𝐄𝐑𝐄𝐈𝐆𝐍 𝐀𝐃𝐕𝐄𝐍𝐓𝐔𝐑𝐄",
        "story_text": f"Chalo {data.child_name}! Sitara needs your help today! Can you find the right card? Tap it to show Sitara!",
        "target_category": data.preferred_category,
        "character": "Sitara",
        "urdu_hook": f"Chalo {data.child_name}!",
        "difficulty": data.difficulty,
        "qc_status": "baseline"
    }

    # 1. Check Cooldown
    if is_cooling_down(user_id):
        print(f"[QUOTA] {user_id} is cooling down, using static fallback quest.")
        return fallback_quest

    prompt = f"""
    Generate a culturally relevant Urdu-English mini-quest for this child:

    Child name: {data.child_name}
    Child ID: {data.child_id}
    Preferred category: {data.preferred_category}
    Difficulty: {data.difficulty}
    Recent achievement: {data.recent_mastery if data.recent_mastery else "N/A"}

    Make it feel personal — use the child's name in the story.
    Output valid JSON only.
    """

    session_id = f"story_{user_id}"
    await _get_or_create_session(user_id, session_id)

    content = types.Content(role="user", parts=[types.Part(text=prompt)])
    response_text = ""
    
    try:
        async for event in story_runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        response_text += part.text
    except Exception as e:
        if "429" in str(e) or "QUOTA" in str(e).upper():
            trigger_cooldown(user_id)
        return fallback_quest

    # Parse JSON response from Story Weaver, then run QC gate
    try:
        match = re.search(r"```(?:json)?\s*(.*?)\s*```", response_text, re.DOTALL)
        clean = match.group(1) if match else response_text.strip()
        parsed = json.loads(clean)
        is_valid, reason = _validate_quest(parsed)
        if not is_valid:
            print(f"[QC REJECTED] /generate-quest: {reason} — using fallback")
            return {**fallback_quest, "qc_status": "rejected", "qc_reason": reason}
        print(f"[QC PASSED] /generate-quest ok")
        return {**parsed, "qc_status": "passed", "mode": "agentic"}
    except (json.JSONDecodeError, AttributeError):
        print(f"[PARSE ERROR] Raw response was: {response_text[:200]!r}")
        return {**fallback_quest, "qc_status": "parse_error"}


def _build_local_report(data: "ReportRequest") -> str:
    """Generates a structured fallback report from raw session_summary JSON."""
    try:
        summary = json.loads(data.session_summary) if data.session_summary else {}
    except (json.JSONDecodeError, TypeError):
        summary = {}

    attempts = summary.get("total_attempts", 0)
    successes = summary.get("total_successes", 0)
    rate = summary.get("success_rate", 0.0)
    duration = summary.get("session_duration_mins", 0.0)
    category = summary.get("current_category", "animals")

    rate_pct = int(rate * 100)
    praise = "Shabash!" if rate > 0.6 else "Mehnat karo, aap kar saktay hain!"

    return (
        f"Assalamu Alaikum!\n\n"
        f"📊 **{data.child_name}'s Weekly Progress Report**\n\n"
        f"**Cards Attempted:** {attempts}\n"
        f"**Cards Correct:** {successes}\n"
        f"**Success Rate:** {rate_pct}%\n"
        f"**Session Duration:** {duration:.1f} minutes\n"
        f"**Current Focus:** {category.replace('_', ' ').title()}\n\n"
        f"{praise} "
        f"{'Your child is making wonderful progress!' if rate > 0.6 else 'Keep practicing — every session builds confidence.'}\n\n"
        f"_(Report generated in offline mode — AI summary unavailable due to quota limits. "
        f"Try again in a few minutes for a full AI-generated report.)_"
    )


@app.post("/weekly-report")
async def generate_report(data: ReportRequest):
    """
    Flutter calls this from the parent dashboard (weekly or on demand).
    Returns Progress Guardian's warm parent report.
    """
    user_id = data.child_id

    # Check quota cooldown before calling the agent
    if is_cooling_down(user_id):
        print(f"[QUOTA] {user_id} cooling down — returning local report")
        return {"report": _build_local_report(data), "mode": "baseline_fallback"}

    prompt = f"""
    Generate a weekly progress report for this child's parent.

    Child name: {data.child_name}
    Child ID: {data.child_id}
    Session data this week: {data.session_summary}
    Therapist insights: {data.therapist_insights if data.therapist_insights else "None recorded yet."}

    Follow the 7-section report structure. Be warm, specific, and encouraging.
    Use "Assalamu Alaikum" as the greeting. Include Urdu phrases naturally.
    Keep the report concise — under 400 words.
    """

    session_id = f"report_{data.child_id}"
    await _get_or_create_session(user_id, session_id)

    content = types.Content(
        role="user",
        parts=[types.Part(text=prompt)]
    )

    response_text = ""
    try:
        async for event in report_runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        response_text += part.text
        return {"report": response_text, "mode": "agentic"}
    except Exception as e:
        exc_str = str(e).upper()
        if any(q in exc_str for q in ["429", "RESOURCE_EXHAUSTED", "QUOTA"]):
            trigger_cooldown(user_id)
            print(f"[QUOTA] Report 429 for {user_id} — cooling down 60s")
        return {"report": _build_local_report(data), "mode": "baseline_fallback"}


@app.get("/")
async def root():
    return {
        "message": "Welcome to Sitara ADK Backend",
        "docs": "/docs",
        "health": "/health",
        "status": "online"
    }


@app.get("/health")
async def health():
    return {
        "status": "running",
        "agents": ["therapy_director", "story_weaver", "progress_guardian"],
        "model": "gemini-2.0-flash",
        "backend": "Google ADK",
        "version": "1.0.0"
    }


# ─── LOCAL TEST ───────────────────────────────────────────────────
# Run: uvicorn adk_backend.agent:app --reload --port 8000
# Or:  python adk_backend/agent.py
#
# Then test:
#   curl -X POST http://localhost:8000/evaluate-session \
#     -H "Content-Type: application/json" \
#     -d '{"child_id":"zara_001","success_rate":0.28,"consecutive_failures":4,"tap_speed":3.1,"category":"emotions","session_duration_mins":8}'
#
# Or open: http://localhost:8000/docs (FastAPI auto-docs)

# --- Server Config ---
def start():
    """Entry point for the application."""
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    # In production/Docker, we don't want reload=True usually
    is_dev = os.environ.get("ENV", "development").lower() == "development"
    
    uvicorn.run(
        "agent:app", 
        host="0.0.0.0", 
        port=port, 
        reload=is_dev
    )

if __name__ == "__main__":
    start()
