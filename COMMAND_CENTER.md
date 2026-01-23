# 🎯 COMMAND CENTER
**Dev Knowledge Base - Your Centralized Resource Hub**

Last Updated: 2026-01-23 | Total Resources: 2,460 files

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
**Count**: 3 personas

| Persona | Use For |
|---------|---------|
| [workflow-orchestrator](../.agent/rules/workflow-orchestrator-persona.md) | Complex workflows, state machines, process automation |
| [devops-engineer](../.agent/rules/devops-persona.md) | Infrastructure, deployments, CI/CD |
| [rules.md](../.agent/rules/rules.md) | DevOps agent guidelines |

**Quick Use**:
```
@[.agent/rules/workflow-orchestrator-persona.md]
Design a multi-step approval workflow
```

---

### 💡 Skills Library
**Location**: `skills/`  
**Count**: 37 production-tested skills

**Top Skills**:
- [multi-agent-patterns-google-adk.md](../skills/multi-agent-patterns-google-adk.md) - 8 multi-agent architectures
- [constitutional-ai-anthropic.md](../skills/constitutional-ai-anthropic.md) - AI ethics framework
- [mcp-debugging-skills.md](../skills/mcp-debugging-skills.md) - MCP troubleshooting
- [kubernetes-resource-optimization-skills.md](../skills/kubernetes-resource-optimization-skills.md) - K8s optimization
- [dapr-configuration-skills.md](../skills/dapr-configuration-skills.md) - Dapr setup

**Browse All**: [skills/](../skills/)

---

### ⚙️ Workflows
**Location**: `.agent/workflows/`  
**Count**: 61 executable workflows

**Categories**:

| Category | Count | Examples |
|----------|-------|----------|
| **Troubleshooting** | 20+ | cors-errors, deployment-issues, database-connection-issues |
| Development | 15+ | adding-new-feature, code-review-testing, create-project-schedule |
| **DevOps** | 10+ | deploying-to-aks, continuous-deployment-monitoring |
| **AI/Automation** | 5+ | apply-for-jobs, chat-testing, crewai-integration |
| **Documentation** | 5+ | documentation-maintenance, skill-upgrade |

**Slash Commands**:
```
/create      - Create new application
/debug       - Debug issues  
/deploy      - Deploy to production
/plan        - Create project plan
/test        - Run tests
/orchestrate - Multi-agent coordination
```

**Browse All**: [.agent/workflows/](../.agent/workflows/)

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
**Total**: 16 major libraries | ~6,000+ files  
**Purpose**: Extended capabilities for Google Antigravity AI coding assistant

---

#### 🤖 Antigravity-Specific Libraries

**1. antigravity-awesome-skills** (`external-libs/antigravity-awesome-skills/`)
- **Files**: 1,872 files
- **Purpose**: Curated skill collection optimized for Antigravity
- **Contains**: Advanced coding patterns, debugging techniques, architecture skills
- **Use with Antigravity**: Reference in prompts for enhanced code generation
  ```
  @[external-libs/antigravity-awesome-skills/[skill-name]]
  ```

**2. antigravity-kit** (`external-libs/antigravity-kit/`)
- **Files**: 278 files  
- **Purpose**: Toolkit and utilities for Antigravity workflows
- **Contains**: Project templates, automation scripts, configuration helpers
- **Use**: Bootstrap new projects with proven patterns

**3. gemini-cli** (`external-libs/gemini-cli/`)
- **Files**: 1,643 files
- **Purpose**: Gemini CLI integration for Antigravity
- **Contains**: Command-line tools, API wrappers, documentation
- **Integration**: CLI tools callable from Antigravity tasks

---

#### 🎭 Claude/Anthropic Resources

**4. claude-cookbooks** (`claude-cookbooks/`)
- **Files**: 416 files (20 categories)
- **Purpose**: Official Anthropic Claude implementation guides
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
| MCP Servers | 7 | ~330 | ✅ Via .mcp config |
| AI Frameworks | 2 | ~550 | ✅ Reference patterns |

**Total External Resources**: ~6,000+ files  
**Total Knowledge**: Claude best practices + MCP tools + AI frameworks

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

- **Main README**: [README.md](../README.md)
- **Skill Index**: [skills/](../skills/)
- **Workflow Index**: [.agent/workflows/](../.agent/workflows/)
- **AI Updates**: [docs/ai-updates/](../docs/ai-updates/)
- **Agent Personas**: [docs/AGENT_PERSONAS.md](../docs/AGENT_PERSONAS.md)
- **Recommended Repos**: [docs/workspace/RECOMMENDED_GITHUB_REPOS.md](../docs/workspace/RECOMMENDED_GITHUB_REPOS.md)

---

## 💡 Pro Tips

1. **Use Personas** - Reference personas for expert guidance
2. **Combine Resources** - Mix workflows + skills + personas for best results
3. **Check AI Updates** - Stay current with latest patterns (docs/ai-updates/)
4. **Leverage MCP** - Use MCP servers for extended capabilities
5. **Search First** - Likely solution already exists in 2,460 files

---

**🎯 Everything you need, one command away.**
