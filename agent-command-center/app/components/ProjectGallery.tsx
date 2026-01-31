'use client';

import { useState } from 'react';

const projects = [
    {
        id: 1,
        title: 'Industrial IoT Predictive Maintenance',
        category: 'Data Analytics',
        status: 'DEPLOYED: LIVE',
        tech: ['PYTORCH', 'TENSORFLOW', 'IOT'],
        description: 'Advanced predictive analytics for industrial machinery using real-time sensor streams and deep learning models.',
        color: 'cyber-cyan'
    },
    {
        id: 2,
        title: 'Global Supply Chain Neural Optimizer',
        category: 'Logistics',
        status: 'MONITORING',
        tech: ['NEXT.JS', 'PYTHON', 'DOCKER'],
        description: 'Optimizing international freight routing through neural network pathfinding and demand forecasting.',
        color: 'cyber-purple'
    },
    {
        id: 3,
        title: 'Smart City Grid Management v2',
        category: 'OSD-INFRA',
        status: 'UAT',
        tech: ['REACT', 'STAGING', 'POSTGRES'],
        description: 'Municipal energy monitoring dashboard with failure preemptive alerts and load balancing visualizer.',
        color: 'cyber-green'
    }
];

export default function ProjectGallery() {
    const [activeIndex, setActiveIndex] = useState(0);

    return (
        <div className="relative h-full flex flex-col font-mono">
            <div className="flex items-center justify-between mb-8 border-b border-cyber-cyan/30 pb-2">
                <h2 className="text-sm font-black text-cyber-cyan tracking-[0.4em] uppercase">Project Gallery</h2>
                <div className="flex gap-4">
                    <button
                        onClick={() => setActiveIndex(prev => (prev > 0 ? prev - 1 : projects.length - 1))}
                        className="text-cyber-cyan hover:text-white transition-all hover:scale-125"
                    >
                        [&lt;]
                    </button>
                    <button
                        onClick={() => setActiveIndex(prev => (prev < projects.length - 1 ? prev + 1 : 0))}
                        className="text-cyber-cyan hover:text-white transition-all hover:scale-125"
                    >
                        [&gt;]
                    </button>
                </div>
            </div>

            <div className="flex-1 relative flex items-center justify-center min-h-[320px] mb-4">
                {/* 3D Stack Container */}
                <div className="relative w-full max-w-[300px] h-full flex items-center justify-center perspective-[1200px] preserve-3d">
                    {projects.map((project, index) => {
                        const offset = index - activeIndex;
                        const absOffset = Math.abs(offset);
                        const isCenter = offset === 0;

                        // Dramatic 3D transform
                        const translateX = offset * 60;
                        const translateZ = absOffset * -100;
                        const rotateY = offset * -25;
                        const opacity = isCenter ? 1 : 0.25;
                        const zIndex = 10 - absOffset;

                        return (
                            <div
                                key={project.id}
                                className="absolute w-[280px] h-[360px] transition-all duration-700 cubic-bezier(0.23, 1, 0.32, 1) cursor-pointer"
                                style={{
                                    transform: `translateX(${translateX}px) translateZ(${translateZ}px) rotateY(${rotateY}deg)`,
                                    opacity,
                                    zIndex,
                                    pointerEvents: isCenter ? 'auto' : 'none'
                                }}
                                onClick={() => setActiveIndex(index)}
                            >
                                <div className={`h-full w-full glass-panel p-6 border-2 flex flex-col relative overflow-hidden ${isCenter ? 'border-cyber-cyan/40 shadow-[0_0_30px_rgba(0,255,249,0.15)]' : 'border-cyber-cyan/5'
                                    }`}>
                                    {/* Project Meta */}
                                    <div className="mb-6">
                                        <div className="flex items-center justify-between mb-3">
                                            <span className="text-[9px] font-bold text-cyber-cyan/60 tracking-widest">{project.category}</span>
                                            <div className="w-1.5 h-1.5 rounded-full bg-cyber-cyan/20"></div>
                                        </div>
                                        <h3 className="text-sm lg:text-md font-black text-white leading-tight uppercase tracking-tight">
                                            {project.title}
                                        </h3>
                                    </div>

                                    {/* Description */}
                                    <div className="flex-1">
                                        <p className="text-[10px] text-white/40 leading-relaxed mb-6 italic border-l-2 border-white/5 pl-3">
                                            {project.description}
                                        </p>

                                        <div className="flex flex-wrap gap-2">
                                            {project.tech.map(t => (
                                                <span key={t} className="text-[9px] font-bold text-white/80 bg-white/5 border border-white/10 px-1.5 py-0.5 rounded-sm">
                                                    {t}
                                                </span>
                                            ))}
                                        </div>
                                    </div>

                                    {/* Status Section */}
                                    <div className="mt-auto pt-4 border-t border-white/5">
                                        <div className="flex items-center justify-between">
                                            <span className="text-[9px] font-black text-cyber-green flex items-center gap-2 tracking-[0.2em]">
                                                <span className="w-2 h-2 rounded-full bg-cyber-green animate-pulse"></span>
                                                {project.status}
                                            </span>
                                            <span className="text-[9px] text-white/20">#{project.id.toString().padStart(3, '0')}</span>
                                        </div>
                                    </div>

                                    {/* Inner Scanline Overlay */}
                                    <div className="absolute inset-0 pointer-events-none bg-[linear-gradient(rgba(0,255,249,0.01)_1px,transparent_1px)] bg-[length:100%_3px] opacity-20"></div>
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>

            {/* Finer pagination markers */}
            <div className="mt-4 flex justify-center gap-3">
                {projects.map((_, i) => (
                    <div
                        key={i}
                        className={`h-0.5 transition-all duration-500 ${i === activeIndex ? 'w-10 bg-cyber-cyan shadow-[0_0_15px_#00fff9]' : 'w-4 bg-white/5'}`}
                    ></div>
                ))}
            </div>
        </div>
    );
}
