# LinkedIn Job Post Extraction Instructions

**Generated**: 2026-01-21 23:33:22

## 🎯 Goal
Extract job posts and application URLs from LinkedIn searches

## 📋 Process

### Step 1: Login to LinkedIn
1. Open browser
2. Go to https://linkedin.com
3. Login with your credentials

### Step 2: Search Each URL

**For each URL below**:
1. Click the link
2. Look for posts containing:
   - "hiring" / "looking for" / "we're hiring"
   - Job titles: Project Controls, Planning Manager, etc.
   - Company names
   - Application links

3. For each job post found:
   - Copy the company name
   - Copy the job title
   - Copy any application URL mentioned
   - Save to the list below

---

## 🔍 Search URLs


### 1. Hiring Project Planning Engineer

**URL**: https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Hiring%20Project%20Planning%20Engineer

**Jobs Found**:
_(Add below)_

```
Company: 
Role: 
URL: 
Notes: 
---
```


### 2. Looking for a Planning

**URL**: https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Looking%20for%20a%20Planning

**Jobs Found**:
_(Add below)_

```
Company: 
Role: 
URL: 
Notes: 
---
```


### 3. Hiring for planning

**URL**: https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Hiring%20for%20planning

**Jobs Found**:
_(Add below)_

```
Company: 
Role: 
URL: 
Notes: 
---
```


### 4. planning & Scheduling

**URL**: https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=planning%20%26%20Scheduling

**Jobs Found**:
_(Add below)_

```
Company: 
Role: 
URL: 
Notes: 
---
```


### 5. Project control

**URL**: https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Project%20control

**Jobs Found**:
_(Add below)_

```
Company: 
Role: 
URL: 
Notes: 
---
```


### 6. project planning

**URL**: https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=project%20planning

**Jobs Found**:
_(Add below)_

```
Company: 
Role: 
URL: 
Notes: 
---
```


### 7. project controls engineer

**URL**: https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=project%20controls%20engineer

**Jobs Found**:
_(Add below)_

```
Company: 
Role: 
URL: 
Notes: 
---
```


### 8. project controls engineer

**URL**: https://www.linkedin.com/search/results/content/?keywords=project%20controls%20engineer

**Jobs Found**:
_(Add below)_

```
Company: 
Role: 
URL: 
Notes: 
---
```


---

## 📝 Alternative: Copy-Paste Method

If you find posts without clear URLs:

1. Copy the entire post text
2. Look for contact information (email, LinkedIn profile)
3. Save to file: `linkedin_manual_jobs.txt`

Format:
```
POST 1:
Company: [Name]
Contact: [Email or LinkedIn]
Post: [Full text]
---
```

---

## ✅ After Collection

Once you have all jobs, run:

```bash
# Convert to applications
python job-application\scripts\linkedin_to_applications.py
```

This will process your findings and generate applications.
