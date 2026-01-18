# TODO App - Design System Specification

**Version**: 1.0  
**Design Language**: Modern, Clean, Dark-Mode First  
**Last Updated**: December 28, 2025

---

## 🎨 Color System

### Brand Colors
```json
{
  "primary": {
    "50": "#EFF6FF",
    "100": "#DBEAFE",
    "200": "#BFDBFE",
    "300": "#93C5FD",
    "400": "#60A5FA",
    "500": "#3B82F6",
    "600": "#2563EB",
    "700": "#1D4ED8",
    "800": "#1E40AF",
    "900": "#1E3A8A"
  },
  "success": {
    "500": "#10B981",
    "600": "#059669"
  },
  "warning": {
    "500": "#F59E0B",
    "600": "#D97706"
  },
  "error": {
    "500": "#EF4444",
    "600": "#DC2626"
  }
}
```

### Neutral Colors (Dark Mode)
```json
{
  "background": {
    "primary": "#0F172A",
    "secondary": "#1E293B",
    "tertiary": "#334155"
  },
  "surface": {
    "elevated": "#1E293B",
    "card": "#334155"
  },
  "text": {
    "primary": "#F1F5F9",
    "secondary": "#CBD5E1",
    "tertiary": "#94A3B8",
    "muted": "#64748B"
  },
  "border": {
    "default": "#334155",
    "hover": "#475569",
    "focus": "#3B82F6"
  }
}
```

### Neutral Colors (Light Mode)
```json
{
  "background": {
    "primary": "#FFFFFF",
    "secondary": "#F8FAFC",
    "tertiary": "#F1F5F9"
  },
  "surface": {
    "elevated": "#FFFFFF",
    "card": "#F8FAFC"
  },
  "text": {
    "primary": "#0F172A",
    "secondary": "#475569",
    "tertiary": "#64748B",
    "muted": "#94A3B8"
  },
  "border": {
    "default": "#E2E8F0",
    "hover": "#CBD5E1",
    "focus": "#3B82F6"
  }
}
```

---

## 📝 Typography

### Font Families
```css
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', monospace;
```

### Font Sizes
```json
{
  "xs": "0.75rem",    /* 12px */
  "sm": "0.875rem",   /* 14px */
  "base": "1rem",     /* 16px */
  "lg": "1.125rem",   /* 18px */
  "xl": "1.25rem",    /* 20px */
  "2xl": "1.5rem",    /* 24px */
  "3xl": "1.875rem",  /* 30px */
  "4xl": "2.25rem",   /* 36px */
  "5xl": "3rem"       /* 48px */
}
```

### Font Weights
```json
{
  "normal": 400,
  "medium": 500,
  "semibold": 600,
  "bold": 700
}
```

### Line Heights
```json
{
  "tight": 1.25,
  "normal": 1.5,
  "relaxed": 1.75
}
```

---

## 📐 Spacing System

```json
{
  "0": "0",
  "1": "0.25rem",   /* 4px */
  "2": "0.5rem",    /* 8px */
  "3": "0.75rem",   /* 12px */
  "4": "1rem",      /* 16px */
  "5": "1.25rem",   /* 20px */
  "6": "1.5rem",    /* 24px */
  "8": "2rem",      /* 32px */
  "10": "2.5rem",   /* 40px */
  "12": "3rem",     /* 48px */
  "16": "4rem",     /* 64px */
  "20": "5rem"      /* 80px */
}
```

---

## 🔲 Border Radius

```json
{
  "none": "0",
  "sm": "0.125rem",   /* 2px */
  "base": "0.25rem",  /* 4px */
  "md": "0.375rem",   /* 6px */
  "lg": "0.5rem",     /* 8px */
  "xl": "0.75rem",    /* 12px */
  "2xl": "1rem",      /* 16px */
  "full": "9999px"
}
```

---

## 🌓 Shadows

### Light Mode
```css
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-base: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
--shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
```

### Dark Mode
```css
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.3);
--shadow-base: 0 1px 3px 0 rgb(0 0 0 / 0.4), 0 1px 2px -1px rgb(0 0 0 / 0.4);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.4), 0 2px 4px -2px rgb(0 0 0 / 0.4);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.4), 0 4px 6px -4px rgb(0 0 0 / 0.4);
--shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.4), 0 8px 10px -6px rgb(0 0 0 / 0.4);
```

---

## 🎭 Component Specifications

