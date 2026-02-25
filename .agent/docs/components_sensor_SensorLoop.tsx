'use client';

import React, { useEffect, useRef, useState } from 'react';
import Webcam from 'react-webcam';
import { recorder } from '@/lib/recorder';

/**
 * SensorLoop.tsx
 * 
 * RESPONSIBILITY:
 * 1. Manage the Webcam feed.
 * 2. Send frames to real MediaPipe SensorWorker.
 * 3. Receive real facial landmarks and update vault.
 */

interface SensorLoopProps {
    onStatusChange?: (status: 'OFF' | 'DEMO' | 'LIVE') => void;
    isMonitoring?: boolean;
    onToggleMonitoring?: (val: boolean) => void;
}

export default function SensorLoop({
    onStatusChange,
    isMonitoring = true,
    onToggleMonitoring
}: SensorLoopProps) {
    const webcamRef = useRef<Webcam>(null);
    const workerRef = useRef<Worker>(null);
    const requestRef = useRef<number | null>(null);
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const [status, setStatus] = useState<'INIT' | 'READY' | 'ERROR'>('INIT');

    // BACK-PRESSURE: Only process one frame at a time
    const frameCount = useRef(0);
    const lastUpdate = useRef(performance.now());
    const [debugStats, setDebugStats] = useState("WAITING...");

    // BACK-PRESSURE: Only process one frame at a time
    const isWorkerBusy = useRef(false);

    const [isVisible, setIsVisible] = useState(true);

    useEffect(() => {
        if (!isMonitoring) {
            // Kill worker if monitoring is off
            workerRef.current?.terminate();
            workerRef.current = null;
            setStatus('INIT');
            setDebugStats("OFFLINE");

            // SECURITY: Clear buffer so no "ghost data" remains
            recorder.reset();
            return;
        }

        // Initialize worker
        try {
            workerRef.current = new Worker(new URL('./SensorWorker.ts', import.meta.url));

            workerRef.current.onmessage = (event) => {
                const { type, data, error } = event.data;

                if (type === 'READY') {
                    console.log("📹 SensorLoop: Worker Ready");
                    setStatus('READY');
                    isWorkerBusy.current = false;
                    setDebugStats("READY");
                    onStatusChange?.('LIVE'); // Notify parent that camera is LIVE
                }

                if (type === 'RESULT') {
                    lastResultTime.current = performance.now();
                    // UNLOCK: Worker finished, ready for next frame
                    isWorkerBusy.current = false;
                    frameCount.current++;

                    // Update FPS every 30 frames
                    if (frameCount.current % 30 === 0) {
                        const now = performance.now();
                        const fps = Math.round(30 / ((now - lastUpdate.current) / 1000));
                        const totalFrames = frameCount.current;
                        setDebugStats(`${fps} FPS | ${totalFrames}F`);
                        lastUpdate.current = now;
                    }

                    // results from MediaPipe
                    recorder.onVision(data);

                    // Update ref for the decoupled drawing loop
                    latestLandmarks.current = data.multiFaceLandmarks[0];
                }

                if (type === 'EMPTY') {
                    lastResultTime.current = performance.now();
                    // UNLOCK: No face found, but we must release the lock to try again
                    isWorkerBusy.current = false;
                    if (canvasRef.current) {
                        const ctx = canvasRef.current.getContext('2d');
                        ctx?.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);

                        // Add subtle "No Face" indicator
                        if (ctx) {
                            ctx.fillStyle = 'rgba(239, 68, 68, 0.4)';
                            ctx.font = '10px monospace';
                            ctx.fillText('NO FACE DETECTED', 10, 20);
                        }
                    }

                    if (frameCount.current % 30 === 0) {
                        setDebugStats(`NO FACE | ${frameCount.current} F`);
                    }
                    frameCount.current++;
                }

                if (type === 'ERROR') {
                    console.error("📹 SensorLoop: Worker Error", error);
                    setStatus('ERROR');
                    isWorkerBusy.current = false;
                    setDebugStats("ERR: REBOOTING...");

                    // Auto-reboot worker if it fails
                    setTimeout(() => {
                        onToggleMonitoring?.(false);
                        setTimeout(() => onToggleMonitoring?.(true), 1000);
                    }, 5000);
                }
            };
        } catch (err) {
            console.error("📹 SensorLoop: Failed to init worker", err);
            setStatus('ERROR');
            setDebugStats("INIT FAIL");
        }

        return () => workerRef.current?.terminate();
    }, [isMonitoring, status]); // Re-run if monitoring toggles

    const latestLandmarks = useRef<any[] | null>(null);
    const isDrawing = useRef(false);

    // DRAW LOOP: Decoupled from processing loop to ensure 60fps UI
    const drawLoop = () => {
        if (!isDrawing.current || !canvasRef.current) return;

        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d'); // Use default alpha: true for transparency
        if (!ctx) return;

        if (!latestLandmarks.current) {
            requestAnimationFrame(drawLoop);
            return;
        }

        const landmarks = latestLandmarks.current;

        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // CONFIG: High-Tech Emerald Style
        const primaryColor = '#34d399';
        ctx.fillStyle = primaryColor;
        ctx.strokeStyle = '#34d39966';
        ctx.lineWidth = 1;

        // OPTIMIZATION: Batch Path for Points
        // Using rect() instead of arc() allows drawing 478 points at 60fps without lag
        ctx.beginPath();
        for (let i = 0; i < landmarks.length; i++) {
            const p = landmarks[i];
            const x = Math.floor(p.x * canvas.width);
            const y = Math.floor(p.y * canvas.height);
            ctx.rect(x, y, 2, 2); // 2x2 px square (looks like dot)
        }
        ctx.fill();

        // OPTIMIZATION: Batch Path for Lines
        // Restored FULL DENSITY (skip=0) as requested by user
        ctx.beginPath();
        for (let i = 0; i < landmarks.length; i++) {
            const p = landmarks[i];
            const x = Math.floor(p.x * canvas.width);
            const y = Math.floor(p.y * canvas.height);
            ctx.moveTo(x, y);

            // Connect to nearby points to form mesh
            const nextIdx = (i + 1) % landmarks.length; // Simple connection
            const nextP = landmarks[nextIdx];
            ctx.lineTo(Math.floor(nextP.x * canvas.width), Math.floor(nextP.y * canvas.height));

            // Cross-connections for "Mesh" look (every 7th point)
            if (i % 7 === 0) {
                const crossIdx = (i + 23) % landmarks.length;
                const crossP = landmarks[crossIdx];
                ctx.lineTo(Math.floor(crossP.x * canvas.width), Math.floor(crossP.y * canvas.height));
            }
        }
        ctx.stroke();

        requestAnimationFrame(drawLoop);
    };

    // Start/Stop Drawing Loop based on monitoring status
    useEffect(() => {
        if (isMonitoring && status === 'READY') {
            isDrawing.current = true;
            requestAnimationFrame(drawLoop);
        } else {
            isDrawing.current = false;
        }
        return () => { isDrawing.current = false; };
    }, [isMonitoring, status]);

    const lastResultTime = useRef(performance.now());
    const lastProcessTime = useRef(0); // THROTTLE: Track last processing time
    const rebootCount = useRef(0);

    const captureFrame = async () => {
        if (!isMonitoring) return;

        // WATCHDOG: If we haven't had a result in 30s while monitoring, reboot the worker.
        // Increased from 10s -> 30s to allow for slow XNNPACK CPU initialization on some devices.
        const now = performance.now();
        // WATCHDOG: Increased to 45s to handle slow initial WASM load on some devices
        if (status === 'READY' && isMonitoring && now - lastResultTime.current > 45000 && rebootCount.current < 3) {
            console.warn(`🚨 [SENSOR] Watchdog triggered - Worker hang detected (${Math.round((now - lastResultTime.current) / 1000)}s). Rebooting...`);
            lastResultTime.current = now; // Prevent instant re-trigger
            rebootCount.current++;
            // Internal reboot logic
            workerRef.current?.terminate();
            workerRef.current = null;
            setStatus('INIT');
            setTimeout(() => onToggleMonitoring?.(true), 2000);
            return;
        }

        if (
            status === 'READY' &&
            !isWorkerBusy.current &&
            workerRef.current &&
            webcamRef.current &&
            webcamRef.current.video &&
            webcamRef.current.video.readyState === 4
        ) {
            const video = webcamRef.current.video;

            try {
                // THROTTLE: Limit to ~15 FPS (66ms) to free up Main Thread
                if (now - lastProcessTime.current > 66) {
                    isWorkerBusy.current = true;
                    lastProcessTime.current = now;

                    // OPTIMIZATION: Aggressive downscale for CPU inference.
                    // 240px is sufficient for face mesh but 4x faster than 480px.
                    const bitmap = await createImageBitmap(video, { resizeWidth: 240 });
                    workerRef.current.postMessage({ type: 'PROCESS_FRAME', image: bitmap }, [bitmap]);
                }
            } catch (err) {
                isWorkerBusy.current = false;
            }
        }
        requestRef.current = requestAnimationFrame(captureFrame);
    };

    useEffect(() => {
        if (status === 'READY' && isMonitoring) {
            lastResultTime.current = performance.now();
            rebootCount.current = 0;
            requestRef.current = requestAnimationFrame(captureFrame);
        }
        return () => {
            if (requestRef.current) cancelAnimationFrame(requestRef.current);
        };
    }, [status, isMonitoring]);

    // ALWAYS RENDER: Do not hide component when off, so user can re-enable it.
    // if (!isMonitoring && !isVisible) return null; 

    return (
        <div className="fixed bottom-4 right-4 z-50 group">
            {/* Main Portal Container */}
            <div className={`relative rounded-2xl overflow-hidden border-2 transition-all duration-500 shadow-2xl bg-black ${isVisible ? 'w-64 h-48 border-emerald-500/50' : 'w-12 h-12 border-slate-700 hover:border-emerald-500/50 cursor-pointer bg-slate-900 flex items-center justify-center'
                }`} onClick={() => !isVisible && setIsVisible(true)}>

                {!isVisible ? (
                    <div className={`animate-pulse text-xs font-black ${isMonitoring ? 'text-emerald-500' : 'text-red-500'}`}>
                        {isMonitoring ? 'LIVE' : 'OFF'}
                    </div>
                ) : (
                    <>
                        {isMonitoring ? (
                            <>
                                <Webcam
                                    ref={webcamRef}
                                    audio={false}
                                    className="absolute inset-0 w-full h-full object-cover"
                                    videoConstraints={{
                                        facingMode: "user"
                                    }}
                                />
                                <canvas
                                    ref={canvasRef}
                                    width={256}
                                    height={192}
                                    className="absolute inset-0 w-full h-full"
                                />
                                {/* Debug Stats Overlay */}
                                <div className="absolute bottom-1 right-1 px-1 py-0.5 bg-black/50 text-[6px] font-mono text-emerald-400 pointer-events-none">
                                    {debugStats}
                                </div>
                            </>
                        ) : (
                            <div className="absolute inset-0 flex items-center justify-center bg-slate-900 text-slate-500 font-mono text-xs">
                                [SENSOR OFFLINE]
                            </div>
                        )}

                        {/* Header Controls */}
                        <div className="absolute top-0 left-0 right-0 p-2 flex justify-between items-start bg-gradient-to-b from-black/80 to-transparent z-10">
                            <div className="px-1.5 py-0.5 bg-emerald-500 text-[8px] font-black text-white rounded uppercase tracking-tighter shadow-emerald-500/20 shadow-lg">
                                Biomarker Stream
                            </div>
                            <div className="flex gap-2">
                                {/* Calibrate Button */}
                                <button
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        recorder.reset();
                                        // Brief visual feedback could be added here
                                        // Simple visual feedback could be added, but console log is in recorder
                                    }}
                                    className="text-white/50 hover:text-cyan-400 transition-colors"
                                    title="Calibrate (Reset Sensors)"
                                >
                                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
                                </button>

                                {/* Power Button */}
                                <button
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        onToggleMonitoring?.(!isMonitoring);
                                    }}
                                    className={`transition-colors ${isMonitoring ? 'text-white/50 hover:text-red-500' : 'text-red-500 hover:text-emerald-400'}`}
                                    title={isMonitoring ? "Disable Sensor" : "Enable Sensor"}
                                >
                                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                                </button>
                                {/* Minify Button */}
                                <button
                                    onClick={(e) => { e.stopPropagation(); setIsVisible(false); }}
                                    className="text-white/50 hover:text-white transition-colors"
                                >
                                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg>
                                </button>
                            </div>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
}
