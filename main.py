import json
import requests
import os
import time
import re
from datetime import datetime
from bs4 import BeautifulSoup

def load_config():
    """Load configuration from config.json"""
    with open('config.json', 'r') as f:
        return json.load(f)

def load_price_history():
    """Load price history from price_history.json"""
    try:
        with open('price_history.json', 'r') as f:
            content = f.read().strip()
            return json.loads(content) if content else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_price_history(history):
    """Save price history to price_history.json"""
    with open('price_history.json', 'w') as f:
        json.dump(history, f, indent=2)

def fetch_price(url):
    """Fetch price from Costco (API or product page)"""
    try:
        # Check if it's an API URL
        if 'gdx-api.costco.com' in url or 'display-price-lite' in url:
            return fetch_price_from_api(url)
        else:
            return fetch_price_from_page(url)
    except Exception as e:
        print(f"  ❌ Error fetching price: {e}")
        return None

def fetch_price_from_api(url):
    """Fetch price from Costco API"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.costco.com/'
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    # Extract price from nested response structure
    if 'priceData' in data and 'displayPrice' in data['priceData']:
        display_price = data['priceData']['displayPrice']
        # Try to get online price first, then delivered price
        price = display_price.get('onlinePrice') or display_price.get('deliveredPrice')
        if price:
            return float(price)
    
    # Fallback: check for direct displayPrice field
    if 'displayPrice' in data:
        price_str = str(data['displayPrice']).replace('$', '').replace(',', '')
        return float(price_str)
    
    return None

def fetch_price_from_page(url):
    """Fetch price from Costco product page"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.costco.com/'
    }
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Method 1: Try to find price using data-testid attribute
    price_element = soup.find(attrs={'data-testid': 'Text_single-price-whole-value'})
    if price_element:
        price_text = price_element.get_text(strip=True)
        # Remove dollar sign and commas
        price_text = price_text.replace('$', '').replace(',', '')
        return float(price_text)
    
    # Method 2: Try to find price in JSON-LD structured data
    scripts = soup.find_all('script', type='application/ld+json')
    for script in scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and data.get('@type') == 'Product':
                if 'offers' in data and 'price' in data['offers']:
                    return float(data['offers']['price'])
        except (json.JSONDecodeError, KeyError, ValueError):
            continue
    
    # Method 3: Search for price patterns in the HTML
    price_pattern = r'data-testid="Text_single-price-whole-value"[^>]*>[\s]*\$?([\d,]+\.?\d*)'
    match = re.search(price_pattern, html_content)
    if match:
        price_text = match.group(1).replace(',', '')
        return float(price_text)
    
    print(f"  ⚠️  Could not find price on page")
    return None

def create_github_issue(item_name, old_price, new_price, item_id):
    """Create a GitHub issue for price change notification"""
    github_token = os.getenv('GITHUB_TOKEN')
    repo = os.getenv('GITHUB_REPOSITORY')
    
    if not github_token or not repo:
        print("GitHub token or repository not found in environment")
        return
    
    title = f"🔔 Price Change Alert: {item_name}"
    body = f"""## Price Change Detected!

**Item:** {item_name}  
**Item ID:** {item_id}  
**Previous Price:** ${old_price:.2f}  
**Current Price:** ${new_price:.2f}  
**Change:** ${new_price - old_price:.2f} ({((new_price - old_price) / old_price * 100):.2f}%)  
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
*This issue was automatically created by the Costco Price Tracker*
"""
    
    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'title': title,
        'body': body,
        'labels': ['price-alert']
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"✅ GitHub issue created for {item_name}")
    except Exception as e:
        print(f"❌ Error creating GitHub issue: {e}")

def check_prices():
    """Main function to check all prices"""
    config = load_config()
    history = load_price_history()
    price_changes = []
    
    print("🔍 Checking Costco prices...")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    for item in config['items']:
        item_name = item['name']
        item_id = item['item_id']
        url = item['url']
        
        print(f"Checking: {item_name} (ID: {item_id})")
        
        current_price = fetch_price(url)
        
        if current_price is None:
            print(f"  ⚠️  Could not fetch price\n")
            continue
        
        print(f"  💰 Current price: ${current_price:.2f}")
        
        # Check if we have historical data for this item
        if item_id in history:
            old_price = history[item_id]['price']
            
            if old_price != current_price:
                print(f"  🔔 PRICE CHANGE! Old: ${old_price:.2f} → New: ${current_price:.2f}")
                price_changes.append({
                    'name': item_name,
                    'item_id': item_id,
                    'old_price': old_price,
                    'new_price': current_price
                })
                
                # Create GitHub issue if notifications are enabled
                if config.get('notification', {}).get('enabled', False):
                    create_github_issue(item_name, old_price, current_price, item_id)
            else:
                print(f"  ✓ No change")
        else:
            print(f"  📝 First time tracking this item")
        
        # Update history
        history[item_id] = {
            'name': item_name,
            'price': current_price,
            'last_checked': datetime.now().isoformat()
        }
        print()
        
        # Add a small delay between requests to avoid rate limiting
        time.sleep(2)
    
    # Save updated history
    save_price_history(history)
    
    # Summary
    if price_changes:
        print(f"\n🎯 Summary: {len(price_changes)} price change(s) detected!")
        for change in price_changes:
            diff = change['new_price'] - change['old_price']
            pct = (diff / change['old_price']) * 100
            print(f"  - {change['name']}: ${change['old_price']:.2f} → ${change['new_price']:.2f} ({pct:+.2f}%)")
    else:
        print("\n✅ No price changes detected.")

if __name__ == '__main__':
    check_prices()
