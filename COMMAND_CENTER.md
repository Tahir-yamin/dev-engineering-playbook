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

### 📦 External Libraries

| Library | Location | Files | Purpose |
|---------|----------|-------|---------|
| Claude Cookbooks | `claude-cookbooks/` | 416 | Official Anthropic guides |
| Claude Skills | `claude-skills-library/` | 50+ | Community skills |
| Claude Subagents | `claude-subagents/` | 137 | Specialized agents |
| Dapr Quickstarts | `dapr-quickstarts/` | 1,223 | Dapr examples |
| MCP Servers | `external-libs/` | 16 libs | MCP server implementations |

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
