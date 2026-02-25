# Compound Engineering & Agentic Workflows

**Topics**: Software Development Methodology, Agentic Workflows, Planning
**Version**: 1.0
**Sources**: `obra/superpowers`, `EveryInc/compound-engineering-plugin`

---

## Skill #1: Compound Engineering Cycle

### Context
"Each unit of engineering work should make subsequent units easier—not harder."
Use this workflow to prevent technical debt and ensure high-quality, reusable code.

### The Cycle
1. **Plan** (`/workflows:plan`): 
   - Thoroughly brainstorm and architect before writing a single line of code.
   - Break work into "bite-sized" tasks (2-5 minutes execution time).
   - *Tools*: `brainstorming`, `writing-plans` (Superpowers).
2. **Work** (`/workflows:work`):
   - Execute tasks in isolated environments (e.g., git worktrees).
   - Enforce **TDD** (Red-Green-Refactor).
   - Use sub-agents for specific tasks.
3. **Review** (`/workflows:review`):
   - Review against the original plan.
   - Check for spec compliance and code quality.
   - Critical issues block progress.
4. **Compound** (`/workflows:compound`):
   - Capture learnings.
   - Codify knowledge into new skills or documentation.
   - Update prompts/agents based on what went wrong/right.

### Prompt Template (Planning Phase)
```markdown
**ROLE**: Senior Architect / Planner

**OBJECTIVE**: Break down the feature "[FEATURE NAME]" into atomic, verifiable tasks.

**CONSTRAINTS**:
- Each task must be actionable by a coding agent in < 5 minutes.
- Must include verification steps (tests or manual checks).
- Follow YAGNI and DRY principles.

**OUTPUT FORMAT**:
1. [Task Name] - [File Paths] - [Verification]
...
```

---

## Skill #2: Superpowers Framework

### Core Concepts
- **Brainstorming First**: never start coding without a "teased out" spec.
- **Git Worktrees**: Use `using-git-worktrees` to keep context clean.
- **Subagent Driven Development**: Dispatch agents for specific files/tasks.
- **Finishing Protocol**: Always verify tests and clean up worktrees before merging.

### Comparison
| Feature | Traditional Dev | Agentic/Compound Dev |
|---------|-----------------|----------------------|
| **Planning** | Ad-hoc, mental model | Explicit, written plans, atomic tasks |
| **Testing** | After code (maybe) | TDD (Red-Green-Refactor) mandatory |
| **Context** | Single cluttered repo | Isolated worktrees per feature |
| **Growth** | Tech debt accumulates | Knowledge compounds (documentation/skills) |

---

## Quick Reference

- **Compound Plugin**: `Plan -> Work -> Review -> Compound`
- **Superpowers**: `Brainstorm -> Worktree -> Plan -> Execute -> Test -> Review`

---

## Related Skills
- `plan-writing`
- `clean-code`
- `testing-patterns`
