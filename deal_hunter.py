import requests
from bs4 import BeautifulSoup
import time

def hunt_for_deals(url, max_price):
    print(f"🕵️‍♂️ Scanning {url} for deals under ${max_price}...\n")
    
    # We use a very specific User-Agent to pretend we are a real Chrome browser on a Mac
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Website blocked us or is down. Status Code: {response.status_code}")
            return
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # ⚠️ THE TRICKY PART: Every website names their HTML code differently.
        # You have to Right-Click -> "Inspect" on the website to find the exact class names.
        # For this example, let's pretend the site uses standard classes like 'item-title' and 'item-price'.
        
        # Find all the "cards" or "blocks" containing items
        items = soup.find_all('div', class_='listing-card') # Change 'listing-card' to match the actual site
        
        if not items:
            print("⚠️ No items found. We probably need to update the HTML class names for this specific site.")
            return

        found_deals = 0
        
        for item in items:
            # Extract the title
            title_element = item.find('h2', class_='item-title')
            title = title_element.text.strip() if title_element else "Unknown Item"
            
            # Extract the price
            price_element = item.find('span', class_='item-price')
            if price_element:
                price_text = price_element.text.strip()
                # Clean up the price (remove '$' and commas to turn it into a real math number)
                clean_price = price_text.replace('$', '').replace(',', '')
                
                try:
                    price_value = float(clean_price)
                    
                    # CHECK IF IT'S A DIRT CHEAP DEAL!
                    if price_value <= max_price:
                        print(f"🚨 DEAL ALERT: {title}")
                        print(f"💰 Price: ${price_value}")
                        print("-" * 30)
                        found_deals += 1
                except ValueError:
                    continue # Skip if the price says "Call for price" or something weird
                    
        print(f"🏁 Scan complete. Found {found_deals} deals matching your criteria.")
        
    except Exception as e:
        print(f"❌ An error occurred: {e}")

# --- Run the Hunter ---
# Note: This is a placeholder URL. You will need to put in the actual site you want to scrape!
target_site = "https://example-equipment-site.com/used-excavators" 
budget_limit = 25000.00 # Set your "dirt cheap" threshold

hunt_for_deals(target_site, budget_limit)
