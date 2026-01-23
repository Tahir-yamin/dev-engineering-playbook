# Claude Healthcare & Life Sciences Skills

**Topics**: Medical AI, HIPAA Compliance, Clinical Workflows, Healthcare Automation  
**Version**: 1.0  
**Source**: Anthropic Claude for Healthcare (January 2026)  
**Last Updated**: 2026-01-19

---

## Overview

Claude for Healthcare provides HIPAA-compliant AI capabilities specifically designed for medical and life sciences applications. These skills enable faster prior authorization, clinical trial support, and patient care coordination.

---

## Skill #1: Prior Authorization Review

### When to Use
- Reviewing documentation for insurance prior authorization
- Accelerating approval processes (60% faster)
- Ensuring compliance with insurance requirements

### Implementation

**Setup**:
```python
# Requires Claude Pro/Team/Enterprise with healthcare tier
# Enable HIPAA-compliant mode
claude_config = {
    "model": "claude-3-sonnet", 
    "hipaa_compliant": True,
    "skill": "prior-authorization-review"
}
```

**Usage Pattern**:
```markdown
**ROLE**: Medical Prior Authorization Specialist

**PATIENT DOCUMENTATION**: [Upload medical records, treatment plans]
**INSURANCE REQUIREMENTS**: [Specify insurance carrier guidelines]

**TASK**:
1. Review all submitted documentation
2. Identify missing requirements
3. Draft authorization request letter
4. Highlight potential denial risks

**DELIVERABLES**:
- Complete prior auth request
- Missing documentation checklist
- Risk assessment
```

### Key Features
- ✅ Connects to CMS Coverage Database
- ✅ References ICD-10 codes automatically
- ✅ Checks National Provider Identifier Registry
- ✅ Generates compliant documentation

### Lessons Learned
- Works best with structured medical records
- Requires clear insurance carrier specifications
- Can reduce prior auth time from days to hours

---

## Skill #2: Clinical Trial Protocol Drafting

### When to Use
- Designing new clinical trials
- Generating FDA-compliant protocols
- Recommending appropriate endpoints

### Implementation

**Prompt Template**:
```markdown
**ROLE**: Clinical Trial Protocol Designer

**STUDY OBJECTIVE**: [Describe the research question]
**THERAPEUTIC AREA**: [e.g., Oncology, Cardiology]
**PHASE**: [Phase I/II/III/IV]

**REQUIREMENTS**:
- Generate protocol outline
- Recommend primary/secondary endpoints
- Consider FDA regulatory pathways
- Include safety monitoring plan

**DELIVERABLES**:
- Protocol draft (ICH-GCP compliant)
- Endpoint justification
- Regulatory pathway recommendation
- Sample size calculation rationale
```

### New Connectors
- **Medidata**: Clinical trial data access
- **PubMed**: Biomedical literature search
- **CMS Database**: Coverage information

### Best Practices
- ✅ Always specify therapeutic area
- ✅ Include historical context from similar trials
- ✅ Request statistical power calculations
- ✅ Review for FDA guideline compliance

---

## Skill #3: FHIR Development Support

### When to Use
- Building healthcare data interoperability
- Converting between healthcare data formats
- Implementing HL7 FHIR standards

### Implementation

**Setup Requirements**:
```bash
# Install FHIR libraries
pip install fhir.resources
pip install hl7apy
```

**Prompt Pattern**:
```markdown
**ROLE**: FHIR Integration Specialist

**DATA SOURCE**: [Describe current data format]
**TARGET**: FHIR R4 standard
**RESOURCES NEEDED**: [Patient, Observation, Medication, etc.]

**TASK**:
- Map source data to FHIR resources
- Generate FHIR JSON/XML
- Validate against FHIR schemas
- Create transformation scripts

**DELIVERABLES**:
- FHIR resource definitions
- Mapping documentation
- Validation scripts
- Sample payloads
```

### Key Capabilities
- Converts instrument data to Allotrope format
- Supports bioinformatics workflows (scVI-tools bundle)
- Nextflow deployment assistance

---

## Skill #4: Patient Message Triage

### When to Use
- Routing patient inquiries to appropriate departments
- Prioritizing urgent messages
- Automating initial responses

