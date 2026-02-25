import os
import shutil

ROOT = r"d:\my-dev-knowledge-base"
AGENT_DIR = os.path.join(ROOT, ".agent", "agents")
AGENT_RULES = os.path.join(ROOT, ".agent", "rules")
CLAUDE_AGENTS = os.path.join(ROOT, ".claude", "agents")
GITHUB_AGENTS = os.path.join(ROOT, ".github", "agents")

def fix_antigravity():
    # 1. Handle the 'agents' file collision
    if os.path.isfile(AGENT_DIR):
        print(f"Fixing file/dir collision: {AGENT_DIR}")
        # Save content of the file to a proper location
        with open(AGENT_DIR, 'r', encoding='utf-8') as f:
            orchestrator_content = f.read()
        
        os.remove(AGENT_DIR)
        os.makedirs(AGENT_DIR)
        
        # Save the orchestrator back as a proper agent
        with open(os.path.join(AGENT_DIR, "orchestrate.agent.md"), 'w', encoding='utf-8') as f:
            f.write(orchestrator_content)
    elif not os.path.exists(AGENT_DIR):
        os.makedirs(AGENT_DIR)
        print(f"Created directory: {AGENT_DIR}")

    # 2. Collect agents from all previous attempts
    sources = [CLAUDE_AGENTS, GITHUB_AGENTS, AGENT_RULES]
    
    # Key mapping
    MAPPING = {
        "alpha.md": "alpha.agent.md",
        "react.md": "react.agent.md",
        "ops.md": "ops.agent.md",
        "sec.md": "sec.agent.md",
        "python.md": "python.agent.md",
        "plan.md": "plan.agent.md",
        "arch.md": "arch.agent.md",
        "test.md": "test.agent.md"
    }

    # Also check the mnemonic long names
    LONG_MAPPING = {
        "alpha-beast.agent.md": "alpha.agent.md",
        "ui-react.agent.md": "react.agent.md",
        "ops-terraform.agent.md": "ops.agent.md",
        "sec-auditor.agent.md": "sec.agent.md",
        "lang-python.agent.md": "python.agent.md",
        "plan-main.agent.md": "plan.agent.md",
        "arch-main.agent.md": "arch.agent.md",
        "test-tdd.agent.md": "test.agent.md"
    }

    for src_dir in sources:
        if not os.path.exists(src_dir): continue
        files = os.listdir(src_dir)
        for f in files:
            src_path = os.path.join(src_dir, f)
            dst_name = None
            if f in MAPPING: dst_name = MAPPING[f]
            elif f in LONG_MAPPING: dst_name = LONG_MAPPING[f]
            elif f.endswith(".agent.md"): dst_name = f
            elif f.endswith(".md") and "agent" in f: dst_name = f.replace(".md", ".agent.md")

            if dst_name:
                dst_path = os.path.join(AGENT_DIR, dst_name)
                # Keep existing file in src? No, move them all to the registry.
                # Actually, let's copy to be safe, then cleanup.
                
                with open(src_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Standardize Frontmatter for Antigravity Recall
                id = dst_name.replace(".agent.md", "")
                if "---" in content:
                    parts = content.split("---", 2)
                    frontmatter = parts[1]
                    # Ensure name: 'id' is at the top
                    lines = frontmatter.strip().split("\n")
                    new_lines = [l for l in lines if not (l.startswith("name:") or l.startswith("target:") or l.startswith("infer:"))]
                    new_frontmatter = f"\nname: '{id}'\ntarget: 'vscode'\ninfer: true\n" + "\n".join(new_lines)
                    content = f"---{new_frontmatter}\n---{parts[2]}"
                
                with open(dst_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Activated Agent: {id} in {AGENT_DIR}")

if __name__ == "__main__":
    fix_antigravity()
