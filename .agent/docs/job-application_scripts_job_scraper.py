"""
Job Scraper - LinkedIn, Indeed, GulfTalent
==========================================
Scrapes job listings from multiple sources.

Usage:
    python job_scraper.py --keywords "Project Controls Manager" --location "UAE"
"""

import json
import os
import re
from datetime import datetime
from urllib.parse import quote_plus
import webbrowser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE_PATH = os.path.join(BASE_DIR, "data", "master_profile.json")
DATA_DIR = os.path.join(BASE_DIR, "data")

# Job board URL templates
JOB_BOARDS = {
    "linkedin": "https://www.linkedin.com/jobs/search/?keywords={keywords}&location={location}&f_TPR=r604800",
    "indeed_uae": "https://ae.indeed.com/jobs?q={keywords}&l={location}",
    "indeed_qatar": "https://qa.indeed.com/jobs?q={keywords}&l={location}",
    "indeed_saudi": "https://sa.indeed.com/jobs?q={keywords}&l={location}",
    "gulfttalent": "https://www.gulftalent.com/jobs/search?q={keywords}&location={location}",
    "bayt": "https://www.bayt.com/en/uae/jobs/{keywords}-jobs/",
    "naukrigulf": "https://www.naukrigulf.com/{keywords}-jobs?location={location}",
    "oil_gas_jobs": "https://www.oilandgasjobsearch.com/jobs/{keywords}",
    "rigzone": "https://www.rigzone.com/jobs/search/{keywords}",
    "google_jobs": "https://www.google.com/search?q={keywords}+jobs+{location}&ibp=htl;jobs"
}

class JobSearcher:
    """Generate job search URLs and manage applications."""
    
    def __init__(self):
        with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
            self.profile = json.load(f)
        
        self.targets = self.profile.get("target_jobs", {})
        self.applications_file = os.path.join(DATA_DIR, "applications_log.json")
        self._load_applications()
    
    def _load_applications(self):
        """Load existing applications log."""
        if os.path.exists(self.applications_file):
            with open(self.applications_file, 'r', encoding='utf-8') as f:
                self.applications = json.load(f)
        else:
            self.applications = {"sent": [], "pending": [], "rejected": [], "interview": []}
    
    def _save_applications(self):
        """Save applications log."""
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(self.applications_file, 'w', encoding='utf-8') as f:
            json.dump(self.applications, f, indent=2)
    
    def generate_search_urls(self, keywords: str = None, location: str = None) -> dict:
        """Generate search URLs for all job boards."""
        
        if not keywords:
            keywords = "Project Controls Manager"
        if not location:
            location = "UAE"
        
        kw_encoded = quote_plus(keywords)
        loc_encoded = quote_plus(location)
        
        urls = {}
        for board, template in JOB_BOARDS.items():
            urls[board] = template.format(keywords=kw_encoded, location=loc_encoded)
        
        return urls
    
    def open_job_searches(self, keywords: str = None, location: str = None, boards: list = None):
        """Open job search URLs in browser."""
        
        urls = self.generate_search_urls(keywords, location)
        
        if boards:
            urls = {k: v for k, v in urls.items() if k in boards}
        
        print(f"\n{'='*60}")
        print(f"OPENING JOB SEARCHES: {keywords} in {location}")
        print(f"{'='*60}\n")
        
        for board, url in urls.items():
            print(f"Opening {board}...")
            webbrowser.open(url)
        
        print(f"\n✓ Opened {len(urls)} job boards")
    
    def log_application(self, company: str, role: str, source: str, 
                       url: str = None, notes: str = None):
        """Log a job application."""
        
        entry = {
            "company": company,
            "role": role,
            "source": source,
            "url": url,
            "notes": notes,
            "date": datetime.now().isoformat(),
            "status": "sent"
        }
        
        # Check for duplicates
        for app in self.applications["sent"]:
            if app["company"] == company and app["role"] == role:
                print(f"⚠ Already applied to {role} at {company}")
                return
        
        self.applications["sent"].append(entry)
        self._save_applications()
        print(f"✓ Logged: {role} at {company}")
    
    def get_stats(self) -> dict:
        """Get application statistics."""
        return {
            "total_sent": len(self.applications["sent"]),
            "pending": len(self.applications["pending"]),
            "interviews": len(self.applications["interview"]),
            "rejected": len(self.applications["rejected"])
        }
    
    def search_all_targets(self):
        """Search for all target job titles in all target locations."""
        
        titles = self.targets.get("titles", ["Project Controls Manager"])
        locations = self.targets.get("locations", ["UAE"])
        
        print(f"\n{'='*60}")
        print("GENERATING ALL JOB SEARCH URLS")
        print(f"{'='*60}\n")
        
        all_urls = []
        
        for title in titles[:3]:  # Top 3 titles
            for loc in locations[:3]:  # Top 3 locations
                urls = self.generate_search_urls(title, loc)
                print(f"\n{title} - {loc}:")
                for board in ["linkedin", "indeed_uae", "gulfttalent"]:
                    if board in urls:
                        print(f"  {board}: {urls[board][:80]}...")
                        all_urls.append({"title": title, "location": loc, "board": board, "url": urls[board]})
        
        # Save URLs
        urls_file = os.path.join(DATA_DIR, "search_urls.json")
        with open(urls_file, 'w', encoding='utf-8') as f:
            json.dump(all_urls, f, indent=2)
        
        print(f"\n✓ Saved {len(all_urls)} search URLs to {urls_file}")
        return all_urls


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Job Scraper")
    parser.add_argument("--keywords", type=str, default="Project Controls Manager")
    parser.add_argument("--location", type=str, default="UAE")
    parser.add_argument("--open", action="store_true", help="Open URLs in browser")
    parser.add_argument("--all", action="store_true", help="Search all targets")
    parser.add_argument("--log", nargs=3, metavar=("COMPANY", "ROLE", "SOURCE"), help="Log application")
    parser.add_argument("--stats", action="store_true", help="Show application stats")
    
    args = parser.parse_args()
    
    searcher = JobSearcher()
    
    if args.stats:
        stats = searcher.get_stats()
        print(f"\n📊 Application Statistics:")
        print(f"   Sent: {stats['total_sent']}")
        print(f"   Interviews: {stats['interviews']}")
        print(f"   Pending: {stats['pending']}")
        print(f"   Rejected: {stats['rejected']}")
    
    elif args.log:
        searcher.log_application(args.log[0], args.log[1], args.log[2])
    
    elif args.all:
        searcher.search_all_targets()
    
    elif args.open:
        searcher.open_job_searches(args.keywords, args.location)
    
    else:
        urls = searcher.generate_search_urls(args.keywords, args.location)
        print(f"\nJob Search URLs for: {args.keywords} in {args.location}")
        print("="*60)
        for board, url in urls.items():
            print(f"{board}: {url}")


if __name__ == "__main__":
    main()
