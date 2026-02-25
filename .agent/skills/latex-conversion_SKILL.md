# LaTeX Conversion Skill

Advanced LaTeX expertise for generating professional academic, technical, and creative documents.

## Core Instructions

1.  **Structure**: Always use standard LaTeX document classes (`article`, `report`, `book`, `beamer`).
2.  **Packages**: Use modern, stable packages:
    *   `amsmath`, `amssymb`, `amsfonts` for mathematics.
    *   `graphicx` for images.
    *   `hyperref` for links and metadata.
    *   `booktabs` for professional tables.
    *   `geometry` for margin control.
    *   `biblatex` with `biber` for citations.
3.  **UTF-8**: Always include `\usepackage[utf8]{inputenc}` and `\usepackage[T1]{fontenc}` for maximum compatibility.

## Templates

### [Premium Article]
```latex
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{geometry}
\usepackage{hyperref}

\geometry{margin=1in}
\hypersetup{colorlinks=true, linkcolor=blue, citecolor=blue, urlcolor=cyan}

\title{Document Title}
\author{Author Name}
\date{\today}

\begin{document}
\maketitle

\begin{abstract}
Your abstract here.
\end{abstract}

\section{Introduction}
Start writing here...

\end{document}
```

## Best Practices
*   Keep files modular using `\input{}` or `\include{}` for long documents.
*   Enclose math in `$...$` for inline and `\[ ... \]` for display.
*   Use `figure` and `table` environments with descriptive captions and labels.
