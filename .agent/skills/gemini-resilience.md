# Gemini API Resilience & Quota Management

**Topics**: Quota Management, Rate Limiting, API Resilience, Model Selection
**Version**: 1.0
**Last Updated**: 2026-01-31

---

## Skill: Overcoming 429 Quota Exhaustion

### When to Use
- Encountering persistent `429 Too Many Requests` or `429 Quota Exhausted` errors.
- Verification of API keys shows they are valid but still failing.
- High-usage features (like RAG or Vision) are impacting general chat availability.

### Patterns & Solutions

#### 1. Smart Retry Logic (The 5-Tier Strategy)
Never assume all 429s are the same. Distinguish between **PerMinute** (transient) and **PerDay** (critical) exhausted limits.

```typescript
async function generateWithRetry(model: any, parts: any[], retries = 5) {
    for (let attempt = 0; attempt < retries; attempt++) {
        try {
            return await model.generateContent(parts);
        } catch (error: any) {
            const errorMessage = JSON.stringify(error) || error.message || "";
            const isRateLimit = error.status === 429 || errorMessage.includes("429") || errorMessage.includes("quota");
            
            // Critical check for Daily limit vs Minute limit
            const isDailyLimit = errorMessage.includes("PerDay") || 
                               (errorMessage.includes("free_tier_requests") && 
                                errorMessage.includes("limit: 0"));

            if (isRateLimit && attempt < retries - 1) {
                if (isDailyLimit) {
                    throw new Error("GEMINI_DAILY_LIMIT: Quota exhausted for 24h.");
                }

                // Extract wait time if possible (e.g., "retry in 1.4s")
                const delayMatch = errorMessage.match(/retry in ([\d\.]+)s/);
                const delay = delayMatch ? parseFloat(delayMatch[1]) * 1000 : (5000 * Math.pow(2, attempt));
                
                await wait(delay + 1000);
                continue;
            }
            throw error;
        }
    }
}
```

#### 2. Dual-Key Architecture (Isolation)
Isolate high-bandwidth features (RAG, Vision) from basic conversation to prevent total service blackout.

- `NEXT_PUBLIC_GEMINI_API_KEY`: General chat / Persona.
- `NEXT_PUBLIC_RAG_API_KEY`: Document Search / Vision analysis.

#### 3. Model Quota Verification (The "Trap" Models)
Some models (like `gemini-2.0-flash` on certain Free Tiers) may report **0 Active Quota** in the Google Cloud Console while `gemini-1.5-flash` or `gemini-2.5-flash` show **Active Quota (e.g., 20/min)**.

**Priority List for Stability**:
1. `gemini-1.5-flash` (Highest stability, widely available quota)
2. `gemini-2.5-flash` (Excellent for complex vision tasks)
3. `gemini-2.0-flash` (Experimental, check quota first)

---

### Lessons Learned:
- ✅ **Dynamic Key Loading**: Fetch `process.env` keys *inside* the service functions, not at module-level, to avoid using cached/empty keys after `.env.local` updates.
- ✅ **Masked Logging**: Always log a masked version of the key (e.g., `Aiza...3x9z`) to verify the handshake without exposing secrets.
- ❌ **Static Model ID**: Avoid hardcoding a single model ID if 429s persist; implement a fallback mechanism.

---

**Source**: Conversation 03631d28 (Gemini API Model Update)
**Related Skills**: [gemini-agent-skills.md](file:///d:/my-dev-knowledge-base/skills/gemini-agent-skills.md)
