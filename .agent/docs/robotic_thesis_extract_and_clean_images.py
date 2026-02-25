import fitz  # PyMuPDF
import os
import cv2
import numpy as np

def clean_watermark(img_path, output_path):
    """
    Remove NotebookLM watermark using targeted approach (Bottom 20%, Top 15%)
    """
    img = cv2.imread(str(img_path))
    if img is None:
        return False
    
    h, w = img.shape[:2]
    result = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Create aggressive mask for watermark zones
    mask = np.zeros_like(gray)
    
    # Bottom 20% & Top 15% & Side 10%
    mask[-int(h * 0.20):, :] = 255
    mask[:int(h * 0.15), :] = 255
    mask[:, :int(w * 0.10)] = 255
    mask[:, -int(w * 0.10):] = 255
    
    # Detect very light text
    _, light_text = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    watermark_mask = cv2.bitwise_and(light_text, mask)
    
    # Edges/Text patterns
    edges = cv2.Canny(gray, 30, 100)
    kernel = np.ones((3,3), np.uint8)
    text_patterns = cv2.dilate(edges, kernel, iterations=2)
    text_patterns = cv2.bitwise_and(text_patterns, mask)
    
    final_mask = cv2.bitwise_or(watermark_mask, text_patterns)
    
    # Cleanup mask
    k7 = np.ones((7,7), np.uint8)
    final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_CLOSE, k7)
    final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_OPEN, k7)
    
    if np.sum(final_mask) > 0:
        result = cv2.inpaint(result, final_mask, 10, cv2.INPAINT_TELEA)
        result = cv2.inpaint(result, final_mask, 7, cv2.INPAINT_NS) # Second pass
        
    cv2.imwrite(str(output_path), result)
    return True

def extract_images(pdf_dir, output_dir, min_size_kb=20):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]
    total_extracted = 0

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_dir, pdf_file)
        print(f"Extracting from {pdf_file}...")
        
        try:
            doc = fitz.open(pdf_path)
            for i in range(len(doc)):
                for img_index, img in enumerate(doc[i].get_images(full=True)):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    
                    if len(image_bytes) < 1024 * min_size_kb:
                        continue
                        
                    # Save temp raw image
                    raw_name = f"{os.path.splitext(pdf_file)[0]}_p{i}_img{img_index}.png"
                    raw_path = os.path.join(output_dir, "raw_" + raw_name)
                    with open(raw_path, "wb") as f:
                        f.write(image_bytes)
                    
                    # Clean it
                    clean_name = f"{os.path.splitext(pdf_file)[0]}_p{i}_img{img_index}.png"
                    clean_path = os.path.join(output_dir, clean_name)
                    
                    if clean_watermark(raw_path, clean_path):
                        print(f"  Saved clean image: {clean_name}")
                        total_extracted += 1
                    
                    # Cleanup raw
                    if os.path.exists(raw_path):
                        os.remove(raw_path)
                        
        except Exception as e:
            print(f"Error processing {pdf_file}: {e}")

    print(f"Done. Extracted {total_extracted} images to {output_dir}")

if __name__ == "__main__":
    base_dir = r"D:\my-dev-knowledge-base\research\robotic_thesis"
    img_dir = os.path.join(base_dir, "images")
    extract_images(base_dir, img_dir)
