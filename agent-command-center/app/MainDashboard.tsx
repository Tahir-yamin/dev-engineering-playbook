"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { PROFILE_DATA } from "./data";
import {
    Terminal,
    Cpu,
    Briefcase,
    MessageSquare,
    Network,
    Activity,
    User,
    Settings,
    Server,
    Brain,
    Layers,
    Cloud,
    FileText,
    Fingerprint,
    Link as LinkIcon,
    CheckCircle,
    Box,
    FileSearch,
    X,
    Award,
    ShieldCheck,
    Globe,
    Zap,
    BarChart3,
    Maximize2,
    BarChart,
    Search as SearchIcon,
    Terminal as TerminalIcon,
    Github,
    Database,
    Star,
    GitFork,
    ExternalLink,
} from "lucide-react";
import { askArchitect } from "../services/geminiService";
import AskTheManual from "./AskTheManual";
import ReactMarkdown from 'react-markdown';
import CommanderLog from "./components/CommanderLog";

const CornerBrackets = () => (
    <>
        <div className="corner-bracket corner-tl" />
        <div className="corner-bracket corner-tr" />
        <div className="corner-bracket corner-bl" />
        <div className="corner-bracket corner-br" />
    </>
);

const TacticalFrame = () => (
    <div className="fixed inset-0 pointer-events-none z-[100] border-[20px] border-transparent">
        <div className="absolute top-0 left-0 w-8 h-8 border-t-2 border-l-2 border-primary/20" />
        <div className="absolute top-0 right-0 w-8 h-8 border-t-2 border-r-2 border-primary/20" />
        <div className="absolute bottom-0 left-0 w-8 h-8 border-b-2 border-l-2 border-primary/20" />
        <div className="absolute bottom-0 right-0 w-8 h-8 border-b-2 border-r-2 border-primary/20" />
        <div className="absolute top-1/2 left-4 -translate-y-1/2 flex flex-col gap-1">
            <div className="w-1 h-1 bg-primary/20 rounded-full" />
            <div className="w-1 h-8 bg-primary/10 rounded-full" />
            <div className="w-1 h-1 bg-primary/20 rounded-full" />
        </div>
        <div className="absolute top-1/2 right-4 -translate-y-1/2 flex flex-col gap-1">
            <div className="w-1 h-1 bg-primary/20 rounded-full" />
            <div className="w-1 h-8 bg-primary/10 rounded-full" />
            <div className="w-1 h-1 bg-primary/20 rounded-full" />
        </div>
    </div>
);

