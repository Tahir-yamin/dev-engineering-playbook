import os
import json
import shutil
import re

ROOT = r"d:\my-dev-knowledge-base"
AGENT_DIR = os.path.join(ROOT, ".agent")
MCP_TARGET = os.path.join(AGENT_DIR, "mcp")
SKILLS_TARGET = os.path.join(AGENT_DIR, "skills", "harvested")
CONFIG_FILE = os.path.join(ROOT, "MCP_CONFIG_MANIFEST.json")

LIBS_TARGET = os.path.join(AGENT_DIR, "libs")
LIBS_TARGET = os.path.join(AGENT_DIR, "libs")

def ensure_dirs():
    for d in [MCP_TARGET, SKILLS_TARGET, LIBS_TARGET, os.path.join(MCP_TARGET, "core-servers")]:
        if not os.path.exists(d):
            os.makedirs(d)
            print(f"Created directory: {d}")

def relocate_libraries():
    print(">>> Relocating Core Libraries and Frameworks...")
    
    # Standard Libraries -> libs/
    libs_to_libs = ["gemini-cli", "langgraph"]
    for lib in libs_to_libs:
        source = os.path.join(ROOT, "external-libs", lib)
        dest = os.path.join(LIBS_TARGET, lib)
        if os.path.exists(source):
            if os.path.exists(dest):
                shutil.rmtree(dest, onexc=_handle_readonly)
            print(f"  Moving {lib} to {dest}")
            shutil.move(source, dest)

    # MCP Specific -> mcp/core-servers/
    mcp_to_mcp = ["entrez-mcp-server", "mcp-scholarly", "mcp-servers"]
    for server in mcp_to_mcp:
        source = os.path.join(ROOT, "external-libs", server)
        # mcp-servers maps to core-servers specifically
        folder_name = "core-servers" if server == "mcp-servers" else server
        dest = os.path.join(MCP_TARGET, "core-servers", folder_name)
        
        if os.path.exists(source):
            if os.path.exists(dest):
                shutil.rmtree(dest, onexc=_handle_readonly)
            print(f"  Moving {server} to {dest}")
            shutil.move(source, dest)

def migrate_mcp_servers():
    if not os.path.exists(CONFIG_FILE):
        print("!! No MCP_CONFIG_MANIFEST.json found. Skipping MCP migration.")
        return

    print(">>> Starting MCP Server Migration...")
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)

    changed = False
    servers = config.get("mcpServers", {})
    
    for name, data in servers.items():
        if "args" in data:
            args = data["args"]
            for i, arg in enumerate(args):
                if "external-libs" in arg:
                    # Extract the folder path
                    match = re.search(r'external-libs/([^/]+)', arg)
                    if match:
                        folder_name = match.group(1)
                        source_path = os.path.normpath(os.path.join(ROOT, "external-libs", folder_name))
                        dest_path = os.path.normpath(os.path.join(MCP_TARGET, folder_name))
                        
                        if os.path.exists(source_path):
                            print(f"  Migrating {name} from {source_path}")
                            print(f"  To: {dest_path}")
                            if os.path.exists(dest_path):
                                shutil.rmtree(dest_path) # Overwrite
                            shutil.move(source_path, dest_path)
                            
                            # Update path in config
                            new_arg = arg.replace(f"external-libs/{folder_name}", f".agent/mcp/{folder_name}")
                            args[i] = new_arg
                            changed = True

    if changed:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
        print("Done: MCP_CONFIG_MANIFEST.json updated with new sovereign paths.")
    else:
        print("  No MCP servers needed migration.")

def harvest_skills():
    print(">>> Starting Physical Skill Harvesting...")
    external_sources = [
        os.path.join(ROOT, "external-libs"),
        os.path.join(ROOT, "docs"),
        os.path.join(ROOT, "white-papers")
    ]
    
    total_harvested = 0
    for src in external_sources:
        if not os.path.exists(src): continue
        for root, dirs, files in os.walk(src):
            if ".git" in root: continue
            for f in files:
                if f.lower() == "skill.md" or f.lower().endswith(".agent.md") or f.lower() == "instructions.md":
                    # For SKILL.md, use folder name
                    if f.lower() in ["skill.md", "instructions.md"]:
                        parent_name = os.path.basename(root)
                        if parent_name == "skills":
                             parent_name = os.path.basename(os.path.dirname(root))
                        dest_fname = f"{parent_name}.md"
                    else:
                        dest_fname = f

                    source_file = os.path.join(root, f)
                    dest_file = os.path.join(SKILLS_TARGET, dest_fname)
                    
                    # Physical Copy
                    shutil.copy2(source_file, dest_file)
                    total_harvested += 1

    print(f"Done: Harvested {total_harvested} files into {SKILLS_TARGET}")

def _handle_readonly(func, path, exc_info):
    import stat
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

def purge_external_libs():
    print(">>> Purging Harvested External-Libs...")
    ext_libs_doc_only = [
        "antigravity-awesome-skills",
        "composio-awesome-claude-skills",
        "vercel-agent-skills",
        "anthropic-quickstarts",
        "awesome-claude-code-subagents",
        "awesome-claude-skills",
        "claude-code-templates",
        "claude-mcps-and-prompts",
        "github-awesome-copilot",
        "knowledge-work-plugins",
        "scraper-twitter-mcp",
        "skills",
        "specs.md",
        "WriteHERE",
        "video-editing-mcp"
    ]
    
    for folder in ext_libs_doc_only:
        path = os.path.join(ROOT, "external-libs", folder)
        if os.path.exists(path):
            print(f"  Purging folder: {folder}")
            # Use onexc for Python 3.12+ or onerror for older
            shutil.rmtree(path, onexc=_handle_readonly)
    print("Done: Purge complete.")

def main():
    print("=" * 60)
    print("  SOVEREIGN CONSOLIDATION -- Antigravity IDE")
    print("=" * 60)
    ensure_dirs()
    migrate_mcp_servers()
    relocate_libraries()
    harvest_skills()
    purge_external_libs()
    print("-" * 60)
    print("Consolidation Complete.")
    print("Next: Run update_registry.py to refresh the index.")
    print("=" * 60)

if __name__ == "__main__":
    main()
