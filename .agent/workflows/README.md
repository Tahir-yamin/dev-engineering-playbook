---
description: Index of all available workflows for troubleshooting and development
---

# Workflows Index

**Total Workflows**: 212  
**Location**: `.agent/workflows/`  
**Last Updated**: 2026-01-31

---

## 🚨 Troubleshooting Workflows (8)

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

### 9. [Alpha Cloud Deployment](./alpha-cloud-deployment.md) ☁️ ALPHA
**Use when**: Deploying to AKS, Dapr, Kafka, or troubleshooting Kubernetes clusters.  
**Fixes**: Sidecar issues, ACR errors, Topic creation, OOMKilled, Pending pods.  
**Includes**: Unified logic from Phase 4/5, monitoring, and automated verification.

---

## 🚀 Development Workflows (5)

### 10. [Alpha Project Lifecycle](./alpha-project-lifecycle.md) 🚀 ALPHA
**Use when**: From initial Socratic discovery to implementation and wrap-up.  
**Includes**: Requirements Analysis, Starting New Projects, Adding Features, and Synergy extraction.

### 20. [Skill Upgrade](./skill-upgrade.md) 🚀
**Use when**: Planning your 2025 learning journey  
**Includes**: Roadmap execution, deep dive steps, learning projects  
**Special**: Guides you from "Practitioner" to "Architect" level

### 21. [Research & Writing Index](./research.md) 📚
**Use when**: Consolidating research, writing, and LaTeX resources.
**Includes**: Governance checks, skill identification, and index generation.

---

## 📚 Meta & DevOps Workflows (7)

### 15. [Documentation Maintenance](./documentation-maintenance.md) ⭐
**Use when**: Adding new workflows, skills, design specs, or requirements  
**Includes**: Creating workflows, updating skills, design system, prompts  
**Special**: This is the workflow for updating the documentation system itself!

### 16. [GitHub Best Practices](./github-best-practices.md)
**Use when**: Setting up new repos, auditing security, configuring CI/CD
**Special**: Fully autonomous workflow with auto-approval for fixes

### 17. [Gemini CLI GitHub Integration](./gemini-cli-github-integration.md)
**Use when**: Integrating Gemini CLI into GitHub workflows
**Includes**: Setup, configuration, example usage

### 18. [Gemini Quota Recovery](./gemini-quota-recovery.md)
**Use when**: Experiencing Gemini 429 errors or quota limits
**Fixes**: Systematic recovery protocol for Gemini 429 errors
**Includes**: Rate limit handling, retry mechanisms, quota monitoring

### 19. [Git Flow Branch Creator](./git-flow-branch-creator.prompt.md)
**Use when**: Creating appropriate branches following Git Flow
**Includes**: Branch naming conventions, automated branch creation

### 20. [Security Remediation](./security-remediation.md) 🛡️
**Use when**: GitHub security alerts, Dependabot alerts, code scanning issues
**Fixes**: Exposed secrets, vulnerability patches, dependency updates
**Includes**: Automated remediation steps, alert management

### 21. [Complete Application QA](./complete-application-qa.md) ✅
**Use when**: End-to-end testing, pre-submission QA, comprehensive validation
**Includes**: Auth testing, CRUD operations, AI chatbot, deployment verification
**Special**: Autonomous self-examination and auto-resolution workflow

### 19. [QA Kanban](./qa-kanban.md) 📋
**Use when**: Testing Kanban board functionality specifically  
**Includes**: Board creation, task movement, status validation

---

## 📊 Data & Analytics Workflows (8) ⭐ NEW

### 1. [Fabric Audit & BPA Remediation](./fabric-audit.prompt.md) ⭐
**Use when**: Microsoft Fabric scan results need remediation patterns.  
**Includes**: BPA results analysis, TMDL remediation snippets.

### 2. [DAX Performance Optimizer](./dax-optimize.prompt.md) ⭐
**Use when**: Slow DAX measures need VertiPaq engine optimization.  
**Includes**: FE/SE bottleneck identification, GIAC patterns.

### 3. [Fabric Governance Standards](./fabric-governance.prompt.md) ⭐
**Use when**: Establishing tenant/workspace governance or documentation.  
**Includes**: Data Dictionary generation, Naming SOPs, Tagging strategy.

### 4. [Power BI DAX Optimization](./power-bi-dax-optimization.prompt.md)
**Use when**: General DAX formula optimization for readability/performance.

### 5. [Power BI Model Design Review](./power-bi-model-design-review.prompt.md)
**Use when**: Evaluating model architecture and relationships.

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
| **Deploying to production** | **alpha-cloud-deployment** |
| **Starting fresh project** | **alpha-project-lifecycle** |
| **Implementing new feature** | **alpha-project-lifecycle** |
| **Kubernetes / Pod issues** | **alpha-cloud-deployment** |
| **Dapr / Kafka / AKS errors** | **alpha-cloud-deployment** |
| **Slow Power BI Report** | **dax-optimize** |
| **Fabric BPA Violations** | **fabric-audit** |
| **No Fabric Documentation** | **fabric-governance** |

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
