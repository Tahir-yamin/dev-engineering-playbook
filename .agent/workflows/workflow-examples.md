# Evolution Agent - Application Management Examples

This document provides practical examples of how the Antigravity Agent manages the deployed application using the MCP Tool Hub.

## 🎯 Common Agent Workflows

### Example 1: Scaling the Frontend

**User Request**: "Scale the frontend to 3 replicas and tell me when it's ready"

**Agent Workflow**:

```
<thought>
User wants to scale the frontend deployment from 2 to 3 replicas.
I will:
1. Use scale_deployment to update the replica count
2. Use k8s_cluster_status to monitor the new pod
3. Confirm when all 3 pods are Running
</thought>

Scaling frontend deployment to 3 replicas...

[Calls scale_deployment with deployment_name="frontend", replicas=3]

✅ Deployment scaled successfully.

Verifying pod status...

[Calls k8s_cluster_status]

✅ All 3 frontend pods are now Running:
- frontend-deployment-abc123: Ready (1/1)
- frontend-deployment-def456: Ready (1/1)
- frontend-deployment-ghi789: Ready (1/1)

Frontend has been scaled to 3 replicas and all pods are healthy!
```

---

### Example 2: Debugging Backend Crash

**User Request**: "The backend keeps crashing, what's wrong?"

**Agent Workflow**:

```
<thought>
Backend is experiencing crashes. I need to:
1. Confirm which pod is affected
2. Check the recent logs for error messages
3. Verify database connectivity (common cause)
</thought>

Let me investigate the backend crash...

[Calls k8s_cluster_status]

⚠️ Found the issue: backend-deployment-xyz123 is in CrashLoopBackOff

Retrieving logs to diagnose...

[Calls analyze_pod_logs with pod_name="backend-deployment-xyz123", lines=50]

🔍 Error found in logs:
```
PrismaClientInitializationError: Can't reach database server at `db-service:5432`
```

Root cause: Database connection failed.

Let me verify the database...

[Calls db_query_stats]

✅ Database pod is healthy.

**Diagnosis**: The backend can't connect to the database. This could be a DNS resolution issue or timing problem during startup.

**Recommended fix**:
1. Restart the backend deployment to retry connection
2. Check if database was ready before backend started

Would you like me to restart the backend deployment?
```

---

### Example 3: Full Health Check

**User Request**: "Is everything running okay?"

**Agent Workflow**:

```
<thought>
User wants a comprehensive health check. I'll run the full diagnostic sweep.
</thought>

Running comprehensive health check...

[Calls health_check_full]

✅ **System Status: HEALTHY**

**Cluster Status**:
- Namespace: todo-chatbot
- Pods: 6 total
  - frontend-deployment (2/2): ✅ Running
  - backend-deployment (1/1): ✅ Running
  - postgres-0 (1/1): ✅ Running
- Restarts: 0 across all pods

**Database**:
- Status: ✅ Connected
- Latency: ~14ms
- Storage: 1Gi allocated, bound

**Services**:
- frontend-service: ✅ Accessible on NodePort 30000
- backend-service: ✅ ClusterIP active
- db-service: ✅ Headless service for StatefulSet

**Summary**: All systems operational. No issues detected.
```

---

### Example 4: Storage Monitoring

**User Request**: "Check if the database has enough disk space"

**Agent Workflow**:

```
<thought>
User is concerned about database storage. I'll check the PVC status and capacity.
</thought>

Checking database storage...

[Calls check_pvc_storage with pvc_name="postgres-pvc"]

✅ **Storage Status**:
- PVC Name: postgres-pvc
- Phase: Bound
- Requested: 1Gi
- Allocated: 1Gi
- Access Mode: ReadWriteOnce
- Volume: Successfully bound to physical storage

**Assessment**: Database has full 1Gi allocated and the PVC is healthy.

⚠️ **Note**: Kubernetes doesn't expose actual usage (how much of the 1Gi is used). 
To check actual database size, you would need to:
```bash
kubectl exec postgres-0 -n todo-chatbot -- du -sh /var/lib/postgresql/data
```

Would you like me to add a tool to check actual disk usage?
```

---

### Example 5: Performance Optimization

**User Request**: "The app feels slow, can you optimize it?"

**Agent Workflow**:

```
<thought>
User reports performance issues. I should:
1. Check cluster resource usage
2. Verify pod health
3. Check database latency
4. Suggest optimization strategies
</thought>

Analyzing performance...

[Calls health_check_full]

**Current Configuration**:
- Frontend: 2 replicas (256Mi memory, 250m CPU each)
- Backend: 1 replica (256Mi memory, 250m CPU)
- Database: 1 replica (512Mi memory, 500m CPU)

[Calls k8s_cluster_status]

**Findings**:
- All pods are healthy
- No restarts or crashes
- Resource limits are conservative

**Recommendations**:

1. **Scale Backend** (currently only 1 replica):
   ```
   I can scale backend to 2 replicas for better load distribution
   ```

2. **Increase Resource Limits** (if node has capacity):
   ```
   Backend memory: 256Mi → 512Mi
   Backend CPU: 250m → 500m
   ```

3. **Enable Horizontal Pod Autoscaling**:
   ```
   Auto-scale frontend between 2-5 replicas based on CPU
   ```

Would you like me to scale the backend to 2 replicas as a first step?
```

---

### Example 6: Disaster Recovery

**User Request**: "Emergency! Everything is down!"

**Agent Workflow**:

```
<thought>
Critical situation. I need to:
1. Assess overall cluster state
2. Identify which components are down
3. Prioritize recovery (database first, then backend, then frontend)
4. Execute recovery steps with user confirmation
</thought>

🚨 Running emergency diagnostics...

[Calls k8s_cluster_status]

**Status Report**:
❌ frontend-deployment: 0/2 pods Running (CrashLoopBackOff)
❌ backend-deployment: 0/1 pods Running (CrashLoopBackOff)
⚠️ postgres-0: 1/1 Running, but 5 restarts

**Recovery Plan**:

**Phase 1: Stabilize Database**
[Calls analyze_pod_logs pod_name="postgres-0"]
[Calls check_pvc_storage]

Database has restarted 5 times but PVC is intact.

**Phase 2: Restart Services in Order**
With your approval, I will:
1. ✅ Restart postgres (stateful, needs to be stable first)
2. ✅ Restart backend (depends on database)
3. ✅ Restart frontend (depends on backend)

**Shall I proceed with the recovery plan?**
```

---

## 🔧 Tool Usage Patterns

### Pattern: Monitor → Diagnose → Fix

```
1. k8s_cluster_status → "What's the current state?"
2. analyze_pod_logs → "Why is it failing?"
3. restart_deployment → "Apply the fix"
4. k8s_cluster_status → "Verify it worked"
```

### Pattern: Preventive Maintenance

```
1. health_check_full → Daily health check
2. check_pvc_storage → Weekly storage check
3. get_service_endpoints → Verify network config
```

### Pattern: Scaling Decision

```
1. k8s_cluster_status → Current replica count
2. [User decision based on load]
3. scale_deployment → Apply new replica count
4. k8s_cluster_status → Verify scale success
```

---

## 📊 Agent Success Metrics

The agent should track:
- ✅ **Uptime**: Percentage of time all pods are Running
- ✅ **Response Time**: How fast the agent detects and responds to issues
- ✅ **Self-Healing**: Number of issues resolved without human intervention
- ✅ **Prediction**: Proactive warnings before failures occur

---

**Version**: 1.0.0  
**Last Updated**: 2025-12-26
