# Quick Start Commands

## Step 1: Install Backend Dependencies
```bash
cd "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\backend"
pip install -r requirements.txt
```

## Step 2: Install Frontend Dependencies
```bash
cd "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\frontend"
npm install
```

## Step 3: Start Backend (Terminal 1)
```bash
cd "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\backend"
python main.py
```

## Step 4: Start Frontend (Terminal 2 - New Window)
```bash
cd "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\frontend"
npm run dev
```

## Step 5: Test the App
Open browser: http://localhost:3001/auth

---

## Troubleshooting

### If you get "ModuleNotFoundError":
```bash
cd backend
pip install -r requirements.txt
```

### If you get npm errors:
```bash
cd frontend
npm install
```

### If ports are already in use:
- Backend: Change port in `backend/main.py` (line with `uvicorn.run`)
- Frontend: Use `npm run dev -- -p 3002` for different port
