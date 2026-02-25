"""
Markdown to HTML Converter for Robotic Thesis White Paper
Generates a print-ready HTML file from the existing Markdown source.
"""
import re
import os

MD_FILE = r"C:\Users\USER\.gemini\antigravity\brain\419b8a00-bf17-494d-b9bc-255902dfb865\Robotic_Thesis_White_Paper.md"
HTML_FILE = r"C:\Users\USER\.gemini\antigravity\brain\419b8a00-bf17-494d-b9bc-255902dfb865\Robotic_Thesis_White_Paper.html"

CSS = """
<style>
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; color: #333; }
    h1 { color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 10px; }
    h2 { color: #34495e; margin-top: 30px; }
    h3 { color: #7f8c8d; }
    img { max-width: 100%; height: auto; border: 1px solid #ddd; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); margin: 20px 0; }
    figure { margin: 0; text-align: center; }
    figcaption { font-style: italic; color: #666; margin-top: 5px; font-size: 0.9em; }
    code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; font-family: Consolas, monospace; }
    table { width: 100%; border-collapse: collapse; margin: 20px 0; }
    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    th { background-color: #f2f2f2; }
    blockquote { border-left: 4px solid #eee; padding-left: 15px; color: #555; }
    @media print {
        body { max-width: 100%; padding: 0; }
        a { text-decoration: none; color: #000; }
    }
</style>
"""

def convert():
    if not os.path.exists(MD_FILE):
        print(f"File not found: {MD_FILE}")
        return

    with open(MD_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Basic Conversions
    html = content
    
    # Titles
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # Bold / Italic
    html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', html)
    html = re.sub(r'\*(.*?)\*', r'<i>\1</i>', html)
    
    # Images with Captions
    # ![Alt](Path) -> <figure><img src="Path" alt="Alt"><figcaption>Alt</figcaption></figure>
    # Note: Using relative paths for portability if possible, or keeping absolute if needed locally.
    # The current MD has absolute paths: C:/.../images/...
    # Browsers might block local file access strictness, but let's try.
    # To make it safer, we'll convert absolute C:/.../images/X to ./images/X relative to the HTML file.
    
    def repl_image(match):
        alt = match.group(1)
        path = match.group(2)
        # Convert to relative path if it points to the artifact images folder
        if "images/" in path:
            filename = path.split("images/")[-1]
            path = f"images/{filename}"
        return f'<figure><img src="{path}" alt="{alt}"><figcaption>{alt}</figcaption></figure>'

    html = re.sub(r'!\[(.*?)\]\((.*?)\)', repl_image, html)
    
    # Lists (Simple unordered)
    # This is a bit hacky with regex, but works for simple lists in the white paper
    lines = html.split('\n')
    in_list = False
    new_lines = []
    for line in lines:
        if line.strip().startswith('- ') or line.strip().startswith('* '):
            if not in_list:
                new_lines.append('<ul>')
                in_list = True
            new_lines.append(f'<li>{line.strip()[2:]}</li>')
        else:
            if in_list:
                new_lines.append('</ul>')
                in_list = False
            new_lines.append(line)
    if in_list: new_lines.append('</ul>')
    
    html = '\n'.join(new_lines)
    
    # Paragraphs (simple double newline)
    html = re.sub(r'\n\n', '</p><p>', html)
    
    # Wrap
    final_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Robotic Thesis White Paper</title>
        {CSS}
    </head>
    <body>
        {html}
    </body>
    </html>
    """
    
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(final_html)
        
    print(f"Generated HTML: {HTML_FILE}")

if __name__ == "__main__":
    convert()
