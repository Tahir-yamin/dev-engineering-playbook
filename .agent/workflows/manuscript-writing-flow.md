---
description: Comprehensive workflow for writing Q1 Journal manuscripts using AI tools safely in 2025-2026.
---

# Q1 Manuscript Writing Workflow (2026 Edition)

## When to Use
- Starting a high-impact research paper.
- Converting a thesis or report into a journal-ready manuscript.
- Ensuring compliance with modern (2026) AI disclosure policies.
- **Special Track**: Engineering, Energy & Technical Papers (IEEE/Elsevier).
- **Review Track**: Systematic Reviews (PRISMA).
- **Privacy Track**: High-security/IP-sensitive research (Prismer).

---

## Step 1: Discovery & Gap Analysis
1. Use **Perplexity Pro** (Academic Focus) to find the top 5 most cited papers in your niche from 2024-2026.
2. Upload these to **NotebookLM** to create a "Research Grounding" source.
3. Ask NotebookLM: "What are the specific unresolved questions mentioned in the 'Future Work' sections of these papers?"

## Step 2: Drafting - Choose Your Tool
### Option A: Cloud Speed (OpenAI Prism / Claude)
1. **Tool**: OpenAI Prism (New Jan 2026).
2. **Action**: Create project, invite collaborators.
3. **Drafting**: Use built-in citation finder to populate references.
4. **Warning**: Do not upload IP-sensitive/proprietary industrial data.

### Option B: Privacy & Control (Prismer - Self-Hosted)
1. **Tool**: **Prismer** (GitHub: `Prismer-AI/Prismer`).
2. **Setup**: Run locally to ensure data never leaves your machine.
3. **Action**: Upload PDFs to Prismer's context manager.
4. **Analysis**: Use the **integrated Jupyter Notebooks** to run your Python data analysis *side-by-side* with your draft.
5. **Drafting**: Write directly in the AI-assisted LaTeX editor.
6. **Advantage**: Seamless transition from Data -> Analysis -> Text without context switching.

## Step 3: Humanization & Voice Integration
1. Apply the **Humanization Skill**: Rewrite sections to include unique laboratory constraints/instrument specifics.
2. **Engineering Special**: Ensure no LLM generated the *experimental design* (prohibited by IEEE).
3. **Gap Check**: Use **Consensus.app** to verify your claims don't contradict 2026 consensus.

## Step 4: Technical Formatting & LaTeX
1. **If using Prismer**: You are already in a LaTeX environment. Use its compilation check.
2. **If using Cloud Tools**: Export to **Overleaf**.
3. Use **Overleaf AI / TeXGPT** to fix compilation errors.
4. Use **Mathpix** to convert handwritten formulas to LaTeX.

## Step 5: Verification & AI Detection Check
1. Run the draft through **Turnitin** (if available) or **GPTZero (2026 Enterprise)**.
2. **Prismer Feature**: Use its built-in *Citation Verification* to ensure no references were hallucinated.
3. **Scite.ai**: Final check for retracted papers.

## Step 6: Disclosure & Submission
1. **General Disclosure**: "The authors acknowledge the use of [Tool Name] for language refinement."
2. **Prismer Disclosure**: "This manuscript was drafted using the Prismer research platform for citations management and LaTeX compilation."
3. **IEEE Specific**: "No AI tools were used to generate experimental results or code logic."

---

Related: [Q1 Writing Skills](file:///d:/my-dev-knowledge-base/skills/q1-journal-writing-skills.md)
