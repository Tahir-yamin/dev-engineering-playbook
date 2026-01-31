'use client';
import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Terminal } from 'lucide-react';

const LOGS = [
    "DAY 5,475: FROM COMMANDING $950M NAVAL OPERATIONS TO ARCHITECTING AI COMMAND CENTERS.",
    "MISSION LOG: 15 YEARS. 3 CONTINENTS. 110+ ENGINEERS. 27 CERTIFICATIONS. ONE OBJECTIVE: EXCELLENCE.",
    "TACTICAL REPORT: INTEGRATING GEMINI AI INTO INDUSTRIAL SYSTEMS. THE FUTURE IS MULTIMODAL.",
    "FIELD NOTES: FROM PAKISTAN NAVY SHIPYARDS TO CUTTING-EDGE AI. EVERY PROJECT IS A CAMPAIGN.",
    "SYSTEM STATUS: NEURAL RAG PROTOCOLS ACTIVE. PREDICTIVE MAINTENANCE ENGINE SYNCED."
];

export default function CommanderLog() {
    const [currentLog, setCurrentLog] = useState(0);

    useEffect(() => {
        const interval = setInterval(() => {
            setCurrentLog(prev => (prev + 1) % LOGS.length);
        }, 10000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="w-full max-w-4xl mx-auto px-4 lg:px-0">
            <div className="relative overflow-hidden bg-primary/5 border border-primary/20 rounded-lg p-3 lg:p-4 backdrop-blur-md">
                <div className="flex items-center gap-3">
                    <div className="flex-shrink-0">
                        <div className="w-8 h-8 rounded-full border border-primary/40 flex items-center justify-center bg-primary/10">
                            <Terminal size={14} className="text-primary animate-pulse" />
                        </div>
                    </div>

                    <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                            <span className="text-[10px] font-mono text-primary/60 uppercase tracking-[0.2em]">Commander's Log // Session Intelligence</span>
                            <div className="h-[1px] flex-1 bg-gradient-to-r from-primary/30 to-transparent" />
                        </div>

                        <AnimatePresence mode="wait">
                            <motion.p
                                key={currentLog}
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: -20 }}
                                transition={{ duration: 0.5, ease: "easeOut" }}
                                className="text-xs lg:text-sm font-mono text-primary/90 tracking-wide uppercase leading-relaxed truncate lg:whitespace-normal"
                            >
                                {LOGS[currentLog]}
                            </motion.p>
                        </AnimatePresence>
                    </div>
                </div>

                {/* HUD Decorative Elements */}
                <div className="absolute top-0 right-0 w-2 h-2 border-t border-r border-primary/40" />
                <div className="absolute bottom-0 left-0 w-2 h-2 border-b border-l border-primary/40" />
            </div>
        </div>
    );
}
