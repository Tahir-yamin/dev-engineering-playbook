import os
import shutil
import re

ROOT = r"d:\my-dev-knowledge-base"
SKILLS_DIR = os.path.join(ROOT, ".agent", "skills")

def _handle_readonly(func, path, exc_info):
    import stat
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

def flatten_directory(base_dir):
    print(f">>> Flattening {base_dir}...")
    
    # 1. First, handle the 'harvested' folder specifically (no prefix needed)
    harvested = os.path.join(base_dir, "harvested")
    if os.path.exists(harvested):
        print("  Moving files from 'harvested' to root...")
        for f in os.listdir(harvested):
            src = os.path.join(harvested, f)
            dest = os.path.join(base_dir, f)
            if os.path.exists(dest):
                # Collision check
                base, ext = os.path.splitext(f)
                dest = os.path.join(base_dir, f"{base}_coll.{ext}")
            shutil.move(src, dest)
        shutil.rmtree(harvested, onexc=_handle_readonly)

    # 2. Iterate over other subdirectories
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path):
            dir_name = item
            print(f"  Processing folder: {dir_name}")
            
            # Walk the subdirectory
            for root, dirs, files in os.walk(item_path, topdown=False):
                for f in files:
                    src_file = os.path.join(root, f)
                    rel_path = os.path.relpath(src_file, item_path)
                    
                    # Flatten the path name
                    # Exception: If it's the main SKILL.md or instructions.md, rename to dir_name.md
                    if f.lower() in ["skill.md", "instructions.md"] and os.path.dirname(rel_path) == ".":
                         flat_name = f"{dir_name}.md"
                    else:
                         # Replace backslashes/slashes with underscores
                         clean_rel = rel_path.replace(os.sep, "_").replace("/", "_")
                         flat_name = f"{dir_name}_{clean_rel}"
                    
                    dest_file = os.path.join(base_dir, flat_name)
                    
                    # Move and handle collisions
                    if os.path.exists(dest_file):
                         base, ext = os.path.splitext(flat_name)
                         dest_file = os.path.join(base_dir, f"{base}_dup{ext}")
                    
                    try:
                        shutil.move(src_file, dest_file)
                    except Exception as e:
                        print(f"    Error moving {f}: {e}")

            # Delete the now-empty subdirectory
            try:
                shutil.rmtree(item_path, onexc=_handle_readonly)
            except Exception as e:
                print(f"    Error deleting folder {dir_name}: {e}")

    print("Flattening complete.")

if __name__ == "__main__":
    flatten_directory(SKILLS_DIR)
