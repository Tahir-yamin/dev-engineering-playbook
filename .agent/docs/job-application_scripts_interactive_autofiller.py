import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE_PATH = os.path.join(BASE_DIR, "data", "master_profile.json")
EXT_DIR = os.path.join(BASE_DIR, "autofill-extension")

def prepare_data():
    with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
        profile = json.load(f)
    
    experiences = []
    for exp in profile.get("experience", []):
        period = exp.get("period", "")
        experiences.append({
            "title": exp.get("title", ""),
            "company": exp.get("company", ""),
            "location": exp.get("location") or "Karachi, Pakistan",
            "description": "\n".join(exp.get("highlights", [])),
            "current": "Present" in period
        })
    
    return {
        "experience": experiences,
        "education": [
            {"institution": "NUST", "field": "Mechanical Engineering", "degree": "Bachelor", "start": "2010", "end": "2014"},
            {"institution": "NED", "field": "Industrial Engineering", "degree": "Master", "start": "2015", "end": "2017"}
        ],
        "skills": ["Project Management", "Primavera", "Excel", "SQL", "AutoCAD", "Planning", "Scheduling"]
    }

def make_js():
    data = prepare_data()
    return """
(function() {
    if (window.__WD_RUNNING) return alert("Already running!");
    window.__WD_RUNNING = true;
    
    console.log('[AUTOFILL] v3.9 Starting...');
    const profile = """ + json.dumps(data) + """;
    let logLines = [];

    const overlay = document.createElement('div');
    overlay.style.cssText = 'position:fixed;top:15px;right:15px;background:#2c3e50;color:#ecf0f1;padding:15px;border-radius:8px;z-index:999999;font:12px monospace;min-width:320px;box-shadow:0 4px 15px rgba(0,0,0,0.3);opacity:0.95';
    document.body.appendChild(overlay);
    
    function updateLog(msg) {
        logLines.push(msg);
        console.log('[AUTOFILL]', msg);
        const html = logLines.slice(-14).join('<br>'); 
        overlay.innerHTML = '<b style="color:#2ecc71">Autofill v3.9</b><hr style="margin:8px 0;opacity:0.3">' + html;
    }

    function wait(ms) { return new Promise(r => setTimeout(r, ms)); }

    function trigger(el) {
        if (!el) return;
        el.focus();
        el.dispatchEvent(new Event('input', {bubbles: true}));
        el.dispatchEvent(new Event('change', {bubbles: true}));
        el.dispatchEvent(new Event('blur', {bubbles: true}));
    }

    // --- LOGIC ---

    async function expandSections() {
        updateLog('Expanding sections...');
        const allBtns = [...document.querySelectorAll('[data-automation-id="add-button"]'), 
                         ...document.querySelectorAll('button[aria-label="Add"]')];
        
        // Exp
        if (allBtns[0]) {
            const expNeeded = profile.experience.length;
            let expCurrent = document.querySelectorAll('[id^="workExperience-"][id$="--jobTitle"]').length;
            while (expCurrent < expNeeded) {
                updateLog('Add Exp (' + (expCurrent+1) + ')');
                allBtns[0].click();
                await wait(1500); 
                expCurrent = document.querySelectorAll('[id^="workExperience-"][id$="--jobTitle"]').length;
            }
        }
        // Edu
        if (allBtns[1]) {
             const eduNeeded = profile.education.length;
             let eduCurrent = document.querySelectorAll('[id^="education-"][id$="--school"]').length;
             while (eduCurrent < eduNeeded) {
                 updateLog('Add Edu (' + (eduCurrent+1) + ')');
                 allBtns[1].click();
                 await wait(1500); 
                 eduCurrent = document.querySelectorAll('[id^="education-"][id$="--school"]').length;
             }
        }
    }

    async function fillExperience() {
        const groups = [...new Set([...document.querySelectorAll('[id^="workExperience-"]')].map(e => e.id.split('--')[0]))];
        updateLog('Filling ' + groups.length + ' Exp');
        
        for (let i = 0; i < Math.min(profile.experience.length, groups.length); i++) {
            const prefix = groups[i];
            const data = profile.experience[i];
            
            updateLog('> ' + data.title.substring(0,15));
            
            const title = document.getElementById(prefix + '--jobTitle');
            if (title) { title.value = data.title; trigger(title); }
            
            const company = document.getElementById(prefix + '--companyName');
            if (company) { company.value = data.company; trigger(company); }
            
            const loc = document.getElementById(prefix + '--location');
            if (loc) { loc.value = data.location; trigger(loc); }
            
            const desc = document.getElementById(prefix + '--roleDescription');
            if (desc) { desc.value = data.description; trigger(desc); }
            
            // Checkbox
            if (data.current) {
                const cb = document.querySelector('#' + prefix + '--isCurrent') || document.querySelector('input[id^="' + prefix + '"][type="checkbox"]');
                if (cb && !cb.checked) cb.click();
            }
        }
    }

    async function fillEducation() {
        const groups = [...new Set([...document.querySelectorAll('[id^="education-"]')].map(e => e.id.split('--')[0]))];
        updateLog('Filling ' + groups.length + ' Edu');

        for (let i = 0; i < Math.min(profile.education.length, groups.length); i++) {
             const prefix = groups[i];
             const data = profile.education[i];
             updateLog('> ' + data.institution);

             const school = document.getElementById(prefix + '--school');
             if (school) {
                 school.value = data.institution;
                 trigger(school);
                 await wait(800);
                 const opt = document.querySelector('[role="option"]');
                 if (opt && !opt.textContent.includes('No Items')) opt.click();
             }
             
             const field = document.getElementById(prefix + '--fieldOfStudy');
             if (field) { 
                 field.value = data.field; 
                 trigger(field);
                 await wait(800);
                 const opt = document.querySelector('[role="option"]');
                 if (opt && !opt.textContent.includes('No Items')) opt.click();
             }

             // Degree
             const degreeBtn = document.getElementById(prefix + '--degree');
             if (degreeBtn) {
                 degreeBtn.click();
                 await wait(1000);
                 const opts = document.querySelectorAll('[role="option"]');
                 const match = [...opts].find(o => o.textContent.includes(data.degree));
                 if (match) match.click();
                 await wait(500);
             }

             // Dates (YYYY)
             // Try standard inputs
             const startInput = document.querySelector('[id^="' + prefix + '"][id$="--firstYear"]') || 
                                document.querySelector('[id="' + prefix + '--firstYear"]');
             if (startInput) {
                 startInput.value = data.start;
                 trigger(startInput);
             } else {
                 // Fallback by label
                 const section = document.getElementById(prefix + '--school').closest('[data-automation-id="education-section"]'); 
                 // Simple fallback not feasible without precise DOM path, relying on IDs for now
             }

             const endInput = document.querySelector('[id^="' + prefix + '"][id$="--lastYear"]') ||
                              document.querySelector('[id="' + prefix + '--lastYear"]');
             if (endInput) {
                 endInput.value = data.end;
                 trigger(endInput);
             }
        }
    }

    async function fillSkills() {
        updateLog('Starting Skills...');
        // REVERT TO BROAD SELECTOR (v3.5)
        let input = document.querySelector('input[placeholder*="Add"]');
        if (!input) input = document.querySelector('[data-automation-id="searchBox"] input');
        // V3.7 specific
        if (!input) input = document.querySelector('input[placeholder*="Type to Add"]');

        if (!input) return updateLog('ERR: Skills input missing');
        
        for (const skill of profile.skills) {
            updateLog('Skill: ' + skill);
            
            input.value = skill;
            input.dispatchEvent(new Event('input', {bubbles: true}));
            
            // AGGRESSIVE TYPING from v3.8
            input.dispatchEvent(new KeyboardEvent('keydown', { bubbles:true, cancelable: true, keyCode: 40, key: 'ArrowDown', charCode: 0 }));
            input.dispatchEvent(new KeyboardEvent('keyup',  { bubbles:true, cancelable: true, keyCode: 40, key: 'ArrowDown', charCode: 0 }));
            
            await wait(2200); 
            
            const menu = document.querySelector('[role="listbox"]');
            if (menu) {
                const opts = Array.from(menu.querySelectorAll('[role="option"]'));
                updateLog('  Found ' + opts.length + ' opts');
                const match = opts.find(o => o.textContent.toLowerCase().includes(skill.toLowerCase().split(' ')[0]));
                
                if (match && !match.textContent.includes('No Items')) {
                     match.click();
                     updateLog('  ✓ Added');
                } else {
                     updateLog('  x No match - Skip');
                }
            } else {
                updateLog('  No dropdown - forcing Enter');
                input.dispatchEvent(new KeyboardEvent('keydown', { bubbles:true, cancelable: true, keyCode: 13, key: 'Enter', charCode: 0 }));
                input.dispatchEvent(new KeyboardEvent('keyup',  { bubbles:true, cancelable: true, keyCode: 13, key: 'Enter', charCode: 0 }));
            }
            await wait(500);
        }
    }

    async function main() {
        try {
            await expandSections();
            await wait(1000);
            await fillExperience();
            await wait(1000);
            await fillEducation(); 
            await wait(1000);
            await fillSkills();
            updateLog('COMPLETE! Review & Submit.');
            setTimeout(() => { overlay.remove(); window.__WD_RUNNING = false; }, 20000);
        } catch (e) {
            updateLog('Error: ' + e.message);
            window.__WD_RUNNING = false;
        }
    }

    main();
})();
"""

