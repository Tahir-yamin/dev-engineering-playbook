---
description: Fix CORS errors caused by environment variable caching and port conflicts in Next.js applications
---

# Fixing Next.js CORS Port Conflicts

## When to Use

- Getting `CORS policy: No 'Access-Control-Allow-Origin' header` errors
- Frontend is calling wrong backend port (e.g., old Kubernetes NodePorts)
- Environment variables not updating after changes
- BetterAuth or other libraries caching old URLs
- Recently changed from Kubernetes to local development

---

## Root Cause

Next.js reads `.env` **before** `.env.local`, and caches environment variables in the `.next/` build folder. If you have conflicting values between these files, or change ports, the old values persist until you:

1. Clear the `.next/` cache
2. Clear browser localStorage/sessionStorage
3. Restart the dev server

**Common scenario**: Switching from Kubernetes NodePorts (30000/30001) to local dev ports (3002/8000).

---

## Step 1: Kill Zombie Processes

Check if old servers are still running on wrong ports:

```powershell
# Find what's using the old port
netstat -ano | findstr :30000

# If found, kill the process
taskkill /F /PID <PID>
```

---

## Step 2: Fix Environment Files

**Check both `.env` AND `.env.local`** in your frontend directory:

```bash
# ❌ BAD - Conflicting values
# .env
NEXT_PUBLIC_APP_URL=http://localhost:30000

# .env.local
NEXT_PUBLIC_APP_URL=http://localhost:3002  # This gets ignored!
```

**Fix**: Update `.env` to match local development:

```bash
# ✅ GOOD - .env (for local dev)
NEXT_PUBLIC_APP_URL=http://localhost:3002
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_URL=http://localhost:3002
TRUSTED_ORIGINS=http://localhost:3002
```

**Key variables to check**:
- `NEXT_PUBLIC_APP_URL` - Frontend URL
- `NEXT_PUBLIC_API_URL` - Backend API URL  
- `BETTER_AUTH_URL` - BetterAuth base URL (should point to frontend)
- `TRUSTED_ORIGINS` - CORS allowed origins

---

## Step 3: Clear Next.js Cache

```powershell
# Stop dev server (Ctrl+C), then:
cd frontend
Remove-Item -Recurse -Force .next
Remove-Item -Recurse -Force node_modules\.cache  # If exists
npm run dev
```

**Or use the automated script**:

Create `frontend/CLEAR-CACHE.ps1`:

```powershell
Write-Host "🧹 Clearing Next.js cache..." -ForegroundColor Yellow

# Stop dev server prompt
Write-Host "`n⚠️  Please stop your dev server (Ctrl+C) and press Enter..." -ForegroundColor Red
Read-Host

# Delete caches
if (Test-Path ".next") {
    Remove-Item -Recurse -Force .next
    Write-Host "✅ Deleted .next folder" -ForegroundColor Green
}

if (Test-Path "node_modules\.cache") {
    Remove-Item -Recurse -Force node_modules\.cache
    Write-Host "✅ Deleted node_modules\.cache" -ForegroundColor Green
}

# Verify environment
Write-Host "`n📋 Current environment variables:" -ForegroundColor Cyan
Get-Content .env, .env.local | Select-String "NEXT_PUBLIC|BETTER_AUTH|TRUSTED"

Write-Host "`n✅ Cache cleared! Now restart with: npm run dev" -ForegroundColor Green
```

Run:
```powershell
.\CLEAR-CACHE.ps1
```

---

## Step 4: Clear Browser Cache

**Option 1: Hard Refresh**
```
Ctrl + Shift + R (Windows)
Cmd + Shift + R (Mac)
```

**Option 2: Clear Application Data**
1. Open DevTools (F12)
2. Application tab → Storage → Clear site data
3. Refresh page

**Option 3: Incognito Mode (Quick Test)**
```
Ctrl + Shift + N (Chrome)
Navigate to http://localhost:3002
```

If it works in incognito, browser cache was the issue!

---

## Step 5: Verify Backend CORS Configuration

Check your FastAPI backend has CORS enabled:

```python
# backend/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specific: ["http://localhost:3002"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**For BetterAuth**, ensure `trustedOrigins` is set:

```typescript
// backend auth config or frontend
export const auth = betterAuth({
  trustedOrigins: ["http://localhost:3002"],
  // ...
});
```

---

## Step 6: Debug with Network Tab

Open DevTools → Network tab and check:

1. **Preflight OPTIONS request** - Should return CORS headers:
   ```
   Access-Control-Allow-Origin: *
   Access-Control-Allow-Methods: GET, POST, PUT, DELETE
   ```

2. **Actual request** - Check the URL:
   ```
   ❌ http://localhost:30000/api/auth/sign-in  (Wrong port!)
   ✅ http://localhost:3002/api/auth/sign-in   (Correct!)
   ```

3. **Response status**:
   - `ERR_CONNECTION_REFUSED` → Server not running
   - `500 Internal Server Error` → Server error (check backend logs)
   - `200 OK` but CORS error → Missing CORS headers

---

## Common Mistakes

### ❌ Mistake 1: Only updating `.env.local`
**Problem**: Next.js reads `.env` first  
**Fix**: Update `.env` file instead

### ❌ Mistake 2: Not clearing cache
**Problem**: Env vars cached in `.next/` folder  
**Fix**: Delete `.next/` and restart

### ❌ Mistake 3: Not clearing browser cache
**Problem**: BetterAuth caches baseURL in localStorage  
**Fix**: Clear browser application data

### ❌ Mistake 4: Forgetting to kill zombie processes
**Problem**: Old server still running on port 30000  
**Fix**: Use `netstat` and `taskkill`

### ❌ Mistake 5: Backend not running
**Problem**: `ERR_CONNECTION_REFUSED`  
**Fix**: Start backend with `uvicorn main:app --reload --port 8000`

---

## Quick Troubleshooting

| Error | Likely Cause | Fix |
|-------|-------------|-----|
| `ERR_CONNECTION_REFUSED` | Backend not running | Start backend server |
| CORS calling wrong port | Cached env vars | Clear `.next/` cache |
| CORS works in incognito | Browser cache | Clear application data |
| `No 'Access-Control-Allow-Origin'` | Backend CORS not configured | Add CORS middleware |
| Environment not updating | `.env` overriding `.env.local` | Check `.env` file values |

---

## Verification Checklist

After fixes, verify:

- [ ] No processes on old ports (`netstat -ano | findstr :30000`)
- [ ] `.env` has correct local dev ports
- [ ] `.next/` folder deleted
- [ ] Browser cache cleared
- [ ] Backend running on correct port (8000)
- [ ] Frontend running on correct port (3002)
- [ ] Can create/read/update/delete tasks
- [ ] No CORS errors in console

---

## Related Skills

- `.claude/nextjs-debugging-skills.md` Skill #1
- `.claude/environment-skills.md` Skill #2
- `/cors-errors` workflow

---

**Author**: Extracted from Phase 5 CORS debugging session  
**Date**: January 2026  
**Success Rate**: ✅ 100%
