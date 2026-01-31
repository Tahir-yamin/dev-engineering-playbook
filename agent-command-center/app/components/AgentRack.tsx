'use client';

import {
    ServerIcon,
    CpuChipIcon,
    ShieldCheckIcon,
    CommandLineIcon,
    SignalIcon,
    LockClosedIcon
} from '@heroicons/react/24/outline';

const modules = [
    { name: 'RESOURCE ALLOCATION', icon: ServerIcon, active: false },
    { name: 'SYSTEM DIAGNOSTICS', icon: CpuChipIcon, active: true }, // Highlighted in mockup
    { name: 'RESOURCE OVERRIDE', icon: CommandLineIcon, active: false },
    { name: 'PROTOCOL OVERRIDE', icon: LockClosedIcon, active: false },
    { name: 'NETWORK SECURITY', icon: ShieldCheckIcon, active: false },
    { name: 'SIGNAL ANALYSIS', icon: SignalIcon, active: false },
];

export default function AgentRack() {
    return (
        <div className="w-[320px] h-[650px] glass-panel tech-border-cyan flex flex-col p-6 relative bg-black/40 backdrop-blur-sm">

            {/* Header */}
            <div className="mb-8 border-b border-cyber-cyan/30 pb-4">
                <h2 className="text-xl font-medium text-cyber-cyan tracking-wider font-sans">AGENT FUNCTION MODULES</h2>
            </div>

            {/* Menu Buttons */}
            <div className="flex-1 space-y-4">
                {modules.map((mod, i) => (
                    <button
                        key={i}
                        className={`w-full text-left p-4 border transition-all duration-300 flex items-center gap-4 group relative overflow-hidden
                        ${mod.active
                                ? 'bg-cyber-cyan/20 border-cyber-cyan text-white shadow-[0_0_15px_rgba(0,255,249,0.3)]'
                                : 'bg-transparent border-white/10 text-white/50 hover:border-cyber-cyan/50 hover:text-white'
                            }`}
                    >
                        <mod.icon className={`w-6 h-6 ${mod.active ? 'text-cyber-cyan' : 'text-current'}`} />
                        <span className="text-sm font-bold tracking-widest uppercase">{mod.name}</span>

                        {/* Active Glow Bar */}
                        {mod.active && (
                            <div className="absolute left-0 top-0 bottom-0 w-1 bg-cyber-cyan shadow-[0_0_10px_#00fff9]"></div>
                        )}
                    </button>
                ))}
            </div>

            {/* Footer Status */}
            <div className="mt-8 pt-4 border-t border-white/10 flex justify-between items-center text-[10px] text-white/30 uppercase tracking-[0.2em]">
                <span>MOD_STATUS</span>
                <span className="text-cyber-cyan animate-pulse">ONLINE</span>
            </div>
        </div>
    );
}
