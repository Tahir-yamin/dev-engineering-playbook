# Enabling Desktop Automation for MS Project & P6

## Step-by-Step Guide (No Paid APIs Required)

---

## PART 1: Enable Python COM for MS Project

### Step 1.1: Run Command Prompt as Administrator

1. Press **Windows + X**
2. Click **"Windows Terminal (Admin)"** or **"Command Prompt (Admin)"**
3. Click **Yes** when prompted

### Step 1.2: Register MS Project COM

Run these commands one by one:

```cmd
cd "C:\Program Files (x86)\Microsoft Office\root\Office16"

regsvr32 MSPRJ.OLB
```

If that fails, try:

```cmd
"C:\Program Files (x86)\Microsoft Office\root\Office16\WINPROJ.EXE" /regserver
```

### Step 1.3: Enable Macro Settings in MS Project

1. Open **MS Project**
2. Go to **File → Options → Trust Center → Trust Center Settings**
3. Click **Macro Settings**
4. Select **"Enable all macros"**
5. Check **"Trust access to the VBA project object model"**
6. Click **OK** twice

### Step 1.4: Add to Windows Firewall Exception

1. Press **Windows + I** → Settings
2. Go to **Privacy & Security → Windows Security → Firewall**
3. Click **"Allow an app through firewall"**
4. Find **Microsoft Project** and check both boxes

### Step 1.5: Test COM Connection

Open a new PowerShell/CMD window and run:

```cmd
python -c "import win32com.client; msp = win32com.client.Dispatch('MSProject.Application'); msp.Visible = True; print('SUCCESS!')"
```

---

## PART 2: Fix pyautogui Window Focus Issues

### Step 2.1: Install Required Package

```cmd
pip install pygetwindow pywinauto
```

### Step 2.2: Use pywinauto for Focus (More Reliable)

Create this test script:

```python
# test_focus.py
from pywinauto import Application
import pyautogui
import time

# Connect to MS Project
app = Application(backend="uia").connect(title_re=".*Project.*")
window = app.top_window()

# Bring to front and focus
window.set_focus()
time.sleep(1)

# Now pyautogui will work
pyautogui.hotkey('alt', 'f')  # File menu
print("Sent Alt+F to MS Project")
```

### Step 2.3: Run Scripts from Same Session

Important: Run Python and MS Project in the **same user session**:
- Don't use Remote Desktop
- Don't run as different user
- Keep MS Project window not minimized

### Step 2.4: Disable UAC Temporarily (for testing)

1. Press **Windows + R** → type `UserAccountControlSettings`
2. Drag slider to **"Never Notify"**
3. Click **OK** and restart
4. **Re-enable after testing!**

---

## PART 3: Understanding P6 XER Format

### XER File Structure

XER is tab-delimited text with this structure:

```
ERMHDR  [version]  [date]  [type]  [user]  ...
%T  [TABLE_NAME]
%F  [field1]  [field2]  [field3]  ...
%R  [value1]  [value2]  [value3]  ...
%R  [value1]  [value2]  [value3]  ...
%T  [NEXT_TABLE]
...
%E
```

### Required Tables for Valid XER

| Table | Purpose |
|-------|---------|
| ERMHDR | Header row (must be first) |
| CURRTYPE | Currency types |
| PROJECT | Project definitions |
| CALENDAR | Work calendars |
| PROJWBS | WBS structure |
| TASK | Activities |
| TASKPRED | Predecessors |
| %E | End marker (must be last) |

### Study Your Original XER

Run this to see the full structure:

```cmd
python -c "
with open(r'D:\Downloads\SCHEDULES-20260120T115910Z-1-001\SCHEDULES\OIL&GAZ TIME SCHEDULE\badra oil.xer', 'r', errors='ignore') as f:
    for line in f:
        if line.startswith('%T') or line.startswith('%F'):
            print(line.strip()[:100])
"
```

---

## PART 4: Test Everything

### Test 1: MS Project COM

```cmd
python d:\my-dev-knowledge-base\scripts\load_badra_to_msproject.py
```

### Test 2: pyautogui with Focus

```cmd
python d:\my-dev-knowledge-base\scripts\automate_msp_import.py
```

### Test 3: XER Analysis

```cmd
python d:\my-dev-knowledge-base\scripts\analyze_badra.py
```

---

## Quick Checklist

Run these commands and tell me the results:

```cmd
# Check 1: COM registration
python -c "import win32com.client; print('win32com OK')"

# Check 2: MS Project COM
python -c "import win32com.client; msp = win32com.client.Dispatch('MSProject.Application'); print('MSProject COM OK')"

# Check 3: pyautogui
python -c "import pyautogui; print('pyautogui OK')"

# Check 4: pywinauto
pip install pywinauto
python -c "from pywinauto import Application; print('pywinauto OK')"
```

---

**Run the checklist above and share the results - I'll help fix whatever fails!**
