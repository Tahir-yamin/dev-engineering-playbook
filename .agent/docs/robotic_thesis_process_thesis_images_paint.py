"""
Graceful Watermark Removal (Paint Over) - Robotic Thesis Edition
Fixed version
"""
import cv2
import os
import numpy as np
from pathlib import Path

def paint_over_watermarks(image_path, output_path):
    # Read image
    img = cv2.imread(str(image_path))
    if img is None:
        print(f"Error loading {image_path}")
        return False
    
    h, w = img.shape[:2]
    
    # Define white color (BGR)
    white = (255, 255, 255)
    
    # 1. Paint over Bottom Footer (NotebookLM signature)
    # usually bottom 60 pixels
    cv2.rectangle(img, (0, h - 80), (w, h), white, -1)
    
    # 2. Paint over Top Header
    # usually top 80 pixels
    cv2.rectangle(img, (0, 0), (w, 100), white, -1)
    
    # Write to output
    cv2.imwrite(str(output_path), img)
    return True

def batch_process():
    input_dir = Path(r"D:\my-dev-knowledge-base\research\robotic_thesis\images_raw")
    output_dir = Path(r"D:\my-dev-knowledge-base\research\robotic_thesis\images_clean")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get images
    images = list(input_dir.glob("*.png"))
    print(f"Processing {len(images)} images...")
    
    count = 0
    for img_path in images:
        output_path = output_dir / img_path.name
        if paint_over_watermarks(img_path, output_path):
            print(f"Cleaned: {img_path.name}")
            count += 1
            
    print(f"Done. Processed {count} images.")

if __name__ == "__main__":
    batch_process()
