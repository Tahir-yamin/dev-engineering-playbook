'use client';

import { userData } from '../data/portfolio';

export default function ProfileConsole() {
    return (
        <div className="w-[900px] h-[650px] glass-panel tech-border-cyan flex flex-col p-6 relative bg-black/40 backdrop-blur-md">

            {/* Top Header */}
            <div className="flex justify-between items-end border-b-2 border-cyber-cyan/30 pb-4 mb-6">
                <div className="flex items-center gap-4">
                    {/* Profile Icon Placeholder */}
                    <div className="w-12 h-12 bg-cyber-cyan/20 border border-cyber-cyan flex items-center justify-center">
                        <span className="text-cyber-cyan font-bold text-xl">TY</span>
                    </div>
                    <div>
                        <h1 className="text-3xl font-medium text-white tracking-widest uppercase font-sans">TAHIR YAMIN</h1>
                        <div className="text-cyber-cyan text-sm tracking-[0.4em] font-bold uppercase">INDUSTRIAL-AI ARCHITECT</div>
                    </div>
                </div>
                <div className="text-right">
                    <div className="text-[10px] text-white/50 uppercase tracking-widest">PROJECTS</div>
                    <div className="flex gap-1 h-3 mt-1">
                        {/* Tiny Progress Bars */}
                        <div className="w-8 h-full bg-cyber-cyan/50"></div>
                        <div className="w-8 h-full bg-cyber-cyan/80"></div>
                        <div className="w-8 h-full bg-cyber-cyan"></div>
                    </div>
                </div>
            </div>

            {/* Main Content Grid */}
            <div className="flex-1 grid grid-cols-12 gap-6">

                {/* Left: Neural Network Visual */}
                <div className="col-span-8 bg-black/30 border border-cyber-cyan/20 relative overflow-hidden p-6 flex items-center justify-center">
                    <div className="absolute top-2 left-2 text-[10px] text-cyber-cyan/60 tracking-widest">NEURAL_DEEP_DIVE :: ACTIVE</div>

                    {/* Stylized Neural Network SVG */}
                    <svg viewBox="0 0 400 300" className="w-full h-full opacity-80 percievel-3d">
                        <defs>
                            <radialGradient id="node-glow" cx="50%" cy="50%" r="50%">
                                <stop offset="0%" stopColor="#00fff9" stopOpacity="0.8" />
                                <stop offset="100%" stopColor="#00fff9" stopOpacity="0" />
                            </radialGradient>
                        </defs>
                        {/* Edges */}
                        <path d="M50 150 L150 50 L250 150 L350 50" stroke="rgba(0,255,249,0.2)" strokeWidth="1" fill="none" />
                        <path d="M50 150 L150 250 L250 150 L350 250" stroke="rgba(0,255,249,0.2)" strokeWidth="1" fill="none" />
                        <path d="M150 50 L250 150 L150 250" stroke="rgba(0,255,249,0.2)" strokeWidth="1" fill="none" />
                        <path d="M250 150 L350 50" stroke="rgba(0,255,249,0.2)" strokeWidth="1" fill="none" />

                        {/* Nodes */}
                        {[...Array(8)].map((_, i) => (
                            <circle key={i} cx={50 + (i * 40)} cy={150 + Math.sin(i) * 100} r="4" fill="white" className="animate-pulse" />
                        ))}
                        <circle cx="150" cy="50" r="6" fill="url(#node-glow)" />
                        <circle cx="250" cy="150" r="8" fill="url(#node-glow)" />
                        <circle cx="350" cy="50" r="6" fill="url(#node-glow)" />
                    </svg>
                </div>

                {/* Right: Charts */}
                <div className="col-span-4 flex flex-col gap-6">

                    {/* Chart 1: Projects Completed */}
                    <div className="flex-1 bg-black/30 border border-cyber-cyan/10 p-4 flex flex-col">
                        <div className="text-[10px] text-white/50 mb-2 uppercase tracking-wider">PROJECTS COMPLETED</div>
                        <div className="flex-1 flex items-end justify-between gap-1">
                            {[30, 45, 25, 60, 80].map((h, i) => (
                                <div key={i} className="w-full bg-cyber-cyan/30 hover:bg-cyber-cyan transition-all duration-300" style={{ height: `${h}%` }}></div>
                            ))}
                        </div>
                    </div>

                    {/* Chart 2: System Efficiency */}
                    <div className="flex-1 bg-black/30 border border-cyber-cyan/10 p-4 flex flex-col">
                        <div className="text-[10px] text-white/50 mb-2 uppercase tracking-wider">SYSTEM EFFICIENCY</div>
                        {/* Line Chart Visual */}
                        <svg viewBox="0 0 100 50" className="w-full h-full overflow-visible">
                            <polyline points="0,50 20,40 40,45 60,20 80,30 100,5" fill="none" stroke="#00fff9" strokeWidth="2" />
                            <polygon points="0,50 20,40 40,45 60,20 80,30 100,5 100,60 0,60" fill="rgba(0,255,249,0.1)" />
                        </svg>
                    </div>

                </div>

            </div>

            {/* Footer Status */}
            <div className="mt-6 flex justify-between text-[10px] uppercase tracking-widest text-cyber-cyan/60">
                <span>SYS.STATUS: OPTIMAL</span>
                <span>SECURE CONNECTION ESTABLISHED</span>
            </div>

        </div>
    );
}
