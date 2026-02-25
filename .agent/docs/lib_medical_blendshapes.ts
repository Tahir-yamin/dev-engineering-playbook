/**
 * blendshapes.ts
 * 
 * RESPONSIBILITY:
 * Convert raw MediaPipe landmarks into clinical "Digital Biomarkers".
 */

export interface ClinicalSignal {
    hypomimia_score: number; // 0-1 (1 = Normal Expressivity, 0 = Frozen Mask)
    blink_rate: number;      // Blinks per minute
    jaw_variance: number;    // Variance in jaw opening
    ear: number;             // Eye Aspect Ratio
}

// Moving Average Window
const HISTORY_SIZE = 30 * 5; // 5 seconds @ 30fps

export class MedicalMath {
    private jawHistory: number[] = [];
    private lastBlinkTime: number = 0;

    // START: Rolling Window Logic
    private blinkTimestamps: number[] = []; // Stores timestamps of blinks in last 60s
    // END: Rolling Window Logic

    /**
     * Ingests raw MediaPipe results and updates clinical scores.
     */
    public processFrame(results: { faceLandmarks?: any[], multiFaceLandmarks?: any[], faceBlendshapes?: any[] }): ClinicalSignal {
        // Handle both old results.multiFaceLandmarks and new results.faceLandmarks
        const landmarks = results.faceLandmarks?.[0] || results.multiFaceLandmarks?.[0];
        const blendshapes = results.faceBlendshapes?.[0]?.categories;

        if (!landmarks || landmarks.length === 0) {
            return this.getNeutralSignal();
        }

        // 1. Calculate Jaw Geometry (Redundant Fallback)
        const jawDist = this.euclidean(landmarks[13], landmarks[14]);
        const faceHeight = this.euclidean(landmarks[10], landmarks[152]);
        const normalizedJaw = faceHeight > 0 ? jawDist / faceHeight : 0;
        this.updateHistory(this.jawHistory, normalizedJaw);
        const jawVariance = this.calculateVariance(this.jawHistory);

        // 2. Blink Detection (Eye Aspect Ratio - EAR)
        const leftEAR = this.calculateEAR(landmarks, [33, 160, 158, 133, 153, 144]);
        const rightEAR = this.calculateEAR(landmarks, [362, 385, 387, 263, 373, 380]);
        const avgEAR = (leftEAR + rightEAR) / 2.0;

        // TUNED THRESHOLD: Increased to 0.28 for higher sensitivity to varied anatomical baselines
        if (avgEAR < 0.28 && Date.now() - this.lastBlinkTime > 150) {
            this.blinkTimestamps.push(Date.now());
            this.lastBlinkTime = Date.now();
        }

        // Prune old blinks (> 30 seconds ago) for higher responsiveness
        const now = Date.now();
        this.blinkTimestamps = this.blinkTimestamps.filter(t => now - t <= 30000);

        // 3. Clinical Expressivity (Hypomimia) using BLENDSHAPES
        // If blendshapes are available (Mediapipe Tasks Vision), use them for high-fidelity scoring.
        let hypomimiaScore = 0;

        if (blendshapes) {
            // Helper to get score by category name
            const getScore = (name: string) => blendshapes.find((b: any) => b.categoryName === name)?.score || 0;

            // A. Brow Activity (Corrugator + Frontalis)
            // browDownLeft, browDownRight, browOuterUpLeft, browOuterUpRight
            const browActivity = Math.max(
                getScore('browDownLeft'), getScore('browDownRight'),
                getScore('browOuterUpLeft'), getScore('browOuterUpRight')
            );

            // B. Mouth Activity (Orbicularis Oris + Zygomaticus)
            // mouthSmile, mouthFrown, mouthPucker, mouthFunnel, mouthOpen
            const mouthActivity = Math.max(
                getScore('mouthSmileLeft'), getScore('mouthSmileRight'),
                getScore('mouthFrownLeft'), getScore('mouthFrownRight'),
                getScore('mouthPucker'), getScore('mouthFunnel'),
                getScore('mouthOpen')
            );

            // C. Combined Clinical Score (0.0 - 1.0)
            // Weighted mix: Mouth (40%) + Brow (40%) + Jaw Variance (20%)
            // We apply a sigmoid-like boost because micro-expressions are subtle (0.1 - 0.3 range)
            const rawActivity = (browActivity * 0.4) + (mouthActivity * 0.4) + (jawVariance * 4.0); // Jaw is geometrically small, so boost x4

            // Clamp and Amplify: Raw activity of 0.2 should map to ~0.6 score to show "Life"
            hypomimiaScore = Math.min(rawActivity * 2.5, 1.0);
        } else {
            // FALLBACK: Old Geometric Method (Legacy)
            const leftBrow = Math.abs(landmarks[70].y - landmarks[105].y);
            const rightBrow = Math.abs(landmarks[300].y - landmarks[334].y);
            const browAvg = (leftBrow + rightBrow) / 2;

            const mouthWidth = this.euclidean(landmarks[61], landmarks[291]);
            const mouthHeight = this.euclidean(landmarks[0], landmarks[17]);
            const mouthAvg = (mouthWidth + mouthHeight) / 2;

            const rawScore = (jawVariance * 1000) + (browAvg * 15) + (mouthAvg * 2);
            hypomimiaScore = Math.min(rawScore, 1.0);
        }

        return {
            hypomimia_score: hypomimiaScore,
            // ROLLING WINDOW BPM
            blink_rate: this.calculateBPM(this.blinkTimestamps),
            jaw_variance: jawVariance,
            ear: avgEAR
        };
    }

