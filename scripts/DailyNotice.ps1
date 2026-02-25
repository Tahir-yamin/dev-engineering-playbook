# Daily Google AI Mastery Notifier
# This script determines the current day of the plan and sends an email notification.

$StartDate = [datetime]"2026-02-01"
$Today = Get-Date

if ($Today -lt $StartDate) {
    Write-Host "The plan has not started yet. Day 1 starts on February 2nd."
    exit
}

$DayNumber = [math]::Floor(($Today - $StartDate).TotalDays) + 1

if ($DayNumber -gt 7) {
    Write-Host "The 7-Day Plan is complete! Congratulations."
    exit
}

$PlanFile = "C:\Users\Administrator\.gemini\antigravity\brain\4cc42ab7-a83f-4872-8e39-12cf19999501\implementation_plan.md"
$Subject = "Day ${DayNumber}: Google AI Mastery Notice"

# Trigger the email utility
python d:\my-dev-knowledge-base\scripts\gmail_utility.py --to "tahiryamin2050@gmail.com" --subject "$Subject" --body_file "$PlanFile"

Write-Host "Daily Notice for Day $DayNumber sent to tahiryamin2050@gmail.com"
