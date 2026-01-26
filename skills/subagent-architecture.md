# Subagent Architectures & Patterns

**Topics**: Multi-Agent Systems, Handoffs, Superpowers Framework
**Version**: 1.0
**Source**: `obra/superpowers`, `VoltAgent/awesome-claude-code-subagents`

---

## Skill #1: The "Dispatcher" Pattern (Superpowers)

### Context
Instead of one monolithic agent doing everything, use a "Dispatcher" to route tasks to specialized subagents.

### The Flow
1. **User Request**: "Add a new API endpoint for user login."
2. **Dispatcher Agent**: Analyses request.
   - *Decision*: Needs backend work -> Activates `backend-developer`.
3. **Subagent Execution**:
   - `backend-developer` reads `specs/auth.yaml`.
   - Implements code in `src/auth/`.
   - Runs tests.
4. **Handoff Back**: Subagent reports success/failure to Dispatcher.
5. **Dispatcher**: Verifies or activates next agent (e.g., `frontend-developer` to hook up the UI).

### Agent Configuration (Example)
```yaml
# .agent/dispatch.yaml
role: "Dispatcher"
instructions: "You route tasks. Do not write code yourself."
tools:
  - invoke_agent(agent_name, task)
  - read_file
```

---

## Skill #2: Independent "Build vs Plan" Agents (OpenCode)

### Context
Separating "Thinking" from "Doing" prevents destructive actions during exploration.

### The Pattern
- **Plan Agent**:
  - **Permissions**: Read-only (Files, search). No shell execution.
  - **Goal**: Create a robust `implementation_plan.md`.
  - **Prompt**: "Analyze the codebase and propose a solution. Do not edit files."
- **Build Agent**:
  - **Permissions**: Full write access, shell execution.
  - **Goal**: Execute the `implementation_plan.md`.
  - **Restriction**: Must follow the plan exactly.

### Why use this?
- Reduces "agent hallucinations" where it deletes files by mistake.
- Allows human review of the Plan before dangerous actions.

---

## Skill #3: Handoff Protocol

### Standard Handoff Format
When passing context between agents, standardizing the handoff message is crucial.

**Template**:
```markdown
# Handoff Report
**From**: [Agent A]
**To**: [Agent B]

## Status
- ✅ Completed: [Task 1], [Task 2]
- ⏳ Pending: [Task 3]

## Context
- Created file: `src/new_feature.ts`
- Encountered error: "DB connection failed" (Log attached)

## Next Steps for You
Please fix the DB connection using the credentials in `.env.example`.
```

---

## Quick Reference
- **Dispatcher**: Hub-and-spoke model.
- **Plan/Build**: Separation of concerns model.
- **Handoff**: Structured context passing.

## Related Skills
- `compound-engineering.md`
- `enterprise-meta-orchestration-guide`
