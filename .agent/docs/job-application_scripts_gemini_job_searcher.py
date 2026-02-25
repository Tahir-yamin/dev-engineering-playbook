"""
Gemini Job Searcher - Option 1 Direct Integration
Uses Google Gemini API with search grounding to find exact job URLs

Setup:
1. Get API key from: https://aistudio.google.com/app/apikey
2. Set environment variable: GEMINI_API_KEY=your_key
   OR
   Pass directly: python gemini_job_searcher.py --api-key your_key
"""
import os
import json
import argparse
from datetime import datetime

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("❌ Error: google-genai not installed")
    print("Run: pip install google-genai")
    exit(1)

def search_jobs_with_gemini(query, location, days=7, api_key=None):
    """
    Search for jobs using Gemini API with search grounding
    
    Args:
        query: Job title/role (e.g., "Project Controls Manager")
        location: City/Country (e.g., "Dubai, UAE")
        days: Jobs posted in last X days
        api_key: Gemini API key
    
    Returns:
        List of job dictionaries with title, company, location, url
    """
    # Configure API
    if not api_key:
        api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        raise ValueError("API key required. Set GEMINI_API_KEY env var or pass --api-key")
    
    # Create client with new SDK
    client = genai.Client(api_key=api_key)
    
    # Construct search prompt
    prompt = f"""
Search Google for "{query} jobs in {location} posted in last {days} days"

Find REAL job postings from company career pages or job boards (LinkedIn, Indeed, Bayt, GulfTalent, etc).

For each job found, extract:
1. Job Title
2. Company Name
3. Location (city)
4. Exact Job URL (the direct link to apply, NOT a search page)

Return ONLY a valid JSON array. No markdown, no explanations. Format:
[
  {{
    "title": "exact job title",
    "company": "company name",
    "location": "city",
    "url": "https://exact-job-url"
  }}
]

Find at least 5 jobs if available.
"""
    
    print(f"\n🔍 Searching with Gemini AI...")
    print(f"   Query: {query}")
    print(f"   Location: {location}")
    print(f"   Posted: Last {days} days")
    
    try:
        # Generate content using new SDK
        response = client.models.generate_content(
            model='gemini-pro',  # Stable model name
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1,
                response_modalities=['TEXT']
            )
        )
        
        # Parse response
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith('```'):
            # Extract JSON from markdown
            lines = response_text.split('\n')
            json_lines = []
            in_code_block = False
            for line in lines:
                if line.strip().startswith('```'):
                    in_code_block = not in_code_block
                    continue
                if in_code_block or (not line.strip().startswith('```')):
                    json_lines.append(line)
            response_text = '\n'.join(json_lines)
        
        # Parse JSON
        jobs = json.loads(response_text)
        
        return jobs
        
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse JSON response: {e}")
        print(f"Raw response: {response.text}")
        return []
    except Exception as e:
        print(f"❌ Error during search: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description='Search for jobs using Gemini API')
    parser.add_argument('--query', default='Project Controls Manager OR Planning Manager',
                        help='Job title or search query')
    parser.add_argument('--location', default='Dubai',
                        help='Location (city or country)')
    parser.add_argument('--days', type=int, default=7,
                        help='Jobs posted in last N days')
    parser.add_argument('--api-key', help='Gemini API key (or set GEMINI_API_KEY env var)')
    parser.add_argument('--output', default='d:\\my-dev-knowledge-base\\job-application\\data\\gemini_jobs.json',
                        help='Output file path')
    
    args = parser.parse_args()
    
    print("🚀 Gemini Job Search - Direct Integration")
    print("=" * 60)
    
    # Search
    jobs = search_jobs_with_gemini(
        query=args.query,
        location=args.location,
        days=args.days,
        api_key=args.api_key
    )
    
    if jobs:
        print(f"\n✅ Found {len(jobs)} jobs!")
        print("=" * 60)
        
        for idx, job in enumerate(jobs, 1):
            print(f"\n{idx}. {job.get('title', 'N/A')}")
            print(f"   Company: {job.get('company', 'N/A')}")
            print(f"   Location: {job.get('location', 'N/A')}")
            print(f"   🔗 URL: {job.get('url', 'N/A')}")
        
        # Save to file
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Saved to: {args.output}")
        print("\n" + "=" * 60)
        print("✅ SUCCESS - Exact job URLs extracted!")
        print("=" * 60)
        
    else:
        print("\n❌ No jobs found or error occurred")
        print("Check your API key and internet connection")

if __name__ == "__main__":
    main()
