"""
SlideClean Watermark Remover (Global Tool)
Based on https://github.com/souravkr529/slideclean

Usage:
    python remove_notebooklm_watermark_slideclean.py <directory_or_file>

Logic:
    1. Detects images in target directory (or single file).
    2. Applies "Pixel Interpolation" (Patch & Blend) to remove NotebookLM watermarks.
    3. Saves cleaned versions (overwrites or creates _clean copy).
"""
import cv2
import numpy as np
import os
import sys
from pathlib import Path

# Config from SlideClean JS logic
WM_CONFIG = {
    "widthRatio": 0.0825, 
    "heightRatio": 0.0375,
    "marginRightRatio": 0.0025, 
    "marginBottomRatio": 0.0027,
    "featherSize": 12
}

def clean_image(image_path, output_path=None):
    if output_path is None:
        output_path = image_path # Overwrite by default if not specified? Or maybe better to be safe.
    
    img = cv2.imread(str(image_path))
    if img is None:
        return False
    
    h, w = img.shape[:2]
    
    # Calculate dimensions
    wmW = int(round(w * WM_CONFIG["widthRatio"]))
    wmH = int(round(h * WM_CONFIG["heightRatio"]))
    mr = int(round(w * WM_CONFIG["marginRightRatio"]))
    mb = int(round(h * WM_CONFIG["marginBottomRatio"]))
    
    x = w - wmW - mr
    y = h - wmH - mb
    
    # Source is immediately above the watermark
    srcY = max(0, y - wmH)
    if srcY < 0: return False

    # Extract ROIs
    dst_roi = img[y:y+wmH, x:x+wmW].astype(np.float32)
    src_roi = img[srcY:srcY+wmH, x:x+wmW].astype(np.float32)
    
    if dst_roi.shape != src_roi.shape: return False

    # Create feather mask
    alpha_mask = np.ones((wmH, wmW), dtype=np.float32)
    feather = float(WM_CONFIG["featherSize"])
    
    for i in range(wmH):
        for j in range(wmW):
            a = 1.0
            if float(i) < feather: a = min(a, float(i) / feather)
            if float(j) < feather: a = min(a, float(j) / feather)
            alpha_mask[i, j] = a
    
    alpha_mask_3c = cv2.merge([alpha_mask, alpha_mask, alpha_mask])
    
    # Blend: dst * (1-a) + src * a
    # (Matches JS logic: edges keep original, center gets clean patch)
    blended = dst_roi * (1.0 - alpha_mask_3c) + src_roi * alpha_mask_3c
    
    img[y:y+wmH, x:x+wmW] = blended.astype(np.uint8)
    
    cv2.imwrite(str(output_path), img)
    return True

def process_target(target_path):
    target = Path(target_path)
    
    if target.is_file():
        print(f"Processing file: {target.name}")
        if clean_image(target, target): # Overwrite
            print("  Cleaned.")
        else:
            print("  Failed.")
            
    elif target.is_dir():
        print(f"Processing directory: {target}")
        images = list(target.glob("*.png")) + list(target.glob("*.jpg"))
        for img in images:
            if clean_image(img, img):
                print(f"  Cleaned: {img.name}")
            else:
                print(f"  Skipped: {img.name}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        print("Usage: python remove_notebooklm_watermark_slideclean.py <dir_or_file>")
        sys.exit(1)
        
    process_target(target)
