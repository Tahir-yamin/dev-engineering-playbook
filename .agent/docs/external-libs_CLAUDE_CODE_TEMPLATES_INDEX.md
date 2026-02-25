# Claude Code Templates Index (aitmpl.com)

**Location**: `external-libs/claude-code-templates/`
**Purpose**: Comprehensive ecosystem of Agents, Commands, Hooks, and Skills for Claude Code.
**Total Components**: 6,000+ items across 50+ categories.

---

## 🤖 Custom Agents (420+ Total)
Specialized personas with tailored system prompts and tool access.
*Path: `external-libs/claude-code-templates/cli-tool/components/agents/`*

### Featured Categories:
- **[Development Team](file:///d:/my-dev-knowledge-base/external-libs/claude-code-templates/cli-tool/components/agents/development-team/)** (17): Backend, Frontend, Fullstack, Mobile, and Web developers.
- **[Programming Languages](file:///d:/my-dev-knowledge-base/external-libs/claude-code-templates/cli-tool/components/agents/programming-languages/)** (50): Experts in Python, TypeScript, Rust, Go, Swift, and more.
- **[DevOps & Infrastructure](file:///d:/my-dev-knowledge-base/external-libs/claude-code-templates/cli-tool/components/agents/devops-infrastructure/)** (39): Kubernetes, Terraform, Azure, AWS, and GCP specialists.
- **[Deep Research Team](file:///d:/my-dev-knowledge-base/external-libs/claude-code-templates/cli-tool/components/agents/deep-research-team/)** (16): Specialists in intelligence gathering and trend analysis.
- **[Security](file:///d:/my-dev-knowledge-base/external-libs/claude-code-templates/cli-tool/components/agents/security/)** (20): Pentesting, auditing, and vulnerability assessment agents.
- **[Meta & Orchestration](file:///d:/my-dev-knowledge-base/external-libs/claude-code-templates/cli-tool/components/agents/mcp-dev-team/)** (8): Agents designed to coordinate other agents.

---

## 🔪 Reusable Commands (220+ Total)
Custom slash commands for deterministic development workflows.
*Path: `external-libs/claude-code-templates/cli-tool/components/commands/`*

### Top Categories:
- **[Project Management](file:///d:/my-dev-knowledge-base/external-libs/claude-code-templates/cli-tool/components/commands/project-management/)** (20): `/todo`, `/sprint-plan`, `/milestone-track`.
- **[Git & Workflow](file:///d:/my-dev-knowledge-base/external-libs/claude-code-templates/cli-tool/components/commands/git-workflow/)** (10): `/commit-conventional`, `/branch-factory`, `/pr-master`.
- **[Testing](file:///d:/my-dev-knowledge-base/external-libs/claude-code-templates/cli-tool/components/commands/testing/)** (15): `/generate-unit-tests`, `/e2e-suite`, `/mock-factory`.
- **[Next.js & Vercel](file:///d:/my-dev-knowledge-base/external-libs/claude-code-templates/cli-tool/components/commands/nextjs-vercel/)** (10): `/setup-auth`, `/optimize-render`, `/deploy-check`.
- **[Orchestration](file:///d:/my-dev-knowledge-base/external-libs/claude-code-templates/cli-tool/components/commands/orchestration/)** (15): Commands for multi-agent task distribution.

---

## 💡 Specialized Skills (4,500+ Total)
Instruction sets and domain expertise for granular task handling.
*Path: `external-libs/claude-code-templates/cli-tool/components/skills/`*

These skills cover every possible niche from LLM fine-tuning to specific regulatory compliance.

---

## 🔗 Integrated MCP Servers (60+ Total)
Pre-configured connections to external APIs and tools.
*Path: `external-libs/claude-code-templates/cli-tool/components/mcps/`*

---

## 🧩 Usage Instructions
1. **Browse**: Use this index to find the category you need.
2. **Read**: View the `.md` files within the subdirectories to see the specific system prompts.
3. **Apply**: Reference the absolute path in your session to "load" that agent or command.

```markdown
# Example: Deploying the Security Auditor
@[d:\my-dev-knowledge-base\external-libs\claude-code-templates\cli-tool\components\agents\security\security-auditor.md]
Audit this codebase for OWASP vulnerabilities.
```

---

**Last Synced**: 2026-02-23  
**Source**: [aitmpl.com](https://aitmpl.com/)
