# Migration Script: Antigravity Storage -> D: Drive
# Run this in PowerShell as Administrator

$SourceGemini = "C:\Users\Administrator\.gemini"
$SourceAntigravity = "C:\Users\Administrator\.antigravity"
$DestRoot = "D:\AntigravityStorage"

# Ensure destination exists
New-Item -ItemType Directory -Force -Path $DestRoot | Out-Null

Function Move-And-Link ($Source, $Dest) {
    if (Test-Path $Source) {
        Write-Host "Migrating $Source to $Dest..."
        
        # 1. Robocopy for safe move (preserves attributes)
        robocopy $Source $Dest /E /MOVE /NFL /NDL /NJH /NJS
        
        if (-not (Test-Path $Source)) {
            # 2. Create Junction (Symbolic Link)
            New-Item -ItemType Junction -Path $Source -Target $Dest
            Write-Host "✅ Created Link: $Source -> $Dest"
        } else {
            Write-Host "❌ Failed to move original folder. Is it open?" -ForegroundColor Red
        }
    } else {
        Write-Host "Skipping $Source (Not found)"
    }
}

# Close potential locking processes (Aggressive)
# Stop-Process -Name "Code" -ErrorAction SilentlyContinue
# Stop-Process -Name "node" -ErrorAction SilentlyContinue

Move-And-Link $SourceGemini "$DestRoot\.gemini"
Move-And-Link $SourceAntigravity "$DestRoot\.antigravity"

Write-Host "Migration Complete. Verify D:\AntigravityStorage"
Pause
