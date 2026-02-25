---
description: Adapt technical white papers for Medium.com (Markdown/LaTeX to Medium).
---

# Medium Publishing Workflow

## Trigger
Use `/medium-publish` to adapt a technical document for Medium.

## Context
Medium.com DOES NOT support:
- LaTeX Math (`$E=mc^2$`)
- Markdown Tables
- Direct File Uploads (PDF/MD)

## Procedure

1.  **Create "Medium Draft" Artifact**:
    -   Duplicate the source Markdown file (e.g., `_Medium_Draft.md`).
    -   **DO NOT** modify the original source.

2.  **Flatten Tables**:
    -   Convert all Markdown tables into bulleted lists or static image placeholders.
    -   *Medium renders tables as unreadable text blocks.*

3.  **Replace Math**:
    -   Convert LaTeX equations to Unicode text equivalents where possible.
    -   For complex equations, take a screenshot and insert as an image.

4.  **Image Handling**:
    -   Ensure all local image paths are resolved to absolute paths for easy finding.
    -   Add `[INSERT IMAGE HERE]` placeholders if specific placement is needed.

5.  **Output Guide**:
    -   Generate a `MEDIUM_PUBLISHING_INSTRUCTIONS.md` file.
    -   Explicitly tell the user to "Copy and Paste" the text and "Drag and Drop" the images.

## Related Workflows
- `/linkedin-publish` - Cross-post article to LinkedIn
- `/write-white-paper` - Original source creation
