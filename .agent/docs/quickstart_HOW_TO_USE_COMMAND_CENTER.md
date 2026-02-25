# 🚀 QUICK START GUIDE
**How to Use Your Knowledge Base Command Center**

**Time to read**: 5 minutes | **Skill level**: Beginner

---

## 📖 What is the Command Center?

The Command Center is your **main navigation hub** - think of it as the table of contents for your entire knowledge base. It helps you quickly find and use:
- Workflows (how to do something step-by-step)
- Skills (reusable techniques and patterns)
- Personas (AI expert roles for different tasks)
- Documentation and resources

---

## 🎯 How to Use It (3 Methods)

### Method 1: Browse Visually 👀
**Best for**: Exploring what's available

1. **Open the Command Center**:
   - File: `d:\my-dev-knowledge-base\COMMAND_CENTER.md`
   - Or click the link at top of `README.md`

2. **Browse categories**:
   - Scroll through sections (Personas, Skills, Workflows, etc.)
   - Click any link to open that resource
   - Example: Click `[workflow-orchestrator](../.agent/rules/workflow-orchestrator-persona.md)`

---

### Method 2: Search for What You Need 🔍
**Best for**: Finding specific solutions

**Use the Smart Search Script**:
```powershell
# Search everything
cd d:\my-dev-knowledge-base
.\scripts\search.ps1 "kubernetes"

# Search only workflows
.\scripts\search.ps1 "deployment" -Type workflow

# Search only skills
.\scripts\search.ps1 "security" -Type skill

# Search only personas
.\scripts\search.ps1 "ml engineer" -Type persona
```

**Results show**:
- File name
- Location path
- Preview of matching content
- Line number

---

### Method 3: Common Task Patterns 🛠️
**Best for**: Getting work done quickly

---

## 📚 Practical Examples

### Example 1: Deploy to Azure Kubernetes
**Goal**: Deploy your app to AKS

**Steps**:
1. **Find the workflow**:
   ```powershell
   .\scripts\search.ps1 "deploying aks" -Type workflow
   ```

2. **Open the workflow**:
   - File: `.agent\workflows\deploying-to-aks.md`

3. **Use DevOps persona for guidance**:
   - Open: `.agent\rules\devops-persona.md`
   - Or reference in your AI chat:
   ```
   @[.agent/rules/devops-persona.md]
   
   Help me deploy to AKS following the deploying-to-aks workflow
   ```

4. **Reference K8s skills as needed**:
   - `skills\kubernetes-resource-optimization-skills.md`

---

### Example 2: Build a Multi-Agent System
**Goal**: Create a system with multiple AI agents working together

**Steps**:
1. **Start with the skill**:
   - File: `skills\multi-agent-patterns-google-adk.md`
   - Read the 8 patterns available

2. **Use the right persona**:
   ```
   @[.agent/rules/agent-organizer.md]
   
   I need to build a multi-agent system for [your use case].
   Use the patterns from skills/multi-agent-patterns-google-adk.md
   ```

3. **Reference white paper for theory**:
   - `white-papers\wp6-multi-agent-systems.md`

4. **Use workflow orchestrator persona**:
   ```
   @[.agent/rules/workflow-orchestrator-persona.md]
   
   Design the workflow coordination for these agents
   ```

---

### Example 3: Audit Security
**Goal**: Perform comprehensive security audit

**Steps**:
1. **Use security persona**:
   ```
   @[.agent/rules/security-auditor.md]
   
   Conduct security audit of my microservices architecture
   ```

2. **Reference MCP config if needed**:
   - `.mcp\claude_desktop_config_sample.json`

3. **Check debugging skills**:
   - `skills\mcp-debugging-skills.md`

---

### Example 4: Optimize ML Model Performance
**Goal**: Improve ML model serving performance

**Steps**:
1. **Use ML engineer persona**:
   ```
   @[.agent/rules/ml-engineer.md]
   
   Optimize my PyTorch model for production serving
   ```

2. **Search for related workflows**:
   ```powershell
   .\scripts\search.ps1 "performance" -Type workflow
   ```

3. **Reference skills**:
   - Look in COMMAND_CENTER.md → Skills Library section
   - Find performance-related skills

---

### Example 5: Fix CORS Errors
**Goal**: Resolve CORS issues in your app

**Quick Search Approach**:
```powershell
# 1. Find the workflow
.\scripts\search.ps1 "cors" -Type workflow

# 2. Output shows:
# File: cors-errors.md
# Location: .agent\workflows\cors-errors.md
# Line: 15 - "Fix 'Access to fetch blocked by CORS policy' errors..."

# 3. Open that file and follow steps
```

**Or Browse Approach**:
1. Open `COMMAND_CENTER.md`
2. Scroll to "Workflows" section
3. Look under "Troubleshooting" category
4. Find "cors-errors"
5. Click the link

---

## 🎭 How to Use Personas

Personas are like **expert consultants** in specific domains.

### Basic Usage
```markdown
@[.agent/rules/[persona-name].md]

[Your question or task]
```

