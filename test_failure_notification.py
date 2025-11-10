#!/usr/bin/env python3
"""
Test script to demonstrate the failure notification behavior
This simulates what happens when a price drops below threshold
"""
import sys

def test_price_alert():
    """Simulate a price alert scenario"""
    print("\n" + "=" * 80)
    print("TESTING PRICE ALERT NOTIFICATION")
    print("=" * 80)
    
    # Simulate checking prices
    print("\n[Checking] iPad A16 128GB")
    print("  Threshold: $299.00")
    print("  Current Price: $329.99")
    print("  ℹ️  Price is $30.99 above threshold - NO ALERT")
    
    print("\n[Checking] AirPods 4 with Active Noise Cancellation")
    print("  Threshold: $149.00")
    print("  Current Price: $148.99")
    print("  ✅ ALERT: Price is $0.01 below threshold!")
    
    alerts_triggered = 1
    
    print("\n" + "=" * 80)
    print(f"Check Complete: {alerts_triggered} new alerts triggered")
    print("=" * 80 + "\n")
    
    # This is the key behavior
    if alerts_triggered > 0:
        print("🚨 EXITING WITH ERROR CODE 1 - Price alert(s) triggered!")
        print("   GitHub Actions will FAIL and send you an email notification.")
        print("\n📧 You will receive an email like:")
        print("   Subject: Run failed: Costco Price Tracker - main")
        print("   Body: Your workflow 'Costco Price Tracker' has failed")
        sys.exit(1)
    else:
        print("✅ EXITING WITH CODE 0 - No price alerts.")
        print("   All prices are above your thresholds.")
        print("   GitHub Actions PASSES - No email sent.")
        sys.exit(0)

if __name__ == "__main__":
    test_price_alert()
