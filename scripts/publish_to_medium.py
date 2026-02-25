import os
import time
import sys
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DRAFT_PATH = os.path.join(BASE_DIR, "..", "content", "medium-drafts", "2026-02-02-dark-arts-project-management.md")

def read_draft():
    """Read and parse the draft post."""
    if not os.path.exists(DRAFT_PATH):
        print(f"❌ Error: Draft not found at {DRAFT_PATH}")
        sys.exit(1)
        
    with open(DRAFT_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract Title (First line starting with #)
    title_match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
    title = title_match.group(1) if title_match else "The 3 Dark Arts of Project Management"
    
    # Extract Body (Everything after the first separator --- or just skip the title)
    body = content
    # Remove the title line
    body = re.sub(r'^#\s+.*', '', body, count=1).strip()
    
    # Remove HTML comments at the end
    body = re.sub(r'<!--.*?-->', '', body, flags=re.DOTALL).strip()
    
    return title, body

def setup_driver_attach():
    """Attach to an existing Chrome instance running on port 9222."""
    print("Connecting to EXISTING Chrome on port 9222...")
    options = Options()
    
    # CRITICAL: This tells Selenium to attach, not launch
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        print("Successfully connected to your Chrome window!")
        return driver
    except Exception as e:
        print("\nFAILED TO CONNECT")
        print("---------------------------------------------------")
        print("Could not find a Chrome instance listening on port 9222.")
        print("DID YOU RUN THIS COMMAND IN YOUR TERMINAL?")
        print(r'"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\Administrator\AppData\Local\Google\Chrome\User Data"')
        print("---------------------------------------------------")
        sys.exit(1)

def main():
    title, body = read_draft()
    
    driver = setup_driver_attach()
    
    try:
        # Check if we are already on Medium
        current_url = driver.current_url
        print(f"📍 Current Tab URL: {current_url}")
        
        if "medium.com/new-story" not in current_url:
            print("🌐 Navigating to Medium New Story...")
            driver.get("https://medium.com/new-story")
        else:
            print("✅ Already on Medium New Story page.")
            
        print("⏳ Waiting for editor to be ready...")
        time.sleep(3)
        
        # Try finding title field
        try:
            print("🔍 Looking for editor fields...")
            title_field = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='editorTitle'], h3.graf--title, textarea[placeholder='Title']"))
            )
            
            print("✍️  Typing Title...")
            title_field.clear()
            title_field.send_keys(title)
            
            # Move to body
            print("✍️  Pasting Body...")
            actions = webdriver.ActionChains(driver)
            actions.send_keys(webdriver.Keys.ENTER)
            actions.perform()
            time.sleep(1)
            
            # Send text via active element
            driver.switch_to.active_element.send_keys(body)
            
            print("\nSUCCESS: Content Drafted!")
            print("Draft saved in your browser. Review and hit 'Publish' when ready.")
            
        except Exception as e:
            print(f"❌ Editor interaction error: {e}")
            
    except Exception as e:
        print(f"❌ Script Error: {e}")
        
    finally:
        print("👋 Detaching from browser.")

if __name__ == "__main__":
    main()