### Button
```typescript
const buttonVariants = {
  primary: {
    color: "text-white",
    background: "bg-blue-600 hover:bg-blue-700",
    border: "border-transparent",
    shadow: "shadow-sm"
  },
  secondary: {
    color: "text-slate-200",
    background: "bg-slate-700 hover:bg-slate-600",
    border: "border-slate-600",
    shadow: "shadow-sm"
  },
  ghost: {
    color: "text-slate-300 hover:text-white",
    background: "hover:bg-slate-800",
    border: "border-transparent",
    shadow: "shadow-none"
  },
  danger: {
    color: "text-white",
    background: "bg-red-600 hover:bg-red-700",
    border: "border-transparent",
    shadow: "shadow-sm"
  }
}

const buttonSizes = {
  sm: "px-3 py-1.5 text-sm",
  md: "px-4 py-2 text-base",
  lg: "px-6 py-3 text-lg"
}
```

### Card
```typescript
const cardStyles = {
  base: "rounded-lg border border-slate-700 bg-slate-800 shadow-lg",
  padding: "p-6",
  hover: "hover:border-slate-600 transition-colors"
}
```

### Input
```typescript
const inputStyles = {
  base: "w-full rounded-md border px-3 py-2",
  colors: "bg-slate-900 border-slate-700 text-slate-100",
  focus: "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
  placeholder: "placeholder:text-slate-500"
}
```

### Task Card
```typescript
const taskCardStyles = {
  base: "rounded-lg border p-4",
  default: "bg-slate-800 border-slate-700 hover:border-slate-600",
  completed: "bg-slate-900 border-slate-800",
  priority: {
    low: "border-l-4 border-l-green-500",
    medium: "border-l-4 border-l-yellow-500",
    high: "border-l-4 border-l-red-500"
  }
}
```

---

## ✨ Animations

### Transitions
```css
--transition-fast: 150ms;
--transition-base: 200ms;
--transition-slow: 300ms;

/* Easing */
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
```

### Common Animations
```css
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes shimmer {
  0% { background-position: -1000px 0; }
  100% { background-position: 1000px 0; }
}
```

---

## 📱 Responsive Breakpoints

```json
{
  "sm": "640px",
  "md": "768px",
  "lg": "1024px",
  "xl": "1280px",
  "2xl": "1536px"
}
```

### Layout Grid
```css
.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 1rem;
}

@media (min-width: 640px) {
  .container { padding: 0 2rem; }
}
```

---

## 🎯 Design Principles

### 1. Dark Mode First
- Design for dark mode, adapt for light
- Ensure sufficient contrast ratios
- Use subtle shadows in dark mode

### 2. Consistency
- Use design tokens consistently
- Follow spacing system
- Maintain visual hierarchy

### 3. Accessibility
- Minimum contrast ratio: 4.5:1 for text
- Focus states visible and clear
- Keyboard navigation support

### 4. Performance
- Optimize images
- Use CSS transforms for animations
- Minimize layout shifts

---

## 📋 Component Library

### Core Components

```typescript
// Components to implement

Button
  - variants: primary, secondary, ghost, danger
  - sizes: sm, md, lg
  - states: default, hover, active, disabled

Card
  - variants: default, elevated
  - interactive: clickable, hoverable

Input
  - types: text, email, password, textarea
  - states: default, focus, error, disabled

Modal
  - sizes: sm, md, lg, xl
  - animations: fade in, slide in

Toast
  - variants: success, error, warning, info
  - positions: top-right, top-center, etc.

DropdownMenu
  - trigger: button, custom
  - animation: fade & scale

Checkbox / Radio
  - states: unchecked, checked, indeterminate
  - sizes: sm, md, lg

Badge
  - variants: default, success, warning, error
  - sizes: sm, md

Skeleton
  - shapes: text, circle, rectangle
  - animation: shimmer
```

---

## 🖼️ Iconography

### Icon Library
- **Primary**: Lucide React
- **Size**: 16px (sm), 20px (md), 24px (lg)
- **Stroke**: 2px default

### Common Icons Used
```typescript
import {
  CheckCircle,      // Completed tasks
  Circle,           // Incomplete tasks
  Plus,             // Add new
  X,                // Close/delete
  Menu,             // Navigation
  Settings,         // Settings
  User,             // Profile
  LogOut,           // Logout
  Github,           // OAuth
  Sparkles,         // AI features
  Calendar,         // Due dates
  Tag               // Categories
} from 'lucide-react'
```

---

## 🎨 Usage Examples

### Task List Layout
```tsx
<div className="space-y-4 p-6">
  <TaskCard
    title="Complete project"
    priority="high"
    completed={false}
  />
</div>
```

### Form Layout
```tsx
<form className="space-y-6">
  <Input
    label="Task Title"
    placeholder="Enter task title..."
  />
  <Button variant="primary" size="md">
    Create Task
  </Button>
</form>
```

---

**Use this specification to maintain consistent design across the application!**
