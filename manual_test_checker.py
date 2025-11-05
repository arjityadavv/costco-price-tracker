#!/usr/bin/env python3
"""
Manual Price Checker - Uses manually extracted prices from Playwright MCP
This is useful for testing the GitHub issue creation logic
"""

import json
import os
from datetime import datetime
from pathlib import Path

# Simulate the prices we found using Playwright MCP
MANUAL_PRICES = {
    "4000285678": {  # iPad A16 128GB
        "name": "iPad, 128GB Wi-Fi (A16 chip)",
        "price": 299.99,
        "url": "https://www.costco.com/ipad-128gb-wi-fi-a16-chip.product.4000285678.html"
    },
    "4000308504": {  # AirPods 4 ANC
        "name": "AirPods 4 with Active Noise Cancellation",
        "price": 149.99,
        "url": "https://www.costco.com/airpods-4-with-active-noise-cancellation.product.4000308504.html"
    }
}


def load_config():
    """Load configuration from config.json"""
    config_path = Path(__file__).parent / "config.json"
    with open(config_path, 'r') as f:
        return json.load(f)


def load_price_history():
    """Load price history from JSON file"""
    history_path = Path(__file__).parent / "price_history.json"
    if history_path.exists():
        with open(history_path, 'r') as f:
            return json.load(f)
    return {}


def save_price_history(history):
    """Save price history to JSON file"""
    history_path = Path(__file__).parent / "price_history.json"
    with open(history_path, 'w') as f:
        json.dump(history, f, indent=2)


def check_prices_manual():
    """Check prices using manual data"""
    config = load_config()
    history = load_price_history()
    
    print("\n" + "=" * 80)
    print("COSTCO PRICE TRACKER - Manual Check (Test Mode)")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Checking {len(config['items'])} items...")
    print("=" * 80)
    
    alerts_triggered = 0
    
    for item in config['items']:
        item_id = item['item_id']
        item_name = item['name']
        threshold = item['price_threshold']
        url = item['url']
        
        print(f"\n[Checking] {item_name}")
        print(f"  Threshold: ${threshold:.2f} or less")
        
        # Get manual price data
        if item_id not in MANUAL_PRICES:
            print(f"  ❌ No manual price data available")
            continue
        
        manual_data = MANUAL_PRICES[item_id]
        current_price = manual_data['price']
        
        print(f"  Current Price: ${current_price:.2f}")
        
        # Check if price is at or below threshold
        if current_price <= threshold:
            savings = threshold - current_price
            print(f"  ✅ ALERT: Price is at or below threshold!")
            print(f"  💰 Target met! Price: ${current_price:.2f} <= ${threshold:.2f}")
            alerts_triggered += 1
        else:
            difference = current_price - threshold
            print(f"  ℹ️  Price is ${difference:.2f} above threshold")
            print(f"  📊 Need drop of ${difference:.2f} to trigger alert")
        
        # Update history
        history[item_id] = {
            'name': item_name,
            'price': current_price,
            'threshold': threshold,
            'last_checked': datetime.now().isoformat(),
            'alert_triggered': current_price <= threshold
        }
    
    # Save updated history
    save_price_history(history)
    
    print("\n" + "=" * 80)
    print(f"Check Complete: {alerts_triggered} alerts triggered")
    print(f"Results saved to price_history.json")
    print("=" * 80 + "\n")
    
    return alerts_triggered


if __name__ == "__main__":
    check_prices_manual()
