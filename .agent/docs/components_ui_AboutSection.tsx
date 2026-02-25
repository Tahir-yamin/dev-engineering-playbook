'use client';

import React from 'react';
import { Microscope, Database, Globe, UserCheck, Shield } from 'lucide-react';

export function AboutSection() {
    const pillars = [
        {
            icon: <Microscope className="w-5 h-5 text-emerald-400" />,
            title: "Clinical Fidelity",
            desc: "Our algorithms are aligned with UPDRS (Unified Parkinson's Disease Rating Scale) protocols, focusing on high-frequency facial and vocal tremors."
        },
        {
            icon: <Shield className="w-5 h-5 text-blue-400" />,
            title: "Zero-Trust Privacy",
            desc: "Raw video and audio are processed exclusively in your browser's memory. No identifying images ever touch our servers or the Gemini API."
        },
        {
            icon: <Database className="w-5 h-5 text-purple-400" />,
            title: "Ground Truth Data",
            desc: "Silent Health transforms raw sensor noise into structured clinical vectors, creating a permanent research record in your Local Vault."
        }
    ];

    return (
        <section className="bg-slate-900/20 py-24 border-b border-white/5">
            <div className="max-w-6xl mx-auto px-8">
                <div className="flex flex-col lg:flex-row gap-20">
                    {/* Mission */}
                    <div className="lg:w-1/3 space-y-6">
                        <h2 className="text-xs font-bold text-slate-500 uppercase tracking-[0.3em]">The Mission</h2>
                        <h3 className="text-3xl font-bold text-white tracking-tight leading-tight">
                            Bridging the gap between <span className="text-emerald-500">clinic visits</span> and daily life.
                        </h3>
                        <p className="text-slate-400 leading-relaxed text-sm">
                            Silent Health was born from the realization that neurological changes are often most visible in the subtle rhythms of daily activity.
                            By utilizing the high-reasoning capabilities of Gemini 3.0 Pro and on-device WASM-based MediaPipe inference, we provide a non-invasive early-warning system that respects the sanctity of the home and the precision of clinical data.
                        </p>
                    </div>

                    {/* Pillars */}
                    <div className="flex-1 grid md:grid-cols-1 gap-8">
                        {pillars.map((p, i) => (
                            <div key={i} className="flex gap-6 items-start p-6 rounded-2xl bg-white/[0.02] border border-white/[0.05] hover:bg-white/[0.04] transition-colors">
                                <div className="p-3 bg-slate-950 rounded-xl shadow-inner uppercase">
                                    {p.icon}
                                </div>
                                <div>
                                    <h4 className="text-white font-bold mb-1 tracking-tight">{p.title}</h4>
                                    <p className="text-slate-500 text-sm leading-relaxed">{p.desc}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </section>
    );
}
