from pypdf import PdfReader
import os

files_to_extract = [
    {
        "input": r"d:\my-dev-knowledge-base\research\robotic_thesis\Embodied_Generalist_Robotics.pdf",
        "output": r"d:\my-dev-knowledge-base\research\robotic_thesis\thesis_content.txt"
    },
    {
        "input": r"d:\my-dev-knowledge-base\job-application\generated\CV_TahirYamin_Saudi_Aramco_APM_Final.pdf",
        "output": r"d:\my-dev-knowledge-base\job-application\generated\cv_industrial_content.txt"
    }
]

for item in files_to_extract:
    try:
        if not os.path.exists(item["input"]):
            print(f"Skipping: {item['input']} not found")
            continue
            
        reader = PdfReader(item["input"])
        text = ""
        for i, page in enumerate(reader.pages):
            text += f"--- PAGE {i+1} ---\n"
            text += page.extract_text() + "\n\n"
        
        with open(item["output"], "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Successfully extracted: {item['input']} -> {item['output']}")
    except Exception as e:
        print(f"Error extracting {item['input']}: {e}")
