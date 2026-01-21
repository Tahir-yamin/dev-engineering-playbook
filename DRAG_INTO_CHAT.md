# 📎 Quick File Reference - For Dragging Into Chat

**Workspace**: 2,460 files | Last Updated: 2026-01-19  
**How to use**: Copy any line below and paste it into the chat - it will automatically become a draggable file reference!

---

## 🔥 Most Used Workflows (Drag into chat)

### Troubleshooting
```
@[.agent/workflows/authentication-issues.md]
@[.agent/workflows/build-failures.md]
@[.agent/workflows/cors-errors.md]
@[.agent/workflows/database-connection-issues.md]
@[.agent/workflows/docker-container-problems.md]
@[.agent/workflows/deployment-issues.md]
@[.agent/workflows/performance-problems.md]
@[.agent/workflows/kubernetes-deployment-testing.md]
```

### Development
```
@[.agent/workflows/adding-new-feature.md]
@[.agent/workflows/code-review-testing.md]
@[.agent/workflows/create-course.md]
@[.agent/workflows/database-schema-changes.md]
@[.agent/workflows/environment-setup.md]
@[.agent/workflows/starting-new-project.md]
```

### Quality & Security
```
@[.agent/workflows/complete-application-qa.md]
@[.agent/workflows/qa-kanban.md]
@[.agent/workflows/security-audit.md]
@[.agent/workflows/security-remediation.md]
```

### 💼 Job Application Automation
```
@[.agent/workflows/apply-for-jobs.md]
@[job-application/data/recent_jobs.md]
@[job-application/data/applications_log.json]
@[job-application/scripts/apply_job.py]
@[job-application/scripts/gmail_oauth_sender.py]
@[skills/cv-optimization-skills.md]
```

**Quick Commands:**
```bash
# Apply with email
python job-application/scripts/apply_job.py --company "AECOM" --role "Project Controls Manager" --email "hr@aecom.com"

# Apply with website form
python job-application/scripts/apply_job.py --company "AECOM" --role "Project Controls Manager" --website

# View stats
python job-application/scripts/job_scraper.py --stats
```

### 🏢 Enterprise Agents (Meta-Orchestration)

**Production-ready agents for enterprise automation:**

- **📄 `.agent/agents/multi-agent-coordinator.md`** - Coordinate 100+ agents (234K msg/min, 99.9% delivery)
- **📄 `.agent/agents/workflow-orchestrator.md`** - Business process automation (99.9% reliability, Saga patterns)
- **📄 `.agent/agents/task-distributor.md`** - Intelligent work allocation and load balancing
- **📄 `.agent/agents/performance-monitor.md`** - Real-time metrics and bottleneck detection
- **📄 `.agent/agents/error-coordinator.md`** - Error handling and auto-recovery
- **📄 `.agent/agents/context-manager.md`** - State management and memory persistence
- **📄 `.agent/agents/agent-organizer.md`** - Team assembly and agent selection
- **📄 `.agent/agents/knowledge-synthesizer.md`** - Pattern recognition and documentation

**Full Guide**: `skills/enterprise-meta-orchestration-guide.md`

**Usage**:
```
@multi-agent-coordinator "Coordinate 5 agents to build a full-stack app"
@workflow-orchestrator "Create deployment pipeline with rollback"
```

**137 Total Agents Available**: `external-libs/awesome-claude-code-subagents/`

---

## Meta Workflows
```
@[.agent/workflows/documentation-maintenance.md]
@[.agent/workflows/ai-ecosystem-monitoring.md]
@[.agent/workflows/skill-upgrade.md]
@[.agent/workflows/github-best-practices.md]
@[.agent/workflows/workflow-orchestrator.md]
@[.agent/workflows/continuous-deployment-monitoring.md]
```

### AI Update Reports (NEW!)
```
@[claude_update_report_2026-01-13.md]
@[claude_update_report_2026-01-08.md]
@[claude_updates_knowledge_base.md]
@[claude_update_log.md]
```

