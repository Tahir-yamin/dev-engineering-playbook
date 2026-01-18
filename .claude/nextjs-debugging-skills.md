# Next.js Debugging Skills

**Purpose**: Troubleshoot common Next.js development issues  
**Topics**: Environment variables, caching, CORS, build errors  
**Version**: 1.0

---

## Skill #1: Debugging Environment Variable Issues

### When to Use
- Environment variables not updating
- API calls going to wrong URLs
- CORS errors after changing ports
- Switching between environments (Dev/K8s/Prod)

### The Problem

Next.js caches environment variables in multiple places:
1. `.next/` build folder
2. Browser localStorage (for some libraries like BetterAuth)
3. Node.js process memory

Simply updating `.env.local` doesn't always trigger a refresh.

### The Solution

**Step 1: Understand the precedence**

```bash
# Next.js reads in this order:
1. .env.$(NODE_ENV).local  (highest priority)
2. .env.local
3. .env.$(NODE_ENV)
4. .env                     (lowest priority - often the culprit!)
```

**Step 2: Clear all caches**

```powershell
# Stop dev server (Ctrl+C)

# Delete build cache
Remove-Item -Recurse -Force .next

# Delete package cache
Remove-Item -Recurse -Force node_modules\.cache

# Restart
npm run dev
```

**Step 3: Verify environment**

```typescript
// Add temporary debug log
console.log('🔍 ENV CHECK:', {
  APP_URL: process.env.NEXT_PUBLIC_APP_URL,
  API_URL: process.env.NEXT_PUBLIC_API_URL,
  NODE_ENV: process.env.NODE_ENV
});
```

**Step 4: Clear browser cache**

```
DevTools (F12) → Application → Clear site data → Refresh
```

### Key Insights

- ✅ Always check `.env` file, not just `.env.local`
- ✅ Delete `.next/` folder when changing env vars
- ✅ Use `NEXT_PUBLIC_*` prefix for client-side vars
- ❌ Don't rely on hot reload for env changes
- 💡 Test in incognito to rule out browser cache

### Related Skills
- Skill #2: Fixing Port Conflicts
- Workflow: `/fixing-nextjs-cors-port-conflicts`

---

## Skill #2: Fixing Port Conflicts

### When to Use
- `ERR_CONNECTION_REFUSED` errors
- Old servers still running after port changes
- Multiple processes competing for same port
- Zombie processes from crashed dev servers

### The Problem

When switching ports (e.g., Kubernetes NodePorts → local dev), old processes may still be listening on previous ports, causing conflicts.

### The Solution

**Step 1: Find the process**

```powershell
# Windows
netstat -ano | findstr :3000

# Output example:
# TCP    0.0.0.0:3000    0.0.0.0:0    LISTENING    12345
#                                                   ↑ PID
```

**Step 2: Kill the process**

```powershell
# Windows
taskkill /F /PID 12345

# Or kill all Node processes (nuclear option)
taskkill /F /IM node.exe
```

**Step 3: Verify port is free**

```powershell
netstat -ano | findstr :3000
# Should return nothing
```

**Step 4: Start fresh**

```powershell
npm run dev
```

### Automation Script

Create `KILL-PORT.ps1`:

```powershell
param([int]$Port = 3000)

Write-Host "🔍 Searching for process on port $Port..." -ForegroundColor Yellow

$process = netstat -ano | findstr ":$Port"

if ($process) {
    $pid = ($process -split '\s+')[-1]
    Write-Host "Found PID: $pid" -ForegroundColor Red
    
    taskkill /F /PID $pid
    Write-Host "✅ Killed process on port $Port" -ForegroundColor Green
} else {
    Write-Host "✅ No process found on port $Port" -ForegroundColor Green
}
```

Usage:
```powershell
.\KILL-PORT.ps1 -Port 3002
```

### Key Insights

- ✅ Always check for zombie processes when changing ports
- ✅ Use automation scripts for common tasks
- ❌ Don't assume Ctrl+C killed the server
- 💡 Keep a port-killing script handy

