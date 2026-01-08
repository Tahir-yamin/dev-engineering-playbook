# Workflows Master Index

**Total Workflows**: 156+ files  
**Last Updated**: 2026-01-08  
**Organization**: By source, problem type, and use case

---

## 🎯 Quick Search

**Need a workflow for**:
- Troubleshooting? → Your original 24 workflows
- Backend development? → shinpr/backend
- Frontend development? → shinpr/frontend
- Production patterns? → wshobson/docs

---

## By Source

### Your Original Workflows (24 files)

Located in: `agents/workflows/`

#### Troubleshooting
- [authentication-issues.md](../agents/workflows/authentication-issues.md) - Login, CSRF, OAuth
- [build-failures.md](../agents/workflows/build-failures.md) - npm, Docker, TypeScript errors
- [cors-errors.md](../agents/workflows/cors-errors.md) - Cross-origin blocks
- [database-connection-issues.md](../agents/workflows/database-connection-issues.md) - SSL, Prisma, Neon
- [docker-container-problems.md](../agents/workflows/docker-container-problems.md) - Container crashes
- [deployment-issues.md](../agents/workflows/deployment-issues.md) - Production checklist
- [performance-problems.md](../agents/workflows/performance-problems.md) - Optimization
- [kubernetes-deployment-testing.md](../agents/workflows/kubernetes-deployment-testing.md) - K8s issues

#### Development
- [adding-new-feature.md](../agents/workflows/adding-new-feature.md) - Feature implementation
- [code-review-testing.md](../agents/workflows/code-review-testing.md) - PR review
- [database-schema-changes.md](../agents/workflows/database-schema-changes.md) - Migrations
- [environment-setup.md](../agents/workflows/environment-setup.md) - Dev environment
- [starting-new-project.md](../agents/workflows/starting-new-project.md) - Project setup

#### Meta & DevOps
- [documentation-maintenance.md](../agents/workflows/documentation-maintenance.md) - Update docs (ENHANCED)
- [github-best-practices.md](../agents/workflows/github-best-practices.md) - Repo setup
- [security-audit.md](../agents/workflows/security-audit.md) - Security scanning
- [security-remediation.md](../agents/workflows/security-remediation.md) - Fix security issues
- [complete-application-qa.md](../agents/workflows/complete-application-qa.md) - End-to-end testing
- [qa-kanban.md](../agents/workflows/qa-kanban.md) - Kanban testing
- [skill-upgrade.md](../agents/workflows/skill-upgrade.md) - Learn new skills

#### Monitoring (NEW)
- [workflow-orchestrator.md](../agents/workflows/workflow-orchestrator.md) - Combine workflows
- [monitor-claude-updates.md](../monitor-claude-updates.md) - Claude ecosystem tracking

---

### shinpr Production Workflows (127 files)

Located in: `workflows/shinpr/`

#### Agents (21 files)
- Specialized workflow agents
- Quality assurance agents
- Development coordinators

#### Backend Workflows (37 files)
- API development patterns
- Database operations
- Service orchestration
- Error handling
- Authentication flows
- Payment processing

#### Frontend Workflows (46 files)
- Component development
- State management
- UI/UX patterns
- Performance optimization
- Testing strategies
- Form handling

#### Commands (11 files)
- Workflow invocation
- Automation scripts
- Quick commands

#### Skills (16 files)
- Workflow-specific skills
- Best practices
- Pattern library

---

### wshobson Documentation (5 files)

Located in: `workflows/wshobson/`

- Usage guides
- Plugin documentation
- Integration patterns
- Best practices
- Configuration examples

---

## By Problem Type

### Troubleshooting & Debugging
| Problem | Workflow |
|---------|----------|
| Authentication failing | [authentication-issues.md](../agents/workflows/authentication-issues.md) |
| Build not working | [build-failures.md](../agents/workflows/build-failures.md) |
| CORS errors | [cors-errors.md](../agents/workflows/cors-errors.md) |
| Database connection lost | [database-connection-issues.md](../agents/workflows/database-connection-issues.md) |
| Docker container crashed | [docker-container-problems.md](../agents/workflows/docker-container-problems.md) |
| Deployment failed | [deployment-issues.md](../agents/workflows/deployment-issues.md) |
| Performance slow | [performance-problems.md](../agents/workflows/performance-problems.md) |
| K8s pod issues | [kubernetes-deployment-testing.md](../agents/workflows/kubernetes-deployment-testing.md) |

