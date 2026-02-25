/// <reference lib="webworker" />
import { FaceLandmarker, FilesetResolver } from "@mediapipe/tasks-vision";

/**
 * SensorWorker.ts (Web Worker)
 * 
 * RESPONSIBILITY:
 * Real-time facial landmark tracking using MediaPipe Tasks-Vision WASM.
 */

let faceLandmarker: FaceLandmarker | null = null;
let isReady = false;

// Initialize MediaPipe
const init = async () => {
    try {
        console.log('📹 Sensor Worker: Loading MediaPipe WASM...');
        const vision = await FilesetResolver.forVisionTasks(
            "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0/wasm"
        );

        faceLandmarker = await FaceLandmarker.createFromOptions(vision, {
            baseOptions: {
                modelAssetPath: `https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task`,
                delegate: "GPU"
            },
            outputFaceBlendshapes: true,
            runningMode: "VIDEO",
            numFaces: 1,
            minFaceDetectionConfidence: 0.2, // Lower threshold to "catch" face faster on CPU
            minTrackingConfidence: 0.2   // Keep lock even if processing lags
        });

        isReady = true;
        postMessage({ type: 'READY' });
        console.log('📹 Sensor Worker: MediaPipe FaceLandmarker Ready!');
    } catch (error) {
        console.error('📹 Sensor Worker: Initialization Failed', error);
        postMessage({ type: 'ERROR', error });
    }
};

init();

// Message Handler
self.onmessage = async (event: MessageEvent) => {
    const { type, image } = event.data;

    if (type === 'PROCESS_FRAME' && isReady && faceLandmarker) {
        try {
            // Process the image frame (should be VideoFrame, ImageBitmap, or HTMLImageElement)
            // In worker, we usually use ImageBitmap passed from main thread
            const results = faceLandmarker.detectForVideo(image, performance.now());

            if (results.faceLandmarks && results.faceLandmarks.length > 0) {
                postMessage({
                    type: 'RESULT',
                    data: {
                        multiFaceLandmarks: results.faceLandmarks,
                        faceBlendshapes: results.faceBlendshapes
                    }
                });
            } else {
                // IMPORTANT: Always reply to release back-pressure lock
                postMessage({ type: 'EMPTY' });
            }
        } catch (error) {
            console.error('Worker Inference Error:', error);
            postMessage({ type: 'ERROR', error });
        }
    }
};
