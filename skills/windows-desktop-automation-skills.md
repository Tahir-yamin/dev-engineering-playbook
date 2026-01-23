# Windows Desktop Automation Skills

> **Purpose**: Automate Windows desktop applications (MS Project, Primavera P6, etc.) using Python-based tools.

## Overview

This skill enables AI-assisted automation of Windows desktop applications through:
- **PyAutoGUI**: Cross-platform GUI automation (mouse, keyboard, screenshots)
- **pywinauto**: Windows-specific application control
- **COM Automation**: Direct application API access (for Office apps)

---

## 🛠️ Installed Tools

| Tool | Purpose | Status |
|------|---------|--------|
| **PyAutoGUI** | Mouse/keyboard control, screenshots | ✅ Installed |
| **pywinauto** | Windows UI automation | ✅ Installed |
| **Pillow** | Image processing for screen capture | ✅ Installed |

---

## 🖱️ PyAutoGUI Usage

### Basic Mouse Control
```python
import pyautogui

# Get screen size
width, height = pyautogui.size()
print(f"Screen: {width}x{height}")

# Move mouse
pyautogui.moveTo(500, 500)  # Absolute position
pyautogui.moveRel(100, 0)   # Relative movement

# Click
pyautogui.click(500, 500)          # Left click
pyautogui.rightClick(500, 500)     # Right click
pyautogui.doubleClick(500, 500)    # Double click

# Drag
pyautogui.drag(100, 0, duration=0.5)  # Drag right
```

### Keyboard Control
```python
import pyautogui

# Type text
pyautogui.typewrite('Hello World', interval=0.05)

# Press keys
pyautogui.press('enter')
pyautogui.press('tab')

# Hotkeys
pyautogui.hotkey('ctrl', 's')       # Save
pyautogui.hotkey('ctrl', 'c')       # Copy
pyautogui.hotkey('alt', 'tab')      # Switch window
pyautogui.hotkey('win', 'd')        # Show desktop
```

### Screenshot and Image Location
```python
import pyautogui

# Take screenshot
screenshot = pyautogui.screenshot()
screenshot.save('screen.png')

# Take region screenshot
region = pyautogui.screenshot(region=(0, 0, 500, 500))

# Find image on screen (useful for buttons)
location = pyautogui.locateOnScreen('button.png')
if location:
    pyautogui.click(pyautogui.center(location))
```

---

## 🪟 pywinauto Usage (Windows-Specific)

### Connect to Application
```python
from pywinauto import Application

# Start new application
app = Application().start("notepad.exe")

# Connect to running application
app = Application().connect(title="Untitled - Notepad")

# Connect by process ID
app = Application().connect(process=12345)
```

### Control Windows
```python
from pywinauto import Application

app = Application().connect(title_re=".*Notepad.*")
window = app.window(title_re=".*Notepad.*")

# Window operations
window.maximize()
window.minimize()
window.restore()
window.set_focus()

# Get window info
print(window.rectangle())
```

### Interact with Controls
```python
from pywinauto import Application

app = Application().connect(title_re=".*Notepad.*")
window = app.window(title_re=".*Notepad.*")

# Type in edit control
window.Edit.type_keys("Hello from pywinauto!")

# Menu access
window.menu_select("File->Save As")

# Button click
# window.Button.click()
```

---

## 📊 MS Project Automation

### Using COM (pywin32)
```python
import win32com.client

# Connect to MS Project
msproject = win32com.client.Dispatch("MSProject.Application")
msproject.Visible = True

# Open project file
msproject.FileOpen("D:\\Projects\\myproject.mpp")

# Access active project
project = msproject.ActiveProject

# List all tasks
for task in project.Tasks:
    if task:
        print(f"{task.ID}: {task.Name}")
        print(f"  Duration: {task.Duration}")
        print(f"  Start: {task.Start}")
        print(f"  Finish: {task.Finish}")
```

### Create New Task
```python
import win32com.client

msproject = win32com.client.Dispatch("MSProject.Application")
project = msproject.ActiveProject

# Add new task
new_task = project.Tasks.Add("New Task from Python")
new_task.Duration = "5d"
new_task.Start = "2026-02-01"

# Save project
msproject.FileSave()
```

### Export to CSV
```python
import win32com.client
import csv

msproject = win32com.client.Dispatch("MSProject.Application")
project = msproject.ActiveProject

with open("project_tasks.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "Name", "Duration", "Start", "Finish"])
    
    for task in project.Tasks:
        if task:
            writer.writerow([
                task.ID,
                task.Name,
                task.Duration,
                task.Start,
                task.Finish
            ])
```

---

## 🔄 Automation Workflow Pattern

### Step-by-Step Automation Script
```python
import pyautogui
import time

def automate_ms_project():
    """Example: Open MS Project and create a new task"""
    
    # Safety pause
    pyautogui.PAUSE = 0.5
    pyautogui.FAILSAFE = True  # Move mouse to corner to abort
    
    # Open Start Menu
    pyautogui.hotkey('win')
    time.sleep(0.5)
    
    # Type application name
    pyautogui.typewrite('Microsoft Project', interval=0.05)
    time.sleep(1)
    
    # Press Enter to launch
    pyautogui.press('enter')
    time.sleep(5)  # Wait for app to load
    
    # Now you can interact with MS Project
    # Use pyautogui.locateOnScreen() to find buttons
    # Use pyautogui.click() to interact
    
    print("MS Project launched!")

if __name__ == "__main__":
    print("Starting in 3 seconds...")
    time.sleep(3)
    automate_ms_project()
```

---

## 🤖 AI-Assisted Workflow

### How I Can Help:
1. **Write automation scripts** - I create the Python code
2. **You run the script** - Execute on your machine
3. **Review results** - Share screenshots or output
4. **Iterate** - I refine the script based on feedback

### Example Request:
> "Write a script to open MS Project, export all tasks to CSV"

I'll provide the complete Python script you can run.

---

## ⚙️ Best Practices

### Safety Features
```python
import pyautogui

# Enable failsafe (move mouse to corner to abort)
pyautogui.FAILSAFE = True

# Add pause between actions
pyautogui.PAUSE = 0.5

# Countdown before starting
for i in range(3, 0, -1):
    print(f"Starting in {i}...")
    time.sleep(1)
```

### Error Handling
```python
import pyautogui

def click_button(image_path, timeout=10):
    """Click button with timeout and retry"""
    import time
    start = time.time()
    
    while time.time() - start < timeout:
        location = pyautogui.locateOnScreen(image_path)
        if location:
            pyautogui.click(pyautogui.center(location))
            return True
        time.sleep(0.5)
    
    raise Exception(f"Button not found: {image_path}")
```

---

## 📋 Quick Commands

```bash
# Test PyAutoGUI
python -c "import pyautogui; print(pyautogui.size())"

# Test pywinauto
python -c "from pywinauto import Application; print('pywinauto ready!')"

# Take screenshot
python -c "import pyautogui; pyautogui.screenshot('test.png'); print('Saved!')"
```

---

## 🔗 Related Resources

- [PyAutoGUI Docs](https://pyautogui.readthedocs.io/)
- [pywinauto Docs](https://pywinauto.readthedocs.io/)
- [MS Project COM Reference](https://docs.microsoft.com/en-us/office/vba/api/project.application)

---

*Last Updated: January 2026*
