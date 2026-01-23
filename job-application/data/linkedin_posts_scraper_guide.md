# LinkedIn Posts Job Scraper - Usage Guide

## ✅ What's Ready

**File**: `linkedin_posts_scraper.py`
**Purpose**: Scrapes LinkedIn **POSTS** (not job board) where people share job openings
**Last 7 Days**: Automatically filters to past week only

---

## 🎯 Exact URLs It Scrapes

Based on your LinkedIn searches:

1. **Project control** posts
2. **project planning** posts
3. **planning & Scheduling** posts
4. **Looking for a Planning** posts

All filtered to: **Last 7 days only**

---

## 🚀 How to Run

### Step 1: Login to LinkedIn

Open LinkedIn in Chrome and login. Keep the browser open.

### Step 2: Run the Scraper

```bash
python d:\my-dev-knowledge-base\job-application\scripts\linkedin_posts_scraper.py
```

### Step 3: What Happens

- Opens Chrome browser (you'll see it)
- Opens your 4 LinkedIn search URLs
- Reads posts from the feed
- Extracts posts that mention:
  - Hiring keywords: "looking for", "urgent requirement", "send CV", etc.
  - Target roles: Project Controls, Planning Manager, Scheduler, etc.
  - Locations: UAE, Qatar, Saudi, etc.

### Step 4: Results

Gets saved to:
```
d:\my-dev-knowledge-base\job-application\data\linkedin_posts_jobs.json
```

---

## 📊 What It Finds

Example output from a post:
```json
{
  "company": "AECOM",
  "role": "Senior Planning Engineer",
  "location": "UAE",
  "post_text": "We are urgently looking for a Senior Planning Engineer...",
  "scraped_at": "2026-01-21T15:35:00"
}
```

---

## 🔄 Auto-Application Workflow

### After Scraping:

```bash
# Read the results
cat d:\my-dev-knowledge-base\job-application\data\linkedin_posts_jobs.json

# For each job found, auto-apply:
python apply_job.py --company "COMPANY_NAME" --role "ROLE" --website
```

Or tell me: **"Apply to all scraped jobs"** and I'll do it automatically!

---

## ⚠️ Important Notes

1. **Browser will open**: You'll see Chrome browser working
2. **Login required**: LinkedIn needs you to be logged in
3. **Takes 2-3 minutes**: Scrapes 4 searches with 10 posts each
4. **Smart filtering**: Only extracts relevant hiring posts

---

## 🎯 Keywords It Looks For

### Hiring Keywords:
- "hiring", "looking for", "we are hiring"
- "urgent requirement", "immediate hiring"
- "vacancy", "position available"
- "send cv", "apply now", "dm me"

### Target Roles:
- Project Control, Planning Manager
- Planning Engineer, Scheduler
- Project Planner, Senior Planning

### Locations:
- UAE, Dubai, Abu Dhabi
- Qatar, Doha
- Saudi, Riyadh, KSA

---

## 💡 Alternative: I Can Search For You

If you don't want to run the scraper, just say:

**"Search LinkedIn posts for planning jobs last 7 days"**

I'll use web API (faster, no browser) and auto-generate applications!

---

**Created**: 2026-01-21
**Status**: Ready to use
