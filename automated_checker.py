"""
Automated Costco iPad A16 Price Checker
Uses Playwright MCP browser automation to check current price

This script documents the automation workflow and provides
helper functions for price checking and alerting.
"""

import json
import re
from datetime import datetime
from pathlib import Path

# Configuration
CONFIG = {
    "product": "iPad, 128GB Wi-Fi (A16 chip)",
    "search_term": "ipad a16",
    "price_threshold": 300.00,
    "costco_url": "https://www.costco.com",
    "product_url": "https://www.costco.com/ipad-128gb-wi-fi-a16-chip.product.4000285678.html"
}

# File paths
HISTORY_FILE = Path(__file__).parent / "price_check_history.json"


def load_history():
    """Load price check history from JSON file"""
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []


def save_history(history):
    """Save price check history to JSON file"""
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)


def parse_price(price_text):
    """
    Extract numeric price from text
    
    Args:
        price_text: String like '$299.99' or '299.99'
        
    Returns:
        float: Numeric price
    """
    price_clean = re.sub(r'[^\d.]', '', price_text)
    return float(price_clean) if price_clean else 0.0


def check_threshold(price, threshold):
    """
    Check if price is below threshold
    
    Returns:
        tuple: (is_below, change_amount, change_percent)
    """
    is_below = price < threshold
    change_amount = threshold - price
    change_percent = (change_amount / threshold) * 100
    return is_below, change_amount, change_percent


def format_alert_message(product, price, threshold, product_url):
    """Generate formatted alert message"""
    is_below, savings, percent = check_threshold(price, threshold)
    
    if is_below:
        return f"""
========================================
🎉 PRICE ALERT! 🎉
========================================
Product: {product}
Current Price: ${price:.2f}
Threshold: ${threshold:.2f}
You Save: ${savings:.2f} ({percent:.1f}% below threshold)

>>> BUY NOW! <<<

Link: {product_url}
========================================
"""
    else:
        return f"""
========================================
Price Check
========================================
Product: {product}
Current Price: ${price:.2f}
Threshold: ${threshold:.2f}
Difference: ${-savings:.2f} above threshold

No action needed.
========================================
"""


def log_price_check(product, price, threshold, alert_triggered):
    """Log price check to history file"""
    history = load_history()
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "product": product,
        "price": price,
        "threshold": threshold,
        "alert_triggered": alert_triggered
    }
    
    history.append(entry)
    save_history(history)
    
    return len(history)


def get_price_stats():
    """Get statistics from price history"""
    history = load_history()
    
    if not history:
        return None
    
    prices = [entry['price'] for entry in history]
    
    return {
        "total_checks": len(history),
        "lowest_price": min(prices),
        "highest_price": max(prices),
        "average_price": sum(prices) / len(prices),
        "current_price": prices[-1],
        "first_check": history[0]['timestamp'],
        "last_check": history[-1]['timestamp']
    }


def print_stats():
    """Print price history statistics"""
    stats = get_price_stats()
    
    if not stats:
        print("No price history available yet.")
        return
    
    print("\n" + "=" * 50)
    print("PRICE HISTORY STATISTICS")
    print("=" * 50)
    print(f"Total Checks: {stats['total_checks']}")
    print(f"Current Price: ${stats['current_price']:.2f}")
    print(f"Lowest Price: ${stats['lowest_price']:.2f}")
    print(f"Highest Price: ${stats['highest_price']:.2f}")
    print(f"Average Price: ${stats['average_price']:.2f}")
    print(f"First Check: {stats['first_check']}")
    print(f"Last Check: {stats['last_check']}")
    print("=" * 50 + "\n")


# ===================================================================
# PLAYWRIGHT MCP WORKFLOW
# ===================================================================
def playwright_workflow_documentation():
    """
    This function documents the Playwright MCP workflow.
    These commands should be executed via MCP client.
    """
    
    workflow = {
        "step_1_navigate": {
            "command": "mcp_playwright_browser_navigate",
            "params": {
                "url": CONFIG['costco_url']
            },
            "description": "Navigate to Costco homepage"
        },
        
        "step_2_search": {
            "command": "mcp_playwright_browser_type",
            "params": {
                "element": "Search box",
                "ref": "e57",  # From page snapshot
                "text": CONFIG['search_term'],
                "submit": True
            },
            "description": "Search for product"
        },
        
        "step_3_wait": {
            "command": "mcp_playwright_browser_wait_for",
            "params": {
                "time": 3
            },
            "description": "Wait for results to load"
        },
        
        "step_4_snapshot": {
            "command": "mcp_playwright_browser_snapshot",
            "params": {},
            "description": "Capture page state"
        },
        
        "step_5_extract_price": {
            "description": "Look for price in snapshot",
            "element_ref": "e1096",  # Reference for 128GB iPad price
            "expected_format": "$299.99"
        }
    }
    
    return workflow


# ===================================================================
# MAIN EXECUTION
# ===================================================================
def main():
    """
    Main function - demonstrates price checking workflow
    
    In production, you would:
    1. Execute Playwright MCP commands to get current price
    2. Parse the price from snapshot data
    3. Check against threshold
    4. Send notifications if needed
    """
    
    print("\n" + "=" * 60)
    print("COSTCO iPAD A16 AUTOMATED PRICE CHECKER")
    print("=" * 60)
    
    # Configuration summary
    print(f"\nConfiguration:")
    print(f"  Product: {CONFIG['product']}")
    print(f"  Search Term: {CONFIG['search_term']}")
    print(f"  Price Threshold: ${CONFIG['price_threshold']:.2f}")
    print(f"  Costco URL: {CONFIG['costco_url']}")
    
    # Show workflow
    print(f"\nPlaywright MCP Workflow:")
    workflow = playwright_workflow_documentation()
    for step, details in workflow.items():
        print(f"  {step}: {details.get('description', 'N/A')}")
    
    # Show last check if available
    print_stats()
    
    # Example price check with current data
    print("Example Price Check:")
    print("-" * 60)
    
    # This would come from Playwright snapshot in production
    example_price_text = "$299.99"
    example_price = parse_price(example_price_text)
    
    # Generate alert message
    alert_msg = format_alert_message(
        CONFIG['product'],
        example_price,
        CONFIG['price_threshold'],
        CONFIG['product_url']
    )
    print(alert_msg)
    
    # Log the check
    is_below, _, _ = check_threshold(example_price, CONFIG['price_threshold'])
    total_checks = log_price_check(
        CONFIG['product'],
        example_price,
        CONFIG['price_threshold'],
        is_below
    )
    
    print(f"Total price checks: {total_checks}")
    print(f"History saved to: {HISTORY_FILE}")
    
    return is_below


if __name__ == "__main__":
    alert_triggered = main()
    
    print("\n" + "=" * 60)
    if alert_triggered:
        print("STATUS: ✅ PRICE ALERT TRIGGERED - BUY NOW!")
    else:
        print("STATUS: ℹ️  No alert - price above threshold")
    print("=" * 60 + "\n")
