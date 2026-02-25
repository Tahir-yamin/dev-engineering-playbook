# Anthropic Knowledge Work Plugins Skills

**Topics**: Claude Cowork, Plugin Manifest, Slash Commands, MCP Integration
**Source**: [Anthropic Knowledge Work Plugins](https://github.com/anthropics/knowledge-work-plugins)
**Version**: 1.0 (2026 Update)

---

## Skill #1: Understanding Plugin Structure

### When to Use
- When creating a new "Digital Coworker" plugin for Claude.
- When customizing an existing plugin for specific company context.

### Implementation Pattern
Every plugin follows a strict file-based structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json     # Manifest: metadata, slash commands, entry points
├── .mcp.json           # Connector config for tool access
├── commands/           # Slash command definitions (Markdown)
└── skills/             # Domain expertise Claude draws on automatically
```

### Key Elements:
1. **Manifest (`plugin.json`)**: Defines Name, Version, and permissions.
2. **Skills**: Encoded expertise in Markdown. Claude reads these *automatically* when relevant to the context.
3. **Commands**: Explicit `/slash-commands` for deterministic actions.
4. **No-Code Architecture**: Purely Markdown and JSON.

---

## Skill #2: Customizing Plugins for Company Context

### When to Use
- Adapting generic marketing/finance/PM plugins to your team's specific tools and terminology.

### Best Practices:
- **Add Company Lingo**: Drop acronyms and org structures into your `/skills` folder.
- **Connect Real Tools**: Update `.mcp.json` to point to internal databases or APIs via MCP.
- **Refine Workflows**: Modify skill instructions to match *your* team's actual SOPs (Standard Operating Procedures).

---

## Skill #3: The "Invisible AI" Pattern (2026 Trend)

### When to Use
- Designing plugins that act as scaffolding rather than just command executors.

### Technique:
- **Observe & Propose**: Write skills that instruct Claude to watch user actions and proactively suggest /preview actions.
- **Reviewable Actions**: Ensure every major change proposed by a plugin is reviewable before execution.

---

Related Skills:
- @[auth-skills.md]
- @[ai-skills.md]
- @[mcp-debugging-skills.md]
