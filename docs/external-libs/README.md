# External Libraries - Master Index

**Complete file listings for all external libraries**

---

## 📚 Available Library Indexes

### Antigravity-Specific
- **[Antigravity Awesome Skills](ANTIGRAVITY_SKILLS_INDEX.md)** - 1,872 files
- **[Antigravity Kit](ANTIGRAVITY_KIT_INDEX.md)** - 278 files  
- **[Gemini CLI](GEMINI_CLI_INDEX.md)** - 1,643 files

### Claude/Anthropic
- **[Claude Cookbooks](CLAUDE_COOKBOOKS_INDEX.md)** - 416 files, 20 categories
- **[Claude Subagents](CLAUDE_SUBAGENTS_INDEX.md)** - 137 agents, 66 categories
- **[Claude Skills Library](CLAUDE_SKILLS_INDEX.md)** - 50+ skills

### MCP Servers
- **[MCP Servers](MCP_SERVERS_INDEX.md)** - All 7 MCP server implementations

### AI Frameworks
- **[LangGraph](LANGGRAPH_INDEX.md)** - 467 files
- **[Vercel Agent Skills](VERCEL_SKILLS_INDEX.md)** - 76 files

---

## 🔍 Quick Search Commands

```powershell
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
@[external-libs/antigravity-awesome-skills/[category]/[file].md]
@[claude-cookbooks/[category]/[file].ipynb]
@[claude-subagents/categories/[domain]/[agent].md]

Help me implement [feature] using patterns from these resources
```

---

**Navigate**: Use the links above to see complete file listings for each library
