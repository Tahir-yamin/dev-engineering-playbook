import os
import re

RULES_DIR = r"d:\my-dev-knowledge-base\.agent\rules"

# Mapping rules: (regex_pattern, new_prefix)
# Ordered by priority
MAPPINGS = [
    (r"alpha-ultimate-beast", "alpha-ultimate"),
    (r"CSharp|dotnet|csharp", "lang-csharp"),
    (r"python", "lang-python"),
    (r"rust", "lang-rust"),
    (r"go-mcp", "lang-go"),
    (r"java-mcp", "lang-java"),
    (r"kotlin", "lang-kotlin"),
    (r"ruby", "lang-ruby"),
    (r"php", "lang-php"),
    (r"swift", "lang-swift"),
    (r"cpp|software-engineer.*v1", "lang-cpp"),
    (r"clojure", "lang-clojure"),
    
    (r"react|nextjs|frontend|angular|winforms|shopify|laravel|drupal|electron|aem", "ui"),
    (r"maui", "ui-mobile"),
    
    (r"azure|aks|saas-architect", "cloud-azure"),
    (r"terraform|bicep|iac|arm-migration|verified-modules", "ops-infra"),
    (r"github-actions|cicd|se-gitops", "ops-ci"),
    (r"ops-cloud|cloud-infrastructure", "ops-cloud"),
    (r"pagerduty|incident|dynatrace|elasticsearch-observability|monitoring", "ops-sre"),
    (r"octopus", "ops-deploy"),
    (r"platform-sre-kubernetes|droid", "ops-k8s"),
    
    (r"sql|postgres|mongo|neon|neo4j|data-modeling|kusto|hlbpa", "data"),
    (r"power-bi|visualization|dax|fabric", "data-bi"),
    
    (r"security|sec-|sec\.|reviewer|stackhawk|audit", "sec"),
    
    (r"arch|adr|blueprint|specification|modernization", "arch"),
    
    (r"plan|planner|project|task|prd|requirements|atlassian|jira|roadmap|implementation-plan", "plan"),
    
    (r"test|tdd|playwright|qa|evaluator|differential", "test"),
    
    (r"accessibility|ux-ui|designer", "ux"),
    
    (r"prompt|code-tour|comet|context7|debug|janitor|mentor|thinking|software-engineer|principal-software|alchemist|sentinel|workflow-orchestrator", "dev"),
    
    (r"writer|content|documentation|address-comments", "doc"),
]

def get_new_name(filename):
    # Remove common redundant words
    clean = filename.lower()
    clean = clean.replace(".agent.md", "").replace(".md", "")
    clean = clean.replace("expert", "").replace("specialist", "").replace("software-engineer", "").replace("-persona", "")
    clean = clean.replace("agent-", "").replace("-agent", "")
    clean = clean.strip("-")

    # Final name fallback
    final_core = clean
    
    for pattern, prefix in MAPPINGS:
        if re.search(pattern, filename, re.IGNORECASE):
            # Special case for alpha
            if prefix == "alpha-ultimate":
                return "alpha-beast.agent.md"
            
            # Extract core identifier if possible
            # e.g. expert-react-frontend -> react
            core = clean
            # If the prefix is already in the name, don't duplicate
            if prefix.split("-")[0] in core:
                final_name = f"{core}.agent.md"
            else:
                final_name = f"{prefix}-{core}.agent.md"
            
            # Clean up double dashes etc
            final_name = final_name.replace("--", "-")
            return final_name

    # Default fallback
    return f"dev-{clean}.agent.md"

def run_renames():
    files = [f for f in os.listdir(RULES_DIR) if f.endswith(".md")]
    print(f"Found {len(files)} files to process.")
    
    rename_map = {}
    
    for f in files:
        new_name = get_new_name(f)
        rename_map[f] = new_name
        
    # Execute renames
    for old, new in rename_map.items():
        old_path = os.path.join(RULES_DIR, old)
        new_path = os.path.join(RULES_DIR, new)
        
        if old_path != new_path:
            print(f"Renaming: {old} -> {new}")
            try:
                # If target exists, merge or handle conflict?
                # For now, just rename. 
                if os.path.exists(new_path):
                    # To avoid loss, let's append a number if conflict
                    base, ext = os.path.splitext(new)
                    count = 1
                    while os.path.exists(os.path.join(RULES_DIR, f"{base}-{count}{ext}")):
                        count += 1
                    new_path = os.path.join(RULES_DIR, f"{base}-{count}{ext}")
                
                os.rename(old_path, new_path)
            except Exception as e:
                print(f"Error renaming {old}: {e}")

if __name__ == "__main__":
    run_renames()
