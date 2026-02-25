# 🚀 Production Deployment Guide
**Evolution of Todo - Hackathon Submission**

## 📋 Pre-Deployment Checklist

- [x] OAuth working locally (Google & GitHub)
- [x] Email verification implemented
- [x] Dashboard auto-refresh functional
- [x] README.md updated
- [x] War stories documented
- [ ] Update OAuth redirect URIs for production
- [ ] Deploy backend to Railway
- [ ] Deploy frontend to Vercel
- [ ] Verify production environment variables

## 🎯 Deployment Architecture

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   Vercel        │─────▶│   Railway       │─────▶│   Neon DB       │
│   (Frontend)    │      │   (Backend)     │      │   (PostgreSQL)  │
│   Next.js 14    │      │   FastAPI       │      │   BetterAuth    │
└─────────────────┘      └─────────────────┘      └─────────────────┘
```

## 🔧 Step 1: Backend Deployment (Railway)

### A. Push Code
```bash
git add .
git commit -m "Final production build"
git push origin main
```

### B. Railway Environment Variables
Go to Railway Project → Settings → Variables

**Add/Update These:**
```env
DATABASE_URL=<your-neon-connection-string>
BETTER_AUTH_SECRET=<same-as-local>
GEMINI_API_KEY=<your-gemini-key>
OPENROUTER_API_KEY=<your-openrouter-key>
SITE_URL=<your-vercel-domain>
APP_NAME=Evolution of Todo
```

**CRITICAL:** After deployment, copy your Railway URL:
```
https://your-app.up.railway.app
```

## 🔧 Step 2: Frontend Deployment (Vercel)

### A. Connect Repository
1. Go to Vercel Dashboard
2. Import your Git repository
3. Select `phase2/frontend` as root directory

### B. Vercel Environment Variables
Go to Project Settings → Environment Variables

**Add These (Production):**
```env
NEXT_PUBLIC_API_URL=https://your-app.up.railway.app
NEXT_PUBLIC_APP_URL=https://your-app.vercel.app
BETTER_AUTH_SECRET=<same-as-local>
DATABASE_URL=<your-neon-connection-string>
GOOGLE_CLIENT_ID=<your-google-id>
GOOGLE_CLIENT_SECRET=<your-google-secret>
GITHUB_CLIENT_ID=<your-github-id>
GITHUB_CLIENT_SECRET=<your-github-secret>
RESEND_API_KEY=<your-resend-key>
EMAIL_FROM=noreply@yourdomain.com
```

### C. Build Settings
```
Framework preset: Next.js
Build command: npm run build
Output directory: .next
Install command: npm install
```

## 🔐 Step 3: Update OAuth Redirect URIs

### Google Cloud Console
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your project
3. APIs & Services → Credentials
4. Edit your OAuth 2.0 Client ID
5. Add to **Authorized redirect URIs:**
   ```
   https://your-app.vercel.app/api/auth/callback/google
   ```

### GitHub Developer Settings
1. Go to [GitHub Settings](https://github.com/settings/developers)
2. Select your OAuth App
3. Update **Authorization callback URL:**
   ```
   https://your-app.vercel.app/api/auth/callback/github
   ```

**⚠️ CRITICAL:** If you skip this step, OAuth will fail with `redirect_uri_mismatch` error!

## 🔧 Step 4: Prisma on Vercel

Vercel needs to generate Prisma Client during build.

### A. Update package.json
Ensure your `build` script includes Prisma generation:
```json
{
  "scripts": {
    "build": "prisma generate && next build"
  }
}
```

### B. Verify postinstall
If build fails, add:
```json
{
  "scripts": {
    "postinstall": "prisma generate"
  }
}
```

## ✅ Step 5: Verification Tests

### Test 1: Backend Health
```bash
curl https://your-app.up.railway.app/health
# Expected: {"status": "ok"}
```

### Test 2: Frontend Landing
```
https://your-app.vercel.app
# Expected: Glassmorphic landing page loads
```

### Test 3: Google OAuth
1. Visit `https://your-app.vercel.app/auth`
2. Click "Google" button
3. Select account
4. Should redirect to dashboard

### Test 4: Email Signup
1. Visit `https://your-app.vercel.app/auth`
2. Switch to "Sign Up"
3. Enter test email
4. Check Resend logs for verification email
5. Click verification link
6. Login should work

### Test 5: AI Chat
1. Login to dashboard
2. Use chat: "Add a task to prepare demo"
3. Task should appear instantly in Kanban board

## 🐛 Common Production Issues

### Issue: "500 Error on OAuth Callback"
**Cause:** Stale `.next` cache or missing env vars

**Fix:**
```bash
# In Vercel dashboard
Settings → General → Redeploy → Clear Build Cache
```

### Issue: "redirect_uri_mismatch"
**Cause:** OAuth redirect URIs not updated

**Fix:** Double-check Google/GitHub settings match your Vercel domain **exactly**

### Issue: "Prisma Client Not Found"
**Cause:** Prisma not generating during build

**Fix:** Add `prisma generate` to build script

### Issue: "Database Connection Failed"
**Cause:** DATABASE_URL missing or incorrect

**Fix:** Verify Neon connection string in Vercel env vars

## 📊 Post-Deployment Monitoring

### Vercel Analytics
- Check deployment logs
- Monitor function execution times
- Track build success rate

### Railway Logs
- Monitor FastAPI startup
- Check AI agent responses
- Track database queries

### Neon Dashboard
- Monitor connection pool
- Check query performance
- Review storage usage

## 🎥 Demo Video Checklist

- [ ] Show landing page animation
- [ ] Demonstrate Google OAuth login
- [ ] Use AI chat to create task
- [ ] Show instant Kanban update
- [ ] Highlight email verification (terminal fallback)
- [ ] Show mobile responsiveness
- [ ] Mention OAuth war story

## 🏆 Submission Links

**Live Demo:** `https://your-app.vercel.app`
**Backend API:** `https://your-app.up.railway.app`
**GitHub Repo:** `https://github.com/your-username/your-repo`
**War Stories:** `/docs/lessons-learned-sso-auth.md`

## 🎯 Judge Talking Points

1. **"Event-Driven Architecture"**
   - Global event bus for instant UI sync
   - No polling, no complex state management

2. **"Security First"**
   - 3 auth methods (Google, GitHub, Email)
   - Mandatory email verification
   - Production-ready with Resend

3. **"Battle-Tested"**
   - Survived 12+ hour OAuth debugging
   - Documented in war stories
   - Clean slate protocol for stability

4. **"Spec-Driven Development"**
   - AI-assisted planning
   - Task breakdown methodology
   - Iterative implementation

---

**Status:** Ready for production deployment 🚀
**Total Development Time:** 48 hours (including 12 hours debugging OAuth)
**Key Learning:** Never upgrade core dependencies mid-hackathon!
