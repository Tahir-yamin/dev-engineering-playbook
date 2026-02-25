import os
import fitz  # PyMuPDF
import sys

def extract_text_from_pdfs(directory):
    output_file = os.path.join(directory, "all_pdf_text.txt")
    
    with open(output_file, "w", encoding="utf-8") as out:
        for filename in os.listdir(directory):
            if filename.lower().endswith(".pdf"):
                pdf_path = os.path.join(directory, filename)
                print(f"Processing {filename}...")
                out.write(f"\n\n--- START OF FILE: {filename} ---\n\n")
                
                try:
                    doc = fitz.open(pdf_path)
                    for page in doc:
                        text = page.get_text()
                        out.write(text)
                    out.write(f"\n\n--- END OF FILE: {filename} ---\n\n")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
                    out.write(f"\nError processing {filename}: {e}\n")
    
    print(f"Text extracted to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = r"D:\my-dev-knowledge-base\research\robotic_thesis"
        
    extract_text_from_pdfs(directory)
