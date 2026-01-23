# External Libraries - Master Index

**Complete file listings for all external libraries**

---

## 📚 Available Library Indexes

### Antigravity-Specific
- **[Antigravity Awesome Skills](ANTIGRAVITY_SKILLS_INDEX.md)** - 1,872 files ✅
- **[Antigravity Kit](ANTIGRAVITY_KIT_INDEX.md)** - 278 files ✅
- **[Gemini CLI](GEMINI_CLI_INDEX.md)** - 1,643 files ✅

### Claude/Anthropic
- **[Claude Cookbooks](#claude-cookbooks)** - 416 files, 20 categories (See COMMAND_CENTER.md)
- **[Claude Subagents](CLAUDE_SUBAGENTS_INDEX.md)** - 137 agents, 66 categories ✅
- **[Claude Skills Library](#claude-skills)** - 50+ skills (Coming soon)

### MCP Servers
- **[MCP Servers](#mcp-servers)** - All 7 MCP server implementations (See COMMAND_CENTER.md)

### AI Frameworks
- **[LangGraph](#langgraph)** - 467 files (Coming soon)
- **[Vercel Agent Skills](#vercel-skills)** - 76 files (Coming soon)

---

## 🔍 Quick Search Commands

```powershell
# From knowledge base root directory:
cd d:\my-dev-knowledge-base

# Search all external libraries
Get-ChildItem external-libs, claude-cookbooks, claude-subagents -Recurse -Filter "*.md"

# Find specific topics
Get-ChildItem -Recurse -Filter "*.md" | Select-String "topic"

# List by library
Get-ChildItem external-libs\[library-name] -Recurse -File
```

---

## 📖 Usage with Antigravity

Reference any file from these indexes in your Antigravity prompts:

```markdown
# From Google Antigravity:
@[external-libs/antigravity-awesome-skills/[category]/[file].md]
@[claude-cookbooks/[category]/[file].ipynb]
@[claude-subagents/categories/[domain]/[agent].md]

Help me implement [feature] using patterns from these resources
```

**Example**:
```markdown
@[claude-subagents/categories/security-scanning/security-auditor.md]
@[skills/multi-agent-patterns-google-adk.md]

Design a secure multi-agent system for my application
```

---

**Navigate**: Use the links above to see complete file listings for each library
