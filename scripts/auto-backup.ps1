# Auto-Backup Script for Knowledge Base

$timestamp = Get-Date -Format "yyyy-MM-dd-HHmm"
$date = Get-Date -Format "yyyy-MM-dd"
$source = "d:\my-dev-knowledge-base"
$backupRoot = "d:\kb-backups"
$dailyBackup = "$backupRoot\daily\kb-$date"
$weeklyBackup = "$backupRoot\weekly\kb-week-$(Get-Date -Format 'yyyy-ww')"

# Ensure backup directories exist
New-Item -ItemType Directory -Path "$backupRoot\daily" -Force | Out-Null
New-Item -ItemType Directory -Path "$backupRoot\weekly" -Force | Out-Null

Write-Host "🔄 Starting Knowledge Base Backup..." -ForegroundColor Cyan
Write-Host "Source: $source"
Write-Host "Daily Backup: $dailyBackup"

# Daily incremental backup (mirror, exclude .git and temp files)
Write-Host "`n📦 Creating daily backup..." -ForegroundColor Yellow
robocopy $source $dailyBackup /MIR /XD .git node_modules __pycache__ .next /LOG+:"$backupRoot\backup-$date.log" /NP /NDL /NFL

if ($LASTEXITCODE -le 7) {
    Write-Host "✅ Daily backup complete" -ForegroundColor Green
} else {
    Write-Host "❌ Daily backup failed with code: $LASTEXITCODE" -ForegroundColor Red
    exit 1
}

# Weekly full backup (on Sunday)
if ((Get-Date).DayOfWeek -eq 'Sunday') {
    Write-Host "`n📦 Creating weekly backup..." -ForegroundColor Yellow
    robocopy $source $weeklyBackup /E /XD .git node_modules __pycache__ /LOG+:"$backupRoot\backup-weekly-$date.log" /NP /NDL /NFL
    
    if ($LASTEXITCODE -le 7) {
        Write-Host "✅ Weekly backup complete" -ForegroundColor Green
    }
}

# Cleanup old daily backups (keep last 7 days)
Write-Host "`n🧹 Cleaning up old daily backups..." -ForegroundColor Yellow
Get-ChildItem "$backupRoot\daily" | 
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-7) } |
    Remove-Item -Recurse -Force

# Cleanup old weekly backups (keep last 4 weeks)
Get-ChildItem "$backupRoot\weekly" | 
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-28) } |
    Remove-Item -Recurse -Force

# Generate backup report
$totalSize = (Get-ChildItem $dailyBackup -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
$fileCount = (Get-ChildItem $dailyBackup -Recurse -File).Count

Write-Host "`n📊 Backup Summary:" -ForegroundColor Cyan
Write-Host "  Files backed up: $fileCount"
Write-Host "  Total size: $([math]::Round($totalSize, 2)) MB"
Write-Host "  Backup location: $dailyBackup"
Write-Host "`n✅ Backup process complete!`n" -ForegroundColor Green
