<#
.SYNOPSIS
    Sovereign Knowledge Base Search v2.1
    Find agents, skills, workflows, and docs by keyword — instantly.

.DESCRIPTION
    Searches filenames first (fast), then content.
    NAME MATCH = keyword found in filename (highest confidence)
    CONTENT    = keyword found inside the file
    
.EXAMPLE
    # Search across everything
    .\scripts\search.ps1 "react ui design"
    
    # Find only agents
    .\scripts\search.ps1 "project management" -Type agent
    
    # Find only skills
    .\scripts\search.ps1 "react ui design" -Type skill
    
    # Find only workflows
    .\scripts\search.ps1 "kubernetes deploy" -Type workflow
    
    # Also search the massive Claude subagents library (slower)
    .\scripts\search.ps1 "react" -Type agent -Deep
#>

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Query,

    # Filter: all | agent | skill | workflow | doc | rule
    [string]$Type = "all",

    # Max results per category
    [int]$Limit = 12,

    # Include deeper dirs (slower but more comprehensive)
    [switch]$Deep
)

$Root = "d:\my-dev-knowledge-base"
$QueryTerms = $Query.ToLower() -split "[\s\-_]+"

# ─── Fast Registry (Primary Tier — always searched) ───────────────────────────
$PrimaryRegistry = @{
    "agent" = @(
        ".agent\agents",
        ".agent\rules",
        ".github\agents",
        ".claude\agents"
    )
    "skill" = @(
        "skills",
        "external-libs\antigravity-kit\.agent\skills"
    )
    "workflow" = @(
        ".agent\workflows"
    )
    "rule" = @(
        ".agent\rules",
        ".claude\rules"
    )
    "doc" = @(
        "docs",
        "white-papers"
    )
}

# ─── Deep Registry (Extended Tier — only with -Deep flag) ─────────────────────
$DeepRegistry = @{
    "agent" = @(
        "agents\subagents\categories",
        "agents\cloudai"
    )
    "skill" = @(
        "external-libs\antigravity-awesome-skills",
        "external-libs\github-awesome-copilot\skills"
    )
    "workflow" = @(
        "external-libs\github-awesome-copilot\prompts"
    )
    "rule" = @()
    "doc" = @()
}

