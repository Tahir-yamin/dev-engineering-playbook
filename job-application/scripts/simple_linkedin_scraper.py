"""
Simple LinkedIn Job Scraper - NO DEPENDENCIES
=============================================
Uses BeautifulSoup and Requests only - works immediately.

Install:
    pip install beautifulsoup4 requests lxml

Usage:
    python simple_linkedin_scraper.py "Project Controls Manager" "UAE"
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from urllib.parse import quote_plus

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


def scrape_linkedin_simple(keywords: str, location: str = "UAE", max_results: int = 25):
    """
    Scrape LinkedIn jobs using simple HTTP requests.
    No Selenium, no browser automation - fast and lightweight.
    """
    
    jobs = []
    
    # Build LinkedIn job search URL
    query = quote_plus(keywords)
    loc = quote_plus(location)
    url = f"https://www.linkedin.com/jobs/search?keywords={query}&location={loc}&f_TPR=r604800"  # Last 7 days
    
    print(f"\n🔍 Scraping LinkedIn Jobs...")
    print(f"   Keywords: {keywords}")
    print(f"   Location: {location}")
    print(f"   URL: {url}\n")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Find job cards
        job_cards = soup.find_all('div', class_='base-card')[:max_results]
        
        if not job_cards:
            print("⚠️ No job cards found. LinkedIn may have changed structure.")
            print("   Trying alternative selectors...")
            job_cards = soup.find_all('div', {'data-entity-urn': True})[:max_results]
        
        for card in job_cards:
            try:
                # Extract job details
                title_elem = card.find('h3', class_='base-search-card__title')
                company_elem = card.find('h4', class_='base-search-card__subtitle')
                location_elem = card.find('span', class_='job-search-card__location')
                link_elem = card.find('a', class_='base-card__full-link')
                
                if title_elem and company_elem:
                    job = {
                        "title": title_elem.text.strip(),
                        "company": company_elem.text.strip(),
                        "location": location_elem.text.strip() if location_elem else location,
                        "link": link_elem['href'] if link_elem else "",
                        "scraped_at": datetime.now().isoformat()
                    }
                    jobs.append(job)
                    print(f"✓ {job['title']} at {job['company']}")
            
            except Exception as e:
                continue
        
        print(f"\n✅ Found {len(jobs)} jobs")
        
        # Save to JSON
        if jobs:
            output_file = os.path.join(DATA_DIR, "linkedin_jobs_simple.json")
            os.makedirs(DATA_DIR, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(jobs, f, indent=2, ensure_ascii=False)
            print(f"📁 Saved: {output_file}")
        
        return jobs
        
    except requests.RequestException as e:
        print(f"❌ Request error: {e}")
        return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []


def main():
    import sys
    
    if len(sys.argv) > 1:
        keywords = sys.argv[1]
        location = sys.argv[2] if len(sys.argv) > 2 else "UAE"
    else:
        keywords = "Project Controls Manager"
        location = "UAE"
    
    scrape_linkedin_simple(keywords, location)


if __name__ == "__main__":
    main()
