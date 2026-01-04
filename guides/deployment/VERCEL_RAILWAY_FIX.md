# Vercel & Railway Deployment Fix Guide - Phase 3

**Issue**: Vercel deployment failing after Phase 4 merge  
**Root Cause**: Vercel trying to build from root but Phase 3 frontend is in `phase2/frontend/`  
**Solution**: Update Vercel project settings to point to correct directory

---

## 🔧 Fix Vercel Deployment

### Step 1: Update Vercel Project Settings

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project: `frontend`
3. Click **Settings** → **General**

### Step 2: Configure Build & Development Settings

**Root Directory**:
```
phase2/frontend
```

**Build Command**:
```bash
npm run build
```

**Output Directory**:
```
.next
```

**Install Command**:
```bash
npm install
```

**Framework Preset**: Next.js

### Step 3: Set Environment Variables

Go to **Settings** → **Environment Variables** and add:

#### Required Variables:

| Variable | Value | Environment |
|----------|-------|-------------|
| `DATABASE_URL` | Your NeonDB connection string | Production |
| `BETTER_AUTH_SECRET` | Your  auth secret (32+ chars) | Production |
| `BETTER_AUTH_URL` | `https://your-vercel-app.vercel.app` | Production |
| `NEXT_PUBLIC_API_URL` | `https://your-railway-backend.up.railway.app` | Production, Preview |
| `NEXT_PUBLIC_APP_URL` | `https://your-vercel-app.vercel.app` | Production, Preview |
| `TRUSTED_ORIGINS` | `https://your-vercel-app.vercel.app,https://your-railway-backend.up.railway.app` | Production |

#### Optional (AI Features):
| Variable | Value | Environment |
|----------|-------|-------------|
| `OPENROUTER_API_KEY` | Your OpenRouter key | Production |
| `GEMINI_API_KEY` | Your Gemini key | Production |

#### OAuth (if using):
| Variable | Value | Environment |
|----------|-------|-------------|
| `GITHUB_CLIENT_ID` | Your GitHub OAuth Client ID | Production |
| `GITHUB_CLIENT_SECRET` | Your GitHub OAuth Secret | Production |
| `GOOGLE_CLIENT_ID` | Your Google OAuth Client ID | Production |
| `GOOGLE_CLIENT_SECRET` | Your Google OAuth Secret | Production |

### Step 4: Trigger Redeployment

**Option A: Via Dashboard**
1. Go to **Deployments** tab
2. Click on the latest failed deployment
3. Click **"Redeploy"**

**Option B: Via Git**
```bash
git commit --allow-empty -m "trigger: Force Vercel redeploy"
git push origin main
```

---

## 🚂 Fix Railway Deployment (Backend)

### Step 1: Check Railway Project

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Find your backend project: `todo-hackathon-phase2`

### Step 2: Update Start Command

**Root Directory**: `/phase2/backend`

**Build Command**:
```bash
pip install -r requirements.txt
```

**Start Command**:
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Step 3: Set Environment Variables

| Variable | Value |
|----------|-------|
| `DATABASE_URL` | Your NeonDB connection string |
| `OPENROUTER_API_KEY` | Your OpenRouter key |
| `GEMINI_API_KEY` | Your Gemini key |
| `BETTER_AUTH_SECRET` | Same as frontend |
| `CORS_ORIGINS` | `https://your-vercel-app.vercel.app` |
| `PORT` | `8000` (Railway sets this automatically) |

### Step 4: Trigger Redeployment

**Option A: Via Dashboard**
1. Click **"Deploy"** → **"Redeploy"**

**Option B: Via Git**
```bash
git push origin main
```

---

## ✅ Verification Checklist

After deployment, verify:

### Frontend (Vercel):
- [ ] Can access: `https://your-app.vercel.app`
- [ ] Login page loads
- [ ] Can create tasks
- [ ] Can view tasks
- [ ] AI chatbot works
- [ ] OAuth login works (if configured)

### Backend (Railway):
- [ ] Can access: `https://your-backend.up.railway.app/docs`
- [ ] API documentation loads
- [ ] Health check endpoint works: `/health`
- [ ] Database connection works

