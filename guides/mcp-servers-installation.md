# MCP Servers Installation Guide

**What Are MCP Servers?**  
MCP (Model Context Protocol) servers are npm packages that extend AI capabilities by connecting to external tools, databases, and services.

**Location**: Not local files - they're GitHub repositories you need to install

---

## 🎬 **Video Editing MCP Servers**

### 1. DaVinci Resolve MCP
**GitHub**: https://github.com/samuelgursky/davinci-resolve-mcp  
**What it does**: Control DaVinci Resolve video editor from AI  
**Features**: Video editing, color grading, media management

#### Installation:
```bash
# Option 1: Using npx (no install needed)
# Just configure in Claude Desktop

# Option 2: Clone from GitHub
cd d:\my-dev-knowledge-base\external-libs
git clone https://github.com/samuelgursky/davinci-resolve-mcp.git
cd davinci-resolve-mcp
npm install
```

#### Setup in Claude Desktop:
Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (Mac)  
Or `%APPDATA%/Claude/claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "davinci-resolve": {
      "command": "node",
      "args": ["d:/my-dev-knowledge-base/external-libs/davinci-resolve-mcp/index.js"]
    }
  }
}
```

---

### 2. Video Editor MCP
**GitHub**: https://github.com/burningion/video-editing-mcp  
**What it does**: Add, edit, and search videos via Video Jungle  
**Integration**: https://www.video-jungle.com/

#### Installation:
```bash
# Clone the repository
cd d:\my-dev-knowledge-base\external-libs
git clone https://github.com/burningion/video-editing-mcp.git
cd video-editing-mcp
npm install
```

#### Setup in Claude:
```json
{
  "mcpServers": {
    "video-editor": {
      "command": "node",
      "args": ["d:/my-dev-knowledge-base/external-libs/video-editing-mcp/build/index.js"],
      "env": {
        "VIDEO_JUNGLE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

---

## 📚 **Research MCP Servers**

### 3. PubMed MCP
**GitHub**: https://github.com/JackKuo666/PubMed-MCP-Server  
**What it does**: Search PubMed for medical/scientific articles  
**Database**: 35+ million biomedical citations

#### Installation:
```bash
# Clone the repository
cd d:\my-dev-knowledge-base\external-libs
git clone https://github.com/JackKuo666/PubMed-MCP-Server.git
cd PubMed-MCP-Server
npm install
```

#### Setup in Claude:
```json
{
  "mcpServers": {
    "pubmed": {
      "command": "node",
      "args": ["d:/my-dev-knowledge-base/external-libs/PubMed-MCP-Server/build/index.js"]
    }
  }
}
```

#### Usage Example:
```
"Search PubMed for recent papers on AI in healthcare published in 2025"
```

---

### 4. Scholarly MCP
**GitHub**: https://github.com/adityak74/mcp-scholarly  
**What it does**: Search scholarly and academic articles  
**Sources**: Google Scholar, academic databases

#### Installation:
```bash
# Clone the repository
cd d:\my-dev-knowledge-base\external-libs
git clone https://github.com/adityak74/mcp-scholarly.git
cd mcp-scholarly
npm install
```

#### Setup in Claude:
```json
{
  "mcpServers": {
    "scholarly": {
      "command": "node",
      "args": ["d:/my-dev-knowledge-base/external-libs/mcp-scholarly/build/index.js"]
    }
  }
}
```

---

### 5. Entrez MCP (NCBI)
**GitHub**: https://github.com/QuentinCody/entrez-mcp-server  
**What it does**: Access NCBI Entrez databases  
**Databases**: PubMed, Gene, Protein, Nucleotide, etc.

#### Installation:
```bash
# Clone the repository
cd d:\my-dev-knowledge-base\external-libs
git clone https://github.com/QuentinCody/entrez-mcp-server.git
cd entrez-mcp-server
npm install
```

#### Setup in Claude:
```json
{
  "mcpServers": {
    "entrez": {
      "command": "node",
      "args": ["d:/my-dev-knowledge-base/external-libs/entrez-mcp-server/build/index.js"],
      "env": {
        "NCBI_API_KEY": "your-ncbi-api-key"
      }
    }
  }
}
```

**Get NCBI API Key**: https://www.ncbi.nlm.nih.gov/account/settings/

---

## 🚀 **Quick Install All**

```powershell
# Navigate to external-libs
cd d:\my-dev-knowledge-base\external-libs

# Clone all MCP servers
git clone https://github.com/samuelgursky/davinci-resolve-mcp.git
git clone https://github.com/burningion/video-editing-mcp.git
git clone https://github.com/JackKuo666/PubMed-MCP-Server.git
git clone https://github.com/adityak74/mcp-scholarly.git
git clone https://github.com/QuentinCody/entrez-mcp-server.git

# Install dependencies for each
cd davinci-resolve-mcp && npm install && cd ..
cd video-editing-mcp && npm install && cd ..
cd PubMed-MCP-Server && npm install && cd ..
cd mcp-scholarly && npm install && cd ..
cd entrez-mcp-server && npm install && cd ..
```

---

## 📝 **Complete Claude Config Example**

Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "davinci-resolve": {
      "command": "node",
      "args": ["d:/my-dev-knowledge-base/external-libs/davinci-resolve-mcp/index.js"]
    },
    "video-editor": {
      "command": "node",
      "args": ["d:/my-dev-knowledge-base/external-libs/video-editing-mcp/build/index.js"],
      "env": {
        "VIDEO_JUNGLE_API_KEY": "your-api-key"
      }
    },
    "pubmed": {
      "command": "node",
      "args": ["d:/my-dev-knowledge-base/external-libs/PubMed-MCP-Server/build/index.js"]
    },
    "scholarly": {
      "command": "node",
      "args": ["d:/my-dev-knowledge-base/external-libs/mcp-scholarly/build/index.js"]
    },
    "entrez": {
      "command": "node",
      "args": ["d:/my-dev-knowledge-base/external-libs/entrez-mcp-server/build/index.js"],
      "env": {
        "NCBI_API_KEY": "your-ncbi-key"
      }
    }
  }
}
```

---

## 🔍 **Where to Find More MCP Servers**

**Full List**: `d:\my-dev-knowledge-base\external-libs\mcp-servers\README.md`

This file contains **100+ MCP servers** for:
- Databases (PostgreSQL, SQLite, MongoDB)
- Cloud services (AWS, Azure, GCP)
- Development tools (GitHub, GitLab, Docker)
- Communication (Slack, Discord, Email)
- And much more!

**Browse**: 
```powershell
code d:\my-dev-knowledge-base\external-libs\mcp-servers\README.md
```

---

## ⚙️ **After Installation**

1. **Restart Claude Desktop**
2. **Test the servers**:
   ```
   "Use PubMed to search for AI research papers from 2025"
   ```

3. **Check if working**:
   - Claude should show MCP tools in the sidebar
   - Tools should appear when you mention them

---

## 🆘 **Troubleshooting**

### Server Not Found:
- Check the path in config file
- Verify `npm install` completed
- Look for `build/index.js` or `index.js` in repo

### API Key Errors:
- Get keys from:
  - Video Jungle: https://www.video-jungle.com/
  - NCBI: https://www.ncbi.nlm.nih.gov/account/settings/

### Permission Errors:
```powershell
# Run as Administrator
npm install --global windows-build-tools
```

---

**Summary**: These are external tools you install via npm/git, then configure in Claude Desktop to use them!
