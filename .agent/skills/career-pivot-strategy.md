# Career Pivot Strategy Skills

**Topics**: CV Tailoring, ATS Optimization, Role Pivoting
**Version**: 1.0

---

## Skill #1: Strategic Role Pivoting

### When to Use
- Applying for a role that differs from your current job title.
- You have the experience but it's buried under a different primary function (e.g., Planning Manager -> Piping Supervisor).
- Avoiding "Overqualified" or "Irrelevant" rejections.

### Strategy Pattern

1.  **Title Re-alignment**:
    -   **Old**: "Senior Planning Engineer | Project Controls Lead"
    -   **New**: "[Target Role Title] | [Secondary Relevant Title] | [Core Credential]"
    -   *Example*: "Piping Supervisor | Site Superintendent | Mechanical Engineer"

2.  **Summary Rewrite**:
    -   Remove: "Strategic planning", "EVM", "Governance", "Reporting".
    -   Inject: "Hands-on", "Site Execution", "Supervision", "QA/QC", "Manpower Management".
    -   *Action*: Move from "Managed a portfolio of..." to "Supervised installation of...".

3.  **Experience Reframing**:
    -   **Before (Planning)**: "Developed Level-4 schedule for piping works."
    -   **After (Execution)**: "Supervised piping fabrication and erection sequences to meet daily targets."
    -   *Key*: Change the *verb* from a passive/monitoring one to an active/execution one.

4.  **Keyword Injection**:
    -   Scan JD for specific systems (e.g., "CWS", "Firefighting", "Brownfield").
    -   Explicitly add these to a "Technical Skills" or "Core Competencies" section.

### Checklist
- [ ] Does the CV title match the Job Post title?
- [ ] Are "management" keywords replaced with "execution" keywords?
- [ ] Is the "Professional Summary" focused on the *future* role, not the past history?
- [ ] Have "soft" skills been replaced with "hard" technical skills relevant to the trade?

---

## Skill #2: ATS Keyword Optimization

### When to Use
- Submitting to large portals (Wood, KBR, Aramco) where AI/ATS filters are the first gate.

### Keyword Injection Protocol

1.  **Exact Match**: Use the exact phrasing from the JD (e.g., "WBS" vs "Work Breakdown Structure").
2.  **Frequency**: Ensure core keywords appear 2-3 times (Summary, Skills, Experience).
3.  **Context**: Don't just list them; use them in sentences.
    -   *Bad*: "Skills: CWS"
    -   *Good*: "Managed installation of Cooling Water Systems (CWS) during shutdown."

---

---

## Skill #3: Profile Safety Protocol

### Golden Rule
**The Master Profile (`master_profile.json`) must ALWAYS reflect your core competency.**
-   For this user: **Senior Planning Engineer / Project Controls Lead**.
-   **Never** leave the master profile in a "Pivoted State" (e.g., Piping Supervisor) after a session.

### Execution Protocol for Radial Pivots
When a job requires a >50% deviation from the core profile (e.g., Applying for a Site Supervisor role):

1.  **Backup**: Ensure `master_profile.json` is safe or backed up.
2.  **Pivot**: Edit the profile *only* for the purpose of generating that specific application's artifacts.
3.  **Generate**: Run the CV/CL generator scripts.
4.  **IMMEDIATE REVERT**: **Mandatory step**. Restore the `master_profile.json` to its original state *before* closing the task.
5.  **Verify**: Confirm the title is back to "Senior Planning Engineer".

*Failure to revert corrupts the "Source of Truth" for future high-value applications.*

---

## Skill #4: Digital Footprint Optimization

### When to Use
- Applying for high-tier technical roles (Aramco, ADNOC, Global Consultants).
- You want to bridge the gap between "Project Planner" and "Data-Driven Specialist".

### Optimization Protocol

1.  **GitHub Synchronisation**:
    -   Include `github.com/[username]` in the CV header.
    -   *Strategy*: Ensure the LinkedIn and GitHub profiles reflect advanced automation skills.
    -   *Logic*: Recruiters in 2026 look for candidates who use AI and scripting (Python) to optimize traditional construction workflows.

2.  **Bio-Detail Layout**:
    -   **Grid View**: Use a side-by-side grid layout for **Education** and **Certifications** to save vertical space while maximizing information density.
    -   **LaTeX Cleaning**: Always strip comments (`%`) and math artifacts (`$|$`) before conversion to ensure a professional digital PDF.

---

## Related Skills
- [job-application-automation](file:///d:/my-dev-knowledge-base/.agent/skills/job-application-automation.md)
