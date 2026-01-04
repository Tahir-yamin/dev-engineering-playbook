---
description: Fix login issues, CSRF errors, session problems, and OAuth redirect failures
---

# Authentication Issues Workflow

## When to Use
- Login not working
- "CSRF token mismatch"
- "Session not found"
- OAuth redirect fails
- Users getting logged out

---

## Step 1: Check Environment Variables

// turbo
```bash
# Run validation
.\scripts\validate-env.ps1
```

Required variables:
- `BETTER_AUTH_SECRET` - Must be 32+ characters
- `BETTER_AUTH_URL` - Must match access URL exactly
- `TRUSTED_ORIGINS` - Must include frontend URL
- `DATABASE_URL` - Must have SSL params

---

## Step 2: Verify Configuration

### BETTER_AUTH_SECRET

```bash
# Check length (Mac/Linux)
echo $BETTER_AUTH_SECRET | wc -c  # Should be 32+

# Generate new if needed (Mac/Linux)
openssl rand -base64 32

# Windows PowerShell
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Minimum 0 -Maximum 256 }))
```

### BETTER_AUTH_URL

```bash
# Must match EXACTLY what browser shows
# ✅ Correct: http://localhost:3000
# ❌ Wrong: http://localhost:3000/
# ❌ Wrong: https://localhost:3000 (if accessing via http)
```

### TRUSTED_ORIGINS

```bash
# Must include all client URLs
TRUSTED_ ORIGINS=http://localhost:3000

# For production, add your domain
TRUSTED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

---

## Step 3: Specific Error Fixes

### "CSRF token mismatch"

```bash
# Step 1: Verify BETTER_AUTH_URL matches your access URL
BETTER_AUTH_URL=http://localhost:3000

# Step 2: Check TRUSTED_ORIGINS includes frontend
TRUSTED_ORIGINS=http://localhost:3000

# Step 3: Restart services
cd phase4/docker
docker-compose restart frontend
```

**Reference**: @.claude/auth-skills.md Skill #1

### "Session not found"

```bash
# Check database connection
psql "$DATABASE_URL"

# Verify session table exists
npx prisma studio
# Look for session table

# Check cookie settings in browser DevTools
# Application → Cookies → Look for better-auth.session_token
```

**Reference**: @.claude/auth-skills.md Skill #3

### OAuth redirect fails

```bash
# Step 1: Check callback URL in provider (GitHub/Google)
# Should be: http://localhost:3000/api/auth/callback/github

# Step 2: Verify client ID and secret
echo $GITHUB_CLIENT_ID
echo $GITHUB_CLIENT_SECRET

# Step 3: Check for typos in environment variables
```

**Reference**: @.claude/auth-skills.md Skill #2

---

## Step 4: Test Authentication

- Clear browser cache and cookies
- Try logging in again
- Check browser console for errors
- Check Network tab for failed requests

---

## Step 5: Deep Dive

If still not working:
```
@.claude/auth-skills.md
Use Skill #1 for complete setup guide
```

---

**Related Skills**: auth-skills.md #1-3, env-skills.md #1
