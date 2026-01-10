---
description: Index of all available workflows for troubleshooting and development
---

# Workflows Index

**Total Workflows**: 25  
**Location**: `.agent/workflows/`  
**Last Updated**: January 10, 2026

---

## 🚨 Troubleshooting Workflows (9)

### 1. [Build Failures](./build-failures.md)
**Use when**: npm build, Docker build, TypeScript errors, dependency issues  
**Fixes**: COPY failed, Module not found, Prisma Client errors

### 2. [Authentication Issues](./authentication-issues.md)
**Use when**: Login broken, CSRF errors, session problems, OAuth failures  
**Fixes**: CSRF token mismatch, Session not found, OAuth redirect fails

### 3. [Docker Container Problems](./docker-container-problems.md)
**Use when**: Container won't start, crashes, unhealthy status  
**Fixes**: Container exits, Port conflicts, Prisma in Docker

### 4. [Database Connection Issues](./database-connection-issues.md)
**Use when**: Connection refused, SSL errors, Prisma can't connect  
**Fixes**: SSL negotiation failed, channel_binding errors, timeouts

### 5. [CORS Errors](./cors-errors.md)
**Use when**: Frontend can't reach backend, CORS policy blocks requests  
**Fixes**: Access-Control-Allow-Origin errors

### 6. [Performance Problems](./performance-problems.md)
**Use when**: Slow pages, laggy UI, high memory usage  
**Fixes**: Bundle size, re-renders, N+1 queries, caching

### 7. [Deployment Issues](./deployment-issues.md)
**Use when**: Moving to production, deploying to cloud, SSL issues  
**Includes**: Pre-deployment checklist, migration process, rollback plan

### 8. [Antigravity Browser Agent Issues](./antigravity-browser-agent-issues.md) 🌐
**Use when**: Browser Agent unavailable, Chrome DevTools Protocol errors  
**Fixes**: Port 9222 conflicts, wsarecv errors, gcloud authentication, firewall blocking  
**Includes**: Step-by-step fix, prevention script, WSL2 workarounds

### 9. [Security Audit](./security-audit.md) 🔐
**Use when**: Before deployment, before committing code, regular audits  
**Fixes**: API key exposure, secrets in ConfigMap, Git history cleanup  
**Includes**: Credential scanning, sealed-secrets, pre-commit hooks

### 10. [Kubernetes Deployment Testing](./kubernetes-deployment-testing.md) ☸️
**Use when**: Phase 4 Kubernetes deployment issues, Helm chart problems  
**Fixes**: Pod failures, service connectivity, ConfigMap issues, SSL errors  
**Includes**: Comprehensive Phase 4 deployment troubleshooting, real-world issues

### 11. [Phase V Troubleshooting](./phase5-troubleshooting.md) 🚀
**Use when**: Phase 5 Kafka, Dapr, or AKS cloud deployment issues  
**Fixes**: Dapr sidecar injection, Kafka/Strimzi issues, ACR pull errors  
**Includes**: Dapr debugging, Kafka topic creation, GitHub Actions CI/CD

---

## 🚀 Development Workflows (5)

### 10. [Starting New Project](./starting-new-project.md)
**Use when**: Beginning new full-stack application  
**Includes**: Project structure, Git setup, environment configuration

### 11. [Adding New Feature](./adding-new-feature.md)
**Use when**: Implementing new functionality, creating API endpoints  
**Includes**: Planning, backend, frontend, testing, integration

### 12. [Code Review & Testing](./code-review-testing.md)
**Use when**: Before deploying, PR review, QA testing  
**Includes**: Quality checklist, security check, performance testing

### 13. [Environment Setup](./environment-setup.md)
**Use when**: Onboarding new devs, fresh machine, setting up CI/CD  
**Includes**: Prerequisites, clone, dependencies, validation

### 14. [Database Schema Changes](./database-schema-changes.md)
**Use when**: Adding tables, modifying columns, migrations  
**Includes**: Safe migration process, rollback plan, monitoring

