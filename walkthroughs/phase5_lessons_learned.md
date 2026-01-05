# Phase 5 Lessons Learned: Troubleshooting & Fixes

This document captures critical issues encountered during Phase 5 implementation and their resolutions.

---

## 1. Dapr Installation on Windows (Manual Fix)
> [!IMPORTANT]
> **Issue**: `dapr init` often stalls or fails on Windows due to network timeouts when downloading the `daprd` binary.
> **Error**: `error downloading daprd binary: stream stalled`

### **Resolution**:
1. **Manual Download**: Download the binaries directly from GitHub Releases.
2. **Directory Structure**: Create the expected Dapr bin directory:
   `mkdir -p $env:USERPROFILE\.dapr\bin`
3. **Placement**: Move `daprd.exe`, `placement.exe`, and `scheduler.exe` into that directory.
4. **Verification**: `dapr run` will now find the binaries without needing a successful `dapr init`.

---

## 2. Database Connectivity (`sslmode` Fallback)
> [!WARNING]
> **Issue**: NeonDB requires `sslmode=require`, but some local Python drivers (like `sqlite` or certain `psycopg2` versions) crash when this argument is passed.
> **Error**: `Connection() got an unexpected keyword argument 'sslmode'`

### **Resolution**:
Implement a try-except block in `db.py` to attempt SSL first, then fallback to a standard connection for local testing:
```python
try:
    engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})
except TypeError:
    engine = create_engine(DATABASE_URL)
```

---

## 3. FastAPI Module Import Consistency
> [!NOTE]
> **Issue**: Confusion between `uvicorn app:app` and `uvicorn main:app`.
> **Error**: `Could not import module "app"`

### **Resolution**:
Always check the filename. In this project, the entry point is `main.py`, so the command must be:
`python -m uvicorn main:app`

---

## 4. Dapr Runtime Dependencies
> [!CAUTION]
> **Issue**: `dapr run` fails if the `placement` and `scheduler` services aren't running.
> **Error**: `Failed to connect to scheduler host`

### **Resolution**:
For local development without Docker, start these services manually in separate background processes:
```powershell
Start-Process -FilePath "$env:USERPROFILE\.dapr\bin\placement.exe" -ArgumentList "--port 50005" -NoNewWindow
Start-Process -FilePath "$env:USERPROFILE\.dapr\bin\scheduler.exe" -ArgumentList "--port 17702" -NoNewWindow
```

---

## 5. Kafka Component Resolution
> [!TIP]
> **Issue**: Dapr components configured for Kubernetes (using service names like `kafka-cluster-kafka-bootstrap`) won't resolve locally.
> **Insight**: This is expected behavior. Local verification should focus on **logic** (using `test_phase5.py`) while full integration is reserved for the AKS environment.
