---
description: Orchestrate end-to-end research, querying, and Studio content generation using Google NotebookLM with selective source management.
---

# /notebooklm-orchestrator: Advanced Research & Selective Synthesis

Use this workflow to choose your analysis strategy: Create new workbooks, analyze all sources, or target specific shared documents.

## Step 1: Strategy Selection
Before starting, choose your context strategy:

### Strategy A: Create New Workbook
Ideal for isolated research or new projects.
```bash
mcp:notebooklm:notebook_create(title="[TOPIC] Research Session")
# Then add sources...
mcp:notebooklm:notebook_add_text(notebook_id="[ID]", text="...", title="[TITLE]")
```

### Strategy B: Analyze All Sources (Unified Context)
Best for finding connections across your entire library.
```bash
mcp:notebooklm:notebook_list()
# Use notebook_id directly in queries/studio calls
```

### Strategy C: Targeted Source Analysis
Focus ONLY on the sources you just shared or specific IDs.
```bash
mcp:notebooklm:notebook_get(notebook_id="[ID]")
# Identify source_ids from the response
# Pass source_ids array to query/studio tools:
mcp:notebooklm:notebook_query(notebook_id="[ID]", query="...", source_ids=["source-uuid-1", "source-uuid-2"])
```

---

## Step 2: Advanced Research (Optional)
Expand your context with deep web/drive search.
```bash
mcp:notebooklm:research_start(query="[TARGET TOPIC]", mode="deep")
# Poll with mcp:notebooklm:research_status(notebook_id="[ID]")
# Import with mcp:notebooklm:research_import(notebook_id="[ID]", task_id="[TASK_ID]")
```

---

## Step 3: Studio Content Generation
Create professional outputs using the selected strategy.

| Artifact | Command | Use Case |
| :--- | :--- | :--- |
| **Slide Deck** | `slide_deck_create` | Presentations (Beginner/Inter/Adv) |
| **Blog/Report** | `report_create` | Summaries and deep dives |
| **Audio** | `audio_overview_create` | Passive learning/Podcasts |
| **Mind Map** | `mind_map_create` | Visual relationship mapping |

---

## Tips for Selective Output
- **Precision**: If the notebook has 50 sources but you only care about one, ALWAYS use `source_ids`.
- **Clarity**: Creating a new notebook (Strategy A) is the safest way to ensure NO hallucinations from unrelated documents.
- **Verification**: Use `studio_status` to monitor large artifact generation.
