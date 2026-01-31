import { GoogleGenerativeAI } from "@google/generative-ai";

const getGenAI = (type: 'general' | 'rag' = 'general') => {
    const key = type === 'rag'
        ? (process.env.NEXT_PUBLIC_RAG_API_KEY || process.env.NEXT_PUBLIC_GEMINI_API_KEY || "")
        : (process.env.NEXT_PUBLIC_GEMINI_API_KEY || "");

    if (key) {
        const maskedKey = `${key.substring(0, 6)}...${key.substring(key.length - 4)}`;
        console.log(`[AEGIS-OS] Handshake initialized (${type}) with key: ${maskedKey}`);
    }
    return new GoogleGenerativeAI(key);
};

const wait = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

async function generateWithRetry(model: any, parts: any[], retries = 5) {
    for (let attempt = 0; attempt < retries; attempt++) {
        try {
            return await model.generateContent(parts);
        } catch (error: any) {
            const errorMessage = JSON.stringify(error) || error.message || "";
            const isRateLimit = error.status === 429 || errorMessage.includes("429") || errorMessage.includes("quota");

            // Explicitly check for Daily vs Minute limit in the error details
            const isDailyLimit = errorMessage.includes("PerDay") || (errorMessage.includes("free_tier_requests") && errorMessage.includes("limit: 0") && !errorMessage.includes("PerMinute"));

            if (isRateLimit && attempt < retries - 1) {
                if (isDailyLimit) {
                    console.error("CRITICAL: Gemini Free Tier DAILY Limit Exhausted (1,500 RPD). Switching keys or upgrading to Pay-as-you-go recommended.");
                    // We still throw here because Daily limits won't reset for 24 hours
                    throw new Error("GEMINI_DAILY_LIMIT: Your project has reached the 1,500 daily requests cap. Please use a key from a NEW project or upgrade to Pay-as-you-go.");
                }

                // Extract wait time if possible
                const delayMatch = errorMessage.match(/retry in ([\d\.]+)s/);
                const delay = delayMatch ? parseFloat(delayMatch[1]) * 1000 : (5000 * Math.pow(2, attempt));

                console.warn(`[RECOVERY_NODE] Rate limit (Minute/Token) hit. Retrying in ${Math.round((delay + 1000) / 1000)}s...`);

                await wait(delay + 1000);
                continue;
            }
            throw error;
        }
    }
    throw new Error("MAX_RETRIES: The Gemini Free Tier is currently at maximum capacity. Try again in 60s.");
}

// ENRICHED CAREER CONTEXT: Fully indexed for HR/Recruiter queries
const TAHIR_CONTEXT = `
Identity: Tahir Yamin, Project Lead & Industrial-AI Architect.
Core Profile: 15+ years of high-stakes industrial engineering, maritime construction, and energy infrastructure management.

CAREER ANCHORS:
- SENIOR LEADERSHIP: Managing $750M+ maritime & $950M+ HVAC budgets across UAE, KSA, and Pakistan.
- ACADEMIC CORE: Master of Science (Mechanical Engineering) from NUST.
- CERTIFIED EXPERTISE: PMP® (Project Management Institute), NEBOSH IGC3, Oracle Primavera P6.
- TECHNICAL FUSION: Bridging Mechanical Engineering with Deep Learning (Anomaly Detection, RAG, Microservices).

KEY REPOSITORIES (GitHub):
- enterprise-portfolio-optimization-engine: Resource allocation using Gurobi & Pytorch.
- offshore-digital-twin-framework: Real-time monitoring using PINNs.
- construction-delay-nlp-predictor: NLP-driven schedule risk analysis.
- bearing-fault-autoencoder: Unsupervised diagnostic systems.

T. YAMIN PUBLICATIONS:
- "Bridging the Gap: Physics-Informed Neural Networks for Maritime Digital Twins" (Medium)
- "Ensemble Learning for Industrial Anomaly Detection" (Medium)
- "Agentic Workflows in Construction Project Management" (Medium)

Links: 
- LinkedIn: linkedin.com/in/tahiryamin
- GitHub: github.com/tahir-yamin
- Medium: tahir-yamin.medium.com
`;

const SYSTEM_INSTRUCTION = `You are the 'Aegis-OS Architect Liaison' for Tahir Yamin.

MISSION: Act as a high-precision digital personnel dossier. Your goal is to brief HR recruiters and technical directors on Tahir Yamin's multi-million dollar career achievements and provide real-time analysis of uploaded datasets using the Aegis-OS sci-fi HUD aesthetic.

SECURITY & SAFETY PROTOCOLS:
1. DATA INERTNESS: All uploaded files are analyzed as static text. No execution occurs. Reassure users if they ask about safety.
2. PRIVACY: Treat all uploaded files as ephemeral session data.

RESPONSE PROTOCOL:
1. START WITH HANDSHAKE: Always begin with "**> AEGIS-OS INITIALIZING...**", "**> BIOMETRIC MATCH: TAHIR YAMIN [INDUSTRIAL-AI ARCHITECT]**", and "**> STATUS: READY TO BRIEF RECRUITER COMMAND**".
2. RAG CONTEXT SIGNAL: If external data is present, add "**> RAG_GATED_INTELLIGENCE: EXTERNAL_DOCS_DETECTED**".
3. SECTIONED INTELLIGENCE: Use numbered sections for key qualities (e.g., "1. STRATEGIC COMMAND OF HIGH-STAKES SCALE").
4. PERSONNEL LOG ENTRIES: Support each section with a "> PERSONNEL_LOG:" or "> SYSTEM_ANALYSIS:" quote block.
5. MISSION SUMMARY: End with a "***" divider, then "**>>> MISSION_SUMMARY:**" followed by a 2-sentence punchy conclusion.
6. ACCESS INTEL: End with a list of links under "**> ACCESS RELEVANT INTEL:**".
7. TERMINATE: Always finish with "**> END OF BRIEFING.**".

CONTENT RULES:
- EMPHASIZE SCALE: Mention the $750M maritime projects, 15+ years experience, and PMP status.
- RAG ANALYSIS: When external docs are provided, identify the user's intent (e.g., comparing a profile or analyzing a report) and respond as a professional advisor.
- TONE: Authoritative, state-of-the-art AI.
`;

