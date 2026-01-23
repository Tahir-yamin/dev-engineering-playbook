# Gemini Job Search Setup Guide

## 🚀 Quick Start (5 Minutes)

### Step 1: Get Your Free API Key

1. Go to: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy your API key

**Free Tier**: 1,500 requests/day (plenty for job searching!)

### Step 2: Set API Key (Choose ONE method)

**Method A: Environment Variable** (Recommended)
```powershell
# Windows PowerShell
$env:GEMINI_API_KEY="your-api-key-here"
```

**Method B: Pass Directly**
```bash
python gemini_job_searcher.py --api-key "your-api-key-here"
```

### Step 3: Test It!

```bash
# Basic test
python job-application/scripts/gemini_job_searcher.py

# Custom search
python job-application/scripts/gemini_job_searcher.py \
  --query "Senior Planning Engineer" \
  --location "Abu Dhabi" \
  --days 7
```

---

## 📋 Usage Examples

### Example 1: Default Search
```bash
cd d:\my-dev-knowledge-base
python job-application\scripts\gemini_job_searcher.py
```
**Searches**: Project Controls Manager OR Planning Manager in Dubai (last 7 days)

### Example 2: Custom Role & Location
```bash
python job-application\scripts\gemini_job_searcher.py \
  --query "Project Controls Manager" \
  --location "Riyadh, Saudi Arabia" \
  --days 14
```

### Example 3: Qatar Jobs
```bash
python job-application\scripts\gemini_job_searcher.py \
  --query "Planning Engineer" \
  --location "Doha, Qatar" \
  --days 7
```

---

## 📦 Output

**File**: `d:\my-dev-knowledge-base\job-application\data\gemini_jobs.json`

**Format**:
```json
[
  {
    "title": "Senior Project Controls Manager",
    "company": "Wood Group",
    "location": "Abu Dhabi",
    "url": "https://careers.woodplc.com/jobs/12345/apply"
  }
]
```

---

## 🔗 Integration with Workflow

### Manual Use:
1. Run `gemini_job_searcher.py`
2. Open `gemini_jobs.json`
3. Use URLs in `apply_job.py --url`

### Automated (Future):
```bash
# Search
python gemini_job_searcher.py

# Generate applications
python apply_from_gemini_results.py
```

---

## ⚠️ Troubleshooting

### "API key required"
- Set `GEMINI_API_KEY` environment variable
- Or pass `--api-key` argument

### "No jobs found"
- Try broader search query
- Increase `--days` parameter
- Check internet connection

### "Failed to parse JSON"
- This is rare - Gemini usually returns valid JSON
- Re-run the search
- If persists, file might have non-JSON content

---

## 💡 Tips

1. **Be specific** with location: "Dubai, UAE" better than just "Dubai"
2. **Date range**: 7 days is good, 14 if you want more results
3. **Query**: Use OR for multiple roles: "Project Controls OR Planning"
4. **Free tier**: 1,500 requests/day = ~50 searches/day with retries

---

## 📊 What's Next?

After testing successfully:
1. ✅ Verify URLs work (click them!)
2. ✅ Use URLs in job applications
3. ✅ Run weekly for new postings
4. 📌 Consider Option 2 (MCP Server) for better integration

Reminder file: `OPTION2_MCP_REMINDER.md`
