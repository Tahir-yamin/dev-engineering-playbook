# Community Resources - Sources & Attribution

This file tracks all community resources added to the knowledge base, with proper attribution and links.

---

## Tier 1: Official & High Priority

### 1. anthropics/skills - Official Anthropic Repository

**URL**: https://github.com/anthropics/skills  
**License**: Apache 2.0 (open source skills) + Source Available (document skills)  
**Downloaded**: 2026-01-08  
**Location**: `skills/official_anthropic/`, `guides/agent-skills-spec/`

**What We Got**:
- All official SKILL.md files from the skills/ directory
- Agent Skills specification documentation (authoring + integration guides)
- Document creation skills (DOCX, PDF, PPTX, XLSX)
- Web app testing skills
- MCP server generation skills
- doc-coauthoring skill

**Key Files**:
- `skills/official_anthropic/doc-coauthoring/` - Collaborative document creation
- `skills/official_anthropic/web-app-testing/` - Browser automation testing
- `skills/official_anthropic/mcp-server-gen/` - MCP server scaffolding
- `guides/agent-skills-spec/authoring-guide.md` - How to create skills
- `guides/agent-skills-spec/integration-guide.md` - How to use in apps

**Contributors**: @klazuka, @claude, @camaris

---

### 2. wshobson/agents - Multi-Agent Orchestration

**URL**: https://github.com/wshobson/agents  
**License**: MIT  
**Downloaded**: 2026-01-08  
**Location**: `skills/wshobson/`, `agents/wshobson/`, `workflows/wshobson/`

**What We Got**:
- 67 focused plugins (granular, single-purpose agents)
- 99 specialized agents (architecture, languages, infrastructure, quality, data/AI)
- 107 agent skills across 18 plugins
- 15 workflow orchestrators (multi-agent coordination)
- 71 development tools

**Skill Categories**:
- **Python** (5 skills): async patterns, testing, packaging, performance, UV package manager
- **JavaScript/TypeScript** (4 skills): advanced types, Node.js patterns, testing, ES6+
- **Kubernetes** (4 skills): manifests, Helm charts, GitOps, security policies
- **Cloud Infrastructure** (4 skills): Terraform, multi-cloud, hybrid networking, cost optimization
- **CI/CD** (4 skills): pipeline design, GitHub Actions, GitLab CI, secrets management
- **Backend** (3 skills): API design, architecture patterns, microservices
- **LLM Applications** (4 skills): LangChain, prompt engineering, RAG, evaluation
- **Blockchain/Web3** (4 skills): DeFi, NFT standards, Solidity security, Web3 testing

**Use Cases**:
- Full-Stack feature development
- Security hardening
- Python development with modern tools
- Kubernetes deployment

**Three-Tier Model Strategy**:
- Opus 4.5 ($5/$25): Critical work, 80.9% SWE-bench, 65% fewer tokens
- Sonnet 4.5 ($3/$15): Balanced performance
- Haiku 4.5 ($1/$5): Fast operations

**Contributors**: @wshobson + 33 contributors

---

## Tier 2: Community Best Practices (Coming Next)

### 3. alirezarezvani/claude-skills
**URL**: https://github.com/alirezarezvani/claude-skills  
**License**: MIT  
**Status**: Planned for Tier 2

### 4. alirezarezvani/claude-code-tresor
**URL**: https://github.com/alirezarezvani/claude-code-tresor  
**License**: MIT  
**Status**: Planned for Tier 2

### 5. shinpr/claude-code-workflows
**URL**: https://github.com/shinpr/claude-code-workflows  
**License**: MIT  
**Status**: Planned for Tier 2

---

## Tier 3: Advanced Orchestration (Coming Later)

### 6. ruvnet/claude-flow
**URL**: https://github.com/ruvnet/claude-flow  
**License**: Check repository  
**Status**: Planned for Tier 3

### 7. VoltAgent/awesome-claude-code-subagents
**URL**: https://github.com/VoltAgent/awesome-claude-code-subagents  
**License**: Unlicense  
**Status**: Planned for Tier 3

### 8. travisvn/awesome-claude-skills
**URL**: https://github.com/travisvn/awesome-claude-skills  
**License**: Check repository  
**Status**: Planned for Tier 3

### 9. CloudAI-X/claude-workflow
**URL**: https://github.com/CloudAI-X/claude-workflow-v2  
**License**: Check repository  
**Status**: Planned for Tier 3

---

## Usage Guidelines

### Attribution Requirements

When using community resources:
1. ✅ Keep the attribution header intact
2. ✅ Link back to original source when sharing
3. ✅ Respect the original license terms
4. ✅ Note if you've modified the content

### License Summary

| Source | License | Commercial Use | Modification |
|--------|---------|----------------|--------------|
| anthropics/skills | Apache 2.0* | Yes | Yes |
| wshobson/agents | MIT | Yes | Yes |
| VoltAgent | Unlicense | Yes | Yes |
| Others | Varies | Check repo | Check repo |

*Note: Document skills (DOCX, PDF, PPTX, XLSX) are source-available, not open source

---

## Changelog

### 2026-01-08: Tier 1 Added
- ✅ anthropics/skills (~30 files)
- ✅ wshobson/agents (~220 files)
- ✅ Total: ~250 files added

### Future Updates
- **Tier 2** (Planned): alirezarezvani repos, shinpr workflows
- **Tier 3** (Planned): VoltAgent subagents, ruvnet claude-flow, travisvn collection

---

## Credits & Thanks

Special thanks to the Claude community for these excellent resources:

- **@anthropic** - Official skills and specification
- **@wshobson** - Comprehensive agent orchestration system
- **@VoltAgent** - 100+ specialized subagents
- **@alirezarezvani** - Real-world business skills
- **@shinpr** - Production workflows
- **@ruvnet** - Multi-agent swarm orchestration
- **@travisvn** - Curated skills collection
- **@CloudAI-X** - Universal plugin system

---

**Last Updated**: 2026-01-08  
**Next Review**: After Tier 2 completion