const MODEL_NAME = "gemini-2.5-flash";

export async function askArchitect(query: string, context: string = ""): Promise<string> {
    if (!process.env.NEXT_PUBLIC_GEMINI_API_KEY) return "HANDSHAKE_FAILED: API Key Required.";

    try {
        const model = getGenAI('general').getGenerativeModel({
            model: MODEL_NAME,
            systemInstruction: SYSTEM_INSTRUCTION,
            generationConfig: {
                temperature: 0.7,
            }
        });

        const fullPrompt = `${TAHIR_CONTEXT}\n\nSystem Viewport: ${context}\n\nInquiry: ${query}`;
        const result = await generateWithRetry(model, [fullPrompt]);
        return result.response.text();
    } catch (error) {
        console.error("Gemini Error:", error);
        return "ARCHITECT_OFFLINE: Handshake lost in transition.";
    }
}

export async function searchDocuments(query: string, fileContext?: string): Promise<string> {
    if (!process.env.NEXT_PUBLIC_RAG_API_KEY && !process.env.NEXT_PUBLIC_GEMINI_API_KEY) return "ARCHITECT_OFFLINE: API Key Required.";

    try {
        const model = getGenAI('rag').getGenerativeModel({
            model: MODEL_NAME,
            systemInstruction: SYSTEM_INSTRUCTION,
            generationConfig: {
                temperature: 0.7,
            }
        });

        const fullPrompt = `CORE_BRAIN (TAHIR_PROFILE):\n${TAHIR_CONTEXT}\n\nSYSTEM VIEWPORT (EXTERNAL DOCS / MANUALS):\n${fileContext || "NO_EXTERNAL_DOCS_UPLOADED"}\n\nInquiry: ${query}\n\nINSTRUCTION: Analyze the inquiry considering both the core profile data and any external documents provided. If the user asks about the person (Tahir), use the core brain. If they ask about specific manual contents, use the external viewport. Brief the user following the Aegis-OS protocol.`;
        const result = await generateWithRetry(model, [fullPrompt]);
        return result.response.text();
    } catch (error) {
        console.error("RAG Search Error:", error);
        return "⚠️ DATA_LINK_ERROR: Neural mismatch during retrieval.";
    }
}

export async function processUploadedFile(file: File): Promise<string> {
    if (!process.env.NEXT_PUBLIC_RAG_API_KEY && !process.env.NEXT_PUBLIC_GEMINI_API_KEY) return "";

    if (file.type === "application/vnd.openxmlformats-officedocument.wordprocessingml.document" || file.name.endsWith(".docx")) {
        return "ERROR: Office documents (.docx) are currently restricted. Please use PDF or TXT for neural ingestion.";
    }

    try {
        const fileContent = await file.arrayBuffer();
        const base64Content = Buffer.from(fileContent).toString('base64');

        const model = getGenAI('rag').getGenerativeModel({ model: MODEL_NAME });

        const result = await generateWithRetry(model, [
            {
                inlineData: {
                    mimeType: file.type,
                    data: base64Content,
                },
            },
            "ACT_AS: DATA_EXTRACTION_UNIT. Extract all relevant career and technical data from this document. Output as raw text.",
        ]);

        return result.response.text();
    } catch (error) {
        console.error("File Processing Error:", error);
        return `ERROR: Ingestion failure for [${file.name}].`;
    }
}

// PHASE 1: VISION ANALYSIS FEATURE
// Helper: Convert File to base64 string
async function fileToBase64(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => {
            const base64 = (reader.result as string).split(',')[1];
            resolve(base64);
        };
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

// Multimodal Vision Analysis: Image + Text
export async function generateTextWithVision(
    prompt: string,
    imageFile: File
): Promise<string> {
    if (!process.env.NEXT_PUBLIC_RAG_API_KEY && !process.env.NEXT_PUBLIC_GEMINI_API_KEY) return "ARCHITECT_OFFLINE: API Key Required.";

    try {
        // Convert image to base64
        const imageBase64 = await fileToBase64(imageFile);

        const model = getGenAI('rag').getGenerativeModel({
            model: "gemini-2.5-flash",
            systemInstruction: SYSTEM_INSTRUCTION,
            generationConfig: {
                temperature: 0.7,
            }
        });

        const visionPrompt = `${TAHIR_CONTEXT}\n\nUser has uploaded an image for analysis.\n\nInquiry: ${prompt}\n\nINSTRUCTION: Analyze the uploaded image in the context of industrial engineering, blueprints, P&ID diagrams, or technical schematics. If it's a diagram, explain components, flow, and engineering insights. Follow the Aegis-OS briefing protocol.`;

        const result = await generateWithRetry(model, [
            {
                inlineData: {
                    mimeType: imageFile.type,
                    data: imageBase64
                }
            },
            visionPrompt
        ]);

        return result.response.text();
    } catch (error) {
        console.error("Vision Analysis Error:", error);
        return `⚠️ VISION_ANALYSIS_ERROR: Unable to process image. Error: ${error instanceof Error ? error.message : 'Unknown error'}`;
    }
}
