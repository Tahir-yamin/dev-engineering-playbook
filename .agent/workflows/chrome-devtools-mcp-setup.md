---
description: Setup Chrome DevTools MCP for browser debugging in Antigravity and other coding agents
---

# Chrome DevTools MCP Setup

## When to Use
- Need browser debugging capabilities in AI coding agents
- Want to capture screenshots, analyze network, get performance insights
- Debugging web applications with AI assistance

---

## Step 1: Install Globally

// turbo
```bash
npm install -g chrome-devtools-mcp@latest
```

---

## Step 2: Configure MCP Client

Add to your MCP configuration (varies by agent):

### For Antigravity / Gemini CLI

Add to `settings.json` or MCP config:
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

### For Claude Code

Add to `.claude/mcp.json`:
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

---

## Step 3: Verify Installation

// turbo
```bash
npx chrome-devtools-mcp@latest --version
```

---

## Step 4: First Use

Example prompt to test:
```
Open https://example.com and take a screenshot
```

---

## Available Tools

| Category | Tools |
|----------|-------|
| **Navigation** | `navigate`, `click`, `type`, `scroll` |
| **Screenshots** | `screenshot`, `element_screenshot` |
| **Network** | `get_network_requests`, `wait_for_network` |
| **Console** | `get_console_logs`, `evaluate_js` |
| **Performance** | `start_trace`, `stop_trace`, `get_insights` |
| **DOM** | `get_element`, `query_selector` |

---

## Requirements

- Node.js v20.19+ (LTS)
- Chrome (current stable)
- npm

---

## Troubleshooting

### Chrome not launching
```bash
# Check if Chrome is in PATH
which google-chrome  # Linux
where chrome         # Windows
```

### Permission issues
```bash
# Run with --no-sandbox (not recommended for production)
npx chrome-devtools-mcp@latest --no-sandbox
```

### Debugging Android
Connect device via USB and enable USB debugging in Chrome.

---

## Related

- [Tool Reference](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/tool-reference.md)
- [Troubleshooting Guide](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/troubleshooting.md)

---

**Source**: [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp)  
**Added**: 2026-01-22
