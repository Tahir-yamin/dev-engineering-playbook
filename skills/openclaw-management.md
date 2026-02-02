# OpenClaw Management Skills

**Purpose**: Best practices for setting up, optimizing, and securing OpenClaw in local-first environments (WSL2/Windows).  
**Source**: Extracted from Local OpenClaw Gateway Setup Session  
**Date**: February 2, 2026

---

## Skill #1: Local LLM Optimization (RAM Constrained)

### When to Use
- Running OpenClaw with **Ollama** on a machine with limited RAM (e.g., 16GB total, 13GB free).
- Encountering "memory allocation" or "not enough space" errors during model load.

### The Problem
Large context windows (default 8192+) consume significant VRAM/RAM. On a 16GB system, a standard Llama 3.2 3B model might exceed limits when combined with other system apps.

### The Solution: Custom OMF (Ollama Model File)
Create a down-scaled version of the model to prioritize RAM safety.

**Step 1: Create a Modelfile**
```dockerfile
FROM llama3.2:3b
# Reduce context window to 4096 (standard is 8k-32k)
PARAMETER num_ctx 4096
# Limit max prediction tokens for speed
PARAMETER num_predict 2048
```

**Step 2: Build and Tag**
```bash
ollama create llama3.2:3b-small -f Modelfile
```

**Step 3: Reference in OpenClaw**
```json
{
  "agents": {
    "defaults": {
      "model": { "primary": "ollama_local/llama3.2:3b-small" }
    }
  }
}
```

---

## Skill #2: Dashboard Access over LAN (Security Bypass)

### When to Use
- Accessing OpenClaw's Control UI via a **WSL2 LAN IP** (e.g., `172.18.x.x`).
- Stuck on "device identity required" error despite having a token.

### The Problem
Browsers block `WebCrypto` (required for identity generation) on insecure `http://` contexts except for `localhost`. WSL2 IPs are seen as insecure "remote" IPs.

### The Solution: Security Degradation for Local/LAN
Enable specific bypasses in `openclaw.json` (formerly `openclaw_config.json`).

```json
{
  "gateway": {
    "bind": "lan",
    "controlUi": {
      "allowInsecureAuth": true,
      "dangerouslyDisableDeviceAuth": true
    }
  }
}
```

**Access Formula**:
Always use the tokenized URL on first visit to ensure the cookie is set correctly:
`http://<IP>:<PORT>/?token=<YOUR_TOKEN>`

---

## Skill #3: Restricted Agent Isolation (WSL2)

### When to Use
- Running an autonomous agent with shell access on your main development machine.
- Policy requires environment isolation and dependency separation.

### The Problem
Running an agent with your primary user's shell access is dangerous. It can see your global SSH keys, private files, and browser profiles.

### The Solution: Dedicated Runner Account
Set up a restricted user in WSL2 to run the OpenClaw daemon.

**Step 1: Create the User**
```bash
sudo adduser openclaw-runner --disabled-password --gecos ""
```

**Step 2: Install CLI as User**
```bash
sudo -u openclaw-runner -i
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/... | bash
nvm install 22
npm install -g openclaw
```

**Step 3: Secure the Config**
```bash
chmod 600 ~/.openclaw/openclaw.json
```

---

## Quick Reference: OpenClaw v2026 Schema Fixes

| Field | Gotcha | Fix |
| :--- | :--- | :--- |
| `gateway.bind` | Cannot use `127.0.0.1` | Use `"loopback"` or `"lan"` |
| `agents.defaults.model` | Cannot be a string | Must be `{ "primary": "model-id" }` |
| `auth.mode` | Defaults to password | Explicitly set to `"token"` if using a token |

---

## Skill #4: Service Management (Restarting)

### When to Use
- "Gateway failed to start: gateway already running" error.
- "Port 18789 is already in use" error.
- After installing new browser binaries or upgrading core packages.

### The Problem
OpenClaw doesn't always shut down cleanly, leaving a "zombie" process holding the port. Running `gateway run` again fails because the port is locked.

### The Solution: Force Kill & Restart (One-Liner)

This command safely kills any process belonging to the `openclaw-runner` user named `node` and restarts the gateway immediately.

```bash
# Force kill old process + Start new instance
sudo pkill -u openclaw-runner node || true && sudo -u openclaw-runner bash -c 'export NVM_DIR="$HOME/.nvm"; . "$NVM_DIR/nvm.sh"; openclaw gateway run'
```

---

## Skill #5: Advanced CLI Command Injection

### When to Use
- The Agent (LLM) is "too chatty" and refuses to execute a slash command.
- You need to paste a sensitive token/cookie and don't want it in the browser history.
- The UI is misformatting your input (e.g., smart quotes).

### The Solution: Direct Injection via Session ID
Bypass the frontend and inject the command directly into the agent's brain stream using the server CLI.

**Step 1: Get the Session ID**
```bash
# Export env variables first!
sudo -u openclaw-runner bash -c 'export NVM_DIR="$HOME/.nvm"; . "$NVM_DIR/nvm.sh"; openclaw sessions list'
# Copy the 36-char ID (e.g., f6317d3d-...)
```

**Step 2: Inject the Command**
```bash
sudo -u openclaw-runner bash -c 'export NVM_DIR="$HOME/.nvm"; . "$NVM_DIR/nvm.sh"; openclaw sessions send <SESSION_ID> "/skill linkedin config cookie <YOUR_COOKIE>"'
```

---

**Total Skills**: 5
**Status**: Verified on Windows 11 / WSL2 (Ubuntu)
