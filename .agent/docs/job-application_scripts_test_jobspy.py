"""
JobSpy Test - Extract Exact Job URLs
Testing for Middle East Project Controls positions
"""
import csv
from jobspy import scrape_jobs

print("🔍 Searching for Project Controls jobs in UAE...")
print("=" * 60)

try:
    jobs = scrape_jobs(
        site_name=["indeed"],  # Indeed is supported in version 1.1.13
        search_term="Project Controls Manager",
        location="Dubai",
        results_wanted=10,  # Small test batch
        country_indeed='United Arab Emirates'
    )
    
    print(f"\n✅ Found {len(jobs)} jobs!")
    print("=" * 60)
    
    if len(jobs) > 0:
        print("\n📊 Sample Results:")
        print(jobs[['site', 'title', 'company', 'location', 'job_url']].head(10))
        
        # Save to CSV
        output_file = "d:\\my-dev-knowledge-base\\job-application\\data\\jobspy_test_results.csv"
        jobs.to_csv(output_file, quoting=csv.QUOTE_NONNUMERIC, escapechar='\\', index=False)
        print(f"\n💾 Saved to: {output_file}")
        
        # Show exact URLs
        print("\n🔗 EXACT JOB URLs EXTRACTED:")
        print("=" * 60)
        for idx, row in jobs.iterrows():
            print(f"{idx+1}. {row['title']}")
            print(f"   Company: {row['company']}")
            print(f"URL: {row['job_url']}")
            print()
    else:
        print("⚠️ No jobs found. This might be due to:")
        print("- Bayt/Indeed blocking the request")
        print("- No jobs matching criteria in last 7 days")
        print("- Geographic restrictions")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
