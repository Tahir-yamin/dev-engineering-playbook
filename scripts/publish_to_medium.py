import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WHITE_PAPER_PATH = os.path.join(BASE_DIR, "..", "white-papers", "wp1-agent-accountability-crisis.md")

def read_whitepaper():
    """Read and parse the white paper."""
    if not os.path.exists(WHITE_PAPER_PATH):
        print(f"❌ Error: White paper not found at {WHITE_PAPER_PATH}")
        sys.exit(1)
        
    with open(WHITE_PAPER_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    title = "The AI Agent Accountability Crisis"
    body_lines = []
    
    # Skip title metadata
    for i, line in enumerate(lines):
        if i >= 2: 
            body_lines.append(line)
            
    return title, "".join(body_lines)

def setup_driver_attach():
    """Attach to an existing Chrome instance running on port 9222."""
    print("🚀 Connecting to EXISTING Chrome on port 9222...")
    options = Options()
    
    # CRITICAL: This tells Selenium to attach, not launch
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        print("✅ Successfully connected to your Chrome window!")
        return driver
    except Exception as e:
        print("\n❌ FAILED TO CONNECT")
        print("---------------------------------------------------")
        print("Could not find a Chrome instance listening on port 9222.")
        print("DID YOU RUN THIS COMMAND IN YOUR TERMINAL?")
        print(r'"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\Administrator\AppData\Local\Google\Chrome\User Data"')
        print("---------------------------------------------------")
        sys.exit(1)

def main():
    title, body = read_whitepaper()
    
    # Try to clean up body text to prevent issues
    # Remove markdown image links as they won't look right plain text
    # (Optional, but good for Medium editor)
    
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
            title_field = WebDriverWait(driver, 10).until(
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
            
            # Send text
            driver.switch_to.active_element.send_keys(body)
            
            print("\n✅ SUCCESS: Content Drafted!")
            print("💾 Draft saved in your browser.")
            
        except Exception as e:
            print(f"❌ Editor interaction error: {e}")
            
    except Exception as e:
        print(f"❌ Script Error: {e}")
        
    finally:
        # Do NOT quit driver, as it would close the user's browser
        print("👋 Detaching from browser (leaving it open).")

if __name__ == "__main__":
    main()