### Available Personas

| Persona | When to Use | Example |
|---------|-------------|---------|
| `workflow-orchestrator` | Complex multi-step processes | "Design approval workflow with rollback" |
| `devops-persona` | Infrastructure, deployments | "Deploy app to AKS with zero downtime" |
| `agent-organizer` | Multi-agent coordination | "Organize 5 agents to build this feature" |
| `security-auditor` | Security audits, compliance | "Audit for OWASP Top 10 vulnerabilities" |
| `ml-engineer` | ML model deployment, MLOps | "Set up model serving with auto-scaling" |

### Example Persona Usage
```markdown
@[.agent/rules/security-auditor.md]

I have a FastAPI backend with PostgreSQL database.
Need to:
1. Implement OAuth 2.0 authentication
2. Ensure GDPR compliance
3. Set up automated security scanning

Please provide implementation plan.
```

---

## 💡 Power User Tips

### Tip 1: Combine Resources
```markdown
@[.agent/rules/devops-persona.md]
@[.agent/workflows/deploying-to-aks.md]

Using the DevOps persona and following the AKS deployment workflow,
help me deploy with these custom requirements: [list requirements]
```

### Tip 2: Quick Search Aliases
Create PowerShell aliases for faster search:
```powershell
# Add to your PowerShell profile
function Search-KB { .\scripts\search.ps1 $args }
function Search-Workflow { .\scripts\search.ps1 $args -Type workflow }
function Search-Skill { .\scripts\search.ps1 $args -Type skill }

# Then use:
Search-KB "kubernetes"
Search-Workflow "deployment"
Search-Skill "security"
```

### Tip 3: Bookmark Common Paths
Keep these locations handy:
- **Workflows**: `.agent\workflows\`
- **Skills**: `skills\`
- **Personas**: `.agent\rules\`
- **Docs**: `docs\`

---

## 📊 Workspace Structure Summary

```
d:\my-dev-knowledge-base\
│
├── COMMAND_CENTER.md          ← START HERE! (Main hub)
├── README.md                   ← Overview and stats
│
├── .agent\
│   ├── rules\                 ← 6 expert personas
│   └── workflows\             ← 61 step-by-step guides
│
├── skills\                    ← 37 reusable techniques
├── white-papers\              ← 7 research papers
├── docs\                      ← Documentation
│   ├── quickstart\           ← This guide!
│   ├── ai-updates\           ← AI ecosystem tracking
│   └── workspace\            ← Stats and resources
│
└── scripts\
    ├── search.ps1            ← Smart search tool
    └── auto-backup.ps1       ← Automated backups
```

---

## 🆘 Troubleshooting

**Q: "I can't find what I'm looking for"**
- Try the search script: `.\scripts\search.ps1 "your-query"`
- Browse COMMAND_CENTER.md categories
- Check the workflow index: `.agent\workflows\README.md`

**Q: "How do I know which persona to use?"**
- See persona catalog: `docs\AGENT_PERSONAS.md`
- Or check COMMAND_CENTER.md → "AI Personas & Rules" section

**Q: "Can I use multiple personas together?"**
- Yes! Reference multiple personas in one request:
  ```
  @[.agent/rules/security-auditor.md]
  @[.agent/rules/ml-engineer.md]
  
  Design secure ML model serving architecture
  ```

**Q: "Search script doesn't work"**
- Make sure you're in the knowledge base directory:
  ```powershell
  cd d:\my-dev-knowledge-base
  .\scripts\search.ps1 "query"
  ```

---

## ✅ Quick Reference Card

| I Want To... | Do This |
|--------------|---------|
| **Browse everything** | Open `COMMAND_CENTER.md` |
| **Find something specific** | `.\scripts\search.ps1 "keywords"` |
| **Deploy to cloud** | Search workflows: `.\scripts\search.ps1 "deploy" -Type workflow` |
| **Use expert guidance** | Reference persona: `@[.agent/rules/[name].md]` |
| **Learn AI patterns** | Read skills: `skills\multi-agent-patterns-google-adk.md` |
| **Troubleshoot issue** | Search workflows in troubleshooting section |
| **See all personas** | `docs\AGENT_PERSONAS.md` (145 available!) |
| **Get stats** | `docs\workspace\WORKSPACE_STATS.md` |

---

## 🚀 Your First Task

**Try this now** (2 minutes):

1. **Search for something**:
   ```powershell
   cd d:\my-dev-knowledge-base
   .\scripts\search.ps1 "your-favorite-topic"
   ```

2. **Open the command center**:
   - File: `d:\my-dev-knowledge-base\COMMAND_CENTER.md`
   - Scroll through and see what's available

3. **Try a persona**:
   ```
   @[.agent/rules/devops-persona.md]
   
   Explain what you can help me with
   ```

**That's it!** You're now ready to use your knowledge base effectively! 🎉

---

**Still confused?** Open `COMMAND_CENTER.md` and just start clicking links to explore!
