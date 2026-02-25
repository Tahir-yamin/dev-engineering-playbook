import os

RULES_DIR = r"d:\my-dev-knowledge-base\.agent\rules"
TARGET_DIR = r"d:\my-dev-knowledge-base\.github\agents"

if not os.path.exists(TARGET_DIR):
    os.makedirs(TARGET_DIR)

def move_and_fix():
    files = [f for f in os.listdir(RULES_DIR) if f.endswith(".md")]
    for f in files:
        src = os.path.join(RULES_DIR, f)
        dst = os.path.join(TARGET_DIR, f)
        
        with open(src, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Add target: 'vscode' and infer: true if in the rules folder
        if "---" in content:
            parts = content.split("---", 2)
            frontmatter = parts[1]
            if "target:" not in frontmatter:
                frontmatter += "\ntarget: 'vscode'"
            if "infer:" not in frontmatter:
                frontmatter += "\ninfer: true"
            content = f"---{frontmatter}---{parts[2]}"
            
        with open(dst, 'w', encoding='utf-8') as file:
            file.write(content)
            
        os.remove(src)
        print(f"Moved and fixed: {f}")

if __name__ == "__main__":
    move_and_fix()
