"""
Simple Watermark Removal by Cropping - Robotic Thesis Edition
Adapted from scripts/crop_watermarks.py

Strategy:
- Remove bottom 20% (NotebookLM watermark area)
- Remove top 10% (Header/Page number area)
- Keep the middle 70% which contains the figure
"""
from PIL import Image
from pathlib import Path
import os

def crop_margins(image_path, output_path):
    try:
        img = Image.open(image_path)
        width, height = img.size
        
        # Crop Logic:
        # Top: Remove 10%
        # Bottom: Remove 20% (NotebookLM is quite tall)
        
        top = int(height * 0.10)
        bottom = int(height * 0.80) 
        
        # (left, top, right, bottom)
        cropped = img.crop((0, top, width, bottom))
        
        cropped.save(output_path)
        print(f"  Cropped: {image_path.name}")
        return True
    except Exception as e:
        print(f"  Error processing {image_path.name}: {e}")
        return False

def batch_process():
    # Use RAW images as source to avoid double-processing
    input_dir = Path(r"D:\my-dev-knowledge-base\research\robotic_thesis\images_raw")
    output_dir = Path(r"D:\my-dev-knowledge-base\research\robotic_thesis\images_cropped")
    output_dir.mkdir(exist_ok=True)
    
    # Get all images
    images = list(input_dir.glob("*.png"))
    print(f"Processing {len(images)} images from {input_dir}")
    print("-" * 50)
    
    count = 0
    for img_path in sorted(images):
        output_path = output_dir / img_path.name
        if crop_margins(img_path, output_path):
            count += 1
            
    print("-" * 50)
    print(f"Done. Cropped {count} images to {output_dir}")

if __name__ == "__main__":
    batch_process()
