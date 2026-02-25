'use client';

import React, { useState } from 'react';
import { Tag } from 'lucide-react';

/**
 * SessionLabelToggle.tsx
 * 
 * RESPONSIBILITY:
 * UI Component for marking the current session as BASELINE vs SIMULATED.
 * Used during pilot study data collection for ground truth validation.
 */

interface SessionLabelToggleProps {
    currentLabel: 'BASELINE' | 'SIMULATED' | 'UNLABELED';
    onChange: (label: 'BASELINE' | 'SIMULATED') => void;
}

export function SessionLabelToggle({ currentLabel, onChange }: SessionLabelToggleProps) {
    const [label, setLabel] = useState(currentLabel);

    const handleToggle = (newLabel: 'BASELINE' | 'SIMULATED') => {
        setLabel(newLabel);
        onChange(newLabel);
    };

    return (
        <div className="flex items-center gap-3 p-4 bg-slate-950 border border-slate-800 rounded-xl">
            <Tag className="w-5 h-5 text-blue-400" />
            <div className="flex-1">
                <div className="text-xs text-slate-400 mb-2">Research Mode - Label This Session</div>
                <div className="flex gap-2">
                    <button
                        onClick={() => handleToggle('BASELINE')}
                        className={`px-4 py-2 rounded-lg text-xs font-bold transition-all ${label === 'BASELINE'
                                ? 'bg-green-600 text-white shadow-lg shadow-green-500/20'
                                : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
                            }`}
                    >
                        ✓ BASELINE (Normal Use)
                    </button>
                    <button
                        onClick={() => handleToggle('SIMULATED')}
                        className={`px-4 py-2 rounded-lg text-xs font-bold transition-all ${label === 'SIMULATED'
                                ? 'bg-orange-600 text-white shadow-lg shadow-orange-500/20'
                                : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
                            }`}
                    >
                        ⚠ SIMULATED (Acting Symptoms)
                    </button>
                </div>
            </div>
            {label !== 'UNLABELED' && (
                <div className="text-[10px] text-slate-500 px-3 py-1 bg-slate-900 rounded-md border border-slate-700">
                    Current: <span className={label === 'BASELINE' ? 'text-green-400' : 'text-orange-400'}>
                        {label}
                    </span>
                </div>
            )}
        </div>
    );
}
