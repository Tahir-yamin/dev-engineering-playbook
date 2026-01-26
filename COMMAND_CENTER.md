# 🎯 COMMAND CENTER
**Dev Knowledge Base - Your Centralized Resource Hub**

Last Updated: 2026-01-26 | Total Resources: 3,063+ files (was 3,060)

---

## 🆕 **NEW USER? → [Quick Start Guide](docs/quickstart/HOW_TO_USE_COMMAND_CENTER.md)**
**Learn how to use this command center with practical examples (5 min read)**

---

## 🚀 Quick Start

```
NEW USER? → docs/quickstart/QUICKSTART_GUIDE.md
NEED HELP? → docs/quickstart/DRAG_INTO_CHAT.md  
VIEW STATS? → docs/workspace/WORKSPACE_STATS.md
```

---

## 📊 Resource Navigator

### 🎭 AI Personas & Rules
**Location**: `.agent/rules/`  
**Count**: 143 personas (was 3) ⭐ **NEW: +140 GitHub Copilot agents integrated!**

**Original Personas**:
| Persona | Use For |
|---------|---------|
| [workflow-orchestrator](.agent/rules/workflow-orchestrator-persona.md) | Complex workflows, state machines, process automation |
| [devops-engineer](.agent/rules/devops-persona.md) | Infrastructure, deployments, CI/CD |
| [rules.md](.agent/rules/rules.md) | DevOps agent guidelines |

**🆕 GitHub Copilot Agents** (140 total):
- **📋 [Complete Catalog](docs/external-libs/GITHUB_COPILOT_AGENTS_INDEX.md)** ← Browse all 140 agents by category
- **Quick Access**: All agents are now in `.agent/rules/*.agent.md`
- **Categories**: Planning (12), Development (30+), Testing (8), DevOps (18), Cloud (15), AI/ML (8), Database (8), Security (6), and more

**Top Integrated Agents**:
- `plan.agent.md` - Implementation planning
- `expert-react-frontend-engineer.agent.md` - React expertise
- `CSharpExpert.agent.md` - C# development
- `terraform.agent.md` - Infrastructure as Code
- `github-actions-expert.agent.md` - CI/CD workflows

**Quick Use**:
```
@[.agent/rules/plan.agent.md]
Create an implementation plan for my feature

@[.agent/rules/expert-react-frontend-engineer.agent.md]
Help me build a React component
```

---

### 💡 Skills Library
**Location**: `skills/`  
**Count**: 101+ production-tested skills (was 100) ⭐ **NEW: +1 Python code quality skills!**

**Top Skills**:
- [python-ruff-linting-skills.md](skills/python-ruff-linting-skills.md) - Python code quality with Ruff (6 skills) ⭐ NEW
- [multi-agent-patterns-google-adk.md](skills/multi-agent-patterns-google-adk.md) - 8 multi-agent architectures
- [constitutional-ai-anthropic.md](skills/constitutional-ai-anthropic.md) - AI ethics framework
- [agentic-rag-mastery.md](skills/agentic-rag-mastery.md) - Deep Dive: CRAG & Self-RAG Implementation ⭐
- [subagent-architecture.md](skills/subagent-architecture.md) - Subagent Dispatcher & Handoff patterns ⭐
- [compound-engineering.md](skills/compound-engineering.md) - "Plan-Work-Review" Cycle Methodology ⭐
- [mcp-debugging-skills.md](skills/mcp-debugging-skills.md) - MCP troubleshooting
- [kubernetes-resource-optimization-skills.md](skills/kubernetes-resource-optimization-skills.md) - K8s optimization
- [dapr-configuration-skills.md](skills/dapr-configuration-skills.md) - Dapr setup

