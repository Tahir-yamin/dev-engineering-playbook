---
description: Master workflow orchestrator - Run single or combined workflows with one command
---

# Workflow Orchestrator

**Purpose**: Easily invoke single or combined workflows  
**Use**: `/@workflow-orchestrator` then specify which workflows to run

---

## 🚀 Quick Commands

### Single Workflows

```
/@workflow-orchestrator claude-monitoring
/@workflow-orchestrator documentation-maintenance  
/@workflow-orchestrator skill-upgrade
```

### Combined Workflows

```
/@workflow-orchestrator claude-monitoring + documentation-maintenance
/@workflow-orchestrator skill-upgrade + documentation-maintenance
```

---

## 📋 Available Workflows

### 1. Claude Monitoring (`claude-monitoring`)

**What it does**: Monitors Claude AI updates from X/Twitter and GitHub  
**Duration**: ~15-20 minutes  
**Output**: Knowledge base + summary report + backups

**Runs**:
- Scan 8 X/Twitter accounts
- Check 12 GitHub repositories
- Extract technical details
- Generate reports
- Create backups

**Invoke**: `/@workflow-orchestrator claude-monitoring`

---

### 2. Documentation Maintenance (`documentation-maintenance`)

**What it does**: Updates skills, workflows, and knowledge base  
**Duration**: ~10-15 minutes  
**Output**: New/updated skill files, workflow files

**Runs**:
- Create new skills from recent learnings
- Update workflow files
- Sync to GitHub knowledge base
- Update indexes
- Commit changes

**Invoke**: `/@workflow-orchestrator documentation-maintenance`

---

### 3. Skill Upgrade (`skill-upgrade`)

**What it does**: Guides through systematic skill upgrading  
**Duration**: Variable (learning-based)  
**Output**: Learning notes, implemented features

**Runs**:
- Path selection (Core Stack, DevOps, AI, Architecture)
- Study recommended repos
- Implement learning project
- Document learnings

**Invoke**: `/@workflow-orchestrator skill-upgrade`

---

## 🔗 Workflow Combinations

### Recommended Combinations

#### **Full Knowledge Update** (Most Common)
```
/@workflow-orchestrator claude-monitoring + documentation-maintenance
```

**What happens**:
1. ✅ Monitor Claude ecosystem for updates
2. ✅ Extract new skills, subagents, workflows
3. ✅ Document findings in knowledge base
4. ✅ Create skill files for reusable patterns
5. ✅ Update workflow files
6. ✅ Commit everything to git

**Duration**: ~30 minutes  
**Frequency**: Every 48 hours

---

#### **Learning Session**
```
/@workflow-orchestrator skill-upgrade + documentation-maintenance
```

**What happens**:
1. ✅ Follow skill upgrade path
2. ✅ Implement learning project
3. ✅ Document lessons learned
4. ✅ Create skills from new knowledge
5. ✅ Update workflow files
6. ✅ Commit changes

**Duration**: 2-4 hours  
**Frequency**: Weekly/biweekly

---

## 📝 Workflow Execution Templates

### Template A: Claude Monitoring Only

```markdown
**WORKFLOW**: Claude Monitoring

**STEPS**:
1. Monitor X/Twitter accounts: @AnthropicAI, @claudeai, @bcherny, @adocomplete, etc.
2. Check GitHub repos: anthropics/skills, wshobson/agents, VoltAgent, etc.
3. Extract technical details (YAML, code examples, configs)
4. Update claude_updates_knowledge_base.md
5. Generate claude_update_report_YYYY-MM-DD.md
6. Create backups in ~/Documents/ClaudeUpdates/
7. Update claude_update_log.md

**DELIVERABLES**:
- Knowledge base (updated)
- Summary report (new)
- Backups (timestamped)
- Log entry

**REFERENCE**: @workflows/monitor-claude-updates.md
```

---

### Template B: Full Knowledge Update (Combined)

```markdown
**WORKFLOW**: Claude Monitoring + Documentation Maintenance

**STEPS**:

**Phase 1: Monitoring (15-20 min)**
1. Monitor X/Twitter accounts
2. Check GitHub repositories
3. Extract technical details
4. Generate reports and backups

**Phase 2: Documentation (10-15 min)**
5. Identify new skills from findings
6. Create/update skill files in skills/
7. Create/update workflows in workflows/
8. Update indexes (skills.md, README.md)
9. Cross-reference related docs
10. Commit all changes to git

**DELIVERABLES**:
- Knowledge base (updated)
- Summary report (new)
- New/updated skill files
- New/updated workflow files
- Git commit with all changes

**REFERENCES**: 
- @workflows/monitor-claude-updates.md
- @agents/workflows/documentation-maintenance.md
```

---

### Template C: Skill Upgrade + Documentation

