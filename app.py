import requests
from bs4 import BeautifulSoup

def crawl_website(url):
    print(f"🚀 Crawling: {url}")
    
    # 1. Send a request to the website
    # We add a 'User-Agent' header so the website thinks we are a normal browser, not a bot
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful (Status code 200)
    if response.status_code == 200:
        # 2. Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 3. Find what you are looking for!
        # Example A: Find the main title of the page
        page_title = soup.title.text if soup.title else "No Title Found"
        print(f"📄 Title: {page_title}")
        
        # Example B: Find all the links (<a> tags) on the page
        print("\n🔗 Found Links:")
        links = soup.find_all('a')
        
        # Print the first 5 links we find
        for link in links[:5]:
            href = link.get('href')
            text = link.text.strip()
            if href:
                print(f"- {text}: {href}")
                
        # Return the data as a dictionary
        return {"title": page_title, "url": url}
        
    else:
        print(f"❌ Failed to retrieve the page. Status code: {response.status_code}")
        return None

# Run the crawler
target_url = "https://news.ycombinator.com/" # Hacker News is a great site to test on
crawled_data = crawl_website(target_url)
