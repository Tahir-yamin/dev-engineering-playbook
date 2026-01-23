"""
Submission Tracker - Mark applications as submitted
Usage:
    python mark_submitted.py --company "Kent" --method "email"
    python mark_submitted.py --company "Egis" --method "portal" --id "APP12345"
"""

import json
import argparse
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
SUBMISSION_LOG = DATA_DIR / "submission_log.json"

def load_submissions():
    """Load existing submissions"""
    if SUBMISSION_LOG.exists():
        with open(SUBMISSION_LOG, 'r') as f:
            return json.load(f)
    return []

def mark_submitted(company: str, method: str, app_id: str = None, notes: str = None):
    """Mark an application as submitted"""
    
    submissions = load_submissions()
    
    submission = {
        "company": company,
        "submitted_date": datetime.now().isoformat(),
        "method": method,  # email, portal, linkedin
        "application_id": app_id,
        "notes": notes,
        "status": "submitted"
    }
    
    submissions.append(submission)
    
    # Save
    with open(SUBMISSION_LOG, 'w') as f:
        json.dump(submissions, f, indent=2)
    
    print(f"✅ Marked {company} as SUBMITTED")
    print(f"   Method: {method}")
    print(f"   Date: {submission['submitted_date']}")
    if app_id:
        print(f"   Application ID: {app_id}")
    
    # Show summary
    print(f"\n📊 Total Submissions: {len(submissions)}")
    
    return submission

def list_submissions():
    """List all submissions"""
    submissions = load_submissions()
    
    if not submissions:
        print("No submissions recorded yet.")
        return
    
    print(f"\n📋 SUBMISSION HISTORY ({len(submissions)} total)\n")
    print("=" * 80)
    
    for i, sub in enumerate(submissions, 1):
        print(f"\n{i}. {sub['company']}")
        print(f"   Date: {sub['submitted_date'][:10]}")
        print(f"   Method: {sub['method']}")
        if sub.get('application_id'):
            print(f"   App ID: {sub['application_id']}")
        if sub.get('notes'):
            print(f"   Notes: {sub['notes']}")

def get_pending():
    """Show which applications are pending submission"""
    import os
    
    # Get all generated companies
    generated_dir = Path(__file__).parent.parent / "generated"
    cv_files = list(generated_dir.glob("CV_TahirYamin_*.docx"))
    
    all_companies = set()
    for cv in cv_files:
        # Extract company name from filename
        # Format: CV_TahirYamin_CompanyName_Date.docx
        parts = cv.stem.split('_')
        if len(parts) >= 3:
            company = parts[2]
            all_companies.add(company)
    
    # Get submitted companies
    submissions = load_submissions()
    submitted_companies = {s['company'] for s in submissions}
    
    # Find pending
    pending = all_companies - submitted_companies
    
    print(f"\n⏳ PENDING SUBMISSIONS ({len(pending)} remaining)\n")
    print("=" * 80)
    for company in sorted(pending):
        print(f"  • {company}")
    
    print(f"\n✅ Submitted: {len(submitted_companies)}")
    print(f"⏳ Pending: {len(pending)}")
    print(f"📊 Total: {len(all_companies)}")

def main():
    parser = argparse.ArgumentParser(description="Track job application submissions")
    parser.add_argument("--company", type=str, help="Company name")
    parser.add_argument("--method", type=str, choices=['email', 'portal', 'linkedin'], 
                       help="Submission method")
    parser.add_argument("--id", type=str, help="Application ID from company")
    parser.add_argument("--notes", type=str, help="Additional notes")
    parser.add_argument("--list", action="store_true", help="List all submissions")
    parser.add_argument("--pending", action="store_true", help="Show pending applications")
    
    args = parser.parse_args()
    
    if args.list:
        list_submissions()
    elif args.pending:
        get_pending()
    elif args.company and args.method:
        mark_submitted(args.company, args.method, args.id, args.notes)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
