import os

AGENT_DIR = r"d:\my-dev-knowledge-base\.agent\agents"

def cleanup_frontmatter():
    if not os.path.exists(AGENT_DIR): return
    
    for f in os.listdir(AGENT_DIR):
        if not f.endswith(".agent.md"): continue
        path = os.path.join(AGENT_DIR, f)
        
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        if "---" in content:
            parts = content.split("---", 2)
            header = parts[0]
            frontmatter = parts[1]
            body = parts[2]
            
            lines = frontmatter.strip().split("\n")
            seen_name = False
            new_lines = []
            
            # The first 'name:' should be the simple ID
            short_id = f.replace(".agent.md", "")
            new_lines.append(f"name: '{short_id}'")
            new_lines.append("target: 'vscode'")
            new_lines.append("infer: true")
            
            for line in lines:
                if line.startswith("name:") or line.startswith("target:") or line.startswith("infer:"):
                    continue
                new_lines.append(line)
            
            new_frontmatter = "\n".join(new_lines)
            new_content = f"---{new_frontmatter}\n---{body}"
            
            with open(path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f"Cleaned up frontmatter for: {f}")

if __name__ == "__main__":
    cleanup_frontmatter()
