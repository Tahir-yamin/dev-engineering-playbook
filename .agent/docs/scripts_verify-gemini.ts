import { GoogleGenerativeAI } from "@google/generative-ai";
import * as dotenv from 'dotenv';
import { resolve } from 'path';

// Load .env.local
dotenv.config({ path: resolve(process.cwd(), '.env.local') });

async function verifyGemini() {
    const apiKey = process.env.NEXT_PUBLIC_GEMINI_API_KEY;
    if (!apiKey) {
        console.error("No API key found in .env.local");
        return;
    }

    const genAI = new GoogleGenerativeAI(apiKey);

    // Testing the model name from user dashboard
    const modelName = "gemini-1.5-flash"; // Trying the most stable first
    const model = genAI.getGenerativeModel({ model: modelName });

    console.log(`Testing model: ${modelName}...`);

    try {
        const result = await model.generateContent("Hello! Are you working? Return JSON: { \"status\": \"ok\" }");
        console.log("Response:", result.response.text());
        console.log("Model VERIFIED!");
    } catch (err: any) {
        console.error(`Model ${modelName} FAILED:`, err.message);

        // Try the 2.5 Flash if 1.5 fails
        const altModelName = "gemini-2.0-flash-exp";
        console.log(`Trying alternative model: ${altModelName}...`);
        const altModel = genAI.getGenerativeModel({ model: altModelName });
        try {
            const altResult = await altModel.generateContent("Hello!");
            console.log("Response:", altResult.response.text());
            console.log("Alt Model VERIFIED!");
        } catch (altErr: any) {
            console.error(`Alt Model ${altModelName} also FAILED:`, altErr.message);
        }
    }
}

verifyGemini();
