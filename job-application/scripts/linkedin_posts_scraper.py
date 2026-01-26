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
    
    # Your search URLs - Updated 2026-01-24
    SEARCH_URLS = [
        # Past 24 hours searches
        "https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=Hiring%20Project%20Planning%20Engineer&origin=FACETED_SEARCH&sid=Z0d&sortBy=%22date_posted%22",
        "https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=Looking%20for%20a%20Planning&origin=FACETED_SEARCH&sid=A%2Cm&sortBy=%22date_posted%22",
        "https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=Hiring%20for%20planning&origin=GLOBAL_SEARCH_HEADER&sid=wIm",
        "https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=planning%20%26%20Scheduling&origin=FACETED_SEARCH&sid=GH-&sortBy=%22date_posted%22",
        "https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=Project%20control&origin=FACETED_SEARCH&sid=dz1&sortBy=%22date_posted%22",
        "https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=project%20planning&origin=FACETED_SEARCH&sid=mR%40",
        "https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=project%20controls%20engineer&origin=FACETED_SEARCH&sid=%3Aqr&sortBy=%22date_posted%22",
        # Past month search for broader coverage
        "https://www.linkedin.com/search/results/content/?datePosted=%22past-month%22&keywords=planning%20%26%20Scheduling&origin=FACETED_SEARCH&sid=JvO&sortBy=%22date_posted%22",
    ]
    
    def __init__(self):
        self.jobs_found = []
        self.output_file = os.path.join(DATA_DIR, "linkedin_posts_jobs.json")
    
    def setup_driver(self):
        """Setup Chrome driver using dedicated scraper profile to persist login."""
        print("  Initializing Chrome driver...")
        options = Options()
        
        # Use dedicated scraper profile (persists login, no conflicts with open browser)
        scraper_profile_dir = os.path.join(BASE_DIR, "chrome_scraper_profile")
        scraper_profile_dir = os.path.abspath(scraper_profile_dir)
        os.makedirs(scraper_profile_dir, exist_ok=True)
        
        print(f"  Using profile: {scraper_profile_dir}")
        options.add_argument(f"--user-data-dir={scraper_profile_dir}")
        
        # Minimal settings for stability
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            print("  ✓ Chrome driver initialized successfully")
            return driver
        except Exception as e:
            print(f"  Error initializing Chrome: {e}")
            print("  Trying without profile...")
            # Fallback: try without profile
            options_simple = Options()
            options_simple.add_argument('--disable-blink-features=AutomationControlled')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options_simple)
            return driver
    
    def extract_job_from_post(self, post_text, post_url=None):
        """Extract job details from post text."""
        
        # Keywords that indicate hiring (expanded list)
        hiring_keywords = [
            'hiring', 'looking for', 'we are hiring', 'urgent requirement',
            'immediate hiring', 'vacancy', 'position available', 'send cv',
            'apply now', 'interested candidates', 'dm me', 'comment interested',
            'join our team', 'job opening', 'career opportunity', 'recruiting',
            'seeking', 'required', 'needed', 'open position', 'apply here',
            'send resume', 'applications invited', 'position open'
        ]
        
        # Check if post contains hiring keywords
        text_lower = post_text.lower()
        has_hiring_keyword = any(keyword in text_lower for keyword in hiring_keywords)
        
        # Target roles (expanded with variations)
        target_roles = [
            'project control', 'planning manager', 'planning engineer',
            'scheduler', 'project planner', 'senior planning', 'scheduling engineer',
            'planning coordination', 'plan engineer', 'schedule manager',
            'project scheduler', 'control engineer', 'planning specialist',
            'scheduling specialist', 'project planning', 'planning & scheduling',
            'planning / scheduling', 'primavera', 'p6 planner'
        ]
        
        # Check if post mentions target roles
        has_target_role = any(role in text_lower for role in target_roles)
        
        # Accept if has EITHER hiring keyword OR target role (more lenient)
        if not (has_hiring_keyword or has_target_role):
            return None
        
        # Try to extract location (expanded globally, not just Middle East)
        locations = [
            'uae', 'dubai', 'abu dhabi', 'qatar', 'doha', 'saudi', 'riyadh', 'ksa',
            'kuwait', 'bahrain', 'oman', 'middle east', 'gcc', 'india', 'pakistan',
            'egypt', 'jordan', 'lebanon', 'uk', 'london', 'europe', 'usa', 'canada',
            'australia', 'asia', 'global', 'remote', 'international', 'netherlands'
        ]
        location_found = next((loc for loc in locations if loc in text_lower), "Global")
        
        # Try to extract company name (often in "We at [Company]" or "@[Company]")
        company_match = re.search(r'(?:we at|working at|@)\\s*([A-Z][\\w\\s&]+?)(?:\\s+(?:are|is|,))', post_text)
        company = company_match.group(1).strip() if company_match else "Multiple Companies"
        
        # Extract role
        role_match = next((role for role in target_roles if role in text_lower), "Planning Position")
        
        return {
            "company": company,
            "role": role_match.title(),
            "location": location_found.upper(),
            "post_url": post_url or "N/A",
            "post_text": post_text[:500],  # First 500 chars
            "scraped_at": datetime.now().isoformat()
        }
    
    def extract_max_posts_from_url(self, url):
        """Extract max posts count from URL parameter, default to 10."""
        # Look for patterns like page=2, start=25, or count=50
        count_match = re.search(r'count=(\d+)', url)
        page_match = re.search(r'page=(\d+)', url)
        
        if count_match:
            return int(count_match.group(1))
        elif page_match:
            return int(page_match.group(1)) * 10
        return 10  # Default
    
    def scrape_posts(self, url, driver):
        """Scrape posts from a LinkedIn search URL."""
        
        # Extract max posts from URL or use default
        max_posts = self.extract_max_posts_from_url(url)
        
        print(f"\\nScraping: {url[:80]}... (max posts: {max_posts})")
        
        try:
            driver.get(url)
            time.sleep(5)  # Wait for page load
            
            # Check if login required (shouldn't be needed with profile)
            if "authwall" in driver.current_url or "login" in driver.current_url:
                print("  ⚠️ Login required - please log in manually...")
                print("  Waiting 60 seconds for you to log in...")
                time.sleep(60)  # Reduced wait time since profile should work
            
            # Infinite scroll until no new posts load (max 500 posts per URL)
            print("  Starting infinite scroll (max 500 posts)...")
            previous_post_count = 0
            no_new_posts_count = 0
            max_no_change_attempts = 3
            max_posts_per_url = 500  # User requested limit
            
            while no_new_posts_count < max_no_change_attempts:
                # Scroll to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)  # Wait for posts to load
                
                # Count current posts
                posts = driver.find_elements(By.CSS_SELECTOR, ".feed-shared-update-v2, .occludable-update")
                current_post_count = len(posts)
                
                # Check if we've hit the limit
                if current_post_count >= max_posts_per_url:
                    print(f"\n  Reached max limit of {max_posts_per_url} posts")
                    break
                
                print(f"  Loaded {current_post_count} posts...", end="\r")
                
                # Check if new posts loaded
                if current_post_count == previous_post_count:
                    no_new_posts_count += 1
                    print(f"  No new posts ({no_new_posts_count}/{max_no_change_attempts})...", end="\r")
                else:
                    no_new_posts_count = 0  # Reset counter
                    previous_post_count = current_post_count
            
            # Final post collection
            posts = driver.find_elements(By.CSS_SELECTOR, ".feed-shared-update-v2, .occludable-update")
            print(f"\n  Finished scrolling. Found {len(posts)} total posts")
            
            # Process all posts (no limit since we already scrolled to get them all)
            print(f"  Processing {len(posts)} posts...")
            for idx, post in enumerate(posts):
                try:
                    # Get post text
                    text_elem = post.find_element(By.CSS_SELECTOR, ".feed-shared-text, .update-components-text")
                    post_text = text_elem.text
                    
                    # Extract post URL
                    post_url = "N/A"
                    try:
                        # Try multiple selectors for post link
                        link_elem = post.find_element(By.CSS_SELECTOR, ".app-aware-link, .feed-shared-actor__container-link, a[href*='/posts/']")
                        post_url = link_elem.get_attribute('href')
                    except:
                        # Fallback: try to find any link in the post
                        try:
                            link_elem = post.find_element(By.CSS_SELECTOR, "a[href*='linkedin.com']")
                            post_url = link_elem.get_attribute('href')
                        except:
                            pass
                    
                    # Extract job details
                    job = self.extract_job_from_post(post_text, post_url)
                    
                    if job:
                        self.jobs_found.append(job)
                        print(f"  + {job['role']} at {job['company']} - {job['location']}")
                        print(f"    Link: {post_url[:60]}...")
                
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
                self.scrape_posts(url, driver)
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
