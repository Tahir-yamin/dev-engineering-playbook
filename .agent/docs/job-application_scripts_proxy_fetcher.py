"""
Free Proxy Fetcher for JobSpy
Fetches working proxies from GitHub sources (ONLY for JobSpy usage)
"""
import requests
import random

def fetch_free_proxies(limit=20):
    """
    Fetch free proxies from GitHub sources
    Returns list of proxy strings in format 'ip:port'
    """
    proxies = []
    
    print("🔍 Fetching free proxies from GitHub...")
    
    # Source 1: ProxiFly (updated every 5 minutes)
    try:
        url = "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.json"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for proxy in data[:limit]:
                proxies.append(f"{proxy['ip']}:{proxy['port']}")
            print(f"✅ ProxiFly: Found {len(proxies)} proxies")
    except Exception as e:
        print(f"⚠️ ProxiFly failed: {e}")
    
    # Source 2: ProxyScraper (fallback)
    if len(proxies) < 10:
        try:
            url = "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/http.txt"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                lines = response.text.strip().split('\n')
                for line in lines[:limit]:
                    if ':' in line and line not in proxies:
                        proxies.append(line.strip())
                print(f"✅ ProxyScraper: Total {len(proxies)} proxies")
        except Exception as e:
            print(f"⚠️ ProxyScraper failed: {e}")
    
    # Shuffle for random distribution
    random.shuffle(proxies)
    
    return proxies[:limit]

if __name__ == "__main__":
    # Test the fetcher
    proxies = fetch_free_proxies(20)
    print(f"\n✅ Fetched {len(proxies)} proxies")
    print("Sample proxies:")
    for p in proxies[:5]:
        print(f"  - {p}")
