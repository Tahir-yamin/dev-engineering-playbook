'use client';

import React from 'react';
import { Brain, ShieldCheck, Activity, Zap, Lock } from 'lucide-react';

export function HeroSection() {
    return (
        <div className="relative overflow-hidden bg-slate-950 pt-16 pb-24 border-b border-white/5">
            {/* Background Glows */}
            <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-emerald-500/10 blur-[120px] rounded-full -mr-64 -mt-64 animate-pulse" />
            <div className="absolute bottom-0 left-0 w-[300px] h-[300px] bg-blue-500/10 blur-[100px] rounded-full -ml-32 -mb-32" />

            <div className="relative z-10 max-w-6xl mx-auto px-8">
                <div className="flex flex-col md:flex-row items-center gap-12">
                    {/* Text Content */}
                    <div className="flex-1 space-y-8 text-center md:text-left">
                        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[10px] font-bold uppercase tracking-widest animate-in fade-in slide-in-from-top-4 duration-700">
                            <Zap className="w-3 h-3 fill-current" />
                            Powered by Gemini 3.0 Pro
                        </div>

                        <h1 className="text-5xl md:text-7xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-br from-white via-white to-slate-500 leading-tight">
                            Silent Health <br />
                            <span className="text-emerald-500">Neuro-Audit</span>
                        </h1>

                        <p className="text-lg text-slate-400 max-w-xl leading-relaxed">
                            Clinical-grade neurological monitoring from your browser.
                            We use multimodal AI to detect subtle tremors, hypomimia, and speech jitter
                            before they become visible to the eye.
                        </p>

                        <div className="flex flex-col sm:flex-row items-center gap-4 justify-center md:justify-start">
                            <div className="flex items-center gap-2 text-xs font-bold text-slate-500">
                                <ShieldCheck className="w-4 h-4 text-emerald-500" />
                                No Video/Audio leaves the device
                            </div>
                            <div className="w-1 h-1 rounded-full bg-slate-800 hidden sm:block" />
                            <div className="flex items-center gap-2 text-xs font-bold text-slate-500">
                                <Lock className="w-4 h-4 text-blue-500" />
                                Anonymized Clinical Vectors
                            </div>
                        </div>
                    </div>

                    {/* Visual Indicators */}
                    <div className="grid grid-cols-2 gap-4 w-full md:w-auto">
                        <div className="p-6 bg-slate-900/40 border border-white/5 rounded-2xl backdrop-blur-sm hover:border-emerald-500/30 transition-all group">
                            <Brain className="w-8 h-8 text-emerald-500 mb-4 group-hover:scale-110 transition-transform" />
                            <div className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">Processing</div>
                            <div className="text-xl font-bold text-white">Edge AI</div>
                        </div>
                        <div className="p-6 bg-slate-900/40 border border-white/5 rounded-2xl backdrop-blur-sm hover:border-blue-500/30 transition-all group">
                            <Activity className="w-8 h-8 text-blue-500 mb-4 group-hover:scale-110 transition-transform" />
                            <div className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">Latency</div>
                            <div className="text-xl font-bold text-white">~33ms</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
