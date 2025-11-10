# Setup Complete! 🎉

## Fossil Engraving Availability Checker

Your automated monitoring system is now active and will check every 6 hours if engraving is available for the Fossil Colleen Three-Hand Watch.

## What Was Created

### 1. **Main Script** (`fossil_engraving_checker.py`)
- Checks Fossil product page for engraving availability
- Looks for error message: "Apologies - Due to an inventory limitation..."
- Creates GitHub Issue when engraving becomes available
- Tracks history of all checks

### 2. **Configuration Files**
- **`fossil_config.json`** - Product details (URL, name, ID)
- **`engraving_history.json`** - Check history (auto-updated)

### 3. **GitHub Actions Workflow** (`.github/workflows/fossil-engraving-checker.yml`)
- Runs automatically every 6 hours
- Monitors engraving availability
- Sends email notification when available

### 4. **Documentation** (`FOSSIL_ENGRAVING_CHECKER.md`)
- Complete guide on how it works
- Troubleshooting tips
- Configuration options

## How It Works

```
┌─────────────────────────────────────────┐
│  Check Runs Every 6 Hours               │
└───────────────┬─────────────────────────┘
                │
                ▼
    ┌───────────────────────┐
    │ Is error message      │
    │ present on page?      │
    └───────┬───────────────┘
            │
     ┌──────┴──────┐
     │             │
    YES           NO
     │             │
     ▼             ▼
┌─────────┐   ┌─────────┐
│ EXIT 1  │   │ EXIT 0  │
│ (PASS)  │   │ (FAIL)  │
└────┬────┘   └────┬────┘
     │             │
     ▼             ▼
┌─────────┐   ┌─────────┐
│ No email│   │ 📧 EMAIL│
│  sent   │   │ SENT!   │
│ (silent)│   │ + Issue │
└─────────┘   └─────────┘
```

## Schedule

**Runs every 6 hours at:**
- 00:00 UTC (12:00 AM)
- 06:00 UTC (6:00 AM)  
- 12:00 UTC (12:00 PM)
- 18:00 UTC (6:00 PM)

## Email Notification

You'll receive an email when:
- ✅ Engraving becomes available
- ✅ Error message disappears
- ✅ Workflow fails (by design)

**Email subject:** `Run failed: Fossil Engraving Checker - main`

## Current Status

**Product:** Colleen Three-Hand Two-Tone Stainless Steel Watch
**Product ID:** BQ3908
**Current Status:** ❌ Engraving NOT available
**Monitoring:** ✅ Active (every 6 hours)

## What Happens Next

1. **First check** will run within 6 hours or on next push
2. **No email** while engraving is unavailable (silent monitoring)
3. **Email sent** when engraving becomes available
4. **GitHub Issue** created with product details
5. **History tracked** in `engraving_history.json`

## Manual Trigger

To check immediately:
1. Go to **Actions** tab on GitHub
2. Select **Fossil Engraving Checker**
3. Click **Run workflow**

## View Results

- **Actions tab** - See all check runs
- **Issues tab** - See alerts when available
- **`engraving_history.json`** - See check history

## Important Notes

### Bot Protection
- Local testing may fail (403 Forbidden) - this is normal
- GitHub Actions servers often have better success
- The workflow will handle errors gracefully

### Email Settings
Make sure you have:
1. GitHub Actions email notifications enabled
2. "Send notifications for failed workflows only" checked
3. Email address verified in GitHub

### Privacy
- All checks happen via GitHub Actions
- No personal data collected
- History stored in your repository

## Comparison with Costco Tracker

| Feature | Costco Tracker | Fossil Checker |
|---------|---------------|----------------|
| **Check Frequency** | Every 2 hours | Every 6 hours |
| **Notification** | Price drops | Engraving available |
| **Current Status** | ⏸️ Disabled | ✅ Active |
| **Items Tracked** | 2 products | 1 product |
| **Alert Method** | Workflow failure → Email | Workflow failure → Email |

## Need Help?

Check `FOSSIL_ENGRAVING_CHECKER.md` for:
- Detailed explanation
- Troubleshooting guide
- Configuration options
- Schedule modification

---

**Setup completed:** November 10, 2025
**Repository:** arjityadavv/costco-price-tracker
**Branch:** main
