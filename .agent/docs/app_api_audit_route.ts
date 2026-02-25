import { NextResponse } from 'next/server';
import { auditor } from '@/lib/gemini-auditor';

/**
 * POST /api/audit
 * 
 * RESPONSIBILITY:
 * Securely communicate with Gemini 2.0 Flash.
 * Receives anonymized vector data, returns clinical analysis.
 */

export async function POST(req: Request) {
    try {
        const body = await req.json();
        const { readings, baseline } = body;

        if (!readings || !baseline) {
            return NextResponse.json({ error: "Missing clinical data vectors" }, { status: 400 });
        }

        console.log(`[AUDIT] Analyzing ${readings.length} frames against ${baseline.length} baseline frames...`);

        // Execute Gemini 2.0 Audit
        const result = await auditor.auditSession(readings, baseline);

        return NextResponse.json(result);

    } catch (error) {
        console.error("Audit API Error:", error);
        return NextResponse.json({ error: "Internal Neuro-Audit Failure" }, { status: 500 });
    }
}
