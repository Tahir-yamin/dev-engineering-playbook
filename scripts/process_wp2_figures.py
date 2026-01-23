"""
Process all 4 WP2 images with mask + inpainting
"""
import cv2
import numpy as np
from pathlib import Path

def create_watermark_mask(image):
    """Create mask for watermark areas"""
    h, w = image.shape[:2]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    mask = np.zeros((h, w), dtype=np.uint8)
    
    # Target bottom-right (NotebookLM watermark)
    watermark_h_start = int(h * 0.92)
    watermark_w_start = int(w * 0.85)
    
    # Target top (header watermarks)
    top_watermark_h_end = int(h * 0.08)
    
    # Detect light text
    _, light_text = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    
    # Apply masks
    mask[watermark_h_start:, watermark_w_start:] = light_text[watermark_h_start:, watermark_w_start:]
    mask[:top_watermark_h_end, :] = light_text[:top_watermark_h_end, :]
    
    # Clean up
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.dilate(mask, kernel, iterations=1)
    
    return mask

def remove_watermark(image_path, output_path):
    """Remove watermark using mask + inpainting"""
    img = cv2.imread(str(image_path))
    if img is None:
        return False
    
    print(f"  {image_path.name}")
    
    mask = create_watermark_mask(img)
    watermark_pixels = np.sum(mask > 0)
    
    if watermark_pixels == 0:
        cv2.imwrite(str(output_path), img)
        print(f"    No watermark detected")
        return True
    
    print(f"    Removing {watermark_pixels} pixels...")
    
    # Dual inpainting for best results
    result = cv2.inpaint(img, mask, 7, cv2.INPAINT_TELEA)
    result = cv2.inpaint(result, mask, 5, cv2.INPAINT_NS)
    
    cv2.imwrite(str(output_path), result)
    print(f"    Done")
    
    return True

# Process all 4 WP2 figures
if __name__ == "__main__":
    input_dir = Path(r"d:\my-dev-knowledge-base\white-papers\wp2-images")
    output_dir = Path(r"d:\my-dev-knowledge-base\white-papers\wp2-images-clean-final")
    output_dir.mkdir(exist_ok=True)
    
    # The 4 WP2 figures
    wp2_figures = [
        "Smarter_AI_Not_Bigger_Models_page3_img1.png",
        "Beyond_Scale_Structure_Truth_page4_img1.png",
        "Smarter_AI_Not_Bigger_Models_page7_img1.png",
        "Smarter_AI_Not_Bigger_page5_img1.png"
    ]
    
    print("Processing WP2 Figures - Mask + Inpainting")
    print("=" * 60)
    
    for fig in wp2_figures:
        input_path = input_dir / fig
        output_path = output_dir / fig
        remove_watermark(input_path, output_path)
    
    print("=" * 60)
    print(f"DONE - All {len(wp2_figures)} figures processed")
    print(f"Output: {output_dir}")
