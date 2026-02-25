# Operator Automation: Cron & Mobile Commands

**Purpose**: Automating the routine intelligence, reporting, and maintenance work of "The Operator."
**Source**: The OpenClaw Operator's Playbook (Section 4)

---

## 📱 **Skill #1: Mobile Command (Telegram)**

**Setup**: Once the Telegram MCP or bot bridge is connected, apply this configuration to allow for remote delegation.

**Deployment Prompt**:
```markdown
You are available via Telegram. Treat Telegram messages with the same priority as direct session commands.

When I send a task via Telegram:
- Confirm receipt immediately.
- Begin the task without waiting for further instruction.
- Deliver results directly back to Telegram.
- Keep responses mobile-friendly (short paragraphs, bullet points).
```

---

## ⏰ **Skill #2: 7:00 AM Morning Briefing**

**Setup**: Configures a proactive daily intelligence report.

**Cron Schedule**: `0 7 * * *`  
**Agent**: `chiefofstaff`

**Deployment Prompt**:
```markdown
Review yesterday's memory log and today's context. 
Generate a morning briefing with exactly these four sections:

1. YESTERDAY'S WINS — what was completed or moved forward.
2. TODAY'S TOP 3 — the three highest-priority tasks for today.
3. PENDING DECISIONS — anything waiting for my input or approval.
4. GROWTH IDEA — one actionable idea based on recent activity or trends.

Deliver to Telegram. Keep total length under 300 words. 
Use bullet points. No preamble. Start with "Morning Briefing — [Date]"
```

---

## 🌑 **Skill #3: Midnight Daily Tracker**

**Setup**: Automated logging of everything done during the day to Notion or a local tracking file.

**Cron Schedule**: `0 0 * * *`  
**Agent**: `daily-tracker`

**Deployment Prompt**:
```markdown
Review today's full session log. Extract and organize:
- COMPLETED: tasks finished today.
- DECISIONS: choices made and reasoning.
- BLOCKERS: anything that slowed progress.
- INSIGHTS: patterns, observations, lessons worth keeping.

Log everything to Notion (or local `TRACKING.md`) under: [Date].
Update MEMORY.md with anything worth retaining long-term.
Run silently. No need to notify unless the process fails.
```

---

## 🛡️ **Skill #4: 2:00 AM Automated GitHub Backup**

**Setup**: Daily configuration and memory safety.

**Cron Schedule**: `0 2 * * *`  
**Agent**: `github-backup`

**Deployment Prompt**:
```markdown
Run the daily workspace backup:
1. Stage all changes in the workspace and `.openclaw` directory.
2. Commit with message: "Daily backup — [YYYY-MM-DD]"
3. Push to main branch on the connected private GitHub repo.
4. Confirm success silently (no notification unless backup fails).
```

---

## 📈 **Skill #5: Weekly Trend Analysis**

**Setup**: Intelligence gathering on specific market trends.

**Cron Schedule**: `0 9 * * 1` (Monday Mornings)  
**Agent**: `researcher`

**Deployment Prompt**:
```markdown
Run the weekly trend scan for [YOUR NICHE]. 

Sources to check:
- Reddit: top posts this week.
- YouTube: trending videos for keywords.
- X/Twitter: trending conversations.

Compile a Weekly Trend Report with:
1. TOP 5 TRENDING TOPICS
2. CONTENT IDEAS (3 ideas ranked by engagement potential)
3. LEAD MAGNET CONCEPTS (2 high-value offers)
4. PAIN POINTS identified.

Post report to Telegram.
```
