"""
Targeted NotebookLM Watermark Removal
Specifically designed to remove "NotebookLM" text watermarks from research papers
"""
import cv2
import numpy as np
from pathlib import Path

def remove_notebooklm_watermark(image_path, output_path):
    """
    Remove NotebookLM watermark using targeted approach
    """
    img = cv2.imread(str(image_path))
    if img is None:
        return False
    
    h, w = img.shape[:2]
    result = img.copy()
    
    # NotebookLM watermarks are typically:
    # 1. Light gray text
    # 2. At bottom of pages
    # 3. Semi-transparent
    # 4. Repetitive pattern
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Create aggressive mask for watermark zones
    mask = np.zeros_like(gray)
    
    # Bottom 20% of image (common NotebookLM location)
    bottom_margin = int(h * 0.20)
    mask[-bottom_margin:, :] = 255
    
    # Top 15% (also common)
    top_margin = int(h * 0.15)
    mask[:top_margin, :] = 255
    
    # Left and right margins (10%)
    side_margin = int(w * 0.10)
    mask[:, :side_margin] = 255
    mask[:, -side_margin:] = 255
    
    # Detect very light text (NotebookLM watermarks are usually light gray)
    _, light_text = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    
    # Combine with zone mask
    watermark_mask = cv2.bitwise_and(light_text, mask)
    
    # Also detect text-like patterns in these zones
    edges = cv2.Canny(gray, 30, 100)
    kernel = np.ones((3,3), np.uint8)
    text_patterns = cv2.dilate(edges, kernel, iterations=2)
    text_patterns = cv2.bitwise_and(text_patterns, mask)
    
    # Combine all detections
    final_mask = cv2.bitwise_or(watermark_mask, text_patterns)
    
    # Clean up mask
    kernel = np.ones((7,7), np.uint8)
    final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_CLOSE, kernel)
    final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_OPEN, kernel)
    
    # Apply aggressive inpainting with larger radius
    if np.sum(final_mask) > 0:
        # Use Telea with large radius for text removal
        result = cv2.inpaint(result, final_mask, 10, cv2.INPAINT_TELEA)
        
        # Second pass for stubborn watermarks
        result = cv2.inpaint(result, final_mask, 7, cv2.INPAINT_NS)
    
    # Post-process to remove any remaining artifacts
    result = cv2.bilateralFilter(result, 9, 75, 75)
    
    cv2.imwrite(str(output_path), result)
    return True

# Process all WP2 images with NotebookLM-specific removal
input_dir = Path(r"d:\my-dev-knowledge-base\white-papers\wp2-images")
output_dir = Path(r"d:\my-dev-knowledge-base\white-papers\wp2-images-notebooklm-removed")
output_dir.mkdir(exist_ok=True)

print("Removing NotebookLM watermarks with targeted approach...")
print("=" * 60)

images = list(input_dir.glob("*.png")) + list(input_dir.glob("*.jpg"))
processed = 0

for img_file in sorted(images):
    print(f"Processing: {img_file.name}...", end=" ")
    output_file = output_dir / img_file.name
    
    if remove_notebooklm_watermark(img_file, output_file):
        processed += 1
        print("OK")
    else:
        print("SKIP")

print("=" * 60)
print(f"DONE - Processed {processed}/{len(images)} images")
print(f"Output: {output_dir}")
print("\nNOTE: This uses aggressive watermark removal targeting NotebookLM text")
