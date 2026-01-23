"""
LinkedIn Auto Post Extractor
Uses browser automation to extract job posts and URLs from LinkedIn searches
"""

import time
from pathlib import Path
import json
from datetime import datetime

# LinkedIn search URLs
LINKEDIN_SEARCHES = [
    "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Hiring%20Project%20Planning%20Engineer",
    "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Looking%20for%20a%20Planning",
    "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Hiring%20for%20planning",
    "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=planning%20%26%20Scheduling",
    "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=Project%20control",
    "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=project%20planning",
    "https://www.linkedin.com/search/results/content/?datePosted=%22past-week%22&keywords=project%20controls%20engineer",
    "https://www.linkedin.com/search/results/content/?keywords=project%20controls%20engineer"
]

def create_extraction_instructions():
    """Create instructions file for manual extraction with browser"""
    
    instructions = f"""# LinkedIn Job Post Extraction Instructions

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

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

"""
    
    for idx, url in enumerate(LINKEDIN_SEARCHES, 1):
        keyword = url.split("keywords=")[1].split("&")[0].replace("%20", " ").replace("%22", "").replace("%26", "&")
        
        instructions += f"""
### {idx}. {keyword}

**URL**: {url}

**Jobs Found**:
_(Add below)_

```
Company: 
Role: 
URL: 
Notes: 
---
```

"""
    
    instructions += """
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
python job-application\\scripts\\linkedin_to_applications.py
```

This will process your findings and generate applications.
"""
    
    # Save instructions
    output_file = Path("job-application/data/linkedin_extraction_guide.md")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    return str(output_file)

def create_browser_automation_script():
    """Create browser automation helper (requires user to be logged in)"""
    
    script = """# LinkedIn Auto-Extraction (Browser Console)

## How to Use:

1. Login to LinkedIn
2. Go to any search URL from the list
3. Open browser console (F12)
4. Paste this script and press Enter
5. Wait for extraction
6. Copy results

## Script:

```javascript
// LinkedIn Post Extractor
(function() {
    console.log('🔍 Extracting LinkedIn posts...');
    
    const posts = [];
    const feedItems = document.querySelectorAll('div.feed-shared-update-v2');
    
    feedItems.forEach((item, index) => {
        try {
            // Get post text
            const textElement = item.querySelector('.feed-shared-inline-show-more-text, .feed-shared-text__text-view');
            const text = textElement ? textElement.innerText : '';
            
            // Check if it's a hiring post
            const hiringKeywords = ['hiring', 'looking for', 'join our team', 'we are hiring', 'opportunity'];
            const isHiringPost = hiringKeywords.some(keyword => text.toLowerCase().includes(keyword));
            
            if (isHiringPost) {
                // Get author
                const author = item.querySelector('.feed-shared-actor__name')?.innerText || 'Unknown';
                
                // Get links
                const links = Array.from(item.querySelectorAll('a[href]'))
                    .map(a => a.href)
                    .filter(href => href.includes('http') && !href.includes('linkedin.com/feed'));
                
                posts.push({
                    author: author,
                    text: text.substring(0, 200) + '...',
                    links: links,
                    fullText: text
                });
                
                console.log(`✅ Found post ${posts.length} by ${author}`);
            }
        } catch(e) {
            console.error('Error processing item:', e);
        }
    });
    
    console.log(`\\n📊 Found ${posts.length} hiring posts`);
    console.log('\\n📋 Results (copy below):');
    console.log(JSON.stringify(posts, null, 2));
    
    // Also copy to clipboard if possible
    if (navigator.clipboard) {
        navigator.clipboard.writeText(JSON.stringify(posts, null, 2));
        console.log('\\n✅ Results copied to clipboard!');
    }
    
    return posts;
})();
```

## After Running:

1. Copy the JSON output
2. Save to: `job-application/data/linkedin_extracted.json`
3. Run: `python linkedin_process_extracted.py`

"""
    
    output_file = Path("job-application/data/linkedin_browser_script.md")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(script)
    
    return str(output_file)

def main():
    print("\n🔗 LinkedIn Auto-Extraction Setup")
    print("=" * 60)
    
    # Create instruction file
    instructions_file = create_extraction_instructions()
    print(f"\n✅ Created extraction guide:")
    print(f"   {instructions_file}")
    
    # Create browser script
    browser_script = create_browser_automation_script()
    print(f"\n✅ Created browser automation script:")
    print(f"   {browser_script}")
    
    print("\n" + "=" * 60)
    print("\n💡 Two Methods Available:")
    print("\n1. **Manual Method**:")
    print(f"   - Open: {instructions_file}")
    print("   - Click each URL and manually extract jobs")
    print("   - Fill in the template")
    
    print("\n2. **Browser Console Method** (Faster):")
    print(f"   - Open: {browser_script}")
    print("   - Follow the script instructions")
    print("   - Paste in browser console on LinkedIn pages")
    print("   - Auto-extracts posts")
    
    print("\n" + "=" * 60)
    print("\n🚀 Quick Start:")
    print("   1. Login to LinkedIn")
    print("   2. Use browser console script for each URL")
    print("   3. Collect all results")
    print("   4. Generate applications")
    print("=" * 60)

if __name__ == "__main__":
    main()
