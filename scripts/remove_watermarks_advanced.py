"""
Advanced watermark removal using inpainting
Detects watermarks and removes them with image inpainting
"""
from PIL import Image
import cv2
import numpy as np
import os

input_dir = r"d:\my-dev-knowledge-base\white-papers\wp2-images"
output_dir = r"d:\my-dev-knowledge-base\white-papers\wp2-images-final"
os.makedirs(output_dir, exist_ok=True)

def remove_watermark_inpaint(image_path, output_path):
    """Remove watermarks using advanced inpainting"""
    img = cv2.imread(image_path)
    if img is None:
        return False
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold to detect watermark (usually light/faded)
    # Watermarks are typically lighter than content
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    
    # Find watermark regions (small text/logos usually at edges)
    # Also check for repeated patterns across image
    
    # Method 1: Detect very light regions (watermarks)
    _, light_mask = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)
    
    # Method 2: Detect edges and text-like patterns
    edges = cv2.Canny(gray, 50, 150)
    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=1)
    
    # Combine masks - focus on top/bottom margins where watermarks usually are
    h, w = img.shape[:2]
    margin = int(h * 0.1)  # Top/bottom 10%
    
    mask = np.zeros_like(gray)
    # Focus on margins
    mask[:margin, :] = light_mask[:margin, :]  # Top margin
    mask[-margin:, :] = light_mask[-margin:, :]  # Bottom margin
    
    # Also check for watermarks in corners
    corner_size = int(min(h, w) * 0.15)
    mask[:corner_size, :corner_size] = light_mask[:corner_size, :corner_size]  # Top-left
    mask[:corner_size, -corner_size:] = light_mask[:corner_size, -corner_size:]  # Top-right
    mask[-corner_size:, :corner_size] = light_mask[-corner_size:, :corner_size]  # Bottom-left
    mask[-corner_size:, -corner_size:] = light_mask[-corner_size:, -corner_size:]  # Bottom-right
    
    # If mask has significant content,  use inpainting
    if np.sum(mask) > 0:
        # Inpaint to remove watermark
        result = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
    else:
        result = img
    
    # Crop to content (remove white margins)
    # Convert to grayscale for edge detection
    gray_result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray_result, 250, 255, cv2.THRESH_BINARY_INV)
    
    # Find bounding box of content
    coords = cv2.findNonZero(binary)
    if coords is not None:
        x, y, w, h = cv2.boundingRect(coords)
        # Add small margin
        margin = 5
        x = max(0, x - margin)
        y = max(0, y - margin)
        w = min(result.shape[1] - x, w + 2*margin)
        h = min(result.shape[0] - y, h + 2*margin)
        
        result = result[y:y+h, x:x+w]
    
    cv2.imwrite(output_path, result)
    return True

# Process all images
print("Removing watermarks with inpainting...")
processed = 0

for filename in sorted(os.listdir(input_dir)):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        
        if remove_watermark_inpaint(input_path, output_path):
            processed += 1
            print(f"  OK {filename}")

print(f"\nDONE Processed: {processed}")
print(f"Output: {output_dir}")
print("\nRecommend reviewing images and using these cleaned versions in WP2")
