# LinkedIn Article Publisher

**Topics**: LinkedIn Article Publishing, Browser Automation, Content Distribution, Rich Text Conversion
**Version**: 1.0 (Windows Adapted)

---

## Skill #1: LinkedIn Article Publisher

### When to Use
- You want to publish a Markdown article to LinkedIn Articles editor while preserving all formatting (headers, bold, links, lists).
- You have an article with multiple images and want precise positioning using "Block-Index" logic.
- You want a safe, automated approach that saves as a **DRAFT** without auto-publishing.

### Prerequisites (Windows)
- **Playwright MCP**: For browser automation.
- **Python 3.9+**: With dependencies.
  ```bash
  pip install Pillow pywin32
  ```
- **Login**: You must be logged into LinkedIn in your default browser or provide the session via MCP.

### Scripts (Local Archive)
The following scripts are located in `scripts/linkedin-scripts/`:
- `parse_markdown.py`: Extracts title, cover image, and content images with block indices.
- `copy_to_clipboard_win.py`: Windows-specific clipboard operations for HTML and images.

---

### Prompt Template

```markdown
**ROLE**: Senior Content Manager & Browser Automation Expert

**CONTEXT**: I have a Markdown article at [PATH_TO_FILE] that I need to publish to LinkedIn Articles.

**REQUIREMENTS**:
1. Use `scripts/linkedin-scripts/parse_markdown.py` to extract article data (JSON).
2. Navigate to `https://www.linkedin.com/article/new/` using Playwright MCP.
3. Upload the first image as the **Cover Image** using `browser_file_upload`.
4. Fill the **Title** field from the parsed data.
5. Copy the HTML content to the clipboard using `scripts/linkedin-scripts/copy_to_clipboard_win.py html`.
6. Paste the content into the editor area (`Meta+v`).
7. Insert all remaining images in **REVERSE ORDER** of their `block_index`.
   - For each image: Copy to clipboard (`copy_to_clipboard_win.py image`), click the block element at the specified index, and paste.
8. Verify everything looks correct and confirm: "Draft saved. Review and publish manually."

**SAFETY**: NEVER click the final "Publish" button. Only save as a draft.
```

### Lessons Learned:
- ✅ **Reverse Insertion**: Always insert images from highest index to lowest to prevent position shifts.
- ✅ **Rich Text Paste**: Pasting HTML via the clipboard is 10x more reliable than typing or using `innerHTML` injection in the LinkedIn editor.
- ✅ **Block-Index**: Using child element indices under the textbox is deterministic, unlike text matching which fails on duplicate content.
- ❌ **Direct Typing**: Avoid using `browser_type` for the entire article body as it often breaks formatting and is extremely slow.

---

## Quick Reference (Windows Support)

| File Type | Utility Command |
|-----------|----------------|
| **Markdown** | `python scripts/linkedin-scripts/parse_markdown.py article.md` |
| **HTML** | `python scripts/linkedin-scripts/copy_to_clipboard_win.py html --file content.html` |
| **Image** | `python scripts/linkedin-scripts/copy_to_clipboard_win.py image path/to/img.png --quality 85` |

---

**Related Skills**:
- `frontend-design` (Layout & Styles)
- `webapp-testing` (Browser Automation Patterns)
- `windows-desktop-automation-skills.md` (PowerShell & CLI)
