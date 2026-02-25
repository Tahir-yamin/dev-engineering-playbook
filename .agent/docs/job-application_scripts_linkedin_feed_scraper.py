"""
LinkedIn Job Scraper - FREE (No Paid API)
==========================================
Uses linkedin-jobs-scraper library - completely free.
Requires LinkedIn authentication for best results.

Setup:
    1. pip install linkedin-jobs-scraper
    2. Set LI_AT_COOKIE environment variable (from LinkedIn cookies)
    
Or use anonymous mode (limited):
    python linkedin_feed_scraper.py --keywords "Project Controls" --location "UAE"
"""

import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


def scrape_linkedin_jobs(keywords: str, location: str = "UAE", limit: int = 25):
    """
    Scrape LinkedIn jobs using free library.
    
    Args:
        keywords: Job search keywords
        location: Location to search
        limit: Max jobs
        
    Returns:
        List of job dictionaries
    """
    try:
        from linkedin_jobs_scraper import LinkedinScraper
        from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
        from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
        from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters
    except ImportError:
        print("❌ Install library: pip install linkedin-jobs-scraper")
        return []
    
    jobs = []
    
    def on_data(data: EventData):
        job = {
            "title": data.title,
            "company": data.company,
            "location": data.place,
            "date": data.date,
            "link": data.link,
            "apply_link": data.apply_link,
            "description": data.description[:500] if data.description else "",
            "scraped_at": datetime.now().isoformat()
        }
        jobs.append(job)
        print(f"✓ {data.title} at {data.company} - {data.place}")
    
    def on_error(error):
        print(f"⚠️ Error: {error}")
    
    def on_end():
        print(f"\n✅ Found {len(jobs)} jobs")
    
    print(f"\n🔍 Searching LinkedIn: {keywords} in {location}")
    print(f"   (FREE - no API costs!)\n")
    
    # Initialize scraper
    scraper = LinkedinScraper(
        headless=True,
        max_workers=1,
        slow_mo=2.0
    )
    
    # Register callbacks
    scraper.on(Events.DATA, on_data)
    scraper.on(Events.ERROR, on_error)
    scraper.on(Events.END, on_end)
    
    # Build query
    queries = [
        Query(
            query=keywords,
            options=QueryOptions(
                locations=[location],
                limit=limit,
                filters=QueryFilters(
                    time=TimeFilters.WEEK,
                    relevance=RelevanceFilters.RECENT
                )
            )
        )
    ]
    
    try:
        scraper.run(queries)
    except Exception as e:
        print(f"❌ Scraper error: {e}")
    
    # Save results
    if jobs:
        output_file = os.path.join(DATA_DIR, "linkedin_jobs.json")
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)
        print(f"\n📁 Saved: {output_file}")
    
    return jobs


def alternative_scrape():
    """
    Alternative: Use JobSpy for multi-platform scraping.
    
    Install: pip install python-jobspy
    """
    try:
        from jobspy import scrape_jobs
        
        print("\n🔍 Using JobSpy (multi-platform, FREE)")
        
        jobs = scrape_jobs(
            site_name=["linkedin", "indeed", "glassdoor"],
            search_term="Project Controls Manager",
            location="UAE",
            results_wanted=20,
            hours_old=168,  # Last 7 days
            country_indeed="UAE"
        )
        
        # Convert to dict
        jobs_list = jobs.to_dict('records')
        
        # Save
        output_file = os.path.join(DATA_DIR, "jobspy_results.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(jobs_list, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Found {len(jobs_list)} jobs from multiple platforms")
        print(f"📁 Saved: {output_file}")
        
        return jobs_list
        
    except ImportError:
        print("❌ Install JobSpy: pip install python-jobspy")
        return []
    except Exception as e:
        print(f"❌ JobSpy error: {e}")
        return []


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="LinkedIn Job Scraper (FREE)")
    parser.add_argument("--keywords", type=str, default="Project Controls Manager")
    parser.add_argument("--location", type=str, default="UAE")
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument("--jobspy", action="store_true", help="Use JobSpy multi-platform scraper")
    
    args = parser.parse_args()
    
    if args.jobspy:
        alternative_scrape()
    else:
        scrape_linkedin_jobs(args.keywords, args.location, args.limit)


if __name__ == "__main__":
    main()
