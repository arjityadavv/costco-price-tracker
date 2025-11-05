# 🛒 Costco Price Tracker

Automatically track Costco product prices and get notified when prices change! Now with **Playwright MCP browser automation** for reliable price checking.

## 🎉 Latest Update: iPad A16 Price Alert!

**🚨 PRICE BELOW THRESHOLD! 🚨**
- **Product**: iPad, 128GB Wi-Fi (A16 chip)
- **Current Price**: $299.99 (After $30 OFF)
- **Threshold**: $300.00
- **Status**: ✅ **BUY NOW!**
- **Link**: [View on Costco.com](https://www.costco.com/ipad-128gb-wi-fi-a16-chip.product.4000285678.html)

## 🌟 Features

- ✅ **Playwright MCP Browser Automation** - Reliable price checking via actual browser
- 📊 Historical price data storage
- 🔔 GitHub Issue notifications when prices change
- ⏰ Runs every 6 hours automatically (GitHub Actions)
- 🎯 Easy configuration via JSON file
- 🚀 No server required - runs entirely on GitHub Actions
- 🔍 Dual method support: API endpoints + Web scraping

## 🚀 Setup

### 1. Fork or Clone This Repository

```bash
git clone https://github.com/yourusername/costco-price-tracker.git
cd costco-price-tracker
```

### 2. Configure Items to Track

Edit `config.json` and add the Costco items you want to track:

```json
{
  "items": [
    {
      "name": "AirPods 4",
      "url": "https://gdx-api.costco.com/catalog/product/product-api/v2/display-price-lite?whsNumber=847&clientId=4900eb1f-0c10-4bd9-99c3-c59e6c1ecebf&item=1611943&locale=en-us",
      "item_id": "1611943"
    }
  ],
  "notification": {
    "enabled": true,
    "method": "github_issue"
  }
}
```

#### How to Find Item URLs:

1. Go to Costco.com and find the product you want to track
2. Note the item number from the product page URL
3. Use this format for the API URL:
   ```
   https://gdx-api.costco.com/catalog/product/product-api/v2/display-price-lite?whsNumber=847&clientId=4900eb1f-0c10-4bd9-99c3-c59e6c1ecebf&item=ITEM_NUMBER&locale=en-us
   ```
   Replace `ITEM_NUMBER` with the actual item number

### 3. Enable GitHub Actions

1. Go to your repository on GitHub
2. Click on the **Actions** tab
3. Enable workflows if prompted
4. The workflow will now run:
   - Every 6 hours automatically
   - Whenever you push changes to `config.json` or `main.py`
   - Manually via the "Run workflow" button

### 4. Configure Notifications (Optional)

The tracker creates GitHub Issues when price changes are detected. Make sure:
- Issues are enabled in your repository settings
- The workflow has permissions to create issues (already configured in the workflow file)

## 📋 Usage

### Test Manually

You can test the tracker locally before pushing to GitHub:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the tracker
python main.py
```

### Trigger Manually on GitHub

1. Go to **Actions** tab
2. Select "Costco Price Tracker" workflow
3. Click "Run workflow"

### View Price History

The `price_history.json` file stores all tracked prices and is automatically updated by the workflow.

### Add More Items

Simply edit `config.json` and add more items to the `items` array:

```json
{
  "items": [
    {
      "name": "AirPods 4",
      "url": "https://gdx-api.costco.com/...",
      "item_id": "1611943"
    },
    {
      "name": "Kirkland Organic Eggs",
      "url": "https://gdx-api.costco.com/...",
      "item_id": "123456"
    }
  ],
  "notification": {
    "enabled": true,
    "method": "github_issue"
  }
}
```

## 📁 Project Structure

```
costco-price-tracker/
├── .github/
│   └── workflows/
│       └── price-tracker.yml    # GitHub Actions workflow
├── config.json                   # Items to track configuration
├── main.py                       # Price tracking script
├── price_history.json           # Historical price data
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🔔 Notifications

When a price change is detected:
- A GitHub Issue is automatically created
- The issue includes:
  - Item name and ID
  - Previous price
  - New price
  - Price change amount and percentage
  - Timestamp

## 🎭 Playwright MCP Browser Automation

For maximum reliability, we now support **Playwright MCP** browser automation! This method uses a real browser to check prices, avoiding API authentication issues.

### Quick Start with Playwright MCP

1. **Navigate to Costco**:
   ```javascript
   mcp_playwright_browser_navigate(url="https://www.costco.com")
   ```

2. **Search for Product**:
   ```javascript
   mcp_playwright_browser_type(
     element="Search box",
     ref="e57",
     text="ipad a16",
     submit=true
   )
   ```

3. **Wait and Extract Price**:
   ```javascript
   mcp_playwright_browser_wait_for(time=3)
   mcp_playwright_browser_snapshot()
   ```

4. **Run Python Price Checker**:
   ```bash
   python check_ipad_price.py
   ```

### Files for Playwright MCP

- `check_ipad_price.py` - Python script with price checking logic
- `playwright_price_checker.md` - Complete workflow documentation
- `price_check_history.json` - Automated price tracking history

### Benefits of Playwright MCP

✅ **No API Authentication Issues** - Uses real browser like a human  
✅ **Reliable Price Extraction** - Sees exactly what users see  
✅ **Handles Dynamic Content** - Works with JavaScript-loaded prices  
✅ **Easy Debugging** - Visual snapshots of page state  

See `playwright_price_checker.md` for the complete workflow!

## ⚙️ Customization

### Change Check Frequency

Edit `.github/workflows/price-tracker.yml` and modify the cron schedule:

```yaml
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
```

Cron examples:
- `'0 */1 * * *'` - Every hour
- `'0 */12 * * *'` - Every 12 hours
- `'0 0 * * *'` - Once daily at midnight

### Disable Notifications

Set `"enabled": false` in `config.json`:

```json
{
  "notification": {
    "enabled": false,
    "method": "github_issue"
  }
}
```

## 🛠️ Troubleshooting

### Workflow not running
- Check if GitHub Actions is enabled in your repository
- Verify the workflow file is in `.github/workflows/`
- Check the Actions tab for error messages

### Price not fetching
- Verify the item URL is correct
- Check if the item ID is valid
- The API might be rate-limited or blocked

### Issues not being created
- Ensure Issues are enabled in repository settings
- Check workflow permissions in `.github/workflows/price-tracker.yml`

## 📝 License

MIT License - feel free to use and modify as needed!

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## ⭐ Support

If you find this useful, please give it a star on GitHub!