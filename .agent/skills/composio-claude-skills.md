# Composio Claude Skills (110+ Integrations)

**Topics**: App Automation, CRM, Project Management, Social Media, DevOps, Communication
**Source**: [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)
**Version**: 1.0 (Feb 2026)
**Last Updated**: 2026-02-08

---

## Overview

These skills allow Claude to perform real actions across 110+ applications using the **Rube MCP (Composio)** gateway. Each skill provides specific tool schemas and workflows for deep integration.

### Core Prerequisite
- **Rube MCP Server**: Add `https://rube.app/mcp` to your Claude configuration.
- **Connection**: Use `RUBE_MANAGE_CONNECTIONS` to authenticate with any toolkit.

---

## Skill Categories

### 🚀 CRMs & Sales Automation
- **[Salesforce](../external-libs/composio-awesome-claude-skills/salesforce-automation/SKILL.md)**: Lead management, object querying, and updates.
- **[HubSpot](../external-libs/composio-awesome-claude-skills/hubspot-automation/SKILL.md)**: Contact sync, deal tracking, and engagement logging.
- **[Pipedrive](../external-libs/composio-awesome-claude-skills/pipedrive-automation/SKILL.md)**: Pipeline management and activity scheduling.
- **[Zoho CRM](../external-libs/composio-awesome-claude-skills/zoho-crm-automation/SKILL.md)**: Customer data management and record updates.

### 💬 Communication & Collaboration
- **[Slack](../external-libs/composio-awesome-claude-skills/slack-automation/SKILL.md)**: Channel messaging, thread replies, and file uploads.
- **[Discord](../external-libs/composio-awesome-claude-skills/discord-automation/SKILL.md)**: Bot-driven messaging and server management.
- **[WhatsApp](../external-libs/composio-awesome-claude-skills/whatsapp-automation/SKILL.md)**: Direct messaging and notification automation.
- **[Telegram](../external-libs/composio-awesome-claude-skills/telegram-automation/SKILL.md)**: Interaction with groups and channels.
- **[Microsoft Teams](../external-libs/composio-awesome-claude-skills/microsoft-teams-automation/SKILL.md)**: Enterprise messaging and calendar integration.

### 📅 Project Management
- **[Jira](../external-libs/composio-awesome-claude-skills/jira-automation/SKILL.md)**: Issue creation, sprint tracking, and status updates.
- **[Linear](../external-libs/composio-awesome-claude-skills/linear-automation/SKILL.md)**: High-speed issue tracking and cycle management.
- **[Trello](../external-libs/composio-awesome-claude-skills/trello-automation/SKILL.md)**: Board/card manipulation and labeling.
- **[Monday.com](../external-libs/composio-awesome-claude-skills/monday-automation/SKILL.md)**: Workspace management and item updates.
- **[Notion](../external-libs/composio-awesome-claude-skills/notion-automation/SKILL.md)**: Page creation, database querying, and property updates.

### 📧 Email & Productivity
- **[Gmail](../external-libs/composio-awesome-claude-skills/gmail-automation/SKILL.md)**: Search, send, reply, and label management.
- **[Outlook](../external-libs/composio-awesome-claude-skills/outlook-automation/SKILL.md)**: Mail and calendar orchestration.
- **[Google Sheets](../external-libs/composio-awesome-claude-skills/googlesheets-automation/SKILL.md)**: Read/write rows, format ranges, and manage worksheets.
- **[Airtable](../external-libs/composio-awesome-claude-skills/airtable-automation/SKILL.md)**: Database-as-a-service automation.

### 🛠️ Development & DevOps
- **[GitHub](../external-libs/composio-awesome-claude-skills/github-automation/SKILL.md)**: PR reviews, issue management, and repo maintenance.
- **[GitLab](../external-libs/composio-awesome-claude-skills/gitlab-automation/SKILL.md)**: CI/CD monitoring and project management.
- **[Vercel](../external-libs/composio-awesome-claude-skills/vercel-automation/SKILL.md)**: Deployment status and project configuration.
- **[Sentry](../external-libs/composio-awesome-claude-skills/sentry-automation/SKILL.md)**: Error monitoring and issue resolution.

### 📱 Social Media
- **[Twitter/X](../external-libs/composio-awesome-claude-skills/twitter-automation/SKILL.md)**: Posting tweets, searching content, and analytics.
- **[Instagram](../external-libs/composio-awesome-claude-skills/instagram-automation/SKILL.md)**: Media posting and comment management.
- **[YouTube](../external-libs/composio-awesome-claude-skills/youtube-automation/SKILL.md)**: Video search and metadata updates.
- **[Reddit](../external-libs/composio-awesome-claude-skills/reddit-automation/SKILL.md)**: Subreddit posting and comment interaction.

---

## Common Implementation Pattern

When using any Composio skill, always follow this pattern:

1. **Scan Tools**: Call `RUBE_SEARCH_TOOLS` with the toolkit name (e.g., `gmail`).
2. **Resolve IDs**: Extract specific IDs (Thread IDs, Label IDs, Project IDs) from list/search tools.
3. **Execute Action**: Use the specific action tool (e.g., `GMAIL_SEND_EMAIL`).
4. **Clean Up**: Provide a summary of the action taken.

---

## Full Listing
For a complete list of 110+ skills and their detailed `SKILL.md` instructions, refer to the local directory:
`../external-libs/composio-awesome-claude-skills/`
