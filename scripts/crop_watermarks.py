"""
Simple watermark removal by cropping margins
Just crop out the top/bottom where watermarks appear
"""
from PIL import Image
from pathlib import Path

def crop_watermark_margins(image_path, output_path):
    """Crop top and bottom margins to remove watermarks"""
    img = Image.open(image_path)
    width, height = img.size
    
    # Crop margins (watermarks usually in top 10% and bottom 10%)
    top_crop = int(height * 0.10)  # Remove top 10%
    bottom_crop = int(height * 0.90)  # Keep only top 90%
    
    # Crop: (left, top, right, bottom)
    cropped = img.crop((0, top_crop, width, bottom_crop))
    
    cropped.save(output_path)
    print(f"Cropped: {image_path.name} -> {output_path.name}")
    return cropped

# Process WP2 images
input_dir = Path(r"d:\my-dev-knowledge-base\white-papers\wp2-images")
output_dir = Path(r"d:\my-dev-knowledge-base\white-papers\wp2-images-cropped")
output_dir.mkdir(exist_ok=True)

print("Cropping watermark margins from images...")
print("=" * 60)

images = list(input_dir.glob("*.png")) + list(input_dir.glob("*.jpg"))

for img_file in sorted(images):
    output_file = output_dir / img_file.name
    crop_watermark_margins(img_file, output_file)

print("=" * 60)
print(f"DONE - Cropped {len(images)} images")
print(f"Output: {output_dir}")
print("\nWatermarks removed by cropping margins!")