---

## 📚 Skills (Drag into chat)

### Your Learning Paths
```
@[skills/SKILL_PATH_0_CORE_STACK.md]
@[skills/SKILL_PATH_A_DEVOPS.md]
@[skills/SKILL_PATH_B_AI_ENGINEERING.md]
@[skills/SKILL_PATH_C_ARCHITECTURE.md]
@[skills/claude-monitoring-skills.md]
```

### Project Management
```
@[skills/project-management/]
@[.agent/workflows/create-project-schedule.md]
@[.agent/workflows/p6-schedule-analysis.md]
```

### Windows Desktop Automation
```
@[skills/windows-desktop-automation-skills.md]
```

### Automation Scripts
```
@[scripts/project-management/]
```

### Official Anthropic Skills
```
@[skills/official_anthropic/docx/]
@[skills/official_anthropic/pdf/]
@[skills/official_anthropic/pptx/]
@[skills/official_anthropic/xlsx/]
@[skills/official_anthropic/mcp-builder/]
@[skills/official_anthropic/webapp-testing/]
```

### Business Skills
```
@[skills/alirezarezvani/c-level/]
@[skills/alirezarezvani/marketing/]
@[skills/alirezarezvani/product/]
@[skills/alirezarezvani/engineering/]
```

### 🌌 Antigravity Ecosystem (NEW)
```
@[external-libs/antigravity-awesome-skills/skills/]   # 223+ skills
@[external-libs/antigravity-kit/.agent/]              # 16 agents, 40 skills, 11 workflows
@[external-libs/antigravity-workspace-template/]      # Gemini workspace template
```

---

## 🗂️ Master Files (Drag into chat)

```
@[README.md]
@[WORKSPACE_STATS.md]
@[QUICKSTART_GUIDE.md]
@[DRAG_INTO_CHAT.md]
@[claude_update_log.md]
@[claude_updates_knowledge_base.md]
```

---

## 📖 Guides (Drag into chat)

### Docker
```
@[guides/docker/GORDON-AI-GUIDE.md]
@[guides/docker/Dockerfile-usage.md]
@[guides/docker/multi-stage-builds.md]
```

### Kubernetes
```
@[guides/kubernetes/]
```

### Authentication
```
@[guides/authentication/]
```

---

## 🤖 Agent Directories (Drag into chat)

### By Source
```
@[agents/wshobson/backend-development/]
@[agents/wshobson/cloud-infrastructure/]
@[agents/wshobson/cicd-automation/]
@[agents/tresor/subagents/]
@[agents/tresor/commands/]
@[agents/subagents/]
@[agents/cloudai/]
```

### Production Workflows
```
@[workflows/shinpr/backend/]
@[workflows/shinpr/frontend/]
@[workflows/shinpr/agents/]
```

---

## 🎯 Common Use Cases

### "I need help with authentication"
```
@[.agent/workflows/authentication-issues.md]
@[guides/authentication/]
```

### "I need help with Docker"
```
@[.agent/workflows/docker-container-problems.md]
```

### "I need help with deployment"
```
@[.agent/workflows/deployment-issues.md]
@[.agent/workflows/kubernetes-deployment-testing.md]
```

### "I want to learn something new"
```
@[.agent/workflows/skill-upgrade.md]
@[QUICKSTART_GUIDE.md]
```

### "I want to review code"
```
@[.agent/workflows/code-review-testing.md]
```

### "I need to document something"
```
@[.agent/workflows/documentation-maintenance.md]
@[.agent/workflows/workflow-orchestrator.md]
```

---

## 💡 How to Use

1. **Find the file you need** in the lists above
2. **Copy the entire line** (including `@[` and `]`)
3. **Paste into our chat** 
4. **It becomes a draggable file reference!**

Example:
- Copy: `@[.agent/workflows/docker-container-problems.md]`
- Paste in chat
- I can now access that file!

---

**Pro Tip**: Bookmark this file for quick access to all your workspace files! 🚀