**🆕 GitHub Copilot Skills** (63 folders):
- Self-contained skill folders with `SKILL.md` + bundled resources
- All integrated into `skills/` directory
- Based on [Agent Skills specification](https://agentskills.io/specification)

**Browse All**: [skills/](skills/)

---

### ⚙️ Workflows
**Location**: `.agent/workflows/`  
**Count**: 196+ executable workflows (was 195) ⭐ **NEW: +1 Python CI/CD workflow added!**

**Original Categories**:

| Category | Count | Examples |
|----------|-------|----------|
| **Troubleshooting** | 21+ | cors-errors, deployment-issues, **fixing-python-lint-ci-failures** ⭐ NEW |
| Development | 15+ | adding-new-feature, code-review-testing, create-project-schedule |
| **DevOps** | 10+ | deploying-to-aks, continuous-deployment-monitoring |
| **Methodology** | 2 | compound-engineering, superpowers-framework |
| **AI/Automation** | 5+ | apply-for-jobs, chat-testing, crewai-integration |
| **Documentation** | 5+ | documentation-maintenance, skill-upgrade |

**🆕 GitHub Copilot Prompts** (134 total):
- **📋 [Complete Catalog](docs/external-libs/GITHUB_COPILOT_PROMPTS_INDEX.md)** ← Browse all 134 prompts by category
- **Quick Access**: All prompts in `.agent/workflows/*.prompt.md`
- **Categories**: Planning (18), Code Gen (15), Testing (11), Infrastructure (12), Cloud (10), Database (6), AI/MCP (15), and more

**Top Integrated Prompts**:
- `create-implementation-plan.prompt.md` - Feature planning
- `breakdown-plan.prompt.md` - Task decomposition
- `openapi-to-application-code.prompt.md` - API implementation
- `terraform-azure-implement.prompt.md` - Azure provisioning
- MCP server generators for 9 languages

**Slash Commands**:
```
/create      - Create new application
/debug       - Debug issues  
/deploy      - Deploy to production
/plan        - Create project plan (Compound Cycle)
/compound    - Run Compound Engineering cycle
/rag-build   - Implement Agentic RAG
/run-tests   - Run tests
/orchestrate - Multi-agent coordination
```

**Browse All**: [.agent/workflows/](.agent/workflows/)

---

### 🔧 MCP Server Configurations
**Location**: `.mcp/`  
**Count**: 2 files

- **claude_desktop_config_sample.json** - Sample MCP setup
- **README.md** - Setup instructions

**Quick Setup**:
```powershell
Copy-Item ".mcp\claude_desktop_config_sample.json" "$env:APPDATA\Claude\claude_desktop_config.json"
```

**External MCP Servers**: `external-libs/` (16 libraries)

---

### 📚 White Papers
**Location**: `white-papers/`  
**Count**: 7 research papers

1. **wp1-agent-accountability-crisis.md** - Agent accountability frameworks
2. **wp2-knowledge-augmented-reasoning.md** - Knowledge integration patterns
3. **wp3-tool-calling-mechanisms.md** - Tool orchestration
4. **wp4-iterative-refinement.md** - Feedback loops
5. **wp5-ai-coding-agents.md** - Code generation patterns
6. **wp6-multi-agent-systems.md** - Multi-agent coordination
7. (+ 1 more)

---

### 📖 Documentation Hub
**Location**: `docs/`

| Section | Files | Purpose |
|---------|-------|---------|
| **ai-updates/** | 6 | Claude & AI ecosystem monitoring |
| **quickstart/** | 3 | Getting started guides |
| **workspace/** | 3 | Stats & resource references |
| **guides/** | - | How-to guides |
| **learning/** | - | Learning notes |

---

### 🏗️ Project Resources

**Kubernetes**: `kubernetes/` - K8s deployment guides  
**Deployment**: `deployment/` - Cloud deployment docs  
**Testing**: `testing/` - QA & testing strategies  
**Troubleshooting**: `troubleshooting/` - Issue resolution  
**Demo Scripts**: `demo-scripts/` - Quick demos

---

### 📦 External Libraries (DETAILED)

**Location**: Multiple directories  
**Total**: 18 major libraries | ~6,700+ files (was ~6,000)  
**Purpose**: Extended capabilities for Google Antigravity AI coding assistant

---

#### 🤖 Antigravity-Specific Libraries

**1. antigravity-awesome-skills** (`external-libs/antigravity-awesome-skills/`)
- **Files**: 1,872 files
- **📋 [Complete File Listing](docs/external-libs/ANTIGRAVITY_SKILLS_INDEX.md)** ← Browse all files by category
- **Purpose**: Curated skill collection optimized for Antigravity
- **Contains**: Advanced coding patterns, debugging techniques, architecture skills
- **Use with Antigravity**: Reference in prompts for enhanced code generation
  ```
  @[external-libs/antigravity-awesome-skills/[skill-name]]
  ```

**2. antigravity-kit** (`external-libs/antigravity-kit/`)
- **Files**: 278 files  
- **📋 [Complete File Listing](docs/external-libs/ANTIGRAVITY_KIT_INDEX.md)** ← Browse all toolkit files
- **Purpose**: Toolkit and utilities for Antigravity workflows
- **Contains**: Project templates, automation scripts, configuration helpers
- **Use**: Bootstrap new projects with proven patterns

**3. gemini-cli** (`external-libs/gemini-cli/`)
- **Files**: 1,643 files
- **📋 [Complete File Listing](docs/external-libs/GEMINI_CLI_INDEX.md)** ← Browse all CLI files
- **Purpose**: Gemini CLI integration for Antigravity
- **Contains**: Command-line tools, API wrappers, documentation
- **Integration**: CLI tools callable from Antigravity tasks

---

#### 🎭 Claude/Anthropic Resources

**4. claude-cookbooks** (`claude-cookbooks/`)
- **Files**: 416 files (20 categories)
- **Purpose**: Official Anthropic Claude implementation guides
- **📋 [Complete File Index](docs/external-libs/README.md#claude-cookbooks)** ← Browse all 416 files
- **Categories**:
  - `capabilities/` - Core Claude features
  - `tool_use/` (29 files) - Tool calling patterns **← KEY for Antigravity**
  - `multimodal/` - Image/video processing
  - `patterns/` - Design patterns
  - `skills/` (23 files) - Reusable capabilities
  - `third_party/` - Integration examples
- **Antigravity Usage**: Reference for LLM best practices and tool calling
  ```
  @[claude-cookbooks/tool_use/[example].ipynb]
  Guide me on implementing similar tool calling in my code
  ```

**5. claude-subagents** (`claude-subagents/`)
- **Files**: 137 specialized agent personas
- **Categories**: 66 domains (see `categories/`)
- **📋 [Complete Agent Listing](docs/external-libs/CLAUDE_SUBAGENTS_INDEX.md)** ← All 137 agents by category
- **Purpose**: Pre-built expert personas for specific tasks
- **Antigravity Integration**: 
  ```
  @[claude-subagents/categories/[domain]/[agent].md]
  Act as this specialized agent for my task
  ```
- **Top Categories**:
  - `09-meta-orchestration/` - Multi-agent coordination
  - `security-scanning/` - Security audits
  - `machine-learning-ops/` - MLOps
  - `cloud-infrastructure/` - Cloud architecture

**6. claude-skills-library** (`claude-skills-library/`)
- **Files**: 50+ community skills
- **Purpose**: Community-contributed Claude skills
- **Format**: Markdown skill definitions
- **Use**: Copy techniques into your workflows

**7. anthropic-quickstarts** (`external-libs/anthropic-quickstarts/`)
- **Files**: 200 quickstart examples
- **Purpose**: Official Anthropic getting-started guides
- **Contains**: API usage, best practices, integration patterns

---

### 🏗️ Structured Development Mode (AI-DLC) ⭐ NEW

**Methodology**: AI-Driven Development Lifecycle (from `specs.md`)
**Status**: ✅ Installed & Native

**Features**:
- **Persistent Memory Bank**: Project context stored in `.specsmd/aidlc/memory-bank.yaml`
- **Specialized Roles**: Distinct personas for Planning, Building, and Operations
- **Bolt Methodology**: Time-boxed execution units

**Commands**:
```
/specsmd-master-agent        → Start Orchestrator (Router)
/specsmd-inception-agent     → Plan Features (Requirements, Stories)
/specsmd-construction-agent  → Build Features (DDD, Tests, Code)
/specsmd-operations-agent    → Deploy Features (Build, Verify)
```

**Workflow**:
1. **Inception**: Gather requirements -> Create User Stories -> Plan Bolts
2. **Construction**: Select Bolt -> Domain Design -> Code -> Test
3. **Operations**: Build Artifacts -> Deploy -> Monitor

**Documentation**:
- [Quick Start](.specsmd/aidlc/quick-start.md)
- [Flow README](.specsmd/aidlc/README.md)

---

#### 🤖 GitHub Copilot Resources (NEW)

**Official GitHub Collection** - Community-contributed agents, prompts, skills, and instructions

**8. github-awesome-copilot** (`external-libs/github-awesome-copilot/`)
- **Files**: 550+ files
- **Repository**: [github/awesome-copilot](https://github.com/github/awesome-copilot)
- **License**: MIT
- **Purpose**: Enterprise-grade GitHub Copilot customizations

**📋 Complete Indexes**:
- **[Agents Index](docs/external-libs/GITHUB_COPILOT_AGENTS_INDEX.md)** ← 140 agents in 10 categories
- **[Prompts Index](docs/external-libs/GITHUB_COPILOT_PROMPTS_INDEX.md)** ← 134 prompts in 10 categories
- **[Instructions Index](docs/external-libs/GITHUB_COPILOT_INSTRUCTIONS_INDEX.md)** ← 163 instructions in 6 categories

**Contents**:

| Type | Count | Categories | Best For |
|------|-------|------------|----------|
| **🤖 Custom Agents** | 140 | Planning, Development, Testing, DevOps, Cloud, AI/ML | Specialized Copilot configurations |
| **🎯 Reusable Prompts** | 134 | Planning, Code Gen, Testing, Infrastructure, Database | Ready-to-use templates |
| **🎯 Agent Skills** | 63 | Various domains | Self-contained skill folders |
| **📋 Custom Instructions** | 163 | Language, Frameworks, Cloud, Data, Best Practices | Behavior customization |
| **📦 Collections** | 83 | Frontend, Partners, etc. | Curated resource sets |

**Quick Access by Category**:

**Planning & Architecture** (12 agents):
- `plan.agent.md` - Implementation planning
- `task-planner.agent.md` - Task breakdown
- `api-architect.agent.md` - API design
- `specification.agent.md` - Spec writing

**Development** (30+ agents):
- `expert-react-frontend-engineer.agent.md` - React expertise
- `expert-nextjs-developer.agent.md` - Next.js specialist
- `CSharpExpert.agent.md` - C# development
- `expert-dotnet-software-engineer.agent.md` - .NET expertise
- `rust-gpt-4.1-beast-mode.agent.md` - Rust expert

**DevOps & Infrastructure** (18 agents):
- `github-actions-expert.agent.md` - CI/CD workflows
- `terraform.agent.md` - Infrastructure as Code
- `platform-sre-kubernetes.agent.md` - K8s SRE

**Cloud Platforms** (15 agents):
- `azure-principal-architect.agent.md` - Azure architecture
- `bicep-plan.agent.md` - Bicep planning
- `terraform-azure-implement.agent.md` - Azure provisioning

**Testing & Quality** (8 agents):
- `tdd-red.agent.md`, `tdd-green.agent.md`, `tdd-refactor.agent.md` - TDD cycle
- `playwright-tester.agent.md` - E2E testing

**Usage Examples**:
```
# Reference an agent
@[external-libs/github-awesome-copilot/agents/plan.agent.md]
Create an implementation plan for my new feature

# Reference a prompt
@[external-libs/github-awesome-copilot/prompts/create-implementation-plan.prompt.md]
Generate a detailed implementation plan

# Copy to your workflows
Copy-Item "external-libs\github-awesome-copilot\agents\*.agent.md" ".agent\rules\"
```

**Integration**: Compatible with all AI coding assistants (GitHub Copilot, Claude, Gemini)

---

#### ✍️ AI Writing Framework (NEW)

**9. WriteHERE** (`external-libs/WriteHERE/`)
- **Files**: 50+ files
- **Repository**: [principia-ai/WriteHERE](https://github.com/principia-ai/WriteHERE)
- **License**: MIT (Open Source)
- **Status**: EMNLP 2025 Accepted (Oral Presentation)
- **Purpose**: Research-grade AI writing framework

**Key Features**:
- 🔄 **Recursive Task Decomposition**: Interleaves planning and execution
- 🎯 **Heterogeneous Tasks**: Integrates different task types
- 🧠 **Dynamic Adaptation**: Mimics human writing behavior
- 📈 **State-of-the-Art**: Outperforms traditional approaches

**Use Cases**:
- Fiction writing
- Technical report generation
- Long-form content creation
- Research paper drafting
- White papers and documentation

**Why It's Special**:
Unlike traditional AI writing tools, WriteHERE eliminates rigid workflows by allowing the AI to dynamically adjust its approach during the writing process—just like humans do.

---

#### 🔧 MCP Server Implementations

**Model Context Protocol (MCP)** - Extends Antigravity with external tools/data

**8. mcp-servers** (`external-libs/mcp-servers/`)
- **Files**: 125 server implementations
- **Purpose**: Core MCP server collection
- **Servers**: File system, database, API integrations
- **Setup**: `.mcp/README.md`

**9. PubMed-MCP-Server** (`external-libs/PubMed-MCP-Server/`)
- **Files**: 10 files
- **Purpose**: Medical research integration
- **Use**: Query PubMed database from Antigravity
- **Antigravity Call**:
  ```typescript
  // Access PubMed data in your code
  await mcp.callTool("pubmed_search", { query: "..." })
  ```

**10. entrez-mcp-server** (`external-libs/entrez-mcp-server/`)
- **Files**: 64 files
- **Purpose**: NCBI Entrez database access
- **Use**: Bioinformatics data retrieval

**11. mcp-scholarly** (`external-libs/mcp-scholarly/`)
- **Files**: 12 files
- **Purpose**: Academic paper search and retrieval
- **Integration**: Research paper access for code documentation

**12. p6xer-mcp-server** (`external-libs/p6xer-mcp-server/`)
- **Files**: 9 files
- **Purpose**: Primavera P6 project management integration
- **Use**: Project scheduling data access

**13. davinci-resolve-mcp** (`external-libs/davinci-resolve-mcp/`)
- **Files**: 84 files
- **Purpose**: Video editing automation
- **Integration**: Control DaVinci Resolve from code

**14. video-editing-mcp** (`external-libs/video-editing-mcp/`)
- **Files**: 25 files
- **Purpose**: Generic video editing tools
- **Use**: Video processing capabilities

---

#### 🔗 AI Framework Integrations

**15. langgraph** (`external-libs/langgraph/`)
- **Files**: 467 files
- **Purpose**: LangChain graph-based workflows
- **Contains**: State machines, multi-agent graphs, workflows
- **Antigravity Integration**: Advanced agent orchestration patterns
  ```python
  # Reference LangGraph patterns in your multi-agent systems
  # See: external-libs/langgraph/examples/
  ```

**16. vercel-agent-skills** (`external-libs/vercel-agent-skills/`)
- **Files**: 76 files
- **Purpose**: Vercel AI SDK integration patterns
- **Use**: Frontend AI integration techniques

---

#### 💡 How to Use with Antigravity

**Method 1: Reference in Prompts**
```markdown
@[external-libs/claude-cookbooks/tool_use/customer_service_agent.ipynb]

I'm building a similar customer service system. 
Use this pattern to implement tool calling in my FastAPI backend.
```

**Method 2: Copy Patterns**
```markdown
I need to implement [feature].

Review these resources and apply best patterns:
- external-libs/antigravity-awesome-skills/[relevant-skill]
- claude-cookbooks/patterns/[pattern]
- claude-subagents/categories/[domain]/[agent].md
```

**Method 3: MCP Tool Integration**
```markdown
Enable the PubMed MCP server from external-libs/PubMed-MCP-Server/
Then help me query medical research for my health app feature.
```

**Method 4: Learn from Examples**
```markdown
Show me how to implement multi-agent coordination.

Reference:
- langgraph examples in external-libs/langgraph/
- claude-cookbooks/patterns/
- Our skills/multi-agent-patterns-google-adk.md
```

---

#### 📊 External Libraries Statistics

| Library Type | Count | Total Files | Antigravity Ready |
|--------------|-------|-------------|-------------------|
| Antigravity-specific | 3 | ~3,800 | ✅ Native |
| Claude/Anthropic | 4 | ~800 | ✅ Compatible |
| **GitHub Copilot** | **1** | **~550** | **✅ Compatible** |
| **AI Writing** | **1** | **~50** | **✅ Research** |
| MCP Servers | 7 | ~330 | ✅ Via .mcp config |
| AI Frameworks | 2 | ~550 | ✅ Reference patterns |

**Total External Resources**: ~6,700+ files (was ~6,000)  
**Total Knowledge**: Claude + GitHub Copilot + MCP + AI frameworks + Writing tools

---

#### 🚀 Quick Start with External Libraries

**1. Explore Available Resources**:
```powershell
# List Antigravity skills
Get-ChildItem external-libs\antigravity-awesome-skills -Recurse -Filter "*.md"

# Browse Claude cookbooks
Get-ChildItem claude-cookbooks -Directory

# Check MCP servers
Get-ChildItem external-libs -Directory | Where-Object { $_.Name -match "mcp" }
```

**2. Setup MCP Servers** (Extends Antigravity capabilities):
```powershell
# Copy MCP config template
Copy-Item .mcp\claude_desktop_config_sample.json $env:APPDATA\Claude\claude_desktop_config.json

# Configure your needed MCP servers
# See: .mcp/README.md
```

**3. Reference in Your Work**:
```markdown
@[external-libs/antigravity-awesome-skills/debugging/advanced-debugging.md]
@[claude-cookbooks/tool_use/tool_chaining.ipynb]

Help me implement advanced debugging with tool chaining for my app
```

---

**🔗 Related Documentation**:
- MCP Setup: `.mcp/README.md`
- Antigravity Kit: `external-libs/antigravity-kit/README.md`
- Claude Cookbooks Guide: `claude-cookbooks/README.md`
- Subagents Catalog: `claude-subagents/README.md`



---

## 🎯 Common Tasks

### Task: Deploy to Azure
```
1. Read: .agent/workflows/deploying-to-aks.md
2. Reference: skills/kubernetes-resource-optimization-skills.md
3. Persona: @[.agent/rules/devops-persona.md]
```

### Task: Build Multi-Agent System
```
1. Read: skills/multi-agent-patterns-google-adk.md
2. Reference: white-papers/wp6-multi-agent-systems.md
3. Persona: @[.agent/rules/workflow-orchestrator-persona.md]
```

### Task: Debug MCP Server
```
1. Read: .agent/workflows/chrome-devtools-mcp-setup.md
2. Reference: skills/mcp-debugging-skills.md
3. Config: .mcp/claude_desktop_config_sample.json
```

### Task: Create AI Ethics Framework
```
1. Read: skills/constitutional-ai-anthropic.md
2. Reference: white-papers/wp1-agent-accountability-crisis.md

### Task: Prepare White Paper Images
```
1. Run: python scripts/extract_pdf_images.py
2. Workflow: .agent/workflows/white-paper-image-prep.md
3. Guide: white-papers/WATERMARK_REMOVAL_GUIDE.md
```
```

---

## 🔍 Search & Discovery

### Find a Workflow
```powershell
# Search by keyword
Get-ChildItem .agent\workflows -Filter "*deploy*"

# List all
Get-ChildItem .agent\workflows -Filter "*.md"
```

### Find a Skill
```powershell
# Search by topic
Get-ChildItem skills -Filter "*kubernetes*"

# List all
Get-ChildItem skills -Filter "*.md"
```

### Find Documentation
```powershell
# AI updates
Get-ChildItem docs\ai-updates

# Quickstart
Get-ChildItem docs\quickstart
```

---

## 📈 Workspace Statistics

**Total Directories**: 36  
**Total Files**: ~2,460  
**Total Size**: ~XXX MB

**Key Resources**:
- ✅ Workflows: 61
- ✅ Skills: 37
- ✅ Rules/Personas: 3
- ✅ White Papers: 7
- ✅ MCP Configs: 2
- ✅ External Libraries: 16

**Growth**: From 84 files → 2,460 files (2,829% growth)

---

## 🛠️ Maintenance

### Update AI Ecosystem
```
/@workflow-orchestrator claude-monitoring + documentation-maintenance
```

### Run Full Verification
```powershell
python scripts/checklist.py .
```

### Backup Workspace
```powershell
$timestamp = Get-Date -Format "yyyy-MM-dd-HHmm"
Copy-Item "." "d:\backup-kb-$timestamp" -Recurse
```

---

## 🔗 Quick Links

- **Main README**: [README.md](README.md)
- **Skill Index**: [skills/](skills/)
- **Workflow Index**: [.agent/workflows/](.agent/workflows/)
- **AI Updates**: [docs/ai-updates/](docs/ai-updates/)
- **Agent Personas**: [docs/AGENT_PERSONAS.md](docs/AGENT_PERSONAS.md)
- **Recommended Repos**: [docs/workspace/RECOMMENDED_GITHUB_REPOS.md](docs/workspace/RECOMMENDED_GITHUB_REPOS.md)

---

## 💡 Pro Tips

1. **Use Personas** - Reference personas for expert guidance
2. **Combine Resources** - Mix workflows + skills + personas for best results
3. **Check AI Updates** - Stay current with latest patterns (docs/ai-updates/)
4. **Leverage MCP** - Use MCP servers for extended capabilities
5. **Search First** - Likely solution already exists in 2,460 files

---

**🎯 Everything you need, one command away.**
