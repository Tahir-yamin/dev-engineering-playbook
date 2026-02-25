---
name: neuro-clinical-auditing
description: Real-time neurological auditing patterns using multimodal AI (vision + voice) and local baselines.
allowed-tools: Read, Write, Edit
version: 1.0
priority: HIGH
---

# Neuro-Clinical Auditing Skill

> **Patterns for high-fidelity neurological monitoring and AI-driven clinical assessment.**

---

## Core Architecture

| Component | Responsibility |
|-----------|----------------|
| **Sensor Engine** | 30Hz 478-point Face Mesh + Web Audio Pitch/Amplitude extraction |
| **Local Baselines** | Capturing user-specific "Healthy State" data in IndexedDB |
| **AI Auditor** | Comparing real-time vectors vs Baseline via High-Reasoning LLMs |
| **Clinical UI** | Rendering UPDRS-aligned trend charts and Markdown reports |

---

## Implementation Patterns

### 1. Robust Baseline Comparison
Never compare raw scores directly. Use **Z-Scores** or **Deltas** relative to the user's specific performance environment.

```typescript
// Pattern: Baseline Calibration Check
const isDeadBaseline = baselineStats.hypomimia < 0.05; 
// If baseline is near-zero, the sensor failed during setup. Don't audit.
```

### 2. Multi-Model Rotation (Free Tier Stability)
When using free-tier LLMs for clinical reasoning, rotate through models to bypass rate limits and "invalid JSON" errors.

```typescript
const FREE_MODELS = [
    "xiaomi/mimo-v2-flash:free",
    "mistralai/mistral-small-24b-instruct:free",
    "deepseek/deepseek-v3:free"
];
// Logic: Try model A -> Catch Error -> Try model B
```

### 3. JSON Repair for Markdown Responses
Models often return unescaped newlines in Markdown tables inside JSON strings. Aggressively sanitize before parsing.

```typescript
function extractJson(text: string) {
    let cleanText = text.replace(/<think>[\s\S]*?<\/think>/gi, "").trim();
    // Aggressively escape internal newlines that break JSON
    const jsonString = cleanText.substring(firstBrace, lastBrace + 1).replace(/\n/g, "\\n");
    return JSON.parse(jsonString);
}
```

---

## Clinical Biomarkers

| Marker | Clinical Significance | Sensor Target |
|--------|----------------------|---------------|
| **Hypomimia** | "Masked Facies" in Parkinson's | 78-point Eyes/Mouth motility |
| **Breathiness** | Laryngeal muscle weakness | Vocal Shimmer / APQ |
| **Micro-Tremor** | High-frequency motor instability | Vocal Jitter / PPQ |
| **Blink Rate** | Fatigue vs. Dopamine levels | Eye Aspect Ratio (EAR) |

---

## Anti-Patterns

- ❌ **Cloud-Processing RAW Video**: Violates patient privacy. Always process at the Edge.
- ❌ **Absolute Thresholds**: Clinical norms vary by age/lighting. Always use Baselines.
- ❌ **Intrusive Spinners**: Use skeleton states or "Zero-Install" instant-on UI.

---

## Verification Criteria

1. **Verify Latency**: 3D Landmarks must maintain >24fps for accurate tremor detection.
2. **Verify Privacy**: Ensure `console.log` doesn't leak base64 image strings.
3. **Verify Audit Trail**: Every session must be persisted to IndexedDB with a unique `tabId`.
