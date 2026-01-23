# LinkedIn Auto-Extraction (Browser Console)

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
    
    console.log(`\n📊 Found ${posts.length} hiring posts`);
    console.log('\n📋 Results (copy below):');
    console.log(JSON.stringify(posts, null, 2));
    
    // Also copy to clipboard if possible
    if (navigator.clipboard) {
        navigator.clipboard.writeText(JSON.stringify(posts, null, 2));
        console.log('\n✅ Results copied to clipboard!');
    }
    
    return posts;
})();
```

## After Running:

1. Copy the JSON output
2. Save to: `job-application/data/linkedin_extracted.json`
3. Run: `python linkedin_process_extracted.py`

