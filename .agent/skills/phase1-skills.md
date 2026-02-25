# Phase 1 Skills - Project Foundation

**Phase**: 1 - Initial Setup
**Topics**: Project structure, database design, basic architecture
**Version**: 1.0

---

## Skill #1: Project Initialization

### When to Use
- Starting a new full-stack project
- Setting up monorepo structure
- Organizing frontend/backend separation

### Prompt Template

```markdown
**ROLE**: Senior Full-Stack Architect

**PROJECT TYPE**: [Web App / SaaS / API / etc]
**TECH STACK**: 
- Frontend: [Next.js / React / Vue]
- Backend: [FastAPI / Express / Django]
- Database: [PostgreSQL / MySQL / MongoDB]

**TASK**: Design optimal project structure

**DELIVERABLES**:
1. Directory structure with explanation
2. package.json / requirements.txt setup
3. Git repository initialization
4. .gitignore configuration
5. README.md template

**CONSTRAINTS**:
- Must support [monorepo / separate repos]
- Must include [Docker / K8s / etc]
```

---

## Skill #2: Database Schema Design

### When to Use
- Designing database for TODO/task management
- Creating relational data models
- Planning for scalability

### Prompt Template

```markdown
**ROLE**: Database architect

**APPLICATION**: TODO/Task Management System

**REQUIREMENTS**:
- Users with authentication
- Tasks with CRUD operations
- Categories/tags support
- Priority levels
- Due dates
- [Additional features]

**TASK**: Design complete database schema

**DELIVERABLES**:
1. Entity-Relationship Diagram (text/mermaid)
2. Table definitions with columns
3. Relationships and foreign keys
4. Indexes for performance
5. Sample SQL/Prisma schema

**CONSIDER**:
- Soft deletes vs hard deletes
- Timestamps (created_at, updated_at)
- User isolation (multi-tenant if needed)
```

---

## Skill #3: Technology Stack Selection

### When to Use
- Choosing between frameworks
- Deciding on frontend/backend combo
- Selecting database and ORM

### Prompt Template

```markdown
**ROLE**: Technical consultant

**PROJECT REQUIREMENTS**:
- Type: [SaaS / Internal tool / Public app]
- Scale: [MVP / Medium / Enterprise]
- Team: [Solo / Small / Large]
- Timeline: [Weeks / Months]

**CURRENT CONSIDERATIONS**:
Option 1: [e.g., Next.js + FastAPI + PostgreSQL]
Option 2: [e.g., React + Express + MongoDB]
Option 3: [Your alternative]

**ANALYZE**:
1. Pros/cons of each stack
2. Learning curve
3. Performance characteristics
4. Deployment complexity
5. Community support
6. Long-term maintenance

**RECOMMEND**: Best option with justification
```

---

## Skill #4: Git Workflow Setup

### When to Use
- Initializing version control
- Setting up branching strategy
- Configuring .gitignore

### Prompt Template

```markdown
**ROLE**: DevOps engineer

**PROJECT**: [Project name and type]
**TEAM SIZE**: [Solo / 2-5 / 5+]

**SETUP REQUIRED**:
1. .gitignore for [languages/frameworks]
2. Branch strategy (main, develop, feature branches)
3. Commit message conventions
4. PR/MR guidelines
5. Git hooks (optional)

**DELIVERABLES**:
- Complete .gitignore file
- Branching strategy document
- Git workflow commands
```

---

## Skill #5: Development Environment Setup

### When to Use
- Setting up local development
- Configuring VS Code / IDE
- Installing dependencies

### Prompt Template

```markdown
**ROLE**: Developer onboarding specialist

**STACK**:
- Frontend: [framework + version]
- Backend: [framework + version]
- Database: [type + version]

**PROVIDE**:
1. Prerequisites checklist (Node, Python, etc.)
2. Step-by-step installation guide
3. VS Code extensions recommended
4. Local development commands
5. How to verify setup works
6. Common setup issues + fixes

**OS**: [Windows / Mac / Linux]
```

---

## Quick Reference: Phase 1 Checklist

### Project Setup
- [ ] Choose technology stack
- [ ] Design database schema
- [ ] Create project structure
- [ ] Initialize Git repository
- [ ] Set up .gitignore
- [ ] Create README.md

### Development Environment
- [ ] Install prerequisites
- [ ] Set up IDE/editor
- [ ] Install dependencies
- [ ] Configure linters/formatters
- [ ] Test basic workflow

### Documentation
- [ ] Architecture overview
- [ ] Setup instructions
- [ ] Development workflow
- [ ] Contributing guidelines

---

## Common Phase 1 Issues

### Issue: "Should I use monorepo or separate repos?"

**Answer**: 
- **Monorepo** if:
  - Small team (1-5 developers)
  - Shared code/types between frontend/backend
  - Want simplified deployment
  
- **Separate repos** if:
  - Large team with specialized roles
  - Different release cycles
  - Independent scaling needs

### Issue: "Which database should I choose?"

**PostgreSQL** for:
- Complex queries
- Relational data
- ACID compliance
- ✅ Recommended for this TODO app

**MongoDB** for:
- Flexible schema
- Document storage
- Rapid prototyping

### Issue: "Prisma vs raw SQL?"

**Use Prisma** (✅ Our choice):
- Type safety with TypeScript
- Auto-generated client
- Easy migrations
- Great DX (Developer Experience)

---

##Lessons Learned - Phase 1

1. **Start with good structure** - Hard to refactor later
2. **Document early** - README and setup docs save time
3. **Use TypeScript** - Catches errors early
4. **Plan schema carefully** - Database migrations are painful
5. **Set up linting early** - Consistent code style matters

---

## Related Skills

- Phase 2: Implementation and API development
- Database Skills: Prisma setup and migrations
- Environment Skills: Local development configuration

---

**Next Phase**: Once foundation is solid, move to Phase 2 for full-stack implementation!
