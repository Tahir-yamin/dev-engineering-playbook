
import json
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Reuse extraction logic
def extract_job_from_post(post_text, post_url="N/A"):
    # Simplified extraction for speed
    text_lower = post_text.lower()
    
    # Keywords
    if "hiring" not in text_lower and "looking for" not in text_lower and "opportunity" not in text_lower:
        # Check for roles if no generic hiring keyword
        if "planning" not in text_lower and "scheduler" not in text_lower and "project control" not in text_lower:
            return None

    return {
        "text": post_text[:200] + "...",
        "full_text": post_text,
        "scraped_at": datetime.now().isoformat()
    }

def main():
    print("=== Active Tab Scraper ===")
    
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        # Connect to existing Chrome
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        print(f"Connected! Current URL: {driver.current_url}")

        # Force navigation if not on search page
        if "search/results" not in driver.current_url:
            print("  Not on search page. Navigating...")
            TARGET_URL = "https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=Hiring%20Planning%20Engineer%20Middle%20East"
            driver.get(TARGET_URL)
            time.sleep(5) # Wait for load

        # Scrape visible posts
        posts = driver.find_elements(By.CSS_SELECTOR, ".feed-shared-update-v2, .occludable-update")
        print(f"Found {len(posts)} posts in active tab.")
        
        jobs = []
        for post in posts:
            try:
                text = post.text
                if len(text) > 50:
                    jobs.append(extract_job_from_post(text))
            except:
                pass
        
        # Save
        if jobs:
            jobs = [j for j in jobs if j is not None]
            output_file = os.path.join("d:\\my-dev-knowledge-base\\job-application\\data", "active_tab_jobs.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(jobs, f, indent=2, ensure_ascii=False)
            print(f"Saved {len(jobs)} jobs to {output_file}")
        else:
            print("No relevant jobs found in current view.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
