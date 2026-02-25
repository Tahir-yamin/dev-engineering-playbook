# Watermark Removal Guide for White Papers

## Automated Removal (Recommended)

We have developed a custom Python script that automatically extracts images from PDFs and removes corner watermarks using Computer Vision inpainting.

**How to use:**
1. Place source PDFs in your `Downloads` folder.
2. Run: `python scripts/extract_pdf_images.py`
3. Check `white-papers/wp3-images-extracted` for the cleaned results.

**Why this is better:**
- **Quality**: Extracts raw binary data from PDF (lossless) instead of screenshots.
- **Speed**: Processes dozens of images in seconds.
- **Clean**: Automatically erases page numbers/logos from corners.

## Manual Options (Fallback)

### Option 1: Google Photos Magic Eraser
1. Upload images to Google Photos
2. Open image in editor -> "Magic Eraser"
3. Select watermark areas

### Option 2: Photoshop Generative Fill
1. Select watermark with lasso tool
2. Choose "Generative Fill" (leave prompt empty)

## Current Script Location
- `scripts/extract_pdf_images.py`

