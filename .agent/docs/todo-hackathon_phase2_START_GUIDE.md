# How to Start the Application

The application consists of two parts: Backend (FastAPI) and Frontend (Next.js).

## Quick Start

### Option 1: Git Bash (Recommended for simplicity)
```bash
sh start.sh
```

### Option 2: PowerShell (Unified Script)
```powershell
.\start.ps1
```

### Option 3: WSL (Windows Subsystem for Linux)
```bash
./start.sh
```

### Option 4: Linux/Ubuntu Terminal

**Step 1: Open Terminal**
- Press `Ctrl + Alt + T` (keyboard shortcut)
- Or search for "Terminal" in your applications menu
- Or right-click on desktop and select "Open in Terminal"

**Step 2: Navigate to Project Directory**
```bash
# If your project is on Windows drive (WSL/Dual Boot)
cd /mnt/d/Hackathon\ phase\ 1\ TODO\ App/todo_hackathon_phase1

# OR if your project is in native Linux location
cd ~/path/to/todo_hackathon_phase1
```

**Step 3: Make script executable (first time only)**
```bash
chmod +x start.sh
```

**Step 4: Run the startup script**
```bash
./start.sh
```

### Option 5: PowerShell (Separate Windows)
Open **two separate PowerShell windows**:

**Window 1 - Backend:**
```powershell
.\start-backend.ps1
```

**Window 2 - Frontend:**
```powershell
.\start-frontend.ps1
```

---

## Manual Start (If scripts don't work)

### Backend
```powershell
cd "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1"
backend\venv\Scripts\python -m backend.main
```

### Frontend
```powershell
cd "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\frontend"
npm run dev -- -p 3002
```

---

## Access the Application

Once both services are running:
- **Frontend:** http://localhost:3002
- **Backend API:** http://localhost:8002
- **API Docs:** http://localhost:8002/docs

---

## Mounting Windows Drives in Linux/WSL

### WSL (Automatic Mounting)

In WSL, Windows drives are **automatically mounted** by default at `/mnt/`:
- C: drive → `/mnt/c/`
- D: drive → `/mnt/d/`
- E: drive → `/mnt/e/`

**Your project location:**
```bash
/mnt/d/Hackathon\ phase\ 1\ TODO\ App/todo_hackathon_phase1
```

### Quick Access Methods

#### 1. Create a Symbolic Link
```bash
# Create a shortcut in your home directory
ln -s "/mnt/d/Hackathon phase 1 TODO App/todo_hackathon_phase1" ~/todo-app

# Now navigate easily:
cd ~/todo-app
./start.sh
```

#### 2. Create a Shell Alias
Add to `~/.bashrc` or `~/.zshrc`:
```bash
alias cdtodo='cd "/mnt/d/Hackathon phase 1 TODO App/todo_hackathon_phase1"'
```

Reload your shell:
```bash
source ~/.bashrc
```

Use it:
```bash
cdtodo
./start.sh
```

### Troubleshooting WSL Mounting

**Check if drives are mounted:**
```bash
ls /mnt/
```

**Manually mount D: drive (if needed):**
```bash
sudo mkdir -p /mnt/d
sudo mount -t drvfs D: /mnt/d
```

**Configure permanent auto-mount:**

Create or edit `/etc/wsl.conf`:
```bash
sudo nano /etc/wsl.conf
```

Add:
```ini
[automount]
enabled = true
root = /mnt/
options = "metadata,umask=22,fmask=11"
mountFsTab = false
```

Restart WSL:
```powershell
# In Windows PowerShell
wsl --shutdown
```

### Dual-Boot Linux (Native Ubuntu)

If using native Ubuntu alongside Windows:

```bash
# Create mount point
sudo mkdir -p /mnt/windows-d

# Find your Windows partition
sudo fdisk -l

# Mount the partition (replace /dev/sdX# with your actual partition)
sudo mount -t ntfs-3g /dev/sda2 /mnt/windows-d

# Navigate to project
cd /mnt/windows-d/Hackathon\ phase\ 1\ TODO\ App/todo_hackathon_phase1
```

**Make it permanent (optional):**

Edit `/etc/fstab`:
```bash
sudo nano /etc/fstab
```

Add line:
```
/dev/sda2  /mnt/windows-d  ntfs-3g  defaults,uid=1000,gid=1000  0  0
```

---

## Stopping the Application

- **For scripts:** Press `Ctrl+C` in the terminal
- **For manual start:** Press `Ctrl+C` in each terminal window