### Integration:
- [ ] Frontend can call backend API
- [ ] CORS is configured correctly
- [ ] Authentication works end-to-end
- [ ] Tasks sync between frontend and backend

---

## 🐛 Common Issues & Fixes

### Issue 1: "Module not found" Error
**Cause**: Vercel building from wrong directory  
**Fix**: Set Root Directory to `phase2/frontend` in Vercel settings

### Issue 2: "API Connection Failed"
**Cause**: CORS or wrong API URL  
**Fix**: 
1. Check `NEXT_PUBLIC_API_URL` matches your Railway URL
2. Update Railway `CORS_ORIGINS` to include Vercel URL

### Issue 3: "Database Connection Failed"
**Cause**: Missing `sslmode=require` in DATABASE_URL  
**Fix**: Ensure DATABASE_URL includes:
```
?sslmode=require&channel_binding=require
```

### Issue 4: " Authentication Error"
**Cause**: Wrong `BETTER_AUTH_URL` or missing secret  
**Fix**:
1. Set `BETTER_AUTH_URL` to your Vercel URL
2. Ensure `BETTER_AUTH_SECRET` is 32+ characters
3. Update `TRUSTED_ORIGINS` to include your Vercel URL

### Issue 5: "Build Timeout"
**Cause**: Vercel installing from wrong package.json  
**Fix**: Verify Root Directory is set to `phase2/frontend`

---

## 📝 Quick Command Reference

### Force Vercel Redeploy:
```bash
git commit --allow-empty -m "feat: Update deployment config"
git push origin main
```

### Check Vercel Logs:
```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Check logs
vercel logs
```

### Check Railway Logs:
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Check logs
railway logs
```

---

## 🎯 Expected Deployment URLs

**Frontend (Vercel)**:
- Production: `https://frontend-[hash].vercel.app`
- Preview: `https://frontend-[hash]-[branch].vercel.app`

**Backend (Railway)**:
- Production: `https://todo-hackathon-phase2-production.up.railway.app`

**Update these URLs in:**
1. Vercel environment variables (`NEXT_PUBLIC_API_URL`)
2. Railway environment variables (`CORS_ORIGINS`)
3. OAuth redirect URLs (GitHub, Google)

---

## 🔄 Deployment Workflow (Phase 3)

```
1. Push to GitHub (main branch)
   ↓
2. Vercel detects change
   ↓
3. Vercel builds from phase2/frontend
   ↓
4. Deployment succeeds
   ↓
5. Railway detects change
   ↓
6. Railway builds from phase2/backend
   ↓
7. Deployment succeeds
   ↓
8. Update OAuth redirect URLs if needed
```

---## ✨ Post-Deployment Tasks

After successful deployment:

1. **Update OAuth Redirect URLs**:
   - GitHub: https://github.com/settings/developers
   - Google: https://console.cloud.google.com/apis/credentials

2. **Update README.md**:
   ```markdown
   ## Live Demo (Phase 3)
   
   - **Frontend**: https://your-app.vercel.app
   - **Backend API**: https://your-backend.up.railway.app
   - **API Docs**: https://your-backend.up.railway.app/docs
   ```

3. **Test All Features**:
   - User registration
   - Login (email, Google, GitHub)
   - Task CRUD operations
   - AI chatbot
   - Real-time updates

---

## 📞 Support

If issues persist:

1. **Check Vercel Build Logs**:
   - Dashboard → Deployments → Click failed deployment → View Logs

2. **Check Railway Logs**:
   - Dashboard → Your Project → Deployments → View Logs

3. **Common Error Patterns**:
   - `ENOENT`: File not found (wrong directory)
   - `MODULE_NOT_FOUND`: Missing dependency
   - `CORS`: Wrong CORS_ORIGINS setting
   - `ECONNREFUSED`: Backend not accessible

---

**Created**: December 30, 2025  
**Purpose**: Fix Phase 3 Vercel/Railway deployment after Phase 4 merge  
**Priority**: Optional (Phase 4 doesn't require cloud deployment)
