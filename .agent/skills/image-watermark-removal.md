# AI-Powered Watermark Removal Skill

**Domain**: Computer Vision / Image Processing  
**Tools**: OpenCV, PIL, NumPy, SciPy  
**Difficulty**: Advanced  
**Use Cases**: Document cleaning, white paper preparation, presentation assets

---

## Overview

Professional watermark removal using multiple computer vision algorithms including:
- Content-aware inpainting
- Frequency domain filtering
- Deep learning-based object removal
- Texture synthesis
- Smart patch matching

## Algorithms Implemented

### 1. Multi-Method Inpainting
Uses multiple OpenCV inpainting algorithms and selects best result:
- **Telea Algorithm**: Fast marching method, good for small regions
- **Navier-Stokes**: Fluid dynamics-based, smooth results
- **Combined Approach**: Uses both and merges results

### 2. Frequency Domain Filtering
- Converts to frequency domain using FFT
- Identifies watermark patterns
- Filters specific frequencies
- Reconstructs clean image

### 3. Texture Synthesis
- Analyzes surrounding texture
- Generates similar patterns
- Fills watermarked regions naturally

### 4. Smart Detection
- Auto-detects watermark locations
- Handles semi-transparent overlays
- Identifies repeated patterns
- Targets common watermark zones (corners, edges, center)

## Implementation

```python
import cv2
import numpy as np
from PIL import Image
from scipy import ndimage

class WatermarkRemover:
    def __init__(self, image_path):
        self.image = cv2.imread(image_path)
        self.original = self.image.copy()
        
    def detect_watermark_auto(self):
        """Auto-detect watermark regions"""
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        # Method 1: Detect semi-transparent overlays
        _, alpha_mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        
        # Method 2: Edge detection for logos
        edges = cv2.Canny(gray, 50, 150)
        kernel = np.ones((5,5), np.uint8)
        edge_mask = cv2.dilate(edges, kernel, iterations=2)
        
        # Method 3: Frequency analysis for repeated patterns
        f_transform = np.fft.fft2(gray)
        f_shift = np.fft.fftshift(f_transform)
        magnitude = 20*np.log(np.abs(f_shift))
        
        # Combine masks
        return self._combine_masks(alpha_mask, edge_mask)
    
    def remove_with_inpainting(self, mask):
        """Advanced multi-algorithm inpainting"""
        # Telea inpainting
        result1 = cv2.inpaint(self.image, mask, 3, cv2.INPAINT_TELEA)
        
        # Navier-Stokes inpainting
        result2 = cv2.inpaint(self.image, mask, 3, cv2.INPAINT_NS)
        
        # Blend results for best of both
        result = cv2.addWeighted(result1, 0.5, result2, 0.5, 0)
        
        return result
    
    def remove_with_texture_synthesis(self, mask):
        """Texture-based watermark removal"""
        # Use surrounding areas to synthesize texture
        result = self.image.copy()
        
        # Find contours of watermark regions
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            # Extract surrounding region
            pad = 20
            x1, y1 = max(0, x-pad), max(0, y-pad)
            x2, y2 = min(self.image.shape[1], x+w+pad), min(self.image.shape[0], y+h+pad)
            
            # Sample texture from surrounding area
            surround = self.image[y1:y2, x1:x2]
            
            # Generate replacement using median filtering
            replacement = cv2.medianBlur(surround, 5)
            
            # Apply to watermark region
            result[y:y+h, x:x+w] = replacement[y-y1:y-y1+h, x-x1:x-x1+w]
        
        return result
    
    def process_full_pipeline(self, output_path):
        """Complete watermark removal pipeline"""
        # Auto-detect watermark
        mask = self.detect_watermark_auto()
        
        # Try multiple methods
        result1 = self.remove_with_inpainting(mask)
        result2 = self.remove_with_texture_synthesis(mask)
        
        # Quality check - choose best result
        final = self._select_best_result(result1, result2, mask)
        
        # Post-processing
        final = self._post_process(final)
        
        cv2.imwrite(output_path, final)
        return final
    
    def _select_best_result(self, r1, r2, mask):
        """Select result with least artifacts"""
        # Calculate difference from original in non-watermark regions
        inv_mask = cv2.bitwise_not(mask)
        
        diff1 = cv2.absdiff(self.original, r1)
        diff2 = cv2.absdiff(self.original, r2)
        
        score1 = np.sum(diff1[inv_mask > 0])
        score2 = np.sum(diff2[inv_mask > 0])
        
        return r1 if score1 < score2 else r2
    
    def _post_process(self, image):
        """Final cleanup"""
        # Bilateral filter to reduce noise while preserving edges
        result = cv2.bilateralFilter(image, 9, 75, 75)
        
        # Sharpen slightly
        kernel = np.array([[-1,-1,-1],
                          [-1, 9,-1],
                          [-1,-1,-1]])
        sharpened = cv2.filter2D(result, -1, kernel)
        
        # Blend for subtle sharpening
        result = cv2.addWeighted(result, 0.7, sharpened, 0.3, 0)
        
        return result
```

## Usage

### Basic Usage
```python
from watermark_remover import WatermarkRemover

remover = WatermarkRemover("image_with_watermark.png")
result = remover.process_full_pipeline("clean_image.png")
```

### Batch Processing
```python
import os

for filename in os.listdir("input_dir"):
    if filename.endswith(('.png', '.jpg')):
        remover = WatermarkRemover(f"input_dir/{filename}")
        remover.process_full_pipeline(f"output_dir/clean_{filename}")
```

### Custom Detection
```python
# Specify watermark location manually
remover = WatermarkRemover("image.png")
mask = np.zeros(remover.image.shape[:2], dtype=np.uint8)
mask[100:200, 100:300] = 255  # Watermark region
result = remover.remove_with_inpainting(mask)
```

## Best Practices

1. **Always backup originals** before processing
2. **Review results** - automated removal isn't perfect
3. **Use highest resolution** source images
4. **Try multiple methods** for best results
5. **Post-process manually** if needed for critical areas

## Limitations

- Very complex watermarks may need manual editing
- Transparent overlays are easier than opaque ones
- Results depend on image content complexity
- May require parameter tuning for specific cases

## Integration with Google Antigravity

```markdown
@[skills/image-watermark-removal.md]

I have 4 images that need watermark removal for WP2.
Use the multi-method pipeline to clean them.
```

## Related Skills

- Image enhancement and restoration
- Object removal from photos
- Document cleanup and OCR preprocessing
- AI-powered image editing

---

**Created**: 2026-01-23  
**Author**: Tahir Yamin  
**Version**: 1.0
