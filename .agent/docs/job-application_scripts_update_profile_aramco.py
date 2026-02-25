import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE_PATH = os.path.join(BASE_DIR, "data", "master_profile.json")

def update_profile():
    with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # New keywords to ensure are present
    new_keywords = [
        "ARAMCO Standards",
        "SAEP-331",
        "Planner III",
        "Senior Planning Engineer",
        "S-Curves",
        "Histograms",
        "Progress Reports",
        "Resource Loading"
    ]
    
    # Update Keywords List (Merge and Deduplicate)
    current_keywords = set(data.get("keywords", []))
    for kw in new_keywords:
        current_keywords.add(kw)
    
    # Restore essential keywords if they were lost (just in case)
    essentials = ["Primavera P6", "EPC", "Project Controls", "Risk Analysis", "Delay Analysis", "FIDIC", "Claim Management"]
    for kw in essentials:
        current_keywords.add(kw)
        
    data["keywords"] = list(sorted(current_keywords))
    
    # Update Technical Skills as well
    current_skills = set(data.get("technical_skills", []))
    current_skills.add("ARAMCO Standards (SAEP-331)")
    current_skills.add("Schedule Quality Compliance")
    data["technical_skills"] = list(sorted(current_skills))
    
    with open(PROFILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    print("Profile updated successfully with ARAMCO/SAEP-331 standards.")

if __name__ == "__main__":
    update_profile()
