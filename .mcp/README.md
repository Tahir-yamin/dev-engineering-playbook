# MCP Configuration

This directory contains MCP (Model Context Protocol) server configurations and samples.

## 📁 Contents

- `claude_desktop_config_sample.json` - Sample Claude Desktop MCP configuration
- `README.md` - This file

## 🚀 Quick Setup

### For Claude Desktop

1. **Locate your Claude Desktop config**:
   ```powershell
   # Windows
   $env:APPDATA\Claude\claude_desktop_config.json
   
   # macOS
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```

2. **Copy sample and customize**:
   ```powershell
   Copy-Item ".mcp\claude_desktop_config_sample.json" "$env:APPDATA\Claude\claude_desktop_config.json"
   ```

3. **Restart Claude Desktop**

## 📚 MCP Server Resources

**Official**:
- [MCP Specification](https://modelcontextprotocol.io/)
- [Anthropic MCP Documentation](https://docs.anthropic.com/claude/docs/mcp)

**Community Servers**:
- Located in `external-libs/mcp-servers/`
- PubMed MCP: `external-libs/PubMed-MCP-Server/`
- Entrez MCP: `external-libs/entrez-mcp-server/`
- Video Editing MCP: `external-libs/video-editing-mcp/`

## 🔧 Available MCP Servers

Check `claude_desktop_config_sample.json` for:
- File system access
- Database connections
- API integrations
- Custom tool servers

## 📝 Creating Custom MCP Servers

See workflows:
- `.agent/workflows/chrome-devtools-mcp-setup.md`
- `.agent/workflows/setting-up-vercel-agent-skills.md`

---

**Last Updated**: 2026-01-23
