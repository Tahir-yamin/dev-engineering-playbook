"""
Apply From Gemini Results - FIXED
Generates job applications from Gemini API search results
"""
import json
import os
import subprocess
from pathlib import Path

def load_gemini_results():
    """Load jobs from Gemini search results"""
    results_file = Path("d:/my-dev-knowledge-base/job-application/data/gemini_jobs.json")
    
    if not results_file.exists():
        print("No Gemini results found!")
        print(f"   Run: python gemini_job_searcher_simple.py first")
        return []
    
    with open(results_file, 'r', encoding='utf-8') as f:
        jobs = json.load(f)
    
    return jobs

def generate_application(job):
    """Generate application for a single job"""
    print(f"\nGenerating application for: {job['title']} @ {job['company']}")
    
    # Build apply_job.py command with CORRECT arguments
    cmd = [
        "python",
        "job-application/scripts/apply_job.py",
        "--company", job['company'],
        "--role", job['title'],  # Fixed: was --job-title, should be --role
        "--website",  # Fixed: was --method website, should be --website flag
        "--url", job['url']
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"SUCCESS - Application generated")
            return True
        else:
            print(f"ERROR: {result.stderr}")
            return False
    except Exception as e:
        print(f"Exception: {e}")
        return False

def main():
    print("Gemini to Applications Generator")
    print("=" * 60)
    
    # Load results
    jobs = load_gemini_results()
    
    if not jobs:
        print("\nNo jobs to process")
        return
    
    print(f"\nFound {len(jobs)} jobs from Gemini search")
    print("=" * 60)
    
    # Show jobs
    for idx, job in enumerate(jobs, 1):
        print(f"\n{idx}. {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   URL: {job['url'][:60]}...")
    
    # Confirm
    print("\n" + "=" * 60)
    response = input(f"\nGenerate applications for all {len(jobs)} jobs? (y/n): ")
    
    if response.lower() != 'y':
        print("Cancelled")
        return
    
    # Generate applications
    print("\n" + "=" * 60)
    print("Generating applications...")
    print("=" * 60)
    
    successful = 0
    failed = 0
    
    for job in jobs:
        if generate_application(job):
            successful += 1
        else:
            failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Output: job-application/output/")
    print("=" * 60)

if __name__ == "__main__":
    main()
