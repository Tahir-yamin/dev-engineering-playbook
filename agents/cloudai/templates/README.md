# Templates

These are files you copy to your own project and customize.

## CLAUDE.md.template

Team-shared development guidelines. Copy to your project root:

```bash
cp CLAUDE.md.template /path/to/your/project/CLAUDE.md
```

Then customize:
- Package manager commands
- Test/build/lint commands
- Code conventions
- Architecture decisions

## settings.local.json.template

Recommended permissions for Claude Code. Copy to your project's `.claude/` directory:

```bash
mkdir -p /path/to/your/project/.claude
cp settings.local.json.template /path/to/your/project/.claude/settings.local.json
```

This pre-allows common safe commands so you don't get prompted every time.
