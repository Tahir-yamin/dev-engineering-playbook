# 🚀 Quick Start Guide - Your Dev Knowledge Base

**Your Workspace**: 2,460 files | Complete consolidation | Enterprise-grade  
**Last Updated**: 2026-01-19

> **🆕 Latest Update (Jan 19, 2026)**: Complete workspace consolidation! 2,460 files unified from multiple sources. 51 workflows, 933 agent files. See `claude_update_log.md` for details.

---

## 📚 Table of Contents

1. [Quick Command Reference](#quick-command-reference)
2. [Finding What You Need](#finding-what-you-need)
3. [Common Project Scenarios](#common-project-scenarios)
4. [Workflow Cheat Sheet](#workflow-cheat-sheet)
5. [File Structure at a Glance](#file-structure-at-a-glance)

---

## ⚡ Quick Command Reference

### When Starting a Project

```bash
# Message me:
"I'm starting a new [project type]. Which skills and agents should I use?"

# Or browse:
Open: skills/INDEX.md  # Find relevant skills by category
Open: agents/INDEX.md  # Find agents for your tech stack
```

### When You Hit a Problem

```bash
# Message me:
"I'm having [specific problem]. Which workflow should I use?"

# Or search workflows:
Open: agents/workflows/  # Browse your original 24 workflows
Open: workflows/shinpr/  # Browse 127 production workflows
```

### When You Need an Agent

```bash
# Message me:
"I need an agent for [task]"

# Examples:
"I need an agent for backend API development"
"I need an agent for frontend React work"
"I need an agent for database optimization"

# I'll point you to the right one from 925+ agents
```

### When You Want to Learn

```bash
# Message me:
"Teach me about [topic]"

# Or run:
/@workflow-orchestrator skill-upgrade

# Browse skills by topic:
- skills/official_anthropic/  # Official Anthropic patterns
- skills/alirezarezvani/      # Business function skills
- skills/SKILL_PATH_*.md      # Your learning paths
```

### Regular Maintenance

```bash
# Every week - Check Claude ecosystem updates:
Open: claude_update_report_2026-01-13.md  # Latest AI trends

# When you learn something new:
/@workflow-orchestrator documentation-maintenance

# Weekly review:
"Show me what's new in my workspace"
```

---

## 🔍 Finding What You Need

### By Problem Type

| Your Need | Where to Look | Quick Open |
|-----------|---------------|------------|
| **Authentication issues** | Your workflows | [authentication-issues.md](agents/workflows/authentication-issues.md) |
| **Docker problems** | Your workflows | [docker-container-problems.md](agents/workflows/docker-container-problems.md) |
| **Database errors** | Your workflows | [database-connection-issues.md](agents/workflows/database-connection-issues.md) |
| **API development** | wshobson agents | `agents/wshobson/backend-development/` |
| **Frontend work** | shinpr workflows | `workflows/shinpr/frontend/` |
| **Cloud/DevOps** | wshobson agents | `agents/wshobson/cloud-infrastructure/` |

**💡 To drag files into chat**: Copy the path, add `@[` before and `]` after  
Example: `@[agents/workflows/authentication-issues.md]` → Drag this into chat!

### By Technology

| Technology | Resource | Path |
|------------|----------|------|
| **Next.js** | Your skill path | [SKILL_PATH_0_CORE_STACK.md](skills/SKILL_PATH_0_CORE_STACK.md) |
| **Docker** | Your guide | [GORDON-AI-GUIDE.md](guides/docker/GORDON-AI-GUIDE.md) |
| **Kubernetes** | Your guides + wshobson | `guides/kubernetes/` + `agents/wshobson/kubernetes/` |
| **Python** | tresor + wshobson | `agents/tresor/subagents/` + workflows |
| **React** | shinpr workflows | `workflows/shinpr/frontend/` |

### By Role/Function

| Role | Skills to Use | Path |
|------|---------------|------|
| **Developer** | Engineering skills | `skills/alirezarezvani/engineering/` |
| **Manager** | Project management | `skills/alirezarezvani/project-management/` |
| **Executive** | C-level advisor | `skills/alirezarezvani/c-level/` |
| **Marketing** | Marketing skills | `skills/alirezarezvani/marketing/` |
| **Product** | Product team | `skills/alirezarezvani/product/` |

---

## 💼 Common Project Scenarios

### Scenario 1: Building a New Feature

**What to do**:
```bash
1. Message me: "I'm building [feature name]. Guide me through the process."

2. I'll help you:
   - Choose the right workflow from shinpr or wshobson
   - Select appropriate agents
   - Apply relevant skills
   - Follow best practices

3. After completion:
   /@workflow-orchestrator documentation-maintenance
```

### Scenario 2: Fixing a Bug

**What to do**:
```bash
1. Identify problem category:
   - Build failure? → [build-failures.md](agents/workflows/build-failures.md)
   - Auth issue? → [authentication-issues.md](agents/workflows/authentication-issues.md)
   - Performance? → agents/wshobson/application-performance/
   
2. Follow the workflow step-by-step

3. If workflow doesn't exist:
   Message me: "I fixed [problem]. Help me document this."
```

### Scenario 3: Learning a New Technology

**What to do**:
```bash
1. Run: /@workflow-orchestrator skill-upgrade

2. I'll ask which path you want (DevOps, AI, Architecture, etc.)

3. I'll guide you through:
   - Recommended skills to study
   - Practice projects to build
   - Documentation to create
   
4. Your learning gets added to the knowledge base
```

### Scenario 4: Code Review

**What to do**:
```bash
1. Use: [code-review-testing.md](agents/workflows/code-review-testing.md)

2. Or message me: "Review this code: [paste code or file path]"

3. I'll apply best practices from:
   - Your documented standards
   - Community best practices
   - Security guidelines
```

### Scenario 5: Deploying to Production

**What to do**:
```bash
1. Checklist: [deployment-issues.md](agents/workflows/deployment-issues.md)

2. Use deployment workflow: 
   - wshobson CI/CD automation
   - Your deployment guides
   
3. Verify with: [complete-application-qa.md](agents/workflows/complete-application-qa.md)
```

---

## 💼 Job Application Automation

### Quick Apply Commands

```bash
# Full automation - search jobs, generate CV, cover letter, apply
/@apply-for-jobs

# Apply to specific company (email)
python job-application/scripts/apply_job.py --company "AECOM" --role "Project Controls Manager" --email "hr@aecom.com"

# Apply to website (generates form data)
python job-application/scripts/apply_job.py --company "AECOM" --role "Project Controls Manager" --website

# View application stats
python job-application/scripts/job_scraper.py --stats

# Check recent job listings with URLs
Open: job-application/data/recent_jobs.md
```

**⚠️ URL Verification Required:**
- Always check the link works before using `--url` parameter
- Use stable portal links from `job-application/data/job_apply_links.md`
- Deep job ID links expire quickly; prefer company career homepage URLs

### Files Location

| File | Purpose |
|------|---------|
| `job-application/generated/` | All CVs, Cover Letters, Form Data |
| `job-application/data/recent_jobs.md` | 30+ recent jobs with apply URLs |
| `job-application/data/applications_log.json` | Track applied jobs (avoid duplicates) |
| `job-application/data/master_profile.json` | Your profile data |

### Current Stats

- **18 applications ready** (CVs + Cover Letters + Form Data)
- **30+ job listings** with direct apply links
- **16 Tier-1 companies** tracked (ADNOC, AECOM, Jacobs, etc.)

---

## 📋 Workflow Cheat Sheet

**Fresh workspace?**
```
"Run /ai-ecosystem-monitoring to find latest AI tools"
```

**Push failed?**
```
"Run /git-push-large-files"
```

### Quick Invocation Commands

```bash
# Claude Monitoring (every 48 hours)
/@workflow-orchestrator claude-monitoring + documentation-maintenance

# Update Documentation (weekly or after major changes)
/@workflow-orchestrator documentation-maintenance

# Learn New Skill (when needed)
/@workflow-orchestrator skill-upgrade

# Combined: Learn + Document
/@workflow-orchestrator skill-upgrade + documentation-maintenance

# Custom combinations (ask me)
"Run [workflow1] + [workflow2] workflows"
```

### Workflow by Need

| When You... | Use This Workflow |
|-------------|-------------------|
| Solve a NEW problem | `/@workflow-orchestrator documentation-maintenance` → Create new workflow |
| Learn something | `/@workflow-orchestrator skill-upgrade` |
| Start new project | [starting-new-project.md](agents/workflows/starting-new-project.md) |
| Add new feature | [adding-new-feature.md](agents/workflows/adding-new-feature.md) |
| Hit Docker issue | [docker-container-problems.md](agents/workflows/docker-container-problems.md) |
| Database problem | [database-connection-issues.md](agents/workflows/database-connection-issues.md) |
| Security concern | [security-audit.md](agents/workflows/security-audit.md) |
| Performance issue | [performance-problems.md](agents/workflows/performance-problems.md) |

---

## 📁 File Structure at a Glance

```
my-dev-knowledge-base/ (2,460 files)
│
├── 🎯 START HERE
│   ├── README.md                    ← Overview & stats
│   ├── WORKSPACE_STATS.md           ← Detailed breakdown
│   ├── QUICKSTART_GUIDE.md          ← This file!
│   ├── DRAG_INTO_CHAT.md            ← Quick file references
│   └── See all files linked below ↓
│
├── 📚 .agent/workflows/ (51 files)
│   ├── workflow-orchestrator.md     ← Master orchestrator
│   ├── documentation-maintenance.md ← Keep docs updated
│   ├── authentication-issues.md     ← Fix auth problems
│   ├── docker-container-problems.md ← Docker troubleshooting
│   ├── deployment-issues.md         ← Deployment help
│   └── [46 more workflows...]       ← Complete collection
│
├── 🤖 agents/ (933 files)
│   ├── wshobson/                    ← Multi-tier agents
│   ├── tresor/                      ← 133 subagents, 19 commands
│   ├── subagents/                   ← Categorized subagents
│   └── [more agent files...]        ← Comprehensive collection
│
├── 📚 External Libraries
│   ├── claude-cookbooks/            ← Official cookbooks
│   ├── claude-skills-library/       ← Skills library
│   ├── claude-subagents/            ← Subagent patterns
│   └── dapr-quickstarts/            ← Dapr examples
│
├── 📖 guides/
│   ├── kubernetes/                  ← K8s guides
│   ├── docker/                      ← Docker guides
│   └── [more guides...]             ← Growing collection
│
├── � Documentation
│   ├── docs/                        ← All project docs
│   ├── deployment/                  ← Deployment guides
│   ├── development/                 ← Dev processes
│   └── project-docs/                ← Project documentation
│
└── 🌐 community/
    ├── SOURCES.md                   ← Full attribution
    ├── CHANGELOG.md                 ← Update history
    └── [community files...]         ← Community resources
```

---

## 🎯 Pro Tips

### Tip 1: Use INDEX Files
```bash
# Don't browse directories manually
# Instead, open these INDEX.md files:
```

**Quick Access Files** ✅:
- **[README.md](README.md)** - Main overview with current stats (2,460 files)
- **[WORKSPACE_STATS.md](WORKSPACE_STATS.md)** - Detailed statistics and growth metrics
- **[.agent/workflows/](. agent/workflows/)** - 51 executable workflows
- **[claude_update_log.md](claude_update_log.md)** - AI ecosystem monitoring log
- **[DRAG_INTO_CHAT.md](DRAG_INTO_CHAT.md)** - Quick file references for chat

**Click any link above to open in your editor!**

### Tip 2: Ask Me to Find Things
```bash
# Instead of searching manually:
"Find me skills related to [topic]"
"Which agent should I use for [task]?"
"Show me workflows for [problem]"

# I know all 2,460 files and can point you to the right one instantly
```

### Tip 3: Use @ References
```bash
# When messaging me, reference files directly:
"Check my @agents/workflows/docker-container-problems.md"
"Use @skills/official_anthropic/webapp-testing/ skill"
"Follow @workflows/shinpr/backend/ patterns"
```

### Tip 4: Combine Resources
```bash
# Mix your originals with community resources:
"Use my authentication workflow + wshobson security agent"
"Apply shinpr backend workflow with official Anthropic patterns"
"Combine tresor subagent with my project workflow"
```

### Tip 5: Document Everything
```bash
# After every major task:
/@workflow-orchestrator documentation-maintenance

# This keeps your workspace:
- ✅ Up-to-date
- ✅ Organized
- ✅ Free of duplicates
- ✅ Stats accurate
```

---

## 🚨 Emergency Quick Reference

| Emergency | Quick Fix |
|-----------|-----------|
| **Site not loading** | [deployment-issues.md](agents/workflows/deployment-issues.md) |
| **Build failing** | [build-failures.md](agents/workflows/build-failures.md) |
| **Auth broken** | [authentication-issues.md](agents/workflows/authentication-issues.md) |
| **Docker crash** | [docker-container-problems.md](agents/workflows/docker-container-problems.md) |
| **DB connection lost** | [database-connection-issues.md](agents/workflows/database-connection-issues.md) |
| **CORS errors** | [cors-errors.md](agents/workflows/cors-errors.md) |
| **Performance slow** | [performance-problems.md](agents/workflows/performance-problems.md) |
| **Security alert** | [security-audit.md](agents/workflows/security-audit.md) |

**Critical**: Just message me with the error and I'll guide you to the right workflow!

---

## 📞 How to Ask Me for Help

### Good Questions:
```bash
✅ "I'm building a REST API. Which agents and workflows should I use?"
✅ "My Docker container won't start. Where's the troubleshooting guide?"
✅ "I need to learn Kubernetes. What's the learning path?"
✅ "Show me production workflow for React components"
✅ "Which subagent handles database optimization?"
```

### Even Better:
```bash
⭐ "I'm working on [specific task]. Guide me step-by-step."
⭐ "I just solved [problem]. Help me document it for future use."
⭐ "Review this code using workspace best practices: [code]"
⭐ "Suggest 3 agents for [project type] development"
```

---

## 🎓 Learning Path Recommendations

### Week 1: Get Familiar
- [ ] Browse [README.md](README.md) and [WORKSPACE_STATS.md](WORKSPACE_STATS.md)
- [ ] Open [skills/INDEX.md](skills/INDEX.md) and explore categories
- [ ] Try one official Anthropic skill
- [ ] Run `/@workflow-orchestrator documentation-maintenance`

### Week 2: Apply to Project
- [ ] Use one of your original workflows
- [ ] Try a shinpr production workflow
- [ ] Use a wshobson agent
- [ ] Document what you learned

### Week 3: Advanced Usage
- [ ] Explore tresor subagents
- [ ] Use slash commands from tresor
- [ ] Combine multiple agents
- [ ] Create a custom workflow

### Ongoing
- [ ] Run Claude monitoring every 48 hours
- [ ] Document all new learnings
- [ ] Update workspace stats weekly
- [ ] Contribute improvements back to community repos

---

## ✅ Success Checklist

After reading this guide, you should know how to:
- [ ] Find the right skill/agent/workflow for any task
- [ ] Invoke workflows with simple commands
- [ ] Ask me effectively for help
- [ ] Navigate your 1,701-file workspace confidently
- [ ] Keep everything organized and up-to-date

---

**Remember**: You have an **enterprise-grade knowledge base** with **2,460 files** representing a **2,828% growth** from the original project. Don't feel overwhelmed - just ask me what you need, and I'll guide you to exactly the right resource!

**Key Principle**: *You don't need to know where everything is. Just know what you need, and ask me. That's what I'm here for.* 🚀
