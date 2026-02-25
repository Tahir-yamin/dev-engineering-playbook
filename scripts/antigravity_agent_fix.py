import os
import shutil

# Sources: We have files in .github/agents/ (where they currently are)
SRC_DIR = r"d:\my-dev-knowledge-base\.github\agents"
# Official Antigravity/Claude Code Target
DST_DIR = r"d:\my-dev-knowledge-base\.claude\agents"

MAPPING = {
    "alpha-beast.agent.md": "alpha.md",
    "ui-react.agent.md": "react.md",
    "ops-terraform.agent.md": "ops.md",
    "sec-auditor.agent.md": "sec.md",
    "lang-python.agent.md": "python.md",
    "plan-main.agent.md": "plan.md",
    "arch-main.agent.md": "arch.md",
    "test-tdd.agent.md": "test.md"
}

if not os.path.exists(DST_DIR):
    os.makedirs(DST_DIR)

def migrate():
    for old_name, new_name in MAPPING.items():
        src = os.path.join(SRC_DIR, old_name)
        dst = os.path.join(DST_DIR, new_name)
        
        if os.path.exists(src):
            with open(src, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract name and fix frontmatter for Claude Code
            # Claude Code expects name: 'short-name' without spaces for recall
            short_id = new_name.replace(".md", "")
            
            if "---" in content:
                parts = content.split("---", 2)
                frontmatter = parts[1]
                # Ensure name is simple for @ recall
                if f"name: {short_id}" not in frontmatter:
                    frontmatter = f"\nname: {short_id}\n" + frontmatter
                
                content = f"---{frontmatter}---{parts[2]}"
            
            with open(dst, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Migrated: {old_name} -> {new_name}")
        else:
            print(f"Source missing: {old_name}")

if __name__ == "__main__":
    migrate()
