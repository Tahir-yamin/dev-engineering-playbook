# Evolution of Todo 🚀 (Hackathon II Submission)

**A Cloud-Native, AI-Agentic Task Manager built with Spec-Driven Development.**

## 🌟 The Vision
We moved beyond simple CRUD. This application features an **AI Agent** that lives inside your dashboard, understanding context and manipulating the database directly via MCP Tools, synced instantly with a reactive UI.

## 🏗️ Tech Stack (The "Clean Slate" Architecture)
* **Frontend:** Next.js 14 (App Router) + Tailwind CSS + Framer Motion (3D Visuals)
* **Backend:** Python FastAPI (REST API + AI Agent)
* **Database:** Neon Serverless PostgreSQL
* **ORM:** Prisma v5 (Stable)
* **Authentication:** BetterAuth with Prisma Adapter (GitHub SSO + Email Verification)
* **AI Engine:** Anthropic/OpenAI via MCP (Model Context Protocol)

## ✨ Key Features
1. **Event-Driven UI Sync:** Chat with the AI ("Add a task to buy milk"), and the Kanban board updates *instantly* without a page refresh.
2. **Secure Authentication:**
   * OAuth 2.0 (GitHub)
   * Mandatory Email Verification (with Dev-Interceptor for hackathon demoing)
3. **Floating 3D Command Center:** A "World Class" glassmorphic landing page.
4. **Spec-Driven Development:** Built following the `Specify -> Plan -> Task -> Implement` cycle.

## 🛠️ Local Setup

### Prerequisites
* Node.js v20+
* Python 3.10+
* PostgreSQL URL (Neon or Local)

### 1. Backend (FastAPI)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8002
```

### 2. Frontend (Next.js)
```bash
cd frontend
# Important: Use Prisma v5 for stability
npm install
npx prisma generate
npx dotenv-cli -e .env.local -- npx prisma db push
npm run dev
```

### 3. Environment Variables
Create `.env.local` in the frontend directory:
```env
DATABASE_URL=your_neon_postgresql_url
BETTER_AUTH_SECRET=your_secret_key
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
NEXT_PUBLIC_APP_URL=http://localhost:3002
NEXT_PUBLIC_API_URL=http://localhost:8002
```

## 🧪 Lessons Learned
See `docs/lessons-learned-sso-auth.md` for a deep dive into how we solved the critical "Silent 500 Error" crash during the hackathon.

## 🎯 Demo Highlights

**Authentication Flow:**
- 2 methods: GitHub OAuth, Email/Password
- Mandatory email verification prevents spam accounts
- Terminal fallback for testing (production uses Resend)

**AI Integration:**
- Natural language task creation
- Instant UI sync via global event bus
- Context-aware task management

**UI/UX:**
- Glassmorphic design with animated backgrounds
- Framer Motion 3D effects
- Responsive Kanban board with drag-and-drop

## 🙏 Credits & Acknowledgments

### **Core Technologies**
- [**Next.js**](https://nextjs.org) by [@vercel](https://github.com/vercel) - React framework  
- [**FastAPI**](https://fastapi.tiangolo.com/) by [@tiangolo](https://github.com/tiangolo) - Python backend framework  
- [**BetterAuth**](https://www.better-auth.com/) by [@better-auth](https://github.com/better-auth/better-auth) - Authentication library that made OAuth possible  
- [**Prisma**](https://www.prisma.io/) by [@prisma](https://github.com/prisma/prisma) - Database ORM (v5.21.1)

### **Hosting & Infrastructure**
- [**Vercel**](https://vercel.com) - Frontend deployment platform  
- [**Railway**](https://railway.app) - Backend deployment platform  
- [**Neon**](https://neon.tech) - Serverless PostgreSQL database

### **UI & Styling**
- [**Tailwind CSS**](https://tailwindcss.com) - Utility-first CSS framework  
- [**Framer Motion**](https://www.framer.com/motion/) - Animation library  
- [**Lucide Icons**](https://lucide.dev) - Beautiful icon set

### **Authentication Providers**
- [**GitHub OAuth**](https://docs.github.com/en/developers/apps/building-oauth-apps) - SSO provider  
- [**Resend**](https://resend.com) - Email delivery service

### **AI & Tools**
- [**OpenAI**](https://openai.com) - AI model provider  
- [**Anthropic Claude**](https://claude.ai) by [@anthropic-ai](https://github.com/anthropic-ai) - AI pair programming assistant for development

### **Special Thanks**
This project was built with inspiration and learning from the open-source community. While we implemented our own solution, we studied best practices from various authentication implementations in the ecosystem.

**Bug Reports & Community Support:**
- BetterAuth Discord community for OAuth debugging help
- Prisma GitHub issues for version compatibility insights
- Vercel documentation and community forums
- Railway community support

---

*Built for the Agentic AI Hackathon 2025.*  
*Survived 12+ hours of OAuth debugging to emerge stronger.* 💪

**Live Demo:** https://frontend-seven-tawny-19.vercel.app  
**Documentation:** See `/docs` folder for detailed implementation guides and lessons learned
