import os
import base64
import json
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Scopes match the existing token.json
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']
TOKEN_FILE = r"d:\my-dev-knowledge-base\job-application\data\token.json"

def send_email(to, subject, body):
    if not os.path.exists(TOKEN_FILE):
        print(f"Error: Token file not found at {TOKEN_FILE}")
        return False

    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    service = build('gmail', 'v1', credentials=creds)

    message = MIMEMultipart()
    message['to'] = to
    message['subject'] = subject
    message.attach(MIMEText(body, 'markdown')) # Using markdown format for rich email

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    
    try:
        sent_message = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()
        
        print(f"Success: Email sent to {to} with Message ID: {sent_message['id']}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--to", required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body_file", required=True)
    args = parser.parse_args()

    with open(args.body_file, 'r', encoding='utf-8') as f:
        body_content = f.read()

    send_email(args.to, args.subject, body_content)
