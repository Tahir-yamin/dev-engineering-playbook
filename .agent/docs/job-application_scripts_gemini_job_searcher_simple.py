"""
Gemini Job Searcher - Official SDK Version
Uses google-genai SDK as per official documentation
"""
import os
import json
import argparse
from datetime import datetime

try:
    from google import genai
except ImportError:
    print("❌ Error: google-genai not installed")
    print("Run: pip install google-genai")
    exit(1)

def search_jobs_with_gemini(query, location, days=7, api_key=None):
    """Search for jobs using Gemini API with official SDK"""
    
    if not api_key:
        api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        raise ValueError("API key required. Set GEMINI_API_KEY env var or pass --api-key")
    
    # Create client with official google-genai SDK
    client = genai.Client(api_key=api_key)
    
    # Construct simpler prompt to avoid safety blocks
    prompt = f"""List 5 Project Controls Manager or Planning Manager job opportunities in {location} that were posted in the last week.

For each job, provide:
- Job Title
- Company Name
- City/Location  
- Application Website URL

Format as JSON array:
[{{"title": "Senior Project Controls Manager", "company": "ABC Company", "location": "Dubai", "url": "https://example.com/careers/job123"}}]"""
    
    print(f"\n🔍 Searching with Gemini AI...")
    print(f"   Query: {query}")
    print(f"   Location: {location}")
    print(f"   Days: {days}")
    
    try:
        # Use official SDK method with relaxed safety settings
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
            config={
                'safety_settings': [
                    {'category': 'HARM_CATEGORY_HARASSMENT', 'threshold': 'BLOCK_NONE'},
                    {'category': 'HARM_CATEGORY_HATE_SPEECH', 'threshold': 'BLOCK_NONE'},
                    {'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT', 'threshold': 'BLOCK_NONE'},
                    {'category': 'HARM_CATEGORY_DANGEROUS_CONTENT', 'threshold': 'BLOCK_NONE'},
                ]
            }
        )
        
        # Debug: Print response
        print(f"\n🔧 Debug: Response received")
        
        # Check prompt feedback first (if prompt itself was blocked)
        if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
            feedback = response.prompt_feedback
            if hasattr(feedback, 'block_reason') and feedback.block_reason:
                print(f"❌ Prompt was blocked: {feedback.block_reason}")
                raise ValueError(f"Prompt blocked by safety filter: {feedback.block_reason}")
        
        # Extract text from response
        if hasattr(response, 'text') and response.text:
            text = response.text
        elif hasattr(response, 'candidates') and len(response.candidates) > 0:
            candidate = response.candidates[0]
            
            # Check finish reason (based on research)
            finish_reason = candidate.finish_reason if hasattr(candidate, 'finish_reason') else None
            print(f"🔧 Finish reason: {finish_reason}")
            
            if finish_reason == "SAFETY":
                safety_info = candidate.safety_ratings if hasattr(candidate, 'safety_ratings') else "No details"
                print(f"❌ Response blocked by safety filter")
                print(f"   Safety ratings: {safety_info}")
                raise ValueError(f"Response blocked by safety filter. Try adjusting your prompt or safety settings.")
            
            # Handle empty parts safely (as per research recommendation)
            if hasattr(candidate, 'content') and candidate.content:
                parts = candidate.content.parts or []  # Use fallback for None
                if parts and len(parts) > 0:
                    text = parts[0].text
                else:
                    print(f"❌ Response has no content parts (empty)")
                    raise ValueError("Response completed but has no content. Model may have generated empty output.")
            else:
                print(f"❌ Candidate has no content attribute")
                raise ValueError("Response has no content")
        else:
            raise ValueError("No response candidates")
            
        text = text.strip()
        
        # Clean markdown if present
        if text.startswith('```'):
            lines = text.split('\n')
            json_lines = []
            in_code = False
            for line in lines:
                if line.strip().startswith('```'):
                    in_code = not in_code
                    continue
                if not in_code or not line.strip().startswith('```'):
                    json_lines.append(line)
            text = '\n'.join(json_lines).strip()
        
        # Parse JSON
        jobs = json.loads(text)
        return jobs
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON Parse Error: {e}")
        print(f"Raw response: {text if 'text' in locals() else 'No response'}")
        return []
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return []

def main():
    parser = argparse.ArgumentParser(description='Search jobs using Gemini API')
    parser.add_argument('--query', default='Project Controls Manager',
                        help='Job title or search query')
    parser.add_argument('--location', default='Dubai',
                        help='Location (city or country)')
    parser.add_argument('--days', type=int, default=7,
                        help='Jobs posted in last N days')
    parser.add_argument('--api-key', help='Gemini API key (or set GEMINI_API_KEY)')
    parser.add_argument('--output', 
                        default='d:\\my-dev-knowledge-base\\job-application\\data\\gemini_jobs.json',
                        help='Output JSON file path')
    
    args = parser.parse_args()
    
    print("🚀 Gemini Job Search - Official SDK")
    print("=" * 60)
    
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
        
        # Save to JSON
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Saved to: {args.output}")
        print("\n" + "=" * 60)
        print("✅ SUCCESS - Job URLs extracted!")
        print("=" * 60)
    else:
        print("\n❌ No jobs found or error occurred")

if __name__ == "__main__":
    main()