---

## Skill #3: Debugging CORS Errors

### When to Use
- `Access-Control-Allow-Origin` errors
- Preflight OPTIONS requests failing
- Auth/API calls blocked by browser
- Works in Postman but not browser

### The Problem

CORS errors have multiple causes:
1. Missing CORS headers on server
2. Wrong origin/port in request
3. Credentials flag mismatch
4. Custom headers not allowed

### Diagnostic Process

**Step 1: Check Network tab**

```
DevTools → Network → Filter: XHR/Fetch
```

Look for:
- Request URL (correct port?)
- Request Method (OPTIONS = preflight)
- Response headers (CORS headers present?)

**Step 2: Verify server CORS config**

```python
# FastAPI
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3002"],  # Specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Step 3: Check client-side config**

```typescript
// Ensure credentials flag matches server
fetch('/api/endpoint', {
  credentials: 'include',  // Must match server allow_credentials
  headers: {
    'Content-Type': 'application/json'
  }
});
```

**Step 4: Test with wildcard**

Temporarily use `allow_origins=["*"]` to confirm CORS is the issue (don't use in production with credentials!)

### Common Patterns

| Error | Cause | Fix |
|-------|-------|-----|
| No `Access-Control-Allow-Origin` | Server CORS not enabled | Add CORS middleware |
| `Origin not allowed` | Wrong origin in allow list | Add your frontend URL |
| Preflight fails | Missing OPTIONS handler | Use CORS middleware (auto-handles) |
| Works in Postman, not browser | Browser security, not CORS | Check cookies/credentials |

### Key Insights

- ✅ CORS is a browser security feature, not a server bug
- ✅ Always check the actual request URL in Network tab
- ✅ Preflight (OPTIONS) happens before actual request
- ❌ Don't use `*` with `credentials: true` in production
- 💡 Test in incognito to rule out cached CORS responses

---

## Skill #4: Debugging Build Errors

### When to Use
- `npm run build` fails
- Type errors only appear in production
- Build succeeds but runtime errors occur
- Environment-specific issues

### Common Build Issues

**Issue 1: Type errors**

```bash
# Error: Property 'recurrence' does not exist on type 'TaskFormData'
```

**Fix**: Update TypeScript types

```typescript
// types/index.ts
export interface TaskFormData {
  // ... existing fields
  recurrence?: string;  // Add missing field
}
```

**Issue 2: Import errors**

```bash
# Error: Module not found: Can't resolve '@/components/...'
```

**Fix**: Check `tsconfig.json` paths

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

**Issue 3: Environment variables**

```bash
# Error: process.env.NEXT_PUBLIC_API_URL is undefined
```

**Fix**: Check variable is defined in `.env` or `.env.production`

### Key Insights

- ✅ Run `npm run build` locally before deploying
- ✅ Use TypeScript strict mode to catch errors early
- ❌ Don't ignore type errors in dev mode
- 💡 Check `.next/` build output for clues

---

## Quick Reference

### Environment Variable Debugging

```powershell
# Check current values
Get-Content .env, .env.local | Select-String "NEXT_PUBLIC"

# Clear cache
Remove-Item -Recurse -Force .next

# Restart with clean slate
npm run dev
```

### Port Conflict Resolution

```powershell
# Find process
netstat -ano | findstr :3002

# Kill process
taskkill /F /PID <PID>
```

### CORS Testing

```powershell
# Test backend directly
curl http://localhost:8000/api/health

# Check CORS headers
curl -I -X OPTIONS http://localhost:8000/api/tasks
```

---

## Related Skills

- `.agent/workflows/fixing-nextjs-cors-port-conflicts.md`
- `.claude/environment-skills.md`
- `.claude/typescript-skills.md`

---

**Total Skills**: 4  
**Last Updated**: January 2026  
**Source**: Phase 5 CORS Debugging Session
