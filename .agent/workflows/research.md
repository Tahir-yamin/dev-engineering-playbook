---
description: Consolidate all research, technical writing, and LaTeX resources into a master index
---

# Research & Writing Resource Index Workflow

This workflow consolidates all skills, agents, workflows, and files related to high-impact Q1 journal writing, technical research, and LaTeX/Markdown conversion within this workspace into a single master index.

## Steps

1. **Search for Core Skills**
   - Search for files matching `*journal*`, `*writing*`, and `*latex*` in `d:\my-dev-knowledge-base\skills`.
   - Identify key skills: `q1-journal-writing-skills.md`, `white-paper-writing-skills.md`, `latex-cv-skills.md`, `autonomous-operator-directives.md`.

2. **Search for Agents & Roles**
   - Search for agents related to "research" and "writing" in `d:\my-dev-knowledge-base\.agent\rules` and `external-libs`.
   - Identify key agents: `research-technical-spike.agent.md`, `se-technical-writer.agent.md`, `task-researcher.agent.md`.

3. **Search for Templates & Scripts**
   - Locate LaTeX templates in `skills\latex-conversion\`.
   - Locate conversion scripts (Python) in `job-application\scripts\` and `external-libs`.
   - **MANDATORY**: Use `scripts\remove_notebooklm_watermark_slideclean.py` for all NotebookLM exports.
   - **MANDATORY**: Use `scripts\convert_md_to_html.py` for HTML/Print-to-PDF fallback.
   - **RECOMMENDED**: Use `workflows\medium-publishing-workflow.md` for blog adaptations.

4. **Verify Governance Rules**
   - Check `d:\my-dev-knowledge-base\.agent\rules` for mandatory protocols.
   - Check `d:\my-dev-knowledge-base\external-libs\WriteHERE` for framework documentation.

5. **Generate Index File**
   - Compile all findings into `C:\Users\Administrator\.gemini\antigravity\brain\419b8a00-bf17-494d-b9bc-255902dfb865\RESEARCH_AND_WRITING_INDEX.md`.
   - Ensure the index includes:
     - **Governance & Protocols**: Mandatory rules.
     - **Core Skills**: Links to skill files.
     - **Agents**: specialized roles.
     - **Templates**: LaTeX and document templates.
     - **Tools**: Conversion scripts and commands.

## Usage

Run this workflow to refresh the index if new research tools or skills are added to the workspace.
