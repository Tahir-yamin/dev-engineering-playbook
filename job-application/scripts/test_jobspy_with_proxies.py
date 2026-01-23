"""
JobSpy Test with FREE Proxies
Tests exact URL extraction for Middle East jobs using GitHub proxy sources
"""
import csv
import sys
from jobspy import scrape_jobs

# Import our proxy fetcher
sys.path.append('d:\\my-dev-knowledge-base\\job-application\\scripts')
from proxy_fetcher import fetch_free_proxies

print("🚀 JobSpy Test with FREE GitHub Proxies")
print("=" * 60)

# Fetch proxies
print("\n📥 Step 1: Fetching free proxies...")
proxies = fetch_free_proxies(limit=15)

if len(proxies) == 0:
    print("❌ No proxies available. Test cannot proceed.")
    sys.exit(1)

print(f"✅ Got {len(proxies)} proxies to try")
print("=" * 60)

# Test JobSpy with proxies
print("\n🔍 Step 2: Searching jobs with proxy rotation...")
print("Target: Project Controls Manager in Dubai")

try:
    jobs = scrape_jobs(
        site_name=["indeed"],  # Test with Indeed first
        search_term="Project Controls Manager",
        location="Dubai",
        results_wanted=5,
        country_indeed='United Arab Emirates',
        proxies=proxies  # Use free proxies!
    )
    
    print(f"\n✅ SUCCESS! Found {len(jobs)} jobs!")
    print("=" * 60)
    
    if len(jobs) > 0:
        print("\n📊 Results with EXACT URLs:")
        for idx, row in jobs.iterrows():
            print(f"\n{idx+1}. {row['title']}")
            print(f"   Company: {row['company']}")
            print(f"   Location: {row['location']}")
            print(f"   🔗 EXACT URL: {row['job_url']}")
        
        # Save results
        output_file = "d:\\my-dev-knowledge-base\\job-application\\data\\jobspy_with_proxies_results.csv"
        jobs.to_csv(output_file, quoting=csv.QUOTE_NONNUMERIC, escapechar='\\', index=False)
        print(f"\n💾 Saved to: {output_file}")
        
        # Success summary
        print("\n" + "=" * 60)
        print("🎉 FREE PROXIES WORKED!")
        print(f"   - Extracted {len(jobs)} exact job URLs")
        print(f"   - Using {len(proxies)} free GitHub proxies")
        print(f"   - Zero cost solution")
        print("=" * 60)
    else:
        print("\n⚠️ No jobs found (search returned 0 results)")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nThis could mean:")
    print("- All proxies failed (tried {})".format(len(proxies)))
    print("- Indeed still blocking despite proxies")
    print("- Need to try LinkedIn instead")
    
    import traceback
    traceback.print_exc()
