# Codebase Map: Dev Knowledge Base

This file documents critical entry points, file dependencies, and "hot paths" within the workspace to ensure consistent updates and reliable navigation.

## 🚀 Critical Entry Points

| File | Purpose | Priority |
|------|---------|----------|
| `COMMAND_CENTER.md` | Central navigation hub for all resources. | CRITICAL |
| `GEMINI.md` | Maestro configuration and behavior rules. | CRITICAL |
| `README.md` | Historical context and high-level project summary. | HIGH |
| `ARCHITECTURE.md` | System map and architectural patterns. | HIGH |

## 📁 Key Directories & Dependencies

### `.agent/` (Maestro Core)
- **Dependency**: Modification of a skill in `.agent/skills/` may require updates to corresponding `workflows/`.
- **Constraint**: Rules in `.agent/rules/` must be referenced by the `GEMINI.md` agent mapping.

### `skills/` (Knowledge Core)
- **Dependency**: The `COMMAND_CENTER.md` acts as the primary index for this directory.
- **Update Rule**: New skills must be registered in the `Resource Navigator` section of `COMMAND_CENTER.md`.

## 🔄 Hot Paths (Frequent Updates)

1. **Automation Addition**: 
   `skills/` → `.agent/workflows/` → `COMMAND_CENTER.md`
2. **AI Ecosystem Sync**: 
   `external-libs/` → `docs/ai-updates/` → `COMMAND_CENTER.md`

## 🛠️ Infrastructure Pointers

- **MCP Config**: Managed in `.mcp/claude_desktop_config_sample.json`.
- **Scripts**: Maintenance tools located in `scripts/` (e.g., `checklist.py`).

---
*Last Updated: 2026-02-12*
