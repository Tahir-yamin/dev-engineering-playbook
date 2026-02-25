---
name: notebooklm-mastery
description: Advanced skill for Google NotebookLM leveraging full MCP server capabilities for deep research, multi-source querying, and Studio content generation (Audio, Video, Mind Maps).
skills:
  - notebooklm
---

# NotebookLM Mastery Skill

This skill provides advanced capabilities for interacting with Google NotebookLM via the MCP server. It enables deep research, source-grounded querying, and the creation of rich Studio artifacts.

## Capabilities

### 1. Advanced Research
- **Fast Research**: Quick search (~30s, ~10 sources) for rapid exploration.
- **Deep Research**: Comprehensive search (~5min, ~40 sources) for thorough analysis.
- **Source Imports**: Automatically import discovered sources from web or Google Drive.

### 2. Multi-Source Querying
- **Context-Aware Answers**: Get answers exclusively grounded in your notebook's sources.
- **Source Targeting**: Query specific sources or the entire notebook.
- **Raw Content Access**: Quickly retrieve raw text from PDFs, websites, or YouTube transcripts.

### 3. Studio Content Generation
- **Audio Overviews**: Generate deep-dive or brief audio discussions.
- **Video Overviews**: Create explainer videos in various visual styles (Classic, Whiteboard, Anime, etc.).
- **Mind Maps**: Visualize relationships between concepts.
- **Flashcards & Quizzes**: Transform documentation into learning materials.
- **Reports & Briefings**: Generate formal documents, study guides, or blog posts.

## Tool Guide

| Action | MCP Tool | Purpose |
| :--- | :--- | :--- |
| **Search** | `research_start` | Find NEW sources on the web or Drive. |
| **Query** | `notebook_query` | Ask questions about EXISTING sources. |
| **Sync** | `source_sync_drive` | Refresh Google Drive-based sources. |
| **Studio** | `report_create`, `mind_map_create` | Generate summarized/visual assets. |

## Usage Patterns

### The "Source Isolation" Strategy (Recommended)
When you want outputs refined to *exactly* what you shared:
1. `notebook_get(notebook_id="...")` to find the UUID of the specific source.
2. `notebook_query` or `studio_tools` using the `source_ids` parameter.
3. This prevents "context leakage" from other documents in the same notebook.

### The "Deep Research" Loop
1. `research_start(query="...", mode="deep")` -> Wait for status.
2. `research_import(notebook_id="...", task_id="...")`.
3. `notebook_query(notebook_id="...", query="Synthesize findings...")`.

### The "Content Creation" Flow
1. `notebook_list()` -> Identify notebook.
2. `report_create(notebook_id="...", report_format="Blog Post")`.
3. `audio_overview_create(notebook_id="...", format="deep_dive")`.

> [!IMPORTANT]
> Always verify research status using `research_status` before attempting to import results.
