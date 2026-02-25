---
description: Convert text or files into professional LaTeX format using premium templates.
---

# LaTeX Conversion Workflow

## Trigger
Use `/latex` or `/latex-conversion` to start a document conversion.

## Steps

1.  **Selection**: Identify the source text or file to convert.
2.  **Analysis**: Determine the appropriate LaTeX document class (Article, Report, Beamer).
3.  **Generation**: 
    *   Load templates from `skills/latex-conversion/SKILL.md`.
    *   Convert Markdown/Text into LaTeX, ensuring:
        *   Headings map to `\section`, `\subsection`.
        *   Lists map to `itemize` or `enumerate`.
        *   Math uses proper `$...$` or `\[ ... \]` delimiters.
        *   Tables follow `booktabs` style.
4.  **Verification**: Perform a mental "compilation check" for common syntax errors.
5.  **Output**: Provide the full LaTeX source code to the user.

## Example
User: `/latex convert my summary.md to an article`
AI: *Generates LaTeX article code based on summary.md content.*

## ⚠️ Windows Compilation Troubleshooting (2026)

**Critical Finding:** Automated installation of LaTeX distributions (MiKTeX, TeX Live, Tectonic) via Chocolatey is highly unreliable in restricted Windows environments.

**Recommended Protocol:**
1.  **Manual Install:** Always prefer manual installation of [MiKTeX](https://miktex.org/download) or a pre-downloaded [Tectonic](https://tectonic-typesetting.github.io/) executable.
2.  **HTML Fallback:** If PDF compilation fails, use `scripts/convert_md_to_html.py` to generate a high-fidelity HTML version that can be "Printed to PDF".
3.  **Tectonic Warning:** Chocolatey often serves outdated Tectonic versions (v0.3.x) which fail to connect to bundle repositories. Use local binaries only.
