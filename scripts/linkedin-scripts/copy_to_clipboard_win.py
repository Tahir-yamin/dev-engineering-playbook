#!/usr/bin/env python3
"""
Windows Clipboard Utility for LinkedIn Articles publishing.

Supports:
- Image files (jpg, png, gif, webp) - copies as image data (DIB)
- HTML content - copies as rich text for paste (CF_HTML)
- Optional image compression before copying

Requirements:
    pip install Pillow pywin32
"""

import argparse
import io
import os
import sys
from pathlib import Path

# Windows clipboard header template for CF_HTML
HTML_CLIPBOARD_HEADER = """Version:0.9
StartHTML:{start_html:08d}
EndHTML:{end_html:08d}
StartFragment:{start_fragment:08d}
EndFragment:{end_fragment:08d}
<html>
<body>
<!--StartFragment-->{html}<!--EndFragment-->
</body>
</html>"""

def compress_image(image_path: str, quality: int = 85, max_size: tuple = (2000, 2000)) -> io.BytesIO:
    """Compress image and return as BytesIO."""
    from PIL import Image
    img = Image.open(image_path)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=quality, optimize=True)
    buffer.seek(0)
    return buffer

def copy_image_to_clipboard_win(image_path: str, quality: int = None) -> bool:
    """Copy image to Windows clipboard as DIB."""
    try:
        import win32clipboard
        from PIL import Image

        if quality:
            img_io = compress_image(image_path, quality)
            image = Image.open(img_io)
        else:
            image = Image.open(image_path)

        # Convert to BMP (DIB format)
        output = io.BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]  # Skip the BMP file header
        output.close()

        win32clipboard.OpenClipboard()
        try:
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        finally:
            win32clipboard.CloseClipboard()
        return True
    except Exception as e:
        print(f"Error copying image: {e}", file=sys.stderr)
        return False

def copy_html_to_clipboard_win(html_content: str) -> bool:
    """Copy HTML to Windows clipboard as CF_HTML."""
    try:
        import win32clipboard
        
        # Format HTML with Windows clipboard header
        fragment = html_content
        html = f"<html><body><!--StartFragment-->{fragment}<!--EndFragment--></body></html>"
        
        # Constants for header calculation
        MARKER_HTML_START = 'StartHTML:'
        MARKER_HTML_END = 'EndHTML:'
        MARKER_FRAG_START = 'StartFragment:'
        MARKER_FRAG_END = 'EndFragment:'
        
        # Initial dummy header to get lengths
        dummy_header = HTML_CLIPBOARD_HEADER.format(
            start_html=0, end_html=0, start_fragment=0, end_fragment=0, html=fragment
        )
        
        header_len = len(HTML_CLIPBOARD_HEADER.format(
            start_html=0, end_html=0, start_fragment=0, end_fragment=0, html=""
        ))
        
        # Precise calculation
        start_html = header_len - len("<html><body><!--StartFragment--><!--EndFragment--></body></html>") + len("<html>")
        end_html = start_html + len("<body><!--StartFragment-->") + len(fragment) + len("<!--EndFragment--></body>")
        start_fragment = start_html + len("<body><!--StartFragment-->")
        end_fragment = start_fragment + len(fragment)
        
        # Re-format with correct offsets
        full_payload = HTML_CLIPBOARD_HEADER.format(
            start_html=start_html, 
            end_html=end_html, 
            start_fragment=start_fragment, 
            end_fragment=end_fragment, 
            html=fragment
        )

        win32clipboard.OpenClipboard()
        try:
            win32clipboard.EmptyClipboard()
            cf_html = win32clipboard.RegisterClipboardFormat("HTML Format")
            win32clipboard.SetClipboardData(cf_html, full_payload.encode("utf-8"))
            # Also set plain text version
            win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, fragment)
        finally:
            win32clipboard.CloseClipboard()
        return True
    except Exception as e:
        print(f"Error copying HTML: {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description='Copy to Windows clipboard for LinkedIn Articles')
    subparsers = parser.add_subparsers(dest='type', required=True)

    # Image subcommand
    img_parser = subparsers.add_parser('image', help='Copy image to clipboard')
    img_parser.add_argument('path', help='Path to image file')
    img_parser.add_argument('--quality', type=int, default=None, help='JPEG quality (1-100)')

    # HTML subcommand
    html_parser = subparsers.add_parser('html', help='Copy HTML to clipboard')
    html_parser.add_argument('content', nargs='?', help='HTML content')
    html_parser.add_argument('--file', '-f', help='Read HTML from file')

    args = parser.parse_args()

    if args.type == 'image':
        if not os.path.exists(args.path):
            print(f"Error: Image not found: {args.path}", file=sys.stderr)
            sys.exit(1)
        success = copy_image_to_clipboard_win(args.path, args.quality)
        if success:
            print(f"Image copied to clipboard: {args.path}")
        sys.exit(0 if success else 1)

    elif args.type == 'html':
        if args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                html = f.read()
        else:
            html = args.content or sys.stdin.read()
        success = copy_html_to_clipboard_win(html)
        if success:
            print(f"HTML copied to clipboard")
        sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
