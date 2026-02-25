"""
Email Draft Creator for Job Applications
=========================================
Creates draft emails in Gmail with CV and cover letter attached.
User reviews and sends manually.

Usage:
    python email_sender.py --company "AECOM" --role "Project Controls Manager" --to "hr@aecom.com"
    python email_sender.py --draft  # Create draft only (recommended)
"""

import json
import os
import smtplib
import imaplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE_PATH = os.path.join(BASE_DIR, "data", "master_profile.json")
GENERATED_DIR = os.path.join(BASE_DIR, "generated")
DATA_DIR = os.path.join(BASE_DIR, "data")
CONFIG_FILE = os.path.join(DATA_DIR, "email_config.env")

def load_email_config():
    """Load email config from env file."""
    config = {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "imap_server": "imap.gmail.com",
        "email": "tahiryamin52@gmail.com",
        "app_password": ""
    }
    
    # Try to load from config file
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    if key == "EMAIL_PRIMARY":
                        config["email"] = value
                    elif key == "APP_PASSWORD_PRIMARY":
                        # Remove spaces from app password
                        config["app_password"] = value.replace(" ", "")
    
    return config

EMAIL_CONFIG = load_email_config()


class EmailDraftCreator:
    """Create email drafts with CV and cover letter attachments."""
    
    def __init__(self, password: str = None):
        with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
            self.profile = json.load(f)
        
        self.email = EMAIL_CONFIG["email"]
        # Priority: command line > config file > environment
        self.password = password or EMAIL_CONFIG.get("app_password") or os.environ.get("GMAIL_APP_PASSWORD", "")
        
    def find_cv(self, company: str) -> str:
        """Find latest CV for company."""
        files = os.listdir(GENERATED_DIR)
        company_clean = company.replace(" ", "_")
        
        cv_files = [f for f in files if f.startswith("CV_") and company_clean in f and f.endswith(".docx")]
        
        if cv_files:
            cv_files.sort(reverse=True)  # Latest first
            return os.path.join(GENERATED_DIR, cv_files[0])
        return None
    
    def find_cover_letter(self, company: str, role: str) -> str:
        """Find latest cover letter for company/role."""
        files = os.listdir(GENERATED_DIR)
        company_clean = company.replace(" ", "_")
        role_clean = role.replace(" ", "_")
        
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
LinkedIn: {p['linkedin']}
"""
        
        return subject, body
    
    def create_draft(self, to_email: str, company: str, role: str) -> dict:
        """Create a draft email in Gmail (does NOT send)."""
        
        if not self.password:
            print("❌ Gmail App Password not set!")
            print("   Set via: --password YOUR_APP_PASSWORD")
            print("   Or environment: GMAIL_APP_PASSWORD=xxx")
            return {"success": False, "error": "No password set"}
        
        # Find attachments
        cv_path = self.find_cv(company)
        cl_path = self.find_cover_letter(company, role)
        
        if not cv_path:
            print(f"⚠ No CV found for {company}")
            print(f"  Generate with: python cv_generator.py --company \"{company}\"")
        
        if not cl_path:
            print(f"⚠ No cover letter found for {company}")
            print(f"  Generate with: python cover_letter_generator.py --company \"{company}\" --role \"{role}\"")
        
        # Create message
        subject, body = self.create_email_content(company, role)
        
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach CV
        if cv_path and os.path.exists(cv_path):
            with open(cv_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(cv_path)}"')
                msg.attach(part)
                print(f"✓ Attached: {os.path.basename(cv_path)}")
        
        # Attach cover letter
        if cl_path and os.path.exists(cl_path):
            with open(cl_path, 'rb') as f:
                part = MIMEBase('text', 'plain')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(cl_path)}"')
                msg.attach(part)
                print(f"✓ Attached: {os.path.basename(cl_path)}")
        
        try:
            # Connect to Gmail IMAP and save as draft
            mail = imaplib.IMAP4_SSL(EMAIL_CONFIG["imap_server"])
            mail.login(self.email, self.password)
            mail.select('[Gmail]/Drafts')
            
            # Append to drafts
            mail.append('[Gmail]/Drafts', '', imaplib.Time2Internaldate(time.time()), msg.as_bytes())
            mail.logout()
            
            print(f"\n✓ Draft created successfully!")
            print(f"  To: {to_email}")
            print(f"  Subject: {subject}")
            print(f"\n📧 Check your Gmail Drafts folder to review and send")
            
            # Log this
            self._log_draft(company, role, to_email)
            
            return {"success": True, "to": to_email, "subject": subject}
            
        except Exception as e:
            print(f"❌ Error creating draft: {e}")
            return {"success": False, "error": str(e)}
    
    def _log_draft(self, company: str, role: str, to_email: str):
        """Log draft creation."""
        log_file = os.path.join(DATA_DIR, "drafts_log.json")
        
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append({
            "company": company,
            "role": role, 
            "to": to_email,
            "created": datetime.now().isoformat(),
            "status": "draft"
        })
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
    
    def preview_email(self, company: str, role: str, to_email: str):
        """Preview email without creating draft."""
        
        subject, body = self.create_email_content(company, role)
        cv_path = self.find_cv(company)
        cl_path = self.find_cover_letter(company, role)
        
        print(f"\n{'='*60}")
        print("EMAIL PREVIEW")
        print(f"{'='*60}")
        print(f"\nTo: {to_email}")
        print(f"From: {self.email}")
        print(f"Subject: {subject}")
        print(f"\n{'-'*60}")
        print(body)
        print(f"{'-'*60}")
        print(f"\nAttachments:")
        print(f"  CV: {os.path.basename(cv_path) if cv_path else 'NOT FOUND'}")
        print(f"  Cover Letter: {os.path.basename(cl_path) if cl_path else 'NOT FOUND'}")
        print(f"{'='*60}")
    
    def save_email_preview(self, company: str, role: str, to_email: str) -> str:
        """Save email as HTML file for easy copy-paste to Gmail."""
        
        subject, body = self.create_email_content(company, role)
        cv_path = self.find_cv(company)
        cl_path = self.find_cover_letter(company, role)
        
        # Create HTML preview
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Email to {company}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 20px auto; padding: 20px; }}
        .header {{ background: #1a73e8; color: white; padding: 20px; border-radius: 8px; }}
        .field {{ margin: 10px 0; padding: 10px; background: #f5f5f5; border-radius: 4px; }}
        .body {{ white-space: pre-wrap; background: white; padding: 20px; border: 1px solid #ddd; margin: 20px 0; }}
        .attachments {{ background: #e8f5e9; padding: 15px; border-radius: 4px; }}
        .btn {{ background: #1a73e8; color: white; padding: 12px 24px; border: none; border-radius: 4px; 
                cursor: pointer; font-size: 16px; margin: 10px 5px; }}
        .btn:hover {{ background: #1557b0; }}
        a {{ color: #1a73e8; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📧 Job Application Email</h1>
        <p>Ready to send to {company}</p>
    </div>
    
    <div class="field"><strong>To:</strong> {to_email}</div>
    <div class="field"><strong>Subject:</strong> {subject}</div>
    
    <h3>Email Body (Copy this):</h3>
    <div class="body" id="emailBody">{body}</div>
    
    <div class="attachments">
        <h3>📎 Attachments to add:</h3>
        <p>1. CV: <a href="file:///{cv_path}">{os.path.basename(cv_path) if cv_path else 'NOT FOUND'}</a></p>
        <p>2. Cover Letter: <a href="file:///{cl_path}">{os.path.basename(cl_path) if cl_path else 'NOT FOUND'}</a></p>
        <p><strong>Files location:</strong> {GENERATED_DIR}</p>
    </div>
    
    <h3>Quick Actions:</h3>
    <button class="btn" onclick="copyBody()">📋 Copy Email Body</button>
    <a href="https://mail.google.com/mail/u/0/#inbox?compose=new" target="_blank">
        <button class="btn">📧 Open Gmail Compose</button>
    </a>
    
    <script>
        function copyBody() {{
            const body = document.getElementById('emailBody').innerText;
            navigator.clipboard.writeText(body);
            alert('Email body copied! Now paste in Gmail.');
        }}
    </script>
    
    <hr>
    <p><em>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}</em></p>
</body>
</html>"""
        
        # Save HTML
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Email_{company.replace(' ', '_')}_{timestamp}.html"
        output_path = os.path.join(GENERATED_DIR, filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"\n✓ Email preview saved: {output_path}")
        print(f"\n📧 Open this file in browser, then:")
        print(f"   1. Click 'Copy Email Body'")
        print(f"   2. Click 'Open Gmail Compose'")
        print(f"   3. Paste body and attach files from: {GENERATED_DIR}")
        
        return output_path


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Create Email Drafts for Job Applications")
    parser.add_argument("--company", type=str, required=True, help="Company name")
    parser.add_argument("--role", type=str, required=True, help="Job title")
    parser.add_argument("--to", type=str, required=True, help="Recipient email")
    parser.add_argument("--password", type=str, help="Gmail App Password")
    parser.add_argument("--preview", action="store_true", help="Preview without creating draft")
    parser.add_argument("--save", action="store_true", help="Save as HTML for manual Gmail compose")
    
    args = parser.parse_args()
    
    creator = EmailDraftCreator(password=args.password)
    
    if args.preview:
        creator.preview_email(args.company, args.role, args.to)
    elif args.save:
        path = creator.save_email_preview(args.company, args.role, args.to)
        # Open in browser
        import webbrowser
        webbrowser.open(f"file:///{path}")
    else:
        creator.create_draft(args.to, args.company, args.role)


if __name__ == "__main__":
    main()
