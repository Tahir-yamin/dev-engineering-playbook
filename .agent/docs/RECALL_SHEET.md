# RECALL SHEET — Antigravity Quick Reference
_Auto-generated — 2026-02-24 00:48_

---

## @ AGENTS  (type @name in chat)

### Fast Mnemonic Agents
| Command | Purpose |
|---------|---------|
| `@alpha` | Ultimate Alpha Beast — transcendent autonomous agent |
| `@react` | React 19.2 frontend expert |
| `@plan` | Project planner & implementaion strategist |
| `@arch` | System architect & ADR writer |
| `@ops` | Terraform / Kubernetes / Infrastructure |
| `@sec` | Security auditor & DevSecOps |
| `@test` | TDD / QA / Playwright expert |
| `@python` | Python / MCP server developer |
| `@orchestrate` | Multi-agent workflow orchestrator |

### All Agents (78+ in registry)
**Location**: `.agent/agents/`  
**Browse**: Open `KNOWLEDGE_INDEX.md` → AGENTS section

**Naming pattern** — agents are grouped by prefix:
| Prefix | Domain |
|--------|--------|
| `@arch-*` | Architecture (ADR, API, blueprint, modernization) |
| `@cloud-azure-*` | Azure IaC (Bicep, Terraform, AVM) |
| `@data-*` | Databases (Postgres, MongoDB, SQL, Power BI) |
| `@dev-*` | Development (debug, janitor, devops, ML, MCP) |
| `@lang-*` | Language specialists (C#, Rust, Go, Java, Python) |
| `@ops-*` | Infrastructure (K8s, GitHub Actions, Terraform) |
| `@plan-*` | Planning (PRD, implementation plan, Jira) |
| `@sec-*` | Security (reviewer, JFrog, StackHawk) |
| `@test-*` | Testing (Playwright, TDD cycle) |
| `@ui-*` | Frontend (React, Next.js, Laravel, Shopify) |
| `@ux-*` | UX (accessibility, designer) |

### Skill Gateway Agents (183 skills registered)
Skills are now accessible as `@skill-<name>`. Examples:
| Command | Skill |
|---------|-------|
| `@skill-frontend-skills` | Next.js & React frontend patterns |
| `@skill-backend-skills` | FastAPI & Python backend patterns |
| `@skill-kubernetes-resource-optimization-skills` | K8s optimization |
| `@skill-python-ruff-linting-skills` | Python code quality |
| `@skill-compound-engineering` | Plan-Work-Review cycle |
| `@skill-fabric-prompts` | 90 Power BI/Fabric patterns |
| `@skill-notebooklm-mastery` | Advanced NotebookLM research |
| `@skill-x-marketing-expert` | X (Twitter) algorithm expertise |
| `@skill-universal-agentic-frameworks` | Agentic masterclass |
| `@skill-cloud-native-mastery` | Cloud-native orchestration |

---

## / WORKFLOWS  (type /name in chat)

### Key Workflows
| Command | Purpose |
|---------|---------|
| `/plan` | Create implementation plan |
| `/debug` | Systematic root cause analysis |
| `/qa` | End-to-end testing |
| `/deploy` | Production deployment |
| `/orchestrate` | Multi-agent coordination |
| `/create` | Build new application |
| `/audit` | Workspace health check |
| `/brainstorm` | Structured feature exploration |
| `/security-audit` | Security review workflow |
| `/alpha-project-lifecycle` | Full project lifecycle |
| `/alpha-cloud-deployment` | AKS + Dapr + Kafka deploy |
| `/compound-development-cycle` | Plan-Work-Review-Compound |
| `/x-viral-optimizer` | Optimize content for X virality |
| `/fabric-audit` | Power BI BPA remediation |

**All 207 workflows** are in `.agent/workflows/` — type `/` and search.

---

## RECALL SYNTAX REFERENCE

```
# Recall with @
@react                          # Fast mnemonic agent
@arch-adr                       # Named agent from registry
@skill-frontend-skills          # Skill gateway
@[.agent/agents/plan.agent.md]  # Full path (any file)

# Recall with /
/plan                           # Workflow slash command
/debug                          # Debug workflow

# Reference any file in chat
@[path/to/any/file.md]          # Works for ANY file in workspace
@[skills/frontend-skills.md]    # Direct skill reference
@[white-papers/wp6-multi-agent-systems.md]  # White paper reference
```

---

## SEARCH TOOLS

```powershell
# Search by keyword (fast)
.\scripts\search.ps1 "react ui" -Type agent
.\scripts\search.ps1 "deploy kubernetes" -Type workflow
.\scripts\search.ps1 "project management" -Type skill

# Rebuild this index
python scripts/build_recall_registry.py
python scripts/build_index.py
```

---
_Total: 331 agents | 183 skill gateways | 207 workflows_
