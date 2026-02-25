"""
Proper Watermark Removal using Masking + Inpainting
Inspired by Lama Cleaner and IOPaint techniques
"""
import cv2
import numpy as np
from pathlib import Path

def create_watermark_mask(image, show_mask=False):
    """
    Create a precise mask for watermark areas
    Focus on bottom-right corner (typical NotebookLM location)
    """
    h, w = image.shape[:2]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Initialize mask
    mask = np.zeros((h, w), dtype=np.uint8)
    
    # Target bottom-right corner (NotebookLM watermark location)
    # Usually last 15% of width and last 8% of height
    watermark_h_start = int(h * 0.92)  # Bottom 8%
    watermark_w_start = int(w * 0.85)  # Right 15%
    
    # Also check for top watermarks (some PDFs have header watermarks)
    top_watermark_h_end = int(h * 0.08)  # Top 8%
    
    # Detect light text in these regions (watermarks are usually light gray)
    _, light_text = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    
    # Apply mask to bottom-right
    mask[watermark_h_start:, watermark_w_start:] = light_text[watermark_h_start:, watermark_w_start:]
    
    # Apply mask to top region
    mask[:top_watermark_h_end, :] = light_text[:top_watermark_h_end, :]
    
    # Clean up mask - remove noise
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # Dilate slightly to ensure we cover all watermark pixels
    mask = cv2.dilate(mask, kernel, iterations=1)
    
    if show_mask:
        # Show the mask for debugging
        cv2.imwrite("debug_mask.png", mask)
        print("Saved debug_mask.png to see what will be inpainted")
    
    return mask

def remove_watermark_with_inpainting(image_path, output_path, show_mask=False):
    """
    Remove watermark using mask + inpainting (Lama Cleaner technique)
    """
    # Load image
    img = cv2.imread(str(image_path))
    if img is None:
        return False, "Failed to load image"
    
    print(f"\nProcessing: {image_path.name}")
    print(f"  Image size: {img.shape[1]}x{img.shape[0]}")
    
    # Create watermark mask
    print("  Creating watermark mask...")
    mask = create_watermark_mask(img, show_mask=show_mask)
    
    # Check if watermark detected
    watermark_pixels = np.sum(mask > 0)
    print(f"  Watermark area detected: {watermark_pixels} pixels")
    
    if watermark_pixels == 0:
        print("  No watermark detected, using original")
        cv2.imwrite(str(output_path), img)
        return True, "No watermark detected"
    
    # Apply inpainting - use Telea algorithm (similar to Lama Cleaner's approach)
    print("  Applying inpainting...")
    result = cv2.inpaint(img, mask, inpaintRadius=7, flags=cv2.INPAINT_TELEA)
    
    # Optional: Apply second pass with NS algorithm for smoother results
    print("  Applying refinement...")
    result = cv2.inpaint(result, mask, inpaintRadius=5, flags=cv2.INPAINT_NS)
    
    # Save result
    cv2.imwrite(str(output_path), result)
    print(f"  Saved to: {output_path.name}")
    
    return True, f"Removed {watermark_pixels} pixels of watermark"

# Test on ONE image first
if __name__ == "__main__":
    input_dir = Path(r"d:\my-dev-knowledge-base\white-papers\wp2-images")
    output_dir = Path(r"d:\my-dev-knowledge-base\white-papers\wp2-images-masked-inpaint")
    output_dir.mkdir(exist_ok=True)
    
    # Test on Figure 1 first
    test_image = "Smarter_AI_Not_Bigger_Models_page3_img1.png"
    
    print("=" * 70)
    print("TESTING WATERMARK REMOVAL - Mask + Inpainting Technique")
    print("=" * 70)
    
    input_path = input_dir / test_image
    output_path = output_dir / test_image
    
    success, message = remove_watermark_with_inpainting(
        input_path, 
        output_path,
        show_mask=True  # Create debug_mask.png to see what was masked
    )
    
    print("\n" + "=" * 70)
    if success:
        print(f"SUCCESS: {message}")
        print(f"\nCheck the results:")
        print(f"  Original: {input_path}")
        print(f"  Cleaned: {output_path}")
        print(f"  Mask used: debug_mask.png")
    else:
        print(f"FAILED: {message}")
    print("=" * 70)