### 20. [Skill Upgrade](./skill-upgrade.md) 🚀
**Use when**: Planning your 2025 learning journey  
**Includes**: Roadmap execution, deep dive steps, learning projects  
**Special**: Guides you from "Practitioner" to "Architect" level

---

## 📚 Meta & DevOps Workflows (7)

### 15. [Documentation Maintenance](./documentation-maintenance.md) ⭐
**Use when**: Adding new workflows, skills, design specs, or requirements  
**Includes**: Creating workflows, updating skills, design system, prompts  
**Special**: This is the workflow for updating the documentation system itself!

### 16. [GitHub Best Practices](./github-best-practices.md)
**Use when**: Setting up new repos, auditing security, configuring CI/CD
**Special**: Fully autonomous workflow with auto-approval for fixes

### 17. [Security Remediation](./security-remediation.md) 🛡️
**Use when**: GitHub security alerts, Dependabot alerts, code scanning issues
**Fixes**: Exposed secrets, vulnerability patches, dependency updates
**Includes**: Automated remediation steps, alert management

### 18. [Complete Application QA](./complete-application-qa.md) ✅
**Use when**: End-to-end testing, pre-submission QA, comprehensive validation
**Includes**: Auth testing, CRUD operations, AI chatbot, deployment verification
**Special**: Autonomous self-examination and auto-resolution workflow

### 19. [QA Kanban](./qa-kanban.md) 📋
**Use when**: Testing Kanban board functionality specifically
**Includes**: Board creation, task movement, status validation

---

## 📖 How to Use

### Method 1: Direct Slash Command
```
/build-failures

Follow the workflow for my Docker build error
```

### Method 2: Reference in Conversation
```
I'm having authentication issues.
Use the /authentication-issues workflow
```

### Method 3: Check This Index
Browse this file to find the right workflow for your problem.

---

## 🎯 Quick Problem → Workflow Mapping

| Problem | Workflow |
|---------|----------|
| Build won't complete | build-failures |
| Can't log in | authentication-issues |
| Docker container fails | docker-container-problems |
| Database connection error | database-connection-issues |
| CORS policy error | cors-errors |
| App is slow | performance-problems |
| Deploying to production | deployment-issues |
| **Browser Agent unavailable** | **antigravity-browser-agent-issues** |
| Starting fresh project | starting-new-project |
| **Kubernetes pods failing** | **kubernetes-deployment-testing** |
| **Need full QA test** | **complete-application-qa** |
| **GitHub security alerts** | **security-remediation** |
| **API keys exposed** | **security-audit** |
| **Dapr sidecar issues** | **phase5-troubleshooting** |
| **Kafka/Strimzi errors** | **phase5-troubleshooting** |
| **AKS deployment fails** | **phase5-troubleshooting** |

---

## ⚡ Workflows with // turbo (Auto-Run Commands)

These workflows have steps that are safe to auto-run:

- authentication-issues (validate-env.ps1)
- docker-container-problems (docker-compose commands)
- database-connection-issues (connection tests)
- cors-errors (health checks)
- starting-new-project (git init, installs)
- environment-setup (installs, validation)
- database-schema-changes (migrations)
- **kubernetes-deployment-testing** (kubectl checks)

---

## 🔗 Related Documentation

- **Skills Library**: `.claude/skills.md` - 60+ skills with prompt templates
- **Phase Guides**: `.claude/phase1-3-skills.md` - Phase-specific guides
- **Topic Guides**: `.claude/docker-skills.md` etc. - Topic deep-dives

---

## 💡 Pro Tips

1. **Start with the index** - Find your workflow here
2. **Follow steps in order** - Workflows are optimized sequences
3. **Check "Related Skills"** - For deeper understanding
4. **Use // turbo annotations** - Auto-run safe commands
5. **Document what works** - Add your learnings back

---

**All workflows tested and verified on TODO Hackathon project!** 🎉
