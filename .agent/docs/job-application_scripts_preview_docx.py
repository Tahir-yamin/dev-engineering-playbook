import sys
from docx import Document

def docx_to_markdown(docx_path):
    try:
        doc = Document(docx_path)
        print(f"# Preview: {docx_path}\n")
        
        for para in doc.paragraphs:
            text = para.text.strip()
            if not text:
                continue
                
            # Simple heuristic for headers (bold + short?)
            # or just bullet points
            
            prefix = ""
            if para.style.name.startswith('List'):
                prefix = "- "
            elif para.style.name.startswith('Heading'):
                level = para.style.name[-1] if para.style.name[-1].isdigit() else '1'
                prefix = "#" * int(level) + " "
            
            # Simple bold/italic handling is hard without iterating runs, 
            # just dumping text for now with basic structure
            print(f"{prefix}{text}\n")
            
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        docx_to_markdown(sys.argv[1])
