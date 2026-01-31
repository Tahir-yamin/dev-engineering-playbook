'use client';

const mainSkills = [
    { name: 'INDUSTRIAL PM', level: 85, color: 'from-cyber-cyan/40 to-cyber-blue', yrs: '12 yrs', tech: ['msp', 'p6', 'sap'] },
    { name: 'FULL-STACK DEV', level: 93, color: 'from-cyber-purple/40 to-cyber-pink', yrs: '13 yrs', tech: ['react', 'next', 'node'] },
    { name: 'AI ENGINEERING', level: 88, color: 'from-cyber-green/40 to-cyber-teal', yrs: '8 yrs', tech: ['python', 'torch', 'rag'] },
    { name: 'AGENT ARCHITECTURE', level: 92, color: 'from-cyber-blue/40 to-cyber-purple', yrs: '5 yrs', tech: ['lang', 'auth', 'cloud'] },
];

const TechIcon = ({ type }: { type: string }) => {
    const icons: Record<string, React.ReactNode> = {
        react: <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />,
        next: <path d="M12 2L2 7v10l10 5 10-5V7L12 2zm0 18l-8-4V8l8-4 8 4v8l-8 4z" />,
        node: <path d="M12 2L4 7v10l8 5 8-5V7l-8-5z" />,
        python: <path d="M12 2a5 5 0 015 5v2h3a2 2 0 012 2v7a2 2 0 01-2 2h-3v2a5 5 0 01-5 5 5 5 0 01-5-5v-2H2a2 2 0 01-2-2v-7a2 2 0 012-2h3V7a5 5 0 015-5z" />,
        torch: <path d="M12 2L2 12h5v10l10-10h-5L12 2z" />,
        rag: <path d="M4 4h16v16H4V4zm2 2v12h12V6H6zm2 2h8v2H8V8zm0 4h8v2H8v-2zm0 4h5v2H8v-2z" />,
        msp: <path d="M3 3h18v18H3V3zm2 2v2h2V5H5zm4 0v2h10V5H9zm-4 4v2h2V9H5zm4 0v2h10V9H9zm-4 4v2h2v-2H5zm4 0v2h10v-2H9z" />,
        p6: <path d="M12 2c5.5 0 10 4.5 10 10s-4.5 10-10 10S2 17.5 2 12 6.5 2 12 2zm0 4c-3.3 0-6 2.7-6 6s2.7 6 6 6 6-2.7 6-6-2.7-6-6-6z" />,
        sap: <path d="M12 2L2 22h20L12 2zm0 4l7 14H5l7-14z" />,
        lang: <path d="M12 2L2 7v10l10 5 10-5V7L12 2z" />,
        auth: <path d="M12 2a5 5 0 00-5 5v3H6a2 2 0 00-2 2v8a2 2 0 002 2h12a2 2 0 002-2v-8a2 2 0 00-2-2h-1V7a5 5 0 00-5-5zm-3 5a3 3 0 116 0v3H9V7z" />,
        cloud: <path d="M6 11a5 5 0 000 10h12a4 4 0 000-8H16a7 7 0 00-10 0z" />,
    };

    return (
        <svg viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4">
            {icons[type] || <circle cx="12" cy="12" r="8" />}
        </svg>
    );
};

export default function SkillsMatrix() {
    return (
        <div className="font-mono p-4">
            <div className="flex items-center justify-between mb-8">
                <div className="flex items-center gap-4">
                    <h2 className="text-sm font-black text-white tracking-[0.4em] uppercase text-osd">Skills Matrix</h2>
                    <div className="h-4 w-px bg-white/20"></div>
                    <div className="text-[10px] text-white/40 uppercase tracking-widest font-black">Proficiency Levels • Real-Time</div>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-x-12 gap-y-10">
                {mainSkills.map((skill) => (
                    <div key={skill.name} className="relative group">
                        <div className="flex justify-between items-end text-[10px] mb-3 tracking-tighter">
                            <span className="text-white font-black uppercase text-osd">{skill.name}</span>
                            <span className="text-white/40 font-bold">{skill.level}% - {skill.yrs}</span>
                        </div>

                        {/* High-Intensity LED Bar */}
                        <div className="h-2 bg-black/60 rounded-full overflow-hidden border border-white/5 relative shadow-inner">
                            <div
                                className={`h-full bg-gradient-to-r ${skill.color} relative z-20 transition-all duration-1000 ease-out osd-glow-${skill.color.split('-')[1]}`}
                                style={{ width: `${skill.level}%` }}
                            >
                                {/* Shimmer overlay */}
                                <div className="absolute inset-0 bg-[linear-gradient(90deg,transparent,rgba(255,255,255,0.4),transparent)] animate-shimmer"></div>
                            </div>
                            {/* Reflection on Grid Floor (Simulated with absolute overflow) */}
                            <div
                                className={`absolute -bottom-10 left-0 h-20 bg-gradient-to-b from-current to-transparent opacity-10 blur-[20px] transition-all duration-500`}
                                style={{ width: `${skill.level}%`, color: `var(--tw-gradient-to)` }}
                            ></div>
                        </div>

                        {/* Tech Stacks with emission */}
                        <div className="flex gap-5 mt-4 opacity-50 group-hover:opacity-100 transition-all duration-300">
                            {skill.tech.map(t => (
                                <div key={t} className="text-white hover:text-cyber-cyan transition-all transform hover:scale-110 drop-shadow-[0_0_2px_rgba(255,255,255,0.2)]">
                                    <TechIcon type={t} />
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>

            {/* Bottom OSD Metadata */}
            <div className="mt-12 pt-8 border-t border-white/10 flex flex-col md:flex-row justify-between gap-6 opacity-30">
                <div className="text-[9px] font-black tracking-widest text-white/50 uppercase">
                    POWERED BY GEMINI 2.0 FLASH | GOOGLE CLOUD RUN | COPYRIGHT © 2026 TAHIR YAMIN
                </div>
                <div className="flex gap-6 text-[9px] font-bold">
                    <span className="text-cyber-cyan">#FRONTEND: REACT 19 / TAILWIND V4</span>
                    <span className="text-cyber-purple">#BACKEND: NODE / PYTHON 3.12</span>
                    <span className="text-cyber-green">#AI: RAG / GEMINI-PRO</span>
                </div>
            </div>
        </div>
    );
}
