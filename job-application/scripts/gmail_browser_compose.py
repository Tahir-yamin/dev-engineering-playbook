"""
Gmail Browser Composer - No Password Needed!
=============================================
Opens Gmail in browser and auto-fills the compose window.
You just review and click Send.

Usage:
    python gmail_browser_compose.py --company "AECOM" --role "Project Controls Manager" --to "hr@aecom.com"
"""

import json
import os
import time
import webbrowser
from urllib.parse import quote
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE_PATH = os.path.join(BASE_DIR, "data", "master_profile.json")
GENERATED_DIR = os.path.join(BASE_DIR, "generated")


class GmailBrowserComposer:
    """Compose emails directly in Gmail browser - no password needed!"""
    
    def __init__(self):
        with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
            self.profile = json.load(f)
    
    def find_cv(self, company: str) -> str:
        """Find latest CV for company."""
        files = os.listdir(GENERATED_DIR)
        company_clean = company.replace(" ", "_")
        cv_files = [f for f in files if f.startswith("CV_") and company_clean in f and f.endswith(".docx")]
        if cv_files:
            cv_files.sort(reverse=True)
            return os.path.join(GENERATED_DIR, cv_files[0])
        return None
    
    def find_cover_letter(self, company: str, role: str) -> str:
        """Find latest cover letter."""
        files = os.listdir(GENERATED_DIR)
        company_clean = company.replace(" ", "_")
        cl_files = [f for f in files if f.startswith("CoverLetter_") and company_clean in f]
        if cl_files:
            cl_files.sort(reverse=True)
            return os.path.join(GENERATED_DIR, cl_files[0])
        return None
    
    def create_email_content(self, company: str, role: str) -> tuple:
        """Generate email subject and body."""
        p = self.profile["personal"]
        name = p["name"]
        
        subject = f"Application for {role} - {name}, PMP"
        
        body = f"""Dear Hiring Manager,

I am writing to express my interest in the {role} position at {company}.

With 15+ years of experience in project controls, planning, and schedule risk management across EPC, Oil & Gas, and offshore projects valued up to USD 750M, I am confident I can contribute to your team's success.

Key Qualifications:
• Expert in Primavera P6 (L1-L4), delay analysis, and EOT/claims support under FIDIC contracts
• Proven leadership managing planning teams and establishing governance frameworks
• Experience working with multinational EPCs and PMCs in UAE and KSA

I have attached my CV and cover letter for your review. I would welcome the opportunity to discuss how my skills can support {company}'s project delivery objectives.

Thank you for considering my application.

Best regards,
{name}, PMP
{p['phone']}
{p['email_primary']}
LinkedIn: {p['linkedin']}"""
        
        return subject, body
    
    def open_gmail_compose(self, to_email: str, company: str, role: str):
        """Open Gmail compose with pre-filled fields using mailto: URL."""
        
        subject, body = self.create_email_content(company, role)
        cv_path = self.find_cv(company)
        cl_path = self.find_cover_letter(company, role)
        
        # Gmail compose URL with pre-filled fields
        gmail_url = (
            f"https://mail.google.com/mail/?view=cm&fs=1"
            f"&to={quote(to_email)}"
            f"&su={quote(subject)}"
            f"&body={quote(body)}"
        )
        
        print(f"\n{'='*60}")
        print("📧 OPENING GMAIL COMPOSE")
        print(f"{'='*60}")
        print(f"\nTo: {to_email}")
        print(f"Subject: {subject}")
        print(f"\n✓ Opening Gmail in browser...")
        
        # Open Gmail
        webbrowser.open(gmail_url)
        
        print(f"\n📎 ATTACH THESE FILES MANUALLY:")
        print(f"   1. CV: {os.path.basename(cv_path) if cv_path else 'NOT FOUND'}")
        print(f"   2. Cover Letter: {os.path.basename(cl_path) if cl_path else 'NOT FOUND'}")
        print(f"\n📁 Files location: {GENERATED_DIR}")
        print(f"\n✓ Review the email and click SEND when ready!")
        print(f"{'='*60}")
        
        return gmail_url


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Open Gmail Compose with pre-filled email")
    parser.add_argument("--company", type=str, required=True, help="Company name")
    parser.add_argument("--role", type=str, required=True, help="Job title")
    parser.add_argument("--to", type=str, required=True, help="Recipient email")
    
    args = parser.parse_args()
    
    composer = GmailBrowserComposer()
    composer.open_gmail_compose(args.to, args.company, args.role)


if __name__ == "__main__":
    main()
