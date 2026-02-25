# Master Knowledge Index: Dev Knowledge Base

This is the centralized "Search & Routing" index for the Gemini Brain. Use this to find specialized expertise across 85k+ files.

## 🗺️ Engineering Domains

### 1. AI & Multi-Agent Systems (MAS)
- **Rules**: `@[.agent/rules/workflow-orchestrator-persona.md]`, `@[.agent/rules/Thinking-Beast-Mode.agent.md]`
- **Skills**: `skills/multi-agent-patterns-google-adk.md`, `skills/crewai-framework-skills.md`, `skills/subagent-architecture.md`
- **Workflows**: `@[.agent/workflows/orchestrate.md]`, `@[.agent/workflows/crewai-integration.md]`
- **External**: `external-libs/langgraph/`, `external-libs/awesome-claude-code-subagents/`

### 2. DevOps, Cloud & Infrastructure
- **Rules**: `@[.agent/rules/devops-persona.md]`, `@[.agent/rules/github-actions-expert.agent.md]`, `@[.agent/rules/terraform.agent.md]`
- **Skills**: `skills/kubernetes-resource-optimization-skills.md`, `skills/dapr-configuration-skills.md`, `skills/helm-configuration-skills.md`
- **Workflows**: `@[.agent/workflows/deploying-to-aks.md]`, `@[.agent/workflows/az-cost-optimize.prompt.md]`
- **Documentation**: `docs/deployment/`, `kubernetes/`, `external-libs/dapr-quickstarts/`

### 3. Software Development (Full Stack)
- **Rules**: `@[.agent/rules/expert-react-frontend-engineer.agent.md]`, `@[.agent/rules/expert-dotnet-software-engineer.agent.md]`, `@[.agent/rules/python-mcp-expert.agent.md]`
- **Skills**: `skills/frontend-skills.md`, `skills/backend-skills.md`, `skills/python-ruff-linting-skills.md`, `skills/latex-conversion/SKILL.md`
- **Workflows**: `@[.agent/workflows/adding-new-feature.md]`, `@[.agent/workflows/openapi-to-application-code.prompt.md]`, `@[.agent/workflows/latex-conversion.md]`
- **External**: `claude-cookbooks/`, `external-libs/antigravity-kit/`

### 4. Database & Persistence
- **Rules**: `@[.agent/rules/postgresql-dba.agent.md]`, `@[.agent/rules/mongodb-performance-advisor.agent.md]`
- **Skills**: `skills/database-skills.md`, `skills/docker-prisma-skills.md`
- **Workflows**: `@[.agent/workflows/database-schema-changes.md]`, `@[.agent/workflows/cosmosdb-datamodeling.prompt.md]`

### 5. Testing & Quality Assurance
- **Rules**: `@[.agent/rules/playwright-tester.agent.md]`, `@[.agent/rules/tdd-red.agent.md]`
- **Skills**: `skills/webapp-testing/`, `skills/debug-skills.md`
- **Workflows**: `@[.agent/workflows/complete-application-qa.md]`, `@[.agent/workflows/chat-testing.md]`

### 6. Specialized & Research Domains
- **Medical/PubMed**: `external-libs/PubMed-MCP-Server/`, `external-libs/mcp-scholarly/`
- **Video Editing**: `external-libs/davinci-resolve-mcp/`, `external-libs/video-editing-mcp/`
- **Project Management (P6/MSP)**: `external-libs/p6xer-mcp-server/`, `skills/project-management/`, `ms_project_import_guide.md`, `SCHEDULE_README.md`
- **Writing Frameworks**: `external-libs/WriteHERE/`
- **X Marketing & Algorithm**: `skills/x-marketing-expert.md`, `@[.agent/workflows/x-viral-optimizer.prompt.md]`

---

## 🚀 Priority Workflows (Slash Commands)

| Command | File Path | Usage |
|---------|-----------|-------|
| `/plan` | `.agent/workflows/create-implementation-plan.prompt.md` | Start any new feature |
| `/schedule` | `PRO_SCHEDULE_MASTER_PROMPT.md` | Start new Fuel Station Schedule |
| `/debug` | `.agent/workflows/comprehensive-bug-analysis.md` | Systematic RCA |
| `/qa` | `.agent/workflows/complete-application-qa.md` | Final E2E testing |
| `/orchestrate` | `.agent/workflows/orchestrate.md` | Multi-agent collaboration |
| `/x-optimize` | `.agent/workflows/x-viral-optimizer.prompt.md` | Optimize technical content for X virality |
| `/audit` | `scripts/checklist.py` | Workspace health check |

---
*Last Updated: 2026-02-12*

## 🧠 Neural Relationships (Phase 7)

| Source Domain | Dependent Component | Impact Vector |
|---------------|---------------------|---------------|
| `infra/` (K8s) | `reports/` (PBI) | Network policies affecting Data Gateway connectivity |
| `.agent/rules/` | `scripts/` | Agent updates requiring script re-validation |
| `external-libs/` | `skills/` | Dependency updates triggering skill distillation |
| `GEMINI.md` | *Full Workspace* | Regulatory/Policy changes affecting all operations |
