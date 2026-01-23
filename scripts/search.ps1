# Smart Search for Knowledge Base

param(
    [Parameter(Mandatory=$true)]
    [string]$Query,
    
    [string]$Type = "all",  # all, workflow, skill, persona, doc, whitepaper
    
    [switch]$Fuzzy = $false
)

# Define search locations
$locations = @{
    "workflow" = ".agent\workflows"
    "skill" = "skills"
    "persona" = ".agent\rules"
    "doc" = "docs"
    "whitepaper" = "white-papers"
    "all" = @(".agent\workflows", "skills", ".agent\rules", "docs", "white-papers")
}

# Get paths to search
$searchPaths = if ($Type -eq "all") { $locations["all"] } else { @($locations[$Type]) }

Write-Host "`n🔍 Searching for: '$Query' in $Type" -ForegroundColor Cyan
Write-Host ("=" * 60) -ForegroundColor Gray

$results = @()

foreach ($path in $searchPaths) {
    if (Test-Path $path) {
        # Search for files containing the query
        $matches = Get-ChildItem $path -Recurse -Filter "*.md" -ErrorAction SilentlyContinue |
            Select-String $Query -List -ErrorAction SilentlyContinue |
            Select-Object @{
                Name="File"; Expression={ $_.Path | Split-Path -Leaf }
            }, @{
                Name="Path"; Expression={ $_.Path -replace [regex]::Escape((Get-Location).Path), "." }
            }, @{
                Name="Preview"; Expression={ ($_.Line).Trim().Substring(0, [Math]::Min(80, ($_.Line).Length)) }
            }, LineNumber
        
        $results += $matches
    }
}

# Display results
if ($results.Count -eq 0) {
    Write-Host "`n❌ No results found for '$Query'" -ForegroundColor Yellow
    Write-Host "`nTry:"
    Write-Host "  - Different keywords"
    Write-Host "  - Broader search type (-Type all)"
    Write-Host "  - Check spelling"
} else {
    Write-Host "`n✅ Found $($results.Count) result(s):`n" -ForegroundColor Green
    
    $results | Format-Table @{
        Label="File"; Expression={ $_.File }; Width=30
    }, @{
        Label="Location"; Expression={ $_.Path }; Width=40
    }, @{
        Label="Line"; Expression={ $_.LineNumber }; Width=6
    }, @{
        Label="Preview"; Expression={ $_.Preview + "..." }
    } -Wrap
    
    Write-Host "`nTip: Use " -NoNewline
    Write-Host "-Type workflow|skill|persona|doc|whitepaper" -ForegroundColor Yellow -NoNewline
    Write-Host " to narrow results"
}

Write-Host "`n"
