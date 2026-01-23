# MCP Servers Setup Guide - Quick Start

**Date**: 2026-01-19  
**Purpose**: Step-by-step setup for video editing and research MCP servers

---

## ✅ **What You Have Installed**

Successfully cloned 5 MCP servers:

### 🎬 Video Editing:
1. **davinci-resolve-mcp** - Control DaVinci Resolve
2. **video-editing-mcp** - Video Jungle integration

### 📚 Research:
3. **PubMed-MCP-Server** - Medical/scientific papers
4. **mcp-scholarly** - Academic research
5. **entrez-mcp-server** - NCBI databases

**Location**: `d:\my-dev-knowledge-base\external-libs\`

---

## 📋 **Step 1: Install Python Dependencies**

### Check Python Version:
```powershell
python --version
# Should be Python 3.8 or higher
```

### Install Dependencies:
```powershell
# Navigate to external-libs
cd d:\my-dev-knowledge-base\external-libs

# DaVinci Resolve MCP
cd davinci-resolve-mcp
pip install -r requirements.txt
cd ..

# PubMed MCP
cd PubMed-MCP-Server
pip install -r requirements.txt
cd ..

# Scholarly MCP
cd mcp-scholarly
pip install -e .
cd ..

# Entrez MCP
cd entrez-mcp-server
pip install -e .
cd ..

