---
description: Fix Antigravity Browser Agent unavailable errors and Chrome DevTools Protocol issues
---

# Antigravity Browser Agent Issues

## When to Use
- Browser Agent shows "Unavailable" or "Unable to Open"
- Chrome DevTools Protocol port 9222 conflicts
- `wsarecv: connection aborted` errors
- Authentication failures with Antigravity IDE
- Language Server connection issues

---

## Step 1: Kill Zombie Chrome Processes

**Symptom**: `Chrome with CDP is already running on port 9222`

### Find and Kill Process

// turbo
```powershell
# Find process using port 9222
netstat -ano | findstr :9222

# Replace <PID> with the number from above command
# taskkill /PID <PID> /F

# Alternative: Kill all Chrome debugging processes
Get-Process chrome -ErrorAction SilentlyContinue | Where-Object {
  $_.Path -like "*Chrome*"
} | Stop-Process -Force

Write-Host "✅ Cleared port 9222" -ForegroundColor Green
```

### Task Manager Method (Manual)
1. Press `Ctrl + Shift + Esc`
2. Go to **Details** tab
3. Find all `chrome.exe` processes → **End Task**
4. Also terminate `WebView` or `antigravity` processes

---

## Step 2: Verify Google Cloud CLI Installation

**Symptom**: `CommandNotFoundException: gcloud` or `You are not logged into Antigravity`

### Check Current Status

// turbo
```powershell
# Test if gcloud is available
if (Get-Command gcloud -ErrorAction SilentlyContinue) {
    Write-Host "✅ gcloud is installed" -ForegroundColor Green
    gcloud --version
} else {
    Write-Host "❌ gcloud CLI not found - installation required" -ForegroundColor Red
}
```

### Install Google Cloud CLI (If Missing)

**PowerShell as Administrator**:
```powershell
# Download and run installer
(New-Object Net.WebClient).DownloadFile(
  "https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe",
  "$env:Temp\GoogleCloudSDKInstaller.exe"
)
& $env:Temp\GoogleCloudSDKInstaller.exe
```

> [!IMPORTANT]
> During installation, **MUST check**: "Add Google Cloud CLI executables to my PATH"

### Manual PATH Configuration (If Installer Failed)

1. **Find gcloud directory** (check one of these):
   - `C:\Program Files\Google\Cloud SDK\google-cloud-sdk\bin`
   - `C:\Users\<USERNAME>\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin`

2. **Add to System PATH**:
   - Press `Windows Key` → type `env`
   - **Edit the system environment variables**
   - Click **Environment Variables**
   - Under **System variables**, select `Path` → **Edit**
   - Click **New** → Paste the `\bin` path
   - Click **OK** on all dialogs

3. **CRITICAL**: **Restart computer** for PATH changes to take effect

---

## Step 3: Authenticate with Google Cloud

**After gcloud is installed**:

```powershell
# Authenticate (opens browser)
gcloud auth login --update-adc

# Verify authentication
gcloud auth list
```

Follow the browser login flow that opens.

---

## Step 4: Configure Windows Firewall

**Symptom**: `wsarecv: An established connection was aborted by the software in your host machine`

### Add Firewall Exclusions

1. Open **Windows Security**
2. **Virus & threat protection** → **Manage settings**
3. **Exclusions** → **Add or remove exclusions**
4. Click **Add an exclusion** → **Folder**
5. Add these folders:
   ```
   C:\Users\<USERNAME>\.gemini
   C:\Users\<USERNAME>\.antigravity
   C:\Program Files\Google\Cloud SDK
   ```

### Create Firewall Rules (If Issues Persist)

**PowerShell as Administrator**:
```powershell
# Allow Chrome DevTools Protocol ports
New-NetFirewallRule -DisplayName "Antigravity Language Server" `
  -Direction Inbound -Protocol TCP -LocalPort 9222,9223 -Action Allow

New-NetFirewallRule -DisplayName "Antigravity Language Server" `
  -Direction Outbound -Protocol TCP -LocalPort 9222,9223 -Action Allow

Write-Host "✅ Firewall rules created" -ForegroundColor Green
```

---

## Step 5: Clean Browser Profile (Nuclear Option)

**Use only if all above steps failed**

