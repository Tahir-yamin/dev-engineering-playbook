# n8n & SEO Automation MCP Setup Guide

This guide will help you finalize the integration of your new MCP servers and workflows.

## 1. Configure n8n MCP Server

In your `mcp_config.json` file (located at `C:\Users\Administrator\.gemini\antigravity\mcp_config.json`), add the following entry under `"mcpServers"`:

```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "node",
      "args": [
        "d:/my-dev-knowledge-base/external-libs/n8n-mcp-server-custom/dist/index.js"
      ],
      "env": {
        "N8N_API_URL": "http://localhost:5678",
        "N8N_API_KEY": "YOUR_N8N_API_KEY"
      }
    }
  }
}
```

> [!NOTE]
> Replace `YOUR_N8N_API_KEY` with your actual n8n API key (Settings → API).

## 2. Import SEO Workflows into n8n

Open your local n8n instance and import the following JSON files from `d:\my-dev-knowledge-base\external-libs\claude-mcps-and-prompts\workflows\`:

- `mcp-servers.json`: The main toolset.
- `subworkflow-search-analytics.json`: For Google Search Console.
- `subworkflow-ga4-report.json`: For Google Analytics 4 reports.
- `subworkflow-ga4-realtime.json`: For Google Analytics 4 real-time data.

## 3. Set Up Prompts

The SEO prompts and style guides are located in:
- `d:\my-dev-knowledge-base\external-libs\claude-mcps-and-prompts\prompts\`: Use these when asking Claude to write or analyze SEO content.
- `d:\my-dev-knowledge-base\external-libs\claude-mcps-and-prompts\guides\`: References for writing styles.

## 4. Environment Variables (.env)

If the workflows require Supabase or Google credentials, update the `.env` file in `d:\my-dev-knowledge-base\external-libs\n8n-mcp-server-custom\.env` (copy from `.env.example` if needed).

```bash
N8N_API_URL=http://localhost:5678
N8N_API_KEY=your_key
# Add Supabase/Google keys as required by the workflows
```
