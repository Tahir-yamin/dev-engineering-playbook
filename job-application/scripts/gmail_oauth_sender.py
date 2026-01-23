"""
Gmail OAuth Email Sender - No Password Needed!
===============================================
Uses Google OAuth2 for authentication.
First run: Opens browser for one-time Google login
After that: Drafts are sent directly to Gmail - no password, no browser!

Setup:
1. Go to: https://console.cloud.google.com/
2. Create a project
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download credentials.json to this folder

Usage:
    python gmail_oauth_sender.py --company "AECOM" --role "Project Controls Manager" --to "hr@aecom.com"
"""

import json
import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

# Google API imports
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False
    print("⚠ Google API not installed. Run: pip install google-auth google-auth-oauthlib google-api-python-client")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE_PATH = os.path.join(BASE_DIR, "data", "master_profile.json")
GENERATED_DIR = os.path.join(BASE_DIR, "generated")
DATA_DIR = os.path.join(BASE_DIR, "data")

# OAuth files
CREDENTIALS_FILE = os.path.join(DATA_DIR, "credentials.json")
TOKEN_FILE = os.path.join(DATA_DIR, "token.json")

# Gmail API scope for creating drafts
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']


class GmailOAuthSender:
    """Send emails via Gmail using OAuth - no password needed!"""
    
    def __init__(self):
        with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
            self.profile = json.load(f)
        
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Gmail using OAuth2."""
        if not GOOGLE_API_AVAILABLE:
            return
        
        creds = None
        
        # Load existing token
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(CREDENTIALS_FILE):
                    print(f"\n❌ Missing credentials.json!")
                    print(f"\nTo set up Gmail OAuth:")
                    print(f"1. Go to: https://console.cloud.google.com/")
                    print(f"2. Create a new project")
                    print(f"3. Enable Gmail API")
                    print(f"4. Create OAuth 2.0 credentials (Desktop app)")
                    print(f"5. Download credentials.json to: {CREDENTIALS_FILE}")
                    return
                
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save token for future runs
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
            print("✓ OAuth token saved - future runs won't need browser auth!")
        
        self.service = build('gmail', 'v1', credentials=creds)
    
    def find_cv(self, company: str) -> str:
        files = os.listdir(GENERATED_DIR)
        company_clean = company.replace(" ", "_")
        cv_files = [f for f in files if f.startswith("CV_") and company_clean in f and f.endswith(".docx")]
        if cv_files:
            cv_files.sort(reverse=True)
            return os.path.join(GENERATED_DIR, cv_files[0])
        return None
    
    def find_cover_letter(self, company: str, role: str) -> str:
        files = os.listdir(GENERATED_DIR)
        company_clean = company.replace(" ", "_")
        cl_files = [f for f in files if f.startswith("CoverLetter_") and company_clean in f]
        if cl_files:
            cl_files.sort(reverse=True)
            return os.path.join(GENERATED_DIR, cl_files[0])
        return None
    
    def create_email_content(self, company: str, role: str) -> tuple:
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
    
    def create_draft(self, to_email: str, company: str, role: str, cc_email: str = None) -> dict:
        """Create a draft in Gmail using OAuth - appears in your Drafts folder!"""
        
        if not self.service:
            print("❌ Gmail API not available. See setup instructions above.")
            return {"success": False}
        
        subject, body = self.create_email_content(company, role)
        cv_path = self.find_cv(company)
        cl_path = self.find_cover_letter(company, role)
        
        # Create message
        msg = MIMEMultipart()
        msg['To'] = to_email
        if cc_email:
            msg['Cc'] = cc_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach CV
        if cv_path and os.path.exists(cv_path):
            with open(cv_path, 'rb') as f:
                part = MIMEBase('application', 'vnd.openxmlformats-officedocument.wordprocessingml.document')
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
            # Create draft via Gmail API
            raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode('utf-8')
            draft = self.service.users().drafts().create(
                userId='me',
                body={'message': {'raw': raw_message}}
            ).execute()
            
            print(f"\n✅ DRAFT CREATED IN GMAIL!")
            print(f"   To: {to_email}")
            print(f"   Subject: {subject}")
            print(f"\n📧 Check your Gmail Drafts folder to review and send!")
            
            # Log
            self._log_draft(company, role, to_email, draft.get('id'))
            
            return {"success": True, "draft_id": draft.get('id')}
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return {"success": False, "error": str(e)}
    
    def _log_draft(self, company: str, role: str, to_email: str, draft_id: str):
        log_file = os.path.join(DATA_DIR, "drafts_log.json")
        logs = []
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
        logs.append({
            "company": company,
            "role": role,
            "to": to_email,
            "draft_id": draft_id,
            "created": datetime.now().isoformat(),
            "status": "draft"
        })
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Create Gmail Draft via OAuth")
    parser.add_argument("--company", type=str, required=True, help="Company name")
    parser.add_argument("--role", type=str, required=True, help="Job title")
    parser.add_argument("--to", type=str, required=True, help="Recipient email")
    parser.add_argument("--cc", type=str, help="CC email (optional)")
    
    args = parser.parse_args()
    
    sender = GmailOAuthSender()
    sender.create_draft(args.to, args.company, args.role, cc_email=args.cc)


if __name__ == "__main__":
    main()
