'use client';

import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

// Pre-calculated coordinates to prevent hydration mismatch (server vs client math precision)
const STATIC_COORDS = [
    { x2: 134.64, y2: 60 }, { x2: 128.28, y2: 68.28 }, { x2: 117.32, y2: 74.64 }, { x2: 104.16, y2: 78.28 },
    { x2: 91.68, y2: 78.28 }, { x2: 80, y2: 74.64 }, { x2: 70.72, y2: 68.28 }, { x2: 65.36, y2: 60 },
    { x2: 65.36, y2: 50.72 }, { x2: 70.72, y2: 42.44 }, { x2: 80, y2: 36.08 }, { x2: 91.68, y2: 32.44 }
];

const STATIC_NODES = [
    { cx: 121.21, cy: 61.21, delay: 0 }, { cx: 100, cy: 70, delay: 0.2 }, { cx: 78.79, cy: 61.21, delay: 0.4 },
    { cx: 70, cy: 40, delay: 0.6 }, { cx: 78.79, cy: 18.79, delay: 0.8 }, { cx: 100, cy: 10, delay: 1.0 },
    { cx: 121.21, cy: 18.79, delay: 1.2 }, { cx: 130, cy: 40, delay: 1.4 }
];

export default function AIAssistant() {
    const [messages, setMessages] = useState([
        { id: 1, role: 'system', text: 'INITIALIZING INTELLIGENCE FEED SERVICE...', time: '01:28' },
        { id: 2, role: 'assistant', text: 'FOUND 3 PROJECTS CORRELATED TO QUERY [POWER-BI]. FILTERING OSD HUD...', time: '01:29' }
    ]);
    const [input, setInput] = useState('');
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);

    const handleSend = (e?: React.FormEvent) => {
        if (e) e.preventDefault();
        if (!input.trim()) return;

        const userMsg = input;
        setInput('');
        setMessages(prev => [...prev, { id: Date.now(), role: 'user', text: `>> CMD: ${userMsg.toUpperCase()}`, time: 'NOW' }]);

        setTimeout(() => {
            setMessages(prev => [...prev, {
                id: Date.now() + 1,
                role: 'assistant',
                text: `[AUTH_L3] PROCESSING REQUEST: "${userMsg.toUpperCase()}"... LINKING DATABASE NODES. ACCESS GRANTED.`,
                time: 'LOG'
            }]);
        }, 600);
    };

    return (
        <div className="flex flex-col h-full font-mono bg-black/40 p-1">
            {/* OSD Header - No bubbles, raw technical header */}
            <div className="flex items-center justify-between mb-4 border-b-2 border-cyber-purple/40 pb-2 px-2">
                <div className="flex items-center gap-3">
                    <div className="flex items-center gap-1">
                        <span className="text-sm font-black text-white tracking-widest uppercase text-osd">Gemini</span>
                        <div className="w-4 h-4">
                            <svg viewBox="0 0 24 24" fill="none" className="animate-spin-slow">
                                <path d="M12 2L14.5 9.5L22 12L14.5 14.5L12 22L9.5 14.5L2 12L9.5 9.5L12 2Z" fill="url(#assist-star)" />
                                <defs>
                                    <linearGradient id="assist-star" x1="0%" y1="0%" x2="100%" y2="100%">
                                        <stop offset="0%" stopColor="#4185f4" />
                                        <stop offset="100%" stopColor="#b026ff" />
                                    </linearGradient>
                                </defs>
                            </svg>
                        </div>
                    </div>
                    <div className="h-4 w-px bg-white/10"></div>
                    <span className="text-[9px] font-bold text-cyber-purple/70 tracking-[0.2em]">INTELLIGENCE_FEED: ONLINE</span>
                </div>
            </div>

            {/* Complex Neural Visualization - integrated, not a box */}
            <div className="h-32 relative mb-4 overflow-hidden rounded border border-white/5 bg-black/40 shadow-inner">
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(176,38,255,0.1),transparent_80%)]"></div>
                <svg className="w-full h-full" viewBox="0 0 200 80">
                    <motion.g
                        animate={{ rotate: 360 }}
                        transition={{ duration: 60, repeat: Infinity, ease: "linear" }}
                        style={{ originX: '100px', originY: '40px' }}
                    >
                        {/* Dense Matrix Lines using Static Coords */}
                        {STATIC_COORDS.map((coord, i) => (
                            <line
                                key={i}
                                x1="100" y1="40"
                                x2={coord.x2}
                                y2={coord.y2}
                                stroke="#b026ff" strokeWidth="0.2" className="opacity-20"
                            />
                        ))}
                        {/* Animated Nodes using Static Coords */}
                        {STATIC_NODES.map((node, i) => (
                            <motion.circle
                                key={i}
                                cx={node.cx}
                                cy={node.cy}
                                r="1" fill="#00fff9"
                                animate={{ opacity: [0.2, 1, 0.2] }}
                                transition={{ duration: 2, repeat: Infinity, delay: node.delay }}
                            />
                        ))}
                    </motion.g>
                    <circle cx="100" cy="40" r="2" fill="#b026ff" className="shadow-[0_0_10px_#b026ff]" />
                </svg>
            </div>

            {/* RAW DATA FEED - No chat bubbles, data logs logs only */}
            <div
                ref={scrollRef}
                className="flex-1 overflow-y-auto space-y-2 mb-4 scrollbar-hide px-2"
            >
                <AnimatePresence initial={false}>
                    {messages.map((msg) => (
                        <motion.div
                            key={msg.id}
                            initial={{ opacity: 0, x: -5 }}
                            animate={{ opacity: 1, x: 0 }}
                            className="font-mono"
                        >
                            <div className="flex gap-2">
                                <span className="text-[8px] text-white/20">[{msg.time}]</span>
                                <span className={`text-[10px] uppercase tracking-tight ${msg.role === 'user' ? 'text-cyber-cyan' :
                                        msg.role === 'system' ? 'text-white/40 italic' :
                                            'text-cyber-purple drop-shadow-[0_0_3px_rgba(176,38,255,0.4)]'
                                    }`}>
                                    {msg.text}
                                </span>
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>
            </div>

            {/* OSD Command Input */}
            <div className="relative border-t border-white/5 pt-4">
                <form onSubmit={handleSend} className="relative group">
                    <div className="absolute left-3 top-1/2 -translate-y-1/2 text-cyber-cyan text-[10px] font-black group-focus-within:animate-pulse">
                        {`>>`}
                    </div>
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="TERMINAL_READY..."
                        className="w-full bg-black/60 border border-white/10 rounded-sm py-2 pl-9 pr-10 text-[10px] text-white focus:outline-none focus:border-cyber-purple/60 focus:ring-1 focus:ring-cyber-purple/20 transition-all uppercase tracking-widest"
                    />
                    <button
                        type="submit"
                        className="absolute right-2 top-1/2 -translate-y-1/2 text-cyber-purple hover:text-white transition-all"
                    >
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" className="w-4 h-4">
                            <path d="M5 12h14M12 5l7 7-7 7" />
                        </svg>
                    </button>
                </form>
                <div className="mt-3 flex gap-4 overflow-x-auto no-scrollbar pb-1">
                    {['#ANALYZE-DEVOPS', '#FILTER-LOGS', '#OSD-REBOOT'].map(tag => (
                        <button
                            key={tag}
                            onClick={() => setInput(tag.replace('#', ''))}
                            className="whitespace-nowrap text-[8px] font-black text-white/30 hover:text-cyber-purple border border-white/5 px-2 py-0.5 rounded-sm transition-all"
                        >
                            {tag}
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
}
