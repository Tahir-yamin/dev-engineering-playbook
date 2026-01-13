# AGENTS.md

## Purpose

This project uses **Spec-Driven Development (SDD)** — a workflow where **no agent is allowed to write code until the specification is complete and approved**.

All AI agents (Claude, Copilot, Gemini, local LLMs, etc.) must follow the **Spec-Kit lifecycle**:

> **Specify → Plan → Tasks → Implement**

This prevents "vibe coding," ensures alignment across agents, and guarantees that every implementation step maps back to an explicit requirement.

---

## How Agents Must Work

Every agent in this project MUST obey these rules:

1. **Never generate code without a referenced Task ID.**
2. **Never modify architecture without updating specs.**
3. **Never propose features without updating specifications.**
4. **Never change approach without documenting reasons.**
5. **Every code file must contain a comment linking it to the Task and Spec sections.**

If an agent cannot find the required spec, it must **stop and request it**, not improvise.

---

## Spec-Kit Workflow (Source of Truth)

### 1. Specify (WHAT — Requirements & Acceptance Criteria)

File Location: `specs/features/*.md`

Contains:
* User journeys
* Requirements
* Acceptance criteria
* Domain rules
* Business constraints

Agents must not infer missing requirements — they must request clarification or propose specification updates.

---

### 2. Plan (HOW — Architecture, Components, Interfaces)

File Location: `specs/phase2-implementation-plan.md`

Includes:
* Component breakdown
* APIs & schema diagrams
* Service boundaries
* System responsibilities
* High-level sequencing

All architectural output MUST be generated from the Specify file.

---

### 3. Tasks (BREAKDOWN — Atomic, Testable Work Units)

File Location: `.gemini/antigravity/brain/.../task.md`

Each Task must contain:
* Task ID
* Clear description
* Preconditions
* Expected outputs
* Artifacts to modify
* Links back to Specify + Plan sections

Agents **implement only what these tasks define**.

---

### 4. Implement (CODE — Write Only What the Tasks Authorize)

Agents now write code, but must:
* Reference Task IDs
* Follow the Plan exactly
* Not invent new features or flows
* Stop and request clarification if anything is underspecified

> The golden rule: **No task = No code.**

---

## Agent Behavior in This Project

### When generating code:

Agents must reference:

```
[Task]: T-001
[From]: specs/features/task-crud.md §2.1, specs/phase2-implementation-plan.md §3.4
```

### When proposing architecture:

Agents must reference:

```
Update required in specs/phase2-implementation-plan.md → add component X
```

### When proposing new behavior or a new feature:

Agents must reference:

```
Requires update in specs/features/[feature].md (WHAT)
```

---

## Project Structure

### Spec-Kit Organization

```
todo_hackathon_phase2/
├── .spec-kit/                    # Spec-Kit configuration
│   └── config.yaml
├── specs/                        # Spec-Kit managed specifications
│   ├── overview.md               # Project overview
│   ├── phase2-fullstack.md       # Phase 2 requirements
│   ├── features/                 # Feature specifications
│   │   ├── task-crud.md
│   │   ├── authentication.md
│   │   └── neural-ui.md
│   ├── api/                      # API specifications
│   │   └── rest-endpoints.md
│   ├── database/                 # Database specifications
│   │   └── schema.md
│   └── ui/                       # UI specifications
│       ├── components.md
│       └── pages.md
├── AGENTS.md                     # This file - Agent instructions
├── CLAUDE.md                     # Root Claude Code instructions
├── phase2/
│   ├── frontend/
│   │   ├── CLAUDE.md            # Frontend-specific guidelines
│   │   └── ... (Next.js app)
│   ├── backend/
│   │   ├── CLAUDE.md            # Backend-specific guidelines
│   │   └── ... (FastAPI app)
│   └── docs/
│       └── CLAUDE.md            # Implementation history
└── README.md
```

---

## Tech Stack (Phase II)

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Context API + Hooks
- **HTTP Client**: Custom API client with Fetch
- **Auth**: Better Auth (client)

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.13+
- **Database ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT
- **Validation**: Pydantic V2

---

## Development Workflow

### Day-to-Day Process

1. **Read Spec**: `@specs/features/[feature].md`
2. **Implement Backend**: Follow `@phase2/backend/CLAUDE.md`
3. **Implement Frontend**: Follow `@phase2/frontend/CLAUDE.md`
4. **Test and Iterate**
5. **Update Specs** if requirements change

