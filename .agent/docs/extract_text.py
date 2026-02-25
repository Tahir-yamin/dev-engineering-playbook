from pypdf import PdfReader
import os

pdf_path = r"D:\my-dev-knowledge-base\SAP PR.pdf"
output_path = r"D:\my-dev-knowledge-base\sap_pr_content.txt"

try:
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n\n--- PAGE BREAK ---\n\n"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Successfully extracted text to {output_path}")
    print(f"Total pages: {len(reader.pages)}")
    print(f"Character count: {len(text)}")
except Exception as e:
    print(f"Error: {e}")
