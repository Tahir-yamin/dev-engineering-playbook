'use client';

const missions = [
    { name: 'TARGETS AI OPTIMIZATION', status: 'ONGOING', time: '14:58:21' },
    { name: 'RESOURCE INFRASTRUCTURE OPTIMIZATION', status: 'ONGOING', time: '14:59:01' },
    { name: 'DATA PROCESSING NODE', status: 'ACTIVE', time: '14:59:21' },
    { name: 'AI ARCHITECTURE OPTIMIZATION', status: 'ONGOING', time: '14:59:21' },
    { name: 'NEURAL INTERFACE OPTIMIZATION', status: 'ONGOING', time: '14:59:21' },
    { name: 'PROTOCOL REFINEMENT OPTIMIZATION', status: 'ONGOING', time: '14:59:21' },
];

export default function MissionLog() {
    return (
        <div className="w-[320px] h-[650px] glass-panel tech-border-amber flex flex-col p-6 relative bg-black/40 backdrop-blur-sm">

            {/* Header */}
            <div className="mb-8 border-b border-[#ffae00]/30 pb-4">
                <h2 className="text-xl font-medium text-[#ffae00] tracking-wider font-sans">PROJECT MISSION LOGS</h2>
            </div>

            {/* Mission List */}
            <div className="flex-1 space-y-3 overflow-y-auto no-scrollbar pr-1">
                {missions.map((m, i) => (
                    <div key={i} className="group relative border border-[#ffae00]/20 bg-[#ffae00]/5 hover:bg-[#ffae00]/10 p-3 transition-all cursor-pointer">

                        {/* Title */}
                        <div className="text-[10px] font-bold text-[#ffae00] mb-1 uppercase tracking-tight">
                            {m.name}
                        </div>

                        {/* Metadata Row */}
                        <div className="flex justify-between items-center text-[8px] font-mono text-white/50">
                            <span className="uppercase">STATUS: <span className="text-white">{m.status}</span></span>
                            <span>LAST UPDATE: {m.time}</span>
                        </div>
                    </div>
                ))}
            </div>

            {/* Footer Status */}
            <div className="mt-8 pt-4 border-t border-white/10 flex justify-between items-center text-[10px] text-white/30 uppercase tracking-[0.2em]">
                <span>LOG_STATUS</span>
                <span className="text-[#ffae00] animate-pulse">RECORDING</span>
            </div>
        </div>
    );
}
