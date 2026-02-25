import { AtomicReading } from "@/lib/storage/db";
import { computeBaseline, aggregateCurrentReadings, detectDeviations, formatDeviationReport } from "@/lib/baseline/detector";

/**
 * gemini-auditor.ts (Migrated to OpenRouter)
 * 
 * RESPONSIBILITY:
 * The "Brain" of the operation.
 * 1. Receives compressed time-series data.
 * 2. Formats a Clinical Prompt.
 * 3. Calls OpenRouter for analysis (DeepSeek).
 */

const OPENROUTER_KEY = process.env.NEXT_PUBLIC_OPENROUTER_API_KEY || '';

export interface AuditResult {
    risk_score: number;
    anomalies: string[];
    clinical_notes: string;
    is_false_positive?: boolean;
    metrics?: {
        current: { hypomimia: number; blinkRate: number; jitter: number; };
        baseline: { hypomimia: number; blinkRate: number; jitter: number; };
    };
}

export class GeminiAuditor {

    private readonly FREE_MODELS = [
        "xiaomi/mimo-v2-flash:free",      // Rank 1: Coding & Logic - 309B MoE
        "mistralai/mistral-small-24b-instruct-2501:free", // Rank 2: Agentic Coding (Devstral 2 2512)
        "deepseek/deepseek-v3:free",      // Rank 3: General Purpose (V3.1 Free)
        "google/gemini-2.0-flash-exp:free", // Rank 5: Speed & Context
        "google/gemini-2.0-flash-001:free", // Alternative Rank 5
        "meta-llama/llama-3.2-3b-instruct:free", // Fallback: Fast & Lightweight
        "openrouter/free"                 // OPTION 1: Automatic Routing (Catch-all)
    ];

    public async auditSession(readings: AtomicReading[], baseline: AtomicReading[]): Promise<AuditResult> {

        if (!OPENROUTER_KEY) {
            return {
                risk_score: 0,
                anomalies: ["Config Missing"],
                clinical_notes: "Waiting for Analysis..."
            };
        }

        const sessionStats = this.calculateStats(readings);
        const baselineStats = this.calculateStats(baseline);

        const baselineMetrics = computeBaseline(baseline);
        const currentReading = aggregateCurrentReadings(readings);
        const deviations = baselineMetrics ? detectDeviations(currentReading, baselineMetrics) : [];
        const deviationReport = formatDeviationReport(deviations, baselineMetrics);

        const SYSTEM_PROMPT = `
        You are an expert Neurological AI Auditor (mPower Protocol).
        
        TASK: Compare [CURRENT SESSION] vs [BASELINE] for signs of Parkinson's/Fatigue.

        DATA INTERPRETATION (FACIAL MOTILITY SCORE 0.0 - 1.0):
        - CRITICAL: LOWER scores represent HIGHER clinical risk (Masked Facies).
        - Score < 0.20: "Masked Facies" (High Risk). Minimal facial muscle activation.
        - Score 0.20 - 0.50: "Reduced Expressivity" (Symptomatic).
        - Score > 0.60: "Normal Expressivity". Healthily dynamic face.

        CLINICAL PRIORITY:
        1. Facial Motility & Vocal Jitter are the strongest markers for Parkinsonian symptoms.
        2. Blink Rate is secondary and often reflects fatigue/concentration rather than motor pathology.

        AUTONOMOUS SKEPTICISM: 
        - DELTA OVER THRESHOLD: If [CURRENT] Motility is HIGHER (better) than [BASELINE], it is NOT a risk. 
        - DEAD BASELINE: If [BASELINE] Motility is < 0.05, calibration likely failed. Do NOT flag as a change.
        - SENSOR ARTIFACT: If Face Metrics are perfectly identical (e.g. 1.000 vs 1.000) while Jitter is high, set is_false_positive: true.

        OUTPUT FORMAT (STRICT JSON):
        { 
          "risk_score": 0-100, 
          "anomalies": ["reason1",...], 
          "is_false_positive": boolean,
          "clinical_notes": "Follow this Markdown format strictly:\n\n### Clinical Summary\n[Brief summary of findings]\n\n### Biomarker Analysis\n| METRIC | BASELINE | CURRENT | DELTA | STATUS |\n| :--- | :--- | :--- | :--- | :--- |\n| Hypomimia (Expressivity) | 0.000 | 0.000 | 0.000 | Normal |\n| Blink Rate (BPM) | 0.0 | 0.0 | 0.0 | Normal |\n| Voice Jitter (Stability) | 0.000 | 0.000 | +0.000 | Significant |\n\n### Risk Analysis\n[Detailed risk assessment]" 
        }
        `;

        const isDeadBaseline = baselineStats.hypomimia < 0.05;

        const prompt = `
            **PROGRAMMATIC AUDIT**: ${deviations.length} deviation(s) detected via Z-Score math.
            
            **METRICS**:
            - CURRENT: Motility: ${sessionStats.hypomimia.toFixed(3)}, Blink: ${sessionStats.blinkRate.toFixed(1)}, Jitter: ${sessionStats.jitter.toFixed(4)}
            - BASELINE: Motility: ${baselineStats.hypomimia.toFixed(3)}, Blink: ${baselineStats.blinkRate.toFixed(1)}, Jitter: ${baselineStats.jitter.toFixed(4)}
            
            ${isDeadBaseline ? '⚠️ WARNING: Baseline Motility is near-zero.' : ''}
            
            ${deviationReport}
            
            **FORMAT**: Return JSON ONLY.
        `;

        // RETRY & ROTATION LOGIC
        // Strategy: Try each model in sequence. If fail, move to next.
        let lastError: any = null;

        for (const model of this.FREE_MODELS) {
            try {
                console.log(`[OPENROUTER] Attempting audit via ${model}...`);

                const controller = new AbortController();
                const timeout = setTimeout(() => controller.abort(), 60000); // 60s per model

                const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
                    method: "POST",
                    headers: {
                        "Authorization": `Bearer ${OPENROUTER_KEY}`,
                        "HTTP-Referer": "http://localhost:3000",
                        "X-Title": "Silent Health",
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        model: model,
                        messages: [{ role: "system", content: SYSTEM_PROMPT }, { role: "user", content: prompt }],
                        max_tokens: 1024
                    }),
                    signal: controller.signal
                });
                clearTimeout(timeout);

