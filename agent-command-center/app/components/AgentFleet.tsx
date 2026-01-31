'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

export default function AgentFleet() {
    const agents = [
        { name: 'FRONTEND-SPECIALIST', status: 'ACTIVE', msg: 'MONITORING UI STATE', memory: '0x7F4A', color: 'cyber-cyan', bgClass: 'bg-cyber-cyan' },
        { name: 'BACKEND-ARCHITECT', status: 'ACTIVE', msg: 'OPTIMIZING API ROUTES', memory: '0x1A2C', color: 'cyber-cyan', bgClass: 'bg-cyber-cyan' },
        { name: 'MOBILE-DEVELOPER', status: 'STANDBY', msg: 'READY', memory: '0xE8B9', color: 'white/40', bgClass: 'bg-white' },
        { name: 'DATABASE-OPTIMIZER', status: 'ACTIVE', msg: 'INDEXING TABLES', memory: '0xCC42', color: 'cyber-cyan', bgClass: 'bg-cyber-cyan' },
        { name: 'SECURITY-ANALYZER', status: 'ENGAGED', msg: 'HEURISTIC ANALYSIS', memory: '0x3D91', color: 'cyber-purple', bgClass: 'bg-cyber-purple' },
        { name: 'API-GATEWAY-MGR', status: 'ACTIVE', msg: 'TRAIN ROUTING OPS', memory: '0x992F', color: 'cyber-cyan', bgClass: 'bg-cyber-cyan' },
        { name: 'CLOUD-INFRA-BOT', status: 'DEPLOYING', msg: 'SCALING PODS', memory: '0xFF01', color: 'cyber-green', bgClass: 'bg-cyber-green' },
        { name: 'ML-ENGINEER', status: 'TRACKING', msg: 'WAITING FOR INPUT', memory: '0x00A0', color: 'cyber-cyan', bgClass: 'bg-cyber-cyan' },
    ];

    return (
        <div className="font-mono h-full flex flex-col p-2">
            <div className="flex items-center justify-between mb-8 border-b-2 border-white/10 pb-2">
                <div className="flex flex-col">
                    <h2 className="text-sm font-black text-white tracking-[0.4em] uppercase text-osd">Agent Fleet</h2>
                    <span className="text-[8px] text-white/30 tracking-widest">OSD_CLUSTER: ACTIVE</span>
                </div>
                <div className="text-[9px] font-bold text-white/20 uppercase tracking-tighter">V5.0-PRO-CORE</div>
            </div>

            <div className="flex-1 space-y-4 overflow-y-auto no-scrollbar pr-2">
                {agents.map((agent, i) => (
                    <div key={agent.name} className="relative group cursor-pointer">
                        <div className="flex items-center justify-between">
                            <div className="flex flex-col gap-0.5">
                                <div className="flex items-center gap-3">
                                    <div className="text-[10px] font-black text-white tracking-tight group-hover:text-cyber-cyan transition-colors">
                                        {agent.name}
                                    </div>
                                    <div className="h-[2px] w-8 bg-white/5 overflow-hidden">
                                        <div className={`h-full ${agent.bgClass} vu-bar`} style={{ animationDelay: `${i * 0.1}s` }}></div>
                                    </div>
                                </div>
                                <div className="text-[8px] font-bold text-white/30 uppercase tracking-widest">{agent.msg}</div>
                            </div>

                            <div className="flex flex-col items-end gap-1">
                                <div className={`px-2 py-0.5 border text-[8px] font-black tracking-[0.1em] text-white transition-all transform group-hover:scale-105 ${agent.status === 'ACTIVE' ? 'bg-cyber-cyan/30 border-cyber-cyan shadow-[0_0_8px_#00fff9]' :
                                    agent.status === 'STANDBY' ? 'bg-white/5 border-white/20 opacity-40' :
                                        'bg-cyber-purple/30 border-cyber-purple shadow-[0_0_8px_#b026ff]'
                                    }`}>
                                    [{agent.status}]
                                </div>
                                <span className="text-[8px] font-mono text-white/10">{agent.memory}</span>
                            </div>
                        </div>
                        {/* Interactive glow line on hover */}
                        <div className="absolute -left-2 -right-2 bottom-0 h-px bg-cyber-cyan/0 group-hover:bg-gradient-to-r group-hover:from-transparent group-hover:via-cyber-cyan/40 group-hover:to-transparent transition-all"></div>
                    </div>
                ))}
            </div>

            {/* Bottom Status Ticker */}
            <div className="mt-8 pt-6 border-t border-white/10">
                <div className="text-[9px] font-black text-white/40 uppercase mb-4 tracking-[0.2em]">Live Status Monitor</div>
                <div className="bg-black/80 border border-white/10 rounded-sm p-3 flex items-center justify-between group overflow-hidden relative">
                    <span className="text-[9px] font-bold text-cyber-cyan tracking-[0.1em] z-10">ACTIVE CORES: 12 PROCESSES</span>
                    <div className="flex gap-1 h-3 z-10">
                        {[1, 2, 3, 4, 5, 6, 7].map(i => (
                            <div key={i} className="w-[3px] bg-cyber-cyan/30 vu-bar" style={{ animationDelay: `${i * 0.05}s` }}></div>
                        ))}
                    </div>
                    {/* Inner pulse */}
                    <div className="absolute inset-0 bg-cyber-cyan/5 opacity-0 group-hover:opacity-100 transition-opacity animate-pulse"></div>
                </div>
            </div>
        </div>
    );
}