    private calculateBPM(timestamps: number[]): number {
        if (timestamps.length < 2) return 0;

        // DYNAMIC WINDOW:
        // Calculate rate based on the ACTUAL time span covered by the buffer.
        // This prevents artificially low BPM during the first 30 seconds.
        const first = timestamps[0];
        const last = timestamps[timestamps.length - 1];
        const durationMs = last - first;

        if (durationMs < 1000) return 0; // Avoid divide-by-zero or massive spikes

        // Rate = (Count - 1) / (Duration in Minutes)
        // We subtract 1 because N timestamps define N-1 intervals
        const rate = ((timestamps.length - 1) / durationMs) * 60000;
        return Math.round(rate);
    }

    private updateHistory(arr: number[], val: number) {
        arr.push(val);
        if (arr.length > HISTORY_SIZE) arr.shift();
    }

    private euclidean(p1: any, p2: any): number {
        if (!p1 || !p2) return 0;
        return Math.sqrt(Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2));
    }

    private calculateEAR(landmarks: any[], indices: number[]): number {
        const p1 = landmarks[indices[0]];
        const p2 = landmarks[indices[1]];
        const p3 = landmarks[indices[2]];
        const p4 = landmarks[indices[3]];
        const p5 = landmarks[indices[4]];
        const p6 = landmarks[indices[5]];

        if (!p1 || !p2 || !p3 || !p4 || !p5 || !p6) return 0.3;

        const num = this.euclidean(p2, p6) + this.euclidean(p3, p5);
        const den = 2.0 * this.euclidean(p1, p4);
        return den > 0 ? num / den : 0.3;
    }

    private calculateVariance(arr: number[]): number {
        if (arr.length < 2) return 0.02; // Default motility
        const mean = arr.reduce((a, b) => a + b, 0) / arr.length;
        return arr.map(x => Math.pow(x - mean, 2)).reduce((a, b) => a + b, 0) / arr.length;
    }

    private getNeutralSignal(): ClinicalSignal {
        return { hypomimia_score: 0, blink_rate: 0, jaw_variance: 0, ear: 0.3 };
    }

    public reset() {
        this.jawHistory = [];
        this.blinkTimestamps = [];
        this.lastBlinkTime = 0;
    }
}
