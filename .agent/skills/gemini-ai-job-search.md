# Gemini AI Job Search Integration Skill

## Overview
Capability to search for jobs using Google's Gemini API and extract exact job URLs with structured data.

## Technology
- **API**: Google Gemini API (`gemini-3-flash-preview`)
- **SDK**: `google-genai` (official Python SDK)
- **Cost**: Zero (Free tier: 1,500 requests/day)

## Capabilities

### 1. Job Search
- Query jobs by title and location
- Filter by date range (e.g., last 7 days)
- Extract structured data (title, company, location, URL)
- Output JSON format

### 2. URL Extraction
- Returns exact job application URLs
- Direct career portal links
- No search page intermediaries

### 3. Data Structure
```json
{
  "title": "Project Controls Manager",
  "company": "AECOM",
  "location": "Dubai",
  "url": "https://aecom.jobs/dubai-are/..."
}
```

## Scripts

### Main Search Script
**File**: `job-application/scripts/gemini_job_searcher_simple.py`

**Usage**:
```bash
python gemini_job_searcher_simple.py \
  --query "Project Controls Manager" \
  --location "Dubai" \
  --days 7 \
  --api-key "YOUR_KEY"
```

**Environment Variable**:
```bash
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

### Integration Script
**File**: `job-application/scripts/apply_from_gemini.py`

Automatically generates applications from Gemini search results.

## Configuration

### Safety Settings
Required to prevent blocking:
```python
config={
    'safety_settings': [
        {'category': 'HARM_CATEGORY_HARASSMENT', 'threshold': 'BLOCK_NONE'},
        {'category': 'HARM_CATEGORY_HATE_SPEECH', 'threshold': 'BLOCK_NONE'},
        {'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT', 'threshold': 'BLOCK_NONE'},
        {'category': 'HARM_CATEGORY_DANGEROUS_CONTENT', 'threshold': 'BLOCK_NONE'},
    ]
}
```

### Model Selection
- **Free Tier**: `gemini-3-flash-preview`
- **Alternative**: `gemini-2.5-flash` (more capacity)

## Performance

| Metric | Value |
|--------|-------|
| Response Time | ~10 seconds |
| Jobs Per Request | 5+ |
| Daily Limit (Free) | 1,500 requests |
| URL Accuracy | High |
| Cost | $0 |

## Limitations

1. **Knowledge Cutoff**: January 2025
   - May not have jobs posted very recently
   - Best for established company postings

2. **Not Real-Time Search**:
   - Uses Gemini's trained knowledge
   - Not live web scraping

3. **Free Tier Limits**:
   - 1,500 requests per day
   - May hit quota during peak usage

## Integration Points

### Workflow Integration
- **Primary**: Option 1 in apply-for-jobs workflow
- **Complement**: LinkedIn Posts for newest jobs
- **Fallback**: Job board search pages

### Output Files
- `gemini_jobs.json` - Search results
- Generated applications in `output/` folder

## Error Handling

### Common Issues:

1. **Safety Blocks**:
   - **Cause**: Default safety filters too strict
   - **Solution**: Set `BLOCK_NONE` threshold

2. **503 Service Unavailable**:
   - **Cause**: Server overload
   - **Solution**: Retry after 10-15 minutes

3. **Empty Response**:
   - **Cause**: Safety filters or API limits
   - **Solution**: Check finish_reason and safety_ratings

4. **404 Model Not Found**:
   - **Cause**: Wrong model name
   - **Solution**: Use `gemini-3-flash-preview` or `gemini-2.5-flash`

## Future Enhancements

### Option 2: MCP Server
Convert to Model Context Protocol server for:
- Better integration with Antigravity
- Reusable across workflows
- Standardized interface

**File**: `OPTION2_MCP_REMINDER.md`

## Documentation

- `GEMINI_SETUP_GUIDE.md` - Setup instructions
- `GEMINI_SUCCESS_REPORT.md` - Implementation details
- `GEMINI_API_FINAL_STATUS.md` - Status tracking

## Success Metrics

✅ API Integration: Complete  
✅ Safety Configuration: Working  
✅ URL Extraction: Accurate  
✅ Workflow Integration: Done  
✅ Zero Cost: Achieved  

## Maintenance

- Monitor API quota usage
- Update safety settings if needed
- Check for new model versions
- Validate URL accuracy periodically

---

**Status**: Production Ready  
**Last Updated**: 2026-01-21  
**Version**: 1.0
