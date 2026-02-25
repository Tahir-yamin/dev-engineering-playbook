import { AtomicReading } from '../storage/db';

/**
 * baseline/detector.ts
 * 
 * RESPONSIBILITY:
 * Compute baseline statistics from historical readings
 * and detect deviations in current metrics.
 * 
 * ALGORITHM:
 * - Rolling window: Last 7 days or 500 readings (whichever is smaller)
 * - Z-Score = (current - mean) / stdDev
 * - Thresholds: Normal (<1σ), Minor (1-2σ), Significant (2-3σ), Critical (>3σ)
 */

export interface BaselineStats {
    metrics: {
        hypomimia: { mean: number; stdDev: number; min: number; max: number; };
        blinkRate: { mean: number; stdDev: number; min: number; max: number; };
        jawVariance: { mean: number; stdDev: number; min: number; max: number; };
        volumeJitter: { mean: number; stdDev: number; min: number; max: number; };
    };
    sampleSize: number;
    dateRange: { start: string; end: string; };
}

export interface Deviation {
    metric: string;
    current: number;
    baseline: number;
    stdDev: number;
    zScore: number;
    severity: 'normal' | 'minor' | 'significant' | 'critical';
}

/**
 * Compute mean and standard deviation for an array of numbers
 */
function computeStats(values: number[]): { mean: number; stdDev: number; min: number; max: number; } {
    if (values.length === 0) {
        return { mean: 0, stdDev: 0, min: 0, max: 0 };
    }

    const mean = values.reduce((sum, val) => sum + val, 0) / values.length;
    const variance = values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / values.length;
    const stdDev = Math.sqrt(variance);
    const min = Math.min(...values);
    const max = Math.max(...values);

    return { mean, stdDev, min, max };
}

/**
 * Compute baseline statistics from historical readings
 * Uses last 7 days or 500 readings, whichever is smaller
 */
export function computeBaseline(readings: AtomicReading[]): BaselineStats | null {
    if (readings.length < 3) {
        // Not enough data for meaningful statistics
        return null;
    }

    // Limit to last 500 readings for performance
    const limitedReadings = readings.slice(-500);

    // Extract metric arrays
    const hypomimiaScores = limitedReadings.map(r => r.face.hypomimia_score);
    const blinkRates = limitedReadings.map(r => r.face.blink_rate);
    const jawVariances = limitedReadings.map(r => r.face.jaw_variance);
    const volumeJitters = limitedReadings.map(r => r.voice.jitter);

    const timestamps = limitedReadings.map(r => r.timestamp);
    const dateRange = {
        start: new Date(Math.min(...timestamps)).toISOString(),
        end: new Date(Math.max(...timestamps)).toISOString()
    };

    return {
        metrics: {
            hypomimia: computeStats(hypomimiaScores),
            blinkRate: computeStats(blinkRates),
            jawVariance: computeStats(jawVariances),
            volumeJitter: computeStats(volumeJitters)
        },
        sampleSize: limitedReadings.length,
        dateRange
    };
}

/**
 * Detect deviations between current reading and baseline
 */
export function detectDeviations(
    current: AtomicReading,
    baseline: BaselineStats
): Deviation[] {
    const deviations: Deviation[] = [];

    // Helper to classify z-score severity (Direction Aware)
    // For Hypomimia: Higher is better, so only negative Z-scores (current < mean) are risky.
    // For Jitter: Lower is better, so only positive Z-scores (current > mean) are risky.
    const getSeverity = (z: number, metricType: 'motility' | 'jitter' | 'neutral'): Deviation['severity'] => {
        if (!isFinite(z)) return 'normal';
        const absZ = Math.abs(z);

        // Direction check
        if (metricType === 'motility' && z > 0) return 'normal'; // Improved expressivity
        if (metricType === 'jitter' && z < 0) return 'normal';   // Reduced tremor

        if (absZ >= 3.0) return 'critical';
        if (absZ >= 2.0) return 'significant';
        if (absZ >= 1.0) return 'minor';
        return 'normal';
    };

    // Helper to safely calculate z-score
    const safeZScore = (current: number, mean: number, stdDev: number): number => {
        if (stdDev < 0.001) return 0;
        return (current - mean) / stdDev;
    };

    // Hypomimia score (Motility)
    const hypomimiaZ = safeZScore(
        current.face.hypomimia_score,
        baseline.metrics.hypomimia.mean,
        baseline.metrics.hypomimia.stdDev
    );
    deviations.push({
        metric: 'Hypomimia Score',
        current: current.face.hypomimia_score,
        baseline: baseline.metrics.hypomimia.mean,
        stdDev: baseline.metrics.hypomimia.stdDev,
        zScore: hypomimiaZ,
        severity: getSeverity(hypomimiaZ, 'motility')
    });

    // Blink rate (Neutral - both directions can be symptomatic)
    const blinkRateZ = safeZScore(
        current.face.blink_rate,
        baseline.metrics.blinkRate.mean,
        baseline.metrics.blinkRate.stdDev
    );
    deviations.push({
        metric: 'Blink Rate',
        current: current.face.blink_rate,
        baseline: baseline.metrics.blinkRate.mean,
        stdDev: baseline.metrics.blinkRate.stdDev,
        zScore: blinkRateZ,
        severity: getSeverity(blinkRateZ, 'neutral')
    });

    // Jaw variance (Motility)
    const jawVarianceZ = safeZScore(
        current.face.jaw_variance,
        baseline.metrics.jawVariance.mean,
        baseline.metrics.jawVariance.stdDev
    );
    deviations.push({
        metric: 'Jaw Variance',
        current: current.face.jaw_variance,
        baseline: baseline.metrics.jawVariance.mean,
        stdDev: baseline.metrics.jawVariance.stdDev,
        zScore: jawVarianceZ,
        severity: getSeverity(jawVarianceZ, 'motility')
    });

    // Volume jitter (Jitter/Tremor)
    const volumeJitterZ = safeZScore(
        current.voice.jitter,
        baseline.metrics.volumeJitter.mean,
        baseline.metrics.volumeJitter.stdDev
    );
    deviations.push({
        metric: 'Volume Jitter',
        current: current.voice.jitter,
        baseline: baseline.metrics.volumeJitter.mean,
        stdDev: baseline.metrics.volumeJitter.stdDev,
        zScore: volumeJitterZ,
        severity: getSeverity(volumeJitterZ, 'jitter')
    });

    return deviations;
}

