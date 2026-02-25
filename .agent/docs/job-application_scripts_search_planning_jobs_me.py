import requests
from pathlib import Path
from datetime import datetime
import re

# Targeted Search URLs for "Planning Engineer" in "Middle East"
# Combining keywords and locations for better precision
LINKEDIN_SEARCHES = [
    # General Middle East
    "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Hiring%20Planning%20Engineer%20Middle%20East",
    "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Project%20Controls%20Middle%20East",
    # Specific High-Value Countries
    "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Hiring%20Planning%20Engineer%20Saudi%20Arabia",
    "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Hiring%20Planning%20Engineer%20UAE",
    "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Hiring%20Planning%20Engineer%20Qatar",
    "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Hiring%20Planning%20Engineer%20Dubai",
     "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Hiring%20Planning%20Engineer%20Riyadh"
]

def save_me_planning_search():
    """
    Save LinkedIn search URLs for Middle East Planning roles.
    """
    # Use existing data directory
    output_path = Path("job-application/data/linkedin_ME_planning_search.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# LinkedIn Middle East Planning Job Search\n\n")
        f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Target**: Planning Engineer / Project Controls\n")
        f.write(f"**Region**: Middle East (KSA, UAE, Qatar)\n\n")
        
        f.write("## 🚀 One-Click Search Links\n")
        f.write("Click these links to open LinkedIn search results directly:\n\n")
        
        for url in LINKEDIN_SEARCHES:
            # Extract readable keyword
            # keywords=Hiring%20Planning%20Engineer%20Middle%20East
            match = re.search(r"keywords=([^&]+)", url)
            if match:
                raw_keyword = match.group(1)
                readable = raw_keyword.replace("%20", " ").replace("%22", "")
            else:
                readable = "Search Query"
            
            f.write(f"- [Search: {readable}]({url})\n")
    
    return str(output_path)

if __name__ == "__main__":
    file_path = save_me_planning_search()
    print(f"Generated search file: {file_path}")