> [!CAUTION]
> This deletes all Antigravity managed Chrome browsing data (not your main Chrome).

```powershell
# Close Antigravity IDE FIRST
Remove-Item -Recurse -Force "$env:USERPROFILE\.gemini\antigravity-browser-profile" -ErrorAction SilentlyContinue

Write-Host "✅ Browser profile cleared - will be recreated on next launch" -ForegroundColor Yellow
```

---

## Step 6: Install Antigravity Browser Extension

**After browser launches**:

1. Watch for popup: **"Install Extension"** → Click **Install**
2. **OR** click **Chrome icon** in IDE's top-right corner to trigger prompt
3. Verify in managed Chrome window:
   - Navigate to `chrome://extensions`
   - Confirm **"Antigravity Browser Control"** is enabled

---

## Step 7: Verify Fix

### Expected Success Indicators

// turbo
```powershell
# Test gcloud
Write-Host "`n🔍 Testing gcloud..." -ForegroundColor Cyan
gcloud --version

# Check port 9222 (should return nothing if IDE is closed)
Write-Host "`n🔍 Checking port 9222..." -ForegroundColor Cyan
$portCheck = netstat -ano | findstr :9222
if ($portCheck) {
    Write-Host "⚠️  Port 9222 is in use - close Antigravity IDE first" -ForegroundColor Yellow
} else {
    Write-Host "✅ Port 9222 is free" -ForegroundColor Green
}

# Check authentication
Write-Host "`n🔍 Checking authentication..." -ForegroundColor Cyan
$authStatus = gcloud auth list --filter=status:ACTIVE --format="value(account)"
if ($authStatus) {
    Write-Host "✅ Authenticated as: $authStatus" -ForegroundColor Green
} else {
    Write-Host "❌ Not authenticated - run: gcloud auth login --update-adc" -ForegroundColor Red
}
```

### Test Browser Agent

In Antigravity IDE chat:
```
Test google.com
```

**Expected**: Agent navigates to Google in the managed Chrome window.

---

## Step 8: WSL2 / Docker Container Users (Advanced)

> [!WARNING]
> Antigravity in WSL2/Docker has network isolation issues with Chrome.

### Solutions

**Option A: Port Forwarding (WSL2)**
```bash
# Inside WSL2
export DISPLAY=:0

# Forward Chrome DevTools Protocol port
netsh.exe interface portproxy add v4tov4 listenport=9222 listenaddress=0.0.0.0 connectport=9222 connectaddress=127.0.0.1
```

**Option B: Install Natively (Recommended)**
- Install Antigravity IDE directly on Windows/Mac host OS
- Avoid running inside containers

---

## Common Error Codes Reference

| Error | Meaning | Fix Step |
|-------|---------|----------|
| `Chrome with CDP is already running` | Port 9222 occupied | Step 1 |
| `CommandNotFoundException: gcloud` | gcloud not in PATH | Step 2 |
| `You are not logged into Antigravity` | Auth expired | Step 3 |
| `wsarecv` | Firewall blocking | Step 4 |
| `Browser startup timed out` | Zombie process or firewall | Steps 1 + 4 |

---

## Prevention: Startup Script

Create `antigravity-startup.ps1` to run before launching IDE:

```powershell
# Kill potential zombie processes
Get-Process chrome -ErrorAction SilentlyContinue | Where-Object {
  $_.CommandLine -like "*remote-debugging-port=9222*"
} | Stop-Process -Force

# Verify gcloud
if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) {
  Write-Error "gcloud CLI not found in PATH!"
  exit 1
}

# Check authentication
$authStatus = gcloud auth list --filter=status:ACTIVE --format="value(account)"
if (-not $authStatus) {
  Write-Host "Refreshing authentication..." -ForegroundColor Yellow
  gcloud auth login --update-adc
}

Write-Host "✅ Ready to launch Antigravity IDE" -ForegroundColor Green
```

---

**Related Documentation**:
- Full troubleshooting guide: `ANTIGRAVITY_BROWSER_AGENT_TROUBLESHOOTING.md`
- [Official Antigravity Docs](https://antigravity.google.com/docs/browser)
- [Google Cloud CLI Installation](https://cloud.google.com/sdk/docs/install)

---

**Status**: ✅ Tested and verified (January 2026)
