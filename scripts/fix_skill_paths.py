import os
import re

ROOT = r"d:\my-dev-knowledge-base"
SKILLS_DIR = os.path.join(ROOT, ".agent", "skills")

FOLDERS = [
    "agent-commands", "agentic-eval", "algolia-grounded-rag", "api-patterns", "app-builder", 
    "appinsights-instrumentation", "architecture", "azure-deployment-preflight", "azure-devops-cli", 
    "azure-resource-visualizer", "azure-role-selector", "azure-static-web-apps", "bash-linux", 
    "behavioral-modes", "brainstorming", "chrome-devtools", "clean-code", "code-review-checklist", 
    "copilot", "database-design", "deployment-procedures", "docker-expert", "documentation-templates", 
    "frontend-design", "frontend-slides", "game-development", "geo-fundamentals", "gh-cli", 
    "git-commit", "github-issues", "i18n-localization", "image-manipulation-image-magick", 
    "latex-conversion", "legacy-circuit-mockups", "lint-and-validate", "make-skill-template", 
    "mcp-builder", "mcp-cli", "microsoft-code-reference", "microsoft-docs", "mobile-design", 
    "nestjs-expert", "neuro-clinical-auditing", "nextjs-best-practices", "nodejs-best-practices", 
    "notebooklm-cleaning", "nuget-manager", "parallel-agents", "performance-profiling", 
    "plan-writing", "plantuml-ascii", "powershell-windows", "prd", "prisma-expert", 
    "project-management", "python-patterns", "react-patterns", "red-team-tactics", "refactor", 
    "seo-fundamentals", "server-management", "skill-seekers", "snowflake-semanticview", 
    "systematic-debugging", "tailwind-patterns", "tdd-workflow", "testing-patterns", 
    "typescript-expert", "ui-ux-pro-max", "vscode-ext-commands", "vscode-ext-localization", 
    "vulnerability-scanner", "web-design-reviewer", "webapp-testing", "youtube-to-ebook"
]

def fix_references():
    print(">>> Correcting internal skill references...")
    
    for filename in os.listdir(SKILLS_DIR):
        if not filename.endswith(".md"): continue
        fpath = os.path.join(SKILLS_DIR, filename)
        
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        new_content = content
        
        for folder in FOLDERS:
            # First, fix the broken .agent_skills_ prefix from previous run
            broken_prefix = f".agent_skills_{folder}_"
            fixed_prefix = f".agent/skills/{folder}_"
            new_content = new_content.replace(broken_prefix, fixed_prefix)

            # Fix local relative paths in the skill's own file
            if filename == f"{folder}.md" or filename == f"{folder}_SKILL.md":
                for sub in ["scripts", "data", "assets", "references", "examples"]:
                    # Ensure we point to the flattened file in the SAME DIR
                    # ./scripts/foo -> folder_scripts_foo
                    new_content = new_content.replace(f"./{sub}/", f"{folder}_{sub}_")
                    # handle bare scripts/
                    pattern = r"(?<![/\.a-z0-9_-])" + re.escape(sub) + r"/"
                    new_content = re.sub(pattern, f"{folder}_{sub}_", new_content)

            # Fix long paths
            prefixes = [".claude/skills/", ".agent/skills/"]
            for prefix in prefixes:
                old_base = f"{prefix}{folder}/"
                new_base = f".agent/skills/{folder}_"
                
                if old_base in new_content:
                    def remap(match):
                        path = match.group(0)
                        suffix = path[len(old_base):]
                        return new_base + suffix.replace("/", "_").replace("\\", "_")
                    
                    pattern = re.escape(old_base) + r"[^ \n\)\"\'`]+"
                    new_content = re.sub(pattern, remap, new_content)

        if new_content != content:
            print(f"  Fixed paths in: {filename}")
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)

    print("Reference correction complete.")

if __name__ == "__main__":
    fix_references()
