import os

ROOT = r"d:\my-dev-knowledge-base\external-libs"
results = []

for root, dirs, files in os.walk(ROOT):
    # Check for skills directory
    if "skills" in [d.lower() for d in dirs]:
        results.append(os.path.join(root, "skills"))
    
    # Check for skill-like files
    for f in files:
        if f.lower() in ["skill.md", "instructions.md", "prompt.md", "system.md"]:
            results.append(os.path.join(root, f))
        elif f.lower().endswith(".agent.md"):
             results.append(os.path.join(root, f))

for r in sorted(list(set(results))):
    print(r)
