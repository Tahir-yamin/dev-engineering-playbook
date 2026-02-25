import sys
import PyPDF2
import os

def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"Error: File not found at {pdf_path}")
        return

    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        
        # Output text to stdout
        print("--- START OF PDF CONTENT ---")
        print(text)
        print("--- END OF PDF CONTENT ---")
        
    except Exception as e:
        print(f"Error reading PDF: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        extract_text_from_pdf(sys.argv[1])
    else:
        print("Usage: python extract_pdf_text.py <path_to_pdf>")
