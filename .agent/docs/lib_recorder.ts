import { db, AtomicReading } from '@/lib/storage/db';
import { MedicalMath } from '@/lib/medical/blendshapes';

/**
 * DataRecorder.ts
 * 
 * RESPONSIBILITY:
 * The "Glue" between Sensors and Database.
 */

const SAMPLE_RATE_MS = 33; // ~30Hz High Fidelity

export class DataRecorder {
    private buffer: Partial<AtomicReading> = {};
    private lastSave = 0;
    private isSaving = false;
    private math = new MedicalMath();

    /**
     * Ingests raw MediaPipe results (landmarks + blendshapes)
     */
    public onVision(rawResults: { faceLandmarks?: unknown[]; multiFaceLandmarks?: unknown[]; faceBlendshapes?: unknown[] }) {
        try {
            // Calculate clinical biomarkers from raw sensor data
            const signal = this.math.processFrame(rawResults);

            this.buffer.face = {
                hypomimia_score: signal.hypomimia_score,
                blink_rate: signal.blink_rate,
                jaw_variance: signal.jaw_variance,
                ear: signal.ear
            };

            this.tryFlush();
        } catch (error) {
            console.error('❌ recorder.onVision ERROR:', error);
        }
    }

    public onAudio(features: { volume: number, jitter: number }) {
        this.buffer.voice = features;
        this.tryFlush();
    }

    private async tryFlush() {
        const now = Date.now();

        // 1. Throttle check
        if (now - this.lastSave < SAMPLE_RATE_MS) return;

        // 2. Concurrency lock
        if (this.isSaving) return;

        // 3. Data check
        if (this.buffer.face || this.buffer.voice) {
            this.isSaving = true;
            // IMPORTANT: Update timestamp BEFORE the await to prevent re-entry 
            // if the database write hangs or is very slow. 
            this.lastSave = now;

            const reading: AtomicReading = {
                timestamp: now,
                face: this.buffer.face || { hypomimia_score: 0, blink_rate: 0, jaw_variance: 0, ear: 0.3 },
                voice: this.buffer.voice || { volume: 0, jitter: 0 }
            };

            try {
                await db.readings.add(reading);
                // SUCCESS: Clear buffer to prevent stale data repetition
                this.buffer = {};
            } catch (error) {
                console.error('❌ DATABASE WRITE FAILED:', error);
            } finally {
                this.isSaving = false;
            }
        }
    }

    public reset() {
        this.buffer = {};
        this.math.reset();
        console.log("💾 Recorder: History Reset");
    }
}

export const recorder = new DataRecorder();
