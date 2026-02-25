#!/usr/bin/env python3
"""
Auto-format files after Claude edits them.
Detects file type and runs appropriate formatter.
"""
import json
import subprocess
import sys
import os

def get_formatter_command(file_path):
    """Return the formatter command for a given file type."""
    ext = os.path.splitext(file_path)[1].lower()
    
    formatters = {
        # JavaScript/TypeScript
        '.js': ['npx', 'prettier', '--write'],
        '.jsx': ['npx', 'prettier', '--write'],
        '.ts': ['npx', 'prettier', '--write'],
        '.tsx': ['npx', 'prettier', '--write'],
        '.json': ['npx', 'prettier', '--write'],
        '.css': ['npx', 'prettier', '--write'],
        '.scss': ['npx', 'prettier', '--write'],
        '.md': ['npx', 'prettier', '--write'],
        '.yaml': ['npx', 'prettier', '--write'],
        '.yml': ['npx', 'prettier', '--write'],
        
        # Python
        '.py': ['black', '--quiet'],
        
        # Go
        '.go': ['gofmt', '-w'],
        
        # Rust
        '.rs': ['rustfmt'],
    }
    
    return formatters.get(ext)

def main():
    try:
        input_data = json.load(sys.stdin)
        file_path = input_data.get('tool_input', {}).get('file_path', '')
        
        if not file_path or not os.path.exists(file_path):
            sys.exit(0)
        
        formatter = get_formatter_command(file_path)
        if formatter:
            cmd = formatter + [file_path]
            try:
                subprocess.run(cmd, capture_output=True, timeout=10)
            except (subprocess.TimeoutExpired, FileNotFoundError):
                # Formatter not installed or timed out - skip silently
                pass
    except Exception:
        # Don't block on formatter errors
        pass

if __name__ == '__main__':
    main()
