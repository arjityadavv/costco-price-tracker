# Costco iPad A16 Price Checker - Playwright MCP Workflow

## Overview
This document describes the complete workflow for checking iPad A16 prices on Costco.com using Playwright MCP browser automation.

## Current Status: ✅ SUCCESS
- **Product**: iPad, 128GB Wi-Fi (A16 chip)
- **Current Price**: $299.99 (After $30 OFF)
- **Threshold**: $300.00
- **Alert Status**: 🚨 **PRICE BELOW THRESHOLD - BUY NOW!**
- **Product URL**: https://www.costco.com/ipad-128gb-wi-fi-a16-chip.product.4000285678.html

## Workflow Steps

### 1. Navigate to Costco.com
```javascript
// Playwright MCP Command
mcp_playwright_browser_navigate(url="https://www.costco.com")
```
**Expected Result**: Homepage loads successfully

### 2. Search for iPad A16
```javascript
// Playwright MCP Command
mcp_playwright_browser_type(
  element="Search box",
  ref="e57",  // Reference from page snapshot
  text="ipad a16",
  submit=true
)
```
**Expected Result**: Navigates to search results page

### 3. Wait for Results to Load
```javascript
// Playwright MCP Command
mcp_playwright_browser_wait_for(time=3)
```
**Expected Result**: Product listings render

### 4. Take Page Snapshot
```javascript
// Playwright MCP Command
mcp_playwright_browser_snapshot()
```

### 5. Extract Product Information

From the snapshot, we found:
- **Heading**: "1 - 2 of 2 results for \"ipad a16\""
- **Products Found**: 2

#### Product 1: iPad 128GB (ref=e1078)
- **Name**: iPad, 128GB Wi-Fi (A16 chip)
- **Price**: $299.99 (ref=e1096)
- **Discount**: After $30 OFF
- **Tags**: AppleCare+ Available, Holiday Savings
- **Rating**: 4.37 out of 5 stars (19 reviews)
- **URL**: https://www.costco.com/ipad-128gb-wi-fi-a16-chip.product.4000285678.html
- **Availability**: Delivery Available, Ship to Warehouse Available

#### Product 2: iPad 256GB (ref=e1162)
- **Name**: iPad, 256GB Wi-Fi (A16 chip)
- **Price**: $399.99 (ref=e1180)
- **Discount**: After $30 OFF
- **Tags**: AppleCare+ Available, Holiday Savings
- **Rating**: 4.33 out of 5 stars (6 reviews)
- **URL**: https://www.costco.com/ipad-256gb-wi-fi-a16-chip.product.4000285631.html
- **Availability**: Delivery Available, Ship to Warehouse Available

## Price Extraction Details

### Method 1: Direct Text Extraction from Snapshot
```yaml
# Look for price elements in the snapshot
generic [ref=e1096]: $299.99  # 128GB model
generic [ref=e1180]: $399.99  # 256GB model
```

### Method 2: Using Element References
```javascript
// If you need to interact with specific elements
// Use the ref values from the snapshot
// Example: ref=e1096 for the $299.99 price
```

## Python Integration

### check_ipad_price.py
The Python script (`check_ipad_price.py`) provides:
- Price parsing logic
- Threshold comparison
- Price history tracking
- Alert generation

### Usage
```python
# Extract price from Playwright snapshot
price_text = "$299.99"  # From ref=e1096

# Parse and check
current_price = parse_price(price_text)
alert_triggered, message = check_price_against_threshold(current_price, 300.00)

# Save to history
save_price_check("iPad, 128GB Wi-Fi (A16 chip)", current_price, alert_triggered)
```

## Automation Options

### Option 1: Manual MCP Workflow
Execute Playwright MCP commands manually when needed.

### Option 2: Scheduled Automation
Create a script that:
1. Runs Playwright MCP commands via MCP client
2. Extracts price from snapshot
3. Runs Python price checker
4. Sends notifications if alert triggered

### Option 3: GitHub Actions Integration
Schedule GitHub Actions to:
1. Use Playwright for browser automation
2. Extract prices
3. Create GitHub Issues for price alerts

## Notifications

When price is below threshold ($300), you can:
- ✅ Send email notification
- ✅ Create GitHub Issue
- ✅ Send SMS via Twilio
- ✅ Post to Slack/Discord webhook
- ✅ Save to price_check_history.json

## Current Alert Status

```
============================================================
*** PRICE ALERT! ***
============================================================
Product: iPad, 128GB Wi-Fi (A16 chip)
Current Price: $299.99
Price Threshold: $300.00
Status: BELOW THRESHOLD
Action: BUY NOW!
Link: https://www.costco.com/ipad-128gb-wi-fi-a16-chip.product.4000285678.html
============================================================
```

## Next Steps

1. **Immediate**: 
   - Review the $299.99 iPad deal
   - Check additional details on Costco.com
   - Verify availability for delivery/pickup

2. **Automation**:
   - Set up scheduled checks (e.g., every 6 hours)
   - Configure notification preferences
   - Add more products to track

3. **Enhancements**:
   - Track both 128GB and 256GB models
   - Add price history charts
   - Compare prices across retailers
   - Track stock availability

## Reference Elements

Key element references from Costco search page:
- Search box: `ref=e57`
- 128GB iPad price: `ref=e1096`
- 128GB iPad link: `ref=e1078`
- 256GB iPad price: `ref=e1180`
- 256GB iPad link: `ref=e1162`

## Files Created

- ✅ `check_ipad_price.py` - Python price checking logic
- ✅ `price_check_history.json` - Price tracking history
- ✅ `playwright_price_checker.md` - This workflow document
