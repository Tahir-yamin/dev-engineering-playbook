---
description: Comprehensive workflow for securing fully funded academic positions (MS/PHD) with a focus on high-stipend regions and IELTS waivers.
---

# Academic Application & Scholarship Workflow

**Status**: 🎓 ACADEMIC MAESTRO ACTIVE
**Focus**: Mechanical Engineering + Embodied AI / Robotics
**Target Regions**: Europe (Salaried), Australia (RTP), Canada, USA

---

## 🎯 COMPLETE ACADEMIC PIPELINE

### 1. DISCOVERY: Scholarly Source & Lab Search
```bash
# Research specific labs and their current funding status
npx -y playwright-researcher "Top Robotics Labs in Norway and Netherlands seeking AI-Mechanical PhDs"

# Find 2026 application deadlines and IELTS waiver policies
# Search Keywords: "English Proficiency Certificate waiver [University Name]"
```

### 2. PROFILING: Success Probability Matrix
| Criteria | Weight | Your Status | Action |
|----------|--------|-------------|--------|
| Research Alignment | 40% | High (Embodied AI) | Align SOP with Lab's latest papers |
| GPA/Transcript | 20% | TBD | Prepare official transcripts |
| English Proficiency | 15% | Waiver Ready | Attach "English Proficiency Certificate" |
| Publications/Thesis | 25% | Strong (White Paper) | Highlight "Green-VLA" and "Taccel" |

### 3. GENERATION: The "Scholar" Deck
- **Academic CV**: Research-first, citing "Embodied Generalist Robotics".
- **Statement of Purpose (SOP)**: Focus on the "Embodied Intelligence" frontier.
- **Research Proposal**: Tailored per lab (use `research-technical-spike.prompt`).

### 4. COLD OUTREACH: Professor Engagement
```bash
# Generate high-impact cold emails to PIs (Principal Investigators)
python job-application\scripts\gmail_oauth_sender.py \
  --professor "Prof. Name" \
  --lab "Autonomous Systems Lab" \
  --attach "CV_Academic.pdf" "Research_Proposal.pdf"
```

### 5. TRACKING: Portal & Scholarship Log
- Track via: `job-application/data/academic_tracking.md`
- Include: First choice university, Second choice, and "Safety" nets.

---

## 🛠️ KEY SCRIPTS & AGENTS

### Specialist Agents:
- **`academic-researcher`**: For deep literature reviews and lab vetting.
- **`specification.agent`**: To parse complex University Admission Requirements.

### Automation Scripts:
| Script | Use for Academic |
|--------|------------------|
| `apply_from_gemini.py` | Refactored for University Portal scraping |
| `gmail_oauth_sender.py` | Sending cold emails to Professors |
| `checklist.py` | Verifying application package completeness |

---

## ✅ SUCCESS CRITERIA
- [ ] 100% Fully Funded (Stipend + Tuition)
- [ ] No IELTS required (Waiver accepted via EPC)
- [ ] High stipend (> $40k USD equivalent in Europe)
- [ ] Research alignment with "Embodied Intelligence"

---
**Last Updated**: 2026-02-24
**Next Action**: Refactor industrial CV to Academic Format.
