# Skill Seekers

**Source**: [yusufkaraaslan/Skill_Seekers](https://github.com/yusufkaraaslan/Skill_Seekers)  
**Version**: 2.7.0  
**Author**: @yusufkaraaslan  
**License**: MIT

---

## Overview

Convert documentation websites, GitHub repositories, and PDFs into Claude AI skills with automatic conflict detection. Supports multi-LLM platforms.

---

## Key Features

### 🌐 Documentation Scraping
Scrape any documentation site and convert to skill format.

### 📄 PDF Support
Extract knowledge from PDF documents.

### 🐙 GitHub Repository Scraping
Three-stream architecture for efficient repo analysis.

### 🤖 Multi-LLM Platform Support
Works with: Claude, GPT, Gemini, Anthropic API

### 🎯 Codebase Analysis & AI Enhancement
Analyze codebases and generate enhanced AI skills.

---

## Installation

### PyPI (Recommended)
```bash
pip install skill-seekers
```

### uv (Modern Python Tool)
```bash
uv add skill-seekers
```

### MCP Integration
Add to MCP config for Claude Code / Antigravity:
```json
{
  "mcpServers": {
    "skill-seekers": {
      "command": "uvx",
      "args": ["skill-seekers", "mcp"]
    }
  }
}
```

---

## Usage Examples

### Documentation Scraping
```bash
skill-seekers scrape https://docs.example.com --output skills/
```

### PDF Extraction
```bash
skill-seekers pdf ./document.pdf --output skills/
```

### GitHub Repository Scraping
```bash
skill-seekers github owner/repo --output skills/
```

### Unified Multi-Source
```bash
skill-seekers multi \
  --url https://docs.example.com \
  --github owner/repo \
  --pdf ./doc.pdf \
  --output skills/
```

---

## MCP Tools Available (18 Total)

| Tool | Description |
|------|-------------|
| `scrape_docs` | Scrape documentation website |
| `extract_pdf` | Extract from PDF |
| `scrape_github` | Analyze GitHub repo |
| `generate_skill` | Generate skill file |
| `upload_skill` | Upload to Claude |
| ... | And 13 more |

---

## Output Structure

```
skills/
├── SKILL.md           # Main skill file
├── knowledge/         # Scraped knowledge
│   ├── category1.md
│   └── category2.md
└── metadata.json      # Skill metadata
```

---

## Related Skills

- [documentation-maintenance](../../.agent/workflows/documentation-maintenance.md)

---

**Added to Knowledge Base**: 2026-01-22  
**Credit**: @yusufkaraaslan
