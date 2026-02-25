import fitz  # PyMuPDF
import os
import io
import cv2
import numpy as np
import argparse

# Default Configuration
DEFAULT_DOWNLOADS_DIR = r"C:\Users\Administrator\Downloads"
DEFAULT_OUTPUT_DIR = r"d:\my-dev-knowledge-base\white-papers\wp3-images-extracted"

def clean_watermark(image_bytes, corner_size_x=150, corner_size_y=50):
    """
    Removes watermarks from image corners using heuristic inpainting.
    
    Args:
        image_bytes: Raw bytes of the image file.
        corner_size_x (int): Width of the corner area to clean.
        corner_size_y (int): Height of the corner area to clean.
        
    Returns:
        numpy.ndarray: The cleaned image, or None if processing fails.
    """
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        return None

    h, w = img.shape[:2]
    mask = np.zeros(img.shape[:2], np.uint8)
    
    # Heuristic: Define regions in bottom corners (common for page numbers/logos)
    # Bottom Right
    cv2.rectangle(mask, (w - corner_size_x, h - corner_size_y), (w, h), 255, -1)
    # Bottom Left
    cv2.rectangle(mask, (0, h - corner_size_y), (corner_size_x, h), 255, -1)
    
    # Telea inpainting is fast and effective for small, static areas
    cleaned = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
    return cleaned

def extract_images(pdf_dir, output_dir, min_size_kb=30):
    """
    Extracts images from all PDF files in the specified directory.
    
    Args:
        pdf_dir (str): Directory containing PDF files.
        output_dir (str): Directory to save extracted images.
        min_size_kb (int): Minimum file size in KB to keep (filters icons).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
        
    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"No PDF files found in {pdf_dir}")
        return

    total_extracted = 0
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_dir, pdf_file)
        print(f"Processing {pdf_file}...")
        
        try:
            doc = fitz.open(pdf_path)
        except Exception as e:
            print(f"Failed to open {pdf_file}: {e}")
            continue
        
        for i in range(len(doc)):
            try:
                page = doc[i]
                image_list = page.get_images(full=True)
                
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    
                    # Filter small images
                    if len(image_bytes) < 1024 * min_size_kb:
                        continue
                        
                    # Clean watermark
                    cleaned_img = clean_watermark(image_bytes)
                    
                    if cleaned_img is not None:
                        out_name = f"{os.path.splitext(pdf_file)[0]}_p{i}_img{img_index}.jpg"
                        out_path = os.path.join(output_dir, out_name)
                        cv2.imwrite(out_path, cleaned_img)
                        print(f"  Saved: {out_name}")
                        total_extracted += 1
            except Exception as e:
                print(f"  Error on page {i}: {e}")
                
    print(f"\nExtraction complete. Total images saved: {total_extracted}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract and clean images from PDFs.")
    parser.add_argument("--input", "-i", default=DEFAULT_DOWNLOADS_DIR, help="Input directory containing PDFs")
    parser.add_argument("--output", "-o", default=DEFAULT_OUTPUT_DIR, help="Output directory for images")
    parser.add_argument("--min-size", "-s", type=int, default=30, help="Minimum image size in KB")
    
    args = parser.parse_args()
    
    print(f"Starting extraction from {args.input} to {args.output}...")
    extract_images(args.input, args.output, args.min_size)
