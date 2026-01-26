# Units: Workspace Dashboard

## 1. Decomposition Strategy
The system is simple enough to be contained in a single deployable unit.

## 2. Unit List

### Unit 001: Dashboard Web App (`001-dashboard-web-app`)
- **Type**: Frontend Application (Next.js)
- **Responsibility**: Hosting the UI and reading local files.
- **Dependencies**: Node.js `fs` module (server-side only).
- **Deployment**: Localhost (dev mode or build).
