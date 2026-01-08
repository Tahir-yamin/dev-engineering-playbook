#!/usr/bin/env bash
# Notification hook - Alerts when Claude needs user input
# Triggered by: Notification event
# Supports: macOS, Linux, Windows (WSL/Git Bash)

# macOS notification
if command -v osascript &> /dev/null; then
    osascript -e 'display notification "Claude needs your input" with title "Claude Code" sound name "Glass"'
# Linux notification (requires notify-send)
elif command -v notify-send &> /dev/null; then
    notify-send "Claude Code" "Claude needs your input" --urgency=normal
# Windows notification via PowerShell (WSL or Git Bash)
elif command -v powershell.exe &> /dev/null; then
    powershell.exe -Command "
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
        [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
        \$template = '<toast><visual><binding template=\"ToastText02\"><text id=\"1\">Claude Code</text><text id=\"2\">Claude needs your input</text></binding></visual></toast>'
        \$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
        \$xml.LoadXml(\$template)
        \$toast = [Windows.UI.Notifications.ToastNotification]::new(\$xml)
        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('Claude Code').Show(\$toast)
    " 2>/dev/null || true
fi

# Always exit 0 - notifications should never block
exit 0
