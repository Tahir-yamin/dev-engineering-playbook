---
description: "Standard procedure for cleaning watermarks from NotebookLM exports (PDF/Images) using SlideClean."
name: "notebooklm-cleaning"
tools: ['execute', 'python']
---

# NotebookLM Cleaning Skill

This skill defines the mandatory process for removing "NotebookLM" watermarks from exported slides and images.

## 🚨 MANDATORY PROTOCOL

**ALL** images and PDFs exported from Google NotebookLM **MUST** be processed with the SlideClean algorithm before being used in:
- White Papers
- Research Reports
- Presentations
- Public Publications

## 🛠️ Tools

- **Script**: `d:\my-dev-knowledge-base\scripts\remove_notebooklm_watermark_slideclean.py`
- **Algorithm**: "SlideClean" (Pixel Interpolation / Patch & Blend)

## 📋 Usage

### Single File
```bash
python d:\my-dev-knowledge-base\scripts\remove_notebooklm_watermark_slideclean.py "path/to/image.png"
```

### Directory
```bash
python d:\my-dev-knowledge-base\scripts\remove_notebooklm_watermark_slideclean.py "path/to/directory"
```

## 🔍 Verification
- Check output images for "clean" suffix or overwrite verification.
- Ensure the bottom-left/right watermark is completely invisible.
