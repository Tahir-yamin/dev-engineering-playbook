"""
Simple Job Scraper with Free Proxies
Uses free GitHub proxies to scrape job URLs directly (no JobSpy dependency)
"""
import requests
import random
from bs4 import BeautifulSoup
import json
from proxy_fetcher import fetch_free_proxies

def test_proxy(proxy):
    """Test if a proxy works"""
    try:
        response = requests.get(
            "https://httpbin.org/ip", 
            proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
            timeout=5
        )
        return response.status_code == 200
    except:
        return False

def scrape_indeed_dubai_with_proxy(proxy):
    """
    Scrape Indeed UAE for Project Controls jobs using a proxy
    Returns list of job URLs
    """
    try:
        url = "https://ae.indeed.com/jobs?q=Project+Controls+Manager&l=Dubai"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        proxies_dict = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        
        response = requests.get(url, headers=headers, proxies=proxies_dict, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            jobs = []
            # Indeed job links have class 'jcs-JobTitle'
            job_links = soup.find_all('a', class_='jcs-JobTitle')
            
            for link in job_links[:5]:
                job_url = "https://ae.indeed.com" + link.get('href', '')
                job_title = link.get_text(strip=True)
                jobs.append({
                    'title': job_title,
                    'url': job_url,
                    'source': 'Indeed UAE',
                    'proxy_used': proxy
                })
            
            return jobs
        else:
            return None
            
    except Exception as e:
        return None

def main():
    print("🚀 Custom Job Scraper with FREE Proxies")
    print("=" * 60)
    
    # Get free proxies
    print("\n📥 Fetching proxies...")
    proxies = fetch_free_proxies(20)
    
    if not proxies:
        print("❌ No proxies available")
        return
    
    print(f"✅ Got {len(proxies)} proxies")
    
    # Test and find working proxies
    print("\n🧪 Testing proxies...")
    working_proxies = []
    for proxy in proxies[:10]:  # Test first 10
        if test_proxy(proxy):
            working_proxies.append(proxy)
            print(f"✅ {proxy} - Working")
            if len(working_proxies) >= 3:  # We only need a few
                break
        else:
            print(f"❌ {proxy} - Failed")
    
    if not working_proxies:
        print("\n❌ No working proxies found")
        return
    
    print(f"\n✅ Found {len(working_proxies)} working proxies")
    
    # Try scraping with working proxies
    print("\n🔍 Scraping Indeed UAE...")
    all_jobs = []
    
    for proxy in working_proxies:
        print(f"\nTrying proxy: {proxy}")
        jobs = scrape_indeed_dubai_with_proxy(proxy)
        
        if jobs:
            print(f"✅ SUCCESS! Found {len(jobs)} jobs")
            all_jobs.extend(jobs)
            break  # We got results, stop trying
        else:
            print(f"❌ Failed with this proxy")
    
    if all_jobs:
        print("\n" + "=" * 60)
        print("🎉 RESULTS - EXACT JOB URLs:")
        print("=" * 60)
        
        for idx, job in enumerate(all_jobs, 1):
            print(f"\n{idx}. {job['title']}")
            print(f"   🔗 URL: {job['url']}")
            print(f"   Using proxy: {job['proxy_used']}")
        
        # Save to file
        output_file = "d:\\my-dev-knowledge-base\\job-application\\data\\scraped_jobs_with_proxies.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_jobs, f, indent=2)
        
        print(f"\n💾 Saved to: {output_file}")
        print("\n" + "=" * 60)
        print("✅ FREE PROXY SCRAPING WORKED!")
        print(f"   - Got {len(all_jobs)} exact job URLs")
        print(f"   - Using free GitHub proxies")
        print(f"   - Zero cost")
        print("=" * 60)
    else:
        print("\n❌ All proxies failed to scrape jobs")
        print("Recommendation: Stick with current stable method (search pages)")

if __name__ == "__main__":
    main()
