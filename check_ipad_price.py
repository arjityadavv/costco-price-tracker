"""
Costco iPad A16 Price Checker using Playwright MCP
This script automates browser interaction to check iPad A16 price on Costco
and notifies if the price is less than $300.
"""

import json
import re
from datetime import datetime

# You would call the Playwright MCP tools from your MCP client
# This script documents the workflow and provides helper functions

PRICE_THRESHOLD = 300.00
SEARCH_TERM = "ipad a16"
COSTCO_URL = "https://www.costco.com"

def parse_price(price_text):
    """
    Extract numeric price from price text like '$299.99'
    
    Args:
        price_text: String containing price (e.g., '$299.99')
        
    Returns:
        float: Numeric price value
    """
    # Remove dollar sign and convert to float
    price_clean = re.sub(r'[^\d.]', '', price_text)
    return float(price_clean)

def check_price_against_threshold(price, threshold):
    """
    Check if price is below threshold
    
    Args:
        price: Current price
        threshold: Price threshold
        
    Returns:
        tuple: (bool, str) - (is_below_threshold, message)
    """
    if price < threshold:
        return True, f"🎉 PRICE ALERT! iPad A16 is ${price:.2f} (below ${threshold:.2f} threshold)"
    else:
        return False, f"iPad A16 is ${price:.2f} (above ${threshold:.2f} threshold)"

def save_price_check(product_name, price, alert_triggered):
    """
    Save price check results to history file
    
    Args:
        product_name: Name of the product
        price: Current price
        alert_triggered: Whether alert was triggered
    """
    history_file = "price_check_history.json"
    
    # Load existing history
    try:
        with open(history_file, 'r') as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []
    
    # Add new check
    history.append({
        "timestamp": datetime.now().isoformat(),
        "product": product_name,
        "price": price,
        "threshold": PRICE_THRESHOLD,
        "alert_triggered": alert_triggered
    })
    
    # Save updated history
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=2)
    
    print(f"Price check saved to {history_file}")

def main():
    """
    Main workflow for checking iPad A16 price
    
    This documents the Playwright MCP workflow:
    1. Navigate to Costco.com
    2. Search for "ipad a16"
    3. Wait for results to load
    4. Extract price from first result (128GB model)
    5. Check against threshold
    6. Send notification if needed
    """
    
    print(f"Starting Costco iPad A16 price check...")
    print(f"Price threshold: ${PRICE_THRESHOLD}")
    print("-" * 50)
    
    # WORKFLOW (to be executed via Playwright MCP):
    # 
    # Step 1: Navigate to Costco
    # mcp_playwright_browser_navigate(url="https://www.costco.com")
    # 
    # Step 2: Search for iPad A16
    # Find search box and type search term
    # mcp_playwright_browser_type(element="Search box", ref="e57", text="ipad a16", submit=True)
    # 
    # Step 3: Wait for page to load
    # mcp_playwright_browser_wait_for(time=3)
    # 
    # Step 4: Take snapshot to see products
    # mcp_playwright_browser_snapshot()
    # 
    # Step 5: Extract price from first product
    # Look for: generic [ref=e1096]: $299.99
    # This is the price element for the 128GB iPad A16
    
    # Example extracted data (you would get this from the snapshot):
    product_name = "iPad, 128GB Wi-Fi (A16 chip)"
    price_text = "$299.99"  # From ref=e1096 in the snapshot
    
    # Parse price
    current_price = parse_price(price_text)
    print(f"Product: {product_name}")
    print(f"Current Price: ${current_price:.2f}")
    
    # Check against threshold
    alert_triggered, message = check_price_against_threshold(current_price, PRICE_THRESHOLD)
    print(message)
    
    # Save to history
    save_price_check(product_name, current_price, alert_triggered)
    
    # If alert triggered, you could:
    # - Send email notification
    # - Create GitHub issue
    # - Send SMS
    # - Post to Slack/Discord
    
    if alert_triggered:
        print("\n📧 Notification would be sent here!")
        print(f"   Product: {product_name}")
        print(f"   Price: ${current_price:.2f}")
        print(f"   Link: https://www.costco.com/ipad-128gb-wi-fi-a16-chip.product.4000285678.html")
    
    return alert_triggered, current_price

if __name__ == "__main__":
    alert_triggered, price = main()
    print("-" * 50)
    if alert_triggered:
        print("✅ ALERT: Price is below threshold!")
    else:
        print("ℹ️  No alert: Price is above threshold")
