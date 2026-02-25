# 90-Second Demo Video Script & Production Guide

**Due**: Before January 4, 2026 submission  
**Maximum Length**: 90 seconds (judges only watch first 90 seconds)  
**Purpose**: Showcase Phase IV Kubernetes deployment and AI chatbot functionality

---

## Video Requirements (From Hackathon Specs)

✅ **Must Include**:
1. Docker image build process
2. Kubernetes deployment (Helm)
3. Application accessibility verification
4. AI chatbot functionality demonstration
5. Task management operations

✅ **Format**:
- MP4 or similar standard format
- 1080p recommended
- Clear audio (if narrated)
- Shareable link (YouTube, Google Drive, etc.)

---

## Recommended Tools

### Screen Recording
- **Windows**: OBS Studio (Free), Camtasia (Paid), Windows Game Bar (Built-in)
- **Cross-platform**: Loom (Free tier), ScreenFlow (Mac)
- **Quick**: NotebookLM (mentioned in hackathon requirements)

### Video Editing
- **Simple**: Clipchamp (Free, Windows built-in)
- **Advanced**: DaVinci Resolve (Free), Adobe Premiere
- **Online**: Kapwing, VEED.io

### AI Narration (Optional)
- **NotebookLM**: AI-generated audio podcast from docs
- **ElevenLabs**: AI voice narration
- **Manual**: Record your own narration

---

## 90-Second Script Breakdown

### Timing Overview

| Section | Time | Content |
|---------|------|---------|
| Intro | 0-10s | Project overview |
| Build | 10-25s | Docker image build |
| Deploy | 25-40s | Helm deployment |
| Demo | 40-75s | Application features |
| Outro | 75-90s | Wrap-up & tech stack |

---

## Detailed Script with Visuals

### Section 1: Introduction (0-10 seconds)

**Visual**: Title slide or README.md on screen

**Narration**:
> "Evolution of Todo - Phase 4: A Cloud-Native AI Chatbot deployed on Kubernetes. Here's how it works in 90 seconds."

**On-Screen Text**:
```
Evolution of Todo - Phase IV
Cloud-Native AI Chatbot
Kubernetes | Docker | Helm
```

**Tips**:
- Keep it punchy
- Show project structure briefly
- Transition quickly

---

### Section 2: Docker Build (10-25 seconds)

**Visual**: Terminal showing Docker build commands

**Narration**:
> "First, we containerize the application. Multi-stage Docker builds optimize image size - frontend at 485MB, backend at 245MB."

**Commands to Show** (Speed up video 2-3x):
```powershell
# Show this command executing
docker build -t todo-frontend:v2 -f phase4/docker/frontend.Dockerfile phase2/frontend

# Show build stages flashing by (sped up)
# Final line should show:
Successfully built abc123def
Successfully tagged todo-frontend:v2

# Quick second command
docker build -t todo-backend:v1 -f phase4/docker/backend.Dockerfile phase2/backend
```

**On-Screen Text** (while building):
```
✓ Multi-stage builds
✓ Production optimized
✓ Health checks configured
```

**Timing**: 15 seconds total
- 5s narration
- 10s build demo (sped up)

---

### Section 3: Helm Deployment (25-40 seconds)

**Visual**: Terminal showing Helm deployment + kubectl verification

**Narration**:
> "Deployment is simple with Helm charts. One command deploys frontend, backend, and all configurations to Kubernetes."

**Commands to Show**:
```powershell
# Deploy with Helm (show command typing)
helm install todo-chatbot phase4/helm/todo-chatbot -n todo-chatbot --create-namespace

# Show output scrolling (sped up):
# NAME: todo-chatbot
# LAST DEPLOYED: ...
# STATUS: deployed

# Verify pods (show this real-time)
kubectl get pods -n todo-chatbot

# Output should show:
# NAME                               READY   STATUS
# todo-app-frontend-xxx             2/2     Running
# todo-app-backend-yyy              1/1     Running
```

**On-Screen Text**:
```
✓ Helm for version control
✓ 2 Frontend replicas (HA)
✓ 1 Backend replica
✓ External NeonDB
```

**Timing**: 15 seconds
- 5s Helm install
- 5s pod verification
- 5s narration

---

### Section 4: Application Demo (40-75 seconds) - **MOST IMPORTANT**

**Visual**: Split-screen: Browser + Terminal/Logs

#### Part A: Access Verification (40-50s)

**Narration**:
> "The application is now live. Frontend on port 30000, backend API on 30001."

