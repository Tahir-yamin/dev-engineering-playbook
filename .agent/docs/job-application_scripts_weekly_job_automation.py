"""
Weekly Job Automation - Gap Dates Only
======================================
Runs weekly to search only gap dates since last search.
Integrates LinkedIn posts + job boards.

Usage:
    python weekly_job_automation.py
"""

import json
import os
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
TRACKER_FILE = os.path.join(DATA_DIR, "search_date_tracker.json")


def load_tracker():
    """Load search date tracker."""
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, 'r') as f:
            return json.load(f)
    return {
        "last_search_date": None,
        "next_search_from": None,
        "search_history": [],
        "settings": {
            "auto_search_gap_days_only": True,
            "include_linkedin_posts": True,
            "max_jobs_per_search": 50
        }
    }


def update_tracker(jobs_found, applications_generated):
    """Update tracker after search."""
    tracker = load_tracker()
    today = datetime.now().strftime("%Y-%m-%d")
    
    tracker["last_search_date"] = today
    tracker["last_search_time"] = datetime.now().strftime("%H:%M:%S")
    tracker["next_search_from"] = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    tracker["search_history"].append({
        "date": today,
        "jobs_found": jobs_found,
        "applications_generated": applications_generated,
        "sources": ["job_boards", "linkedin_posts"]
    })
    
    with open(TRACKER_FILE, 'w') as f:
        json.dump(tracker, f, indent=2)
    
    print(f"\nUpdated tracker: Next search from {tracker['next_search_from']}")


def get_gap_dates():
    """Get date range to search (gap dates only)."""
    tracker = load_tracker()
    
    if not tracker["last_search_date"]:
        # First run - search last 7 days
        from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        print(f"\nFirst run - searching last 7 days")
    else:
        # Search from day after last search
        last_date = datetime.strptime(tracker["last_search_date"], "%Y-%m-%d")
        from_date = (last_date + timedelta(days=1)).strftime("%Y-%m-%d")
        print(f"\nSearching gap dates: {from_date} to today")
    
    to_date = datetime.now().strftime("%Y-%m-%d")
    
    return from_date, to_date


def main():
    """Run weekly automation."""
    
    print("=" * 60)
    print("WEEKLY JOB APPLICATION AUTOMATION")
    print("=" * 60)
    
    # Get gap dates
    from_date, to_date = get_gap_dates()
    
    if from_date == to_date:
        print(f"\nNo gap - already searched today ({to_date})")
        print("Next run will search from tomorrow onwards")
        return
    
    # Run LinkedIn posts search (integrated)
    print(f"\n1. Searching LinkedIn posts ({from_date} to {to_date})...")
    print("   Keywords: Project control, planning, scheduling")
    print("   (Integration point - call LinkedIn scraper here)")
    
    # Run job boards search
    print(f"\n2. Searching job boards ({from_date} to {to_date})...")
    print("   Platforms: Bayt, GulfTalent, NaukriGulf, LinkedIn Jobs")
    print("   (Integration point - call job scraper here)")
    
    # Example: would integrate actual searches here
    jobs_found = 0
    applications_generated = 0
    
    print(f"\n3. Results:")
    print(f"   Jobs found: {jobs_found}")
    print(f"   Applications generated: {applications_generated}")
    
    # Update tracker
    update_tracker(jobs_found, applications_generated)
    
    print(f"\n{'=' * 60}")
    print("AUTOMATION COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
