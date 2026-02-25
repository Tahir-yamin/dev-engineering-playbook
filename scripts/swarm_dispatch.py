#!/usr/bin/env python3
"""
Swarm Orchestrator v1.0
Automates the selection and handoff between the 148+ specialized agents.
"""

import sys
import json
import os

AGENT_CATALOG = "d:/my-dev-knowledge-base/docs/external-libs/GITHUB_COPILOT_AGENTS_INDEX.md"
AGENT_RULES_DIR = "d:/my-dev-knowledge-base/.agent/rules"

def get_best_agent(task_description):
    """
    Simulated logic to find the best agent from the catalog.
    In real usage, the Master Orchestrator calls this to find specialized help.
    """
    # This is a helper script for the LLM to quickly locate agent files
    keywords = {
        "security": "se-security-reviewer",
        "react": "expert-react-frontend-engineer",
        "nextjs": "expert-nextjs-developer",
        "dotnet": "CSharpExpert.agent.md",
        "k8s": "platform-sre-kubernetes",
        "plan": "plan.agent.md",
        "audit": "scripts/checklist.py"
    }
    
    for key, agent in keywords.items():
        if key in task_description.lower():
            return agent
    return "orchestrator"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
        agent = get_best_agent(task)
        print(f"RECOMMENDED_AGENT: {agent}")
