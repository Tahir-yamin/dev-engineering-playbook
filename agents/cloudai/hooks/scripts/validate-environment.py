#!/usr/bin/env python3
"""
SessionStart hook - Validates environment on session startup.
Checks for required tools, configuration, and potential issues.
"""
import json
import os
import shutil
import sys


def check_environment():
    """Check for required tools and configuration."""
    warnings = []
    info = []

    # Check for Node.js
    if shutil.which("node"):
        info.append("Node.js available")
    else:
        warnings.append("Node.js not found - npm commands may fail")

    # Check for Python
    if shutil.which("python3"):
        info.append("Python 3 available")
    else:
        warnings.append("Python 3 not found - some hooks may fail")

    # Check for Git
    if shutil.which("git"):
        info.append("Git available")
    else:
        warnings.append("Git not found - version control commands unavailable")

    # Check for .env file (warning if missing in project root)
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    env_file = os.path.join(project_dir, ".env")

    if not os.path.exists(env_file):
        warnings.append("No .env file found - environment variables may be needed")

    # Check for package.json (Node project)
    package_json = os.path.join(project_dir, "package.json")
    if os.path.exists(package_json):
        node_modules = os.path.join(project_dir, "node_modules")
        if not os.path.exists(node_modules):
            warnings.append("node_modules not found - run 'npm install' first")

    return info, warnings


def main():
    try:
        info, warnings = check_environment()

        # Print environment status
        if info:
            print("Environment check:")
            for item in info:
                print(f"  {item}")

        if warnings:
            print("\nWarnings:")
            for warning in warnings:
                print(f"  {warning}")

        # SessionStart hooks should not block - just inform
        sys.exit(0)

    except Exception as e:
        print(f"Environment check error: {e}")
        sys.exit(0)


if __name__ == "__main__":
    main()
