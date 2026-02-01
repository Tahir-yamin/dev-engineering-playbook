---
description: Systematic recovery protocol for Gemini API 429 / Quota exhausted errors
---

# Workflow: Gemini API Quota Recovery

## When to Use
- You see `429 Too Many Requests` in the logs.
- The AI responds with "HANDSHAKE_FAILED" or "ARCHITECT_OFFLINE".
- You suspect the 1,500 daily requests cap or a 20 requests/minute cap has been hit.

---

## Step 1: Verify Quota in Cloud Console
Don't guess. Check the source of truth.

1.  Open [Google Cloud Console - APIs & Services](https://console.cloud.google.com/apis/api/generativeai.googleapis.com/quotas).
2.  Look for **"Generate Content requests"** for both `gemini-1.5-flash` and `gemini-2.5-flash`.
3.  **Action**: If "Active Quota" is 0 for your preferred model, you **MUST** switch to a model with >0 quota.

---

## Step 2: Implement Exponential Backoff
If the error is `PerMinute`, wait. If `PerDay`, stop.

```bash
# Check if your generateWithRetry logic handles the wait time extraction
# search for 'retry in' in error.message
```

---

## Step 3: Dual-Key Isolation
If one key is exhausted, deploy a second key for segmented functions.

1.  Add `NEXT_PUBLIC_RAG_API_KEY` to `.env.local`.
2.  Update `geminiService.ts` to use `getGenAI('rag')` for vision/search tasks.

---

## Step 4: Validate .env Synchronization
Next.js sometimes caches env variables.

// turbo
```powershell
# Restart the development server to clear env cache
Stop-Process -Name "node" -Force
npm run dev
```

---

## Step 5: Test Handshake
Run a minimal test query to verify the link.

```bash
# Verify log output for [AEGIS-OS] Handshake initialized (general) with key: Aiza...
```

---

**Related Skills**: [gemini-resilience.md](file:///d:/my-dev-knowledge-base/skills/gemini-resilience.md)
**Sources**: @conversation:03631d28
