# Professional Automation: The SaaSpocalypse Patterns (2026)

These patterns, released in early February 2026, represent the shift from "AI Assistants" to "Professional Autonomy." They integrate expert-level logic into standardized files.

## 1. The Playbook Pattern
A "Playbook" is a Markdown file that defines an organization's standard positions, acceptable ranges, and redlines.

**Pattern Implementation**:
- **Standard Position**: "We require Net-45 payment terms."
- **Fallback**: "Net-30 is acceptable if a 2% discount is applied."
- **Escalation Trigger**: "Anything less than Net-30 requires CFO approval."

**How to use locally**:
Create `docs/playbooks/legal.local.md` and reference it whenever reviewing contracts.

## 2. The Risk Tiering Pattern (Green/Yellow/Red)
Instead of vague feedback, use a tiered severity system to automate decision-making.

- 🟢 **GREEN (Acceptable)**: Aligns with playbook. No action needed.
- 🟡 **YELLOW (Negotiate)**: Deviates but within fallback range. Generate redline.
- 🔴 **RED (Escalate)**: Outside acceptable range. Stop and manifest a risk report.

## 3. Variance / Flux Driver Pattern
Used primarily in Finance and COGS analysis. Decomposes gaps into specific narratives.

**Workflow**:
1. **Gather Data**: Compare Actual vs Budget.
2. **Identify Drivers**: Price Effect, Volume Effect, Mix Effect, or Timing.
3. **Generate Narrative**: "Variance of $X is 80% driven by [Volume Effect] due to [Event]."

## 4. Invisible Scaffolding
The agent observes user behavior and silently references these playbooks to offer proactive "Reviewable Actions."

---
**References**:
- `external-libs/knowledge-work-plugins/legal/commands/review-contract.md`
- `external-libs/knowledge-work-plugins/finance/commands/variance-analysis.md`
