import json
import os
import argparse
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE_PATH = os.path.join(BASE_DIR, "data", "master_profile.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "generated")

def escape_latex(text):
    if not isinstance(text, str):
        return str(text)
    chars = {
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

def generate_latex_cl(company, job_title, job_ref=None, location="Saudi Arabia"):
    profile = load_profile()
    p = profile["personal"]
    
    # === HEADER (Same as CV) ===
    latex_template = r"""
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[margin=1in]{geometry} 
\usepackage{titlesec}
\usepackage{enumitem}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{helvet}
\renewcommand{\familydefault}{\sfdefault}
\usepackage{parskip} % For proper paragraph spacing

% Colors
\definecolor{awesome-darknight}{RGB}{19, 26, 40}
\definecolor{awesome-blue}{RGB}{0, 78, 172} 
\definecolor{awesome-gray}{RGB}{65, 65, 65}
\definecolor{light-gray}{RGB}{100, 100, 100}

\hypersetup{colorlinks=true, linkcolor=awesome-blue, urlcolor=awesome-blue}

\begin{document}

% === HEADER ===
\begin{center}
    {\Huge \textbf{\color{awesome-darknight} """ + escape_latex(p["name"]) + r"""}} \\[0.2cm]
    {\Large \color{awesome-gray} """ + escape_latex(p["title"]) + r"""} \\[0.3cm]
    
    \small \color{light-gray}
    """ + escape_latex(p["location"]) + r""" \quad \textbullet \quad 
    """ + escape_latex(p["phone"]) + r""" \quad \textbullet \quad 
    """ + escape_latex(p["email_primary"]) + r"""
\end{center}

\vspace{0.8cm}
\today
\vspace{0.5cm}

\textbf{To: Hiring Team} \\
\textbf{""" + escape_latex(company) + r"""} \\
\vspace{0.5cm}

\textbf{Subject: Application for """ + escape_latex(job_title) + (r" (Ref: " + escape_latex(job_ref) + r")" if job_ref else "") + r"""}

\vspace{0.5cm}

Dear Hiring Manager,

With over 15 years of experience in Project Controls and Planning for major EPC and Oil \& Gas projects (up to USD 750M+), I am writing to express my strong interest in the """ + escape_latex(job_title) + r""" role at """ + escape_latex(company) + r""". My background in managing complex brownfield and greenfield portfolios, combined with my expertise in Primavera P6, Schedule Risk Analysis, and FIDIC-based claims management, aligns directly with the requirements of your projects team in """ + escape_latex(location) + r""".

Throughout my career, I have consistently delivered results by optimizing schedules and leading diverse planning teams. At my previous roles, I successfully:

\begin{itemize}
    \item \textbf{Led Integrated Planning:} Managed Level 4 schedules for multi-billion dollar portfolios, ensuring alignment between engineering, procurement, and construction phases.
    \item \textbf{Risk Mitigation:} Implemented quantitative schedule risk analysis (QSRA) to identify critical path threats early, reducing potential delays by up to 20\%.
    \item \textbf{Team Leadership:} Mentored junior planners and established standardized WBS/CBS structures across project lifecycles.
\end{itemize}

I am particularly drawn to """ + escape_latex(company) + r"""'s reputation for excellence in the region. I am confident that my technical proficiency in P6 and Power BI, coupled with my strategic approach to project controls, will allow me to make an immediate impact on your ongoing projects.

I would welcome the opportunity to discuss how my experience aligns with your specific needs. I am available for an immediate interview and am fully open to relocation to """ + escape_latex(location) + r""".

Thank you for your time and consideration.

\vspace{0.5cm}
Sincerely,

\vspace{0.5cm}
\textbf{""" + escape_latex(p["name"]) + r"""}

\end{document}
"""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"CL_TahirYamin_{company}_{timestamp}.tex"
    output_path = os.path.join(OUTPUT_DIR, filename)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(latex_template)
    
    print(f"Generated LaTeX CL: {output_path}")
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--company", help="Company Name")
    parser.add_argument("--title", help="Job Title")
    parser.add_argument("--ref", help="Job Ref", default=None)
    parser.add_argument("--location", help="Job Location", default="Saudi Arabia")
    
    args = parser.parse_args()
    
    if args.company and args.title:
        generate_latex_cl(args.company, args.title, args.ref, args.location)
    else:
        # Default fallback for testing
        generate_latex_cl("Wood", "Principal Planner", "26819")
