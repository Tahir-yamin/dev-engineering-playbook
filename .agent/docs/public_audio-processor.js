/**
 * audio-processor.js
 * 
 * Custom AudioWorkletProcessor for real-time clinical feature extraction.
 * Replaces deprecated ScriptProcessorNode.
 */

class AudioProcessor extends AudioWorkletProcessor {
    constructor() {
        super();
        this._lastFrameTime = 0;
    }

    process(inputs, _outputs, _parameters) {
        const input = inputs[0];
        if (!input || input.length === 0) return true;

        const channelData = input[0];
        const length = channelData.length;
        if (length === 0) return true;

        // 1. RMS (Volume/Energy)
        let sumSquares = 0;
        for (let i = 0; i < length; i++) {
            sumSquares += channelData[i] * channelData[i];
        }
        const rms = Math.sqrt(sumSquares / length);

        // 2. ZCR (Zero Crossing Rate - mapped to "Jitter")
        // High ZCR usually indicates noise or high-frequency "jitter" in speech.
        let crossings = 0;
        for (let i = 1; i < length; i++) {
            if ((channelData[i] >= 0 && channelData[i - 1] < 0) ||
                (channelData[i] < 0 && channelData[i - 1] >= 0)) {
                crossings++;
            }
        }
        const zcr = crossings; // Number of crossings in this buffer

        // Emit features to main thread
        this.port.postMessage({
            rms,
            zcr,
            ts: Date.now()
        });

        return true;
    }
}

registerProcessor('audio-processor', AudioProcessor);
