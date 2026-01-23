"""
LinkedIn Post Scraper for Job Openings - Last 7 Days
====================================================
Scrapes LinkedIn posts where people share job openings.
Uses the exact search URLs you provided.

Install:
    pip install selenium webdriver-manager

Usage:
    python linkedin_posts_scraper.py
"""

import json
import os
import time
import re
from datetime import datetime

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    HAS_SELENIUM = True
except ImportError:
    HAS_SELENIUM = False
    print("Install: pip install selenium webdriver-manager")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


class LinkedInPostScraper:
    """Scrapes LinkedIn posts for job openings."""
    
    # Your search URLs
    SEARCH_URLS = [
        "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Project%20control&origin=GLOBAL_SEARCH_HEADER",
        "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=project%20planning&origin=GLOBAL_SEARCH_HEADER",
        "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=planning%20%26%20Scheduling&origin=GLOBAL_SEARCH_HEADER",
        "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Looking%20for%20a%20Planning&origin=GLOBAL_SEARCH_HEADER",
    ]
    
    def __init__(self):
        self.jobs_found = []
        self.output_file = os.path.join(DATA_DIR, "linkedin_posts_jobs.json")
    
    def setup_driver(self):
        """Setup Chrome driver - simple and reliable."""
        options = Options()
        
        # Basic settings only
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        return driver
    
    def extract_job_from_post(self, post_text):
        """Extract job details from post text."""
        
        # Keywords that indicate hiring
        hiring_keywords = [
            'hiring', 'looking for', 'we are hiring', 'urgent requirement',
            'immediate hiring', 'vacancy', 'position available', 'send cv',
            'apply now', 'interested candidates', 'dm me', 'comment interested'
        ]
        
        # Check if post contains hiring keywords
        text_lower = post_text.lower()
        if not any(keyword in text_lower for keyword in hiring_keywords):
            return None
        
        # Target roles
        target_roles = [
            'project control', 'planning manager', 'planning engineer',
            'scheduler', 'project planner', 'senior planning', 'scheduling engineer'
        ]
        
        # Check if post mentions target roles
        if not any(role in text_lower for role in target_roles):
            return None
        
        # Try to extract location (UAE, Qatar, Saudi, etc.)
        locations = ['uae', 'dubai', 'abu dhabi', 'qatar', 'doha', 'saudi', 'riyadh', 'ksa']
        location_found = next((loc for loc in locations if loc in text_lower), "Middle East")
        
        # Try to extract company name (often in "We at [Company]" or "@[Company]")
        company_match = re.search(r'(?:we at|working at|@)\\s*([A-Z][\\w\\s&]+?)(?:\\s+(?:are|is|,))', post_text)
        company = company_match.group(1).strip() if company_match else "Multiple Companies"
        
        # Extract role
        role_match = next((role for role in target_roles if role in text_lower), "Planning Position")
        
        return {
            "company": company,
            "role": role_match.title(),
            "location": location_found.upper(),
            "post_text": post_text[:500],  # First 500 chars
            "scraped_at": datetime.now().isoformat()
        }
    
    def scrape_posts(self, url, driver, max_posts=10):
        """Scrape posts from a LinkedIn search URL."""
        
        print(f"\\nScraping: {url[:80]}...")
        
        try:
            driver.get(url)
            time.sleep(5)  # Wait for page load
            
            # Check if login required
            if "authwall" in driver.current_url or "login" in driver.current_url:
                print("  ! Login required - opening browser for you to login...")
                print("  After login, the script will continue automatically")
                time.sleep(30)  # Give time to login
            
            # Scroll to load more posts
            for i in range(3):  # Scroll 3 times
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Find all post containers
            posts = driver.find_elements(By.CSS_SELECTOR, ".feed-shared-update-v2, .occludable-update")
            
            print(f"  Found {len(posts)} posts")
            
            for idx, post in enumerate(posts[:max_posts]):
                try:
                    # Get post text
                    text_elem = post.find_element(By.CSS_SELECTOR, ".feed-shared-text, .update-components-text")
                    post_text = text_elem.text
                    
                    # Extract job details
                    job = self.extract_job_from_post(post_text)
                    
                    if job:
                        self.jobs_found.append(job)
                        print(f"  + {job['role']} at {job['company']} - {job['location']}")
                
                except Exception as e:
                    continue
        
        except Exception as e:
            print(f"  Error: {e}")
    
    def run(self):
        """Run the scraper on all search URLs."""
        
        if not HAS_SELENIUM:
            print("\\nPlease install: pip install selenium webdriver-manager")
            return []
        
        print("\\n=== LinkedIn Post Scraper - Job Openings ===")
        print(f"Searching {len(self.SEARCH_URLS)} keyword combinations...")
        
        driver = self.setup_driver()
        
        try:
            for url in self.SEARCH_URLS:
                self.scrape_posts(url, driver, max_posts=10)
                time.sleep(3)  # Delay between searches
            
            # Save results
            self._save_results()
            
        finally:
            driver.quit()
        
        return self.jobs_found
    
    def _save_results(self):
        """Save scraped jobs to JSON."""
        
        if not self.jobs_found:
            print("\\n! No job posts found")
            return
        
        # Remove duplicates
        unique_jobs = []
        seen = set()
        for job in self.jobs_found:
            key = f"{job['company']}_{job['role']}"
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(unique_jobs, f, indent=2, ensure_ascii=False)
        
        print(f"\\n=== Results ===")
        print(f"Total job posts found: {len(unique_jobs)}")
        print(f"Saved to: {self.output_file}")
        print(f"\\nReady to generate applications!")


def main():
    scraper = LinkedInPostScraper()
    scraper.run()


if __name__ == "__main__":
    main()
