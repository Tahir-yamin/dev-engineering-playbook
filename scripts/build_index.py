"""
Build KNOWLEDGE_INDEX.md — Complete categorized index.
All agents, skills, and workflows grouped by topic with @ and / syntax.
"""

import os
import re
from datetime import datetime

ROOT = r"d:\my-dev-knowledge-base"
OUTPUT = os.path.join(ROOT, "KNOWLEDGE_INDEX.md")

# ── Helpers ───────────────────────────────────────────────────────────────────
def get_desc(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for _ in range(20):
                line = f.readline()
                if line.lower().startswith("description:"):
                    d = line.split(":", 1)[1].strip().strip('"\'')
                    return d[:90] if len(d) > 90 else d
                m = re.match(r'^#{1,2}\s+(.+)', line)
                if m:
                    return m.group(1).strip()[:90]
    except Exception:
        pass
    return ""

def row(recall, path, desc):
    d = desc if desc else "—"
    return f"| `{recall}` | `{path}` | {d} |"

def table_header():
    return ["| Recall | File | Description |", "|--------|------|-------------|"]

# ── Load agents ───────────────────────────────────────────────────────────────
def load_agents():
    d = os.path.join(ROOT, ".agent", "agents")
    agents = {}
    for f in sorted(os.listdir(d)):
        if not f.endswith(".agent.md"): continue
        fpath = os.path.join(d, f)
        try:
            snippet = open(fpath, encoding='utf-8', errors='ignore').read(120)
            if "SKILL GATEWAY" in snippet: continue  # skip gateways
        except Exception:
            pass
        name = f.replace(".agent.md", "")
        desc = get_desc(fpath)
        agents[name] = (f".agent/agents/{f}", desc)
    return agents

# ── Load skills ───────────────────────────────────────────────────────────────
def load_skills():
    skills = []
    seen = set()

    # Define sources to scan
    SOURCES = [
        os.path.join(ROOT, ".agent", "skills"),
        os.path.join(ROOT, ".agent", "libs"),
        os.path.join(ROOT, ".agent", "docs"),
        os.path.join(ROOT, ".agent", "mcp")
    ]

    for src in SOURCES:
        if not os.path.exists(src): continue
        
        # We only care about .md files in these sectors
        for f in sorted(os.listdir(src)):
            if not f.endswith(".md"): continue
            if f.lower() in ("index.md", "readme.md", ".gitignore"): continue
            
            # Avoid gateway agents
            if f.endswith(".agent.md") and src.endswith("agents"): continue
            
            name = f.replace(".md", "")
            # If it's something like 'instructions_typescript.md' in docs, use that name
            rel_src = os.path.relpath(src, ROOT).replace("\\", "/")
            path = f"{rel_src}/{f}"
            
            if name in seen: continue
            seen.add(name)
            skills.append((name, path, get_desc(os.path.join(src, f))))

    return sorted(skills, key=lambda x: x[0].lower())

# ── Load workflows ────────────────────────────────────────────────────────────
def load_workflows():
    d = os.path.join(ROOT, ".agent", "workflows")
    wfs = []
    for f in sorted(os.listdir(d)):
        if not f.endswith(".md") or f == "README.md": continue
        name = f.replace(".md", "")
        desc = get_desc(os.path.join(d, f))
        wfs.append((name, f".agent/workflows/{f}", desc))
    return wfs

# ── Category mappings ─────────────────────────────────────────────────────────
AGENT_CATS = {
    "Mnemonic (Fast Access)": [
        "alpha", "react", "plan", "arch", "ops", "sec", "test", "python", "orchestrate"
    ],
    "Architecture & Design": lambda n: n.startswith("arch"),
    "Cloud & Azure": lambda n: n.startswith("cloud-azure"),
    "Data & Databases": lambda n: n.startswith("data-"),
    "DevOps & Infrastructure": lambda n: n.startswith("dev-devops") or n.startswith("ops-"),
    "Development (General)": lambda n: n.startswith("dev-") and not n.startswith("dev-devops"),
    "Language Specialists": lambda n: n.startswith("lang-"),
    "Planning & Management": lambda n: n.startswith("plan"),
    "Security": lambda n: n.startswith("sec"),
    "Testing & QA": lambda n: n.startswith("test"),
    "Frontend & UI": lambda n: n.startswith("ui-") or n.startswith("ux-"),
    "Power BI & Fabric": lambda n: "bi" in n or "power-bi" in n or "fabric" in n,
    "Orchestration & Agents": lambda n: n.startswith("orchestrate") or n.startswith("specsmd"),
    "Other": lambda n: True,
}

SKILL_CATS = {
    "Frontend & UI": ["frontend-skills", "industrial-hud-design", "ui-ux-pro-max",
                      "frontend-design", "web-design-reviewer"],
    "Backend & API": ["backend-skills", "api-patterns", "nestjs-expert", "nodejs-best-practices"],
    "React / Next.js": ["nextjs-best-practices", "nextjs-debugging-skills", "react-patterns", "frontend-slides"],
    "Python": ["python-ruff-linting-skills", "python-async-patterns-skills", "python-patterns"],
    "Cloud & Kubernetes": ["cloud-native-mastery", "aks-troubleshooting-skills",
                           "kubernetes-resource-optimization-skills",
                           "helm-configuration-skills", "dapr-configuration-skills",
                           "docker-expert", "deployment-procedures"],
    "Azure & IaC": ["azure-deployment-preflight", "azure-devops-cli", "azure-resource-visualizer",
                    "azure-role-selector", "azure-static-web-apps"],
    "DevOps & Automation": ["compound-engineering", "operator-automation", "saaspocalypse-skills",
                            "autonomous-operator-directives", "enterprise-meta-orchestration-guide",
                            "bash-linux", "powershell-windows"],
    "AI & Multi-Agent": ["universal-agentic-frameworks", "multi-agent-patterns-google-adk",
                          "brainstorming", "behavioral-modes", "parallel-agents",
                          "app-builder", "algolia-grounded-rag", "mcp-builder", "mcp-debugging-skills"],
    "Data & Analytics": ["fabric-prompts", "fabric-workforce", "database-skills",
                          "database-design", "docker-prisma-skills", "prisma-expert",
                          "performance-profiling"],
    "Project Management": ["primavera-p6-skills", "project-scheduling-best-practices",
                            "ms-project-skills", "senior-planner-scheduler-guide"],
    "Security": ["vulnerability-scanner", "red-team-tactics", "constitutional-ai-anthropic"],
    "Testing": ["testing-patterns", "webapp-testing", "tdd-workflow", "systematic-debugging",
                "debug-skills"],
    "Writing & Research": ["q1-journal-writing-skills", "white-paper-writing-skills",
                            "content-creation-research-guide", "notebooklm-mastery",
                            "linkedin-article-publisher"],
    "X / Social Media": ["x-marketing-expert"],
    "TypeScript / JS": ["typescript-expert", "tailwind-patterns"],
    "Mobile": ["mobile-design"],
    "MCP & Tools": ["mcp-builder", "mcp-cli", "gh-cli", "git-commit", "github-issues", "composio-claude-skills"],
    "ClaudeCode / Copilot": ["claude-code-slash-commands", "claude-code-templates-mastery",
                               "soul-templates", "anthropic-plugins-skills"],
    "Other Skills": [],
}

WF_CATS = {
    "Build & Create": ["create", "enhance", "app-builder", "create-spring-boot",
                        "create-spring-boot-kotlin", "create-implementation-plan",
                        "openapi-to-application-code"],
    "Planning": ["plan", "breakdown-plan", "breakdown-epic-arch", "breakdown-epic-pm",
                  "breakdown-feature-implementation", "breakdown-feature-prd", "brainstorm",
                  "create-architectural-decision-record", "create-technical-spike",
                  "create-specification", "create-implementation-plan", "update-implementation-plan",
                  "sa-plan", "sa-implement", "sa-generate"],
    "Deployment & DevOps": ["deploy", "alpha-cloud-deployment", "alpha-project-lifecycle",
                             "environment-setup", "phase5-chat-completion", "docker",
                             "devops-rollout-plan", "containerize-aspnet", "multi-stage-dockerfile",
                             "build-failures"],
    "Debugging & QA": ["debug", "complete-application-qa", "qa-kanban", "chat-testing",
                        "code-review-testing", "compound-development-cycle", "fixing"],
    "Security": ["security-audit", "security-remediation", "ai-prompt-engineering-safety-review"],
    "Git & GitHub": ["git-workflow-manager", "git-flow-branch-creator", "git-push-large-files",
                      "create-github-action-workflow-specification", "conventional-commit",
                      "create-github-issue", "create-github-pull-request",
                      "gemini-cli-github-integration", "github-best-practices"],
    "Data & Power BI": ["fabric-audit", "dax-optimize", "fabric-governance",
                         "power-bi-dax-optimization", "power-bi-model-design-review",
                         "power-bi-performance-troubleshooting", "power-bi-report-design",
                         "cosmosdb-datamodeling", "database-schema-changes",
                         "database-connection-issues", "postgresql"],
    "Kubernetes & Cloud": ["alpha-cloud-deployment", "az-cost-optimize", "azure-resource-health",
                            "docker-container-problems", "cors-errors", "authentication-issues",
                            "performance-problems"],
    "AI & Agents": ["orchestrate", "crewai-integration", "implement-agentic-rag",
                     "ai-ecosystem-monitoring", "gemini-quota-recovery", "mcp-create",
                     "csharp-mcp-server-generator", "python-mcp-server-generator",
                     "typescript-mcp-server-generator", "go-mcp-server-generator",
                     "java-mcp-server-generator"],
    "Documentation": ["readme", "create-readme", "documentation-maintenance",
                       "documentation-writer", "create-llms", "update-llms",
                       "architecture-blueprint-generator", "technology-stack-blueprint"],
    "Testing (Code)": ["playwright", "playwright-automation", "playwright-generate-test",
                         "pytest-coverage", "javascript-typescript-jest", "csharp-xunit",
                         "csharp-mstest"],
    "C# / .NET": ["csharp-async", "csharp-docs", "dotnet-best-practices",
                   "dotnet-design-pattern-review", "ef-core", "containerize-aspnetcore",
                   "containerize-aspnet-framework", "dotnet-upgrade-analysis"],
    "Writing & Research": ["write-white-paper", "manuscript-writing-flow", "research",
                             "medium-publishing-workflow", "latex-conversion",
                             "youtube-to-ebook", "create-course"],
    "X & Social": ["x-viral-optimizer"],
    "Workflows & Automation": ["workflow-orchestrator", "apply-for-jobs", "skill-upgrade",
                                 "project-wrap-up", "compound-development-cycle",
                                 "memory-merger", "remember", "copilot-monitoring"],
    "Other Workflows": [],
}

def categorize(items, cat_map, key_fn):
    """Assign items to categories. key_fn(item) returns the name to match."""
    assigned = {cat: [] for cat in cat_map}
    used = set()

    for item in items:
        name = key_fn(item)
        matched = False

        for cat, matcher in cat_map.items():
            if cat == "Other" or cat == "Other Skills" or cat == "Other Workflows":
                continue
            if isinstance(matcher, list):
                if name in matcher or any(name.startswith(m.replace("*","")) for m in matcher if "*" in m):
                    if name not in used:
                        assigned[cat].append(item)
                        used.add(name)
                        matched = True
                        break
            elif callable(matcher):
                if matcher(name) and name not in used:
                    assigned[cat].append(item)
                    used.add(name)
                    matched = True
                    break

        if not matched and name not in used:
            other_key = [k for k in cat_map if "Other" in k]
            if other_key:
                assigned[other_key[0]].append(item)
            used.add(name)

    return assigned

# ── Generate ──────────────────────────────────────────────────────────────────
agents = load_agents()
skills = load_skills()
workflows = load_workflows()
now = datetime.now().strftime("%Y-%m-%d %H:%M")

out = []
out.append(f"# KNOWLEDGE INDEX")
out.append(f"_Generated {now} | Total: {len(agents)} agents · {len(skills)} skills · {len(workflows)} workflows_")
out.append("")
out.append("> **Tip**: Press `Ctrl+F` and type any keyword to find files.")
out.append("> Then type that filename directly after `@` in Antigravity chat, or `/` for workflows.")
out.append("")
out.append("---")
out.append("")
out.append("## HOW TO RECALL")
out.append("")
out.append("| What | How | Example |")
out.append("|------|-----|---------|")
out.append("| Agent / Skill | Type `@` then filename | `@frontend-skills` → loads Frontend Skills |")
out.append("| Workflow | Type `/` then workflow name | `/plan` → opens planning workflow |")
out.append("| Any file | Type `@` → pick Files | Browse workspace files |")
out.append("| Rules | Type `@` → pick Rules | Browse `.agent/rules/` |")
out.append("| Terminal | Type `@` → pick Terminal | Use current terminal context |")
out.append("")
out.append("---")
out.append("")

# ═══════════════════════════════════════════════════════════════════════
# SECTION 1: AGENTS (@ recall)
# ═══════════════════════════════════════════════════════════════════════
out.append("# @ AGENTS")
out.append("")
out.append("Type `@name` directly in chat. Fuzzy search — partial names work.")
out.append("")

out.append("## ⚡ FAST MNEMONIC AGENTS")
out.append("")
fast = [
    ("@alpha",       ".agent/agents/alpha.agent.md",     "Ultimate autonomous beast — all domains"),
    ("@react",       ".agent/agents/react.agent.md",     "Expert React 19.2 frontend engineer"),
    ("@plan",        ".agent/agents/plan.agent.md",      "Project planner & implementation strategist"),
    ("@arch",        ".agent/agents/arch.agent.md",      "System architect & ADR writer"),
    ("@ops",         ".agent/agents/ops.agent.md",       "Terraform / Kubernetes / DevOps"),
    ("@sec",         ".agent/agents/sec.agent.md",       "Security auditor & DevSecOps"),
    ("@test",        ".agent/agents/test.agent.md",      "TDD / QA / Playwright expert"),
    ("@python",      ".agent/agents/python.agent.md",    "Python / MCP server developer"),
    ("@orchestrate", ".agent/agents/orchestrate.agent.md", "Multi-agent workflow orchestrator"),
]
out += table_header()
for recall, path, desc in fast:
    out.append(row(recall, path, desc))
out.append("")

# Categorized agents
agent_cats = categorize(
    [(n,) + v for n, v in agents.items()],
    {k: v for k, v in AGENT_CATS.items() if k != "Mnemonic (Fast Access)"},
    lambda x: x[0]
)

for cat, items in agent_cats.items():
    if not items: continue
    out.append(f"## {cat}")
    out.append("")
    out += table_header()
    for name, path, desc in sorted(items, key=lambda x: x[0]):
        out.append(row(f"@{name}", path, desc))
    out.append("")

out.append("---")
out.append("")

# ═══════════════════════════════════════════════════════════════════════
# SECTION 2: SKILLS (@ recall via filename)
# ═══════════════════════════════════════════════════════════════════════
out.append("# @ SKILLS")
out.append("")
out.append("Type `@` then the **filename** shown below. Antigravity fuzzy-finds it instantly.")
out.append("")

skill_cats = categorize(
    skills,
    SKILL_CATS,
    lambda x: x[0]
)

for cat, items in skill_cats.items():
    if not items: continue
    fname_hint = "SKILL.md" if "SKILL" in (items[0][1] if items else "") else items[0][0] if items else ""
    out.append(f"## {cat}")
    out.append("")
    out += table_header()
    for name, path, desc in sorted(items, key=lambda x: x[0]):
        fname = path.split("/")[-1]
        out.append(row(f"@{fname}", path, desc))
    out.append("")

out.append("---")
out.append("")

# ═══════════════════════════════════════════════════════════════════════
# SECTION 3: WORKFLOWS (/ slash commands)
# ═══════════════════════════════════════════════════════════════════════
out.append("# / WORKFLOWS")
out.append("")
out.append("Type `/name` in chat to invoke a workflow step-by-step.")
out.append("")

wf_cats = categorize(
    workflows,
    WF_CATS,
    lambda x: x[0]
)

for cat, items in wf_cats.items():
    if not items: continue
    out.append(f"## {cat}")
    out.append("")
    out += table_header()
    for name, path, desc in sorted(items, key=lambda x: x[0]):
        out.append(row(f"/{name}", path, desc))
    out.append("")

out.append("---")
out.append("")
out.append(f"_Total: {len(agents)} agents · {len(skills)} skills · {len(workflows)} workflows_")
out.append(f"_Regenerate: `python scripts/build_index.py`_")

content = "\n".join(out)
with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"[OK] {OUTPUT}")
print(f"  Agents:    {len(agents)}")
print(f"  Skills:    {len(skills)}")
print(f"  Workflows: {len(workflows)}")
print(f"  Lines:     {len(out)}")