### Implementation

**Configuration**:
```json
{
  "skill": "patient-message-triage",
  "departments": ["urgent_care", "scheduling", "billing", "pharmacy"],
  "urgency_levels": ["emergency", "urgent", "routine"],
  "auto_respond": true
}
```

**Usage**:
```markdown
**ROLE**: Patient Communication Coordinator

**INCOMING MESSAGE**: [Patient message text]
**HISTORICAL CONTEXT**: [Patient medical history if available]

**ANALYZE**:
1. Determine urgency level
2. Identify appropriate department
3. Extract key medical terms/symptoms
4. Flag potential emergencies

**OUTPUT**:
- Urgency: [Emergency/Urgent/Routine]
- Route to: [Department]
- Suggested response: [Draft response]
- Escalation needed: [Yes/No]
```

### Safety Features
- ✅ Flags potential medical emergencies
- ✅ HIPAA-compliant message handling
- ✅ Maintains patient privacy
- ✅ Audit trail for all decisions

---

## Skill #5: Allotrope Data Conversion

### When to Use
- Converting laboratory instrument data
- Standardizing data formats for analysis
- Integrating multiple data sources

### Implementation

**Supported Instruments**:
- Mass spectrometers
- Chromatography systems
- Plate readers
- Sequencers

**Prompt Template**:
```markdown
**ROLE**: Laboratory Data Engineer

**INSTRUMENT TYPE**: [Specify instrument]
**INPUT FORMAT**: [Vendor-specific format]
**OUTPUT**: Allotrope Data Format (ADF)

**CONVERSION REQUIREMENTS**:
- Preserve all metadata
- Maintain data integrity
- Include quality control metrics
- Generate validation report

**DELIVERABLES**:
- ADF JSON file
- Conversion script
- Validation summary
- Metadata mapping document
```

---

## Quick Reference Commands

### Database Connections
```python
# Connect to CMS Coverage Database
cms_query = "coverage requirements for [procedure]"

# Search PubMed
pubmed_query = "clinical trials [condition] [intervention]"

# Lookup ICD-10 codes
icd_lookup = "diabetes mellitus type 2"
```

### Common Use Cases
| Use Case | Skill | Time Savings |
|----------|-------|--------------|
| Prior Authorization | #1 | 60% faster |
| Protocol Design | #2 | 40% faster |
| Data Integration | #3 | 70% faster |
| Message Routing | #4 | 80% faster |
| Data Conversion | #5 | 50% faster |

---

## Integration Examples

### Python Integration
```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

# Use healthcare skill
response = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": "Review this prior auth request: [documentation]"
    }],
    metadata={
        "skill": "prior-authorization-review",
        "hipaa_mode": True
    }
)
```

### API Integration
```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-3-sonnet-20240229",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Analyze clinical trial data"}],
    "metadata": {"skill": "clinical-trial-protocol"}
  }'
```

---

## Compliance & Security

### HIPAA Compliance Checklist
- [x] End-to-end encryption
- [x] Access logging and audit trails  
- [x] Data retention policies
- [x] Patient privacy protection
- [x] Secure data transmission
- [x] Business Associate Agreement (BAA) required

### Data Handling
- **PHI Protection**: All patient data encrypted at rest and in transit
- **De-identification**: Option to de-identify data before processing
- **Retention**: Configurable data retention (default: no storage)
- **Access Control**: Role-based access control (RBAC)

---

## Related Skills
- General Claude Skills (claude-skills.md)
- Data Integration Skills (data-skills.md)
- API Integration Skills (api-skills.md)

---

## Resources

### Official Documentation
- Claude for Healthcare: https://www.anthropic.com/healthcare
- FHIR Specification: https://www.hl7.org/fhir/
- Allotrope Foundation: https://www.allotrope.org/

### GitHub Repositories
- anthropics/skills (healthcare branch)
- Expected: anthropics/healthcare-skills

### Community
- Healthcare AI Reddit: r/HealthcareAI
- FHIR Community: chat.fhir.org

---

**Healthcare AI is transforming medicine - use these skills responsibly with appropriate medical oversight!** 🏥
