# 🎭 Complete Agent Persona Library

**Total Available**: 145 specialized agent personas  
**Current in `.agent/rules/`**: 3  
**Workspace Repository**: 142 additional personas

---

## 📊 Persona Distribution

| Source | Count | Status |
|--------|-------|--------|
| `.agent/rules/` | 3 | ✅ Active (workflow-orchestrator, devops, rules) |
| `claude-subagents/categories/` | 137 | 📦 Available |
| `agents/wshobson/` | 5 | 📦 Available |

---

## 🎯 Top Priority Personas to Add

### 1. **Security & Compliance** (4 personas)
- `security-auditor` - DevSecOps, OWASP, compliance (GDPR/HIPAA/SOC2)
- `security-scanner` - Vulnerability assessment, penetration testing
- `compliance-auditor` - Regulatory frameworks, audit trails

**Location**: `agents/wshobson/security-*/agents/`

### 2. **Multi-Agent Orchestration** (2 personas)
- `agent-organizer` - Team assembly, task decomposition, coordination
- `multi-agent-coordinator` - Distributed workflows, agent communication

**Location**: `claude-subagents/categories/09-meta-orchestration/`

### 3. **ML & AI Engineering** (3 personas)
- `ml-engineer` - PyTorch 2.x, TensorFlow, model serving, MLOps
- `data-scientist` - Feature engineering, experimentation, statistical analysis
- `llm-specialist` - Fine-tuning, RAG, prompt engineering

**Location**: `agents/wshobson/machine-learning-ops/agents/`, `llm-application-dev/agents/`

### 4. **Cloud & Infrastructure** (7 personas)
- `cloud-architect` - AWS, Azure, GCP design
- `kubernetes-operator` - K8s management, helm, operators
- `terraform-specialist` - Infrastructure as Code
- `network-engineer` - VPC, load balancing, CDN
- `database-optimizer` - Query optimization, indexing
- `cicd-engineer` - GitHub Actions, ArgoCD, pipelines
- `observability-engineer` - Prometheus, Grafana, tracing

**Location**: `agents/wshobson/cloud-infrastructure/agents/`, `observability-monitoring/agents/`

### 5. **Full-Stack Development** (10+ personas)
- **Backend**: `fastapi-pro`, `django-pro`, `nodejs-expert`
- **Frontend**: `react-expert`, `vue-specialist`, `nextjs-pro`
- **Mobile**: `flutter-expert`, `ios-developer`, `android-expert`
- **Systems**: `rust-pro`, `golang-pro`, `cpp-pro`

**Location**: `agents/wshobson/` (various categories)

### 6. **SEO & Content** (10 personas)
- `seo-technical-optimizer` - Site speed, Core Web Vitals
- `seo-content-writer` - SEO-optimized content creation
- `seo-keyword-strategist` - Keyword research, strategy
- `seo-authority-builder` - Backlinks, domain authority

**Location**: `agents/wshobson/seo-*/agents/`

### 7. **Performance & Testing** (5 personas)
- `performance-engineer` - Load testing, optimization
- `test-automator` - E2E testing, test generation
- `code-reviewer` - Automated code review
- `debugger` - Systematic debugging, root cause analysis

**Location**: `agents/wshobson/performance-*/agents/`, `unit-testing/agents/`

### 8. **Specialized Domains** (20+ personas)
- `game-developer` - Unity, Unreal, game logic
- `blockchain-expert` - Web3, smart contracts
- `quant-analyst` - Quantitative trading, risk management
- `payment-integration` - Stripe, PayPal, payment processing
- `accessibility-auditor` - WCAG compliance, a11y

**Location**: `agents/wshobson/` (50+ specialized categories)

---

## 📁 Complete Category Index

### Meta & Orchestration
- agent-organizer
- multi-agent-coordinator
- task-distributor
- context-manager

### Security
- security-auditor (comprehensive)
- security-scanner
- compliance-auditor
- penetration-tester

### ML/AI (8 total)
- ml-engineer
- data-scientist
- llm-specialist
- model-optimizer
- feature-engineer
- mlops-engineer

### Cloud Infrastructure (15+ total)
- cloud-architect
- kubernetes-operator  
- terraform-specialist
- network-engineer
- database-optimizer
- cicd-engineer
- observability-engineer