# Video Editing MCP (if it has requirements)
cd video-editing-mcp
pip install -r requirements.txt
```

---

## 🔧 **Step 2: Configure Claude Desktop**

### Windows Configuration File:
**Location**: `%APPDATA%\Claude\claude_desktop_config.json`

Create or edit this file:

```json
{
  "mcpServers": {
    "davinci-resolve": {
      "command": "python",
      "args": [
        "d:/my-dev-knowledge-base/external-libs/davinci-resolve-mcp/resolve_mcp_server.py"
      ]
    },
    "pubmed": {
      "command": "python",
      "args": [
        "d:/my-dev-knowledge-base/external-libs/PubMed-MCP-Server/pubmed_server.py"
      ]
    },
    "scholarly": {
      "command": "python",
      "args": [
        "-m",
        "mcp_scholarly"
      ],
      "cwd": "d:/my-dev-knowledge-base/external-libs/mcp-scholarly"
    },
    "entrez": {
      "command": "python",
      "args": [
        "-m",
        "entrez_mcp_server"
      ],
      "cwd": "d:/my-dev-knowledge-base/external-libs/entrez-mcp-server",
      "env": {
        "NCBI_API_KEY": "YOUR_NCBI_API_KEY_HERE"
      }
    },
    "video-editor": {
      "command": "python",
      "args": [
        "d:/my-dev-knowledge-base/external-libs/video-editing-mcp/server.py"
      ],
      "env": {
        "VIDEO_JUNGLE_API_KEY": "YOUR_VIDEO_JUNGLE_API_KEY_HERE"
      }
    }
  }
}
```

### Quick Access to Config:
```powershell
# Open config file in notepad
notepad $env:APPDATA\Claude\claude_desktop_config.json
```

---

## 🔑 **Step 3: Get API Keys**

### 1️⃣ **NCBI API Key** (Required for Entrez MCP)

**Why**: Access to PubMed and NCBI databases  
**Cost**: FREE

**Steps**:
1. Go to: https://www.ncbi.nlm.nih.gov/account/register/
2. Create an NCBI account (free)
3. Log in and go to: https://www.ncbi.nlm.nih.gov/account/settings/
4. Scroll to "API Key Management"
5. Click "Create an API Key"
6. Copy your API key

**Add to config**:
```json
"env": {
  "NCBI_API_KEY": "paste-your-key-here"
}
```

---

### 2️⃣ **Video Jungle API Key** (Required for Video Editor MCP)

**Why**: Video editing and management  
**Cost**: Check pricing at https://www.video-jungle.com/

**Steps**:
1. Go to: https://www.video-jungle.com/
2. Sign up for an account
3. Navigate to API settings or developer section
4. Generate an API key
5. Copy your API key

**Add to config**:
```json
"env": {
  "VIDEO_JUNGLE_API_KEY": "paste-your-key-here"
}
```

---

### 3️⃣ **DaVinci Resolve** (No API Key Needed!)

**Requirements**:
- DaVinci Resolve installed on your machine
- DaVinci Resolve must be running
- No API key required!

---

### 4️⃣ **PubMed MCP** (No API Key Needed!)

**Free to use!** No API key required for basic usage.

---

### 5️⃣ **Scholarly MCP** (No API Key Needed!)

**Free to use!** Searches Google Scholar without API key.

---

## 🚀 **Step 4: Test Your Setup**

### 1. Restart Claude Desktop
Close and reopen Claude Desktop to load the new configuration.

### 2. Verify MCP Servers
In Claude Desktop, you should see MCP tools in the sidebar or tool menu.

### 3. Test Each Server

#### Test PubMed:
```
"Search PubMed for recent papers on AI in healthcare from 2025"
```

#### Test Scholarly:
```
"Find academic papers about machine learning published in 2024"
```

#### Test Entrez (if you have API key):
```
"Search NCBI databases for gene information about BRCA1"
```

#### Test DaVinci Resolve (if you have it running):
```
"Get the current project timeline information from DaVinci Resolve"
```

#### Test Video Editor (if you have API key):
```
"List my videos in Video Jungle"
```

---

## 🐛 **Troubleshooting**

### MCP Server Not Showing Up?

1. **Check config file location**:
   ```powershell
   cat $env:APPDATA\Claude\claude_desktop_config.json
   ```

2. **Verify Python path**:
   ```powershell
   where python
   # Should show: C:\Users\...\Python\python.exe
   ```

3. **Test MCP server manually**:
   ```powershell
   cd d:\my-dev-knowledge-base\external-libs\PubMed-MCP-Server
   python pubmed_server.py
   # Should start without errors
   ```

4. **Check Claude Desktop logs**:
   ```powershell
   # Logs are usually in:
   # %APPDATA%\Claude\logs\
   ```

### Python Import Errors?

```powershell
# Reinstall dependencies
cd d:\my-dev-knowledge-base\external-libs\PubMed-MCP-Server
pip install -r requirements.txt --force-reinstall
```

### Permission Errors?

```powershell
# Run as Administrator
# Right-click PowerShell → "Run as Administrator"
```

---

## 📝 **Usage Examples**

### Research Papers:
```
"Search PubMed for papers about CRISPR published in the last 6 months"
"Find Google Scholar articles on quantum computing from MIT"
"Get gene information for TP53 from NCBI"
```

### Video Editing (with DaVinci Resolve):
```
"Get current timeline details"
"List all clips in the current project"
```

### Video Management (with Video Jungle):
```
"Upload this video to Video Jungle"
"Search for videos tagged 'tutorial'"
```

---

## 🎯 **Next Steps**

1. ✅ Start with **PubMed** and **Scholarly** (no API keys needed!)
2. ✅ Get **NCBI API key** for advanced research
3. ⏳ Get **Video Jungle API key** if you need video management
4. ⏳ Install **DaVinci Resolve** if you need professional video editing

---

## 📚 **Additional Resources**

- **Full installation guide**: `guides/mcp-servers-installation.md`
- **Content creation guide**: `skills/content-creation-research-guide.md`
- **All MCP servers list**: `external-libs/mcp-servers/README.md`

---

## ✨ **Summary**

**What Works Now (No API Keys)**:
- ✅ PubMed MCP - Search medical papers
- ✅ Scholarly MCP - Search academic research

**What Needs API Keys**:
- 🔑 Entrez MCP - NCBI API key (FREE)
- 🔑 Video Editor MCP - Video Jungle API key (PAID)

**What Needs Software**:
- 💿 DaVinci Resolve MCP - DaVinci Resolve installed

**Start here**: Test PubMed and Scholarly first - they work immediately! 🚀
