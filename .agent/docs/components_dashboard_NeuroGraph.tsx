'use client';

import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Activity } from 'lucide-react';

/**
 * NeuroGraph.tsx
 * 
 * RESPONSIBILITY:
 * Visualize the 30Hz "Clinical Signal" stream.
 * Shows the "Hypomimia Score" (Jaw/Smile variance) over time.
 */

interface SignalPoint {
    time: string;
    hypomimia: number; // 0-100
    blinkRate: number; // 0-30
}

interface NeuroGraphProps {
    data: SignalPoint[];
}

export default function NeuroGraph({ data }: NeuroGraphProps) {
    if (!data || data.length === 0) {
        return (
            <div className="flex items-center justify-center h-full text-slate-600 text-xs animate-pulse">
                <Activity className="w-4 h-4 mr-2" /> WAITING FOR BIOSIGNAL...
            </div>
        );
    }

    return (
        <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis
                    dataKey="time"
                    hide={true}
                />
                <YAxis
                    domain={[0, 100]}
                    tick={{ fill: '#64748b', fontSize: 10 }}
                    axisLine={false}
                    tickLine={false}
                />
                <Tooltip
                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b' }}
                    itemStyle={{ fontSize: '11px' }}
                />
                <Line
                    type="monotone"
                    dataKey="hypomimia"
                    stroke="#10b981"
                    strokeWidth={2}
                    dot={false}
                    isAnimationActive={false} // Performance optimization for real-time
                />
                <Line
                    type="step"
                    dataKey="blinkRate"
                    stroke="#3b82f6"
                    strokeWidth={1}
                    dot={false}
                    strokeDasharray="5 5"
                />
            </LineChart>
        </ResponsiveContainer>
    );
}
