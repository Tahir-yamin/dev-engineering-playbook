"use client";

import { useState } from "react";
import { Upload, FileText, Search, X, CheckCircle, Terminal, Image as ImageIcon } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { processUploadedFile, searchDocuments, generateTextWithVision } from "../services/geminiService";

export default function AskTheManual() {
    const [uploadedFiles, setUploadedFiles] = useState<{ name: string; content: string }[]>([]);
    const [isUploading, setIsUploading] = useState(false);
    const [query, setQuery] = useState("");
    const [searchResult, setSearchResult] = useState("");
    const [isSearching, setIsSearching] = useState(false);

    // PHASE 1: Vision Analysis State
    const [uploadedImage, setUploadedImage] = useState<File | null>(null);
    const [imagePreview, setImagePreview] = useState<string | null>(null);

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const files = e.target.files;
        if (!files || files.length === 0) return;

        setIsUploading(true);

        for (const file of Array.from(files)) {
            // Support PDF, TXT, DOC
            if (file.type.includes("pdf") || file.type.includes("text") || file.type.includes("document")) {
                const extractedText = await processUploadedFile(file);
                if (extractedText) {
                    setUploadedFiles(prev => [...prev, { name: file.name, content: extractedText }]);
                }
            }
        }

        setIsUploading(false);
    };

    // PHASE 1: Image Upload Handler
    const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        // Validate image type and size
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file (PNG, JPG, WEBP)');
            return;
        }
        if (file.size > 4 * 1024 * 1024) { // 4MB limit
            alert('Image size must be less than 4MB');
            return;
        }

        setUploadedImage(file);

        // Create preview
        const reader = new FileReader();
        reader.onload = (e) => {
            setImagePreview(e.target?.result as string);
        };
        reader.readAsDataURL(file);
    };

    const clearImage = () => {
        setUploadedImage(null);
        setImagePreview(null);
    };

    const handleSearch = async () => {
        if (!query) return;

        // Check if we have either uploaded files OR an image
        if (uploadedFiles.length === 0 && !uploadedImage) return;

        setIsSearching(true);

        try {
            let result: string;

            // PHASE 1: Use Vision API if image is uploaded
            if (uploadedImage) {
                result = await generateTextWithVision(query, uploadedImage);
            } else {
                // Use existing RAG (text-only)
                const combinedContext = uploadedFiles.map(f => `[${f.name}]\n${f.content}`).join("\n\n---\n\n");
                result = await searchDocuments(query, combinedContext);
            }

            if (result.startsWith("ERROR:")) {
                setSearchResult(`⚠️ DATA_PROCESSING_ERROR: ${result.split("ERROR:")[1].trim()}`);
            } else {
                setSearchResult(result);
            }
        } catch (error) {
            setSearchResult(`⚠️ SYSTEM_ERROR: ${error instanceof Error ? error.message : 'Unknown error'}`);
        } finally {
            setIsSearching(false);
        }
    };

    const removeFile = (index: number) => {
        setUploadedFiles(prev => prev.filter((_, i) => i !== index));
    };

    return (
        <div className="w-full h-full flex flex-col gap-0 hud-panel rounded-lg overflow-hidden">
            {/* STICKY HEADER */}
            <div className="flex items-center justify-between border-b border-primary/20 p-6 bg-slate-900/50 shrink-0">
                <div>
                    <h2 className="text-primary font-bold tracking-widest uppercase text-lg">Aegis-OS Knowledge Base</h2>
                    <p className="text-xs text-primary/60 font-mono mt-1">INDUSTRIAL AI CORE + RAG SUPPLEMENT</p>
                </div>
                <div className="text-[10px] font-mono text-green-400 bg-green-400/10 px-3 py-1 rounded border border-green-400/20">
                    STATUS: ARCHITECT_LIAISON_ONLINE
                </div>
            </div>

            {/* SCROLLABLE CONTENT AREA */}
            <div className="flex-1 overflow-y-auto custom-scrollbar p-6 space-y-6">
                {/* Core Knowledge Indicator */}
                <div className="bg-primary/5 border border-primary/20 rounded p-4 text-xs font-mono leading-relaxed relative overflow-hidden">
                    <div className="absolute top-0 right-0 p-2 opacity-10"><Search size={60} /></div>
                    <div className="text-primary font-bold mb-3 uppercase tracking-widest flex items-center gap-2 text-sm">
                        <CheckCircle size={16} className="text-green-500" /> Pre-Indexed Career Intelligence
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-y-2 text-slate-300">
                        <div className="flex items-center gap-3">
                            <div className="w-1.5 h-1.5 bg-primary"></div> 14+ Years Industrial Architecture
                        </div>
                        <div className="flex items-center gap-3">
                            <div className="w-1.5 h-1.5 bg-primary"></div> PMP® Project Governance
                        </div>
                        <div className="flex items-center gap-3">
                            <div className="w-1.5 h-1.5 bg-primary"></div> NUST Masters / Thermal Systems
                        </div>
                        <div className="flex items-center gap-3">
                            <div className="w-1.5 h-1.5 bg-primary"></div> Industrial AI / RAG Protocols
                        </div>
                    </div>
                    <div className="mt-4 text-primary/80 font-bold border-t border-primary/10 pt-3 text-[11px] leading-snug">
                        LIAISON_NOTE: My core brain is already synchronized with your profile. Upload docs ONLY for analysis of external datasets.
                    </div>
                </div>

                {/* Upload Zone */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* Document Upload */}
                    <div className="relative">
                        <input
                            type="file"
                            id="file-upload"
                            multiple
                            accept=".pdf,.txt"
                            onChange={handleFileUpload}
                            className="hidden"
                        />
                        <label
                            htmlFor="file-upload"
                            className="flex flex-col items-center justify-center p-6 border-2 border-dashed border-primary/20 rounded-lg cursor-pointer hover:border-primary/50 hover:bg-primary/5 transition-all text-center group h-full"
                        >
                            <Upload className="text-primary/50 group-hover:text-primary mb-2 transition-colors" size={28} />
                            <span className="text-xs font-mono text-slate-300 mb-1 uppercase tracking-widest">
                                {isUploading ? "INGESTING..." : "DOCUMENTS"}
                            </span>
                            <p className="text-[10px] text-primary/40 font-mono px-2">
                                PDF / TXT for RAG analysis
                            </p>
                        </label>
                    </div>

                    {/* PHASE 1: Image Upload */}
                    <div className="relative">
                        <input
                            type="file"
                            id="image-upload"
                            accept="image/*"
                            onChange={handleImageUpload}
                            className="hidden"
                        />
                        <label
                            htmlFor="image-upload"
                            className="flex flex-col items-center justify-center p-6 border-2 border-dashed border-cyan-500/20 rounded-lg cursor-pointer hover:border-cyan-500/50 hover:bg-cyan-500/5 transition-all text-center group h-full"
                        >
                            <ImageIcon className="text-cyan-500/50 group-hover:text-cyan-500 mb-2 transition-colors" size={28} />
                            <span className="text-xs font-mono text-slate-300 mb-1 uppercase tracking-widest">
                                VISION ANALYSIS
                            </span>
                            <p className="text-[10px] text-cyan-500/40 font-mono px-2">
                                Blueprints, P&IDs, Diagrams
                            </p>
                        </label>
                    </div>
                </div>

                {/* PHASE 1: Image Preview */}
                {imagePreview && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="bg-slate-900/80 border border-cyan-500/30 rounded-lg p-4"
                    >
                        <div className="flex items-center justify-between mb-3">
                            <div className="flex items-center gap-2">
                                <ImageIcon className="text-cyan-500" size={16} />
                                <span className="text-xs font-mono text-slate-200 uppercase">Vision Target Loaded</span>
                            </div>
                            <button
                                onClick={clearImage}
                                className="text-slate-500 hover:text-red-400 p-1 transition-colors"
                            >
                                <X size={16} />
                            </button>
                        </div>
                        <img
                            src={imagePreview}
                            alt="Uploaded diagram"
                            className="max-h-64 w-full object-contain rounded border border-cyan-500/20 bg-black/40"
                        />
                        <div className="mt-2 text-[10px] text-cyan-500/60 font-mono">
                            {uploadedImage?.name} ({(uploadedImage!.size / 1024).toFixed(1)}KB)
                        </div>
                    </motion.div>
                )}

                {/* Uploaded Files List */}
                {uploadedFiles.length > 0 && (
                    <div className="space-y-2">
                        <div className="text-[10px] font-mono text-primary/40 uppercase mb-2">ACTIVE_DATA_NODES:</div>
                        <AnimatePresence>
                            {uploadedFiles.map((file, idx) => (
                                <motion.div
                                    key={idx}
                                    initial={{ opacity: 0, scale: 0.95 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    exit={{ opacity: 0, scale: 0.95 }}
                                    className="flex items-center justify-between bg-slate-900/80 border border-primary/20 rounded p-3"
                                >
                                    <div className="flex items-center gap-3">
                                        <FileText className="text-primary" size={18} />
                                        <span className="text-sm font-mono text-slate-200">{file.name}</span>
                                        <span className="text-[10px] text-primary/40 bg-primary/5 px-2 py-0.5 rounded border border-primary/10">
                                            {Math.floor(file.content.length / 1000)}KB_CONTENT
                                        </span>
                                    </div>
                                    <button
                                        onClick={() => removeFile(idx)}
                                        className="text-slate-500 hover:text-red-400 p-1 transition-colors"
                                    >
                                        <X size={16} />
                                    </button>
                                </motion.div>
                            ))}
                        </AnimatePresence>
                    </div>
                )}

                {/* Search Interface */}
                <div className="sticky bottom-0 bg-black/80 backdrop-blur-md pt-4 pb-2 mt-4">
                    <div className="flex gap-3">
                        <div className="flex-1 relative">
                            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-primary/50" size={18} />
                            <input
                                type="text"
                                value={query}
                                onChange={(e) => setQuery(e.target.value)}
                                onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                                placeholder="PROMPT_SYSTEM_COMMAND..."
                                className="w-full bg-slate-950 border border-primary/30 rounded-lg pl-12 pr-4 py-3 text-base font-mono text-slate-200 placeholder:text-primary/20 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/20 transition-all"
                            />
                        </div>
                        <button
                            onClick={handleSearch}
                            disabled={isSearching || (!query || (uploadedFiles.length === 0 && !uploadedImage))}
                            className="px-8 bg-primary/10 border border-primary text-primary font-mono text-sm rounded-lg hover:bg-primary/20 disabled:opacity-30 disabled:cursor-not-allowed transition-all uppercase tracking-[0.2em] font-bold"
                        >
                            {isSearching ? (uploadedImage ? "ANALYZING_VISION..." : "SCANNING...") : "QUERY"}
                        </button>
                    </div>
                </div>

                {/* Search Results */}
                <AnimatePresence>
                    {searchResult && (
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="bg-black/50 border border-primary/30 rounded-lg p-6 shadow-neon-cyan mt-6"
                        >
                            <div className="flex items-center gap-2 text-xs font-mono text-primary mb-4 pb-2 border-b border-primary/10 uppercase tracking-widest">
                                <Terminal size={14} /> Intelligence_Briefing:
                            </div>
                            <div className="text-base text-slate-200 leading-relaxed whitespace-pre-wrap font-display">
                                {searchResult}
                            </div>
                            <div className="mt-6 flex justify-between items-center text-[10px] font-mono text-primary/40 uppercase">
                                <span>Ref: RAG_LIAISON_PROTOCOL_V2</span>
                                <span>Hash: {Math.random().toString(16).slice(2, 10).toUpperCase()}</span>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>

                {!searchResult && (
                    <div className="py-20 flex flex-col items-center justify-center text-primary/20 text-sm font-mono tracking-[0.3em] gap-4">
                        <div className="w-12 h-1 bg-primary/10 rounded-full animate-pulse" />
                        SYSTEM_IDLE_AWAITING_INPUT
                        <div className="w-12 h-1 bg-primary/10 rounded-full animate-pulse" />
                    </div>
                )}
            </div>
        </div>
    );
}
