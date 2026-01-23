# UI UX Pro Max Skill

**Source**: [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)  
**Version**: 2.0  
**Author**: @nextlevelbuilder  
**License**: MIT

---

## Overview

An AI skill that provides design intelligence for building professional UI/UX across multiple platforms. Features intelligent design system generation with 100 industry-specific reasoning rules.

---

## Key Features

### 1. Design System Generator (v2.0)
AI-powered reasoning engine that analyzes project requirements and generates complete, tailored design systems.

### 2. 100 Industry-Specific Rules
Pre-built reasoning rules for:
- E-commerce
- SaaS dashboards
- Wellness/Spa
- Finance/Trading
- Social platforms
- And 95+ more

### 3. Pre-Delivery Checklist
Automated quality assurance:
- [ ] No emojis as icons (use SVG: Heroicons/Lucide)
- [ ] cursor-pointer on all clickable elements
- [ ] Hover states with smooth transitions (150-300ms)
- [ ] Light mode: text contrast 4.5:1 minimum
- [ ] Focus states visible for keyboard nav
- [ ] prefers-reduced-motion respected
- [ ] Responsive: 375px, 768px, 1024px, 1440px

---

## Installation

### CLI (Recommended)
```bash
npx ui-ux-pro-max@latest install
```

### Antigravity / Gemini CLI
Add to your skill path or reference directly.

---

## Usage

### Generate Design System
```
@ui-ux-pro-max generate design system for [PROJECT_TYPE]
```

### Example Output

```
+----------------------------------------------------------------------------------------+
| TARGET: Serenity Spa - RECOMMENDED DESIGN SYSTEM                                       |
+----------------------------------------------------------------------------------------+
| PATTERN: Hero-Centric + Social Proof                                                   |
| STYLE: Soft UI Evolution                                                               |
| COLORS: Primary #E8B4B8 | Secondary #A8D5BA | CTA #D4AF37                             |
| TYPOGRAPHY: Cormorant Garamond / Montserrat                                            |
| KEY EFFECTS: Soft shadows + Smooth transitions (200-300ms)                             |
| AVOID: Bright neon colors, Harsh animations, Dark mode, AI purple/pink gradients       |
+----------------------------------------------------------------------------------------+
```

---

## Anti-Patterns to Avoid

- ❌ Bright neon colors
- ❌ Harsh animations
- ❌ Dark mode by default (check user preference)
- ❌ AI purple/pink gradients
- ❌ Using emojis as functional icons

---

## Related Skills

- [frontend-design](../frontend-design/SKILL.md)
- [mobile-design](../mobile-design/SKILL.md)

---

**Added to Knowledge Base**: 2026-01-22  
**Credit**: @nextlevelbuilder
