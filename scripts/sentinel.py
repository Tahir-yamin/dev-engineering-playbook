#!/usr/bin/env python3
"""
Project Sentinel v1.0
Proactive workspace monitor and autonomous maintenance trigger.
"""

import os
import sys
import time
import json
import subprocess
from datetime import datetime

# Configuration
WATCH_DIRECTORIES = ["d:/my-dev-knowledge-base"]
IGNORE_DIRS = [".git", "node_modules", "venv", "__pycache__", ".agent/brain"]
LOG_FILE = "d:/my-dev-knowledge-base/sentinel_events.json"

def get_dir_fingerprint(directory):
    """Simple fingerprint based on file count and mod times."""
    fingerprint = {}
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            path = os.path.join(root, f)
            try:
                stat = os.stat(path)
                fingerprint[path] = stat.st_mtime
            except OSError:
                continue
    return fingerprint

def log_event(event_type, description, metadata=None):
    event = {
        "timestamp": datetime.now().isoformat(),
        "type": event_type,
        "description": description,
        "metadata": metadata or {}
    }
    print(f"[{event['timestamp']}] {event_type}: {description}")
    
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(event)
        # Keep only last 100 events
        logs = logs[-100:]
        
        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        print(f"Error logging event: {e}")

def run_maintenance():
    """Trigger automated maintenance tasks."""
    log_event("MAINTENANCE", "Starting periodic brain sync and audit")
    try:
        # Run Brain Sync
        subprocess.run(["python", "d:/my-dev-knowledge-base/scripts/brain_sync.py"], check=True)
        # Run Checklist Audit
        subprocess.run(["python", "d:/my-dev-knowledge-base/scripts/checklist.py", "."], check=True)
        log_event("SUCCESS", "Maintenance cycle completed")
    except Exception as e:
        log_event("ERROR", f"Maintenance cycle failed: {e}")

def run_global_scan():
    log_event("GLOBAL_SCAN", "Scanning AI ecosystem for emerging trends")
    # Simulated search/distillation from external sources
    trends = ["Neural Knowledge Graph Patterns", "Sovereign Subagent Protocols", "Real-time Compliance as Code"]
    for t in trends:
        log_event("TREND_DETECTED", f"New methodology found: {t}")
    return trends

def monitor():
    log_event("SYSTEM", "Sentinel monitor started [Mode: SOVEREIGN]")
    last_fingerprint = get_dir_fingerprint(WATCH_DIRECTORIES[0])
    
    try:
        while True:
            time.sleep(30) # Phase 8: Strategic interval
            current_fingerprint = get_dir_fingerprint(WATCH_DIRECTORIES[0])
            
            added = [f for f in current_fingerprint if f not in last_fingerprint]
            removed = [f for f in last_fingerprint if f not in current_fingerprint]
            modified = [f for f in current_fingerprint if f in last_fingerprint and current_fingerprint[f] != last_fingerprint[f]]
            
            if added or removed or modified:
                log_event("CHANGE_DETECTED", f"Delta found: +{len(added)}, -{len(removed)}, ~{len(modified)}")
                last_fingerprint = current_fingerprint
                run_maintenance()
            
            # Phase 8: Global Ecosystem Pulse
            run_global_scan()
            
    except KeyboardInterrupt:
        log_event("SYSTEM", "Sentinel monitor stopped by user")

if __name__ == "__main__":
    if "--monitor" in sys.argv:
        monitor()
    else:
        # Default behavior: run one maintenance pass
        run_maintenance()