def setup():
    if not os.path.exists(EXT_DIR): os.makedirs(EXT_DIR)
    
    manifest = {
        "manifest_version": 3,
        "name": "Workday Autofiller",
        "version": "3.9",
        "description": "Final Combined Polish",
        "permissions": ["activeTab", "scripting"],
        "host_permissions": ["https://*.myworkdayjobs.com/*"],
        "action": {"default_popup": "popup.html"}
    }
    with open(os.path.join(EXT_DIR, "manifest.json"), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
    
    popup_html = """<!DOCTYPE html>
<html>
<head><style>
body { width: 250px; padding: 15px; font-family: sans-serif; background:#f5f6fa; }
button { width: 100%; padding: 12px; background: #2ecc71; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; }
button:hover { background: #27ae60; }
#status { margin-top: 15px; padding: 10px; border-radius: 4px; font-size: 13px; display: none; background: #fff; border: 1px solid #ddd; }
.success { color: #27ae60; border-color: #27ae60 !important; }
</style></head>
<body>
<h3>Autofill v3.9</h3>
<p style="font-size:12px;color:#7f8c8d">Final Polish</p>
<button id="run">START v3.9</button>
<div id="status">Ready</div>
<script src="popup.js"></script>
</body>
</html>"""
    
    with open(os.path.join(EXT_DIR, "popup.html"), 'w', encoding='utf-8') as f:
        f.write(popup_html)
    
    with open(os.path.join(EXT_DIR, "popup.js"), 'w', encoding='utf-8') as f:
        f.write(r"""
document.getElementById('run').addEventListener('click', async () => {
    const status = document.getElementById('status');
    status.style.display = 'block';
    status.textContent = 'Injecting...';
    try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            files: ['content.js'],
            world: 'MAIN'
        });
        status.textContent = 'Running...';
        status.className = 'success';
    } catch (e) {
        status.textContent = 'Err: ' + e.message;
    }
});
""")
    
    with open(os.path.join(EXT_DIR, "content.js"), 'w', encoding='utf-8') as f:
        f.write(make_js())
    
    print("Extension v3.9 Generated - FINAL")

if __name__ == "__main__":
    setup()