export default function MainDashboard() {
    const [mounted, setMounted] = useState(false);
    const [bootSequence, setBootSequence] = useState(true);
    const [query, setQuery] = useState("");
    const [aiResponse, setAiResponse] = useState("");
    const [isTyping, setIsTyping] = useState(false);
    const [showRAGModal, setShowRAGModal] = useState(false);
    const [showNeuralLink, setShowNeuralLink] = useState(false);
    const [leftPanelCollapsed, setLeftPanelCollapsed] = useState(false);
    const [rightPanelCollapsed, setRightPanelCollapsed] = useState(false);
    const [selectedCert, setSelectedCert] = useState<any>(null);
    const [selectedArticle, setSelectedArticle] = useState<any>(null);
    const [selectedProject, setSelectedProject] = useState<any>(null);
    const [dashIndex, setDashIndex] = useState(0);
    const [showReadmeModal, setShowReadmeModal] = useState(false);
    const [readmeContent, setReadmeContent] = useState("");
    const [showSimModal, setShowSimModal] = useState(false);
    const [simStatus, setSimStatus] = useState<'normal' | 'anomaly' | 'resolving' | 'resolved'>('anomaly');

    // Auto-advance dashboard slider
    useEffect(() => {
        const timer = setInterval(() => {
            setDashIndex((prev) => (prev + 1) % (PROFILE_DATA as any).dashboards.length);
        }, 5000);
        return () => clearInterval(timer);
    }, []);

    useEffect(() => {
        setMounted(true);
        const timer = setTimeout(() => setBootSequence(false), 1500);
        return () => clearTimeout(timer);
    }, []);

    const handleAsk = async () => {
        if (!query) return;
        setIsTyping(true);
        setAiResponse("INITIALIZING_AGENT_CORE...");
        const response = await askArchitect(query);
        setAiResponse(response);
        setIsTyping(false);
    };

    const handleResolveAnomaly = () => {
        setSimStatus('resolving');
        setTimeout(() => {
            setSimStatus('resolved');
        }, 4000);
    };

    // Fetch README content
    useEffect(() => {
        const fetchReadme = async () => {
            try {
                const response = await fetch("/api/readme");
                if (response.ok) {
                    const text = await response.text();
                    setReadmeContent(text);
                } else {
                    setReadmeContent("ERROR_FETCHING_INTEL: /README.md access denied or file missing.");
                }
            } catch (error) {
                setReadmeContent("ERROR_FETCHING_INTEL: System communication breakdown.");
            }
        };
        fetchReadme();
    }, []);

    // Prevent hydration mismatch
    if (!mounted) return null;

    if (bootSequence) {
        return (
            <div className="flex h-screen items-center justify-center bg-[#050b14] font-mono text-primary">
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="space-y-4 text-center"
                >
                    <div className="text-4xl font-bold tracking-[0.3em] animate-pulse">AEGIS-OS v4.0.2</div>
                    <div className="text-xs opacity-50 underline">LOADING_ARCHITECT_RECORDS: TAHIR_YAMIN</div>
                </motion.div>
            </div>
        );
    }

    return (
        <div className="bg-[#050b14] text-slate-300 font-display min-h-screen selection:bg-primary selection:text-black flex flex-col relative overflow-x-hidden tactical-cursor">
            <div className="scanline" />
            <div className="biometric-scanner" />
            <div className="noise-overlay" />
            <TacticalFrame />

            {/* Header */}
            <header className="fixed top-0 left-0 w-full h-12 flex items-center justify-between px-6 z-50 border-b border-primary/30 bg-[#050b14]/90 backdrop-blur-sm">
                <div className="flex items-center gap-4">
                    <span className="text-xs font-mono text-primary/70">MOSSOUT [SIG]</span>
                    <div className="h-2 w-24 bg-slate-800 rounded-sm overflow-hidden border border-primary/30">
                        <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: "66%" }}
                            className="h-full bg-primary shadow-[0_0_10px_#00f0ff]"
                        />
                    </div>
                </div>
                <div className="flex-1 flex justify-center gap-12 font-mono text-[10px] text-primary/50 tracking-widest hidden md:flex">
                    <span>/// 30</span>
                    <span>250</span>
                    <span className="text-primary text-base">▼</span>
                    <span>N</span>
                    <span>65</span>
                </div>
                <nav className="flex items-center gap-3 ml-auto flex-wrap justify-end">
                    <button
                        onClick={() => setShowNeuralLink(!showNeuralLink)}
                        className={`flex items-center gap-2 px-3 py-1.5 rounded border transition-all text-[10px] font-bold tracking-widest uppercase ${showNeuralLink ? 'bg-primary text-black border-primary' : 'bg-transparent border-primary/30 text-primary/60 hover:border-primary hover:text-primary'}`}
                    >
                        <Brain size={14} />
                        <span className="hidden sm:inline">Neural_Link</span>
                    </button>

                    <button
                        onClick={() => setLeftPanelCollapsed(!leftPanelCollapsed)}
                        className={`flex items-center gap-2 px-3 py-1.5 rounded border transition-all text-[10px] font-bold tracking-widest uppercase ${leftPanelCollapsed ? 'bg-primary/20 border-primary text-primary' : 'bg-transparent border-primary/30 text-primary/60 hover:border-primary hover:text-primary'}`}
                    >
                        <Settings size={14} />
                        <span className="hidden sm:inline">{leftPanelCollapsed ? 'Show_Agents' : 'Hide_Agents'}</span>
                    </button>
                    <button
                        onClick={() => setRightPanelCollapsed(!rightPanelCollapsed)}
                        className={`flex items-center gap-2 px-3 py-1.5 rounded border transition-all text-[10px] font-bold tracking-widest uppercase ${rightPanelCollapsed ? 'bg-secondary/20 border-secondary text-secondary' : 'bg-transparent border-secondary/30 text-secondary/60 hover:border-secondary hover:text-secondary'}`}
                    >
                        <Activity size={14} />
                        <span className="hidden sm:inline">{rightPanelCollapsed ? 'Show_Intel' : 'Hide_Intel'}</span>
                    </button>
                    <button
                        onClick={() => setShowRAGModal(true)}
                        className="flex items-center gap-3 bg-primary/10 border border-primary/40 px-4 py-1.5 rounded hover:bg-primary/20 hover:border-primary transition-all group"
                    >
                        <FileSearch size={16} className="text-primary group-hover:scale-110 transition-transform" />
                        <div className="text-left">
                            <div className="text-[10px] font-bold text-primary group-hover:text-primary leading-none uppercase tracking-tighter">Ask The</div>
                            <div className="text-[11px] font-black text-primary leading-none uppercase">Manual</div>
                        </div>
                    </button>
                    <div className="flex items-center gap-2 border-l border-primary/20 pl-3">
                        <motion.button
                            onClick={() => setShowReadmeModal(true)}
                            animate={{ opacity: [0.3, 1, 0.3] }}
                            transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
                            className="flex items-center gap-2 bg-red-500/10 border border-red-500/40 px-3 py-1 rounded-full hover:bg-red-500/20 transition-all cursor-pointer mr-2"
                        >
                            <div className="w-1.5 h-1.5 rounded-full bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.8)]" />
                            <span className="text-[9px] font-bold text-red-500 uppercase tracking-widest">Architect_Readme</span>
                        </motion.button>
                        <div className="text-[9px] text-primary/50 font-mono uppercase tracking-widest mr-2">Power</div>
                        <div className="w-16 h-1.5 bg-primary/10 rounded-full overflow-hidden border border-primary/20">
                            <motion.div
                                animate={{ width: "30%" }}
                                className="h-full bg-primary shadow-neon"
                            />
                        </div>
                    </div>
                </nav>
            </header>

            <main className="relative pt-24 pb-24 px-4 md:px-8 min-h-screen w-full flex flex-col gap-6">
                <CommanderLog />

                <div className="flex flex-col md:flex-row gap-6">
                    {/* Left Section: Agent Rack */}
                    <AnimatePresence>
                        {!leftPanelCollapsed && (
                            <motion.section
                                initial={{ width: 0, opacity: 0, x: -50 }}
                                animate={{ width: 288, opacity: 1, x: 0 }}
                                exit={{ width: 0, opacity: 0, x: -50 }}
                                className="hidden md:flex flex-col w-72 shrink-0 hud-panel tactical-border rounded-lg p-1 perspective-left transform transition-transform duration-500 overflow-y-auto no-scrollbar"
                            >
                                <CornerBrackets />
                                <div className="bg-primary/10 border-b border-primary/30 p-3 mb-4 sticky top-0 z-10">
                                    <h2 className="text-primary font-bold tracking-widest text-xs uppercase glitch-hover">Industrial Dev Stack</h2>
                                    <div className="text-xs text-primary/60 font-mono">LOCAL KNOWLEDGE SYNC [STABLE]</div>
                                </div>
                                <div className="flex-1 space-y-3 px-2 pb-2">
                                    {[
                                        { name: "PRIMAVERA P6", level: "98%", icon: <Activity size={18} /> },
                                        { name: "POWER BI", level: "95%", icon: <BarChart size={18} /> },
                                        { name: "PYTHON / AI", level: "92%", icon: <Brain size={18} /> },
                                        { name: "NEXT.JS / REACT", level: "88%", icon: <Terminal size={18} /> },
                                        { name: "DOCKER / K8S", level: "85%", icon: <Layers size={18} /> },
                                        { name: "SQL / DATA", level: "90%", icon: <Database size={18} /> },
                                    ].map((skill, idx) => (
                                        <div key={idx} className="group relative border border-primary/20 bg-slate-900/50 hover:bg-primary/10 hover:border-primary transition-all duration-300 p-3 rounded">
                                            <div className="absolute top-0 right-0 p-1 opacity-0 group-hover:opacity-100 transition-opacity">
                                                <Settings size={10} className="text-primary" />
                                            </div>
                                            <div className="flex items-center gap-3">
                                                <span className="text-primary/80">{skill.icon}</span>
                                                <div className="flex-1">
                                                    <h3 className="text-base font-semibold text-white group-hover:text-primary transition-colors">{skill.name}</h3>
                                                    <div className="w-full bg-slate-800 h-1.5 mt-2 rounded-full overflow-hidden">
                                                        <motion.div
                                                            initial={{ width: 0 }}
                                                            animate={{ width: skill.level }}
                                                            className="bg-primary h-full rounded-full shadow-[0_0_8px_#00f0ff]"
                                                        />
                                                    </div>
                                                </div>
                                                <span className="text-xs font-mono text-primary/80 font-bold">{skill.level}</span>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </motion.section>
                        )}
                    </AnimatePresence>

                    {/* Center Section: Core Profile Metadata */}
                    <div className="flex-1 flex flex-col gap-6 pb-20 px-2">
                        {/* Summary Header */}
                        <div className="hud-panel rounded-lg p-5 border-l-4 border-primary bg-primary/5 relative">
                            <CornerBrackets />
                            <div className="flex flex-col lg:flex-row items-center lg:items-start gap-6">
                                <div className="relative">
                                    <div className="w-24 h-24 lg:w-32 lg:h-32 rounded-full border-2 border-primary/50 overflow-hidden bg-black flex items-center justify-center p-1">
                                        {(PROFILE_DATA as any).avatar ? (
                                            <img
                                                src={(PROFILE_DATA as any).avatar}
                                                alt={PROFILE_DATA.name}
                                                className="w-full h-full object-cover rounded-full filter grayscale hover:grayscale-0 transition-all duration-500"
                                            />
                                        ) : (
                                            <Fingerprint size={80} className="text-primary opacity-80" />
                                        )}
                                    </div>
                                    <div className="absolute -bottom-2 -right-2 bg-primary text-black text-[8px] font-bold px-1 rounded">VERIFIED</div>
                                </div>
                                <div className="text-center lg:text-left">
                                    <h1 className="text-4xl font-black tracking-tighter text-white uppercase italic mb-1 glitch-hover">{PROFILE_DATA.name}</h1>
                                    <p className="text-sm text-primary font-mono tracking-[0.4em] mb-4 uppercase flex items-center gap-2">
                                        <span className="w-2 h-2 rounded-full bg-primary animate-ping" />
                                        {PROFILE_DATA.title}
                                    </p>
                                    <p className="text-[11px] text-slate-400 max-w-2xl leading-relaxed font-mono opacity-80">{PROFILE_DATA.summary}</p>
                                </div>
                            </div>
                        </div>

                        {/* Impact Stats Grid */}
                        <div className="grid grid-cols-2 lg:grid-cols-5 gap-3">
                            {[
                                { label: "Naval Eng Scope", val: PROFILE_DATA.impact.maritime_value, icon: ShieldCheck, color: "text-primary" },
                                { label: "HVAC Managed", val: PROFILE_DATA.impact.hvac_budget, icon: Zap, color: "text-yellow-400" },
                                { label: "Ship Repair", val: PROFILE_DATA.impact.ship_repair, icon: Box, color: "text-blue-400" },
                                { label: "Command Span", val: PROFILE_DATA.impact.team_size, icon: User, color: "text-green-400" },
                                { label: "Total Tenure", val: PROFILE_DATA.impact.total_exp, icon: Globe, color: "text-secondary" },
                            ].map((stat, i) => (
                                <div key={i} className="hud-panel tactical-border p-3 border-t border-primary/20 flex flex-col items-center text-center group hover:bg-primary/5 transition-all">
                                    <stat.icon size={16} className={`${stat.color} mb-1 opacity-70 group-hover:opacity-100 transition-opacity`} />
                                    <div className="text-lg font-bold text-white tracking-tighter">{stat.val}</div>
                                    <div className="text-[10px] text-slate-500 uppercase tracking-widest leading-tight">{stat.label}</div>
                                </div>
                            ))}
                        </div>

                        {/* Experience Grid */}
                        <div className="space-y-4">
                            <div className="flex items-center gap-2 mb-2 px-1 border-b border-primary/10 pb-2">
                                <Activity size={14} className="text-primary" />
                                <h2 className="text-[10px] font-bold tracking-[0.3em] uppercase text-primary/80">Career_Chronicle_Operational_History</h2>
                            </div>
                            <div className="space-y-10">
                                {PROFILE_DATA.experience.map((exp, i) => (
                                    <div key={i} className="relative pl-8 border-l-2 border-primary/30 py-2 group hover:border-primary transition-colors">
                                        <div className="absolute -left-[9px] top-4 w-4 h-4 rounded-full bg-[#050b14] border-2 border-primary animate-pulse" />
                                        <div className="flex flex-col md:flex-row md:items-center justify-between mb-4 gap-2">
                                            <div>
                                                <h3 className="text-xl font-bold text-white uppercase tracking-tight group-hover:text-primary transition-colors leading-none mb-1">{exp.role}</h3>
                                                <div className="text-primary/70 font-mono text-sm uppercase tracking-wider">{exp.company}</div>
                                            </div>
                                            <div className="text-right">
                                                <div className="text-sm font-mono text-white/50">{exp.period}</div>
                                                <div className="text-[10px] text-primary/40 uppercase tracking-widest">{exp.location}</div>
                                            </div>
                                        </div>
                                        <ul className="space-y-3">
                                            {exp.points.map((point, j) => (
                                                <li key={j} className="text-slate-300 text-base leading-relaxed flex gap-3 group/item">
                                                    <span className="text-primary font-mono mt-1 opacity-50 select-none group-hover/item:opacity-100 transition-opacity">0{j + 1}</span>
                                                    <span>{point}</span>
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Certifications Registry */}
                        <div className="space-y-4">
                            <div className="flex items-center gap-2 mb-2 px-1 border-b border-secondary/10 pb-2">
                                <Award size={14} className="text-secondary" />
                                <h2 className="text-[10px] font-bold tracking-[0.3em] uppercase text-secondary/80">Professional_Credentials_Registry</h2>
                            </div>
                            <div className="max-h-96 overflow-y-auto pr-2 custom-scrollbar">
                                <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                                    {PROFILE_DATA.certifications.map((cert, i) => (
                                        <button
                                            key={i}
                                            onClick={() => setSelectedCert(cert)}
                                            className="hud-panel tactical-border p-4 border-b-2 border-b-secondary/20 hover:bg-secondary/10 transition-all flex flex-col items-center text-center gap-3 group relative overflow-hidden h-full"
                                        >
                                            <div className="absolute top-0 right-0 w-8 h-8 bg-secondary/10 rotate-45 transform translate-x-4 -translate-y-4"></div>
                                            <div className="w-12 h-12 rounded-full border border-secondary/20 flex items-center justify-center bg-secondary/10 group-hover:bg-secondary/30 group-hover:border-secondary transition-all">
                                                <Briefcase size={20} className="text-secondary" />
                                            </div>
                                            <div>
                                                <div className="text-[11px] font-bold text-white leading-tight uppercase mb-1 group-hover:text-secondary transition-colors line-clamp-2">{cert.title}</div>
                                                <div className="text-[9px] text-slate-500 uppercase font-mono tracking-tighter">{cert.issuer}</div>
                                                <div className="mt-2 text-[8px] text-primary/40 font-mono uppercase tracking-[0.2em] animate-pulse">Tactical_Inspect</div>
                                            </div>
                                        </button>
                                    ))}
                                </div>
                            </div>
                        </div>

                        {/* Industrial Analytics & Command Centers */}
                        <div className="mb-12">
                            <div className="flex items-center justify-between mb-6 px-1 border-b border-primary/20 pb-4">
                                <div className="flex items-center gap-3">
                                    <BarChart3 size={18} className="text-primary" />
                                    <h2 className="text-xs font-bold tracking-[0.4em] uppercase text-primary/80">Industrial_Analytics_Command_Centers</h2>
                                </div>
                                <div className="flex gap-2">
                                    {(PROFILE_DATA as any).dashboards.map((_: any, i: number) => (
                                        <button
                                            key={i}
                                            onClick={() => setDashIndex(i)}
                                            className={`w-2 h-2 rounded-full transition-all ${i === dashIndex ? 'bg-primary w-6' : 'bg-primary/20 hover:bg-primary/40'}`}
                                        />
                                    ))}
                                </div>
                            </div>

                            <div className="relative h-[500px] w-full group overflow-hidden rounded-xl border border-primary/20 shadow-2xl">
                                <AnimatePresence mode="wait">
                                    <motion.div
                                        key={dashIndex}
                                        initial={{ opacity: 0, x: 100 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        exit={{ opacity: 0, x: -100 }}
                                        transition={{ duration: 0.7, ease: "anticipate" }}
                                        className="absolute inset-0 cursor-pointer"
                                        onClick={() => setSelectedCert({
                                            title: (PROFILE_DATA as any).dashboards[dashIndex].title,
                                            url: (PROFILE_DATA as any).dashboards[dashIndex].image,
                                            description: (PROFILE_DATA as any).dashboards[dashIndex].description,
                                            issuer: (PROFILE_DATA as any).dashboards[dashIndex].platform
                                        })}
                                    >
                                        <img
                                            src={(PROFILE_DATA as any).dashboards[dashIndex].image}
                                            alt="Dashboard"
                                            className="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity duration-700"
                                        />
                                        <div className="absolute inset-0 bg-gradient-to-t from-[#050b14] via-transparent to-transparent" />

                                        <div className="absolute bottom-0 left-0 right-0 p-8 transform translate-y-4 group-hover:translate-y-0 transition-transform duration-500">
                                            <div className="bg-primary/10 backdrop-blur-md border-l-4 border-primary p-6 max-w-2xl">
                                                <div className="text-[10px] text-primary font-mono uppercase mb-2 tracking-[0.3em]">
                                                    {(PROFILE_DATA as any).dashboards[dashIndex].platform} // NODE_{dashIndex + 1}
                                                </div>
                                                <h3 className="text-4xl font-black text-white uppercase tracking-tighter mb-4 leading-none">
                                                    {(PROFILE_DATA as any).dashboards[dashIndex].title}
                                                </h3>
                                                <p className="text-slate-300 font-mono text-sm leading-relaxed mb-6 opacity-0 group-hover:opacity-100 transition-opacity duration-1000 delay-200">
                                                    {(PROFILE_DATA as any).dashboards[dashIndex].description}
                                                </p>
                                                <div className="flex items-center gap-4">
                                                    <button className="flex items-center gap-2 bg-primary text-black px-6 py-2 font-bold uppercase tracking-widest text-[10px] hover:bg-white transition-colors">
                                                        <Maximize2 size={14} />
                                                        Tactical_Inspect
                                                    </button>
                                                    <div className="flex items-center gap-2">
                                                        <div className="w-2 h-2 rounded-full bg-primary animate-pulse" />
                                                        <span className="text-[9px] text-primary/60 font-mono uppercase tracking-widest">Neural_Link_Stable</span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </motion.div>
                                </AnimatePresence>

                                {/* Slider Navigation */}
                                <button
                                    onClick={(e) => { e.stopPropagation(); setDashIndex((idx) => (idx - 1 + (PROFILE_DATA as any).dashboards.length) % (PROFILE_DATA as any).dashboards.length) }}
                                    className="absolute left-4 top-1/2 -translate-y-1/2 bg-black/40 backdrop-blur-md p-3 border border-primary/20 text-primary hover:bg-primary hover:text-black transition-all opacity-0 group-hover:opacity-100"
                                >
                                    <X className="rotate-90" />
                                </button>
                                <button
                                    onClick={(e) => { e.stopPropagation(); setDashIndex((idx) => (idx + 1) % (PROFILE_DATA as any).dashboards.length) }}
                                    className="absolute right-4 top-1/2 -translate-y-1/2 bg-black/40 backdrop-blur-md p-3 border border-primary/20 text-primary hover:bg-primary hover:text-black transition-all opacity-0 group-hover:opacity-100"
                                >
                                    <X className="-rotate-90" />
                                </button>
                            </div>
                        </div>

                        {/* Bottom Row: Academics */}
                        <div className="hud-panel p-6 border-t-2 border-primary/20 bg-primary/5">
                            <div className="flex items-center gap-2 mb-6 px-1 border-b border-primary/10 pb-2">
                                <Layers size={14} className="text-primary" />
                                <h2 className="text-xs font-bold tracking-[0.3em] uppercase text-primary/80">Academic_Infrastructure</h2>
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                {PROFILE_DATA.education.map((edu, i) => (
                                    <div key={i} className="hud-panel p-5 border-r-2 border-r-primary/30 group hover:bg-primary/5 transition-all">
                                        <div className="flex justify-between items-start mb-2">
                                            <h3 className="text-sm font-bold text-white uppercase group-hover:text-primary transition-colors tracking-wide">{edu.institution}</h3>
                                            <span className="text-[10px] text-primary font-mono bg-primary/15 px-2 py-1 rounded font-bold">{edu.period}</span>
                                        </div>
                                        <div className="text-xs text-primary/90 mb-3 font-mono uppercase tracking-tight font-semibold">{edu.degree}</div>
                                        <p className="text-xs text-slate-400 italic leading-relaxed border-l-2 border-primary/30 pl-4">{edu.details}</p>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* GitHub Strategic Portfolio: Tactical Command */}
                        <div className="mb-12">
                            <div className="flex items-center justify-between mb-8 px-1 border-b border-primary/20 pb-4">
                                <div className="flex items-center gap-3">
                                    <Github size={20} className="text-primary" />
                                    <h2 className="text-xs font-bold tracking-[0.4em] uppercase text-primary/80">Strategic_Asset_Repository[GITHUB]</h2>
                                </div>
                                <div className="flex items-center gap-4 text-[10px] font-mono text-primary/40 uppercase">
                                    <div className="flex items-center gap-1.5"><div className="w-1.5 h-1.5 rounded-full bg-green-500" /> SYNC_LOCAL</div>
                                    <div className="flex items-center gap-1.5"><div className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse" /> LIVE_ARCHIVE</div>
                                </div>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                                {PROFILE_DATA.projects.map((proj, i) => (
                                    <div key={i} className="hud-panel p-5 group flex flex-col justify-between border border-primary/20 hover:border-primary/60 transition-all duration-500 bg-slate-900/40 backdrop-blur-sm relative overflow-hidden shadow-lg">
                                        <div className="absolute top-0 right-0 w-16 h-16 bg-primary/5 -rotate-45 translate-x-10 -translate-y-10 group-hover:bg-primary/10 transition-colors" />

                                        <div>
                                            <div className="flex justify-between items-start mb-4">
                                                <div className="p-2 bg-primary/10 rounded group-hover:bg-primary/20 transition-colors">
                                                    <Terminal size={16} className="text-primary" />
                                                </div>
                                                <div className="flex gap-3 text-[10px] font-mono text-primary/60 font-bold">
                                                    <div className="flex items-center gap-1"><Star size={10} /> 12</div>
                                                    <div className="flex items-center gap-1"><GitFork size={10} /> 4</div>
                                                </div>
                                            </div>

                                            <h3 className="text-sm font-black text-white uppercase tracking-tight mb-3 group-hover:text-primary transition-colors leading-none">{proj.title}</h3>
                                            <p className="text-[11px] text-slate-300 leading-relaxed font-mono opacity-80 group-hover:opacity-100 transition-opacity mb-4 line-clamp-3">
                                                {proj.description}
                                            </p>
                                            <div className="flex items-center justify-between">
                                                <div className="flex gap-2 flex-wrap mb-2">
                                                    {proj.tech.map((t, j) => (
                                                        <span key={j} className="text-[11px] font-bold font-mono text-white bg-black/60 px-2.5 py-1 rounded border border-primary/50 shadow-[0_0_8px_rgba(34,211,238,0.2)] tracking-wide hover:bg-primary hover:text-black transition-all cursor-default">
                                                            {t}
                                                        </span>
                                                    ))}
                                                </div>
                                                <button
                                                    onClick={(e) => {
                                                        e.stopPropagation();
                                                        window.open(proj.githubUrl, "_blank");
                                                    }}
                                                    className="opacity-0 group-hover:opacity-100 p-1.5 hover:bg-primary/20 rounded transition-all text-primary"
                                                >
                                                    <Github size={14} />
                                                </button>
                                            </div>
                                            <div className="mt-4 pt-4 border-t border-primary/20 flex items-center justify-between">
                                                <button
                                                    onClick={() => setSelectedProject(proj)}
                                                    className="text-[9px] font-black text-primary uppercase tracking-[0.2em] hover:text-white transition-colors flex items-center gap-2"
                                                >
                                                    <Zap size={10} className="animate-pulse" />
                                                    Tactical_Briefing
                                                </button>
                                                <div className="text-[8px] text-slate-500 font-mono italic">REPO_ALPHA_V4</div>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>

                    {/* Right Section: Intel Log */}
                    <AnimatePresence>
                        {!rightPanelCollapsed && (
                            <motion.section
                                initial={{ width: 0, opacity: 0, x: 50 }}
                                animate={{ width: 288, opacity: 1, x: 0 }}
                                exit={{ width: 0, opacity: 0, x: 50 }}
                                className="hidden md:flex flex-col w-64 shrink-0 hud-panel rounded-lg p-1 border-secondary/30 perspective-right transition-all overflow-y-auto no-scrollbar"
                            >
                                <CornerBrackets />
                                <div className="bg-secondary/10 border-b border-secondary/30 p-3 mb-4 sticky top-0 z-10">
                                    <h2 className="text-secondary font-bold tracking-widest text-xs uppercase">Intel Feed</h2>
                                    <div className="text-[10px] text-secondary/60 font-mono">PUBLICATIONS & ASSETS</div>
                                </div>
                                <div className="flex-1 space-y-4 px-2 pb-6">
                                    <div className="text-[10px] font-mono text-secondary/40 uppercase mb-2 border-l border-secondary/30 pl-2">TECHNICAL_PUBLICATIONS</div>
                                    {PROFILE_DATA.publications?.map((pub, i) => (
                                        <div key={i} className="border border-secondary/20 p-3 bg-slate-900/40 rounded hover:border-secondary transition-all group">
                                            <h3 className="text-xs font-bold text-white mb-2 uppercase tracking-widest group-hover:text-secondary transition-colors leading-tight">{pub.title}</h3>
                                            <div className="text-[11px] text-slate-500 font-mono mb-2 uppercase tracking-tighter">{pub.issuer} // {pub.date}</div>
                                            <button
                                                onClick={() => setSelectedArticle(pub)}
                                                className="w-full text-[10px] bg-secondary/10 text-secondary py-1.5 rounded border border-secondary/20 hover:bg-secondary/20 transition-all uppercase tracking-widest font-bold"
                                            >
                                                Scan Briefing
                                            </button>
                                        </div>
                                    ))}

                                    <div className="text-xs font-mono text-primary/40 uppercase mt-6 mb-2 border-l border-primary/30 pl-2">MISSION_LOGS</div>
                                    {PROFILE_DATA.projects.map((proj, i) => (
                                        <div key={i} className="border border-primary/20 p-3 bg-slate-900/40 rounded hover:border-primary transition-all group">
                                            <h3 className="text-xs font-bold text-white mb-2 uppercase tracking-widest group-hover:text-primary transition-colors leading-tight">{proj.title}</h3>
                                            <div className="flex justify-between items-center text-[10px]">
                                                <span className="text-primary/70 font-mono">UNIT_{i + 1}</span>
                                                <div className="flex gap-0.5">
                                                    <div className="w-1.5 h-3 bg-primary animate-pulse" />
                                                    <div className="w-1.5 h-3 bg-primary/40" />
                                                </div>
                                            </div>
                                        </div>
                                    ))}

                                    <div className="text-xs font-mono text-cyan-500/40 uppercase mt-8 mb-4 border-l-2 border-cyan-500/30 pl-2">NASA_BEARING_DIAGNOSTICS</div>
                                    <div
                                        onClick={() => setShowSimModal(true)}
                                        className={`hud-panel p-4 border-2 transition-all group cursor-pointer ${simStatus === 'anomaly' ? 'bg-red-500/5 border-red-500/30 hover:border-red-500/60' : 'bg-cyan-500/5 border-cyan-500/20 hover:border-cyan-500/50'}`}
                                    >
                                        <div className="flex items-center justify-between mb-2">
                                            <span className={`text-[9px] font-mono tracking-widest uppercase italic ${simStatus === 'anomaly' ? 'text-red-500 animate-pulse' : 'text-cyan-500'}`}>
                                                {simStatus === 'anomaly' ? 'Anomaly_Detected: [CRITICAL]' : 'Node_Status: [ONLINE]'}
                                            </span>
                                            <div className="flex gap-1">
                                                <motion.div animate={{ height: [4, 12, 6] }} transition={{ repeat: Infinity, duration: 0.5 }} className={`w-1 ${simStatus === 'anomaly' ? 'bg-red-500' : 'bg-cyan-500'}`} />
                                                <motion.div animate={{ height: [8, 4, 10] }} transition={{ repeat: Infinity, duration: 0.7 }} className={`w-1 ${simStatus === 'anomaly' ? 'bg-red-500' : 'bg-cyan-500'}`} />
                                            </div>
                                        </div>

                                        <div className="space-y-3">
                                            <div>
                                                <div className="flex justify-between text-[8px] font-mono text-slate-400 mb-1">
                                                    <span>BEARING_VIBRATION_HZ</span>
                                                    <span className={simStatus === 'anomaly' ? 'text-red-500' : 'text-cyan-500'}>{simStatus === 'anomaly' ? 'HIGH_VAR' : 'STABLE'}</span>
                                                </div>
                                                <div className="w-full h-1 bg-slate-800 rounded-full overflow-hidden">
                                                    <motion.div animate={{ width: simStatus === 'anomaly' ? ["60%", "95%", "75%"] : ["45%", "65%", "55%"] }} transition={{ duration: 0.5, repeat: Infinity, ease: "easeInOut" }} className={`h-full ${simStatus === 'anomaly' ? 'bg-red-500' : 'bg-cyan-500'}`} />
                                                </div>
                                            </div>
                                            <div>
                                                <div className="flex justify-between text-[8px] font-mono text-slate-400 mb-1">
                                                    <span>ANOMALY_CONFIDENCE_RAG</span>
                                                    <span className={simStatus === 'anomaly' ? 'text-red-500' : 'text-green-500'}>{simStatus === 'anomaly' ? '92.4%' : '0.02%'}</span>
                                                </div>
                                                <div className="w-full h-1 bg-slate-800 rounded-full overflow-hidden">
                                                    <motion.div animate={{ width: simStatus === 'anomaly' ? "92.4%" : "2%" }} className={`h-full ${simStatus === 'anomaly' ? 'bg-red-500' : 'bg-green-500'}`} />
                                                </div>
                                            </div>
                                        </div>

                                        <div className="mt-4 pt-4 border-t border-white/5 text-[8px] font-mono text-white/30 leading-relaxed italic uppercase tracking-tighter">
                                            {simStatus === 'anomaly' ? '>>> CRITICAL_FAILURE_PREDICTED' : '>>> Normal_Operational_Signals'}<br />
                                            {">>> CLICK TO RESOLVE ANOMALY"}
                                        </div>
                                    </div>
                                </div>
                            </motion.section>
                        )}
                    </AnimatePresence>

                    {/* Tactical Case Study Modal */}
                    <AnimatePresence>
                        {selectedProject && (
                            <div className="fixed inset-0 z-[150] flex items-center justify-center p-4 bg-black/95 backdrop-blur-md">
                                <motion.div
                                    initial={{ opacity: 0, y: 50 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, y: 50 }}
                                    className="hud-panel w-full max-w-4xl max-h-[85vh] overflow-hidden flex flex-col relative border-2 border-primary/50 shadow-neon bg-[#050b14]"
                                >
                                    <div className="p-6 border-b border-primary/30 flex items-center justify-between bg-primary/10">
                                        <div className="flex items-center gap-4">
                                            <div className="p-3 bg-primary/20 border border-primary/40 rounded-lg">
                                                <Zap className="text-primary animate-pulse" size={24} />
                                            </div>
                                            <div>
                                                <h2 className="text-xl font-black text-white uppercase tracking-tighter leading-tight">{selectedProject.title}</h2>
                                                <div className="text-[10px] text-primary/60 font-mono uppercase tracking-[0.3em]">Project_Architecture // Deep_Dive</div>
                                            </div>
                                        </div>
                                        <button
                                            onClick={() => setSelectedProject(null)}
                                            className="p-2 hover:bg-primary/20 rounded-full transition-colors text-primary"
                                        >
                                            <X size={24} />
                                        </button>
                                    </div>

                                    <div className="flex-1 overflow-y-auto p-10 no-scrollbar">
                                        <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
                                            <div className="md:col-span-2 space-y-8">
                                                <section>
                                                    <h4 className="text-[10px] font-bold text-primary uppercase tracking-[0.4em] mb-4 border-l-2 border-primary pl-3">Mission_Parameters</h4>
                                                    <p className="text-lg text-slate-200 leading-relaxed font-light italic">
                                                        "{selectedProject.description}"
                                                    </p>
                                                </section>

                                                <section>
                                                    <h4 className="text-[10px] font-bold text-primary uppercase tracking-[0.4em] mb-4 border-l-2 border-primary pl-3">Architectural_Blueprint</h4>
                                                    <div className="p-6 bg-primary/5 border border-primary/20 rounded-lg relative overflow-hidden group">
                                                        <div className="absolute top-0 right-0 w-32 h-32 bg-primary/5 -rotate-45 transform translate-x-16 -translate-y-16 group-hover:bg-primary/10 transition-all"></div>
                                                        <p className="text-sm text-slate-300 leading-7 font-mono relative z-10">
                                                            {selectedProject.architecture}
                                                        </p>
                                                    </div>
                                                </section>

                                                <section className="grid grid-cols-2 gap-6">
                                                    <div className="hud-panel p-4 border-secondary/20 bg-secondary/5">
                                                        <div className="text-[9px] text-secondary font-bold uppercase tracking-widest mb-2">Deploy_Status</div>
                                                        <div className="text-xl font-black text-white uppercase italic tracking-tighter">Production</div>
                                                    </div>
                                                    <div className="hud-panel p-4 border-green-500/20 bg-green-500/5">
                                                        <div className="text-[9px] text-green-500 font-bold uppercase tracking-widest mb-2">Health_Index</div>
                                                        <div className="text-xl font-black text-white uppercase italic tracking-tighter">98.4%</div>
                                                    </div>
                                                </section>
                                            </div>

                                            <div className="space-y-8">
                                                <section>
                                                    <h4 className="text-[10px] font-bold text-primary uppercase tracking-[0.4em] mb-4">Technical_Stack</h4>
                                                    <div className="flex flex-col gap-2">
                                                        {selectedProject.tech.map((t: string, j: number) => (
                                                            <div key={j} className="flex items-center gap-3 p-3 bg-slate-900/50 border border-primary/20 hover:border-primary/50 transition-all rounded">
                                                                <Box size={14} className="text-primary/60" />
                                                                <span className="text-xs font-mono text-slate-300 lowercase">{t}</span>
                                                            </div>
                                                        ))}
                                                    </div>
                                                </section>

                                                <section>
                                                    <h4 className="text-[10px] font-bold text-primary uppercase tracking-[0.4em] mb-4">Repository_Intel</h4>
                                                    <a
                                                        href={selectedProject.githubUrl}
                                                        target="_blank"
                                                        className="w-full flex items-center justify-center gap-3 bg-primary text-black py-4 font-black uppercase tracking-widest text-[11px] hover:bg-white transition-all shadow-neon"
                                                    >
                                                        <Github size={18} />
                                                        View Source Alpha
                                                    </a>
                                                </section>
                                            </div>
                                        </div>
                                    </div>

                                    <div className="p-4 border-t border-primary/20 bg-primary/5 flex justify-between items-center px-8">
                                        <div className="flex gap-6">
                                            <div className="flex items-center gap-2">
                                                <div className="w-1.5 h-1.5 rounded-full bg-green-500" />
                                                <span className="text-[9px] text-slate-500 font-mono uppercase tracking-[0.2em]">NODE_SYNC_SUCCESS</span>
                                            </div>
                                            <div className="flex items-center gap-2">
                                                <div className="w-1.5 h-1.5 rounded-full bg-primary" />
                                                <span className="text-[9px] text-slate-500 font-mono uppercase tracking-[0.2em]">ENCRYPTED_STREAM_ON</span>
                                            </div>
                                        </div>
                                        <span className="text-[10px] font-black text-primary/40 tracking-[0.5em] italic">AEGIS-OS // STRATEGIC_ASSET</span>
                                    </div>
                                </motion.div>
                            </div>
                        )}
                    </AnimatePresence>

                    {/* NASA Bearing Diagnostic Modal */}
                    <AnimatePresence>
                        {showSimModal && (
                            <div className="fixed inset-0 z-[160] flex items-center justify-center p-4 bg-black/90 backdrop-blur-xl">
                                <motion.div
                                    initial={{ opacity: 0, scale: 0.9, y: 20 }}
                                    animate={{ opacity: 1, scale: 1, y: 0 }}
                                    exit={{ opacity: 0, scale: 0.9, y: 20 }}
                                    className={`hud-panel w-full max-w-4xl max-h-[85vh] overflow-hidden flex flex-col relative border-2 shadow-2xl ${simStatus === 'anomaly' ? 'border-red-500/50 shadow-red-500/20' : 'border-cyan-500/50 shadow-cyan-500/20'} bg-[#050b14]`}
                                >
                                    <div className={`p-6 border-b flex items-center justify-between ${simStatus === 'anomaly' ? 'bg-red-500/10 border-red-500/30' : 'bg-cyan-500/10 border-cyan-500/30'}`}>
                                        <div className="flex items-center gap-4">
                                            <div className={`p-3 border rounded-lg ${simStatus === 'anomaly' ? 'bg-red-500/20 border-red-500/40 text-red-500' : 'bg-cyan-500/20 border-cyan-500/40 text-cyan-500'}`}>
                                                <Activity size={24} className={simStatus === 'anomaly' ? 'animate-pulse' : ''} />
                                            </div>
                                            <div>
                                                <h2 className="text-xl font-black text-white uppercase tracking-tighter">NASA_BEARING_DIAGNOSTICS</h2>
                                                <div className={`text-[10px] font-mono uppercase tracking-[0.3em] ${simStatus === 'anomaly' ? 'text-red-500' : 'text-cyan-500'}`}>
                                                    Dataset_v4 // {simStatus === 'anomaly' ? 'FAULT_DETECTED' : 'SYSTEM_SYNCED'}
                                                </div>
                                            </div>
                                        </div>
                                        <button onClick={() => setShowSimModal(false)} className="p-2 hover:bg-white/10 rounded-full transition-colors text-white/50 hover:text-white">
                                            <X size={24} />
                                        </button>
                                    </div>

                                    <div className="flex-1 overflow-y-auto p-8 no-scrollbar">
                                        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                                            {/* Column 1: Vibration Chart */}
                                            <div className="lg:col-span-2 space-y-6">
                                                <section className="hud-panel p-6 bg-black/40 border-white/5">
                                                    <h4 className="text-[10px] font-bold text-primary/60 uppercase tracking-[0.4em] mb-6">Real-Time_Vibration_Spectrum</h4>
                                                    <div className="h-48 flex items-end gap-1 px-2 border-b border-white/10 pb-1">
                                                        {Array.from({ length: 40 }).map((_, i) => (
                                                            <motion.div
                                                                key={i}
                                                                animate={{
                                                                    height: simStatus === 'anomaly'
                                                                        ? [
                                                                            Math.random() * 40 + (i % 5 === 0 ? 60 : 20) + "%",
                                                                            Math.random() * 50 + (i % 5 === 0 ? 80 : 30) + "%",
                                                                            Math.random() * 30 + (i % 5 === 0 ? 50 : 10) + "%"
                                                                        ]
                                                                        : [
                                                                            Math.random() * 20 + 10 + "%",
                                                                            Math.random() * 30 + 15 + "%",
                                                                            Math.random() * 10 + 5 + "%"
                                                                        ]
                                                                }}
                                                                transition={{ repeat: Infinity, duration: simStatus === 'anomaly' ? 0.3 : 1.5, delay: i * 0.05 }}
                                                                className={`flex-1 rounded-t-sm ${simStatus === 'anomaly' ? (i % 5 === 0 ? 'bg-red-500' : 'bg-red-500/30') : 'bg-cyan-500/40'}`}
                                                            />
                                                        ))}
                                                    </div>
                                                    <div className="flex justify-between text-[8px] font-mono text-white/20 mt-2 px-2">
                                                        <span>0Hz</span>
                                                        <span>1200Hz</span>
                                                        <span>2400Hz</span>
                                                        <span>3600Hz (Harmonics)</span>
                                                    </div>
                                                </section>

                                                <div className="grid grid-cols-2 gap-4">
                                                    <div className="hud-panel p-4 border-white/5 bg-white/2">
                                                        <div className="text-[9px] text-slate-500 font-bold uppercase mb-2">RMS_VIBRATION</div>
                                                        <div className={`text-xl font-black font-mono tracking-tighter ${simStatus === 'anomaly' ? 'text-red-500' : 'text-white'}`}>
                                                            {simStatus === 'anomaly' ? '0.248g' : '0.042g'}
                                                        </div>
                                                    </div>
                                                    <div className="hud-panel p-4 border-white/5 bg-white/2">
                                                        <div className="text-[9px] text-slate-500 font-bold uppercase mb-2">KURTOSIS_INDEX</div>
                                                        <div className={`text-xl font-black font-mono tracking-tighter ${simStatus === 'anomaly' ? 'text-orange-500' : 'text-white'}`}>
                                                            {simStatus === 'anomaly' ? '4.82' : '2.95'}
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>

                                            {/* Column 2: Diagnostic Intel */}
                                            <div className="space-y-6">
                                                <section>
                                                    <h4 className="text-[10px] font-bold text-primary/60 uppercase tracking-[0.4em] mb-4">Fault_Analysis</h4>
                                                    <div className="space-y-3">
                                                        <div className={`p-3 border rounded text-xs font-mono transition-all ${simStatus === 'anomaly' ? 'border-red-500/40 bg-red-500/10 text-red-100' : 'border-white/10 bg-white/5 text-slate-400'}`}>
                                                            <div className="flex justify-between mb-1">
                                                                <span>INNER_RACE_FAULT</span>
                                                                <span>{simStatus === 'anomaly' ? 'HIGH_PROB' : 'NORMAL'}</span>
                                                            </div>
                                                            <div className="w-full h-1 bg-black/40 rounded-full overflow-hidden">
                                                                <motion.div animate={{ width: simStatus === 'anomaly' ? "88%" : "4%" }} className={`h-full ${simStatus === 'anomaly' ? 'bg-red-500' : 'bg-cyan-500'}`} />
                                                            </div>
                                                        </div>
                                                        <div className={`p-3 border rounded text-xs font-mono transition-all ${simStatus === 'anomaly' ? 'border-orange-500/40 bg-orange-500/10 text-orange-100' : 'border-white/10 bg-white/5 text-slate-400'}`}>
                                                            <div className="flex justify-between mb-1">
                                                                <span>OUTER_RACE_FAULT</span>
                                                                <span>{simStatus === 'anomaly' ? 'MODERATE' : 'NORMAL'}</span>
                                                            </div>
                                                            <div className="w-full h-1 bg-black/40 rounded-full overflow-hidden">
                                                                <motion.div animate={{ width: simStatus === 'anomaly' ? "42%" : "2%" }} className={`h-full ${simStatus === 'anomaly' ? 'bg-orange-500' : 'bg-cyan-500'}`} />
                                                            </div>
                                                        </div>
                                                    </div>
                                                </section>

                                                <section className="p-4 bg-primary/5 border border-primary/20 rounded-lg">
                                                    <div className="flex gap-2 items-center mb-2">
                                                        <Brain size={14} className="text-primary" />
                                                        <span className="text-[10px] font-bold text-primary uppercase tracking-widest">Architect_Recommendation</span>
                                                    </div>
                                                    <p className="text-[10px] text-slate-300 leading-relaxed font-mono italic">
                                                        {simStatus === 'anomaly'
                                                            ? "DETECTED: Inner race spalling confirmed via vibration harmonics at 1200Hz. Recommend immediate lubrication cycle and operational load reduction to prevent catastrophic bearing seizure."
                                                            : "OPTIMAL: Predictive model confirms operational signature matches baseline. Continuous monitoring active."
                                                        }
                                                    </p>
                                                </section>

                                                {simStatus === 'anomaly' && (
                                                    <button
                                                        onClick={handleResolveAnomaly}
                                                        className="w-full bg-red-500 hover:bg-red-600 text-black py-4 font-black uppercase tracking-[0.3em] text-xs shadow-neon transition-all hover:scale-[1.02] active:scale-95"
                                                    >
                                                        INITIATE_REPAIR_PROTOCOL
                                                    </button>
                                                )}

                                                {simStatus === 'resolving' && (
                                                    <div className="w-full bg-white/5 border border-white/20 p-4 text-center">
                                                        <div className="flex items-center justify-center gap-3 mb-3">
                                                            <motion.div
                                                                animate={{ rotate: 360 }}
                                                                transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
                                                                className="text-primary"
                                                            >
                                                                <Settings size={20} />
                                                            </motion.div>
                                                            <span className="text-[10px] font-bold text-primary uppercase tracking-widest animate-pulse">Resolving Anomaly...</span>
                                                        </div>
                                                        <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                                                            <motion.div
                                                                initial={{ width: 0 }}
                                                                animate={{ width: "100%" }}
                                                                transition={{ duration: 4 }}
                                                                className="h-full bg-primary"
                                                            />
                                                        </div>
                                                    </div>
                                                )}

                                                {simStatus === 'resolved' && (
                                                    <div className="w-full bg-green-500/10 border border-green-500/30 p-4 text-center rounded-lg shadow-neon-green">
                                                        <div className="flex flex-col items-center gap-2">
                                                            <CheckCircle className="text-green-500" size={32} />
                                                            <span className="text-xs font-black text-green-500 uppercase tracking-widest">Anomaly Resolved</span>
                                                            <p className="text-[9px] text-green-500/60 font-mono">System stability restored to 99.98% baseline.</p>
                                                            <button
                                                                onClick={() => {
                                                                    setSimStatus('normal');
                                                                    setShowSimModal(false);
                                                                }}
                                                                className="mt-4 text-[9px] border border-green-500/40 px-4 py-2 hover:bg-green-500 hover:text-black transition-all uppercase font-bold"
                                                            >
                                                                Return to Ops
                                                            </button>
                                                        </div>
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    </div>

                                    <div className="p-4 bg-black/40 border-t border-white/5 flex justify-between items-center text-[8px] font-mono text-white/20 px-8">
                                        <span>DIAGNOSTIC_SESSION_ID: 0x-NASA-B-4921</span>
                                        <span className="animate-pulse">STREAMLINK_ACTIVE_SECURE</span>
                                    </div>
                                </motion.div>
                            </div>
                        )}
                    </AnimatePresence>
                </div>
            </main>

            {/* Footer Container */}
            <footer className="fixed bottom-0 left-0 w-full h-10 flex items-center justify-between px-6 z-50 border-t border-primary/30 bg-[#050b14]/90 backdrop-blur-sm" >
                <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
                        <span className="text-[10px] font-mono text-primary/70 uppercase tracking-widest">System_Optimal</span>
                    </div>
                    <div className="hidden md:flex items-center gap-4 border-l border-primary/20 pl-4">
                        <span className="text-[10px] font-mono text-slate-500">LATENCY: 12ms</span>
                        <span className="text-[10px] font-mono text-slate-500">SEC_LEVEL: 4 [RESTRICTED]</span>
                    </div>
                </div>
                <div className="flex items-center gap-6">
                    <div className="flex items-center gap-2">
                        <span className="text-[10px] font-mono text-primary/50 uppercase">Neural_Load</span>
                        <div className="w-20 h-1 bg-slate-800 rounded-full overflow-hidden">
                            <motion.div initial={{ width: 0 }} animate={{ width: "42%" }} className="h-full bg-primary" />
                        </div>
                    </div>
                    <span className="text-[10px] font-mono text-primary/70 tracking-widest hidden sm:block">AEGIS_OS_V4.0.2</span>
                </div>
            </footer>

            {/* Neural Modal */}
            <AnimatePresence>
                {
                    showRAGModal && (
                        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
                            <motion.div
                                initial={{ scale: 0.9, opacity: 0 }}
                                animate={{ scale: 1, opacity: 1 }}
                                exit={{ scale: 0.9, opacity: 0 }}
                                className="w-full max-w-4xl h-[80vh] bg-black border border-primary/30 rounded-lg shadow-2xl relative overflow-hidden"
                            >
                                <button
                                    onClick={() => setShowRAGModal(false)}
                                    className="absolute top-4 right-4 text-primary/50 hover:text-primary z-10"
                                >
                                    <X size={24} />
                                </button>
                                <AskTheManual />
                            </motion.div>
                        </div>
                    )
                }
            </AnimatePresence>

            {/* Floating Neural Link Trigger */}
            {
                !showNeuralLink && (
                    <motion.button
                        initial={{ scale: 0, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        whileHover={{ scale: 1.1, boxShadow: "0 0 20px rgba(0, 240, 255, 0.4)" }}
                        onClick={() => setShowNeuralLink(true)}
                        className="fixed bottom-14 left-6 w-12 h-12 rounded-full bg-black border-2 border-primary/50 flex items-center justify-center text-primary z-[60] shadow-neon group"
                    >
                        <Brain size={24} className="group-hover:animate-pulse" />
                        <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-black animate-pulse" />
                    </motion.button>
                )
            }

            {/* Floating Neural Link Widget */}
            <AnimatePresence>
                {
                    showNeuralLink && (
                        <motion.div
                            initial={{ x: 100, opacity: 0 }}
                            animate={{ x: 0, opacity: 1 }}
                            exit={{ x: 100, opacity: 0 }}
                            className="fixed bottom-16 right-6 w-full max-w-sm z-[100] hud-panel rounded-lg shadow-neon border-2 border-primary/50 bg-black/95 p-4 font-mono overflow-hidden"
                            style={{ position: 'fixed', left: 'auto' }}
                        >
                            <CornerBrackets />
                            <div className="flex items-center justify-between border-b border-primary/30 pb-2 mb-4">
                                <div className="flex items-center gap-2">
                                    <Brain size={18} className="text-primary" />
                                    <span className="text-primary font-bold tracking-widest text-sm uppercase italic">Neural_Liaison_Handshake</span>
                                </div>
                                <div className="flex items-center gap-3">
                                    <div className="flex items-center gap-1.5 bg-green-500/10 px-2 py-0.5 rounded border border-green-500/20">
                                        <div className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
                                        <span className="text-green-500 text-[9px] font-bold tracking-widest uppercase">Online</span>
                                    </div>
                                    <button onClick={() => setShowNeuralLink(false)} className="text-primary/50 hover:text-primary transition-colors"><X size={16} /></button>
                                </div>
                            </div>

                            <div className="h-72 overflow-y-auto custom-scrollbar space-y-3 text-[11px] mb-4 pr-2">
                                <div className="opacity-40 italic">{">>> AEGIS-OS PERSPECTIVE ENGAGED."}</div>
                                <div className="opacity-40">
                                    <span className="text-green-500">root@sys:~$</span> handshake --target LIAISON --auth RECRUITER_LVL_1
                                </div>
                                <div className="opacity-40 pb-2 border-b border-primary/10">
                                    <span className="text-green-500">root@sys:~$</span> status --ready
                                </div>
                                <div className="text-primary/90 pl-3 border-l border-primary/30 leading-relaxed whitespace-pre-wrap font-display tracking-tight">
                                    {aiResponse || ">>> HANDSHAKE_ESTABLISHED. I am the Aegis-OS Liaison. I have full clearance to brief you on Tahir's $750M marine engineering milestones and Industrial-AI research. State your inquiry regarding personnel capabilities."}
                                </div>
                                {isTyping && (
                                    <motion.div animate={{ opacity: [0.4, 1] }} transition={{ repeat: Infinity }} className="text-primary italic">
                                        {">>> DECRYPTING_BIOMETRIC_DATA..."}
                                    </motion.div>
                                )}
                            </div>

                            <div className="flex gap-2 items-center border-t border-primary/20 pt-3 bg-black/50">
                                <span className="text-green-500 text-xs">$</span>
                                <input
                                    type="text"
                                    autoFocus
                                    value={query}
                                    onChange={(e) => setQuery(e.target.value)}
                                    onKeyDown={(e) => e.key === "Enter" && handleAsk()}
                                    placeholder="TYPE_NEURAL_QUERY..."
                                    className="flex-1 bg-transparent border-none focus:ring-0 p-0 text-primary placeholder:text-primary/20 text-xs font-mono"
                                />
                                <button
                                    onClick={handleAsk}
                                    disabled={isTyping}
                                    className="text-[10px] font-bold text-primary border border-primary/40 px-3 py-1 hover:bg-primary hover:text-black transition-all shadow-[0_0_10px_rgba(0,240,255,0.2)]"
                                >
                                    TRANSMIT
                                </button>
                            </div>
                        </motion.div>
                    )
                }
            </AnimatePresence>

            {/* Large Certificate Preview Modal */}
            <AnimatePresence>
                {
                    selectedCert && (
                        <div className="fixed inset-0 z-[150] flex items-center justify-center p-4 bg-black/90 backdrop-blur-xl">
                            <motion.div
                                initial={{ scale: 0.8, opacity: 0 }}
                                animate={{ scale: 1, opacity: 1 }}
                                exit={{ scale: 0.8, opacity: 0 }}
                                className="w-full max-w-5xl h-[90vh] bg-[#050b14] border-2 border-secondary/40 rounded-xl shadow-neon-amber relative flex flex-col overflow-hidden"
                            >
                                <div className="bg-secondary/10 border-b border-secondary/30 p-4 flex justify-between items-center">
                                    <div className="flex items-center gap-3">
                                        <Award className="text-secondary" />
                                        <div>
                                            <h3 className="text-white font-bold uppercase tracking-widest">{selectedCert.title}</h3>
                                            <p className="text-[10px] text-secondary/60 font-mono uppercase">{selectedCert.issuer}</p>
                                        </div>
                                    </div>
                                    <button onClick={() => setSelectedCert(null)} className="text-secondary/50 hover:text-secondary p-2 transition-colors">
                                        <X size={28} />
                                    </button>
                                </div>
                                <div className="flex-1 overflow-auto p-4 flex items-center justify-center bg-black/40">
                                    {selectedCert.url.endsWith('.pdf') ? (
                                        <iframe src={selectedCert.url} className="w-full h-full border-none rounded" title="Certificate PDF" />
                                    ) : (
                                        <img src={selectedCert.url} alt={selectedCert.title} className="max-w-full max-h-full object-contain shadow-2xl" />
                                    )}
                                </div>
                                <div className="p-4 bg-black/60 border-t border-secondary/20 text-center">
                                    <p className="text-slate-400 text-sm font-mono italic max-w-2xl mx-auto">{selectedCert.description}</p>
                                    <a
                                        href={selectedCert.url}
                                        target="_blank"
                                        className="inline-block mt-4 text-[10px] bg-secondary/20 text-secondary border border-secondary/30 px-6 py-2 hover:bg-secondary hover:text-black transition-all uppercase font-bold tracking-[0.3em]"
                                    >
                                        Open Original Asset
                                    </a>
                                </div>
                            </motion.div>
                        </div>
                    )
                }
            </AnimatePresence>

            {/* Documentation Legend Modal */}
            <AnimatePresence>
                {showReadmeModal && (
                    <div className="fixed inset-0 z-[150] flex items-center justify-center p-4 bg-black/95 backdrop-blur-md">
                        <motion.div
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            className="hud-panel w-full max-w-4xl max-h-[85vh] overflow-hidden flex flex-col relative border-2 border-red-500/50 shadow-neon"
                        >
                            <div className="p-4 border-b border-red-500/30 flex items-center justify-between bg-red-500/10">
                                <div className="flex items-center gap-3">
                                    <FileText className="text-red-500" size={20} />
                                    <h2 className="text-sm font-black text-red-500 uppercase tracking-[0.4em]">AEGIS-OS // DEVELOPMENT_MANUAL</h2>
                                </div>
                                <button
                                    onClick={() => setShowReadmeModal(false)}
                                    className="p-1.5 hover:bg-red-500/20 rounded-full transition-colors text-red-500"
                                >
                                    <X size={20} />
                                </button>
                            </div>

                            <div className="flex-1 overflow-y-auto p-8 no-scrollbar bg-black/50">
                                <div className="space-y-6 text-slate-300 markdown-content">
                                    <ReactMarkdown
                                        components={{
                                            h1: ({ node, ...props }) => <h1 className="text-xl font-bold text-red-500 mb-4 uppercase tracking-widest border-b border-red-500/30 pb-2" {...props} />,
                                            h2: ({ node, ...props }) => <h2 className="text-lg font-bold text-white mt-6 mb-3 uppercase tracking-wider" {...props} />,
                                            h3: ({ node, ...props }) => <h3 className="text-base font-bold text-slate-200 mt-4 mb-2 uppercase" {...props} />,
                                            code: ({ node, ...props }) => <code className="bg-red-500/10 text-red-400 px-1 py-0.5 rounded text-[12px]" {...props} />,
                                            pre: ({ node, ...props }) => <pre className="bg-slate-900/50 border border-red-500/20 p-4 rounded-lg overflow-x-auto text-slate-300 my-4" {...props} />,
                                            ul: ({ node, ...props }) => <ul className="list-disc list-inside space-y-1 ml-2" {...props} />,
                                            ol: ({ node, ...props }) => <ol className="list-decimal list-inside space-y-1 ml-2" {...props} />,
                                            a: ({ node, ...props }) => <a className="text-cyan-400 hover:text-cyan-300 underline underline-offset-4" {...props} />,
                                        }}
                                    >
                                        {readmeContent}
                                    </ReactMarkdown>
                                </div>
                            </div>

                            <div className="p-3 border-t border-red-500/20 bg-red-500/5 flex justify-between items-center text-[10px] uppercase font-bold text-red-500/60 tracking-widest px-6">
                                <span>V4.0.2 // STABLE_READY</span>
                                <span>DECENTRALIZED ARCHITECTURE</span>
                            </div>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>

            {/* Publication Preview Modal */}
            <AnimatePresence>
                {
                    selectedArticle && (
                        <div className="fixed inset-0 z-[150] flex items-center justify-center p-4 bg-black/95 backdrop-blur-md">
                            <motion.div
                                initial={{ x: 500, opacity: 0 }}
                                animate={{ x: 0, opacity: 1 }}
                                exit={{ x: 500, opacity: 0 }}
                                className="w-full max-w-3xl h-[85vh] bg-[#050b14] border border-primary/30 rounded-lg shadow-2xl relative flex flex-col"
                            >
                                <div className="bg-primary/10 border-b border-primary/30 p-4 flex justify-between items-center">
                                    <div className="flex items-center gap-3 text-primary">
                                        <Globe size={20} />
                                        <span className="font-bold uppercase tracking-[0.2em]">{selectedArticle.issuer} // PERSPECTIVE</span>
                                    </div>
                                    <button onClick={() => setSelectedArticle(null)} className="text-primary/50 hover:text-primary"><X size={24} /></button>
                                </div>
                                <div className="flex-1 overflow-y-auto p-8 font-display">
                                    <h2 className="text-2xl font-bold text-white mb-6 uppercase tracking-tighter leading-tight border-b border-primary/10 pb-4">{selectedArticle.title}</h2>
                                    <div className="text-primary/60 text-xs font-mono mb-8 flex gap-4 uppercase">
                                        <span>Tahir Yamin</span>
                                        <span>{selectedArticle.date}</span>
                                    </div>
                                    <div className="text-slate-300 leading-relaxed text-lg space-y-6">
                                        <div className="bg-primary/5 p-4 border-l-2 border-primary italic text-sm">
                                            Summary: {selectedArticle.summary}
                                        </div>
                                        <p className="opacity-80">This article investigates high-stakes engineering milestones through the lens of Industrial AI models. Tahir Yamin explores the intersection of traditional project management and agentic systems.</p>
                                        <div className="py-12 flex flex-col items-center gap-6 border-y border-primary/10 my-8">
                                            <div className="w-16 h-16 rounded-full border border-primary/30 flex items-center justify-center animate-pulse">
                                                <Brain className="text-primary" />
                                            </div>
                                            <div className="text-center">
                                                <p className="text-xs font-mono text-primary/50 uppercase mb-4 tracking-widest leading-relaxed">External Link Encryption Required to proceed reading...</p>
                                                <a
                                                    href={selectedArticle.url}
                                                    target="_blank"
                                                    className="bg-primary text-black px-8 py-3 font-bold uppercase tracking-[0.2em] transform hover:scale-105 transition-all shadow-neon"
                                                >
                                                    Read Full Article on Medium
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </motion.div>
                        </div>
                    )
                }
            </AnimatePresence>
        </div>
    );
}
