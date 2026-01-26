# Bolt Plan: Workspace Dashboard

**Intent**: `001-workspace-dashboard`

## Execution Strategy
We will execute this in 2 sequential bolts.

### Bolt 1: Project Scaffold (`001-scaffold`)
- **Unit**: `001-dashboard-web-app`
- **Goal**: Initialize Next.js app and basic UI shell.
- **Stories Covered**: None (Enabler).
- **Output**: Working `localhost:3000` with a Homepage.

### Bolt 2: Core Features (`002-core-features`)
- **Unit**: `001-dashboard-web-app`
- **Goal**: Implement file reading and list views.
- **Stories Covered**:
    - `001-view-workflows`
    - `002-view-rules`
- **Output**: Fully functional dashboard.
