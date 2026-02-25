import { GoogleGenerativeAI } from "@google/generative-ai";
import * as dotenv from "dotenv";

dotenv.config({ path: ".env.local" });

const key = process.env.NEXT_PUBLIC_GEMINI_API_KEY;

async function diagnose() {
    if (!key) {
        console.error("❌ No API key found in .env.local");
        return;
    }

    console.log("🔍 Diagnosing Gemini API Availability...");
    console.log("-----------------------------------------");

    const versions = ['v1beta', 'v1'];

    for (const v of versions) {
        console.log(`\n📡 Testing Endpoint Version: ${v}`);
        try {
            const genAI = new GoogleGenerativeAI(key);
            // Internal hack to change version for diagnosis if needed, 
            // but the SDK doesn't expose listModels with a version easily.
            // We will use fetch to be sure.

            const response = await fetch(`https://generativelanguage.googleapis.com/${v}/models?key=${key}`);
            const data = await response.json();

            if (data.error) {
                console.error(`❌ ${v} Error:`, data.error.message);
                continue;
            }

            console.log(`✅ ${v} success! Available Models:`);
            data.models?.forEach((m: any) => {
                console.log(`- ${m.name.replace('models/', '')} (${m.supportedGenerationMethods.join(', ')})`);
            });

        } catch (err: any) {
            console.error(`❌ ${v} Failed:`, err.message);
        }
    }
}

diagnose();
