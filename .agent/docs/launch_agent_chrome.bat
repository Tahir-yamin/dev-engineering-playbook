@echo off
echo Launching Agent Chrome...
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="d:\my-dev-knowledge-base\agent_chrome_profile" --disable-blink-features=AutomationControlled --disable-infobars
pause
