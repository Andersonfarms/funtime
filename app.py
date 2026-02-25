# ==========================================
# DHI // DATA-LINK v0.1
# System Engineered by: NyssaFire Gaming & Michael Anderson @ Anderson Farms
# Core Uplink Established: 2026-02-25 // 12:15 CST
# ==========================================
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

# A set to keep track of where we have already been (so we don't go in circles)
visited_urls = set()

def crawl_and_hunt(url, max_pages=10):
    # Stop if we've hit our limit or already visited this page
    if len(visited_urls) >= max_pages or url in visited_urls:
        return
    
    print(f"🕸️ Crawling: {url}")
    visited_urls.add(url)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code != 200:
            return
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # --- THE HUNTER: Look for keywords ---
        page_text = soup.get_text().lower()
        keywords = ["barn find", "must haul away", "free to a good home", "liquidation"]
        
        for word in keywords:
            if word in page_text:
                print(f"🚨 POTENTIAL DEAL FOUND on {url} (Trigger: '{word}')")
                print("-" * 40)
                break # Only flag the page once
                
        # --- THE SPIDER: Find new links to crawl next ---
        links = soup.find_all('a', href=True)
        for link in links:
            # Join relative links (like '/category/tools') into full URLs
            next_url = urljoin(url, link['href'])
            
            # Basic rule: Only crawl links on the same website for now to avoid wandering into the abyss
            if urlparse(next_url).netloc == urlparse(url).netloc:
                if next_url not in visited_urls:
                    time.sleep(1) # Be polite, don't crash their server
                    crawl_and_hunt(next_url, max_pages) # Recursion: The crawler calls itself!
                    
    except Exception as e:
        print(f"⚠️ Failed to crawl {url}: {e}")

# Drop the spider on a seed URL (Replace with a real message board or classified site)
seed_url = "https://news.ycombinator.com/" 
crawl_and_hunt(seed_url, max_pages=5)
