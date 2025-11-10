# Email Notification Setup

## How It Works

The price tracker now uses **workflow failure** to trigger email notifications:

### Exit Code Logic

```python
if alerts_triggered > 0:
    # Price dropped below threshold - FAIL the workflow
    sys.exit(1)  # ❌ Sends email notification
else:
    # All prices above threshold - PASS the workflow  
    sys.exit(0)  # ✅ No email (silent success)
```

### When You Get Emails

You'll receive an email notification **ONLY** when:
- ✅ A price drops **to or below** your threshold
- ✅ The workflow **fails** (exit code 1)

### When You DON'T Get Emails

You won't receive emails when:
- ❌ All prices are **above** your thresholds
- ❌ The workflow **passes** (exit code 0)

## Email Notification Details

### Email Subject
```
Run failed: Costco Price Tracker - main
```

### What's Included
- Workflow name and run number
- Failed step details
- Link to view the full workflow run
- View the GitHub Issue created for the price alert

## Configuring Email Notifications

GitHub sends failure emails by default to:
1. The person who triggered the workflow
2. The repository owner

### To Ensure You Receive Emails

1. **Check your GitHub notification settings:**
   - Go to: https://github.com/settings/notifications
   - Under "Actions" → Enable "Email"
   - Enable "Send notifications for failed workflows only"

2. **Watch your repository:**
   - Go to your repository
   - Click "Watch" → "All Activity"

3. **Check your email preferences:**
   - Make sure GitHub emails aren't going to spam
   - Verify your email in GitHub settings

## Testing the Notification

Run this test script to see the failure behavior:
```bash
python test_failure_notification.py
```

This will simulate a price alert and exit with code 1 (failure).

## Current Price Status

| Product | Current Price | Threshold | Alert Status |
|---------|--------------|-----------|--------------|
| iPad A16 128GB | $329.99 | ≤ $299.00 | ❌ Above (no alert) |
| AirPods 4 ANC | $148.99 | ≤ $149.00 | ✅ **WILL TRIGGER ALERT** |

## Next Automated Run

- **Schedule:** Every 2 hours
- **Next Check:** Within 2 hours
- **Expected:** Workflow will fail for AirPods alert
- **Result:** You'll receive an email notification

## Manual Testing

Test the workflow immediately:
```bash
# Push changes to trigger workflow
git add .
git commit -m "Update price checker to fail on alerts"
git push

# Or trigger manually from GitHub:
# Go to Actions → Costco Price Tracker → Run workflow
```

## Viewing Alerts

After receiving an email:
1. Click the workflow run link in the email
2. View the failed step output to see price details
3. Check the "Issues" tab for the created price alert
4. The issue will contain:
   - Current price
   - Your threshold
   - Savings amount
   - Product link
