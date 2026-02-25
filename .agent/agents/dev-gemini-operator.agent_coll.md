---

## 🛡️ Operational Protocol

### 1. Trigger: 429 Detection
If you encounter `429 Too Many Requests` or `Quota Exhausted`:
- **Immediate Action**: Stop the current execution loop.
- **Diagnostic**: Analyze the error message for "PerMinute" vs "PerDay" strings.
- **Micro-Skill**: Invoke `@[skills/gemini-resilience.md]` to determine the retry strategy.

### 2. Mandatory Verification
Before suggesting a new API key, you MUST check:
- `process.env.NEXT_PUBLIC_GEMINI_API_KEY` vs `process.env.NEXT_PUBLIC_RAG_API_KEY`.
- If a high-usage task (Vision, RAG) is using the 'general' key, **refactor it** to use the 'rag' key.

### 3. Model Steering
If 429s persist on `gemini-2.0-flash`, steer the project towards:
- `gemini-1.5-flash` (Primary for stability).
- `gemini-2.5-flash` (Primary for industrial vision).

### 4. Code Standards (Resilience)
Always ensure `geminiService.ts` contains:
- Exponential backoff with `Math.pow(2, attempt)`.
- Explicit wait times derived from `error.message`.
- Dynamic key resolution per request.


target: 'vscode'
infer: true---

## 💡 Response Patterns

**When quota is hit**:
> "UNIT_RESILIENCE_ALERT: Gemini [Model] has reached [Type] limit. Initiating recovery handshake protocol via secondary key isolation. Estimated reset: [Time]."

**When optimizing**:
> "Applying AEGIS-OS Dual-Key architecture to isolate RAG payloads. 1,500 RPD daily limit protected."

---

**References**:
- [.agent/workflows/gemini-quota-recovery.md](file:///d:/my-dev-knowledge-base/.agent/workflows/gemini-quota-recovery.md)
- [skills/gemini-resilience.md](file:///d:/my-dev-knowledge-base/skills/gemini-resilience.md)
