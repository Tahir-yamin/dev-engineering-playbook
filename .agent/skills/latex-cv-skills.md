# LaTeX CV Skills & Templates

## Why LaTeX for CVs?
- **Professional Typography**: Superior formatting and consistency.
- **Version Control**: Text-based source files work great with Git.
- **Separation of Content and Design**: easy to change style without rewriting content.

## ATS Compatibility Note
> **Critical:** While LaTeX produces beautiful PDFs, some older ATS (Applicant Tracking Systems) struggle to parse them correctly compared to standard DOCX files. 
> To ensure maximum ATS compatibility, use **single-column layouts** and standard fonts in your LaTeX templates.

## Basic LaTeX CV Template (ATS-Friendly)

Save this as `cv.tex` and compile with `pdflatex cv.tex`.

```latex
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[margin=0.75in]{geometry}
\usepackage{titlesec}
\usepackage{enumitem}
\usepackage{hyperref}

% Formatting sections
\titleformat{\section}{\Large\bfseries\uppercase}{}{0em}{}[\titlerule]
\titlespacing{\section}{0pt}{10pt}{5pt}

% Formatting bullets
\setlist[itemize]{leftmargin=*}

\begin{document}

% Header
\begin{center}
    {\Huge \textbf{YOUR NAME}} \\ \vspace{5pt}
    City, Country | +1-234-567-890 | email@example.com \\
    \url{linkedin.com/in/yourprofile} | \url{github.com/yourprofile}
\end{center}

% Professional Summary
\section{Professional Summary}
Results-oriented professional with [Number] years of experience in [Industry]. Proven track record in [Key Skill 1] and [Key Skill 2]. Committed to delivering high-quality results in fast-paced environments.

% Experience
\section{Experience}
\textbf{Job Title} \hfill Month Year -- Present \\
\textit{Company Name}, City, Country
\begin{itemize}
    \item Achievement 1: Quantifiable result (e.g., increased efficiency by 20\%).
    \item Achievement 2: Led a team of X people to deliver Y project.
    \item Achievement 3: Solved Z problem using [Skill/Tool].
\end{itemize}

\vspace{5pt}

\textbf{Previous Job Title} \hfill Month Year -- Month Year \\
\textit{Company Name}, City, Country
\begin{itemize}
    \item Achievement 1.
    \item Achievement 2.
\end{itemize}

% Education
\section{Education}
\textbf{Degree Name} \hfill Year \\
\textit{University Name}, City, Country

% Skills
\section{Skills}
\begin{itemize}
    \item \textbf{Technical:} Python, Java, SQL, LaTeX, Git
    \item \textbf{Tools:} Jira, Trello, Excel, VS Code
    \item \textbf{Languages:} English (Native), Spanish (Intermediate)
\end{itemize}

\end{document}
```

## How to Compile
1.  **Online (Recommended):** Use [Overleaf](https://www.overleaf.com/). Paste the code above into a new project.
2.  **Local Installation:**
    -   **Windows:** Install [MiKTeX](https://miktex.org/)
    -   **Mac:** Install [MacTeX](https://www.tug.org/mactex/)
    -   **Linux:** `sudo apt-get install texlive-full`

## Converting to ATS-Friendly Text
If you need a plain text version for an ATS form, use `pandoc`:
`pandoc cv.tex -t plain -o cv.txt`
