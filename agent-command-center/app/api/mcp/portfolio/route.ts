import { NextResponse } from 'next/server';
import { PROFILE_DATA } from '@/app/data';

export async function GET() {
    return NextResponse.json({
        schema_version: "1.0.0",
        agent_compatibility: ["gemini-2.0", "claude-3.5", "gpt-4"],
        last_updated: new Date().toISOString(),

        profile: {
            name: PROFILE_DATA.name,
            title: PROFILE_DATA.title,
            summary: PROFILE_DATA.summary,
            location: PROFILE_DATA.location,
            email: PROFILE_DATA.socials.email,
        },

        capabilities: [
            "vision_analysis",
            "industrial_consulting",
            "project_management",
            "ai_integration"
        ],

        industrial_impact: {
            total_budget_managed_usd: PROFILE_DATA.impact.hvac_budget,
            largest_project_budget: PROFILE_DATA.impact.maritime_value,
            team_leadership_max: PROFILE_DATA.impact.team_size,
            sectors: ["Naval Shipbuilding", "HVAC Industrial", "Construction"],
            certifications_count: PROFILE_DATA.certifications.length
        },

        certifications: PROFILE_DATA.certifications.map(cert => ({
            title: cert.title,
            issuer: cert.issuer,
            description: cert.description
        })),

        projects: PROFILE_DATA.projects.map(proj => ({
            title: proj.title,
            description: proj.description,
            technologies: proj.tech,
            github_url: proj.githubUrl
        })),

        ai_integration: {
            primary_model: "Gemini 2.0 Flash",
            features: [
                "Multimodal Vision Analysis",
                "RAG-based Career Intelligence",
                "Interactive Industrial Simulations"
            ]
        }
    });
}