                // Handle server errors that warrant a retry with next model
                if (!response.ok) {
                    const status = response.status;
                    const errorText = await response.text();
                    console.warn(`[OPENROUTER] ${model} Failed (HTTP ${status}): ${errorText}`);

                    // If 404 (Not Found) or 429 (Rate Limit) or 5xx (Server Error), try next model.
                    // If 401 (Auth), stop immediately.
                    if (status === 401) throw new Error("Invalid API Key");

                    lastError = new Error(`HTTP ${status}: ${errorText}`);
                    continue; // Try next model
                }

                const data = await response.json();
                if (data.error) {
                    console.warn(`[OPENROUTER] ${model} API Error: ${data.error.message}`);
                    lastError = new Error(data.error.message);
                    continue;
                }

                // SUCCESS
                const content = data.choices[0].message.content;
                let report;
                try {
                    report = this.extractJson(content);
                } catch (e) {
                    console.warn(`[OPENROUTER] ${model} returned invalid JSON. Raw (first 100): ${content.substring(0, 100)}...`);
                    lastError = new Error("Invalid JSON response");
                    continue;
                }

                const clinical_notes = report.clinical_notes || 'No significant deviations detected.';

                return {
                    ...report,
                    clinical_notes,
                    metrics: { current: sessionStats, baseline: baselineStats }
                };

            } catch (error: any) {
                const isTimeout = error.name === 'AbortError';
                console.warn(`[OPENROUTER] ${model} Error: ${isTimeout ? 'Timeout' : error.message}`);
                lastError = error;
                // Loop continues to next model
            }
        }

        // All models failed
        console.error("OpenRouter Audit Final Failure! All models exhausted.", lastError);
        return {
            risk_score: -1,
            anomalies: ["Audit Service Unavailable"],
            clinical_notes: `## ⚠️ AUDIT FAILURE\nNetwork busy. Please retry the audit. Last error: ${lastError?.message || 'Unknown'}`
        };
    }

    private extractJson(text: string): any {
        // 1. Remove <think> blocks (common in reasoning models)
        let cleanText = text.replace(/<think>[\s\S]*?<\/think>/gi, "").trim();

        // 2. Remove markdown code blocks
        cleanText = cleanText.replace(/```json\n?|\n?```/g, "").trim();

        // 3. Find first '{' and last '}'
        const firstBrace = cleanText.indexOf('{');
        const lastBrace = cleanText.lastIndexOf('}');

        if (firstBrace === -1 || lastBrace === -1 || lastBrace <= firstBrace) {
            throw new Error("No JSON object found in response");
        }

        let jsonString = cleanText.substring(firstBrace, lastBrace + 1);

        // 4. Aggressive Sanitization for Markdown Tables in JSON
        // Common Issue: Models interpret \n in markdown as a literal newline in the string, breaking JSON.
        // We need to escape newlines that are inside string values.
        // Simple heuristic: If we see a newline that isn't seemingly part of the JSON structure, escape it.
        // Actually, a safer regex approach for common "markdown in json" errors:

        try {
            return JSON.parse(jsonString);
        } catch (e) {
            console.warn("JSON Parse Failed. Attempting to repair unescaped newlines...");
            // customized repair: escape control characters (0x00-0x1F) except inside likely structural places?
            // simpler: replace actual newlines with \n
            // carefully: this might break formatting if not done right, but better than a crash.
            // Let's rely on a known trick: passing the string through a cleaner.

            // Try to escape unescaped newlines
            jsonString = jsonString.replace(/\n/g, "\\n");

            try {
                return JSON.parse(jsonString);
            } catch (e2) {
                // If that fails, it might be effectively unrecoverable without a heavy parser.
                // One last try: sometimes they use single quotes?
                throw new Error("Invalid JSON response (Markdown formatting error)");
            }
        }
    }

    private calculateStats(readings: AtomicReading[]) {
        if (readings.length === 0) return { hypomimia: 1, blinkRate: 15, jitter: 0 };

        const sum = readings.reduce((acc, r) => ({
            hypomimia: acc.hypomimia + (r.face?.hypomimia_score || 0),
            blinkRate: acc.blinkRate + (r.face?.blink_rate || 0),
            jitter: acc.jitter + (r.voice?.jitter || 0)
        }), { hypomimia: 0, blinkRate: 0, jitter: 0 });

        return {
            hypomimia: sum.hypomimia / (readings.length || 1),
            blinkRate: sum.blinkRate / (readings.length || 1),
            jitter: sum.jitter / (readings.length || 1)
        };
    }
}

export const auditor = new GeminiAuditor();
