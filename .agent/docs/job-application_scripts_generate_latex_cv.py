import json
import os
import re
import argparse
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE_PATH = os.path.join(BASE_DIR, "data", "master_profile.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "generated")

def escape_latex(text):
    """Escape special LaTeX characters."""
    if not isinstance(text, str):
        return str(text)
    chars = {
        "|": " - ", # Safer than math mode pipe
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "\\": r"\textbackslash{}",
    }
    return "".join(chars.get(c, c) for c in text)

def load_profile():
    with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_keywords(job_description, profile):
    """Simple keyword extraction matching profile keywords in JD."""
    jd_lower = job_description.lower()
    found = set()
    
    # Check profile keywords
    for kw in profile.get("keywords", []):
        if kw.lower() in jd_lower:
            found.add(kw)
            
    # Check technical skills
    for skill in profile.get("technical_skills", []):
         if skill.lower() in jd_lower:
            found.add(skill)

    return list(found)

def generate_latex(job_description_path=None, company=None):
    profile = load_profile()
    
    jd_keywords = []
    if job_description_path and os.path.exists(job_description_path):
        with open(job_description_path, 'r', encoding='utf-8') as f:
            jd_text = f.read()
            jd_keywords = extract_keywords(jd_text, profile)

    p = profile["personal"]
    
    # Combine skills
    all_skills = set(profile["technical_skills"])
    for kw in jd_keywords:
        all_skills.add(kw)
    
    sorted_skills = sorted(list(all_skills), key=str.lower)
    skills_str = ", ".join([escape_latex(s) for s in sorted_skills])

    # === MODERN TEMPLATE (Awesome CV Style) ===
    latex_template = r"""
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[margin=0.6in, top=0.6in, bottom=0.6in]{geometry} % Narrower margins
\usepackage{titlesec}
\usepackage{enumitem}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{helvet} % Helvetica font (modern sans-serif)
\renewcommand{\familydefault}{\sfdefault}

% Professional Colors (Awesome CV -ish)
\definecolor{awesome-darknight}{RGB}{19, 26, 40}
\definecolor{awesome-blue}{RGB}{0, 78, 172} % Wood-like blue
\definecolor{awesome-gray}{RGB}{65, 65, 65}
\definecolor{light-gray}{RGB}{100, 100, 100}

\hypersetup{
    colorlinks=true,
    linkcolor=awesome-blue,
    filecolor=awesome-blue,      
    urlcolor=awesome-blue,
}

% Section Styling
\titleformat{\section}
  {\Large\bfseries\color{awesome-blue}\uppercase} % Format
  {} % Label
  {0em} % Sep
  {} % Before
  [\titlerule] % After (Underline)

\titlespacing{\section}{0pt}{14pt}{8pt}

% List Styling
\setlist[itemize]{leftmargin=*, label={\color{awesome-blue}\small\textbullet}, itemsep=2pt, parsep=0pt}

\begin{document}

% === HEADER ===
\begin{center}
    {\Huge \textbf{\color{awesome-darknight} """ + escape_latex(p["name"]) + r"""}} \\[0.2cm]
    {\Large \color{awesome-gray} """ + escape_latex(p["title"]) + r"""} \\[0.3cm]
    
    \small \color{light-gray}
    """ + escape_latex(p["location"]) + r""" \quad \textbullet \quad 
    """ + escape_latex(p["phone"]) + r""" \quad \textbullet \quad 
    \href{mailto:""" + escape_latex(p["email_primary"]) + r"""}{""" + escape_latex(p["email_primary"]) + r"""} \\
    \href{https://""" + escape_latex(p["linkedin"]) + r"""}{""" + escape_latex(p["linkedin"]) + r"""} \quad \textbullet \quad 
    \href{https://""" + escape_latex(p.get("github", "github.com/Tahir-yamin")) + r"""}{""" + escape_latex(p.get("github", "github.com/Tahir-yamin")) + r"""}
\end{center}

\vspace{0.4cm}

% === SUMMARY ===
\section{Professional Summary}
\large
""" + escape_latex(profile["professional_summary"]) + r"""
\normalsize

% === COMPETENCIES ===
\section{Core Competencies}
\begin{center}
\begin{tabular}{p{0.45\textwidth} p{0.45\textwidth}}
""" 
    # Create 2-column table for competencies
    comps = profile["core_competencies"]
    mid = (len(comps) + 1) // 2
    
    for i in range(mid):
        left = escape_latex(comps[i])
        right = escape_latex(comps[mid + i]) if (mid + i) < len(comps) else ""
        latex_template += r"\textbullet\ " + left + r" & \textbullet\ " + right + r" \\" + "\n"
        
    latex_template += r"""
\end{tabular}
\end{center}

% === EXPERIENCE ===
\section{Professional Experience}
"""

    for exp in profile["experience"]:
        latex_template += r"\noindent \textbf{\large " + escape_latex(exp["title"]) + r"}" 
        latex_template += r" \hfill \textbf{\color{awesome-blue}" + escape_latex(exp["period"]) + r"}" + r"\\" + "\n"
        latex_template += r"\textit{" + escape_latex(exp["company"]) + r"} | " + escape_latex(exp["industry"]) 
        if "project_value" in exp:
             latex_template += r" | " + escape_latex(exp["project_value"])
        latex_template += r"\\" + "\n"
        
        latex_template += r"\begin{itemize}" + "\n"
        for highlight in exp["highlights"]:
             latex_template += r"    \item " + escape_latex(highlight) + "\n"
        latex_template += r"\end{itemize}" + "\n\n"

    latex_template += r"""
% === EDUCATION ===
\section{Education}
"""
    for edu in profile["education"]:
         latex_template += r"\noindent \textbf{" + escape_latex(edu["degree"]) + r"}"
         latex_template += r" \hfill " + escape_latex(edu["institution"]) + r"\\" + "\n"

    latex_template += r"""
% === CERTIFICATIONS ===
\section{Certifications}
\begin{itemize}[noitemsep]
"""
    for cert in profile["certifications"]:
        latex_template += r"    \item " + escape_latex(cert) + "\n"
    latex_template += r"""\end{itemize}

% === SKILLS ===
\section{Technical Skills}
\noindent """ + skills_str + r"""

\end{document}
"""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"CV_TahirYamin_{company if company else 'Generic'}_{timestamp}.tex"
    output_path = os.path.join(OUTPUT_DIR, filename)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(latex_template)
    
    print(f"Generated LaTeX: {output_path}")
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-file", help="Path to JD file")
    parser.add_argument("--company", help="Company Name")
    args = parser.parse_args()
    
    generate_latex(args.job_file, args.company)
