'use client';

import { useEffect, useRef, useState } from 'react';


/**
 * AudioLoop.tsx
 * 
 * RESPONSIBILITY:
 * 1. Listen for Voice Activity (VAD).
 * 2. Extract Audio Features (Jitter/Shimmer/MFCC) locally.
 * 3. Does NOT record raw audio (Privacy).
 */

export default function AudioLoop({
    onFeature,
    onAudioLevel,
    disabled = false
}: {
    onFeature: (features: { volume: number, jitter: number }) => void;
    onAudioLevel?: (level: number) => void;
    disabled?: boolean;
}) {
    const [listening, setListening] = useState(false);

    const handlersRef = useRef({ onFeature, onAudioLevel });
    useEffect(() => {
        handlersRef.current = { onFeature, onAudioLevel };
    }, [onFeature, onAudioLevel]);

    const contextRef = useRef<AudioContext | null>(null);
    const streamRef = useRef<MediaStream | null>(null);

    useEffect(() => {
        if (disabled) {
            contextRef.current?.close();
            streamRef.current?.getTracks().forEach(track => track.stop());
            setListening(false);
            return;
        }

        const startAudio = async () => {
            try {
                // 1. Get Microphone
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                streamRef.current = stream;

                const context = new AudioContext();
                contextRef.current = context;

                // 2. Load AudioWorklet
                await context.audioWorklet.addModule('/audio-processor.js');

                const source = context.createMediaStreamSource(stream);
                const workletNode = new AudioWorkletNode(context, 'audio-processor');

                workletNode.port.onmessage = (event) => {
                    const { rms, zcr } = event.data;
                    const { onAudioLevel: cbAudio, onFeature: cbFeature } = handlersRef.current;
                    cbAudio?.(rms || 0);
                    cbFeature({
                        volume: rms,
                        jitter: zcr
                    });
                };

                source.connect(workletNode);
                // Note: Worklet nodes don't necessarily need to connect to destination 
                // unless we want to hear the feedback.

                // Chrome Security: AudioContext starts suspended until interaction
                if (context.state === 'suspended') {
                    await context.resume();
                }

                setListening(true);
            } catch (err) {
                console.error("❌ Audio Access Denied or Hardware Error:", err);
            }
        };

        startAudio().catch(e => console.error("🔇 Audio Startup Exception:", e));

        return () => {
            contextRef.current?.close();
            streamRef.current?.getTracks().forEach(track => track.stop());
        };
    }, [disabled]);

    return (
        <div className="hidden">
            {/* Audio Processor Active: {listening ? 'ON' : 'OFF'} */}
        </div>
    );
}
