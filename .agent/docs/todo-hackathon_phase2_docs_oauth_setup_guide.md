# OAuth Apps Setup Guide 🔐

Complete guide to setting up Google and GitHub OAuth for your Todo app.

---

## 🎯 Quick Overview

You'll need to create:
1. **Google OAuth App** (5 minutes)
2. **GitHub OAuth App** (3 minutes)
3. **Email Service** (Resend - 2 minutes)

Then add credentials to `.env.local` and I'll handle the rest!

---

## 1️⃣ Google OAuth Setup

### Step A: Go to Google Cloud Console
1. Visit: https://console.cloud.google.com/
2. Sign in with your Google account

### Step B: Create Project (if you don't have one)
1. Click dropdown next to "Google Cloud" logo
2. Click "NEW PROJECT"
3. Name: `Todo App` or anything you like
4. Click "CREATE"

### Step C: Enable OAuth
1. In left sidebar → **APIs & Services** → **OAuth consent screen**
2. Choose **External** (unless you have Google Workspace)
3. Click "CREATE"

### Step D: Fill OAuth Consent Screen
**App information:**
- App name: `AI Todo App`
- User support email: your email
- Developer contact: your email

**Scopes** (click "ADD OR REMOVE SCOPES"):
- Select: `userinfo.email`
- Select: `userinfo.profile`
- Click "UPDATE"

Click "SAVE AND CONTINUE" through remaining steps

### Step E: Create OAuth Credentials
1. Left sidebar → **Credentials**
2. Click "+ CREATE CREDENTIALS" → "OAuth client ID"
3. Application type: **Web application**
4. Name: `Todo App Local`

**Authorized redirect URIs:**
```
http://localhost:3002/api/auth/callback/google
```

5. Click "CREATE"

### Step F: Copy Credentials
You'll see a modal with:
- **Client ID**: `xxxxx.apps.googleusercontent.com`
- **Client Secret**: `GOCSPX-xxxxx`

**Copy both** - we'll add to `.env.local` later!

---

## 2️⃣ GitHub OAuth Setup

### Step A: Go to GitHub Settings
1. Visit: https://github.com/settings/developers
2. Click "OAuth Apps" in left sidebar
3. Click "New OAuth App"

### Step B: Fill Application Details
- **Application name**: `AI Todo App`
- **Homepage URL**: `http://localhost:3002`
- **Authorization callback URL**: `http://localhost:3002/api/auth/callback/github`
- **Application description**: (optional) `AI-powered todo list`

Click "Register application"

### Step C: Generate Client Secret
1. You'll see your **Client ID** immediately
2. Click "Generate a new client secret"
3. Copy the secret **NOW** (you can't see it again!)

**Copy both:**
- **Client ID**: `Iv1.xxxxx`
- **Client Secret**: `xxxxx`

---

## 3️⃣ Email Service Setup (Resend)

### Why Resend?
- Free tier: 3,000 emails/month
- Simple API
- No credit card required
- Perfect for email verification codes

### Step A: Create Resend Account
1. Visit: https://resend.com/signup
2. Sign up (GitHub login works!)

### Step B: Get API Key
1. Go to: https://resend.com/api-keys
2. Click "+ Create API Key"
3. Name: `Todo App`
4. Permissions: **Full Access** (or just "Sending access")
5. Click "Create"

### Step C: Copy API Key
- Format: `re_xxxxx`
- **Copy it!** You can't view it again

### Step D: Verify Domain (Optional for production)
For localhost testing, you can use **any email** as sender.
For production, verify your domain at https://resend.com/domains

---

## 4️⃣ Add All Credentials to `.env.local`

Open `d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\phase2\frontend\.env.local`

Add these lines:

```bash
# Existing variables
DATABASE_URL="your existing value"
BETTER_AUTH_SECRET="your existing value"
NEXT_PUBLIC_APP_URL=http://localhost:3002
NEXT_PUBLIC_API_URL=http://localhost:8002

# ===== NEW: Google OAuth =====
GOOGLE_CLIENT_ID=xxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxx

# ===== NEW: GitHub OAuth =====
GITHUB_CLIENT_ID=Iv1.xxxxx
GITHUB_CLIENT_SECRET=xxxxx

# ===== NEW: Email Service (Resend) =====
RESEND_API_KEY=re_xxxxx
EMAIL_FROM=noreply@localhost  # For testing; use real domain in production
```

**Important:** Replace `xxxxx` with your actual credentials!

---

## 5️⃣ Restart Frontend Dev Server

After adding env variables:
```bash
# Stop the frontend (Ctrl+C)
# Start again
npm run dev
```

Environment variables are only loaded on startup!

---

## ✅ Verification Checklist

Before I implement the code:
- [ ] Google OAuth app created
- [ ] GitHub OAuth app created  
- [ ] Resend account created
- [ ] All credentials added to `.env.local`
- [ ] Frontend restarted

---

## 🚀 What Happens Next

Once you confirm credentials are set, I'll:
1. ✅ Fix light mode styling (sidebar, cards, text)
2. ✅ Add BetterAuth OAuth configuration
3. ✅ Update auth page with SSO buttons
4. ✅ Add email verification flow
5. ✅ Create verification code page
6. ✅ Configure email sending with Resend

Then you'll be able to:
- Sign in with Google (one click!)
- Sign in with GitHub (one click!)
- Sign up with email → receive verification code → verify
- All users stored in database with correct provider info

---

## 📝 Production Deployment Notes

When you deploy to Vercel:
1. Update OAuth callback URLs:
   - Google: `https://yourdomain.com/api/auth/callback/google`
   - GitHub: `https://yourdomain.com/api/auth/callback/github`
2. Add all env variables to Vercel dashboard
3. Verify your domain in Resend for production emails

---

## ❓ Common Issues

**"Client ID not found"**
→ Make sure you added credentials to `.env.local` (not `.env`)

**"Redirect URI mismatch"**
→ Callback URL must match exactly: `http://localhost:3002/api/auth/callback/google`

**"Cannot send email"**
→ Check RESEND_API_KEY is correct and starts with `re_`

---

Ready to implement! Let me know when you've added the credentials to `.env.local` and I'll start coding! 🚀
