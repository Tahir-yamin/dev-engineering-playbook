/**
 * export-pilot-data.ts
 * 
 * RESPONSIBILITY:
 * Export pilot study data to CSV for statistical analysis in R/Python.
 * Generates ground truth dataset for calculating Sensitivity, Specificity, ROC curves.
 * 
 * USAGE:
 * Add a button in the UI or run via browser console:
 * ```
 * import { exportPilotData } from '@/lib/export-pilot-data';
 * exportPilotData();
 * ```
 */

import { db } from './storage/db';

export async function exportPilotData() {
    console.log("[EXPORT] Starting data extraction from IndexedDB...");
    const sessions = await db.sessions.toArray();

    if (sessions.length === 0) {
        alert('⚠️ No sessions found. Run a sensing session first.');
        return;
    }

    // CSV Header
    let csv = 'session_id,date,label,risk_score,clinical_summary,anomalies,' +
        'hypomimia_raw,hypomimia_baseline,' +
        'blink_raw,blink_baseline,' +
        'jitter_raw,jitter_baseline,' +
        'flagged_as_abnormal\n';

    // CSV Rows
    let exportedCount = 0;
    for (const session of sessions) {
        const report = session.neuro_report;
        if (!report) continue;

        const current = report.metrics?.current;
        const baseline = report.metrics?.baseline;

        const hDev = report.baseline_comparison?.hypomimia?.severity || 'normal';
        const bDev = report.baseline_comparison?.blink_rate?.severity || 'normal';
        const vDev = report.baseline_comparison?.voice_jitter?.severity || 'normal';
        const flagged = ['significant', 'critical'].some(s => [hDev, bDev, vDev].includes(s)) ? 1 : 0;

        const label = session.session_label || 'UNLABELED';
        const summary = (report.clinical_notes || '').replace(/["\n\r]/g, ' ').slice(0, 100);
        const anomalies = (report.anomalies || []).join('; ');

        csv += `"${session.id}","${session.date}","${label}",${report.risk_score || 0},"${summary}","${anomalies}",` +
            `${(current?.hypomimia || 0).toFixed(4)},${(baseline?.hypomimia || 0).toFixed(4)},` +
            `${(current?.blinkRate || 0).toFixed(2)},${(baseline?.blinkRate || 0).toFixed(2)},` +
            `${(current?.jitter || 0).toFixed(6)},${(baseline?.jitter || 0).toFixed(6)},` +
            `${flagged}\n`;
        exportedCount++;
    }

    if (exportedCount === 0) {
        alert('⚠️ Found sessions, but no AI reports ready to export yet.');
        return;
    }

    const fileName = `silent-health-export-${new Date().toISOString().split('T')[0]}.csv`;
    const BOM = '\uFEFF';
    const content = BOM + csv;

    // TRY METHOD 1: MODERN FILE SYSTEM ACCESS API
    if (typeof window !== 'undefined' && 'showSaveFilePicker' in window) {
        try {
            const handle = await (window as any).showSaveFilePicker({
                suggestedName: fileName,
                types: [{
                    description: 'CSV File',
                    accept: { 'text/csv': ['.csv'] },
                }],
            });
            const writable = await handle.createWritable();
            await writable.write(content);
            await writable.close();
            alert("✅ SUCCESS: File saved correctly!");
            return;
        } catch (err) {
            if ((err as Error).name === 'AbortError') return;
            console.error("Method 1 failed, falling back...", err);
        }
    }

    // METHOD 2: REINFORCED BLOB DOWNLOAD
    try {
        const blob = new Blob([content], { type: 'text/csv;charset=utf-8' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');

        a.style.display = 'none';
        a.href = url;
        a.download = fileName;

        document.body.appendChild(a);

        // Critical: Small delay to ensure browser registers the anchor
        setTimeout(() => {
            a.click();
            console.log(`✅ Method 2 triggered: ${fileName}`);

            // Critical: Wait much longer before revoking
            setTimeout(() => {
                window.URL.revokeObjectURL(url);
                if (document.body.contains(a)) document.body.removeChild(a);
            }, 10000);
        }, 100);

        // EXTRA SECURE FALLBACK: CLIPBOARD
        setTimeout(() => {
            const copyPrompt = confirm("✅ Export Started!\n\nIf the browser downloaded a 'UUID' file or nothing happened, click OK to COPY the data to your clipboard as an emergency fallback.");
            if (copyPrompt) {
                navigator.clipboard.writeText(csv).then(() => {
                    alert("📋 SUCCESS: Data copied to clipboard! You can paste it into Notepad now.");
                });
            }
        }, 1000);

    } catch (err) {
        console.error("❌ Export failed:", err);
        alert("❌ Export failed. Data printed to browser console (F12) for recovery.");
        console.log("--- START CSV DATA ---");
        console.log(csv);
        console.log("--- END CSV DATA ---");
    }
}
