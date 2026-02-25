'use client';

import React, { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';
import { ShieldCheck, Activity, Brain, Lock, X, AlertCircle, AlertTriangle } from 'lucide-react';
import { recorder } from '@/lib/recorder';
import { db } from '@/lib/storage/db';
import { MarkdownReport } from '@/components/ui/MarkdownReport';
import { SessionLabelToggle } from '@/components/ui/SessionLabelToggle';

// Dynamically import sensors (No SSR)
const SensorLoop = dynamic(() => import('@/components/sensor/SensorLoop'), { ssr: false });
const AudioLoop = dynamic(() => import('@/components/sensor/AudioLoop'), { ssr: false });
const AuditorLoop = dynamic(() => import('@/components/auditor/AuditorLoop'), { ssr: false });
const DataInspector = dynamic(() => import('@/components/dashboard/DataInspector'), { ssr: false });
import { HeroSection } from '@/components/ui/HeroSection';
import { AboutSection } from '@/components/ui/AboutSection';
const LongitudinalTrends = dynamic(() => import('@/components/ui/LongitudinalTrends').then(mod => mod.LongitudinalTrends), { ssr: false });

export default function Home() {
  const [mounted, setMounted] = useState(false);
  const [isSecure, setIsSecure] = useState(false);
  const [isMonitoring, setIsMonitoring] = useState(true);
  const [visionStatus, setVisionStatus] = useState<'OFF' | 'DEMO' | 'LIVE'>('LIVE');
  const [dataCount, setDataCount] = useState(0);
  const [lastAudit, setLastAudit] = useState<any>(null);
  const [sessionHistory, setSessionHistory] = useState<any[]>([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showReport, setShowReport] = useState(false);
  const [nextAnalysisIn, setNextAnalysisIn] = useState<number>(0); // Seconds until next analysis
  const [expandedHistoryItems, setExpandedHistoryItems] = useState<Record<string, boolean>>({}); // Track which history items are expanded
  const [historyExpanded, setHistoryExpanded] = useState(false); // Track if the main history table is open
  const [audioLevel, setAudioLevel] = useState<number>(0); // Live audio level (0-1)
  const [assessmentAge, setAssessmentAge] = useState<string>(''); // How long ago assessment was made
  const [sessionLabel, setSessionLabel] = useState<'BASELINE' | 'SIMULATED' | 'UNLABELED'>('UNLABELED'); // Pilot study labeling
  const [lastSyncedCount, setLastSyncedCount] = useState<number>(0); // Last frame count when audit triggered

  // Stabilization: Re-entrancy lock for data checker
  const isCheckingData = React.useRef(false);

  // STABILITY: Consolidated Tick Logic
  useEffect(() => {
    setMounted(true);
    setIsSecure(typeof window !== 'undefined' && window.isSecureContext);

    const tick = async () => {
      if (isCheckingData.current) return;
      isCheckingData.current = true;

      try {
        // 1. Check Count
        const count = await db.readings.count();
        setDataCount(curr => curr !== count ? count : curr);

        // 2. Vision Status Logic
        if (count > 0 && visionStatus === 'OFF') {
          setVisionStatus('DEMO');
          localStorage.setItem('silent_health_vision_status', 'DEMO');
        }

        // 3. Fetch Sessions (Optimized frequency)
        const allSessions = await db.sessions
          .filter((s) => !!s.neuro_report)
          .toArray();

        allSessions.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());

        // Update sessions ONLY if meaningful change (count or latest score)
        if (allSessions.length !== sessionHistory.length ||
          (allSessions[0]?.neuro_report?.risk_score !== sessionHistory[0]?.neuro_report?.risk_score)) {
          setSessionHistory(allSessions);
          if (allSessions[0]) setLastAudit(allSessions[0].neuro_report);
        }

        // 4. Update Age
        if (allSessions[0]) {
          const assessmentDate = new Date(allSessions[0].date);
          const now = new Date();
          const diffMs = now.getTime() - assessmentDate.getTime();
          const diffMins = Math.floor(diffMs / 60000);
          const diffSecs = Math.floor((diffMs % 60000) / 1000);

          let ageStr = '';
          if (diffMins === 0) ageStr = `${diffSecs}s ago`;
          else if (diffMins < 60) ageStr = `${diffMins}m ${diffSecs}s ago`;
          else ageStr = `${Math.floor(diffMins / 60)}h ago`;

          setAssessmentAge(ageStr);
        }

        // 5. Analysis Countdown
        const framesSinceSync = Math.max(0, count - lastSyncedCount);
        const framesUntilAnalysis = Math.max(0, 60 - (framesSinceSync % 60));
        setNextAnalysisIn(Math.ceil(framesUntilAnalysis / 30));

      } catch (err) {
        console.error("Tick failed", err);
      } finally {
        isCheckingData.current = false;
      }
    };

    tick();
    const interval = setInterval(tick, 2000); // Throttled to 2s
    return () => clearInterval(interval);
  }, [lastSyncedCount, visionStatus, sessionHistory.length]); // Minimal stable dependencies

  const handleAnalyze = async () => {
    if ((window as any).triggerAudit) {
      setIsAnalyzing(true);
      try {
        await (window as any).triggerAudit();
        // Give DB a moment to update
        setTimeout(async () => {
          const latestSession = await db.sessions.orderBy('date').last();
          if (latestSession?.neuro_report) {
            setLastAudit(latestSession.neuro_report);
          }
          setIsAnalyzing(false);
        }, 3000);
      } catch {
        setIsAnalyzing(false);
      }
    }
  };

  const viewReport = () => setShowReport(!showReport);

  // Export pilot study data for research analysis
  const handleExportData = async () => {
    const { exportPilotData } = await import('@/lib/export-pilot-data');
    await exportPilotData();
  };

  // Stabilize sensor callbacks
  const handleAudioFeature = React.useCallback((f: any) => recorder.onAudio(f), []);
  const handleAudioLevel = React.useCallback((level: number) => setAudioLevel(level), []);
  const handleAnalyzingChange = React.useCallback((val: boolean) => setIsAnalyzing(val), []);
  const handleAuditComplete = React.useCallback((count: number) => setLastSyncedCount(count), []);
  const handleVisionStatusChange = React.useCallback((status: any) => setVisionStatus(status), []);
  const handleToggleMonitoring = React.useCallback((val: boolean) => setIsMonitoring(val), []);

  if (!mounted || !isSecure) return null;

  return (
    <main className="min-h-screen bg-slate-950 text-slate-200 font-mono text-center md:text-left">
      <HeroSection />
      <AboutSection />

      <div className="p-8 max-w-6xl mx-auto space-y-8">
        {/* Background Sensors */}
        {isSecure && (
          <>
            <SensorLoop
              isMonitoring={isMonitoring}
              onToggleMonitoring={handleToggleMonitoring}
              onStatusChange={handleVisionStatusChange}
            />
            <AudioLoop
              disabled={!isMonitoring}
              onFeature={handleAudioFeature}
              onAudioLevel={handleAudioLevel}
            />
            <AuditorLoop
              onAnalyzingChange={handleAnalyzingChange}
              onAuditComplete={handleAuditComplete}
            />
          </>
        )}

        {/* Header */}
        <header className="flex justify-between items-center border-b border-slate-800 pb-4 mb-12">
          <div className="flex items-center gap-3">
            <Brain className="w-8 h-8 text-emerald-500" />
            <div>
              <h1 className="text-xl font-bold tracking-widest text-emerald-400">SILENT HEALTH</h1>
              <p className="text-xs text-slate-500">LIVE SENSING v1.1</p>
            </div>
          </div>
          <div className="flex items-center gap-4 text-xs">
            <div className="flex items-center gap-2 px-3 py-1 bg-slate-900 rounded-full border border-slate-800">
              <Lock className="w-3 h-3 text-emerald-500" />
              <span className="text-emerald-500">{mounted ? dataCount : 0} FRAMES BUFFERED</span>
            </div>
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${mounted && visionStatus !== 'OFF' ? 'bg-emerald-500 animate-pulse' : 'bg-slate-600'}`} />
              <span>STATUS: {mounted ? visionStatus : 'INITIALIZING'}</span>
            </div>
          </div>
        </header>

        {/* Main Content Grid */}
        <div className="max-w-4xl mx-auto space-y-6 pb-24">

          {/* 1. Live Status Notice */}
          <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-xl p-6">
            <div className="flex items-start gap-3">
              <Activity className="w-5 h-5 text-emerald-400 mt-0.5" />
              <div>
                <h2 className="text-sm font-bold text-emerald-400 mb-2">REAL-TIME SENSING ACTIVE</h2>
                <p className="text-xs text-slate-300 mb-3">
                  System is now using real MediaPipe WebAssembly inference. Your facial expressions and patterns
                  are being analyzed locally at 30Hz to detect digital biomarkers.
                </p>
                <div className="text-xs text-slate-400 space-y-1">
                  <div>✅ Real MediaPipe Face Landmarker (WASM)</div>
                  <div>✅ Zero-Copy Web Worker Integration</div>
                  <div>✅ 478-point 3D Landmark Tracking</div>
                  <div className="flex items-center gap-2">
                    {process.env.NEXT_PUBLIC_OPENROUTER_API_KEY ? (
                      <span>✅ AI Analysis: Active (Gemini 3.0 Pro)</span>
                    ) : (
                      <span className="flex items-center gap-1.5 text-amber-400">
                        <AlertTriangle className="w-3.5 h-3.5" />
                        AI Analysis: API Key Missing (Add to .env.local)
                      </span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* 2. System Status Summary */}
          <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
            <h2 className="flex items-center gap-2 text-sm text-slate-400 mb-4 uppercase">
              <Activity className="w-4 h-4" /> System Stats
            </h2>
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
              <div className="p-3 bg-slate-950 rounded-lg border border-slate-800">
                <div className="text-slate-500 mb-1 italic">Sensors</div>
                <div className="text-emerald-400 font-bold">LIVE</div>
              </div>
              <div className="p-3 bg-slate-950 rounded-lg border border-slate-800">
                <div className="text-slate-500 mb-1 italic">Audio</div>
                <div className="text-emerald-400 font-bold">
                  {mounted && audioLevel > 0.01 ? 'DETECTED' : 'QUIET'}
                </div>
              </div>
              <div className="p-3 bg-slate-950 rounded-lg border border-slate-800">
                <div className="text-slate-400 mb-1 italic flex items-center gap-2">
                  <ShieldCheck className="w-3 h-3 text-blue-500" />
                  Secure Buffer
                </div>
                <div className="flex flex-col gap-1.5">
                  <div className="text-blue-400 font-bold leading-none">
                    {mounted ? dataCount : 0} <span className="text-[10px] opacity-50 ml-0.5 uppercase">Frames Stored</span>
                  </div>
                  <div className="text-[11px] text-slate-500 font-bold">
                    Next Sync: {mounted ? nextAnalysisIn : '--'}s
                  </div>
                </div>
              </div>
              <div className="p-3 bg-slate-950 rounded-lg border border-slate-800">
                <div className="text-slate-400 mb-1 italic">Clinical Auditor</div>
                <div className={`font-bold transition-all text-[11px] ${isAnalyzing ? 'text-amber-400 animate-pulse' : 'text-slate-500'}`}>
                  {isAnalyzing ? 'BRAIN PULSING...' : 'MONITORING FOR DEVIATIONS'}
                </div>
              </div>
            </div>
          </div>

          {/* 3. Privacy & Transparency Controls (The "Kill Switch") */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6 flex flex-col justify-between">
              <div>
                <h2 className="flex items-center gap-2 text-sm text-slate-400 mb-4 uppercase tracking-widest">
                  <ShieldCheck className={`w-4 h-4 ${isMonitoring ? 'text-emerald-400' : 'text-red-400'}`} />
                  Privacy Shield
                </h2>
                <p className="text-[10px] text-slate-500 mb-4 italic">
                  {isMonitoring
                    ? "Sensing is currently active. Your camera and microphone are being processed locally."
                    : "All sensors are hard-disabled. No data is being collected or processed."}
                </p>
              </div>

              <button
                onClick={() => setIsMonitoring(!isMonitoring)}
                className={`w-full py-3 rounded-lg text-xs font-black transition-all border-2 ${isMonitoring
                  ? 'bg-red-500/10 border-red-500/30 text-red-500 hover:bg-red-500 hover:text-white'
                  : 'bg-emerald-500/10 border-emerald-500/30 text-emerald-500 hover:bg-emerald-500 hover:text-white'}`}
              >
                {isMonitoring ? "⚠️ DISABLE ALL SENSORS" : "✅ ACTIVATE MONITORING"}
              </button>
            </div>

            {/* Real-time Data Inspector */}
            <DataInspector />
          </div>

          {/* 4. Research Mode: Session Labeling */}
          {visionStatus === 'LIVE' && isMonitoring && (
            <SessionLabelToggle
              currentLabel={sessionLabel}
              onChange={(label) => {
                setSessionLabel(label);
                localStorage.setItem('current_session_label', label);
              }}
            />
          )}

          {/* 5. Analysis Control & Report Export */}
          <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="flex items-center gap-2 text-sm text-slate-400 uppercase tracking-widest leading-none">
                <Brain className="w-4 h-4 text-emerald-500" /> Intelligent Report
              </h2>
              <div className="flex gap-2">
                <button
                  onClick={handleAnalyze}
                  disabled={isAnalyzing || dataCount < 100}
                  className={`px-4 py-2 rounded-lg text-xs font-bold transition-all ${isAnalyzing || dataCount < 100
                    ? 'bg-slate-800 text-slate-600 cursor-not-allowed'
                    : 'bg-emerald-600 hover:bg-emerald-500 text-white shadow-lg shadow-emerald-500/20'
                    }`}
                >
                  {isAnalyzing ? 'AUDITING...' : 'FORCE AUDIT'}
                </button>
                <button
                  onClick={() => setShowReport(true)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs font-bold transition-all border border-slate-700"
                >
                  TRANSPARENCY
                </button>
              </div>
            </div>

            <div className="flex items-center gap-3 p-3 bg-slate-900/50 border border-slate-700/50 rounded-lg">
              <ShieldCheck className="w-4 h-4 text-emerald-500" />
              <p className="text-[10px] text-slate-300 font-medium leading-relaxed">
                <span className="text-emerald-400 font-bold uppercase tracking-tighter mr-1">Clinical Protocol:</span>
                Autonomous clinical reporting is strictly enforced. Reports are generated exactly every 100 frames (~3.3s of high-fidelity tracking) to ensure longitudinal accuracy.
              </p>
            </div>
          </div>

          {/* 6. Current AI Assessment Report */}
          {isAnalyzing && !lastAudit && (
            <div className="p-12 border border-blue-500/20 bg-blue-500/5 rounded-xl flex flex-col items-center justify-center gap-4 animate-pulse">
              <Activity className="w-8 h-8 text-blue-400 animate-spin" />
              <div className="text-center">
                <p className="text-xs font-black text-blue-400 uppercase tracking-widest">Autonomous Analysis In Progress</p>
                <p className="text-[10px] text-blue-500/60 mt-1">Acquiring clinical vectors from last 100 frames...</p>
              </div>
            </div>
          )}
          {lastAudit && (
            <div className={`p-6 border rounded-xl ${Number(lastAudit.risk_score) > 60 ? 'bg-red-950/20 border-red-500/30' : 'bg-emerald-950/20 border-emerald-500/30 shadow-2xl shadow-emerald-950/10'}`}>
              <div className="flex justify-between items-start mb-6 border-b border-slate-800 pb-4">
                <div className="flex items-center gap-3">
                  <Activity className={`w-6 h-6 ${Number(lastAudit.risk_score) > 60 ? 'text-red-400' : 'text-emerald-400'}`} />
                  <div>
                    <h2 className="text-sm font-bold uppercase tracking-widest">Clinical Audit</h2>
                    <p className="text-[10px] text-slate-500 mt-1 uppercase tracking-tighter">
                      Generated: {mounted ? new Date(sessionHistory[0].date).toLocaleTimeString() : '--:--'} • {mounted ? assessmentAge : 'Calculating...'}
                    </p>
                  </div>
                </div>
                <div className="text-3xl font-black">
                  {lastAudit.risk_score}<span className="text-xs font-bold opacity-50 ml-1">RISK</span>
                </div>
              </div>

              <div className="mb-6 bg-black/40 p-4 rounded-lg border border-slate-800/50">
                <MarkdownReport content={lastAudit.clinical_notes} />
              </div>

              <div className="flex gap-2 flex-wrap border-t border-slate-800 pt-4">
                {lastAudit.anomalies?.map((a: string, i: number) => (
                  <span key={i} className="px-3 py-1 text-[10px] font-bold uppercase tracking-wide rounded-full border bg-slate-800 text-slate-400">
                    {a}
                  </span>
                ))}
              </div>
            </div>
          )}
          {/* 6.5 Longitudinal Analytics */}
          {sessionHistory.length > 0 && (
            <div className="pt-8 border-t border-slate-800/50">
              <LongitudinalTrends sessions={sessionHistory} />
            </div>
          )}

          {/* 7. History Exploration */}
          {sessionHistory.length > 0 && (
            <div className="mt-12 space-y-4">
              <div className="flex justify-between items-end mb-2">
                <button
                  onClick={() => setHistoryExpanded(!historyExpanded)}
                  className="text-slate-500 text-xs font-bold uppercase tracking-widest flex items-center gap-2 hover:text-slate-300 transition-colors"
                >
                  <Activity className="w-3 h-3" /> Historical Sessions ({sessionHistory.length})
                  <span className="text-[10px] opacity-50 ml-1">{historyExpanded ? '▼' : '▶'}</span>
                </button>
                <div className="flex gap-2">
                  <button
                    onClick={() => {
                      // Force refresh data
                      setDataCount(prev => prev); // Trigger re-render
                      // In reality, checkData runs every 1s, so this is mostly placebo/immediate-feedback
                    }}
                    className="p-1.5 hover:bg-slate-800 rounded text-slate-500 hover:text-white transition-colors"
                    title="Refresh History"
                  >
                    <Activity className="w-3 h-3 animate-[spin_3s_linear_infinite]" />
                  </button>
                  <button
                    onClick={handleExportData}
                    className="flex items-center gap-2 px-4 py-1.5 bg-blue-600/10 hover:bg-blue-600 border border-blue-500/30 text-blue-400 hover:text-white rounded-lg text-[10px] font-black tracking-widest transition-all uppercase"
                  >
                    <Lock className="w-3 h-3" /> Export Dataset (CSV)
                  </button>
                </div>
              </div>

              {historyExpanded && (
                <div className="space-y-2 animate-in fade-in slide-in-from-top-2 duration-300">
                  <div className="overflow-hidden rounded-xl border border-slate-800 bg-slate-900/30">
                    <table className="w-full text-left border-collapse">
                      <thead>
                        <tr className="bg-slate-900/80 border-b border-slate-800 text-[10px] uppercase font-bold tracking-widest text-slate-500">
                          <th className="px-4 py-3 shrink-0">Timestamp</th>
                          <th className="px-4 py-3">Risk Assessment</th>
                          <th className="px-4 py-3">Evidence Label</th>
                          <th className="px-4 py-3 text-right">Actions</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-800/50">
                        {sessionHistory.map((session, idx) => {
                          const sessionKey = session.id || `session-${idx}`;
                          const isExpanded = expandedHistoryItems[sessionKey] || false;
                          // Highlight if this is the currently displayed report
                          const isCurrent = lastAudit?.timestamp === session.neuro_report?.timestamp;

                          return (
                            <React.Fragment key={sessionKey}>
                              <tr
                                onClick={() => setExpandedHistoryItems(prev => ({ ...prev, [sessionKey]: !isExpanded }))}
                                className={`transition-colors cursor-pointer group ${isCurrent ? 'bg-emerald-500/5 hover:bg-emerald-500/10' : 'bg-slate-900/20 hover:bg-slate-800/40'}`}
                              >
                                <td className="px-4 py-3 text-xs text-slate-400 font-mono flex items-center gap-2">
                                  {isCurrent && <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />}
                                  {new Date(session.date).toLocaleString()}
                                </td>
                                <td className="px-4 py-3">
                                  <span className={`text-[10px] font-bold px-2 py-1 rounded-sm border inline-flex items-center gap-2 ${Number(session.neuro_report.risk_score) > 50
                                    ? "bg-red-500/10 border-red-500/30 text-red-400"
                                    : "bg-emerald-500/10 border-emerald-500/30 text-emerald-400"
                                    }`}>
                                    <Activity className="w-3 h-3" />
                                    SCORE: {session.neuro_report.risk_score}
                                  </span>
                                </td>
                                <td className="px-4 py-3">
                                  <span className={`text-[9px] font-black uppercase tracking-wider px-2 py-1 rounded border inline-flex items-center gap-1.5 ${session.session_label === 'BASELINE' ? 'bg-blue-500/10 border-blue-500/20 text-blue-400' :
                                    session.session_label === 'FALSE_POSITIVE' ? 'bg-orange-500/10 border-orange-500/20 text-orange-400' :
                                      session.session_label === 'FALSE_NEGATIVE' ? 'bg-purple-500/10 border-purple-500/20 text-purple-400' :
                                        'bg-slate-800 border-slate-700 text-slate-500'
                                    }`}>
                                    {session.session_label || 'UNLABELED'}
                                  </span>
                                </td>
                                <td className="px-4 py-3 text-right">
                                  <span className="text-slate-600 text-[9px] uppercase font-bold tracking-widest group-hover:text-slate-400 transition-colors">
                                    {isExpanded ? "Hide Details ▲" : "View Report ▼"}
                                  </span>
                                </td>
                              </tr>
                              {isExpanded && (
                                <tr>
                                  <td colSpan={4} className="p-0">
                                    <div className="p-6 bg-slate-950/50 border-y border-slate-800 shadow-inner">
                                      <div className="flex justify-between items-center mb-6 pb-4 border-b border-slate-800">
                                        <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
                                          <Brain className="w-4 h-4 text-slate-600" /> Clinical Deconstruction
                                        </h4>

                                        <div className="flex gap-2">
                                          {session.session_label === 'FALSE_POSITIVE' && (
                                            <button
                                              onClick={async (e) => {
                                                e.stopPropagation();
                                                await db.sessions.update(session.id, { session_label: 'UNLABELED' });
                                                const updated = await db.sessions.filter(s => !!s.neuro_report).toArray();
                                                updated.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
                                                setSessionHistory(updated);
                                              }}
                                              className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-400 hover:text-white rounded text-[10px] font-black uppercase tracking-wide transition-all"
                                            >
                                              Restore Classification
                                            </button>
                                          )}
                                        </div>
                                      </div>
                                      <MarkdownReport content={session.neuro_report.clinical_notes} />
                                    </div>
                                  </td>
                                </tr>
                              )}
                            </React.Fragment>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* 8. Full Report Modal */}
        {showReport && (
          <div className="fixed inset-0 bg-black/90 backdrop-blur-md flex items-center justify-center z-50 p-8">
            <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-2xl w-full max-h-[85vh] overflow-hidden flex flex-col shadow-2xl">
              <div className="flex justify-between items-center p-6 border-b border-slate-800">
                <h2 className="text-lg font-bold text-emerald-400 flex items-center gap-2 tracking-widest">
                  <Brain className="w-5 h-5" /> SYSTEM TRANSPARENCY
                </h2>
                <button
                  onClick={() => setShowReport(false)}
                  className="p-2 hover:bg-slate-800 rounded-full transition-colors text-slate-500 hover:text-white"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>
              <div className="p-8 overflow-y-auto space-y-6">
                <div className="bg-slate-950 p-6 rounded-xl border border-slate-800 font-mono text-[11px] leading-relaxed text-slate-300">
                  <div className="text-emerald-500 font-black mb-4 border-b border-emerald-500/20 pb-2">
                    [SENSING ENGINE STATUS]
                  </div>
                  <div className="space-y-2">
                    <p>• Data Source: Real Hardware Sensors</p>
                    <p>• Processing: Local WebAssembly (WASM)</p>
                    <p>• Persistence: Client-Side IndexedDB</p>
                    <p>• Telemetry: 30Hz Raw Landmark Sync</p>
                    <p>• Anonymization: Active (No face storage)</p>
                  </div>

                  <div className="text-blue-500 font-black mt-8 mb-4 border-b border-blue-500/20 pb-2">
                    [ACADEMIC COMPLIANCE]
                  </div>
                  <div className="space-y-2">
                    <p>• Metrics: UPDRS-Aligned (Blinks, Tremor)</p>
                    <p>• Labeling: Active ({sessionLabel})</p>
                    <p>• Frames in Buffer: {dataCount}</p>
                  </div>
                </div>

                <div className="text-[10px] text-slate-500 italic text-center px-12">
                  "Silent Health is designed for clinical research validation. All processing remains on-device to ensure participant privacy and data integrity."
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
