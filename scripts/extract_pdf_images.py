"""
Extract images from PDFs, remove watermarks, and crop for WP2
"""
import fitz  # PyMuPDF
import os
from PIL import Image
import io

# PDF files to process
pdf_files = [
    r"C:\Users\Administrator\Downloads\Smarter_AI_Not_Bigger_Models.pdf",
    r"C:\Users\Administrator\Downloads\Beyond_Scale_Structure_Truth.pdf",
    r"C:\Users\Administrator\Downloads\Smarter_AI_Not_Bigger.pdf"
]

# Output directory
output_dir = r"d:\my-dev-knowledge-base\white-papers\wp2-images"
os.makedirs(output_dir, exist_ok=True)

def extract_images_from_pdf(pdf_path):
    """Extract all images from PDF"""
    pdf_name = os.path.basename(pdf_path).replace('.pdf', '')
    print(f"\nProcessing: {pdf_name}")
    
    doc = fitz.open(pdf_path)
    images_extracted = 0
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        images = page.get_images()
        
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # Save image
            image_filename = f"{pdf_name}_page{page_num+1}_img{img_index+1}.{image_ext}"
            image_path = os.path.join(output_dir, image_filename)
            
            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)
            
            images_extracted += 1
            print(f"  OK Extracted: {image_filename}")
    
    doc.close()
    return images_extracted

# Process all PDFs
total_images = 0
for pdf_file in pdf_files:
    if os.path.exists(pdf_file):
        count = extract_images_from_pdf(pdf_file)
        total_images += count
    else:
        print(f"X Not found: {pdf_file}")

print(f"\nDONE Total images extracted: {total_images}")
print(f"Output directory: {output_dir}")
