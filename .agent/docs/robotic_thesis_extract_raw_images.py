import fitz  # PyMuPDF
import os

def extract_raw_images(pdf_dir, output_dir, min_size_kb=10):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]
    total_extracted = 0

    print(f"Extracting RAW images (no cleaning) to: {output_dir}")

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_dir, pdf_file)
        print(f"Processing {pdf_file}...")
        
        try:
            doc = fitz.open(pdf_path)
            for i in range(len(doc)):
                # Get all images on the page
                image_list = doc[i].get_images(full=True)
                
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    try:
                        base_image = doc.extract_image(xref)
                        image_bytes = base_image["image"]
                        ext = base_image["ext"]
                        
                        # Filter tiny icons
                        if len(image_bytes) < 1024 * min_size_kb:
                            continue
                            
                        filename = f"{os.path.splitext(pdf_file)[0]}_p{i+1}_img{img_index}.{ext}"
                        filepath = os.path.join(output_dir, filename)
                        
                        with open(filepath, "wb") as f:
                            f.write(image_bytes)
                            
                        print(f"  Saved: {filename}")
                        total_extracted += 1
                    except Exception as e:
                        print(f"  Error extracting image {img_index} on page {i}: {e}")
                        
        except Exception as e:
            print(f"Error opening {pdf_file}: {e}")

    print(f"\nDone. Extracted {total_extracted} raw images.")

if __name__ == "__main__":
    base_dir = r"D:\my-dev-knowledge-base\research\robotic_thesis"
    # Create a separate folder for raw images to compare
    img_dir = os.path.join(base_dir, "images_raw")
    extract_raw_images(base_dir, img_dir)
