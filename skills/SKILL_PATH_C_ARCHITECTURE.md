# 🏗️ Path C: Enterprise Architecture

**Goal**: Design systems that handle millions of users and complex domains.
**Timeline**: 2025 Q3-Q4

---

## 1. Event-Driven Architecture
Decouple your services for scalability.

- **Tools**: Apache Kafka, RabbitMQ, NATS

### 🔬 Micro-Skills
1.  **Idempotency Handling**:
    -   *Skill*: Designing consumers that can process the same message twice safely.
    -   *Test*: Send the "Add XP" event 5 times for the same Task ID. The user should only get XP once.
2.  **Schema Evolution**:
    -   *Skill*: Adding a field to an event without breaking old consumers.
    -   *Test*: Add `bonus_xp` to the event and ensure the old consumer still works.
3.  **Dead Letter Queues (DLQ)**:
    -   *Skill*: Handling "poison pills" (messages that crash the consumer).
    -   *Test*: Send a malformed JSON and verify it moves to the DLQ after 3 retries.

### 🛠️ Workflow: Event-Driven Gamification
1.  **Define Event**: Create a `TaskCompleted` event schema (Protobuf or JSON).
2.  **Publish**: In `backend/tasks.py`, publish the event to `pubsub` topic after DB commit.
3.  **Consume**: Create a new `gamification-service` that subscribes to `pubsub`.
4.  **Process**: When event arrives, calculate XP and update User stats.

### Recommended Repos
- `dotnet-architecture/eShopOnDapr`

---

## 2. Microservices Patterns & Dapr
Simplify distributed system complexity.

- **Tools**: Dapr (Distributed Application Runtime)

### 🔬 Micro-Skills
1.  **Sidecar Pattern Debugging**:
    -   *Skill*: Understanding how the app talks to the sidecar (localhost:3500).
    -   *Test*: Use `curl` to call the Dapr sidecar's API directly to invoke a method.
2.  **State Management Abstraction**:
    -   *Skill*: Switching state stores (Redis -> CosmosDB) without changing code.
    -   *Test*: Change the Dapr component YAML and restart. The app should still work.
3.  **Resiliency Policies**:
    -   *Skill*: Configuring retries and circuit breakers in YAML.
    -   *Test*: Kill the database and see Dapr retry the connection 3 times before failing.

### 🛠️ Workflow: Dapr Integration
1.  **Install**: Add Dapr to your K8s cluster (`dapr init -k`).
2.  **Inject**: Add `dapr.io/enabled: "true"` annotation to your Deployment.
3.  **State Store**: Refactor `backend/db.py` to use Dapr SDK for KV storage.
4.  **Verify**: Check the Dapr dashboard to see the service map.

### Recommended Repos
- `dapr/dapr`

---

## 3. System Design
The theory behind the practice.

- **Resources**: "System Design Primer", "ByteByteGo"
- **Key Concepts**:
    - **Caching**: Write-through vs Look-aside strategies.
    - **Sharding**: Splitting one big DB into smaller pieces.
    - **CAP Theorem**: Consistency vs Availability vs Partition Tolerance.

### Learning Project
1. **Diagram**: Draw the C4 model for your current Todo App.
2. **Case Study**: Read "Design Twitter" and explain how you'd build the news feed.

### Recommended Repos
- `donnemartin/system-design-primer`
