# Content Creation & Research Skills - Quick Reference

**Purpose**: Skills for video editing, research papers, articles, and content creation  
**Installed**: 2026-01-19  
**Location**: `.agent/agents/`

---

## ✅ **Installed Skills**

### 1. **Technical Writer** (`technical-writer.md`)
**Use for**: Research papers, technical articles, documentation

**Capabilities**:
- ✅ Research paper writing
- ✅ Technical articles
- ✅ Academic documentation
- ✅ API documentation
- ✅ User guides
- ✅ White papers
- ✅ Case studies
- ✅ Technical content

**How to use**:
```markdown
@technical-writer "Write a research paper on AI agents for my university project"
```

---

### 2. **Content Marketer** (`content-marketer.md`)
**Use for**: Blog posts, articles, marketing content

**Capabilities**:
- ✅ Blog posts
- ✅ Articles
- ✅ Social media content
- ✅ White papers
- ✅ Case studies
- ✅ Ebooks
- ✅ SEO-optimized content
- ✅ Email campaigns

**How to use**:
```markdown
@content-marketer "Write a blog post about AI ecosystem trends in 2026"
```

---

### 3. **Research Analyst** (`research-analyst.md`)
**Use for**: Research, data analysis, academic papers

**Capabilities**:
- ✅ Comprehensive research
- ✅ Data analysis
- ✅ Academic research
- ✅ Market research
- ✅ Trend analysis
- ✅ Report writing
- ✅ Statistical analysis
- ✅ Literature review

**How to use**:
```markdown
@research-analyst "Research the latest AI agent frameworks and create a comparative analysis"
```

---

## 🎬 **Video Editing (via MCP Servers)**

### Available MCP Servers:

#### 1. **DaVinci Resolve MCP**
**Repository**: https://github.com/sam​uelgursky/davinci-resolve-mcp  
**Capabilities**:
- Video editing
- Color grading
- Media management
- Project control

**Setup**:
```json
{
  "mcpServers": {
    "davinci-resolve": {
      "command": "npx",
      "args": ["-y", "davinci-resolve-mcp"]
    }
  }
}
```

#### 2. **Video Editor MCP** 
**Repository**: https://github.com/burningion/video-editing-mcp  
**Integration**: Video Jungle (https://www.video-jungle.com/)  
**Capabilities**:
- Add videos
- Edit videos
- Search videos
- Video management

**Setup**:
```json
{
  "mcpServers": {
    "video-editor": {
      "command": "npx",
      "args": ["-y", "video-editing-mcp"]
    }
  }
}
```

---

## 📚 **Additional Research Resources**

### MCP Servers for Research:

#### **PubMed MCP**
- Search medical/scientific articles
- Access biomedical research
- Repository: https://github.com/JackKuo666/PubMed-MCP-Server

#### **Scholarly MCP**
- Search academic articles
- Research papers
- Repository: https://github.com/adityak74/mcp-scholarly

#### **Entrez MCP**
- NCBI databases access
- Gene information
- Protein data
- Repository: https://github.com/QuentinCody/entrez-mcp-server

---

## 🚀 **Quick Start Examples**

### Research Paper:
```markdown
"I need to write a research paper on multi-agent systems. Use the research-analyst 
agent to find recent papers, then technical-writer to create an academic paper 
with proper citations."
```

### Blog Article:
```markdown
"Write a 1500-word blog article about AI ecosystem monitoring. Use content-marketer
agent with SEO optimization for technology blogs."
```

### Video Project:
```markdown
"I want to edit my tutorial video. Set up the Video Editor MCP server so I can 
manage my video clips and create a final edit."
```

---

## 📁 **Where Everything Is**

| Resource Type | Location |
|---------------|----------|
| **Agents** | `.agent/agents/` |
| **Full Subagent Library** | `external-libs/awesome-claude-code-subagents/categories/` |
| **MCP Server List** | `external-libs/mcp-servers/README.md` |
| **Skills Library** | `external-libs/skills/skills/` |

---

## 💡 **More Available Skills**

From `awesome-claude-code-subagents`:

### Business & Product (08):
- business-analyst
- customer-success-manager
- legal-advisor
- product-manager
- project-manager
- sales-engineer
- scrum-master
- ux-researcher

### Research & Analysis (10):
- competitive-analyst
- data-researcher
- market-researcher
- search-specialist
- trend-analyst

**Total**: 137 specialized subagents available!

---

## 🔧 **Installation Commands**

### Copy more agents:
```powershell
# Copy all business agents
Copy-Item "d:\my-dev-knowledge-base\external-libs\awesome-claude-code-subagents\categories\08-business-product\*.md" -Destination "d:\my-dev-knowledge-base\.agent\agents\" -Force

# Copy all research agents
Copy-Item "d:\my-dev-knowledge-base\external-libs\awesome-claude-code-subagents\categories\10-research-analysis\*.md" -Destination "d:\my-dev-knowledge-base\.agent\agents\" -Force
```

### Install MCP servers:
```bash
# Install video editing MCP
npm install -g video-editing-mcp
npm install -g davinci-resolve-mcp

# Install research MCPs
npm install -g @jkkuo/pubmed-mcp-server
npm install -g mcp-scholarly
```

---

**You now have professional writing, research, and video editing capabilities!** 📝🎬📊
