# Reference Documentation Index

**Project**: TODO Hackathon  
**Purpose**: Organized reference for all tools, features, and components  
**Last Updated**: December 29, 2025

---

## 📚 What's in Reference/

This folder contains detailed documentation for every tool, feature, and component created during this project. Unlike skills (which tell you HOW), these documents tell you WHAT and WHY.

---

## 📁 Reference Documents

### 1. [Tools & Scripts](./tools-and-scripts.md)
**What**: Documentation for all custom scripts and utilities

**Covers**:
- `validate-env.ps1` - Environment validation
- `migrate-secrets.ps1` - Secret migration
- PowerShell patterns and best practices
- Future script ideas

**When to Use**:
- Understanding what scripts do
- Learning how to create new scripts
- Troubleshooting script issues

---

### 2. [Features Implementation](./features-implementation.md)
**What**: Complete guide to all features implemented

**Covers**:
- Authentication (Better Auth, OAuth, Sessions)
- Task Management (CRUD operations)
- AI Features (Chat, Suggestions)
- UI/UX (Dark Mode, Responsive Design)
- Docker & Deployment
- Performance Optimizations

**Total Features**: 15+ major features documented

**When to Use**:
- Understanding how a feature works
- Learning implementation patterns
- Seeing lessons learned
- Planning similar features

---

### 3. [Components Library](./components-library.md)
**What**: Catalog of all React components created

**Covers**:
- Core Components (TaskList, TaskCard, TaskForm)
- UI Base Components (Button, Input, Modal)
- Feature Components (Header, ThemeToggle, AIChat)
- Props, usage, and styling for each

**Total Components**: 13+ documented

**When to Use**:
- Finding a component to reuse
- Understanding component props
- Learning React patterns
- Building new features

---

## 🎯 How to Use Reference Docs

### Scenario 1: "How does [feature] work?"
```
1. Open features-implementation.md
2. Find the feature in the table of contents
3. Read implementation details
4. Check code examples
5. Review lessons learned
```

### Scenario 2: "What components are available?"
```
1. Open components-library.md
2. Browse by category
3. Check props and usage
4. Copy example code
```

### Scenario 3: "What does [script] do?"
```
1. Open tools-and-scripts.md
2. Find the script
3. Read what it does
4. See usage examples
5. Check related documentation
```

---

## 🔗 How Reference Relates to Other Docs

### Reference vs Skills
|  | Reference | Skills |
|---|---|---|
| **Purpose** | WHAT & WHY | HOW |
| **Content** | Features, components, tools | Prompt templates, patterns |
| **Use Case** | Understanding | Asking AI for help |
| **Example** | "Better Auth integrat ion details" | "Help me fix CSRF error" |

### Reference vs Workflows
|  | Reference | Workflows |
|---|---|---|
| **Purpose** | Documentation | Step-by-step guides |
| **Content** | Implementation details | Procedures |
| **Use Case** | Learning | Doing |
| **Example** | "How AIChat works" | "How to add new feature" |

---

## 📊 Documentation Hierarchy

```
.claude/
├── skills.md                    # Skills index (HOW to ask AI)
├── rules/
│   └── project-guide.md         # Project overview
├── reference/                   # ← YOU ARE HERE
│   ├── README.md               # This file
│   ├── tools-and-scripts.md   # Scripts documentation
│   ├── features-implementation.md  # Features documentation
│   └── components-library.md  # Components documentation
│
.agent/workflows/               # Step-by-step procedures
.specify/                       # Design system
.history/prompts/              # Successful prompts
```

---

## 💡 Quick Lookup

### "I need to understand..."

| Topic | Reference Doc |
|-------|--------------|
| validate-env.ps1 script | tools-and-scripts.md #1 |
| migrate-secrets.ps1 script | tools-and-scripts.md #2 |
| Better Auth setup | features-implementation.md #1 |
| GitHub OAuth | features-implementation.md #2 |
| Task CRUD | features-implementation.md #4-7 |
| AI Chat | features-implementation.md #8 |
| Dark Mode | features-implementation.md #10 |
| Docker Setup | features-implementation.md #13 |
| TaskList component | components-library.md (Core) |
| Button component | components-library.md (UI Base) |
| Modal component | components-library.md (UI Base) |
| Header component | components-library.md (Feature) |

---

## 🎯 Reference Documentation Goals

### What Reference Docs Provide
✅ **Complete understanding** of what was built  
✅ **Implementation details** with code examples  
✅ **Lessons learned** from building it  
✅ **Props and usage** for components  
✅ **Environment variables** needed  
✅ **Related documentation** links  

### What Reference Docs Don't Cover
❌ Step-by-step troubleshooting → Use workflows  
❌ AI prompt templates → Use skills  
❌ Project setup → Use project guide  
❌ Design tokens → Use design system  

---

## 📝 Maintaining Reference Docs

### When to Update

**Add to tools-and-scripts.md**:
- Created a new script
- Modified existing script significantly
- Learned new script patterns

**Add to features-implementation.md**:
- Implemented new feature
- Modified existing feature significantly
- Learned lessons about feature

**Add to components-library.md**:
- Created new component
- Significantly refactored component
- Added new component variant

### How to Update

Use the documentation-maintenance workflow:
```
/documentation-maintenance

I [created/modified] [script/feature/component]
Help me update the reference docs
```

The workflow will Guide you to the right file and section.

---

## 🎓 Learning Paths

### Path 1: New Developer
1. Read `project-guide.md` (big picture)
2. Skim `features-implementation.md` (what exists)
3. Browse `components-library.md` (UI building blocks)
4. Reference `tools-and-scripts.md` (utilities available)

### Path 2: Adding Feature
1. Check `features-implementation.md` (similar features?)
2. Review `components-library.md` (reusable components?)
3. Check `tools-and-scripts.md` (helpful scripts?)
4. Follow `/adding-new-feature` workflow

### Path 3: Understanding Codebase
1. Start with `features-implementation.md`
2. For UI: Dive into `components-library.md`
3. For tooling: Check `tools-and-scripts.md`
4. For patterns: See lessons learned in each

---

## 🌟 Best Practices

### Using Reference Docs
✅ **Read first** before asking AI  
✅ **Link to sections** when asking for help  
✅ **Copy code examples** as starting points  
✅ **Learn from lessons** to avoid mistakes  
✅ **Cross-reference** related docs  

### Example Usage with AI
```
@.claude/reference/features-implementation.md

I read about the AI Chat feature (section #8).
I want to add streaming responses.
Help me implement this using the existing pattern.
```

---

## 🔗 Related Documentation

- **Project Overview**: `.claude/rules/project-guide.md`
- **Skills Library**: `.claude/skills.md`
- **Workflows**: `.agent/workflows/README.md`
- **Design System**: `.specify/design-system.md`
- **Successful Prompts**: `.history/prompts/successful-prompts.md`

---

**Everything you built, documented and organized!** 🎉

**Use these references to understand the past and build the future.**
