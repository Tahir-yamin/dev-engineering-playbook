"""
Professional Watermark Removal - Robotic Thesis Edition
Adapted from scripts/watermark_remover_pro.py
"""
import cv2
import numpy as np
import os
from pathlib import Path

class WatermarkRemover:
    def __init__(self, image_path):
        self.image = cv2.imread(str(image_path))
        if self.image is None:
            raise ValueError(f"Could not load image: {image_path}")
        self.original = self.image.copy()
        self.h, self.w = self.image.shape[:2]
        
    def detect_watermark_auto(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        # Method 1: Detect very light/faded text
        _, light_mask = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)
        
        # Method 2: Detect edges
        edges = cv2.Canny(gray, 30, 100)
        kernel = np.ones((3,3), np.uint8)
        edge_mask = cv2.dilate(edges, kernel, iterations=1)
        
        # Method 3: Zone Mask (Top/Bottom 15%, Sides 15%)
        zone_mask = np.zeros_like(gray)
        margin_v = int(self.h * 0.15)
        margin_h = int(self.w * 0.15)
        
        zone_mask[:margin_v, :] = 255
        zone_mask[-margin_v:, :] = 255
        zone_mask[:, :margin_h] = 255
        zone_mask[:, -margin_h:] = 255
        
        # Combine masks
        combined = cv2.bitwise_and(light_mask, zone_mask)
        combined = cv2.bitwise_or(combined, cv2.bitwise_and(edge_mask, zone_mask))
        
        # Clean up
        kernel = np.ones((5,5), np.uint8)
        combined = cv2.morphologyEx(combined, cv2.MORPH_CLOSE, kernel)
        combined = cv2.morphologyEx(combined, cv2.MORPH_OPEN, kernel)
        
        return combined
    
    def remove_with_multi_inpaint(self, mask):
        # TELEA
        result_telea = cv2.inpaint(self.image, mask, 5, cv2.INPAINT_TELEA)
        # Navier-Stokes
        result_ns = cv2.inpaint(self.image, mask, 5, cv2.INPAINT_NS)
        # Blend (favor TELEA)
        alpha = 0.6
        result = cv2.addWeighted(result_telea, alpha, result_ns, 1-alpha, 0)
        return result
    
    def post_process(self, image):
        # Bilateral filter for smoothing while preserving edges
        smoothed = cv2.bilateralFilter(image, 9, 50, 50)
        # Subtle sharpening
        kernel_sharpen = np.array([[-0.5,-0.5,-0.5], [-0.5, 5.0,-0.5], [-0.5,-0.5,-0.5]])
        sharpened = cv2.filter2D(smoothed, -1, kernel_sharpen)
        # Blend
        result = cv2.addWeighted(smoothed, 0.8, sharpened, 0.2, 0)
        return result

    def process(self, output_path):
        print(f"  Auto-detecting watermarks...")
        mask = self.detect_watermark_auto()
        
        if np.sum(mask) == 0:
            print("  No watermark detected, saving original.")
            cv2.imwrite(str(output_path), self.image)
            return
            
        print(f"  Inpainting {np.sum(mask>0)} pixels...")
        result = self.remove_with_multi_inpaint(mask)
        
        print("  Post-processing...")
        final = self.post_process(result)
        
        cv2.imwrite(str(output_path), final)
        print(f"  Saved to: {output_path}")

def batch_process():
    input_dir = Path(r"D:\my-dev-knowledge-base\research\robotic_thesis\images_raw")
    output_dir = Path(r"D:\my-dev-knowledge-base\research\robotic_thesis\images_pro")
    output_dir.mkdir(exist_ok=True)
    
    images = list(input_dir.glob("*.png"))
    print(f"Processing {len(images)} images from {input_dir}")
    
    for i, img_path in enumerate(images, 1):
        print(f"\n[{i}/{len(images)}] {img_path.name}")
        try:
            remover = WatermarkRemover(img_path)
            output_path = output_dir / img_path.name
            remover.process(output_path)
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    batch_process()
