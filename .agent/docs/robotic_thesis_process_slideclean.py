"""
SlideClean Port - Watermark Removal Logic
Based on https://github.com/souravkr529/slideclean

Logic:
1. Identify watermark area (bottom-right corner usually).
2. Copy a clean patch from *immediately above* the watermark.
3. Blend it over the watermark with a feathered edge (alpha gradient) to make it seamless.
"""
import cv2
import numpy as np
import os
from pathlib import Path

# Config from index.html
WM_CONFIG = {
    "widthRatio": 0.0825, 
    "heightRatio": 0.0375,
    "marginRightRatio": 0.0025, 
    "marginBottomRatio": 0.0027,
    "featherSize": 12
}

def remove_watermark_slideclean(image_path, output_path):
    img = cv2.imread(str(image_path))
    if img is None:
        print(f"Error loading {image_path}")
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
    
    if srcY < 0:
        return False # Image too small?
        
    # Extract ROI (Region of Interest)
    # Target (Watermark area)
    dst_roi = img[y:y+wmH, x:x+wmW].astype(np.float32)
    
    # Source (Clean area above)
    src_roi = img[srcY:srcY+wmH, x:x+wmW].astype(np.float32)
    
    # Verify shapes
    if dst_roi.shape != src_roi.shape:
        print("  Shape mismatch, skipping")
        return False

    # Create feather mask (Alpha blending)
    # JS: if (i < 12) a = Math.min(a, i / 12);
    # JS: if (j < 12) a = Math.min(a, j / 12);
    
    alpha_mask = np.ones((wmH, wmW), dtype=np.float32)
    
    feather = WM_CONFIG["featherSize"]
    
    for i in range(wmH):
        for j in range(wmW):
            a = 1.0
            if i < feather:
                a = min(a, i / feather)
            if j < feather:
                a = min(a, j / feather)
            alpha_mask[i, j] = a
            
    # Expand mask for 3 channels (BGR)
    alpha_mask_3c = cv2.merge([alpha_mask, alpha_mask, alpha_mask])
    
    # Blending: res = dst * (1 - a) + src * a
    # Wait, the JS logic was: res = dst * (1 - a) + src * a
    # And a starts at 1.0, and reduces to 0.0 at edges?
    # JS Code:
    # let a = 1.0;
    # if (i < 12) a = Math.min(a, i / 12); -> a becomes small (close to 0) at top edge
    # res = dst * (1-a) + src * a
    # If a = 0 (edge), res = dst (original watermark). 
    # If a = 1 (center), res = src (clean patch).
    # This means the "feathering" makes the CLEAN PATCH disappear at the edges, revealing the original watermark? 
    # That sounds wrong if we want to hide it.
    # checking logic again...
    
    # JS: Math.round(dst.data[idx + c] * (1 - a) + src.data[idx + c] * a)
    # If a=1 (main area), we get SRC (clean). 
    # If a=0 (edge), we get DST (watermark).
    # So the edges of the patch match the underlying watermark area? That blends the patch *into* the watermark?
    # Usually you want to blend the patch into the surrounding *clean* area. 
    # But here the DST IS the watermark area. 
    # So at the top edge (i=0, a=0), we are keeping the original pixels at y.
    # But src is from y - wmH. 
    # So pixels at y are being blended with pixels at y - wmH.
    # If a=0, we keep pixel at y.
    # This implies the watermark *doesn't* start exactly at y, or the feathering is to smooth the transition.
    # Let's trust the JS logic exactly.
    
    blended = dst_roi * (1.0 - alpha_mask_3c) + src_roi * alpha_mask_3c
    
    # Put back
    img[y:y+wmH, x:x+wmW] = blended.astype(np.uint8)
    
    cv2.imwrite(str(output_path), img)
    return True

def process_target_pdf():
    input_dir = Path(r"D:\my-dev-knowledge-base\research\robotic_thesis\images_raw")
    output_dir = Path(r"D:\my-dev-knowledge-base\research\robotic_thesis\images_slideclean")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Filter for specific PDF images
    target_prefix = "Embodied_Generalist_Robotics"
    images = [f for f in input_dir.glob("*.png") if f.name.startswith(target_prefix)]
    
    print(f"Applying SlideClean to {len(images)} images from {target_prefix}...")
    
    count = 0
    for img_path in images:
        output_path = output_dir / img_path.name
        if remove_watermark_slideclean(img_path, output_path):
            print(f"  Cleaned: {img_path.name}")
            count += 1
            
    print(f"Done. Processed {count} images to {output_dir}")

if __name__ == "__main__":
    process_target_pdf()