/**
 * Format deviations as markdown table for Gemini prompt
 */
export function formatDeviationReport(deviations: Deviation[], baseline: BaselineStats | null): string {
    if (!baseline || baseline.sampleSize < 10) {
        return '## BASELINE COMPARISON (CALIBRATING)\n\n' +
            '**Status**: Capturing Clinical Signature...\n' +
            '**Data Needed**: 100 frames (~3s) of stable monitoring.\n\n' +
            '| Metric | Value | Baseline | Z-Score | Status |\n' +
            '|--------|-------|----------|---------|--------|\n' +
            '| Hypomimia | ... | CALIB | ... | ⏳ CALIB |\n' +
            '| Blink Rate | ... | CALIB | ... | ⏳ CALIB |\n' +
            '| Motility | ... | CALIB | ... | ⏳ CALIB |';
    }

    const significantDeviations = deviations.filter(d => d.severity !== 'normal');

    let report = '## BASELINE COMPARISON (Rolling Window)\n\n';
    report += `**Sample Size**: ${baseline.sampleSize} frames extracted from memory.\n\n`;

    report += '| Metric | Current | Baseline (μ±σ) | Z-Score | Status |\n';
    report += '|--------|---------|----------------|---------|--------|\n';

    deviations.forEach(d => {
        const statusEmoji =
            d.severity === 'critical' ? '🔴 CRITICAL' :
                d.severity === 'significant' ? '🟠 SIGNIFICANT' :
                    d.severity === 'minor' ? '🟡 MINOR' :
                        '✅ NORMAL';

        report += `| ${d.metric} | ${d.current.toFixed(2)} | ${d.baseline.toFixed(2)}±${d.stdDev.toFixed(2)} | ${d.zScore > 0 ? '+' : ''}${d.zScore.toFixed(2)} | ${statusEmoji} |\n`;
    });

    report += '\n';

    if (significantDeviations.length > 0) {
        report += `**⚠️ DEVIATIONS DETECTED**: ${significantDeviations.length} clinical indicators showing significant variance from your baseline.\n\n`;
    } else {
        report += '**✅ ALL METRICS WITHIN NORMAL RANGE**\n';
    }

    return report;
}

/**
 * Aggregate current readings into a single representative reading
 * (Take median or mean of recent readings)
 */
export function aggregateCurrentReadings(readings: AtomicReading[]): AtomicReading {
    if (readings.length === 0) {
        // Return zero values if no readings
        return {
            timestamp: Date.now(),
            face: { hypomimia_score: 0, blink_rate: 0, jaw_variance: 0, ear: 0.3 },
            voice: { volume: 0, jitter: 0 }
        };
    }

    // Use mean for aggregation
    const hypomimia = readings.reduce((sum, r) => sum + r.face.hypomimia_score, 0) / readings.length;
    const blinkRate = readings.reduce((sum, r) => sum + r.face.blink_rate, 0) / readings.length;
    const jawVariance = readings.reduce((sum, r) => sum + r.face.jaw_variance, 0) / readings.length;
    const volume = readings.reduce((sum, r) => sum + r.voice.volume, 0) / readings.length;
    const jitter = readings.reduce((sum, r) => sum + r.voice.jitter, 0) / readings.length;
    const ear = readings.reduce((sum, r) => sum + (r.face.ear || 0), 0) / readings.length;

    return {
        timestamp: readings[readings.length - 1].timestamp,
        face: {
            hypomimia_score: hypomimia,
            blink_rate: blinkRate,
            jaw_variance: jawVariance,
            ear
        },
        voice: {
            volume,
            jitter
        }
    };
}