---

## CLAUDE.md Files

### Root CLAUDE.md
Provides project navigation and spec usage instructions.

### Frontend CLAUDE.md
- Stack: Next.js 14, TypeScript, Tailwind CSS
- Component patterns
- API client usage
- Styling guidelines

### Backend CLAUDE.md
- Stack: FastAPI, SQLModel, Neon PostgreSQL
- Project structure
- API conventions
- Database patterns

---

## Referencing Specs

### In Claude Code

```bash
# Implement a feature
You: @specs/features/task-crud.md implement the create task feature

# Implement API
You: @specs/api/rest-endpoints.md implement the GET /api/tasks endpoint

# Update database
You: @specs/database/schema.md add due_date field to tasks

# Full feature across stack
You: @specs/features/authentication.md implement Better Auth login
```

---

## Agent Failure Modes (What Agents MUST Avoid)

Agents are NOT allowed to:
* Freestyle code or architecture
* Generate missing requirements
* Create tasks on their own
* Alter stack choices without justification
* Add endpoints, fields, or flows that aren't in the spec
* Ignore acceptance criteria
* Produce "creative" implementations that violate the plan

If a conflict arises between spec files, the hierarchy is:
**Constitution > Specify > Plan > Tasks**

---

## Current Phase: Phase II Complete

### Completed Features
- ✅ Task CRUD operations (Basic Level)
- ✅ User authentication with Better Auth
- ✅ RESTful API with all required endpoints
- ✅ Neural network UI theme
- ✅ Search & filter system
- ✅ 4-column Kanban board
- ✅ Real-time analytics dashboard
- ✅ Dark/light mode toggle
- ✅ Mobile responsive design

### Next Phase: Phase III (AI Chatbot)
- OpenAI ChatKit UI
- OpenAI Agents SDK
- MCP (Model Context Protocol) Server
- Stateless chat with database persistence
- Natural language task management

---

## Key Principles

1. **Spec-First**: Always write spec before code
2. **Reference Everything**: Every code change links to a spec
3. **No Improvisation**: If spec is unclear, ask - don't guess
4. **Document Iterations**: Keep spec history updated
5. **Maintain Alignment**: All agents follow same specs

---

**For detailed implementation history**: See `@phase2/docs/CLAUDE.md`  
**For feature specifications**: See `@specs/features/`  
**For API docs**: See `@specs/api/`

---

## 2026 AI Agent Developments

### Claude Cowork (January 12-13, 2026)
- **Desktop AI for non-technical users** (macOS)
- Controlled local folder access for file management
- Natural language interface for office tasks
- Democratizes agent functionality beyond developers

### Claude for Healthcare (January 11, 2026)
- **HIPAA-compliant** medical AI applications
- Clinical trial protocols and regulatory submissions
- Enterprise partnerships (Allianz insurance)
- Specialized vertical AI trend

### Multi-Agent Orchestration
- **1,445% increase** in enterprise adoption (Gartner)
- **40%** of apps to embed agents by end of 2026
- **$8.5B** market (2026), **$35B** by 2030
- Major platforms: Microsoft, Google ADK, OpenAI, CrewAI

### AI Co-Workers Ecosystem
- Microsoft 365 Copilot, Slack AI, Notion AI, Asana AI
- Shift from "assistant" to "teammate"
- Autonomous planning and execution

**Latest Report**: See `claude_update_report_2026-01-13.md`

---

## Browser Testing Best Practices

### ⚠️ CRITICAL: Always Clear Input Fields

When using the browser agent to test forms, **ALWAYS use `ClearText: true`** for input operations:

```
# CORRECT - Clears field before typing
browser_input(Index=1, Text="user@example.com", ClearText=true)

# WRONG - Appends to existing text causing concatenation bugs
browser_input(Index=1, Text="user@example.com")
```

### Why This Matters
- Fields may have autofill data
- Previous failed attempts leave text in fields
- Concatenated text causes "Invalid email or password" errors
- Debugging becomes difficult when you can't see the actual values

### Workflow Reference
See `.agent/workflows/browser-testing.md` for complete testing guidelines.

---

**Last Updated**: 2026-01-13  
**Phase**: Phase II Complete, Phase III in progress, **Latest AI Update: Jan 13, 2026**  
**Hackathon**: "Evolution of Todo - Mastering Spec-Driven Development & Cloud Native AI"
