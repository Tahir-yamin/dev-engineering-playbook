# Phase 5 Pre-AKS Testing Guide

Follow these steps to verify Phase 5 functionality on your local machine before proceeding to the Azure AKS deployment.

---

## Step 1: Logic Verification (The "Gold Standard")
Run the comprehensive test suite to verify all Phase 5 logic (MCP, Events, Datetime).

```powershell
cd "phase2/backend"
python test_phase5.py
```
**What to look for**: `7/7 tests passed!`

---

## Step 2: Backend Health Check
Start the backend standalone to verify database connectivity and the `sslmode` fix.

```powershell
cd "phase2/backend"
python -m uvicorn main:app --port 8000
```
**Verify**: Open `http://localhost:8000/health` in your browser. You should see `{"status": "healthy"}`.

---

## Step 3: Notification Service Check
Verify the new microservice starts correctly.

```powershell
cd "phase4/services/notification-service"
python -m uvicorn main:app --port 8001
```
**Verify**: Open `http://localhost:8001/dapr/subscribe`. You should see the JSON list of Kafka topic subscriptions.

---

## Step 4: MCP Discovery
Verify the Antigravity agent can "see" the new Phase 5 tools.

```powershell
# In your browser or via curl
curl http://localhost:8000/agent/tools
```
**Verify**: Check that `set_reminder` is in the list of tools.

---

## Step 5: CI/CD Dry Run
Check the GitHub Actions workflow for syntax errors.

1. Go to your GitHub repository.
2. Click on the **Actions** tab.
3. Select **Deploy to Azure AKS**.
4. Click **Run workflow** (even if it fails due to missing secrets, it verifies the YAML structure).

---

## 🎥 Demo Video Checklist
When recording your demo, show these three things:
1. **The Test Suite**: Running `test_phase5.py` with all greens.
2. **The New Tool**: Asking the agent to "Set a reminder for my task" and showing the success message.
3. **The Notification Service**: Showing the logs of the service starting up and subscribing to topics.