```markdown
**WORKFLOW**: Skill Upgrade + Documentation Maintenance

**STEPS**:

**Phase 1: Learning (2-4 hours)**
1. Choose skill path (Core Stack, DevOps, AI, Architecture)
2. Study recommended repositories
3. Implement learning project
4. Take notes on challenges and solutions

**Phase 2: Documentation (10-15 min)**
5. Create skill file for new knowledge
6. Document gotchas and solutions
7. Create workflow if repeatable process
8. Update indexes
9. Commit changes to git

**DELIVERABLES**:
- Learning notes (docs/learning/)
- New skill files
- Updated workflows
- Git commit

**REFERENCES**:
- @agents/workflows/skill-upgrade.md
- @agents/workflows/documentation-maintenance.md
```

---

## 🎯 How to Use

### Step 1: Choose Your Workflow

Decide what you need:
- **Just monitoring?** → Use Template A
- **Monitoring + document findings?** → Use Template B (Recommended)
- **Learning new skills?** → Use Template C

### Step 2: Invoke the Workflow

**Single workflow**:
```
I need to run the Claude monitoring workflow.
Use: @workflow-orchestrator claude-monitoring
```

**Combined workflow**:
```
I need to run Claude monitoring and document the findings.
Use: @workflow-orchestrator claude-monitoring + documentation-maintenance
```

### Step 3: Let the AI Execute

The AI will:
1. Understand which workflows to run
2. Execute them in sequence
3. Use the appropriate templates
4. Generate all deliverables
5. Commit changes
6. Provide summary

---

## 🔄 Recurring Workflows

### Every 48 Hours
```
/@workflow-orchestrator claude-monitoring + documentation-maintenance
```

Set a calendar reminder:
- **Event**: "Run Claude Updates"
- **Frequency**: Every 2 days
- **Action**: Message the AI with the command above

### Weekly
```
/@workflow-orchestrator skill-upgrade + documentation-maintenance
```

Set a calendar reminder:
- **Event**: "Weekly Skill Learning"
- **Frequency**: Every Monday
- **Action**: Message the AI with the command above

---

## 📊 Workflow Status Tracking

After each workflow run, the AI will update:

**For Claude Monitoring**:
- `claude_update_log.md` - Execution history
- `claude_updates_knowledge_base.md` - Cumulative knowledge
- Timestamped reports

**For Documentation Maintenance**:
- Git commit messages
- Updated indexes
- Cross-references

**For Skill Upgrade**:
- `docs/learning/` notes
- New skill files
- Updated workflows

---

## 💡 Pro Tips

### Tip 1: Use Combined Workflows
Always combine `claude-monitoring` with `documentation-maintenance` to ensure findings are properly documented.

### Tip 2: Set Reminders
Use calendar reminders for recurring workflows. The AI cannot auto-schedule.

### Tip 3: Review Deliverables
After workflow execution, the AI will provide paths to review. Check them to ensure quality.

### Tip 4: Customize Templates
Feel free to modify the templates in this file for your specific needs.

### Tip 5: Chain Multiple Workflows
You can chain 3+ workflows if needed:
```
/@workflow-orchestrator claude-monitoring + skill-upgrade + documentation-maintenance
```

---

## 🚨 Troubleshooting

**Q: The AI doesn't understand my command**  
A: Use the exact format: `/@workflow-orchestrator [workflow-name]`

**Q: Can I skip parts of a workflow?**  
A: Yes, specify: "Run claude-monitoring but skip the backup step"

**Q: How do I know what workflows are available?**  
A: Check the "Available Workflows" section above or list files in `workflows/` and `agents/workflows/`

**Q: Can I create my own workflow?**  
A: Yes! Follow `@agents/workflows/documentation-maintenance.md` to create a new workflow file.

---

## 📚 Related Documentation

- [Monitor Claude Updates Workflow](file:///d:/Hackathon%20phase%201%20TODO%20App/todo_hackathon_phase1/my-dev-knowledge-base/workflows/monitor-claude-updates.md)
- [Documentation Maintenance Workflow](file:///d:/Hackathon%20phase%201%20TODO%20App/todo_hackathon_phase1/my-dev-knowledge-base/agents/workflows/documentation-maintenance.md)
- [Skill Upgrade Workflow](file:///d:/Hackathon%20phase%201%20TODO%20App/todo_hackathon_phase1/my-dev-knowledge-base/agents/workflows/skill-upgrade.md)

---

## 🎓 Example Usage

### Scenario 1: Regular Monitoring
**You**: `/@workflow-orchestrator claude-monitoring + documentation-maintenance`

**AI executes**:
- Scans all X accounts and GitHub repos
- Generates knowledge base and reports
- Creates skill files for new patterns found
- Updates workflows
- Commits everything to git
- Provides summary with paths to review

---

### Scenario 2: Learning Session
**You**: `/@workflow-orchestrator skill-upgrade` (Path B: AI Engineering)

**AI guides you**:
- Recommends repos to study (LangChain, LlamaIndex)
- Suggests implementing a RAG pipeline
- Helps document learnings
- Creates skill files for new knowledge

Then you run:
**You**: `/@workflow-orchestrator documentation-maintenance`

**AI finalizes**:
- Converts your notes into skills
- Updates indexes
- Commits changes

---

**Created**: 2026-01-08  
**Version**: 1.0  
**Supports**: Single and combined workflow execution
