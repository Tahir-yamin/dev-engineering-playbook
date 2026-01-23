"""
LinkedIn Job Posts Scraper
Extracts job opportunities from LinkedIn search URLs
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from pathlib import Path
import re

# LinkedIn search URLs (last 7 days)
LINKEDIN_SEARCHES = [
    "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Hiring%20Project%20Planning%20Engineer",
    "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Looking%20for%20a%20Planning",
    "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Hiring%20for%20planning",
    "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=planning%20%26%20Scheduling",
    "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Project%20control",
    "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=project%20planning",
    "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=project%20controls%20engineer",
    "https://www.linkedin.com/search/results/content/?keywords=project%20controls%20engineer"
]

def extract_job_from_post(post_text):
    """
    Extract job information from LinkedIn post text
    
    Args:
        post_text: Text content of LinkedIn post
    
    Returns:
        dict: Job information or None
    """
    # Common patterns for job posts
    hiring_keywords = [
        "hiring", "looking for", "we're hiring", "join our team",
        "opportunity", "position available", "now hiring", "urgently hiring"
    ]
    
    # Check if it's a job post
    text_lower = post_text.lower()
    if not any(keyword in text_lower for keyword in hiring_keywords):
        return None
    
    # Extract company name (look for patterns)
    company = None
    company_patterns = [
        r"at\s+([A-Z][A-Za-z\s&]+)",
        r"([A-Z][A-Za-z\s&]+)\s+is\s+hiring",
        r"Join\s+([A-Z][A-Za-z\s&]+)",
    ]
    
    for pattern in company_patterns:
        match = re.search(pattern, post_text)
        if match:
            company = match.group(1).strip()
            break
    
    # Extract role
    role = None
    role_patterns = [
        r"(Project\s+Controls?\s+(?:Manager|Engineer|Specialist))",
        r"(Planning\s+(?:Manager|Engineer|Specialist))",
        r"(Project\s+Planning\s+(?:Manager|Engineer))",
        r"(Scheduling\s+(?:Manager|Engineer))",
    ]
    
    for pattern in role_patterns:
        match = re.search(pattern, post_text, re.IGNORECASE)
        if match:
            role = match.group(1)
            break
    
    # Extract location
    location = None
    location_patterns = [
        r"in\s+(Dubai|UAE|Saudi\s+Arabia|Riyadh|Jeddah|Abu\s+Dhabi)",
        r"(Dubai|UAE|Saudi\s+Arabia|Riyadh|Jeddah|Abu\s+Dhabi)"
    ]
    
    for pattern in location_patterns:
        match = re.search(pattern, post_text, re.IGNORECASE)
        if match:
            location = match.group(1)
            break
    
    if role or company:
        return {
            "title": role or "Project Controls / Planning Role",
            "company": company or "See LinkedIn Post",
            "location": location or "UAE/Saudi",
            "source": "LinkedIn Post",
            "url": "https://linkedin.com/feed",  # Will be updated with actual post URL
            "snippet": post_text[:200] + "..."
        }
    
    return None

def scrape_linkedin_search(url, session=None):
    """
    Scrape a LinkedIn search URL for job posts
    
    Note: This is a basic scraper. LinkedIn requires authentication
    for full access. This will extract what's publicly visible.
    
    Args:
        url: LinkedIn search URL
        session: Optional requests session
    
    Returns:
        list: Job posts found
    """
    if session is None:
        session = requests.Session()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = session.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Note: LinkedIn requires login for most content
            # This is a placeholder - actual scraping would need
            # proper authentication
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract visible text
            text = soup.get_text()
            
            # Look for job-related content
            jobs = []
            
            # This is simplified - real implementation would need
            # proper LinkedIn session and parsing
            print(f"   ⚠️  LinkedIn requires authentication for full access")
            print(f"   💡 Recommendation: Use Gemini AI or manual search")
            
            return jobs
            
        else:
            print(f"   ❌ Failed to access: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return []

def search_all_linkedin_sources():
    """
    Search all LinkedIn URLs and aggregate results
    
    Returns:
        list: All jobs found
    """
    print("\n📱 LinkedIn Job Posts Search")
    print("=" * 60)
    print(f"Searching {len(LINKEDIN_SEARCHES)} keyword combinations...")
    print("=" * 60)
    
    all_jobs = []
    session = requests.Session()
    
    for idx, url in enumerate(LINKEDIN_SEARCHES, 1):
        # Extract keyword from URL
        keyword = url.split("keywords=")[1].split("&")[0].replace("%20", " ").replace("%22", "").replace("%26", "&")
        
        print(f"\n{idx}. Searching: {keyword}")
        
        jobs = scrape_linkedin_search(url, session)
        
        if jobs:
            print(f"   ✅ Found {len(jobs)} posts")
            all_jobs.extend(jobs)
        else:
            print(f"   ℹ️  No direct results (requires LinkedIn login)")
    
    return all_jobs

def save_linkedin_urls_for_manual_search():
    """
    Save LinkedIn search URLs for manual browsing
    
    Returns:
        str: Path to saved file
    """
    output_file = Path("job-application/data/linkedin_search_urls.md")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# LinkedIn Job Search URLs\n\n")
        f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("**Instructions**: Click each link and browse manually for job posts\n\n")
        f.write("---\n\n")
        
        for idx, url in enumerate(LINKEDIN_SEARCHES, 1):
            keyword = url.split("keywords=")[1].split("&")[0].replace("%20", " ").replace("%22", "").replace("%26", "&")
            
            f.write(f"## {idx}. {keyword}\n\n")
            f.write(f"**Link**: [{keyword}]({url})\n\n")
            f.write("**What to look for**:\n")
            f.write("- Posts with 'hiring', 'looking for', 'join our team'\n")
            f.write("- Company names and direct application links\n")
            f.write("- Save any promising URLs\n\n")
            f.write("---\n\n")
    
    return str(output_file)

def main():
    """
    Main execution - save LinkedIn URLs for manual search
    """
    print("\n🔗 LinkedIn Integration - URL Export")
    print("=" * 60)
    
    # Save URLs for manual browsing
    file_path = save_linkedin_urls_for_manual_search()
    
    print(f"\n✅ LinkedIn search URLs saved to:")
    print(f"   {file_path}")
    print("\n💡 Recommendation:")
    print("   1. Open the file above")
    print("   2. Click each LinkedIn link")
    print("   3. Browse posts manually (requires LinkedIn account)")
    print("   4. Save any job URLs you find")
    print("\n   OR use Gemini AI search for automated results!")
    print("=" * 60)

if __name__ == "__main__":
    main()
