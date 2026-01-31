'use client';

export default function Header() {
    return (
        <header className="border-b border-cyber-cyan/10 bg-black/60 backdrop-blur-xl sticky top-0 z-[1001] monitor-curve-vignette opacity-95">
            <div className="mx-auto px-6 lg:px-10 py-3">
                <div className="flex flex-col lg:flex-row items-center justify-between gap-4">

                    {/* Left: Identity - DENSE TYPOGRAPHY */}
                    <div className="flex items-center gap-4 group">
                        <div className="flex items-baseline gap-3">
                            <h1 className="text-white font-mono font-black tracking-[-0.08em] text-xl lg:text-2xl uppercase text-osd">
                                TAHIR YAMIN
                            </h1>
                            <span className="text-white/20 font-black text-xl">|</span>
                            <span className="text-cyber-cyan font-black font-mono text-[11px] tracking-[0.4em] uppercase drop-shadow-[0_0_8px_rgba(0,255,249,0.3)]">
                                INDUSTRIAL-AI ARCHITECT
                            </span>
                        </div>
                    </div>

                    {/* Center: Live Data Ticker - MOCKUP ALIGNED */}
                    <div className="flex items-center justify-center gap-10 font-mono text-[9px] tracking-[0.3em] font-black">
                        {[
                            { label: 'Agents Active', val: '8', color: 'cyan', textClass: 'text-cyber-cyan/50', bgClass: 'bg-cyber-cyan' },
                            { label: 'Workflows Deployed', val: '200+', color: 'purple', textClass: 'text-cyber-purple/50', bgClass: 'bg-cyber-purple' },
                            { label: 'Yrs Experience', val: '15', color: 'green', textClass: 'text-cyber-green/50', bgClass: 'bg-cyber-green' }
                        ].map(stat => (
                            <div key={stat.label} className="flex flex-col items-center gap-1.5 group">
                                <div className="flex items-center gap-2">
                                    <span className="text-white text-xs text-osd">{stat.val}</span>
                                    <span className={`${stat.textClass} uppercase font-black`}>{stat.label}</span>
                                </div>
                                {/* Visualizer Bars */}
                                <div className="flex gap-0.5 h-1.5">
                                    {[1, 2, 3, 4, 5].map(i => (
                                        <div
                                            key={i}
                                            className={`w-[2px] ${stat.bgClass} opacity-40 group-hover:opacity-100 transition-all`}
                                            style={{ height: `${20 + (i * 15) % 80}%` }}
                                        ></div>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>

                    {/* Right: Cloud Interface Status */}
                    <div className="flex items-center gap-8">
                        <div className="flex items-center gap-4 px-5 py-2 bg-cyber-green/10 border border-cyber-green/40 rounded shadow-[0_0_15px_rgba(57,255,20,0.15)]">
                            <div className="relative">
                                <div className="w-2 h-2 rounded-full bg-cyber-green osd-glow-green"></div>
                                <div className="absolute inset-0 bg-cyber-green blur-[6px] opacity-70 animate-ping"></div>
                            </div>
                            <span className="text-[10px] font-mono text-cyber-green font-black tracking-[0.5em] uppercase">
                                AI COPILOT: <span className="text-white">ONLINE</span>
                            </span>
                        </div>

                        <div className="flex items-center gap-3">
                            <div className="flex flex-col items-end">
                                <span className="text-sm font-black text-white tracking-widest leading-none uppercase text-osd">Gemini</span>
                            </div>
                            <div className="relative w-8 h-8">
                                <div className="absolute inset-0 bg-blue-500/30 blur-[15px]"></div>
                                <svg className="relative z-10 w-full h-full drop-shadow-[0_0_8px_rgba(255,255,255,0.6)]" viewBox="0 0 24 24">
                                    <path d="M12 2L14.5 9.5L22 12L14.5 14.5L12 22L9.5 14.5L2 12L9.5 9.5L12 2Z" fill="url(#main-star-grad)" />
                                    <defs>
                                        <linearGradient id="main-star-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                                            <stop offset="0%" stopColor="#4285F4" />
                                            <stop offset="100%" stopColor="#B026FF" />
                                        </linearGradient>
                                    </defs>
                                </svg>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </header>
    );
}
