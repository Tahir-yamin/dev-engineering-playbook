import os
import shutil
import subprocess

ROOT = r"d:\my-dev-knowledge-base"
AGENT_ROOT = os.path.join(ROOT, ".agent")

# Strict keep list
KEEP_IN_ROOT = [
    ".agent", ".git", ".venv", ".vscode", "scripts", 
    "ARCHITECTURE.md", "GEMINI.md", "README.md", "KNOWLEDGE_INDEX.md",
    "CLEAN_BRAIN_POLICY.md", "CODEBASE.md", "COMMAND_CENTER.md",
    "MASTER_KNOWLEDGE_INDEX.md", "MCP_CONFIG_MANIFEST.json", 
    ".gitignore", ".env"
]

# Explicit Sector Mapping
SECTOR_MAP = {
    "agents": "agents",
    "docs": "docs",
    "skills": "skills",
    "workflows": "workflows",
    "libs": "libs",
    "rules": "rules"
}

def robust_move_folder(src, dst):
    if not os.path.exists(src): return
    print(f"  Consolidating folder: {os.path.basename(src)} -> {os.path.relpath(dst, AGENT_ROOT)}")
    
    # Use robocopy for speed and robustness on Windows if available
    try:
        # /MOVE moves files and dirs, /E subdirs including empty, /IS include same files, /IT include tweaked files
        # /NP no progress, /NFL no file list, /NDL no dir list (for silence)
        # /R:0 /W:0 - skip locked files immediately
        subprocess.run(['robocopy', src, dst, '/MOVE', '/E', '/IS', '/IT', '/NP', '/NFL', '/NDL', '/R:0', '/W:0'], 
                       capture_output=True)
        # Robocopy might leave the empty source shell root if it's in use or special
        if os.path.exists(src) and not os.listdir(src):
            os.rmdir(src)
    except Exception as e:
        # Fallback to shutil
        try:
            if os.path.exists(dst):
                for item in os.listdir(src):
                    s = os.path.join(src, item)
                    d = os.path.join(dst, item)
                    if os.path.isdir(s): robust_move_folder(s, d)
                    else: shutil.move(s, d)
                os.rmdir(src)
            else:
                shutil.move(src, dst)
        except Exception as e2:
            print(f"    Failed to move {src}: {e2}")

def robust_move_file(src, dst):
    if not os.path.exists(src): return
    try:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(dst):
            base, ext = os.path.splitext(dst)
            dst = f"{base}_coll{ext}"
        shutil.move(src, dst)
    except Exception as e:
        print(f"    Failed to move file {src}: {e}")

def consolidate():
    print(">>> ULTIMATE SOVEREIGN CONSOLIDATION <<<")
    
    for item in os.listdir(ROOT):
        if item in KEEP_IN_ROOT: continue
        
        src_path = os.path.join(ROOT, item)
        
        # 1. Route based on item type and name
        if os.path.isdir(src_path):
            if item in SECTOR_MAP:
                target = os.path.join(AGENT_ROOT, SECTOR_MAP[item])
            else:
                target = os.path.join(AGENT_ROOT, "libs", item)
            robust_move_folder(src_path, target)
        else:
            # It's a file
            target = os.path.join(AGENT_ROOT, "docs", item)
            robust_move_file(src_path, target)

def flatten():
    print(">>> Flattening intelligence sectors...")
    sectors = ["agents", "docs", "skills", "workflows", "libs", "rules"]
    exclude = [".git", "node_modules", ".venv", "__pycache__", ".history"]
    
    for sector in sectors:
        sector_path = os.path.join(AGENT_ROOT, sector)
        if not os.path.exists(sector_path): continue
        
        print(f"  Sector: {sector}")
        # Use topdown=False to process children first for easy rmdir
        for root, dirs, files in os.walk(sector_path, topdown=False):
            if any(ex in root.split(os.sep) for ex in exclude): continue
            if root == sector_path: continue
            
            rel = os.path.relpath(root, sector_path)
            for f in files:
                src = os.path.join(root, f)
                # Entry point logic
                if f.lower() in ["skill.md", "instructions.md", "prompt.md", "system.md"]:
                    parts = rel.split(os.sep)
                    flat_name = f"{parts[-1]}.md" if parts else f
                else:
                    prefix = rel.replace(os.sep, "_").replace("/", "_")
                    flat_name = f"{prefix}_{f}"
                
                dest = os.path.join(sector_path, flat_name)
                if os.path.exists(dest):
                    base, ext = os.path.splitext(flat_name)
                    dest = os.path.join(sector_path, f"{base}_alt{ext}")
                
                try:
                    shutil.move(src, dest)
                except:
                    pass
            
            # Try to cleanup empty dir
            if not os.listdir(root):
                try: os.rmdir(root)
                except: pass

def main():
    consolidate()
    flatten()
    print(">>> Consolidation Complete. Root is Clean.")

if __name__ == "__main__":
    main()
