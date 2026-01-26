---
description: Automated workflow for extracting and cleaning images from PDF white papers
---

# White Paper Image Preparation Workflow

This workflow automates the process of extracting high-quality images from PDF source files and removing common watermarks (like page numbers or logos in corners) using computer vision techniques.

## Prerequisites

- Python 3.x
- `scripts/extract_pdf_images.py`
- Source PDFs in `Downloads` folder (or custom location)

## Workflow Steps

1. **Prepare Source PDFs**
   - Place your source PDF files (e.g., scientific papers, reports) in your `Downloads` folder.
   - Alternatively, place them in a dedicated `source_pdfs` directory.

2. **Run Extraction Script**
   Run the extraction tool from the project root:
   ```powershell
   python scripts/extract_pdf_images.py
   ```
   
   **Options:**
   - Specify input directory: `python scripts/extract_pdf_images.py -i "path/to/pdfs"`
   - Specify output directory: `python scripts/extract_pdf_images.py -o "white-papers/my-images"`
   - Filter small images: `python scripts/extract_pdf_images.py --min-size 50` (KB)

3. **Review Extracted Images**
   - Navigate to `white-papers/wp3-images-extracted` (default output).
   - View the images to ensure watermarks are successfully removed and quality is sufficient.

4. **Select and Rename**
   - Choose the best figures for your white paper.
   - Copy them to a final folder (e.g., `white-papers/wp3-images-final`).
   - Rename them descriptively (e.g., `wp3-concept-diagram.jpg`).

5. **Update Markdown**
   - Update your `.md` file to reference the new images.
   - Add detailed captions.

## How It Works

The script `scripts/extract_pdf_images.py` combines two powerful steps:
1.  **PyMuPDF Extraction**: Pulls raw image streams from the PDF (better than screenshots).
2.  **OpenCV Inpainting**: Automatically detects corners (where watermarks live) and uses the Telea inpainting algorithm to erase them and fill the gap with surrounding textures.

// turbo-all
