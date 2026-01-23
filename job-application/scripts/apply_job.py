"""
Unified Job Application Script
===============================
One command for all job applications:
- Generates tailored CV
- Generates cover letter
- For EMAIL jobs: Creates Gmail draft
- For WEBSITE jobs: Creates form data HTML with CV/CL attached

Usage:
    # Email application
    python apply_job.py --company "AECOM" --role "Project Controls Manager" --email "hr@aecom.com"
    
    # Website application
    python apply_job.py --company "AECOM" --role "Project Controls Manager" --website
"""

import json
import os
import sys
from datetime import datetime

# Add scripts directory to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))

from cv_generator import CVGenerator
from cover_letter_generator import CoverLetterGenerator
from form_data_generator import FormDataGenerator

GENERATED_DIR = os.path.join(BASE_DIR, "generated")


class UnifiedJobApplication:
    """Unified job application handler."""
    
    def __init__(self):
        self.cv_gen = CVGenerator()
        self.cl_gen = CoverLetterGenerator()
        self.form_gen = FormDataGenerator()
    
    def apply(self, company: str, role: str, email: str = None, website: bool = False, 
              cc_email: str = None, job_description: str = None, apply_url: str = None):
        """
        Apply to a job.
        
        Args:
            company: Company name
            role: Job title
            email: Recruiter email (for email applications)
            website: If True, generate form data for website application
            cc_email: CC email for email applications
            job_description: Optional job description for ATS optimization
            apply_url: Direct link to the job application page
        """
        self.apply_url = apply_url
        
        print(f"\n{'='*60}")
        print(f"🎯 JOB APPLICATION: {role} at {company}")
        print(f"{'='*60}")
        
        # Step 1: Generate CV
        print(f"\n📄 Step 1: Generating tailored CV...")
        cv_path = self.cv_gen.generate_cv(
            job_title=role,
            company=company,
            job_description=job_description
        )
        
        # Step 2: Generate Cover Letter
        print(f"\n✉️ Step 2: Generating cover letter...")
        cl_path = self.cl_gen.generate(
            company=company,
            role=role
        )
        
        # Step 3: Route based on type
        if email:
            print(f"\n📧 Step 3: Creating Gmail draft...")
            self._send_email(company, role, email, cc_email)
        elif website:
            print(f"\n🌐 Step 3: Generating website form data...")
            self._generate_website_data(company, role, cv_path, cl_path, self.apply_url)
        else:
            print(f"\n✅ Step 3: Files ready for manual application")
            print(f"   CV: {cv_path}")
            print(f"   Cover Letter: {cl_path}")
        
        print(f"\n{'='*60}")
        print(f"✅ APPLICATION PACKAGE READY!")
        print(f"{'='*60}")
    
    def _send_email(self, company: str, role: str, email: str, cc_email: str = None):
        """Send email via Gmail OAuth."""
        try:
            from gmail_oauth_sender import GmailOAuthSender
            sender = GmailOAuthSender()
            sender.create_draft(email, company, role, cc_email=cc_email)
        except Exception as e:
            print(f"❌ Email error: {e}")
            print(f"   Run manually: python gmail_oauth_sender.py --company \"{company}\" --role \"{role}\" --to \"{email}\"")
    
    def _generate_website_data(self, company: str, role: str, cv_path: str, cl_path: str, apply_url: str = None):
        """Generate website form data with attached files and apply link."""
        
        data = self.form_gen.generate_form_data(company, role)
        
        # Generate apply button HTML
        apply_btn_html = ""
        if apply_url:
            apply_btn_html = f'''<a href="{apply_url}" target="_blank" class="btn apply-btn">🚀 OPEN JOB & APPLY NOW</a>'''
        
        # Enhanced HTML with file locations
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Website Application - {company}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 20px auto; padding: 20px; background: #f5f5f5; }}
        .header {{ background: linear-gradient(135deg, #1a73e8, #4285f4); color: white; padding: 25px; border-radius: 12px; }}
        .files {{ background: #e8f5e9; padding: 20px; margin: 20px 0; border-radius: 8px; border-left: 4px solid #4caf50; }}
        .files h3 {{ color: #2e7d32; margin-top: 0; }}
        .file-link {{ display: block; padding: 10px; background: white; margin: 10px 0; border-radius: 4px; }}
        .section {{ background: white; padding: 20px; margin: 15px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .section h3 {{ margin-top: 0; color: #1a73e8; border-bottom: 2px solid #1a73e8; padding-bottom: 10px; }}
        .field {{ margin: 10px 0; padding: 12px; background: #f8f9fa; border-radius: 6px; cursor: pointer; transition: all 0.2s; }}
        .field:hover {{ background: #e3f2fd; transform: translateX(5px); }}
        .field label {{ font-weight: bold; color: #666; font-size: 12px; text-transform: uppercase; }}
        .field .value {{ display: block; margin-top: 5px; font-size: 14px; }}
        .copyable {{ background: #fff3e0; padding: 15px; border-radius: 6px; cursor: pointer; margin: 10px 0; border-left: 4px solid #ff9800; }}
        .copyable:hover {{ background: #ffe0b2; }}
        .copied {{ animation: flash 0.5s; }}
        @keyframes flash {{ 0%,100% {{ background: #c8e6c9; }} }}
        .btn {{ background: #1a73e8; color: white; padding: 12px 24px; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; margin: 5px; text-decoration: none; display: inline-block; }}
        .btn:hover {{ background: #1557b0; }}
        .apply-btn {{ background: linear-gradient(135deg, #4caf50, #2e7d32); font-size: 18px; padding: 15px 30px; margin: 15px 0; display: block; text-align: center; }}
        .apply-btn:hover {{ background: linear-gradient(135deg, #66bb6a, #388e3c); }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🌐 Website Application Package</h1>
        <p><strong>Company:</strong> {company} | <strong>Role:</strong> {role}</p>
        <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
    </div>
    
    <div class="files">
        <h3>🚀 APPLY HERE</h3>
        {apply_btn_html if apply_url else '<p style="color:#888;">No direct link - search company careers page</p>'}
        <h3 style="margin-top:20px;">📎 UPLOAD THESE FILES</h3>
        <div class="file-link">
            <strong>CV:</strong><br>
            <code>{cv_path}</code>
        </div>
        <div class="file-link">
            <strong>Cover Letter:</strong><br>
            <code>{cl_path}</code>
        </div>
        <button class="btn" onclick="window.open('file:///{os.path.dirname(cv_path)}')">📁 Open Files Folder</button>
    </div>
    
    <div class="section">
        <h3>👤 Personal Information</h3>
        {"".join(f'<div class="field" onclick="copyField(this)"><label>{k.replace("_", " ").title()}</label><span class="value">{v}</span></div>' for k, v in data["personal"].items() if v)}
    </div>
    
    <div class="section">
        <h3>📅 Availability</h3>
        {"".join(f'<div class="field" onclick="copyField(this)"><label>{k.replace("_", " ").title()}</label><span class="value">{v}</span></div>' for k, v in data["availability"].items())}
    </div>
    
    <div class="section">
        <h3>📝 Professional Summary</h3>
        <p style="color:#666; font-size:12px;">Click to copy - use whichever fits the form</p>
        <div class="copyable" onclick="copyField(this)">
            <strong>Short Version (50 words):</strong><br><br>
            {data["summaries"]["short_50_words"]}
        </div>
        <div class="copyable" onclick="copyField(this)">
            <strong>Headline:</strong><br><br>
            {data["summaries"]["headline"]}
        </div>
    </div>
    
    <div class="section">
        <h3>🛠️ Skills</h3>
        <div class="copyable" onclick="copyField(this)">
            {data["skills"]["comma_separated"]}
        </div>
    </div>
    
    <div class="section">
        <h3>💰 Salary Expectation</h3>
        {"".join(f'<div class="field" onclick="copyField(this)"><label>{k.replace("_", " ").title()}</label><span class="value">{v}</span></div>' for k, v in data["salary"].items())}
    </div>
    
    <div class="section">
        <h3>🏆 Key Achievements</h3>
        {"".join(f'<div class="copyable" onclick="copyField(this)">{i}. {ach}</div>' for i, ach in enumerate(data["achievements"], 1))}
    </div>
    
    <div class="section">
        <h3>✉️ Cover Letter Snippet</h3>
        <div class="copyable" onclick="copyField(this)">
            {data["cover_letter_snippet"]}
        </div>
    </div>
    
    <script>
        function copyField(el) {{
            const text = el.querySelector('.value')?.innerText || el.innerText;
            navigator.clipboard.writeText(text.trim().replace(/^\\d+\\.\\s*/, ''));
            el.classList.add('copied');
            setTimeout(() => el.classList.remove('copied'), 500);
        }}
    </script>
</body>
</html>"""
        
        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"WebsiteApp_{company.replace(' ', '_')}_{timestamp}.html"
        output_path = os.path.join(GENERATED_DIR, filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"\n✓ Website application package saved!")
        print(f"\n📍 HTML File: {output_path}")
        print(f"📍 CV File: {cv_path}")
        print(f"📍 Cover Letter: {cl_path}")
        print(f"\n📋 Open the HTML file in browser - click fields to copy, then paste in website form")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Unified Job Application")
    parser.add_argument("--company", type=str, required=True, help="Company name")
    parser.add_argument("--role", type=str, required=True, help="Job title")
    parser.add_argument("--email", type=str, help="Recruiter email (for email applications)")
    parser.add_argument("--website", action="store_true", help="Website application (generates form data)")
    parser.add_argument("--url", type=str, help="Direct apply URL for the job listing")
    parser.add_argument("--cc", type=str, default="tahiryamin2050@gmail.com", help="CC email")
    parser.add_argument("--jd", type=str, help="Path to job description file for ATS optimization")
    
    args = parser.parse_args()
    
    # Load job description if provided
    job_desc = None
    if args.jd and os.path.exists(args.jd):
        with open(args.jd, 'r', encoding='utf-8') as f:
            job_desc = f.read()
    
    app = UnifiedJobApplication()
    app.apply(
        company=args.company,
        role=args.role,
        email=args.email,
        website=args.website,
        cc_email=args.cc,
        job_description=job_desc,
        apply_url=args.url
    )


if __name__ == "__main__":
    main()
