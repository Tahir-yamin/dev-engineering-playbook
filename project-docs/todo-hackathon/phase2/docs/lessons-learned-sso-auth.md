# 🛑 War Stories: Debugging SSO & BetterAuth
**Date:** December 2025  
**Topic:** Resolving Silent 500 Errors in Next.js + BetterAuth  
**Duration:** 12+ hours of debugging

## 📉 The Problem
During Phase 2, we hit a critical blocker: **Silent 500 Internal Server Errors** whenever initializing BetterAuth.

**Symptoms:**
* Browser showed `500 Internal Server Error` on OAuth callback
* **Zero logs** appeared in the Next.js terminal
* Error occurred before request handler could execute
* Database schema appeared correct

**Impact:** 
* OAuth (Google/GitHub) was completely broken
* Email login worked intermittently
* Hackathon progress blocked for 12+ hours

## 🕵️ The Investigation (What We Tried)

### ❌ Attempt 1: The "Raw Pool" Approach
We initially tried connecting BetterAuth to PostgreSQL using a raw `pg` Pool.

**Result:** Failed. BetterAuth's internal schema requirements were too strict for our manual SQL setup.

**Lesson:** Modern auth libraries expect ORMs, not raw SQL.

### ❌ Attempt 2: The "Bleeding Edge" (Prisma v7)
We switched to the Prisma Adapter but installed the latest version (`v7.2.0`).

**Result:** Catastrophic Failure.

**Why:** Prisma v7 deprecated the `url = env(...)` syntax in `schema.prisma`, but the `prisma db push` command *still required it*. We were stuck in a dependency loop where we couldn't push the schema.

**Error Message:**
```
P1012 Schema validation error
Function not available in this datasource: env()
```

**Lesson:** Never upgrade major versions of core infrastructure during a hackathon.

### ❌ Attempt 3: The "Configuration Hell"
We spent 4 hours tweaking `auth.ts`, assuming we had missing Environment Variables. We added `console.log` everywhere, but nothing printed.

**Discovery:** Next.js swallows errors that occur during the *module initialization phase* (before the request handler runs).

**Lesson:** Browser logs lie. The 500 error in the network tab means nothing if server logs are empty.

## ✅ The Solution: The "Clean Slate" Protocol

We finally fixed it by identifying a **Version Mismatch** between the generated Prisma Client and the runtime library, combined with stale Next.js cache.

### Step 1: Downgrade to Stability
We uninstalled all v7 artifacts and pinned **Prisma to v5.21.1**. This is the industry standard for production Next.js apps today.

```bash
npm uninstall prisma @prisma/client
npm install prisma@5.21.1 @prisma/client@5.21.1 --save-exact
```

### Step 2: The Nuclear Option
We realized Next.js was caching the broken v7 client. We executed:

```bash
# Kill all Node processes
taskkill /F /IM node.exe

# Delete everything
Remove-Item -Recurse -Force node_modules
Remove-Item -Recurse -Force .next
Remove-Item package-lock.json

# Fresh install
npm install
npx prisma generate
```

This forced a complete rebuild of the internal client binaries.

### Step 3: The Diagnostic Script
Instead of guessing, we wrote a standalone script (`diagnose.ts`) using `tsx` to load the auth module *outside* of Next.js.

```typescript
import dotenv from 'dotenv';
dotenv.config({ path: '.env.local' });

console.log('DATABASE_URL:', process.env.DATABASE_URL ? '✓ Set' : '✗ Missing');
console.log('BETTER_AUTH_SECRET:', process.env.BETTER_AUTH_SECRET ? '✓ Set' : '✗ Missing');

try {
    const { auth } = await import('./src/lib/auth.ts');
    console.log('✅ Auth module loaded successfully!');
} catch (error) {
    console.error('❌ CAUGHT ERROR:', error);
}
```

**Result:** It finally printed the hidden error (Client Mismatch), confirming our hypothesis.

### Step 4: The Final Fix - Cache Clearing
Even after fixing Prisma versions, the 500 persisted. The root cause was **stale `.next` cache** holding incompatible compiled code.

```bash
Remove-Item -Recurse -Force .next
npm run dev
```

**Result:** OAuth started working immediately! 🎉

## 🎓 Key Takeaways

### 1. **Never upgrade core infra mid-hackathon**
Stick to stable versions (Prisma v5 over v7). Bleeding edge = bleeding time.

### 2. **Browser logs lie**
A 500 error in the network tab means nothing if the server logs are empty. Use a standalone diagnostic script (`node diagnose.js`) to test startup logic.

### 3. **Authentication is Hard**
Pre-verify your database adapter (Prisma vs Drizzle) before writing a single line of frontend code. Read the adapter's GitHub issues first.

### 4. **Next.js caches aggressively**
After major dependency changes, always delete `.next` folder. The build cache can hold stale binaries that cause silent failures.

### 5. **Module initialization errors are invisible**
If `console.log` in your route handler doesn't print, the error is happening during module loading. Extract the problematic import into a standalone script to debug.

## 🚀 Event-Driven UI Sync (Bonus Fix)

Once Auth was fixed, we discovered the UI wasn't updating when the AI added tasks.

**Problem:** ChatWidget creates task → Dashboard doesn't refresh

**Fix:** We implemented a lightweight **Global Event Bus**.

**Implementation:**
```typescript
// ChatWidget.tsx
window.dispatchEvent(new CustomEvent('task-update'));

// Dashboard page.tsx
useEffect(() => {
    const handleTaskUpdate = () => fetchTasks();
    window.addEventListener('task-update', handleTaskUpdate);
    return () => window.removeEventListener('task-update', handleTaskUpdate);
}, []);
```

**Result:** Instant UI sync without complex state management! ⚡

## 📊 Timeline

- **Hour 0-2:** Implement basic email auth (working)
- **Hour 3:** Add OAuth, immediate 500 errors
- **Hour 4-6:** Try raw pg Pool (failed)
- **Hour 7-9:** Upgrade to Prisma v7 (catastrophic)
- **Hour 10-11:** Configuration debugging (no progress)
- **Hour 12:** Write diagnostic script (breakthrough!)
- **Hour 13:** Downgrade to Prisma v5
- **Hour Error 14:** Clean slate rebuild
- **Hour 15:** Clear `.next` cache → **OAuth works!** 🎉

## 🏆 Victory Metrics

After the fix:
- ✅ Google OAuth: Account chooser loads, callback succeeds
- ✅ GitHub OAuth: Configured and functional
- ✅ Email verification: Prevents fake accounts
- ✅ Dashboard auto-refresh: Instant UI sync
- ✅ Terminal fallback: Dev-friendly testing

**From 500 errors to production-ready in 15 hours.** 💪

---

*This document serves as both a postmortem and a guide for future developers facing similar issues. The struggle was real, but the learning was worth it.*
