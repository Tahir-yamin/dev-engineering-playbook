import os

DIR = r"d:\my-dev-knowledge-base\.github\agents"

def cleanup_lints():
    files = [f for f in os.listdir(DIR) if f.endswith(".md")]
    for f in files:
        path = os.path.join(DIR, f)
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        if "---" in content:
            parts = content.split("---", 2)
            lines = parts[1].split("\n")
            new_lines = [l for l in lines if not l.strip().startswith("skills:")]
            new_frontmatter = "\n".join(new_lines)
            new_content = f"---{new_frontmatter}---{parts[2]}"
            
            with open(path, 'w', encoding='utf-8') as file:
                file.write(new_content)

if __name__ == "__main__":
    cleanup_lints()
