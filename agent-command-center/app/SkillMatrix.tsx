"use client";

import { PROFILE_DATA } from "./data";
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, ResponsiveContainer } from "recharts";

const data = [
    { subject: "Reliability Eng", A: 95, fullMark: 100 },
    { subject: "Industrial AI", A: 90, fullMark: 100 },
    { subject: "Project Mgmt", A: 98, fullMark: 100 },
    { subject: "Cloud/DevOps", A: 85, fullMark: 100 },
    { subject: "Simulation/CAD", A: 92, fullMark: 100 },
    { subject: "Data Science", A: 88, fullMark: 100 },
];

export default function SkillMatrix() {
    return (
        <div className="h-[400px] w-full">
            <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
                    <PolarGrid stroke="rgba(var(--hud-cyan), 0.2)" />
                    <PolarAngleAxis
                        dataKey="subject"
                        tick={{ fill: "rgb(var(--hud-cyan))", fontSize: 10, fontFamily: "monospace" }}
                    />
                    <Radar
                        name="Skills"
                        dataKey="A"
                        stroke="rgb(var(--hud-cyan))"
                        fill="rgb(var(--hud-cyan))"
                        fillOpacity={0.6}
                    />
                </RadarChart>
            </ResponsiveContainer>
            <div className="mt-4 grid grid-cols-2 gap-2">
                {Object.entries(PROFILE_DATA.skills).map(([category, items]) => (
                    <div key={category} className="hud-panel p-2 text-[8px]">
                        <div className="text-hud-amber mb-1 font-bold underline">{category.toUpperCase()}</div>
                        <div className="flex flex-wrap gap-1">
                            {items.map(s => (
                                <span key={s} className="bg-hud-cyan/10 px-1 border border-hud-cyan/20">{s}</span>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
