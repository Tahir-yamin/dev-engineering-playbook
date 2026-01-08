# Tier 1 Upgrade - Clone & Organize Script

**Purpose**: Clone official repositories and systematically copy files to your knowledge base  
**Tier**: 1 - Official Anthropic + wshobson/agents  
**Estimated Files**: ~250

---

## Step 1: Clone Repositories

Run these commands in a temporary directory (e.g., `D:\temp\claude-repos`):

```powershell
# Create temp directory
New-Item -Path "D:\temp\claude-repos" -ItemType Directory -Force
cd "D:\temp\claude-repos"

# Clone Tier 1 repositories
git clone https://github.com/anthropics/skills anthropics-skills
git clone https://github.com/wshobson/agents wshobson-agents
```

---

## Step 2: Copy Skills from anthropics/skills

### Target Files from `anthropics-skills/skills/`:
All SKILL.md files including:
- doc-coauthoring
- web-app-testing  
- mcp-server-generation
- docx, pdf, pptx, xlsx (document skills)
- And all others in the skills/ folder

### Copy Command:
```powershell
# Copy all skill files
Copy-Item -Path "D:\temp\claude-repos\anthropics-skills\skills\*" `
          -Destination "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\my-dev-knowledge-base\skills\official_anthropic\" `
          -Recurse -Force

# Verify count
Get-ChildItem "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\my-dev-knowledge-base\skills\official_anthropic\" -Recurse
```

### Copy Agent Skills Spec Documentation:
```powershell
# Copy specification docs
Copy-Item -Path "D:\temp\claude-repos\anthropics-skills\agent-skills-spec\*" `
          -Destination "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\my-dev-knowledge-base\guides\agent-skills-spec\" `
          -Recurse -Force
```

---

## Step 3: Copy from wshobson/agents

### Repository Structure:
```
wshobson-agents/
├── plugins/          ← 67 plugins (agents organized by topic)
├── skills/           ← 107 agent skills  
├── orchestrators/    ← 15 workflow orchestrators
├── tools/            ← 71 development tools
└── docs/             ← Documentation
```

### Copy Agents:
```powershell
# Copy agent plugins  
Copy-Item -Path "D:\temp\claude-repos\wshobson-agents\plugins\*" `
          -Destination "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\my-dev-knowledge-base\agents\wshobson\" `
          -Recurse -Force
```

### Copy Skills:
```powershell
# Copy agent skills
Copy-Item -Path "D:\temp\claude-repos\wshobson-agents\skills\*" `
          -Destination "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\my-dev-knowledge-base\skills\wshobson\" `
          -Recurse -Force
```

### Copy Workflows/Orchestrators:
```powershell
# Copy workflow orchestrators
Copy-Item -Path "D:\temp\claude-repos\wshobson-agents\orchestrators\*" `
          -Destination "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\my-dev-knowledge-base\workflows\wshobson\" `
          -Recurse -Force
```

---

## Step 4: Add Attribution Headers

For each copied file, prepend this header:

```powershell
# PowerShell script to add headers
$workspace = "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\my-dev-knowledge-base"

# Add header to anthropics/skills files
$anthropicFiles = Get-ChildItem "$workspace\skills\official_anthropic" -Filter "*.md" -Recurse

foreach ($file in $anthropicFiles) {
    $content = Get-Content $file.FullName -Raw
    
    # Skip if header already exists
    if ($content -match "^---\nsource:") {
        continue
    }
    
    $header = @"
---
source: https://github.com/anthropics/skills
author: @anthropic
license: Apache 2.0 / Source Available
downloaded: 2026-01-08
modified: false
---

"@
    
    $newContent = $header + $content
    Set-Content -Path $file.FullName -Value $newContent
}

Write-Host "✅ Added headers to Anthropic skill files"

# Repeat for wshobson files
$wshobsonSkills = Get-ChildItem "$workspace\skills\wshobson" -Filter "*.md" -Recurse

foreach ($file in $wshobsonSkills) {
    $content = Get-Content $file.FullName -Raw
    
    if ($content -match "^---\nsource:") {
        continue
    }
    
    $header = @"
---
source: https://github.com/wshobson/agents
author: @wshobson
license: MIT
downloaded: 2026-01-08
modified: false
---

"@
    
    $newContent = $header + $content
    Set-Content -Path $file.FullName -Value $newContent
}

Write-Host "✅ Added headers to wshobson skill files"

# Repeat for agents and workflows
$wshobsonAgents = Get-ChildItem "$workspace\agents\wshobson" -Filter "*.md" -Recurse

foreach ($file in $wshobsonAgents) {
    $content = Get-Content $file.FullName -Raw
    
    if ($content -match "^---\nsource:") {
        continue
    }
    
    $header = @"
---
source: https://github.com/wshobson/agents
author: @wshobson
license: MIT
downloaded: 2026-01-08
modified: false
---

"@
    
    $newContent = $header + $content
    Set-Content -Path $file.FullName -Value $newContent
}

Write-Host "✅ Added headers to wshobson agent files"
```

---

## Step 5: Generate File Counts

```powershell
$workspace = "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\my-dev-knowledge-base"

Write-Host "`n📊 Tier 1 File Counts:"
Write-Host "====================="

$anthropicCount = (Get-ChildItem "$workspace\skills\official_anthropic" -Recurse -File).Count
Write-Host "Anthropic Skills: $anthropicCount files"

$wshobsonSkillsCount = (Get-ChildItem "$workspace\skills\wshobson" -Recurse -File).Count
Write-Host "wshobson Skills: $wshobsonSkillsCount files"

$wshobsonAgentsCount = (Get-ChildItem "$workspace\agents\wshobson" -Recurse -File).Count
Write-Host "wshobson Agents: $wshobsonAgentsCount files"

$wshobsonWorkflowsCount = (Get-ChildItem "$workspace\workflows\wshobson" -Recurse -File).Count
Write-Host "wshobson Workflows: $wshobsonWorkflowsCount files"

$totalTier1 = $anthropicCount + $wshobsonSkillsCount + $wshobsonAgentsCount + $wshobsonWorkflowsCount
Write-Host "`nTotal Tier 1 Files: $totalTier1"
```

---

## Step 6: Run After Completion

After all files are copied and headers added:

```powershell
# Message me:
"Tier 1 files copied. Ready to create indexes and update documentation."
```

I'll then:
1. Create master INDEX.md files
2. Update your README.md with new stats
3. Create QUICKSTART_TIER1.md guide
4. Generate WORKSPACE_STATS.md
5. Commit everything to git

---

## Verification Checklist

- [ ] anthropics-skills cloned successfully
- [  ] wshobson-agents cloned successfully
- [ ] All Anthropic skills copied to `skills/official_anthropic/`
- [ ] Agent skills spec copied to `guides/agent-skills-spec/`
- [ ] wshobson skills copied to `skills/wshobson/`
- [ ] wshobson agents copied to `agents/wshobson/`
- [ ] wshobson workflows copied to `workflows/wshobson/`
- [ ] Attribution headers added to all files
- [ ] File counts verified (expected ~250 total)

---

**After Completion**: Message me and I'll create the indexes and documentation!
