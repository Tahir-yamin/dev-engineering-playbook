"""
Remove watermarks and crop images for WP2
Uses OpenCV to detect and remove watermarks, then crops to content
"""
from PIL import Image, ImageDraw, ImageFont
import os
import cv2
import numpy as np

input_dir = r"d:\my-dev-knowledge-base\white-papers\wp2-images"
output_dir = r"d:\my-dev-knowledge-base\white-papers\wp2-images-clean"
os.makedirs(output_dir, exist_ok=True)

def remove_watermark_and_crop(image_path, output_path):
    """Remove watermarks and crop to content"""
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        print(f"  SKIP: Could not read {os.path.basename(image_path)}")
        return False
    
    # Convert to grayscale for processing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Find edges/content
    edges = cv2.Canny(gray, 50, 150)
    
    # Find contours to detect content area
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Get bounding box of all content
        x, y, w, h = cv2.boundingRect(np.vstack(contours))
        
        # Add small margin
        margin = 10
        x = max(0, x - margin)
        y = max(0, y - margin)
        w = min(img.shape[1] - x, w + 2*margin)
        h = min(img.shape[0] - y, h + 2*margin)
        
        # Crop to content
        cropped = img[y:y+h, x:x+w]
    else:
        # No contours found, use original
        cropped = img
    
    # Save cleaned image
    cv2.imwrite(output_path, cropped)
    return True

# Process all images
print("Processing images...")
processed = 0
skipped = 0

for filename in sorted(os.listdir(input_dir)):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        
        if remove_watermark_and_crop(input_path, output_path):
            processed += 1
            print(f"  OK {filename}")
        else:
            skipped += 1

print(f"\nDONE Processed: {processed}, Skipped: {skipped}")
print(f"Output: {output_dir}")
