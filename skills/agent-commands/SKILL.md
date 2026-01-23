# Agent Commands (mitsuhiko)

**Source**: [mitsuhiko/agent-stuff](https://github.com/mitsuhiko/agent-stuff)  
**Author**: @mitsuhiko (Armin Ronacher - Flask creator)  
**License**: MIT

---

## Overview

Commands for Claude/AI agents focused on session management and release automation. Created by Armin Ronacher (creator of Flask).

---

## Commands

### /handoff

**Purpose**: Creates detailed handoff plan for session continuation.

**When to Use**:
- Before ending a long session
- When another agent will continue work
- For context preservation

**Usage**:
```
/handoff
```

**Creates**:
- Session summary
- Current state documentation
- Next steps plan
- Context for pickup

---

### /pickup

**Purpose**: Resumes work from previous handoff session.

**When to Use**:
- Starting new session after handoff
- Continuing work from another agent
- Resuming interrupted work

**Usage**:
```
/pickup
```

**Reads**:
- Previous handoff notes
- Session state
- Pending tasks

---

### /make-release

**Purpose**: Automates repository release with version management.

**When to Use**:
- Publishing new version
- Creating tagged release
- Version bump with changelog

**Usage**:
```
/make-release [major|minor|patch]
```

**Performs**:
- Version bump
- Changelog update
- Git tag creation
- Release notes generation

---

### /update-changelog

**Purpose**: Updates changelog with recent commits.

**When to Use**:
- Before release
- After feature merges
- Regular maintenance

**Usage**:
```
/update-changelog
```

**Generates**:
- Commit summaries
- Categorized changes
- Date stamps

---

## Skills Available

From the agent-stuff repository:

| Skill | Purpose |
|-------|---------|
| `browser` | Browser automation skill |
| `tmux` | Terminal multiplexer management |
| `sentry` | Error tracking integration |
| `improve-skill` | Self-improvement prompts |
| `ghidra` | Reverse engineering tool |

---

## Installation

### Add to Your Workspace

1. Clone repo:
```bash
git clone https://github.com/mitsuhiko/agent-stuff.git
```

2. Copy commands to your `.agent/workflows/`:
```bash
cp agent-stuff/commands/* .agent/workflows/
```

3. Copy skills to your `skills/`:
```bash
cp -r agent-stuff/skills/* skills/
```

---

## Why Use These

1. **Session Continuity** - Never lose context between sessions
2. **Release Automation** - Consistent release process
3. **Best Practices** - From experienced engineer (Flask creator)

---

**Added to Knowledge Base**: 2026-01-22  
**Credit**: @mitsuhiko (Armin Ronacher)
