"""
Build a fast SKILL_NAMES.md — clean list of every skill/agent filename
so users know exactly what to type after @ in Antigravity.
"""

import os
import re

ROOT = r"d:\my-dev-knowledge-base"
OUTPUT = os.path.join(ROOT, "SKILL_NAMES.md")

def get_desc(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for _ in range(20):
                line = f.readline()
                if line.lower().startswith("description:"):
                    return line.split(":", 1)[1].strip().strip('"\'')[:80]
                m = re.match(r'^#{1,2}\s+(.+)', line)
                if m:
                    return m.group(1).strip()[:80]
    except Exception:
        pass
    return ""

def rel(path):
    return path.replace(ROOT + os.sep, "").replace("\\", "/")

# ── Collect all resources ────────────────────────────────────────────────────

sections = {
    "agents":    [],
    "skills":    [],
    "workflows": [],
}

# Agents (.agent/agents/)
agent_dir = os.path.join(ROOT, ".agent", "agents")
for f in sorted(os.listdir(agent_dir)):
    if f.endswith(".agent.md") and "gateway" not in open(os.path.join(agent_dir, f), encoding='utf-8', errors='ignore').read(80):
        name = f.replace(".agent.md", "")
        desc = get_desc(os.path.join(agent_dir, f))
        sections["agents"].append((name, f".agent/agents/{f}", desc))

# Skills (skills/ — top-level .md files and SKILL.md files)
skills_dir = os.path.join(ROOT, "skills")
for dirpath, _, filenames in os.walk(skills_dir):
    for f in sorted(filenames):
        if not f.endswith(".md"): continue
        depth = len(os.path.relpath(dirpath, skills_dir).split(os.sep))
        is_skill_md = f == "SKILL.md"
        is_top = depth == 1 and f.endswith(".md") and f != "INDEX.md"
        if is_skill_md or is_top:
            fpath = os.path.join(dirpath, f)
            rel_path = rel(fpath)
            desc = get_desc(fpath)
            # Display name
            if is_skill_md:
                display = os.path.basename(dirpath)
            else:
                display = f.replace(".md", "")
            sections["skills"].append((display, rel_path, desc))

# Antigravity-kit skills
akit = os.path.join(ROOT, "external-libs", "antigravity-kit", ".agent", "skills")
for dirpath, _, filenames in os.walk(akit):
    for f in filenames:
        if f == "SKILL.md":
            fpath = os.path.join(dirpath, f)
            folder = os.path.basename(dirpath)
            desc = get_desc(fpath)
            sections["skills"].append((f"[kit] {folder}", rel(fpath), desc))

# Workflows (.agent/workflows/)
wf_dir = os.path.join(ROOT, ".agent", "workflows")
for f in sorted(os.listdir(wf_dir)):
    if f.endswith(".md"):
        name = f.replace(".md", "")
        desc = get_desc(os.path.join(wf_dir, f))
        sections["workflows"].append((name, f".agent/workflows/{f}", desc))

# ── Write output ─────────────────────────────────────────────────────────────
lines = []
lines.append("# HOW TO USE @ IN ANTIGRAVITY")
lines.append("")
lines.append("When you type `@` in the chat box, Antigravity opens a picker with:")
lines.append("- **Files** → any file in your workspace")
lines.append("- **Rules** → `.agent/rules/`")  
lines.append("- **Terminal** → current terminal output")
lines.append("- **Conversations** → past chat history")
lines.append("")
lines.append("**Just start typing after `@`** — it fuzzy-searches all file names.")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## QUICK REFERENCE — What to type after @")
lines.append("")

# Fast agents
lines.append("### Fastest: Mnemonic @agents")
lines.append("| Type this | Gets you |")
lines.append("|-----------|----------|")
mnemonics = [
    ("@react", "Expert React 19.2 engineer"),
    ("@alpha", "Ultimate autonomous agent"),
    ("@plan", "Project planner & strategist"),
    ("@arch", "System architect"),
    ("@ops", "Terraform / Kubernetes / DevOps"),
    ("@sec", "Security auditor"),
    ("@test", "TDD / QA expert"),
    ("@python", "Python developer"),
    ("@orchestrate", "Multi-agent orchestrator"),
]
for cmd, desc in mnemonics:
    lines.append(f"| `{cmd}` | {desc} |")

lines.append("")
lines.append("---")
lines.append("")

# Skills
lines.append(f"## SKILLS — type @  then the filename  ({len(sections['skills'])} available)")
lines.append("")
lines.append("| Type after @ | File | Description |")
lines.append("|---|---|---|")
for name, path, desc in sorted(sections["skills"], key=lambda x: x[0]):
    # Show just the filename for fuzzy search hint
    fname = path.split("/")[-1]
    lines.append(f"| `{fname}` | `{path}` | {desc} |")

lines.append("")
lines.append("---")
lines.append("")

# Agents  
lines.append(f"## AGENTS — type @ then agent name  ({len(sections['agents'])} available)")
lines.append("")
lines.append("| Type after @ | File | Description |")
lines.append("|---|---|---|")
for name, path, desc in sections["agents"]:
    lines.append(f"| `{name}` | `{path}` | {desc} |")

lines.append("")
lines.append("---")
lines.append("")

# Workflows
lines.append(f"## WORKFLOWS — type / then name  ({len(sections['workflows'])} available)")
lines.append("")
lines.append("| Type after / | File | Description |")
lines.append("|---|---|---|")
for name, path, desc in sections["workflows"]:
    lines.append(f"| `/{name}` | `{path}` | {desc} |")

lines.append("")
lines.append("---")
lines.append("")
lines.append("## FILES — reference ANY workspace file directly")
lines.append("")
lines.append("You can also type @ and browse to reference ANY file:")
lines.append("```")
lines.append("@ white-papers/wp6-multi-agent-systems.md")
lines.append("@ kubernetes/README.md")
lines.append("@ MASTER_KNOWLEDGE_INDEX.md")
lines.append("@ external-libs/antigravity-kit/.agent/skills/frontend-design/SKILL.md")
lines.append("```")

content = "\n".join(lines)
with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"[OK] Written: {OUTPUT}")
print(f"  Agents:    {len(sections['agents'])}")
print(f"  Skills:    {len(sections['skills'])}")
print(f"  Workflows: {len(sections['workflows'])}")
print(f"  Total rows: {len(sections['agents']) + len(sections['skills']) + len(sections['workflows'])}")
