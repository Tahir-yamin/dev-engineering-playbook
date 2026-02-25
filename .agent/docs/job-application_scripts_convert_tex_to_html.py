
import os
import re
import sys
import traceback

def tex_to_html(tex_path):
    try:
        with open(tex_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Strip LaTeX comments
        content = re.sub(r'(?<!\\)%.*', '', content)

        # Extract Name
        name_match = re.search(r'\\Huge \\textbf{\\color{awesome-darknight} (.*?)}', content)
        name = name_match.group(1) if name_match else "Name Not Found"
        
        # Detect Document Type
        is_cover_letter = "Dear Hiring Manager" in content or "To: Hiring Team" in content or "Dear " in content
        
        html_content = ""
        title = ""
        salutation = "Hiring Manager,"
        # Name is already extracted above, but good to be safe if regex fails
        if not 'name' in locals(): name = ""

        if is_cover_letter:
            print("Detected Cover Letter...")
            
            # Robust Body Extraction
            # 1. Broad match
            body_tex = "Content not found."
            try:
                # Better regex to match "Dear [Anything]," to "Sincerely,"
                body_match = re.search(r'Dear (.*?,)(.*?)Sincerely,', content, re.DOTALL | re.IGNORECASE)
                if body_match:
                     salutation = body_match.group(1).strip()
                     # In the template we use "Dear Hiring Manager," so let's adjust
                     body_tex = body_match.group(2).strip()
                     # Clean up vspace
                     body_tex = re.sub(r'\\vspace\{.*?\}', '', body_tex)
            except Exception as e:
                print(f"Body extraction error: {e}")

            # Formatting
            try:
                # \textbf{...} -> <b>...</b>
                body_tex = re.sub(r'\\textbf\{(.*?)\}', r'<b>\1</b>', body_tex)
                
                # Lists
                body_tex = body_tex.replace(r'\begin{itemize}', '<ul>')
                body_tex = body_tex.replace(r'\end{itemize}', '</ul>')
                # \item ... \n -> <li>...</li>
                # Use a safer substitution or just line-by-line
                body_tex = re.sub(r'\\item\s+(.*?)$', r'<li>\1</li>', body_tex, flags=re.MULTILINE)
                
                # Paragraphs (Double newline)
                paragraphs = body_tex.split('\n\n')
                # Filter out empty or just tags
                formatted_pars = []
                for p in paragraphs:
                    p = p.strip()
                    if not p: continue
                    if p.startswith('<ul>') or p.startswith('<li>') or p.startswith('</ul>'):
                        formatted_pars.append(p)
                    else:
                        formatted_pars.append(f"<p>{p}</p>")
                
                body_html = "\n".join(formatted_pars)
            except Exception as e:
                print(f"Formatting error: {e}")
                body_html = f"<pre>{body_tex}</pre>"

            # Metadata
            recipient = "Hiring Team"
            subject = "Application"
            try:
               rec_m = re.search(r'\\textbf{To: Hiring Team} \\\\\s*\\textbf{(.*?)}', content)
               if rec_m: recipient = rec_m.group(1)
               
               sub_m = re.search(r'\\textbf{Subject: (.*?)}', content)
               if sub_m: subject = sub_m.group(1)
            except:
                pass

            html_content = f"""
            <div class="letter-body">
                <div class="meta">
                    <p><strong>To: Hiring Team</strong><br><strong>{recipient}</strong></p>
                    <p><strong>Subject: {subject}</strong></p>
                    <p>Dear {salutation}</p>
                </div>
                <div class="content">
                    {body_html}
                </div>
                <div class="signoff">
                    <p>Sincerely,</p>
                    <p><strong>{name}</strong></p>
                </div>
            </div>
            """

        else:
            print("Detected CV...")
            # CV Logic (Simplified/Existing)
            # Title
            title_match = re.search(r'{\\Large \\color{awesome-gray} (.*?)}', content)
            title = title_match.group(1) if title_match else ""
            
            # Contact - simplified extraction
            phone = ""
            email = ""
            linkedin_url = ""
            github_url = ""
            location = ""
            try:
                # Find the small text block after header
                contact_m = re.search(r'\\small \\color\{light-gray\}(.*?)\\end\{center\}', content, re.DOTALL)
                if contact_m:
                    contact_text = contact_m.group(1)
                    # Extract location (before first bullet or line break)
                    loc_m = re.match(r'\s*(.*?)\s*\\quad', contact_text)
                    if loc_m: location = loc_m.group(1).strip()

                    # Extract phone
                    ph_m = re.search(r'([+\d-]{10,})', contact_text)
                    if ph_m: phone = ph_m.group(1).strip()

                    # Extract email
                    em_m = re.search(r'href\{mailto:(.*?)\}', contact_text)
                    if em_m: email = em_m.group(1).strip()

                    # Extract LinkedIn
                    li_m = re.search(r'href\{https://linkedin\.com/in/(.*?)\}', contact_text)
                    if li_m: linkedin_url = f"linkedin.com/in/{li_m.group(1).strip()}"

                    # Extract GitHub
                    gh_m = re.search(r'href\{https://github\.com/(.*?)\}', contact_text)
                    if gh_m: github_url = f"github.com/{gh_m.group(1).strip()}"
            except Exception as e:
                print(f"Contact extraction error: {e}")

            # Summary
            summary = ""
            try:
                sm = re.search(r'\\section{Professional Summary}\s*\\large\s*(.*?)\s*\\normalsize', content, re.DOTALL)
                if sm: summary = sm.group(1).strip()
            except: pass
            
            # Competencies
            competencies = []
            try:
                # Find all lines with \textbullet
                # Fix: Use negative lookbehind (?<!\\)& to avoid matching \&
                bullets = re.findall(r'\\textbullet\\ (.*?)(?:(?<!\\)&|\\\\)', content)
                competencies = [b.strip() for b in bullets if b.strip()]
            except: pass

            # Experience
            experiences = []
            try:
                exp_section = re.search(r'\\section{Professional Experience}(.*?)\\section{Education}', content, re.DOTALL)
                if exp_section:
                    exp_text = exp_section.group(1)
                    # Split by \noindent \textbf{\large
                    items = re.split(r'\\noindent \\textbf{\\large ', exp_text)[1:]
                    for item in items:
                        lines = item.split('\n')
                        role = lines[0].split('}')[0]
                        # Extract Period
                        period = ""
                        pm = re.search(r'\\color{awesome-blue}(.*?)\}', lines[0])
                        if pm: period = pm.group(1)
                        
                        company = ""
                        cm = re.search(r'\\textit{(.*?)}', item)
                        if cm: company = cm.group(1)
                        
                        highlights = re.findall(r'\\item (.*?)$', item, re.MULTILINE)
                        # Clean highlights
                        cleaned_highlights = []
                        for h in highlights:
                            h = re.sub(r'\\textbf\{(.*?)\}', r'<strong>\1</strong>', h)
                            cleaned_highlights.append(h)
                        
                        experiences.append({
                            "role": role, "period": period, "company": company, "highlights": cleaned_highlights
                        })
            except Exception as e:
                print(f"Experience extraction error: {e}")

            # Education
            education = ""
            try:
                edu_section = re.search(r'\\section{Education}\s*(.*?)\s*(?:\\section|\\vfill|\\end{document})', content, re.DOTALL)
                if edu_section:
                    education = edu_section.group(1).strip()
                    # Clean up \noindent, \textbf, \hfill, \\
                    education = re.sub(r'\\noindent\s*', '', education)
                    education = re.sub(r'\\textbf\{(.*?)\}', r'<strong>\1</strong>', education)
                    education = re.sub(r'\\hfill\s*', ' - ', education)
                    education = education.replace('\\\\', '<br>')
            except: pass

            # Certifications
            certifications = ""
            try:
                cert_section = re.search(r'\\section{Certifications}\s*\\begin{itemize}(.*?)\\end{itemize}', content, re.DOTALL)
                if cert_section:
                    items = re.findall(r'\\item (.*?)$', cert_section.group(1), re.MULTILINE)
                    certifications = "<ul>" + "".join(f"<li>{i.strip()}</li>" for i in items) + "</ul>"
                else:
                    # Fallback
                    cert_section = re.search(r'\\section{Certifications}\s*(.*?)\s*(?:\\section|\\vfill|\\end{document})', content, re.DOTALL)
                    if cert_section: certifications = cert_section.group(1).strip()
            except: pass

            # Skills
            skills = ""
            # Skills
            skills = ""
            try:
                # 1. Try finding itemize environment
                list_match = re.search(r'\\section{Technical Skills}\s*\\begin{itemize}(.*?)\\end{itemize}', content, re.DOTALL)
                if list_match:
                    items = re.findall(r'\\item (.*?)$', list_match.group(1), re.MULTILINE)
                    # Clean and Format Items
                    cleaned_items = []
                    for i in items:
                        # Handle \textbf{}
                        i = re.sub(r'\\textbf\{(.*?)\}', r'<strong>\1</strong>', i)
                        # Handle &
                        i = i.replace(r'\&', '&')
                        if i.strip():
                            cleaned_items.append(i)
                    
                    # Convert to HTML UL
                    skills = "<ul>" + "".join(f"<li>{i}</li>" for i in cleaned_items) + "</ul>"
                else:
                    # 2. Fallback to old behavior (paragraph)
                    skm = re.search(r'\\section{Technical Skills}\s*\\noindent (.*?)\s*(?:\\vfill|\\end{document})', content, re.DOTALL)
                    if skm: skills = skm.group(1).strip()
            except: pass

            # Footer Extraction (References)
            footer = ""
            try:
                fm = re.search(r'\\vfill\s*\\begin{center}\s*\\textit{(.*?)}\s*\\end{center}', content, re.DOTALL)
                if fm: footer = f'<div style="text-align: center; margin-top: 40px; font-style: italic; color: #555;">{fm.group(1)}</div>'
            except: pass

            html_content = f"""
            <h3>Professional Summary</h3>
            <div class="summary">{summary}</div>

            <h3>Core Competencies</h3>
            <div class="competencies">
                {''.join(f'<div>&bull; {c}</div>' for c in competencies)}
            </div>

            <h3>Professional Experience</h3>
            {''.join(f'''
            <div class="job">
                <div class="job-header">
                    <span class="role">{exp['role']}</span>
                    <span class="period">{exp['period']}</span>
                </div>
                <div class="company">{exp['company']}</div>
                <ul>
                    {''.join(f'<li>{h}</li>' for h in exp['highlights'])}
                </ul>
            </div>
            ''' for exp in experiences)}

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <h3>Education</h3>
                    <div class="education">{education}</div>
                </div>
                <div>
                    <h3>Certifications</h3>
                    <div class="certifications">{certifications}</div>
                </div>
            </div>

            <h3>Technical Skills</h3>
            <div class="skills">
                {skills}
            </div>
            {footer}
            """

        # Final Cleanup of HTML Content (Unescape LaTeX)
        def clean_latex_escapes(text):
            # First handle latex formatting commands -> HTML
            text = re.sub(r'\\textbf\{([^}]*)\}', r'<strong>\1</strong>', text)
            text = re.sub(r'\\textit\{([^}]*)\}', r'<em>\1</em>', text)
            text = re.sub(r'\\textbullet\s*\\?\s*', '&bull; ', text)
            text = re.sub(r'\\textbullet', '&bull;', text)
            # Then handle escape characters
            replacements = {
                r'\&': '&',
                r'\%': '%',
                r'\$': '$',
                r'\#': '#',
                r'\_': '_',
                r'\{': '{',
                r'\}': '}',
                r'$|$': '|', # Handle common latex separator artifact
                r'\textasciitilde{}': '~',
                r'\textasciicircum{}': '^',
                r'\textbackslash{}': '\\',
                r'---': '—', # Em-dash (must come before en-dash)
                r'--': '–', # En-dash
            }
            for old, new in replacements.items():
                text = text.replace(old, new)
            # Strip any remaining \command{content} -> content
            text = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', text)
            # Remove any naked \command
            text = re.sub(r'\\[a-zA-Z]+', '', text)
            # Final trim of double spaces
            text = re.sub(r'\s+', ' ', text).strip()
            return text

        html_content = clean_latex_escapes(html_content)
        name = clean_latex_escapes(name)
        title = clean_latex_escapes(title)

        # Prepare Header Contact
        header_contact_html = ""
        if not is_cover_letter:
            header_contact_html = f"""
            <div class="header-contact">
                {location} &bull; {phone} &bull; <a href="mailto:{email}">{email}</a><br>
                <a href="https://{linkedin_url}">{linkedin_url}</a> &bull; <a href="https://{github_url}">{github_url}</a>
            </div>
            """

        # Final Template
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{name} - Document</title>
            <style>
                @page {{
                    margin: 0mm;
                    size: A4;
                }}
                body {{ 
                    font-family: 'Helvetica', 'Arial', sans-serif; 
                    color: #333; 
                    line-height: 1.6; 
                    max-width: 900px; 
                    margin: 0 auto; 
                    padding: 40px; 
                    padding-top: 60px;
                    padding-bottom: 60px;
                }}
                h1 {{ color: #131a28; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px; text-align: center; }}
                h2 {{ color: #414141; margin-top: 0; font-weight: normal; text-align: center; font-size: 1.2em; }}
                .header-contact {{ text-align: center; color: #646464; font-size: 0.9em; margin-bottom: 15px; }}
                .header-contact a {{ color: #004eac; text-decoration: none; }}
                h3 {{ color: #004eac; border-bottom: 2px solid #ddd; padding-bottom: 5px; margin-top: 20px; text-transform: uppercase; font-size: 1em; }}
                .summary {{ font-size: 1em; }}
                .competencies {{ display: grid; grid-template-columns: 1fr 1fr; gap: 5px; font-size: 0.9em; }}
                .job {{ margin-bottom: 15px; }}
                .job-header {{ display: flex; justify-content: space-between; align-items: baseline; }}
                .role {{ font-weight: bold; font-size: 1em; color: #000; }}
                .period {{ color: #004eac; font-weight: bold; font-size: 0.9em; }}
                .company {{ font-style: italic; color: #555; margin-bottom: 2px; font-size: 0.9em; }}
                ul {{ margin-top: 2px; padding-left: 20px; }}
                li {{ margin-bottom: 1px; }}
                .skills {{ background: #f9f9f9; padding: 10px; border-radius: 5px; font-size: 0.9em; }}
                .letter-body {{ font-size: 1em; margin-top: 10px; line-height: 1.5; }}
                .meta p {{ margin: 0 0 5px 0; }}
                .signoff {{ margin-top: 25px; }}
                @media print {{
                    @page {{
                        margin: 15mm;
                        size: A4;
                    }}
                    body {{ 
                        padding: 0;
                        margin: 0;
                        font-size: 11pt; 
                        color: #000 !important;
                        -webkit-print-color-adjust: exact; 
                    }}
                    h3 {{ margin-top: 15px; text-transform: uppercase; color: #004eac !important; -webkit-print-color-adjust: exact; }}
                    .period {{ color: #004eac !important; -webkit-print-color-adjust: exact; }}
                    /* Force visibility */
                    * {{ visibility: visible !important; }}
                }}
            </style>
        </head>
        <body>
            <h1>{name}</h1>
            {f'<h2>{title}</h2>' if not is_cover_letter else ''}
            
            {header_contact_html}

            {html_content}
        </body>
        </html>
        """
        
        output_path = tex_path.replace(".tex", ".html")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"HTML Generated: {output_path}")

    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_tex_to_html.py <path_to_tex_file>")
    else:
        tex_to_html(sys.argv[1])
