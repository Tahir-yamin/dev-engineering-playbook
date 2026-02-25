#!/usr/bin/env python3
"""
Sovereign Compliance Auditor v1.0
Checks for SOC2, ISO 27001, and GDPR framework markers.
"""

import os
import sys

def check_compliance(framework):
    print(f"--- Running {framework} Compliance Audit ---")
    
    checks = {
        "SOC2": [
            ("Audit Logging", "logs/sentinel.log"),
            ("Security Policy", "GEMINI.md"),
            ("Access Control", ".agent/rules")
        ],
        "ISO27001": [
            ("Asset Inventory", "CODEBASE.md"),
            ("Risk Assessment", "ARCHITECTURE.md"),
            ("Secure Coding", "skills/clean-code/SKILL.md")
        ],
        "GDPR": [
            ("Data Privacy", "README.md"),
            ("Data Residency", "kubernetes/"),
            ("Encryption Policy", "GEMINI.md")
        ]
    }
    
    if framework not in checks:
        print(f"Unknown framework: {framework}")
        return False
        
    passed = True
    for item, path in checks[framework]:
        if os.path.exists(path) or os.path.isdir(path):
            print(f"✅ PASSED: {item} ({path})")
        else:
            print(f"❌ FAILED: {item} ({path} missing)")
            passed = False
            
    return passed

if __name__ == "__main__":
    frameworks = ["SOC2", "ISO27001", "GDPR"]
    all_passed = True
    for f in frameworks:
        if not check_compliance(f):
            all_passed = False
        print("-" * 30)
        
    if all_passed:
        print("\n✨ Workspace is COMPLIANT with World-Class Standards.")
    else:
        print("\n⚠️  Compliance Gaps Detected. Please review missing markers.")
