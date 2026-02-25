# Universal Agentic Frameworks (Elite Masterclass)

**Purpose**: The definitive guide to multi-agent orchestration, agentic RAG, and framework-specific patterns (CrewAI, Google ADK, OpenAI AgentKit, Microsoft AI Foundry, Gemini CLI).
**Unified From**: 10+ redundant agentic skill files.

---

## 🏗️ PART 1: ELITE MULTI-AGENT PATTERNS (The Decision Matrix)

| Pattern | Metaphor | Best For... | Implementation Strategy |
| :--- | :--- | :--- | :--- |
| **Sequential** | Assembly Line | Data pipelines | Step A output → Step B input. |
| **Dispatcher** | Concierge | Intent routing | Master agent routes to specialists. |
| **Fan-Out/Gather** | Octopus | Speed/Diversity | Parallel execution + Synthesis step. |
| **Russian Doll** | Hierarchical | Complex goals | Sub-agents treated as tools by parents. |
| **Editor's Desk** | Gen + Critic | Quality Control | Generator creates → Critic validates → Loop. |
| **Safety Net** | Human-in-Loop | High-risk | Explicit "Pause & Review" gate. |

### The "Plan vs. Build" Separation
A critical pattern for safety and accuracy:
1. **Plan Agent**: Read-only access. Produces `implementation_plan.md`.
2. **Build Agent**: Write/Execute access. Follows the plan exactly.

---

## 🎨 PART 2: ECOSYSTEM DOMINANCE (Framework Patterns)

### 1. CrewAI (Role-Based Teamwork)
- **Agents**: Defined by `role`, `goal`, and `backstory`.
- **Tasks**: Assignments with `expected_output` and `context` dependencies.
- **Process**: `sequential` (default) or `hierarchical` (requires a Manager agent).
- **Flows**: Event-driven `@start`, `@listen`, and `@router` decorators for precise control.

### 2. Google ADK (Production-Grade Orchestration)
- **Tiered Context**: Shift from session logs (Tier 2) to ephemeral working context (Tier 1).
- **Processors**: Modular pipeline for auth, instructions, and tool handling.
- **State**: Use `output_key` in agents to avoid race conditions in parallel flows.

### 3. OpenAI AgentKit & SDK
- **Responses API**: The successor to Assistants API (Sunset 2026). Single request for chat, tools, and streaming.
- **Handoffs**: Native support for delegating tasks between specialized agents.
- **Guardrails**: Integrated input/output validation schemas.

### 4. Microsoft AI Foundry
- **Persistent Agents**: Support for long-running threads and Azure-hosted file search/code interpreter.
- **Deployment**: Use `azd` patterns to bundle Bicep (IaC) with agent logic.

---

## 🔍 PART 3: AGENTIC RAG & SELF-CORRECTION

### Corrective RAG (CRAG)
1. **Retrieve**: Fetch from Vector DB.
2. **Grade**: LLM scores docs as `relevant` or `irrelevant`.
3. **Decide**:
   - 0% Relevant → **Transform Query** → **Web Search** (Fallback).
   - >0% Relevant → Filter out noise → Generate.

### Self-RAG (The Critic)
Adds a post-generation check to verify:
- **Grounding**: Is the answer supported by retrieved docs?
- **Utility**: Does it actually solve the user's question?

---

## 🛠️ PART 4: CLI & TOOLING (The Operator's Kit)

### Gemini CLI (Sovereign Automation)
- **GitHub Integration**: `@gemini-cli fix this issue` triggers automated analysis, fix, and PR creation.
- **Custom Skills**: Define `.agent/skills/` with `SKILL.md` and associated automation scripts.
- **Chaining**: `gemini chain --skill A --skill B "Task"` for production-line execution.

### Tooling Recommendations
- **Orchestration**: LangGraph, CrewAI, PydanticAI.
- **Search API**: Tavily (Search for AI), Serper.
- **Vector DB**: Qdrant, Chroma, Vector (PostgreSQL).

---

## 🚀 MASTER COMPLETION CHECKLIST
- [ ] Agent roles are discrete and non-overlapping.
- [ ] Handoff protocols use structured `markdown` reports.
- [ ] Fallback (Web Search) is implemented for all research tasks.
- [ ] Destructive actions (DAP) require a "Plan vs. Build" separation.

**Last Updated**: February 2026
**Intelligence Level**: Alpha-Fused Master