**Visual**:
- Browser navigating to `http://localhost:30000`
- Show frontend loading
- Show clean UI

**On-Screen Text**:
```
Frontend: http://localhost:30000 ✓
Backend: http://localhost:30001 ✓
```

#### Part B: AI Chatbot Demo (50-70s)

**This is the star - spend most time here!**

**Narration**:
> "The AI chatbot manages tasks through natural language. Watch this..."

**Visual**: Focus on AI chat interface

**Actions** (pre-recorded, smooth demo):
```
User types: "Add a task to prepare demo video"

AI responds: "I've created a new task: 'Prepare demo video'"
[Show task appearing in UI]

User types: "Show me all my tasks"

AI responds: "You have 3 tasks: ..."
[Show task list in UI]

User types: "Mark the demo video task as complete"

AI responds: "Great! I've marked 'Prepare demo video' as complete"
[Show task status changing to completed with animation]
```

**On-Screen Text** (overlay while demo runs):
```
✓ Natural language processing
✓ OpenRouter AI integration
✓ MCP tool architecture
✓ Real-time task management
```

**Timing**: 20 seconds
- 5s chatbot explanation
- 15s live demo

#### Part C: Features Showcase (70-75s)

**Visual**: Quick montage

- Create task via UI (2s)
- Delete task (1s)
- Filter tasks by status (2s)

**No narration needed** - just visual demonstration

---

### Section 5: Outro (75-90 seconds)

**Visual**: Technology stack slide or architecture diagram

**Narration**:
> "Built with Next.js, FastAPI, NeonDB, and Kubernetes. Deployed locally with Helm, production-ready for cloud. Phase 4 complete."

**On-Screen Text**:
```
Tech Stack:
━━━━━━━━━━━━━━━━━━━━━━
Frontend: Next.js 14
Backend: FastAPI + SQLModel
Database: NeonDB (Serverless PostgreSQL)
AI: OpenRouter + OpenAI Agents SDK
Deployment: Kubernetes + Helm
Container: Docker Desktop

GitHub: [Your Repo URL]
Demo: Phase IV - Kubernetes Deployment
```

**Timing**: 15 seconds

---

## Pre-Production Checklist

### Before Recording

- [ ] **Clean Up Environment**
  - Close unnecessary browser tabs
  - Clear terminal history
  - Hide sensitive information
  - Use incognito/private browser

- [ ] **Prepare Demo Data**
  - Create 2-3 sample tasks
  - Test AI chatbot responses
  - Ensure all features work smoothly

- [ ] **Test Run**
  - Record a practice run
  - Check timing (must be under 90s!)
  - Verify audio quality
  - Check screen resolution

- [ ] **Prepare Terminal**
  - Increase font size for readability
  - Use clear color scheme
  - Pre-type commands in a script (if needed)

---

## Recording Tips

### Visual Quality

1. **Resolution**: 1920x1080 (1080p) minimum
2. **Frame Rate**: 30 FPS minimum
3. **Screen Area**: Full screen or focused application window
4. **Cursor**: Make cursor visible and easy to follow

### Audio Quality

1. **Background Noise**: Record in quiet environment
2. **Microphone**: Use external mic if possible
3. **Volume**: Clear and consistent
4. **Pacing**: Speak clearly, not too fast

### Editing

1. **Speed Up Builds**: 2-3x speed for Docker/Helm operations
2. **Transitions**: Smooth cuts between sections
3. **Text Overlays**: Add key points as on-screen text
4. **Music**: Optional, light background music (royalty-free)

---

## Alternative Approach: Slide-Based with Voiceover

**If live demo is difficult**:

### Slide Script (7-9 slides, 10s each)

1. **Title Slide**: Project name + overview
2. **Architecture**: Simple diagram of system
3. **Docker Build**: Screenshot of build output
4. **Helm Deploy**: Screenshot of deployment
5. **Frontend**: Screenshot of UI
6. **AI Chat**: Screenshot of chatbot conversation
7. **Task Management**: Screenshot of CRUD operations
8. **Tech Stack**: List of technologies
9. **Outro**: GitHub link + thank you

**Tool**: PowerPoint/Google Slides + Loom/OBS for recording

---

## NotebookLM Approach (Easiest)

### Using NotebookLM for AI-Generated Audio

1. Upload your documentation to NotebookLM:
   - `README.md`
   - `CLAUDE.md`
   - `MANUAL-OPERATIONS-GUIDE.md`
   - `DEPLOYMENT-STATUS.md`

