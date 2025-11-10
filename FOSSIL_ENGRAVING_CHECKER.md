# Fossil Engraving Availability Checker

Automated monitoring system to check if engraving is available for Fossil products.

## Overview

This checker monitors the Fossil website to detect when engraving becomes available for specified products. It checks every 6 hours and sends an email notification when the engraving feature is enabled.

## How It Works

### Monitoring Logic

1. **Checks every 6 hours** via GitHub Actions
2. **Looks for the error message**: "Apologies - Due to an inventory limitation, we are unable to engrave this product at this time."
3. **Email notification** when engraving becomes available (message disappears)

### Exit Code Strategy

```python
if engraving_available:
    sys.exit(0)  # Triggers workflow FAILURE → Email sent ✅
else:
    sys.exit(1)  # Workflow passes → No email (silent monitoring)
```

## Files

### Core Files

- **`fossil_engraving_checker.py`** - Main monitoring script
- **`fossil_config.json`** - Product configuration
- **`engraving_history.json`** - Check history (auto-updated)
- **`.github/workflows/fossil-engraving-checker.yml`** - GitHub Actions workflow

### Configuration

**`fossil_config.json`**
```json
{
  "product_url": "https://www.fossil.com/en-us/products/colleen-three-hand-two-tone-stainless-steel-watch/BQ3908.html",
  "product_name": "Colleen Three-Hand Two-Tone Stainless Steel Watch",
  "product_id": "BQ3908"
}
```

## Email Notifications

### When You Get Emails

✅ **You WILL receive an email when:**
- Engraving becomes available
- Error message disappears from the page
- Workflow fails (exit code 0)

### Email Details

**Subject:** `Run failed: Fossil Engraving Checker - main`

**Content includes:**
- Link to workflow run
- Link to GitHub Issue with details
- Timestamp of availability

### When You DON'T Get Emails

❌ **You WON'T receive emails when:**
- Engraving is still unavailable
- Error message is still present
- Workflow passes (exit code 1)

## GitHub Actions Schedule

```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
```

**Check times (UTC):**
- 00:00 (12:00 AM)
- 06:00 (6:00 AM)
- 12:00 (12:00 PM)
- 18:00 (6:00 PM)

## Current Status

**Product:** Colleen Three-Hand Two-Tone Stainless Steel Watch (BQ3908)

**Current Status:** ❌ Engraving NOT available
- Error message is present on the page
- Monitoring active every 6 hours

## Manual Testing

### Run Locally

```bash
python fossil_engraving_checker.py
```

**Note:** Local runs may fail due to bot protection (403 Forbidden). This is expected. GitHub Actions servers may have better success.

### Trigger Manually on GitHub

1. Go to **Actions** tab
2. Select **Fossil Engraving Checker**
3. Click **Run workflow**

## Workflow Behavior

### Scenario 1: Engraving NOT Available (Current)

```
Check runs → Message found → Exit 1 → Workflow passes → No email
```

### Scenario 2: Engraving Becomes Available

```
Check runs → No message → Exit 0 → Workflow FAILS → Email sent! 📧
```

### Scenario 3: Check Error (403, timeout, etc.)

```
Check runs → Error → Exit 1 → Workflow passes → No email
```

## History Tracking

The script maintains a history of checks in `engraving_history.json`:

```json
{
  "BQ3908": {
    "product_name": "Colleen Three-Hand Two-Tone Stainless Steel Watch",
    "currently_available": false,
    "last_checked": "2025-11-10T23:38:36.958203",
    "checks": [
      {
        "available": false,
        "message": "Error message present",
        "timestamp": "2025-11-10T23:38:36.958203",
        "status_code": 200
      }
    ]
  }
}
```

## GitHub Issue Creation

When engraving becomes available, an automated issue is created:

**Issue Title:** `🎉 Engraving Available: Colleen Three-Hand Two-Tone Stainless Steel Watch`

**Labels:** `engraving-available`, `automated`

**Content:**
- Product name and ID
- Direct link to product page
- Timestamp of availability
- Automatic tracking information

## Monitoring Multiple Products

To monitor additional products, add them to `fossil_config.json`:

```json
{
  "products": [
    {
      "product_url": "https://www.fossil.com/en-us/products/...",
      "product_name": "Product Name",
      "product_id": "PRODUCT_ID"
    }
  ]
}
```

Then update the script to loop through multiple products.

## Disabling the Checker

To stop monitoring:

1. **Disable the workflow:**
   ```bash
   # Edit .github/workflows/fossil-engraving-checker.yml
   # Comment out the schedule trigger
   ```

2. **Or delete the workflow file:**
   ```bash
   rm .github/workflows/fossil-engraving-checker.yml
   ```

## Troubleshooting

### No Emails Received

1. **Check GitHub notification settings:**
   - Go to: https://github.com/settings/notifications
   - Enable "Email" under "Actions"
   - Enable "Send notifications for failed workflows only"

2. **Check workflow runs:**
   - Go to Actions tab
   - Look for failed runs (red ❌)
   - Failed runs trigger emails

3. **Verify email address:**
   - Check your GitHub email settings
   - Make sure emails aren't in spam

### Workflow Always Fails

If you're getting too many emails:
- Engraving may actually be available
- Check the product page manually
- Review `engraving_history.json` for patterns

### 403 Forbidden Errors

This is normal for local testing. Fossil's website blocks some automated requests. GitHub Actions servers often have better success.

## Dependencies

```txt
requests>=2.31.0
beautifulsoup4>=4.12.0
```

## Schedule Modification

To change the check frequency, edit the cron expression:

```yaml
# Every 3 hours
- cron: '0 */3 * * *'

# Every 12 hours
- cron: '0 */12 * * *'

# Daily at 9 AM UTC
- cron: '0 9 * * *'

# Twice daily (9 AM and 9 PM UTC)
- cron: '0 9,21 * * *'
```

## Next Steps

1. ✅ Push changes to GitHub
2. ✅ Workflow will start running automatically every 6 hours
3. ✅ You'll receive email when engraving becomes available
4. ✅ Check the Issues tab for detailed alerts
5. ✅ Monitor `engraving_history.json` for tracking history
