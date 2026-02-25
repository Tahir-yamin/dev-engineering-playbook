import os

ROOT = r"d:\my-dev-knowledge-base"

def count_files(directory):
    total = 0
    for root, dirs, files in os.walk(directory):
        total += len(files)
    return total

categories = {
    "Maestro Hub (.agent)": os.path.join(ROOT, ".agent"),
    "External Libs & Accelerators": os.path.join(ROOT, "external-libs"),
    "Skills & Knowledge": os.path.join(ROOT, "skills"),
    "Job Apps & Career": os.path.join(ROOT, "job-application"),
    "GitHub Meta & Archive": os.path.join(ROOT, ".github"),
    "Browser Profiles (Data)": os.path.join(ROOT, "agent_chrome_profile"),
    "Temporary & Scraper Data": os.path.join(ROOT, "temp_scraper_profile"),
    "Legacy Archive": os.path.join(ROOT, "LEGACY_ARCHIVE"),
    "Core Documentation (docs)": os.path.join(ROOT, "docs"),
    "Scripts & Utilities": os.path.join(ROOT, "scripts"),
}

print(f"{'Category':<35} | {'File Count':<10}")
print("-" * 50)

grand_total = 0
for name, path in categories.items():
    if os.path.exists(path):
        count = count_files(path)
        print(f"{name:<35} | {count:<10}")
        grand_total += count
    else:
        print(f"{name:<35} | {'N/A':<10}")

# Count root files separately
root_files = len([f for f in os.listdir(ROOT) if os.path.isfile(os.path.join(ROOT, f))])
print(f"{'Root Context Files':<35} | {root_files:<10}")
grand_total += root_files

print("-" * 50)
print(f"{'GRAND TOTAL (Tracked Categories)':<35} | {grand_total:<10}")
