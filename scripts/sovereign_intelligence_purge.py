import os
import shutil
import stat

ROOT = r"d:\my-dev-knowledge-base"
AGENT_ROOT = os.path.join(ROOT, ".agent")

GARBAGE_DIRS = [".git", "node_modules", ".next", "__pycache__", "dist", "build", ".turbo", ".vercel"]
GARBAGE_FILES = [
    "package-lock.json", "package.json", "yarn.lock", "pnpm-lock.yaml", 
    "tsconfig.json", "eslint.config.mjs", "postcss.config.mjs", "next.config.ts", 
    "next-env.d.ts", "BUILD_ID", ".env.local"
]

def _handle_readonly(func, path, exc_info):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except:
        pass

def purge_aggressive():
    print(">>> Aggressive Purge of .agent sectors...")
    sectors = ["agents", "docs", "skills", "workflows", "libs", "rules"]
    
    total_purged = 0
    
    for sector in sectors:
        sector_path = os.path.join(AGENT_ROOT, sector)
        if not os.path.exists(sector_path):
            continue
            
        print(f"  Walking sector: {sector}...")
        for root, dirs, files in os.walk(sector_path, topdown=False):
            # Kill garbage directories
            for d in dirs:
                if d in GARBAGE_DIRS:
                    d_path = os.path.join(root, d)
                    print(f"    Removing dir: {d_path}")
                    shutil.rmtree(d_path, onerror=_handle_readonly)
                    total_purged += 1
            
            # Kill garbage files
            for f in files:
                if f in GARBAGE_FILES or any(f.endswith(ext) for ext in [".js.map", ".ts.map", ".pyc"]):
                    f_path = os.path.join(root, f)
                    try:
                        os.chmod(f_path, stat.S_IWRITE)
                        os.remove(f_path)
                        total_purged += 1
                    except:
                        pass
                        
    print(f">>> Aggressive Purge complete. Total items removed: {total_purged}")

if __name__ == "__main__":
    purge_aggressive()