### Backend Development (12+ total)
- fastapi-pro
- django-pro
- nodejs-expert
- golang-pro
- rust-pro
- backend-architect

### Frontend Development (8+ total)
- react-expert
- vue-specialist
- nextjs-pro
- angular-expert
- frontend-optimizer

### Mobile Development (6 total)
- flutter-expert
- ios-developer
- android-expert
- react-native-pro
- mobile-architect

### Systems Programming (4 total)
- rust-pro
- golang-pro
- cpp-pro
- c-pro

### SEO (10 total)
- seo-technical-optimizer
- seo-content-writer
- seo-keyword-strategist
- seo-meta-optimizer
- seo-authority-builder
- seo-content-planner
- seo-cannibalization-detector
- seo-content-refresher
- seo-snippet-hunter
- seo-structure-architect

### Database (6 total)
- database-optimizer
- database-architect
- migration-specialist
- query-optimizer

### Testing & QA (6 total)
- test-automator
- performance-engineer
- code-reviewer
- debugger
- qa-engineer

### Game Development (2 total)
- game-developer
- unity-expert

### Specialized (20+ total)
- blockchain-expert
- quant-analyst
- payment-integration
- accessibility-auditor
- documentation-generator
- api-designer
- shell-scripter
- julia-developer

---

## 🚀 Recommended Actions

### Immediate (Copy to `.agent/rules/`)
1. **agent-organizer** - Essential for multi-agent coordination
2. **security-auditor** - Critical for production security
3. **ml-engineer** - Growing ML/AI needs

### Short-term
4. **cloud-architect** - Infrastructure design
5. **frontend-optimizer** - UI/UX performance
6. **test-automator** - QA automation

### Medium-term
- Domain-specific personas as needed
- Custom persona creation for unique requirements

---

## 📝 Usage Examples

### Method 1: Reference from Workspace
```
@[agents/wshobson/security-scanning/agents/security-auditor.md]

Conduct security audit of our microservices
```

### Method 2: Copy to .agent/rules/
```powershell
Copy-Item "agents\wshobson\security-scanning\agents\security-auditor.md" ".agent\rules\" -Force
```

Then reference:
```
@[.agent/rules/security-auditor.md]
```

### Method 3: Use Claude Subagents
```
@[claude-subagents/categories/09-meta-orchestration/agent-organizer.md]

Organize a team of agents for this complex task
```

---

## 📚 Full Category List (66 categories)

1. accessibility-compliance
2. agent-orchestration
3. api-scaffolding
4. api-testing-observability
5. application-performance
6. arm-cortex-microcontrollers
7. backend-api-security
8. backend-development
9. blockchain-web3
10. business-analytics
11. c4-architecture
12. cicd-automation
13. cloud-infrastructure
14. code-documentation
15. code-refactoring
16. code-review-ai
17. codebase-cleanup
18. comprehensive-review
19. content-marketing
20. context-management
21. customer-sales-automation
22. data-engineering
23. data-validation-suite
24. database-cloud-optimization
25. database-design
26. database-migrations
27. debugging-toolkit
28. dependency-management
29. deployment-strategies
30. deployment-validation
31. developer-essentials
32. distributed-debugging
33. documentation-generation
34. dotnet-contribution
35. error-debugging
36. error-diagnostics
37. framework-migration
38. frontend-mobile-development
39. frontend-mobile-security
40. full-stack-orchestration
41. functional-programming
42. game-development
43. git-pr-workflows
44. hr-legal-compliance
45. incident-response
46. javascript-typescript
47. julia-development
48. jvm-languages
49. kubernetes-operations
50. llm-application-dev
51. machine-learning-ops
52. multi-platform-apps
53. observability-monitoring
54. payment-processing
55. performance-testing-review
56. python-development
57. quantitative-trading
58. security-compliance
59. security-scanning
60. seo-analysis-monitoring
61. seo-content-creation
62. seo-technical-optimization
63. shell-scripting
64. systems-programming
65. tdd-workflows
66. team-collaboration
67. unit-testing
68. web-scripting

---

**📍 Location Map**:
- `claude-subagents/categories/` - 137 personas (66 categories)
- `agents/wshobson/` - 5 personas (66 categories with agents/ subdirs)
- `.agent/rules/` - 3 personas (current active)

**Total Available**: 145 specialized agent personas ready to use!
