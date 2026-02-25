import json
import os
import random
import string
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "data", "credentials.json")

def generate_complex_password(length=16):
    """Generate a random 16-character complex password."""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

def store_credentials(company, email, password):
    """Store credentials in credentials.json."""
    os.makedirs(os.path.dirname(CREDENTIALS_PATH), exist_ok=True)
    
    data = {}
    if os.path.exists(CREDENTIALS_PATH):
        try:
            with open(CREDENTIALS_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = {}
            
    data[company] = {
        "email": email,
        "password": password,
        "created_at": datetime.now().isoformat()
    }
    
    with open(CREDENTIALS_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    
    return CREDENTIALS_PATH

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        comp = sys.argv[1]
        mail = sys.argv[2] if len(sys.argv) > 2 else "tahiryamin2050@gmail.com"
        pwd = generate_complex_password()
        path = store_credentials(comp, mail, pwd)
        print(f"Credentials stored for {comp}:")
        print(f"  Email: {mail}")
        print(f"  Password: {pwd}")
        print(f"  File: {path}")
