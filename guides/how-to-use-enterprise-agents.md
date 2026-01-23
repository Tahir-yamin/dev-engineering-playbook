# 🚀 How to Use Enterprise Agents - Quick Start

**5-Minute Guide to Using Meta-Orchestration Agents**

---

## ⚡ Super Quick Start (30 seconds)

### Option 1: Drag & Drop
1. Open your AI tool (Claude Desktop, Cursor, etc.)
2. Drag this file into chat: `.agent/agents/workflow-orchestrator.md`
3. Ask: `"Create a deployment workflow for my app"`
4. Done! ✅

### Option 2: @ Mention (Claude Code/Cline)
```markdown
@workflow-orchestrator "Create a deployment pipeline"
```

---

## 📁 Where Are The Agents?

**Location**: `d:\my-dev-knowledge-base\.agent\agents\`

**Top 3 to Start With**:
1. **workflow-orchestrator.md** - Business automation
2. **multi-agent-coordinator.md** - Coordinate multiple agents
3. **task-distributor.md** - Smart work allocation

---

## 🎯 Common Use Cases

### 1️⃣ **Build a Feature** (5 min)
```markdown
@multi-agent-coordinator

"I need to build a user authentication feature. Coordinate:
- backend-developer: Create auth API
- frontend-developer: Build login UI
- security-specialist: Add encryption
- qa-engineer: Write tests"
```

### 2️⃣ **Create Workflow** (3 min)
```markdown
@workflow-orchestrator

"Create a customer onboarding workflow:
1. User registers
2. Email verification
3. Profile setup
4. Welcome email
5. Dashboard access

Include error handling and retry logic"
```

### 3️⃣ **Distribute Tasks** (2 min)
```markdown
@task-distributor

"I have 15 tasks and 5 developers. Distribute optimally considering:
- Developer skills
- Current workload
- Task dependencies"
```

---

## 💡 Pro Tips

### ✅ **Do's**:
- Start with one agent
- Be specific about requirements
- Mention dependencies
- Ask for error handling

### ❌ **Don'ts**:
- Don't use multiple agents for simple tasks
- Don't forget to specify constraints
- Don't skip error handling

---

## 🔥 Power Moves

### **Combine Agents**:
```markdown
# Step 1: Design
@workflow-orchestrator "Design the process"

# Step 2: Execute
@multi-agent-coordinator "Execute with these agents..."

# Step 3: Monitor
@performance-monitor "Track metrics"
```

### **Save State**:
```markdown
@context-manager "Save current pipeline state"

# Resume later:
@context-manager "Resume from last checkpoint"
```

---

## 📚 Learn More

- **Full Guide**: `skills/enterprise-meta-orchestration-guide.md`
- **All Agents**: `.agent/agents/` (11 installed)
- **Complete Collection**: `external-libs/awesome-claude-code-subagents/` (137 agents!)

---

## 🆘 Troubleshooting

**Agent not found?**
- Check path: `.agent/agents/workflow-orchestrator.md`
- Verify file exists: `ls .agent/agents/`

**Not working?**
- Try drag & drop instead of @ mention
- Copy-paste agent content directly
- Restart your AI tool

---

**That's it! Start with workflow-orchestrator and experiment!** 🎉
