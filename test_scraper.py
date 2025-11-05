import requests
import json
import re

def fetch_costco_page(url):
    """Fetch Costco product page and extract price information"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        print(f"🔍 Fetching URL: {url}\n")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        html_content = response.text
        
        # Method 1: Look for JSON-LD structured data
        print("=" * 80)
        print("Method 1: Searching for JSON-LD structured data...")
        print("=" * 80)
        json_ld_pattern = r'<script type="application/ld\+json">(.*?)</script>'
        json_ld_matches = re.findall(json_ld_pattern, html_content, re.DOTALL)
        
        for i, match in enumerate(json_ld_matches):
            try:
                data = json.loads(match)
                print(f"\n📦 JSON-LD Block {i+1}:")
                print(json.dumps(data, indent=2))
                
                # Look for price in the structured data
                if isinstance(data, dict):
                    if '@type' in data and data['@type'] == 'Product':
                        if 'offers' in data:
                            print(f"\n💰 FOUND PRICE IN JSON-LD: {data['offers']}")
            except json.JSONDecodeError:
                continue
        
        # Method 2: Look for JavaScript variables with price data
        print("\n" + "=" * 80)
        print("Method 2: Searching for JavaScript price variables...")
        print("=" * 80)
        
        # Common patterns for price in JavaScript
        price_patterns = [
            r'price["\']?\s*:\s*["\']?(\d+\.?\d*)',
            r'displayPrice["\']?\s*:\s*["\']?\$?(\d+\.?\d*)',
            r'currentPrice["\']?\s*:\s*["\']?\$?(\d+\.?\d*)',
            r'"price":\s*"?\$?(\d+\.?\d*)"?',
            r'data-price="(\d+\.?\d*)"',
            r'price&quot;:&quot;(\d+\.?\d*)'
        ]
        
        for pattern in price_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            if matches:
                print(f"\n✓ Pattern '{pattern}' found prices: {matches[:5]}")  # Show first 5 matches
        
        # Method 3: Look for specific Costco data objects
        print("\n" + "=" * 80)
        print("Method 3: Searching for Costco-specific data objects...")
        print("=" * 80)
        
        # Look for window.digitalData or similar objects
        digital_data_pattern = r'window\.digitalData\s*=\s*({.*?});'
        digital_data_match = re.search(digital_data_pattern, html_content, re.DOTALL)
        if digital_data_match:
            try:
                data = json.loads(digital_data_match.group(1))
                print("\n📊 Found window.digitalData:")
                print(json.dumps(data, indent=2)[:2000])  # First 2000 chars
            except json.JSONDecodeError as e:
                print(f"Could not parse digitalData: {e}")
        
        # Method 4: Look for product data in script tags
        print("\n" + "=" * 80)
        print("Method 4: Searching for product data in script tags...")
        print("=" * 80)
        
        script_pattern = r'<script[^>]*>(.*?)</script>'
        scripts = re.findall(script_pattern, html_content, re.DOTALL | re.IGNORECASE)
        
        for i, script in enumerate(scripts):
            if 'price' in script.lower() and ('product' in script.lower() or 'item' in script.lower()):
                # Try to find JSON objects in the script
                json_pattern = r'\{[^{}]*"price"[^{}]*\}'
                json_matches = re.findall(json_pattern, script, re.IGNORECASE)
                if json_matches:
                    print(f"\n📝 Script block {i+1} contains price data:")
                    for match in json_matches[:3]:  # Show first 3 matches
                        print(f"  {match[:200]}")  # First 200 chars
        
        # Method 5: Simple text search for price patterns
        print("\n" + "=" * 80)
        print("Method 5: Direct price text search...")
        print("=" * 80)
        
        price_text_patterns = [
            r'\$(\d{1,4}(?:,\d{3})*(?:\.\d{2})?)',
            r'USD\s*(\d+\.?\d*)',
        ]
        
        all_prices = set()
        for pattern in price_text_patterns:
            matches = re.findall(pattern, html_content)
            all_prices.update(matches)
        
        print(f"\n💵 All dollar amounts found on page: {sorted(all_prices)}")
        
        # Save full HTML for manual inspection if needed
        print("\n" + "=" * 80)
        print("💾 Saving full HTML to 'page_content.html' for manual inspection...")
        print("=" * 80)
        with open('page_content.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return html_content
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    # Test URL
    url = "https://www.costco.com/p/-/ipad-128gb-wi-fi-a16-chip/4000285678?storeId=10301&partNumber=4000285678&catalogId=10701&langId=-1&krypto=hf4C4watXtGIAglObT4RmazHLwMidBmXSOQoD%2FUjwGGAYG7KRLSMsMXzqW6Chvg743akS6OLOG%2BiDx40tku0uzUOjkesguqLAOwzyjfOT0r3wEJ2iWOVgSjtdAsxMrWW"
    
    fetch_costco_page(url)
