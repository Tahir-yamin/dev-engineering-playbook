---
name: mcp-builder
description: MCP (Model Context Protocol) server building principles. Tool design, resource patterns, best practices.
skills:
  - id: 1
    description: Designing MCP Tools for AI Agents.
    content: |
      ## Skill #1: MCP Tool Design Principles

      ### When to Use
      - Creating tools for AI Coding Assistants (Claude Desktop, Cursor, Antigravity) to act on your behalf.

      ### Pattern
      - **Atomic Tools**: Each tool should do ONE thing well (e.g., `search_index` vs `search_and_summarize`).
      - **Schema Validation**: Use Zod or JSON Schema to strictly define inputs.
      - **Return Types**: Always return explicit success/error states:
      ```typescript
      return {
        content: [{ type: "text", text: JSON.stringify(result) }],
        isError: false
      };
      ```

  - id: 2
    description: Using MCP for UI Scaffolding (Google Stitch).
    content: |
      ## Skill #2: UI Scaffolding with Stitch MCP

      ### When to Use
      - Rapidly generating frontend components that adhere to a specific design system.

      ### Pattern
      1. **Define the Spec**: Tell the MCP what you want (e.g., "A Mission Control dashboard with glassmorphism").
      2. **Iterate**: Use the `stitch_generate_screen_from_text` tool to refine.
      3. **Bridge**: Once the UI is generated, manually wire it to your real data sources (Next.js Actions).

  - id: 3
    description: Bridging External APIs via Custom MCP.
    content: |
      ## Skill #3: API Bridging (The Telemetry Pattern)

      ### When to Use
      - Connecting live data (latency, status, metrics) to an AI context.

      ### Pattern
      Instead of pasting logs into chat:
      1. Create a `read_resource` tool in your MCP server.
      2. Fetch the external API data inside the tool handler.
      3. The Agent simply calls `read_metrics` and gets the latest JSON snapshot.
---
