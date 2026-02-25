import os
import shutil
import filecmp

ROOT = r"d:\my-dev-knowledge-base"
SOURCE_SKILLS = os.path.join(ROOT, "skills")
TARGET_SKILLS = os.path.join(ROOT, ".agent", "skills")
HARVESTED_DIR = os.path.join(TARGET_SKILLS, "harvested")

def _handle_readonly(func, path, exc_info):
    import stat
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

def merge_folders(src, dest):
    if not os.path.exists(src):
        return
    if not os.path.exists(dest):
        os.makedirs(dest)

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            merge_folders(s, d)
        else:
            if os.path.exists(d):
                if filecmp.cmp(s, d, shallow=False):
                    continue
                else:
                    base, ext = os.path.splitext(item)
                    d_new = os.path.join(dest, f"{base}.merged{ext}")
                    shutil.copy2(s, d_new)
            else:
                shutil.copy2(s, d)

def consolidate():
    if not os.path.exists(SOURCE_SKILLS):
        print("Source skills folder not found.")
        return

    if not os.path.exists(HARVESTED_DIR):
        os.makedirs(HARVESTED_DIR)

    print(f">>> Consolidating root skills into {TARGET_SKILLS}...")

    for item in os.listdir(SOURCE_SKILLS):
        src_item = os.path.join(SOURCE_SKILLS, item)
        
        # 1. Top-level .md files -> harvested/
        if os.path.isfile(src_item) and item.endswith(".md"):
            if item == "INDEX.md": continue # Skip the index
            dest_item = os.path.join(HARVESTED_DIR, item)
            print(f"  Harvesting: {item}")
            shutil.copy2(src_item, dest_item)
        
        # 2. Directories -> .agent/skills/
        elif os.path.isdir(src_item):
            dest_item = os.path.join(TARGET_SKILLS, item)
            print(f"  Merging directory: {item}")
            merge_folders(src_item, dest_item)

    # 3. Purge source
    print("Purging root skills folder...")
    shutil.rmtree(SOURCE_SKILLS, onexc=_handle_readonly)
    print("Consolidation complete.")

if __name__ == "__main__":
    consolidate()
