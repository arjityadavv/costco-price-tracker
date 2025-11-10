#!/usr/bin/env python3
"""
Fossil Engraving Availability Checker
Monitors if engraving is available for a specific Fossil product.

Exit Codes:
- 0: Engraving is available - workflow FAILS to send notification
- 1: Engraving is NOT available (message present) - workflow passes silently
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def load_fossil_config():
    """Load Fossil product configuration"""
    config_path = Path(__file__).parent / "fossil_config.json"
    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    return {
        "product_url": "https://www.fossil.com/en-us/products/colleen-three-hand-two-tone-stainless-steel-watch/BQ3908.html",
        "product_name": "Colleen Three-Hand Two-Tone Stainless Steel Watch",
        "product_id": "BQ3908"
    }


def load_engraving_history():
    """Load engraving availability history"""
    history_path = Path(__file__).parent / "engraving_history.json"
    if history_path.exists():
        with open(history_path, 'r') as f:
            return json.load(f)
    return {}


def save_engraving_history(history):
    """Save engraving availability history"""
    history_path = Path(__file__).parent / "engraving_history.json"
    with open(history_path, 'w') as f:
        json.dump(history, f, indent=2)


def check_engraving_availability(url, product_id):
    """
    Check if engraving is available by looking for the error message
    
    Args:
        url: Product page URL
        product_id: Product ID
        
    Returns:
        dict: {
            'available': bool,
            'message': str,
            'timestamp': str
        }
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
        
        print(f"[Checking] Engraving availability for product {product_id}")
        print(f"  URL: {url}")
        
        # Create a session for better connection handling
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=30, allow_redirects=True)
        
        # Check for common blocking status codes
        if response.status_code == 403:
            print(f"  ⚠️ Access forbidden (403). Site may be blocking automated requests.")
            print(f"  ℹ️  This is expected when running locally. GitHub Actions may have better success.")
            return {
                'available': None,
                'message': 'Access forbidden - possible bot detection',
                'timestamp': datetime.now().isoformat(),
                'status_code': 403
            }
        
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for the error message
        error_message = "Apologies - Due to an inventory limitation, we are unable to engrave this product at this time."
        
        # Search for the message in the page content
        page_text = soup.get_text()
        message_found = error_message in page_text
        
        # Also check for specific button or element that might contain this message
        error_button = soup.find('button', string=lambda text: text and error_message in text)
        
        if message_found or error_button:
            print(f"  ❌ Engraving NOT available - Error message found")
            return {
                'available': False,
                'message': 'Error message present',
                'timestamp': datetime.now().isoformat(),
                'status_code': response.status_code
            }
        else:
            print(f"  ✅ Engraving AVAILABLE - No error message found")
            return {
                'available': True,
                'message': 'No error message',
                'timestamp': datetime.now().isoformat(),
                'status_code': response.status_code
            }
        
    except requests.exceptions.HTTPError as e:
        print(f"  ⚠️ HTTP Error: {e}")
        return {
            'available': None,
            'message': f'HTTP Error: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        print(f"  ⚠️ Error checking availability: {e}")
        return {
            'available': None,
            'message': f'Error: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }


def create_github_issue(product_name, product_url, product_id):
    """
    Create a GitHub issue when engraving becomes available
    
    Args:
        product_name: Name of the product
        product_url: Product URL
        product_id: Product ID
    """
    github_token = os.environ.get('GITHUB_TOKEN')
    repo = os.environ.get('GITHUB_REPOSITORY')
    
    if not github_token or not repo:
        print("⚠️ GitHub token or repository not configured. Skipping issue creation.")
        return
    
    issue_title = f"🎉 Engraving Available: {product_name}"
    issue_body = f"""## Engraving Feature Now Available!

**Product:** {product_name}
**Product ID:** {product_id}
**Product Link:** {product_url}

The engraving feature is now available for this product! The inventory limitation message is no longer displayed.

**Timestamp:** {datetime.now().isoformat()}

---
*This alert was automatically generated by the Fossil Engraving Availability Checker.*
"""
    
    api_url = f"https://api.github.com/repos/{repo}/issues"
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    data = {
        'title': issue_title,
        'body': issue_body,
        'labels': ['engraving-available', 'automated']
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        print(f"✅ GitHub issue created for {product_name}")
    except Exception as e:
        print(f"❌ Failed to create GitHub issue: {e}")


def check_engraving():
    """Main function to check engraving availability"""
    config = load_fossil_config()
    history = load_engraving_history()
    
    print("\n" + "=" * 80)
    print("FOSSIL ENGRAVING AVAILABILITY CHECKER")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Product: {config['product_name']}")
    print("=" * 80)
    
    product_id = config['product_id']
    product_url = config['product_url']
    product_name = config['product_name']
    
    # Check availability
    result = check_engraving_availability(product_url, product_id)
    
    # Update history
    if product_id not in history:
        history[product_id] = {
            'product_name': product_name,
            'checks': []
        }
    
    history[product_id]['checks'].append(result)
    history[product_id]['last_checked'] = result['timestamp']
    history[product_id]['currently_available'] = result['available']
    
    # Keep only last 50 checks
    if len(history[product_id]['checks']) > 50:
        history[product_id]['checks'] = history[product_id]['checks'][-50:]
    
    # Save history
    save_engraving_history(history)
    
    print("\n" + "=" * 80)
    print("Check Complete")
    print("=" * 80 + "\n")
    
    # Exit codes for GitHub Actions notification
    if result['available'] is True:
        # Engraving is available - create issue and FAIL workflow to notify
        print("🎉 ENGRAVING IS AVAILABLE!")
        create_github_issue(product_name, product_url, product_id)
        print("\n🚨 EXITING WITH ERROR CODE 0 - Engraving available!")
        print("   GitHub Actions will FAIL and send you an email notification.")
        sys.exit(0)  # Exit 0 to trigger failure notification
    elif result['available'] is False:
        # Engraving is NOT available - pass silently
        print("⏳ Engraving still not available. Continuing to monitor...")
        print("\n✅ EXITING WITH CODE 1 - No change detected.")
        sys.exit(1)  # Exit 1 to pass silently
    else:
        # Error occurred
        print("⚠️ Unable to determine availability due to error.")
        print("\n✅ EXITING WITH CODE 1 - Error occurred.")
        sys.exit(1)


if __name__ == "__main__":
    check_engraving()