2. Generate Audio Overview:
   - NotebookLM creates a podcast-style discussion
   - Two AI hosts discuss your project
   - Automatically generated, engaging

3. Add Visuals:
   - Use the AI audio as background
   - Layer screenshots/screen recordings on top
   - Sync visuals with audio narrative

**Pros**: 
- No recording your own voice
- Professional-sounding
- Engaging format

**Cons**:
- Less control over exact script
- Need to time visuals to audio

---

## Post-Production

### Final Checks

- [ ] **Length**: Exactly 90 seconds or less
- [ ] **Quality**: Clear video and audio
- [ ] **Content**: All required elements included
- [ ] **Branding**: Project name visible
- [ ] **Links**: GitHub repo shown at end

### Export Settings

**Recommended**:
- Format: MP4 (H.264)
- Resolution: 1920x1080 (1080p)
- Frame Rate: 30 FPS
- Bitrate: 8-10 Mbps (good quality without huge file)

### Upload Options

1. **YouTube** (Recommended)
   - Upload as "unlisted" (shareable link only)
   - Add to playlist if multiple submissions
   - Easy embedding for judges

2. **Google Drive**
   - Upload MP4
   - Set sharing to "Anyone with link can view"
   - Copy shareable link

3. **Vimeo**
   - Professional platform
   - Good video quality
   - Privacy settings available

---

## Example Storyboard

```
[00:00-00:10] ━━━━━━━━━ Title + Overview
           Visual: Title slide with tech logos
           Audio: Project introduction

[00:10-00:25] ━━━━━━━━━ Docker Build
           Visual: Terminal with docker build commands
           Audio: "Multi-stage builds optimize..."
           On-screen: Size optimization stats

[00:25-00:40] ━━━━━━━━━ Helm Deployment
           Visual: helm install + kubectl get pods
           Audio: "One command deploys everything..."
           On-screen: Pod status checkmarks

[00:40-00:50] ━━━━━━━━━ Access Verification
           Visual: Browser opening localhost:30000
           Audio: "Application is live..."
           On-screen: URL + Port info

[00:50-00:70] ━━━━━━━━━ AI Chatbot Demo ⭐
           Visual: Split screen - chat + task list
           Audio: "AI manages tasks through natural language..."
           On-screen: Feature callouts

[00:70-00:90] ━━━━━━━━━ Tech Stack + Outro
           Visual: Architecture diagram or stack list
           Audio: "Built with Next.js, FastAPI..."
           On-screen: GitHub link
```

---

## Time-Saving Tips

### Quick Production (2 hours)

1. **Use Template** (30 min)
   - Find a tech demo template
   - Customize with your content

2. **Record in One Take** (30 min)
   - Script every word
   - Practice once
   - Record twice, keep best

3. **Minimal Editing** (45 min)
   - Trim start/end
   - Add title slide
   - Add outro slide
   - Export

4. **Upload & Submit** (15 min)

**Total**: 2 hours for basic professional demo

---

## Common Mistakes to Avoid

❌ **Don't**:
- Go over 90 seconds (judges stop watching!)
- Show errors or failures
- Include sensitive credentials
- Use tiny fonts (unreadable)
- Ramble or move too slowly
- Forget to show AI chatbot (it's the highlight!)

✅ **Do**:
- Time everything precisely
- Show smooth, rehearsed demo
- Use clear, large fonts
- Keep pace brisk
- Highlight unique features (AI!)
- End with strong call-to-action

---

## Checklist Before Submission

- [ ] Video is 90 seconds or less
- [ ] All required elements shown (Docker, Helm, K8s, AI, Tasks)
- [ ] Audio is clear and audible
- [ ] Video quality is 1080p
- [ ] No sensitive information visible
- [ ] GitHub repo link included
- [ ] Uploaded to stable platform (YouTube/Drive)
- [ ] Link is publicly accessible
- [ ] Link tested in incognito mode
- [ ] Link added to submission form

---

## Optional Enhancements (If Time Permits)

- **Background Music**: Upbeat, tech-themed (royalty-free from YouTube Audio Library)
- **Captions**: Add subtitles for accessibility
- **Animations**: Smooth transitions between sections
- **Picture-in-Picture**: Show yourself in corner (builds trust)
- **Branding**: Consistent color scheme matching project theme

---

**Priority**: 🔴 **CRITICAL** - Required for submission  
**Time Investment**: 2-4 hours (depending on approach)  
**Impact**: First impression for judges - make it count!  
**Deadline**: Submit with Phase IV before January 4, 2026
