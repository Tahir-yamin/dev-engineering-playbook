'use client';

import React, { useMemo } from 'react';
import { SessionSummary } from '@/lib/storage/db';
import {
    AreaChart,
    Area,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    Brush
} from 'recharts';
import { Activity, AlertTriangle, CheckCircle2 } from 'lucide-react';

interface LongitudinalTrendsProps {
    sessions: SessionSummary[];
}

const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
        const data = payload[0].payload;
        return (
            <div className={`bg-slate-950/90 border ${data.isMisclassified ? 'border-orange-500/50' : data.isRealAlert ? 'border-red-500/50' : 'border-emerald-500/30'} p-4 rounded-xl shadow-[0_0_20px_rgba(16,185,129,0.1)] backdrop-blur-xl`}>
                <p className="text-[10px] font-bold text-slate-500 uppercase tracking-[0.2em] mb-3 border-b border-white/5 pb-2">{data.timestamp}</p>
                <div className="space-y-2">
                    <div className="flex justify-between items-end gap-6">
                        <span className="text-slate-400 text-xs">Clinical Risk</span>
                        <span className={`text-lg font-black leading-none ${data.risk_score > 60 ? 'text-red-400' : 'text-emerald-400'}`}>
                            {data.risk_score}<span className="text-[10px] opacity-50 ml-0.5">%</span>
                        </span>
                    </div>

                    {data.isMisclassified && (
                        <div className="flex items-center gap-2 px-2 py-1 rounded bg-orange-500/10 border border-orange-500/20">
                            <AlertTriangle className="w-3 h-3 text-orange-400" />
                            <span className="text-[9px] font-black text-orange-400 uppercase tracking-tighter">
                                {data.isAutoFiltered ? 'Auto Filter' : 'Clinician Override'}
                            </span>
                        </div>
                    )}

                    <div className="flex justify-between items-center gap-6 pt-1">
                        <span className="text-slate-400 text-xs text-nowrap">Session Mode</span>
                        <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${data.isRealAlert
                            ? 'bg-red-500/20 text-red-100 border-red-500/30'
                            : data.isMisclassified
                                ? 'bg-orange-500/20 text-orange-400 border-orange-500/30'
                                : 'bg-slate-800 text-blue-400 border-blue-500/20'
                            }`}>
                            {data.label}
                        </span>
                    </div>
                </div>
            </div>
        );
    }
    return null;
};

export function LongitudinalTrends({ sessions }: LongitudinalTrendsProps) {
    const [mounted, setMounted] = React.useState(false);
    const [filters, setFilters] = React.useState({
        stable: true,
        alert: true,
        misclassified: true
    });


    React.useEffect(() => {
        setMounted(true);
    }, []);

    // 1. Process all sessions into base data
    const allProcessedData = useMemo(() => {
        if (!mounted || !sessions || sessions.length === 0) return [];


        return [...sessions]
            .filter(s => s && s.neuro_report)
            .map(s => {
                const report = s.neuro_report!;
                const metrics = report.metrics?.current;

                // Robust numeric parsing: Ensure score is always a finite number
                const rawScore = Number(report.risk_score);
                const score = !isNaN(rawScore) && isFinite(rawScore) ? rawScore : 0;

                const label = s.session_label || 'UNLABELED';
                const isHighRisk = score > 60;
                const isGroundTruth = label === 'BASELINE' || label === 'SIMULATED';
                const isFalse = label === 'FALSE_POSITIVE' || label === 'FALSE_NEGATIVE';
                const isAutoFiltered = report.anomalies?.includes("Autonomous Noise Rejection (Sensor Artifact)");

                const isRealAlert = isHighRisk && !isGroundTruth && !isFalse && !isAutoFiltered;
                const isMisclassified = (isFalse || isAutoFiltered) && isHighRisk;
                const isStable = !isRealAlert && !isMisclassified;

                return {
                    id: s.id,
                    date: s.date || new Date().toISOString(),
                    timestamp: s.date ? new Date(s.date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : 'N/A',
                    risk_score: score,
                    hypomimia: Number(metrics?.hypomimia) || 0,
                    jitter: Number(metrics?.jitter) || 0,
                    label: label,
                    isRealAlert,
                    isMisclassified,
                    isStable,
                    isAutoFiltered
                };
            })
            .sort((a, b) => {
                const timeA = new Date(a.date).getTime();
                const timeB = new Date(b.date).getTime();
                // Safe sort: Handle invalid dates by forcing them to the beginning
                if (isNaN(timeA) && isNaN(timeB)) return 0;
                if (isNaN(timeA)) return -1;
                if (isNaN(timeB)) return 1;
                return timeA - timeB;
            });
    }, [sessions]);

    // 2. Apply Filters
    const filteredData = useMemo(() => {
        return allProcessedData.filter(d => {
            if (d.isRealAlert && !filters.alert) return false;
            if (d.isMisclassified && !filters.misclassified) return false;
            if (d.isStable && !filters.stable) return false;
            return true;
        });
    }, [allProcessedData, filters]);

    // 3. (Removed) Manual Slicing - Pass all filtered data to chart and let Brush handle the view
    // The chart will now render all data but zoom into the Brush's range by default if needed, 
    // or show all. For best UX with Brush, we pass the full dataset.

    if (!mounted || !sessions || sessions.length === 0) {
        return (
            <div className={`p-8 rounded-3xl bg-slate-900/40 border border-white/5 flex flex-col items-center justify-center text-center space-y-4 min-h-[300px] transition-opacity duration-500 ${mounted ? 'opacity-100' : 'opacity-0'}`}>
                <Activity className="w-12 h-12 text-slate-700 animate-pulse" />
                <p className="text-slate-500 font-medium">
                    {!mounted ? 'Calibrating Viewport...' : 'Insufficient data for longitudinal analysis.'}
                    <br />
                    {mounted && 'Run multiple audits to build your trendline.'}
                </p>
            </div>
        );
    }

    return (
        <div className="space-y-8 py-4">
            <style jsx global>{`
                @keyframes clinical-blink {
                    0%, 100% { opacity: 1; transform: scale(1); filter: drop-shadow(0 0 15px rgba(239, 68, 68, 0.8)); }
                    50% { opacity: 0.6; transform: scale(1.15); filter: drop-shadow(0 0 25px rgba(239, 68, 68, 1)); }
                }
                .alert-blink {
                    animation: clinical-blink 1s ease-in-out infinite;
                    transform-origin: center;
                }
                /* Custom Brush Styling */
                .recharts-brush-slide {
                    fill: #1e293b !important; /* Slate 800 */
                    opacity: 0.5;
                }
                .recharts-brush-traveller {
                    fill: #10b981 !important; /* Emerald 500 */
                }
                .recharts-brush-text {
                    fill: #94a3b8 !important; /* Slate 400 */
                    font-size: 10px;
                }
            `}</style>

            <div className="flex flex-col xl:flex-row xl:items-end justify-between px-2 gap-6">
                <div>
                    <div className="flex items-center gap-2 mb-1">
                        <div className="w-1.5 h-6 bg-emerald-500 rounded-full" />
                        <h3 className="text-3xl font-black text-white tracking-tighter uppercase italic">Longitudinal Audit</h3>
                    </div>
                    <p className="text-[10px] font-black text-slate-500 uppercase tracking-[0.3em] flex items-center gap-2">
                        <Activity className="w-3 h-3 text-emerald-500" /> {filteredData.length} Sessions Available
                    </p>
                </div>

                <div className="flex flex-wrap items-center gap-6">
                    {/* Category Filters */}
                    <div className="flex gap-2">
                        <button
                            onClick={() => setFilters(f => ({ ...f, stable: !f.stable }))}
                            className={`flex items-center gap-2 px-3 py-1.5 rounded-full border transition-all ${filters.stable ? 'bg-emerald-500/20 border-emerald-500/40 text-emerald-400' : 'bg-slate-900/50 border-slate-800 text-slate-600'}`}
                        >
                            <div className={`w-2 h-2 rounded-full ${filters.stable ? 'bg-emerald-500' : 'bg-slate-700'}`} />
                            <span className="text-[9px] font-black uppercase tracking-widest">Stable</span>
                        </button>

                        <button
                            onClick={() => setFilters(f => ({ ...f, alert: !f.alert }))}
                            className={`flex items-center gap-2 px-3 py-1.5 rounded-full border transition-all ${filters.alert ? 'bg-red-500/20 border-red-500/40 text-red-400' : 'bg-slate-900/50 border-slate-800 text-slate-600'}`}
                        >
                            <div className={`w-2 h-2 rounded-full ${filters.alert ? 'bg-red-500' : 'bg-slate-700'}`} />
                            <span className="text-[9px] font-black uppercase tracking-widest">Alerts</span>
                        </button>

                        <button
                            onClick={() => setFilters(f => ({ ...f, misclassified: !f.misclassified }))}
                            className={`flex items-center gap-2 px-3 py-1.5 rounded-full border transition-all ${filters.misclassified ? 'bg-orange-500/20 border-orange-500/40 text-orange-400' : 'bg-slate-900/50 border-slate-800 text-slate-600'}`}
                        >
                            <div className={`w-2 h-2 rounded-full ${filters.misclassified ? 'bg-orange-500' : 'bg-slate-700'}`} />
                            <span className="text-[9px] font-black uppercase tracking-widest">Overrides</span>
                        </button>
                    </div>
                </div>
            </div>

            <div className="relative">
                <div className="h-[400px] w-full bg-[#020617]/50 border border-white/5 rounded-[2.5rem] p-8 backdrop-blur-md relative group overflow-hidden">
                    <div className="absolute top-0 right-0 w-96 h-96 bg-emerald-500/5 blur-[120px] rounded-full -mr-32 -mt-32 transition-opacity group-hover:opacity-100 opacity-50 pointer-events-none" />

                    {filteredData.length === 0 ? (
                        <div className="h-full flex flex-col items-center justify-center text-slate-700 space-y-4">
                            <Activity className="w-12 h-12 opacity-10 animate-pulse" />
                            <p className="text-[10px] font-black uppercase tracking-[0.3em]">No matching sessions in this view</p>
                        </div>
                    ) : (
                        <ResponsiveContainer width="99%" height="100%" debounce={50}>
                            <AreaChart data={filteredData} margin={{ top: 20, right: 30, left: 10, bottom: 40 }}>
                                <defs>
                                    <linearGradient id="colorRisk" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#10b981" stopOpacity={0.2} />
                                        <stop offset="50%" stopColor="#10b981" stopOpacity={0.05} />
                                        <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="#ffffff05" vertical={false} />
                                <XAxis
                                    dataKey="id"
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{ fill: '#475569', fontSize: 10, fontWeight: '900' }}
                                    tickFormatter={(id) => {
                                        const payload = filteredData.find(d => d.id === id);
                                        return payload ? payload.timestamp : '';
                                    }}
                                    dy={10}
                                />
                                <YAxis
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{ fill: '#475569', fontSize: 10, fontWeight: '900' }}
                                    domain={[0, 100]}
                                    ticks={[0, 25, 50, 75, 100]}
                                />
                                <Tooltip
                                    content={<CustomTooltip />}
                                    cursor={{ stroke: '#10b981', strokeWidth: 1, strokeDasharray: '4 4' }}
                                />

                                <Area
                                    type="linear"
                                    dataKey="risk_score"
                                    stroke="#10b981"
                                    strokeWidth={3}
                                    fill="url(#colorRisk)"
                                    isAnimationActive={false}
                                    connectNulls={true}
                                    dot={(props: any) => {
                                        const { cx, cy, payload } = props;
                                        if (!cx || !cy) return null;
                                        const dotId = `dot-${payload.id}`;
                                        if (payload.isMisclassified) {
                                            return (
                                                <g key={dotId}>
                                                    <circle cx={cx} cy={cy} r={8} fill="transparent" stroke="#f97316" strokeWidth={2} strokeDasharray="4 2" />
                                                    <circle cx={cx} cy={cy} r={4} fill="#f97316" />
                                                </g>
                                            );
                                        }
                                        if (payload.isRealAlert) {
                                            return (
                                                <g key={dotId} className="alert-blink">
                                                    <circle cx={cx} cy={cy} r={10} fill="#ef444420" />
                                                    <circle cx={cx} cy={cy} r={6} fill="#ef4444" stroke="#ffffff" strokeWidth={2} />
                                                </g>
                                            );
                                        }
                                        return <circle key={dotId} cx={cx} cy={cy} r={4} fill="#10b981" stroke="#ffffff30" strokeWidth={1} />;
                                    }}
                                    activeDot={{ r: 8, stroke: '#fff', strokeWidth: 2, fill: '#10b981' }}
                                />

                                <Brush
                                    dataKey="id"
                                    height={30}
                                    stroke="#10b981"
                                    fill="#0f172a"
                                    tickFormatter={() => ''} /* Hide ticks in brush for cleaner look */
                                    className="text-[10px]"
                                />
                            </AreaChart>
                        </ResponsiveContainer>
                    )}
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 rounded-2xl bg-white/[0.02] border border-white/[0.05]">
                    <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Last Analysis</div>
                    <div className="text-2xl font-black text-white">{filteredData.length > 0 ? filteredData[filteredData.length - 1].risk_score : 0}%</div>
                    <div className="text-[10px] font-bold text-emerald-500 uppercase mt-1 flex items-center gap-1">
                        <CheckCircle2 className="w-3 h-3" /> Stable Trend
                    </div>
                </div>
                <div className="p-4 rounded-2xl bg-white/[0.02] border border-white/[0.05]">
                    <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Clinical Alerts</div>
                    <div className="text-2xl font-black text-red-500">{filteredData.filter(d => d.isRealAlert).length}</div>
                    <div className="text-[10px] font-bold text-slate-400 uppercase mt-1">Confirmed Findings</div>
                </div>
                <div className="p-4 rounded-2xl bg-white/[0.02] border border-white/[0.05]">
                    <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Misclassifications</div>
                    <div className="text-2xl font-black text-orange-500">{filteredData.filter(d => d.isMisclassified).length}</div>
                    <div className="text-[10px] font-bold text-slate-400 uppercase mt-1">Clinician Overrides</div>
                </div>
            </div>
        </div>
    );
}
