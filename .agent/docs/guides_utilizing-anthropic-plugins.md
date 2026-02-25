# Utilizing Anthropic Knowledge Work Plugins

Anthropic's "Knowledge Work Plugins" are modular, file-based extensions that turn Claude into a domain expert for specific roles.

## 1. Available Plugins (The "Marketplace")

Anthropic has open-sourced 11 core plugins:
1.  **Productivity**: Tasks, calendars, and personal workflows.
2.  **Enterprise Search**: Cross-tool information retrieval.
3.  **Product Management**: Writing specs and roadmaps.
4.  **Sales**: Prospect research and deal prep.
5.  **Marketing**: Content drafting and campaign planning.
6.  **Data**: Dataset querying and visualization.
7.  **Customer Support**: Triage and response drafting.
8.  **Finance**: Financial modeling and metric tracking.
9.  **Legal**: Document review and compliance.
10. **Biology Research**: Literature search and experiment planning.
11. **Plugin Management**: Creating and customizing your own plugins.

## 2. Why They are Beneficial

- **Modular Expertise**: You don't need a single prompt to do everything. Load a "Sales" plugin only when doing sales work.
- **Deterministic Commands**: Use symbols like `/pm:write-spec` to trigger specific, predefined workflows instead of relying on fuzzy natural language.
- **Easy Customization**: Because they are just Markdown and JSON files, you can update them by simply changing the text in your workspace.
- **Tool Connectivity**: They link Claude directly to your internal tools via MCP (Model Context Protocol).

## 3. How to Utilize Them Here

I have cloned the official repository into `external-libs/knowledge-work-plugins`. You can utilize them in several ways:

### A. Use as Templates
Copy a folder (e.g., `product-management`) to your own project and modify the `skills/` and `commands/` to fit your specific needs.

### B. Reference Skills via Antigravity
You can direct me to "Read the skills from the Marketing plugin" by referencing the path:
`@[external-libs/knowledge-work-plugins/marketing/skills/marketing-strategy.md]`

### C. Build Custom Slash Commands
Follow the manifest structure in `.claude-plugin/plugin.json`:
1.  **Define command**: Add a name and description in `plugin.json`.
2.  **Create Markdown guide**: Write the prompt for that command in `commands/command-name.md`.
3.  **Execute**: Invoke via `/command-name` in supported environments like Claude Code or Cowork.

---
**Location**: `d:\my-dev-knowledge-base\external-libs\knowledge-work-plugins`
