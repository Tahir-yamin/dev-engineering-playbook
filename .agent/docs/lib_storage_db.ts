import Dexie, { Table } from 'dexie';

/**
 * db.ts
 * 
 * RESPONSIBILITY:
 * Manage the "Data Vault" (Local IndexedDB).
 * 
 * PRIVACY POLICY:
 * 1. AtomicReadings (Raw 30Hz data) -> 24 hour retention.
 * 2. SessionSummaries (Aggregated) -> 30 day retention.
 * 3. NO cloud sync of raw data.
 */

export interface AtomicReading {
    id?: number; // Auto-increment key
    timestamp: number;
    face: {
        hypomimia_score: number;
        blink_rate: number;
        jaw_variance: number;
        ear: number; // Eye Aspect Ratio
    };
    voice: {
        volume: number;
        jitter: number;
    };
}

export interface NeuroReport {
    risk_score: number | string;
    summary?: string;
    clinical_notes?: string;
    anomalies?: string[];
    metrics?: {
        current: {
            hypomimia: number;
            blinkRate: number;
            jawVariance: number;
            jitter: number;
            volume: number;
        };
        baseline?: {
            hypomimia: number;
            blinkRate: number;
            jawVariance: number;
            jitter: number;
            volume: number;
        };
    };
    baseline_comparison?: {
        hypomimia: { severity: string; deviation: string };
        blink_rate: { severity: string; deviation: string };
        jaw_variance: { severity: string; deviation: string };
        voice_jitter: { severity: string; deviation: string };
    };
    timestamp?: number;
}

export interface SessionSummary {
    id?: string; // UUID
    date: string; // ISO Date
    duration_ms: number;
    neuro_report?: NeuroReport; // Professional clinical report
    session_label?: 'BASELINE' | 'SIMULATED' | 'FALSE_POSITIVE' | 'FALSE_NEGATIVE' | 'UNLABELED'; // For clinical verification
}

export class SilentHealthDB extends Dexie {
    readings!: Table<AtomicReading>;
    sessions!: Table<SessionSummary>;

    constructor() {
        super('SilentHealthDB');

        // Version 1: Original schema
        this.version(1).stores({
            readings: '++id, timestamp',
            sessions: 'id, date'
        });

        // Version 2: Add session_label for pilot study
        this.version(2).stores({
            readings: '++id, timestamp',
            sessions: 'id, date, session_label'
        });
    }
}

export const db = new SilentHealthDB();
