"""
Professional Watermark Removal Tool
Multi-algorithm approach with quality selection
"""
import cv2
import numpy as np
import os
from pathlib import Path

class WatermarkRemover:
    """Advanced watermark removal using multiple CV algorithms"""
    
    def __init__(self, image_path):
        self.image = cv2.imread(str(image_path))
        if self.image is None:
            raise ValueError(f"Could not load image: {image_path}")
        self.original = self.image.copy()
        self.h, self.w = self.image.shape[:2]
        
    def detect_watermark_auto(self):
        """Auto-detect watermark regions using multiple methods"""
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        # Method 1: Detect very light/faded text (typical watermarks)
        _, light_mask = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)
        
        # Method 2: Detect edges/text-like patterns
        edges = cv2.Canny(gray, 30, 100)
        kernel = np.ones((3,3), np.uint8)
        edge_mask = cv2.dilate(edges, kernel, iterations=1)
        
        # Method 3: Focus on typical watermark zones
        zone_mask = np.zeros_like(gray)
        
        # Common watermark locations:
        margin_v = int(self.h * 0.15)  # Top/bottom 15%
        margin_h = int(self.w * 0.15)  # Left/right 15%
        corner_size = int(min(self.h, self.w) * 0.20)  # 20% corners
        
        # Top and bottom margins
        zone_mask[:margin_v, :] = 255
        zone_mask[-margin_v:, :] = 255
        
        # Left and right margins
        zone_mask[:, :margin_h] = 255
        zone_mask[:, -margin_h:] = 255
        
        # Also add center region (common for watermarks)
        center_h, center_w = self.h // 2, self.w // 2
        center_size_h, center_size_w = self.h // 4, self.w // 4
        zone_mask[center_h-center_size_h:center_h+center_size_h,
                 center_w-center_size_w:center_w+center_size_w] = 128
        
        # Combine masks intelligently
        combined = cv2.bitwise_and(light_mask, zone_mask)
        combined = cv2.bitwise_or(combined, cv2.bitwise_and(edge_mask, zone_mask))
        
        # Clean up mask
        kernel = np.ones((5,5), np.uint8)
        combined = cv2.morphologyEx(combined, cv2.MORPH_CLOSE, kernel)
        combined = cv2.morphologyEx(combined, cv2.MORPH_OPEN, kernel)
        
        return combined
    
    def remove_with_multi_inpaint(self, mask):
        """Use both inpainting algorithms and blend"""
        # TELEA - fast marching method
        result_telea = cv2.inpaint(self.image, mask, 5, cv2.INPAINT_TELEA)
        
        # Navier-Stokes - fluid dynamics based
        result_ns = cv2.inpaint(self.image, mask, 5, cv2.INPAINT_NS)
        
        # Blend results - TELEA better for text, NS better for regions
        alpha = 0.6  # Favor TELEA slightly
        result = cv2.addWeighted(result_telea, alpha, result_ns, 1-alpha, 0)
        
        return result, result_telea, result_ns
    
    def remove_with_texture_patch(self, mask):
        """Texture-based removal using patch matching"""
        result = self.image.copy()
        
        # Find watermark regions
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            # Skip very small regions
            if cv2.contourArea(contour) < 100:
                continue
                
            x, y, w, h = cv2.boundingRect(contour)
            
            # Get surrounding clean region
            pad = max(20, int(max(w, h) * 0.5))
            x1 = max(0, x - pad)
            y1 = max(0, y - pad)
            x2 = min(self.w, x + w + pad)
            y2 = min(self.h, y + h + pad)
            
            # Extract patch
            patch = self.image[y1:y2, x1:x2].copy()
            
            # Create mask for this patch
            patch_mask = np.zeros(patch.shape[:2], dtype=np.uint8)
            px, py = x - x1, y - y1
            patch_mask[py:py+h, px:px+w] = 255
            
            # Inpaint this specific patch
            patch_clean = cv2.inpaint(patch, patch_mask, 7, cv2.INPAINT_TELEA)
            
            # Apply to result
            result[y1:y2, x1:x2] = patch_clean
        
        return result
    
    def post_process(self, image):
        """Final enhancement"""
        # Bilateral filter to reduce artifacts while preserving edges
        smoothed = cv2.bilateralFilter(image, 9, 50, 50)
        
        # Very subtle sharpening
        kernel_sharpen = np.array([[-0.5,-0.5,-0.5],
                                   [-0.5, 5.0,-0.5],
                                   [-0.5,-0.5,-0.5]])
        sharpened = cv2.filter2D(smoothed, -1, kernel_sharpen)
        
        # Blend for natural look
        result = cv2.addWeighted(smoothed, 0.8, sharpened, 0.2, 0)
        
        return result
    
    def process_full_pipeline(self, output_path, auto_detect=True, custom_mask=None):
        """
        Complete watermark removal pipeline
        
        Args:
            output_path: Where to save result
            auto_detect: Use automatic detection (default: True)
            custom_mask: Optional manual mask (numpy array)
        
        Returns:
            Cleaned image as numpy array
        """
        # Get watermark mask
        if custom_mask is not None:
            mask = custom_mask
        elif auto_detect:
            print("  Auto-detecting watermarks...")
            mask = self.detect_watermark_auto()
        else:
            raise ValueError("Must provide custom_mask or set auto_detect=True")
        
        # Skip if no watermark detected
        if np.sum(mask) == 0:
            print("  No watermark detected, using original")
            cv2.imwrite(str(output_path), self.image)
            return self.image
        
        print(f"  Watermark mask area: {np.sum(mask > 0)} pixels")
        
        # Try multiple algorithms
        print("  Applying multi-algorithm inpainting...")
        blended, result_telea, result_ns = self.remove_with_multi_inpaint(mask)
        
        print("  Applying texture-based removal...")
        result_texture = self.remove_with_texture_patch(mask)
        
        # Select best result by measuring artifacts in non-watermark regions
        inv_mask = cv2.bitwise_not(mask)
        
        # Calculate how much the results differ from original in clean areas
        diff_blended = np.mean(cv2.absdiff(self.original, blended)[inv_mask > 0])
        diff_texture = np.mean(cv2.absdiff(self.original, result_texture)[inv_mask > 0])
        
        print(f"  Quality scores - Blended: {diff_blended:.2f}, Texture: {diff_texture:.2f}")
        
        # Choose result with least change to clean areas
        if diff_blended < diff_texture:
            final = blended
            print("  Selected: Blended inpainting")
        else:
            final = result_texture
            print("  Selected: Texture-based")
        
        # Post-process
        print("  Post-processing...")
        final = self.post_process(final)
        
        # Save
        cv2.imwrite(str(output_path), final)
        print(f"  Saved to: {output_path}")
        
        return final

def batch_remove_watermarks(input_dir, output_dir):
    """Process all images in a directory"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    image_files = list(input_path.glob("*.png")) + list(input_path.glob("*.jpg")) + list(input_path.glob("*.jpeg"))
    
    print(f"\nProcessing {len(image_files)} images...")
    print("=" * 60)
    
    for i, img_file in enumerate(sorted(image_files), 1):
        print(f"\n[{i}/{len(image_files)}] {img_file.name}")
        
        try:
            remover = WatermarkRemover(img_file)
            output_file = output_path / img_file.name
            remover.process_full_pipeline(output_file)
            print("  SUCCESS")
        except Exception as e:
            print(f"  ERROR: {e}")
    
    print(f"\n{'=' * 60}")
    print(f"DONE - Processed {len(image_files)} images")
    print(f"Output directory: {output_path}")

if __name__ == "__main__":
    # Usage
    input_dir = r"d:\my-dev-knowledge-base\white-papers\wp2-images"
    output_dir = r"d:\my-dev-knowledge-base\white-papers\wp2-images-professional"
    
    batch_remove_watermarks(input_dir, output_dir)
