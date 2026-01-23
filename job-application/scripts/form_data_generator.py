"""
Website Application Form Data Generator
=======================================
Generates pre-filled form data for job application websites.
When a job has a website link instead of email, use this to get copy-paste ready data.

Usage:
    python form_data_generator.py --company "AECOM" --role "Project Controls Manager"
    python form_data_generator.py --company "AECOM" --role "Project Controls Manager" --save
"""

import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE_PATH = os.path.join(BASE_DIR, "data", "master_profile.json")
GENERATED_DIR = os.path.join(BASE_DIR, "generated")


class FormDataGenerator:
    """Generate copy-paste ready data for website application forms."""
    
    def __init__(self):
        with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
            self.profile = json.load(f)
    
    def generate_form_data(self, company: str = None, role: str = None) -> dict:
        """Generate all form fields."""
        
        p = self.profile["personal"]
        
        # Short summary (50 words)
        short_summary = f"PMP-certified Project Controls professional with 15+ years in EPC, Oil & Gas, and offshore projects. Expert in Primavera P6, schedule risk analysis, delay/EOT claims under FIDIC. Led teams up to 15 engineers on USD 750M+ portfolios. Available immediately for UAE/GCC roles."
        
        # Long summary (100 words)
        long_summary = self.profile.get("professional_summary", short_summary)
        
        # Skills comma-separated
        skills_csv = ", ".join(self.profile.get("technical_skills", []) + 
                              ["Project Controls", "Planning & Scheduling", "Delay Analysis", 
                               "EOT Claims", "FIDIC", "Earned Value Management", "PMP"])
        
        # Experience one-liners
        exp_lines = []
        for exp in self.profile.get("experience", [])[:4]:
            line = f"{exp['title']} | {exp['company']} | {exp['period']}"
            if exp.get('project_value'):
                line += f" | {exp['project_value']}"
            exp_lines.append(line)
        
        # Top achievements
        achievements = [
            "Led project controls function for USD 750M+ EPC portfolio including submarines, naval vessels, and offshore jackets",
            "Managed 15-engineer multi-disciplinary planning team across multiple concurrent projects",
            "Supported successful EOT claims through delay analysis and schedule substantiation under FIDIC",
            "Established planning governance frameworks and progress measurement standards adopted company-wide",
            "Reduced reporting time by 50% through Power BI dashboard automation"
        ]
        
        form_data = {
            "personal": {
                "full_name": p["name"],
                "first_name": p["name"].split()[0],
                "last_name": p["name"].split()[-1],
                "email": p["email_primary"],
                "phone": p["phone"],
                "linkedin": p["linkedin"],
                "portfolio": p.get("portfolio", ""),
                "location": p["location"],
                "city": "Karachi",
                "country": "Pakistan",
            },
            "availability": {
                "notice_period": "Immediate",
                "start_date": "Immediate",
                "relocation": "Yes",
                "relocation_locations": "UAE, Qatar, Saudi Arabia, Europe",
                "work_authorization": "Requires Sponsorship",
                "willing_to_travel": "Yes (up to 50%)",
            },
            "summaries": {
                "short_50_words": short_summary,
                "long_100_words": long_summary,
                "headline": f"{p['title']}",
                "tagline": "15+ Years | EPC | Oil & Gas | Primavera P6 | PMP",
            },
            "skills": {
                "comma_separated": skills_csv,
                "core_competencies": self.profile.get("core_competencies", []),
                "technical_tools": self.profile.get("technical_skills", []),
            },
            "experience": {
                "years_experience": "15+",
                "current_title": self.profile["experience"][0]["title"] if self.profile.get("experience") else "",
                "current_company": self.profile["experience"][0]["company"] if self.profile.get("experience") else "",
                "one_liners": exp_lines,
            },
            "education": {
                "highest_degree": "MSc Mechanical Engineering",
                "university": "NUST, Pakistan",
                "certifications": self.profile.get("certifications", []),
            },
            "salary": {
                "expected_uae": "18,000 - 22,000 AED",
                "expected_qatar": "18,000 - 25,000 QAR",
                "expected_saudi": "20,000 - 28,000 SAR",
                "current_salary": "Competitive",
                "negotiable": "Yes - based on total package",
            },
            "achievements": achievements[:3],
            "cover_letter_snippet": f"With 15+ years of experience in project controls across EPC, Oil & Gas, and offshore projects valued up to USD 750M, I am confident I can contribute to {company or 'your company'}'s success in the {role or 'Project Controls'} role.",
        }
        
        return form_data
    
    def print_form_data(self, company: str = None, role: str = None):
        """Print form data in copy-paste friendly format."""
        
        data = self.generate_form_data(company, role)
        
        print(f"\n{'='*70}")
        print(f"📋 APPLICATION FORM DATA - {company or 'Generic'}")
        print(f"{'='*70}")
        
        print(f"\n--- PERSONAL INFORMATION ---")
        for key, val in data["personal"].items():
            print(f"{key.replace('_', ' ').title()}: {val}")
        
        print(f"\n--- AVAILABILITY ---")
        for key, val in data["availability"].items():
            print(f"{key.replace('_', ' ').title()}: {val}")
        
        print(f"\n--- PROFESSIONAL SUMMARY ---")
        print(f"\nShort (50 words):")
        print(data["summaries"]["short_50_words"])
        print(f"\nHeadline: {data['summaries']['headline']}")
        
        print(f"\n--- SKILLS (copy this) ---")
        print(data["skills"]["comma_separated"])
        
        print(f"\n--- EXPERIENCE ---")
        print(f"Years: {data['experience']['years_experience']}")
        print(f"Current: {data['experience']['current_title']} at {data['experience']['current_company']}")
        
        print(f"\n--- SALARY EXPECTATION ---")
        for key, val in data["salary"].items():
            print(f"{key.replace('_', ' ').title()}: {val}")
        
        print(f"\n--- TOP 3 ACHIEVEMENTS (pick for form) ---")
        for i, ach in enumerate(data["achievements"], 1):
            print(f"{i}. {ach}")
        
        print(f"\n--- COVER LETTER SNIPPET ---")
        print(data["cover_letter_snippet"])
        
        print(f"\n{'='*70}")
        
        return data
    
    def save_form_data(self, company: str, role: str) -> str:
        """Save form data as HTML for easy copy-paste."""
        
        data = self.generate_form_data(company, role)
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Application Data - {company}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 20px auto; padding: 20px; }}
        .header {{ background: #2e7d32; color: white; padding: 20px; border-radius: 8px; }}
        .section {{ background: #f5f5f5; padding: 15px; margin: 15px 0; border-radius: 8px; }}
        .section h3 {{ margin-top: 0; color: #2e7d32; }}
        .field {{ margin: 8px 0; padding: 8px; background: white; border-radius: 4px; cursor: pointer; }}
        .field:hover {{ background: #e8f5e9; }}
        .field label {{ font-weight: bold; color: #666; }}
        .field .value {{ display: block; margin-top: 4px; }}
        .copyable {{ background: #fff3e0; padding: 10px; border-radius: 4px; cursor: pointer; }}
        .copyable:hover {{ background: #ffe0b2; }}
        .btn {{ background: #2e7d32; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; margin: 5px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📋 Application Form Data</h1>
        <p><strong>Company:</strong> {company} | <strong>Role:</strong> {role}</p>
        <p>Click any field to copy!</p>
    </div>
    
    <div class="section">
        <h3>Personal Information</h3>
        {"".join(f'<div class="field" onclick="copyText(this)"><label>{k.replace("_", " ").title()}:</label><span class="value">{v}</span></div>' for k, v in data["personal"].items())}
    </div>
    
    <div class="section">
        <h3>Availability</h3>
        {"".join(f'<div class="field" onclick="copyText(this)"><label>{k.replace("_", " ").title()}:</label><span class="value">{v}</span></div>' for k, v in data["availability"].items())}
    </div>
    
    <div class="section">
        <h3>Professional Summary (Click to Copy)</h3>
        <div class="copyable" onclick="copyText(this)">
            <strong>Short (50 words):</strong><br>
            {data["summaries"]["short_50_words"]}
        </div>
        <br>
        <div class="copyable" onclick="copyText(this)">
            <strong>Long (100 words):</strong><br>
            {data["summaries"]["long_100_words"][:500]}
        </div>
    </div>
    
    <div class="section">
        <h3>Skills (Click to Copy)</h3>
        <div class="copyable" onclick="copyText(this)">
            {data["skills"]["comma_separated"]}
        </div>
    </div>
    
    <div class="section">
        <h3>Salary Expectation</h3>
        {"".join(f'<div class="field" onclick="copyText(this)"><label>{k.replace("_", " ").title()}:</label><span class="value">{v}</span></div>' for k, v in data["salary"].items())}
    </div>
    
    <div class="section">
        <h3>Top Achievements (Pick for Form)</h3>
        {"".join(f'<div class="copyable" onclick="copyText(this)" style="margin:5px 0;">{i}. {ach}</div>' for i, ach in enumerate(data["achievements"], 1))}
    </div>
    
    <div class="section">
        <h3>Cover Letter Snippet</h3>
        <div class="copyable" onclick="copyText(this)">
            {data["cover_letter_snippet"]}
        </div>
    </div>
    
    <script>
        function copyText(element) {{
            const text = element.querySelector('.value')?.innerText || element.innerText;
            navigator.clipboard.writeText(text.trim());
            element.style.background = '#c8e6c9';
            setTimeout(() => element.style.background = '', 500);
        }}
    </script>
    
    <p><em>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}</em></p>
</body>
</html>"""
        
        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"FormData_{company.replace(' ', '_')}_{timestamp}.html"
        output_path = os.path.join(GENERATED_DIR, filename)
        os.makedirs(GENERATED_DIR, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"\n✓ Form data saved: {output_path}")
        print(f"📋 Open in browser - click any field to copy!")
        
        return output_path


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate Form Data for Website Applications")
    parser.add_argument("--company", type=str, default="", help="Company name")
    parser.add_argument("--role", type=str, default="Project Controls Manager", help="Job title")
    parser.add_argument("--save", action="store_true", help="Save as HTML file")
    
    args = parser.parse_args()
    
    gen = FormDataGenerator()
    
    if args.save:
        path = gen.save_form_data(args.company or "Generic", args.role)
        print(f"\n📍 HTML File: {path}")
        print(f"   (Open this file in your browser to copy-paste fields)")
    else:
        gen.print_form_data(args.company, args.role)


if __name__ == "__main__":
    main()
