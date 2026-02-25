'use client';

import React, { useEffect, useState } from 'react';
import { db, AtomicReading } from '@/lib/storage/db';
import { Table, Eye } from 'lucide-react';

export default function DataInspector() {
    const [recentReadings, setRecentReadings] = useState<AtomicReading[]>([]);

    const refreshData = async () => {
        try {
            // Fetch last 5 readings
            const readings = await db.readings
                .orderBy('timestamp')
                .reverse()
                .limit(5)
                .toArray();
            setRecentReadings(readings);
        } catch (error) {
            console.error("Failed to fetch recent readings:", error);
        }
    };

    useEffect(() => {
        refreshData();
        const interval = setInterval(refreshData, 2000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
            <h2 className="flex items-center gap-2 text-sm text-slate-400 mb-4 uppercase tracking-widest">
                <Eye className="w-4 h-4 text-blue-400" /> Raw Data Inspector (Live)
            </h2>

            <div className="overflow-x-auto">
                <table className="w-full text-[10px] font-mono text-slate-400">
                    <thead>
                        <tr className="border-b border-slate-800 text-slate-500 uppercase">
                            <th className="text-left pb-2 font-normal">Timestamp</th>
                            <th className="text-left pb-2 font-normal text-emerald-400">Face (Score/EAR)</th>
                            <th className="text-left pb-2 font-normal text-blue-400">Voice (Vol/Jitter)</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800/50">
                        {recentReadings.map((r, i) => (
                            <tr key={r.id || i} className="group hover:bg-slate-800/20">
                                <td className="py-2 text-slate-500">
                                    {new Date(r.timestamp).toLocaleTimeString()}
                                </td>
                                <td className="py-2">
                                    <span className="text-emerald-500/80">MOTILITY:{r.face.hypomimia_score.toFixed(2)}</span>
                                    <span className="mx-1 opacity-20">|</span>
                                    <span className="text-emerald-500/80">BPM:{r.face.blink_rate.toFixed(0)}</span>
                                    <span className="mx-1 opacity-20">|</span>
                                    <span className="text-[9px] text-emerald-600/60 uppercase">EAR:{r.face.ear?.toFixed(3) || '0.000'}</span>
                                </td>
                                <td className="py-2">
                                    <span className="text-blue-500/80">VOL:{(r.voice.volume * 100).toFixed(1)}%</span>
                                    <span className="mx-1 opacity-20">|</span>
                                    <span className="text-blue-500/80">JITTER:{r.voice.jitter.toFixed(3)}</span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>

                {recentReadings.length === 0 && (
                    <div className="text-center py-6 text-slate-600 italic">
                        No active data streams detected. Start the sensor loop to see raw telemetry.
                    </div>
                )}
            </div>

            <p className="mt-4 text-[9px] text-slate-600 italic">
                * This data is being recorded locally every 1000ms. It strictly resides in your browser's IndexedDB.
            </p>
        </div>
    );
}
