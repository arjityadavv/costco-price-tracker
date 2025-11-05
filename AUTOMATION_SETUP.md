# 🤖 GitHub Actions Automated Price Tracking Setup

## ✅ Setup Complete!

Your Costco price tracker is now configured to automatically monitor prices and create GitHub Issues when prices drop to your target levels!

## 📋 What's Configured

### Tracked Products

| Product | Current Price | Target Price | Status |
|---------|--------------|--------------|--------|
| iPad A16 (128GB Wi-Fi) | $299.99 | $299.00 or less | ⏳ Waiting ($0.99 above) |
| AirPods 4 with ANC | $149.99 | $149.00 or less | ⏳ Waiting ($0.99 above) |

### Automation Schedule

- **Frequency**: Every 2 hours (12 checks per day)
- **Method**: Web scraping via GitHub Actions
- **Alerts**: GitHub Issues created automatically when price drops

## 🚀 How It Works

1. **GitHub Actions runs every 2 hours** (configured in `.github/workflows/price-tracker.yml`)
2. **Script checks current prices** for all items in `config.json`
3. **If price ≤ threshold**:
   - ✅ Creates a GitHub Issue with price alert
   - 💾 Updates `price_history.json`
   - 📝 Commits changes to repository
4. **If price > threshold**:
   - ℹ️ Logs status (waiting for price drop)
   - 💾 Updates history without creating issue

## 📂 Files Created/Updated

- ✅ `config.json` - Updated with both products and price thresholds
- ✅ `playwright_price_checker.py` - Main automated checker script
- ✅ `manual_test_checker.py` - Local testing script (uses manual prices)
- ✅ `.github/workflows/price-tracker.yml` - GitHub Actions workflow (every 2 hours)
- ✅ `price_history.json` - Tracks price history and alert status

## 🎯 Price Thresholds

As configured, alerts will be triggered when:
- **iPad A16 128GB**: Price drops to **$299.00 or less**
- **AirPods 4 ANC**: Price drops to **$149.00 or less**

## 🔔 GitHub Issue Alerts

When a price drops to your threshold, a GitHub Issue will be automatically created with:
- 🎉 Alert title with product name and price
- 💰 Current price vs threshold
- 💵 Amount you're saving
- 🔗 Direct link to product page
- ⏰ Timestamp of alert

Example issue title: `🎉 Price Alert: iPad A16 (128GB Wi-Fi) - $298.99`

## 📊 Monitor Price Checks

### View in GitHub Actions
1. Go to your repository
2. Click **Actions** tab
3. See "Costco Price Tracker" workflow runs

### Manual Trigger
1. Go to **Actions** tab
2. Select "Costco Price Tracker" workflow
3. Click "Run workflow" button
4. Select branch and run

### Check Price History
View `price_history.json` in your repository to see:
- All historical prices
- Last check timestamp
- Alert status for each product

## 🧪 Local Testing

### Test with Manual Prices (No Network Required)
```bash
python manual_test_checker.py
```

This uses the prices we extracted via Playwright MCP ($299.99 and $149.99) to test the logic locally.

### Test with Live Scraping (Requires Network)
```bash
python playwright_price_checker.py
```

**Note**: May timeout due to Costco's bot protection. GitHub Actions has better success rates.

## ⚙️ Customization

### Change Price Thresholds

Edit `config.json`:
```json
{
  "items": [
    {
      "name": "iPad A16 (128GB Wi-Fi)",
      "price_threshold": 289.00  // Change this
    },
    {
      "name": "AirPods 4 with Active Noise Cancellation",
      "price_threshold": 139.00  // Change this
    }
  ]
}
```

### Change Check Frequency

Edit `.github/workflows/price-tracker.yml`:
```yaml
on:
  schedule:
    - cron: '0 */1 * * *'  # Every 1 hour
    # or
    - cron: '0 */4 * * *'  # Every 4 hours
    # or
    - cron: '0 9,17 * * *'  # Twice daily (9 AM and 5 PM)
```

### Add More Products

1. Search for product on Costco.com using Playwright MCP
2. Extract product URL and current price
3. Add to `config.json`:
```json
{
  "name": "Product Name",
  "search_term": "search term",
  "price_threshold": 100.00,
  "url": "https://www.costco.com/product-url.html",
  "item_id": "item_number"
}
```

## 🔍 Current Status

Run this command to see current status:
```bash
python manual_test_checker.py
```

Output shows:
- ✅ Alert triggered (price at/below threshold)
- ℹ️ Waiting (price above threshold)
- 📊 Amount needed to drop for alert

## 📈 What Happens Next

1. **Every 2 hours**, GitHub Actions will check prices
2. **When iPad drops to $299.00 or less** → You'll get a GitHub Issue
3. **When AirPods drop to $149.00 or less** → You'll get a GitHub Issue
4. **Price history updates** automatically with each check
5. **No duplicate alerts** - only creates issue when price newly drops

## 🎊 Success Criteria

Your automation is working if:
- ✅ GitHub Actions runs every 2 hours
- ✅ `price_history.json` updates with timestamps
- ✅ No errors in Actions logs
- ✅ GitHub Issues created when price drops

## 🆘 Troubleshooting

### Workflow not running
- Check Actions tab → Enable workflows if disabled
- Verify cron schedule is correct
- Try manual trigger to test

### Price not updating
- Web scraping may fail due to bot protection
- Check Actions logs for errors
- Consider using manual_test_checker.py locally

### No GitHub Issues created
- Verify `GITHUB_TOKEN` is available (automatic in Actions)
- Check Issues tab - ensure Issues are enabled
- Verify price actually dropped below threshold

## 📝 Notes

- **Current prices are $0.99 above threshold** - alerts will trigger with next price drop
- **AirPods deal expires today (11/6/25)** - price may increase after today
- **GitHub Actions is free** for public repos (2000 minutes/month for private)
- **Rate limiting**: 2-hour intervals prevent excessive requests

---

## 🎯 Quick Start Checklist

- [x] Products configured in config.json
- [x] Price thresholds set ($299 for iPad, $149 for AirPods)
- [x] GitHub Actions workflow created
- [x] Automated checks every 2 hours
- [x] Price history tracking enabled
- [x] GitHub Issue alerts configured
- [ ] Push to GitHub to activate automation
- [ ] Watch Actions tab for first run
- [ ] Wait for price drops!

## 🚀 Next Steps

1. **Commit and push** these changes to GitHub
2. **Enable Actions** in your repository settings
3. **Watch the Actions tab** for the first automated run
4. **Receive alerts** via GitHub Issues when prices drop!

```bash
git add .
git commit -m "Setup automated price tracking with GitHub Actions"
git push origin main
```

🎉 **You're all set!** The automation will start working as soon as you push to GitHub.