### Development
| Task | Workflow |
|------|----------|
| Add new feature | [adding-new-feature.md](../agents/workflows/adding-new-feature.md) |
| Code review | [code-review-testing.md](../agents/workflows/code-review-testing.md) |
| Database migration | [database-schema-changes.md](../agents/workflows/database-schema-changes.md) |
| Setup environment | [environment-setup.md](../agents/workflows/environment-setup.md) |
| Start new project | [starting-new-project.md](../agents/workflows/starting-new-project.md) |
| Backend API | shinpr/backend/ |
| Frontend component | shinpr/frontend/ |

### Quality & Testing
| Task | Workflow |
|------|----------|
| End-to-end QA | [complete-application-qa.md](../agents/workflows/complete-application-qa.md) |
| Kanban testing | [qa-kanban.md](../agents/workflows/qa-kanban.md) |
| Security audit | [security-audit.md](../agents/workflows/security-audit.md) |
| Fix security issues | [security-remediation.md](../agents/workflows/security-remediation.md) |

### Meta & Maintenance
| Task | Workflow |
|------|----------|
| Update documentation | [documentation-maintenance.md](../agents/workflows/documentation-maintenance.md) |
| Learn new skill | [skill-upgrade.md](../agents/workflows/skill-upgrade.md) |
| GitHub setup | [github-best-practices.md](../agents/workflows/github-best-practices.md) |
| Monitor Claude updates | [monitor-claude-updates.md](../monitor-claude-updates.md) |
| Combine workflows | [workflow-orchestrator.md](../agents/workflows/workflow-orchestrator.md) |

---

## By Technology

### Backend
- shinpr/backend/ - 37 comprehensive workflows
- Your database workflows
- API scaffolding patterns

### Frontend  
- shinpr/frontend/ - 46 comprehensive workflows
- Component patterns
- State management

### DevOps
- Your K8s workflow
- Docker workflows
- CI/CD patterns from wshobson

### Database
- Your database-connection-issues.md
- Your database-schema-changes.md
- shinpr backend database patterns

---

## By Development Phase

### Planning
- starting-new-project.md
- shinpr planning workflows
- Architecture patterns

### Development
- adding-new-feature.md
- shinpr backend + frontend workflows
- Code patterns from wshobson

### Testing
- code-review-testing.md
- complete-application-qa.md
- qa-kanban.md
- shinpr testing workflows

### Deployment
- deployment-issues.md
- kubernetes-deployment-testing.md
- CI/CD workflows

### Maintenance
- documentation-maintenance.md
- security-audit.md
- performance-problems.md

---

## Quick Invocation

### Use Workflow Orchestrator
```bash
# Single workflow
/@workflow-orchestrator [workflow-name]

# Combined workflows
/@workflow-orchestrator [workflow1] + [workflow2]

# Common combinations
/@workflow-orchestrator claude-monitoring + documentation-maintenance
/@workflow-orchestrator skill-upgrade + documentation-maintenance
```

### Direct Reference
```bash
# Message me:
"Use @agents/workflows/docker-container-problems.md"
"Follow @workflows/shinpr/backend/ patterns"
```

---

## Production-Ready Workflows (from shinpr)

**27 Releases** tested in production:

### The Workflow (General Development)
- Feature planning
- Implementation
- Testing
- Deployment

### The Diagnosis Workflow (Debugging)
- Problem identification
- Root cause analysis
- Fix implementation
- Verification

### The Reverse Engineering Workflow
- Codebase understanding
- Architecture mapping
- Documentation generation
- Knowledge transfer

---

**Total**: 156+ workflow files  
**Coverage**: Troubleshooting → Development → QA → Deployment  
**Ready**: All workflows immediately usable!
