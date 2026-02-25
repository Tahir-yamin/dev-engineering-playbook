
(function() {
    if (window.__WD_RUNNING) return alert("Already running!");
    window.__WD_RUNNING = true;
    
    console.log('[AUTOFILL] v3.9 Starting...');
    const profile = {"experience": [{"title": "Senior Planning Engineer / Project Controls Lead", "company": "Pakistan State Oil (PSO)", "location": "Karachi, Pakistan", "description": "Lead project planning and controls function for nationwide oil & gas retail and infrastructure projects\nDeveloped and governed Level-3 & Level-4 baseline schedules, progress rules, and reporting standards\nReviewed contractor programmes, challenged logic and durations, and advised management on accept/reject decisions\nPerformed schedule variance analysis, EVM (SPI/CPI), forecasting, and early-warning reporting\nSupported EOT evaluations and contractor claims through planning narratives and impact assessments aligned with FIDIC principles\nProduced commercially focused executive reports and Power BI dashboards for portfolio-level decision making", "current": true}, {"title": "Project Planning & Scheduling Manager", "company": "Karachi Shipyard & Engineering Works (KS&EW)", "location": "Karachi, Pakistan", "description": "Led the project controls function for USD 750M+ EPC portfolio including submarines, naval vessels, offshore jackets, and topsides\nEstablished programme baselines, integrated engineering, procurement, fabrication, and construction schedules\nControlled critical path, float erosion, and delay events, advising leadership on mitigation and recovery options\nSupported variation identification and EOT preparation, providing schedule substantiation and delay analysis\nChaired programme review meetings with clients, PMCs, Naval HQ, and international EPC partners\nManaged and mentored a multi-disciplinary planning team (15 engineers)", "current": false}, {"title": "Project Planning Manager", "company": "Titanno Pvt Ltd (Nova Marine)", "location": "Karachi, Pakistan", "description": "Managed planning, scheduling, and project controls for offshore construction and ship repair EPC projects\nDeveloped baseline and execution schedules, manpower histograms, and cash flow forecasts\nServed as single point of accountability for schedule inputs to claims, variations, and management decisions\nSupported EOT submissions through progress analysis, logic review, and delay substantiation\nProvided commercial planning input for EPC tenders including timelines, man-hour estimates, and risk considerations", "current": false}, {"title": "Project Planning & Controls Engineer", "company": "SKM Air Conditioning (UAE) | Zamil Air Conditioners (KSA)", "location": "UAE & Saudi Arabia", "description": "Provided project planning, scheduling, and controls support for large-scale HVAC and industrial EPC projects\nDeveloped execution schedules, monitored progress, and supported commercial reporting to clients\nAssisted in delay monitoring, recovery planning, and claims-related planning support\nSupported project managers and commercial teams with schedule-based recommendations impacting payments, variations, and recovery", "current": false}], "education": [{"institution": "NUST", "field": "Mechanical Engineering", "degree": "Bachelor", "start": "2010", "end": "2014"}, {"institution": "NED", "field": "Industrial Engineering", "degree": "Master", "start": "2015", "end": "2017"}], "skills": ["Project Management", "Primavera", "Excel", "SQL", "AutoCAD", "Planning", "Scheduling"]};
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