function Get-RelativePath($path) {
    return $path -replace [regex]::Escape($Root + "\"), ".\"
}

function Match-Query($text) {
    $lower = $text.ToLower()
    foreach ($term in $QueryTerms) {
        if ($lower -notmatch [regex]::Escape($term)) { return $false }
    }
    return $true
}

function Search-Dirs($dirs) {
    $hits = @()
    foreach ($dir in $dirs) {
        $fullDir = Join-Path $Root $dir
        if (-not (Test-Path $fullDir)) { continue }

        Get-ChildItem $fullDir -Recurse -Filter "*.md" -ErrorAction SilentlyContinue | ForEach-Object {
            $file = $_
            $nameScore = if (Match-Query $file.BaseName) { 3 } else { 0 }

            $preview = ""
            $contentScore = 0
            try {
                $lines = Get-Content $file.FullName -TotalCount 15 -ErrorAction Stop
                $snippet = ($lines -join " ")
                if (Match-Query $snippet) {
                    $contentScore = 1
                    $descLine = $lines | Where-Object {
                        $_ -match "description:" -or $_ -match "^#\s"
                    } | Select-Object -First 1
                    if ($descLine) {
                        $preview = ($descLine -replace "^---$", "" -replace "^description:\s*[`"']?|[`"']?$", "" -replace "^#+\s*", "").Trim()
                    }
                }
            } catch {}

            $score = $nameScore + $contentScore
            if ($score -gt 0) {
                $hits += [PSCustomObject]@{
                    Score   = $score
                    File    = $file.BaseName
                    RelPath = Get-RelativePath $file.FullName
                    Preview = if ($preview.Length -gt 72) { $preview.Substring(0,72) + "..." } else { $preview }
                    Signal  = if ($nameScore -gt 0) { "NAME" } else { "CONTENT" }
                }
            }
        }
    }
    return $hits | Sort-Object Score -Descending | Select-Object -First $Limit
}

# ─── Determine what to search ─────────────────────────────────────────────────
$searchTypes = if ($Type -eq "all") { @("agent","skill","workflow","doc") } else { @($Type) }

# ─── Banner ───────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "  ================================================================" -ForegroundColor DarkCyan
Write-Host "   SEARCH  |  '$Query'  |  type: $Type$(if ($Deep) {' [DEEP]'} else {' [FAST]'})" -ForegroundColor Cyan
Write-Host "  ================================================================" -ForegroundColor DarkCyan
Write-Host ""

$totalFound = 0

foreach ($t in $searchTypes) {
    if (-not $PrimaryRegistry.ContainsKey($t)) {
        Write-Host "  Unknown type: '$t'. Valid: all, agent, skill, workflow, rule, doc" -ForegroundColor Yellow
        continue
    }

    # Combine primary + optional deep dirs
    $dirs = $PrimaryRegistry[$t]
    if ($Deep -and $DeepRegistry.ContainsKey($t)) {
        $dirs = $dirs + $DeepRegistry[$t]
    }

    $results = Search-Dirs $dirs
    if (-not $results -or $results.Count -eq 0) { continue }
    $totalFound += $results.Count

    # Section header
    Write-Host "  [$($t.ToUpper())]  $($results.Count) result(s)" -ForegroundColor Cyan
    Write-Host "  ----------------------------------------------------------------" -ForegroundColor DarkGray

    foreach ($r in $results) {
        $label = if ($r.Signal -eq "NAME") { "[NAME MATCH]" } else { "[CONTENT]   " }
        $color = if ($r.Signal -eq "NAME") { "Green" } else { "White" }

        Write-Host "  $label " -NoNewline -ForegroundColor $color
        Write-Host $r.File -ForegroundColor Yellow

        if ($r.Preview) {
            Write-Host "              $($r.Preview)" -ForegroundColor Gray
        }

        Write-Host "              $($r.RelPath)" -ForegroundColor DarkGray

        # Show recall syntax for agents and rules
        if ($t -eq "agent" -or $t -eq "rule") {
            $recall = $r.RelPath -replace "\\", "/"
            Write-Host "              @[$recall]" -ForegroundColor DarkYellow
        }
        Write-Host ""
    }
}

# ─── Summary ──────────────────────────────────────────────────────────────────
if ($totalFound -eq 0) {
    Write-Host "  No results found for '$Query'" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  Tips:" -ForegroundColor Cyan
    Write-Host "    Shorter query:   .\scripts\search.ps1 'react'" -ForegroundColor Gray
    Write-Host "    No hyphens:      .\scripts\search.ps1 'ui design'" -ForegroundColor Gray
    Write-Host "    Filter by type:  .\scripts\search.ps1 'deploy' -Type workflow" -ForegroundColor Gray
    Write-Host "    Broader search:  .\scripts\search.ps1 'react' -Type agent -Deep" -ForegroundColor Gray
} else {
    Write-Host "  ================================================================" -ForegroundColor DarkCyan
    Write-Host "   Total: $totalFound result(s)" -ForegroundColor Green
    Write-Host "  ================================================================" -ForegroundColor DarkCyan
    Write-Host ""
    Write-Host "  Recall syntax: @[path/to/agent.md]" -ForegroundColor Cyan
    Write-Host "  Fast agents:   @react  @alpha  @sec  @plan  @arch  @ops  @test" -ForegroundColor Gray
    Write-Host "  Narrow search: .\scripts\search.ps1 'topic' -Type agent|skill|workflow" -ForegroundColor Gray
    if (-not $Deep) {
        Write-Host "  More results:  Add -Deep flag for extended search" -ForegroundColor DarkGray
    }
}
Write-Host ""
