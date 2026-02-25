'use client';

import { useEffect, useRef } from 'react';
import { db } from '@/lib/storage/db';

/**
 * AuditorLoop.tsx
 * 
 * RESPONSIBILITY:
 * The "Cron Job" of the browser.
 * Checks on interval if a nightly audit is due.
 */

export default function AuditorLoop({
    onAnalyzingChange,
    onAuditComplete
}: {
    onAnalyzingChange?: (val: boolean) => void,
    onAuditComplete?: (count: number) => void
}) {
    const isAnalyzing = useRef(false);
    const isChecking = useRef(false); // Lock to prevent interval overlap
    const lastAuditCount = useRef(0);
    const lastAuditAttempt = useRef(0);

    const setIsAnalyzing = (val: boolean) => {
        isAnalyzing.current = val;
        onAnalyzingChange?.(val);
    };

    // Initialize history on mount
    useEffect(() => {
        (async () => {
            const count = await db.readings.count();
            lastAuditCount.current = count;
            onAuditComplete?.(count);
            console.log(`📡 [AUDITOR] Initialized at ${count} frames. Next trigger at ${count + 300}.`);

            // CLEANUP: Delete sessions stuck in "..." or "SESSION STALLED" state
            // Reasoning: In-progress audits killed by refresh/HMR are invalid and should vanish.
            const stalled = await db.sessions
                .filter(s =>
                    s.neuro_report?.risk_score === '...' ||
                    (s.neuro_report?.risk_score === 'N/A' && (s.neuro_report?.clinical_notes?.includes('SESSION STALLED') ?? false))
                )
                .toArray();

            if (stalled.length > 0) {
                console.log(`🧹 [AUDITOR] Deleting ${stalled.length} stalled/phantom sessions.`);
                await db.sessions.bulkDelete(stalled.map(s => s.id));
            }
        })();
    }, []);

    const checkAuditDue = async () => {
        if (isChecking.current) return;

        // Recovery: If we've been "analyzing" for more than 60s, something hung. Reset.
        if (isAnalyzing.current && (Date.now() - lastAuditAttempt.current > 60000)) {
            console.warn("⚠️ [AUDITOR] Analysis Task Timeout. Resetting Lock.");
            setIsAnalyzing(false);
        }

        if (isAnalyzing.current) return;

        // BACK-PRESSURE: Avoid overlapping checks
        if (isChecking.current) return;
        isChecking.current = true;

        try {
            const count = await db.readings.count();

            // TRIGGER: Every 300 NEW frames since last audit (~10s at 30fps)
            // MINIMUM DATA: Require enough history for baseline Comparison
            if (count >= lastAuditCount.current + 300 && count >= 500) {
                // LOCK IMMEDIATELY
                setIsAnalyzing(true);
                lastAuditAttempt.current = Date.now();
                console.log(`🚀 [AUDITOR] Pulse [Next 300 @ ${lastAuditCount.current + 300}]. Analyzing...`);

                try {
                    // 1. Fetch data SURGICALLY (High Performance)
                    const toProcess = await db.readings.orderBy('timestamp').reverse().limit(100).toArray();
                    const baseline = await db.readings.orderBy('timestamp').reverse().offset(100).limit(500).toArray();

                    // Restore Chronological Order
                    toProcess.reverse();
                    baseline.reverse();

                    console.log(`📊 [AUDITOR] Analyzing Snapshot [${toProcess.length} pts] vs Baseline [${baseline.length} pts]`);

                    // 2. RETENTION POLICY: Surgical Deletion
                    const fiveMinsAgo = Date.now() - (5 * 60 * 1000);
                    await db.readings.where('timestamp').below(fiveMinsAgo).delete();

                    // 3. PHANTOM SESSION: Update Log Now
                    const phantomId = crypto.randomUUID();
                    await db.sessions.add({
                        id: phantomId,
                        date: new Date().toISOString(),
                        duration_ms: 2000,
                        session_label: 'UNLABELED',
                        neuro_report: {
                            risk_score: '...',
                            clinical_notes: '# NEURO-ANALYSIS IN PROGRESS...\nSychronizing with Clinical Brain.',
                            anomalies: ['Optimizing...']
                        }
                    });

                    // 4. Trigger AI Audit with 60s Watchdog
                    const controller = new AbortController();
                    const timeoutId = setTimeout(() => controller.abort(), 60000);

                    try {
                        const response = await fetch('/api/audit', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ readings: toProcess, baseline }),
                            signal: controller.signal
                        });
                        clearTimeout(timeoutId);

                        if (!response.ok) throw new Error("API Failure");
                        const report = await response.json();

                        // 5. Finalize
                        await db.sessions.update(phantomId, { neuro_report: report });

                        // Update marker ONLY ON SUCCESS to ensure re-try on transient failure
                        const currentCount = await db.readings.count();
                        lastAuditCount.current = currentCount;
                        onAuditComplete?.(currentCount);
                        console.log(`✅ [AUDITOR] Pulse Complete. Ref:${phantomId}`);

                    } catch (fetchErr: any) {
                        const isTimeout = fetchErr.name === 'AbortError';
                        await db.sessions.update(phantomId, {
                            neuro_report: {
                                risk_score: 'ERR',
                                clinical_notes: isTimeout ? "## ⚠️ GATEWAY TIMEOUT\nNeural nodes are congested. Retrying..." : "## ⚠️ NEURO-SYNC FAILED\nConnection lost.",
                                anomalies: ["Sync Failure"]
                            }
                        });
                    } finally {
                        setIsAnalyzing(false);
                    }
                } catch (err) {
                    console.error("❌ [AUDITOR] Pulse Failed:", err);
                    setIsAnalyzing(false);
                }
            }
        } catch (err) {
            console.error("❌ [AUDITOR] Index Error:", err);
        } finally {
            isChecking.current = false;
        }
    };

    useEffect(() => {
        (window as any).triggerAudit = checkAuditDue;
        const interval = setInterval(checkAuditDue, 2000);
        return () => {
            clearInterval(interval);
            delete (window as any).triggerAudit;
        };
    }, []);

    return null;
}
