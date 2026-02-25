#!/usr/bin/env python3
"""
Protect sensitive files from modification.
Blocks edits to production configs, lock files, and sensitive directories.
"""
import json
import sys
import os
import fnmatch

# Files/patterns to protect (exit code 2 = block)
PROTECTED_PATTERNS = [
    # Lock files (usually shouldn't be manually edited)
    'package-lock.json',
    'yarn.lock',
    'pnpm-lock.yaml',
    'Gemfile.lock',
    'poetry.lock',
    'Cargo.lock',
    
    # Sensitive files
    '.env',
    '.env.local',
    '.env.production',
    '**/secrets/*',
    '**/credentials/*',
    
    # Git internals
    '.git/*',
    
    # CI/CD (warn but don't block)
    # '.github/workflows/*',
]

# Files that should warn but not block
WARN_PATTERNS = [
    '.github/workflows/*',
    'docker-compose.yml',
    'Dockerfile',
    '**/production/*',
]

def matches_pattern(file_path, patterns):
    """Check if file matches any protected pattern."""
    file_path = file_path.lstrip('./')
    for pattern in patterns:
        if fnmatch.fnmatch(file_path, pattern):
            return pattern
        if fnmatch.fnmatch(os.path.basename(file_path), pattern):
            return pattern
    return None

def main():
    try:
        input_data = json.load(sys.stdin)
        file_path = input_data.get('tool_input', {}).get('file_path', '')
        
        if not file_path:
            sys.exit(0)
        
        # Check for blocked patterns
        blocked = matches_pattern(file_path, PROTECTED_PATTERNS)
        if blocked:
            print(f"🚫 BLOCKED: {file_path}")
            print(f"   Matches protected pattern: {blocked}")
            print("   Use --force if this is intentional")
            sys.exit(2)  # Block the operation
        
        # Check for warning patterns
        warned = matches_pattern(file_path, WARN_PATTERNS)
        if warned:
            print(f"⚠️ WARNING: Editing sensitive file: {file_path}")
            print(f"   Matches pattern: {warned}")
            # Don't block, just warn
            sys.exit(0)
            
    except Exception:
        sys.exit(0)

if __name__ == '__main__':
    main()
