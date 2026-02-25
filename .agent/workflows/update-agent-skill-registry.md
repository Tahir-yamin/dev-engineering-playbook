---
description: Add new agents or skills to the registry and rebuild the recall index
---

# Update Agent & Skill Registry

// turbo-all

Use this workflow whenever:
- A new agent file is created or imported
- A new skill file is added to `skills/`
- The user asks to "add X to the registry" or "make X recallable"
- After migrating agents from any source directory

---

## STEP 1 — Place the file in the correct location

**New Agent** → `.agent/agents/my-expert.agent.md`  
**New Skill** → `skills/my-skill.md` OR `skills/my-skill/SKILL.md`  
**New Workflow** → `.agent/workflows/my-workflow.md`

Naming conventions:
| Domain | Prefix |
|---|---|
| Architecture | `arch-` |
| Cloud / Azure | `cloud-azure-` |
| Data | `data-` |
| DevOps / K8s | `ops-` |
| Development | `dev-` |
| Language | `lang-` |
| Planning | `plan-` |
| Security | `sec-` |
| Testing | `test-` |
| Frontend | `ui-` |

---

## STEP 2 — Run the registry updater

```powershell
python scripts/update_registry.py
```

This single command does everything:
1. **Sovereign Consolidation**: Physically moves MCP servers and harvests external skills into the `.agent/` core.
2. **Path Management**: Automatically updates `MCP_CONFIG_MANIFEST.json` to point to the new local paths.
3. **Frontmatter Refinement**: Fixes metadata on all agent files (`name`, `target: vscode`, `infer: true`).
4. **Recall Synthesis**: Creates `@skill-*` gateway agents and rebuilds the 3,000+ line `KNOWLEDGE_INDEX.md`.

---

## STEP 3 — Verify in Antigravity

Type `@` in chat and search for the new entry.
Type `/` in chat and search for any new workflow.
Open `KNOWLEDGE_INDEX.md` and `Ctrl+F` confirmation.

---

## Frontmatter Template (for new agents)

```yaml
---
name: 'your-agent-name'
target: 'vscode'
infer: true
description: "One-line description shown in @ picker"
---
```

---

## File Location Reference

| Resource | Directory | Recall |
|---|---|---|
| Agent | `.agent/agents/*.agent.md` | `@name` |
| Skill (file) | `skills/*.md` | `@filename` |
| Skill (folder) | `skills/name/SKILL.md` | `@SKILL.md` |
| Workflow | `.agent/workflows/*.md` | `/name` |
| Rules | `.agent/rules/*.md` | `@` → Rules |
