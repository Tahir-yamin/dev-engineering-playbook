# Repository Cleanup Script
# Purpose: Remove unnecessary files (.git, tests, build artifacts) from cloned repositories
# Saves: ~131 MB (77% reduction)

Write-Host "🧹 Starting Repository Cleanup..." -ForegroundColor Cyan
Write-Host ""

$externalLibs = "d:\my-dev-knowledge-base\external-libs"

# Calculate initial size
Write-Host "📊 Calculating initial size..." -ForegroundColor Yellow
$initialSize = (Get-ChildItem $externalLibs -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB
Write-Host "Initial size: $([math]::Round($initialSize, 2)) MB" -ForegroundColor White
Write-Host ""

# 1. Remove .git folders (saves ~131 MB)
Write-Host "🗑️  Removing .git folders..." -ForegroundColor Yellow
$gitFolders = Get-ChildItem $externalLibs -Recurse -Directory -Filter ".git" -Force -ErrorAction SilentlyContinue
$gitCount = ($gitFolders | Measure-Object).Count
Write-Host "Found $gitCount .git folders"
$gitFolders | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "✅ Removed .git folders" -ForegroundColor Green
Write-Host ""

# 2. Remove node_modules
Write-Host "🗑️  Removing node_modules..." -ForegroundColor Yellow
$nodeModules = Get-ChildItem $externalLibs -Recurse -Directory -Filter "node_modules" -Force -ErrorAction SilentlyContinue
$nodeCount = ($nodeModules | Measure-Object).Count
Write-Host "Found $nodeCount node_modules folders"
$nodeModules | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "✅ Removed node_modules" -ForegroundColor Green
Write-Host ""

# 3. Remove test folders
Write-Host "🗑️  Removing test folders..." -ForegroundColor Yellow
$testFolders = @(
    Get-ChildItem $externalLibs -Recurse -Directory -Filter "tests" -ErrorAction SilentlyContinue
    Get-ChildItem $externalLibs -Recurse -Directory -Filter "__tests__" -ErrorAction SilentlyContinue
    Get-ChildItem $externalLibs -Recurse -Directory -Filter "test" -ErrorAction SilentlyContinue
)
$testCount = ($testFolders | Measure-Object).Count
Write-Host "Found $testCount test folders"
$testFolders | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "✅ Removed test folders" -ForegroundColor Green
Write-Host ""

# 4. Remove build/dist folders
Write-Host "🗑️  Removing build artifacts..." -ForegroundColor Yellow
$buildFolders = @(
    Get-ChildItem $externalLibs -Recurse -Directory -Filter "dist" -ErrorAction SilentlyContinue
    Get-ChildItem $externalLibs -Recurse -Directory -Filter "build" -ErrorAction SilentlyContinue
    Get-ChildItem $externalLibs -Recurse -Directory -Filter ".turbo" -ErrorAction SilentlyContinue
)
$buildCount = ($buildFolders | Measure-Object).Count
Write-Host "Found $buildCount build folders"
$buildFolders | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "✅ Removed build artifacts" -ForegroundColor Green
Write-Host ""

# 5. Remove .github/workflows (we don't need CI configs)
Write-Host "🗑️  Removing .github/workflows..." -ForegroundColor Yellow
$workflows = Get-ChildItem $externalLibs -Recurse -Directory -Filter "workflows" -ErrorAction SilentlyContinue | Where-Object { $_.Parent.Name -eq ".github" }
$workflowCount = ($workflows | Measure-Object).Count
Write-Host "Found $workflowCount workflow folders"
$workflows | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "✅ Removed workflows" -ForegroundColor Green
Write-Host ""

# Calculate final size
Write-Host "📊 Calculating final size..." -ForegroundColor Yellow
$finalSize = (Get-ChildItem $externalLibs -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB
$saved = $initialSize - $finalSize
$percentSaved = [math]::Round(($saved / $initialSize) * 100, 1)

Write-Host ""
Write-Host "════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "✅ Cleanup Complete!" -ForegroundColor Green
Write-Host "════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "Initial size:  $([math]::Round($initialSize, 2)) MB" -ForegroundColor White
Write-Host "Final size:    $([math]::Round($finalSize, 2)) MB" -ForegroundColor White
Write-Host "Space saved:   $([math]::Round($saved, 2)) MB ($percentSaved%)" -ForegroundColor Green
Write-Host ""
Write-Host "Kept: Markdown files, skill definitions, examples, documentation" -ForegroundColor Cyan
Write-Host "Removed: .git history, tests, build artifacts, CI configs" -ForegroundColor Yellow
Write-Host ""

# Show what remains
Write-Host "📁 Repositories after cleanup:" -ForegroundColor Cyan
Get-ChildItem $externalLibs -Directory | ForEach-Object {
    $fileCount = (Get-ChildItem $_.FullName -Recurse -File -ErrorAction SilentlyContinue | Measure-Object).Count
    $size = (Get-ChildItem $_.FullName -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB
    Write-Host "  $($_.Name): $fileCount files, $([math]::Round($size, 2)) MB"
}
