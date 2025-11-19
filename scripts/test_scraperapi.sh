#!/bin/bash
# Quick ScraperAPI service health check

cd /var/www/leadfinder
source venv/bin/activate

echo "Testing ScraperAPI service..."
echo "======================================"
echo ""

python3 << 'PYEND'
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('SCRAPER_API_KEY', '85b4c902f3a35f1e3fdd002ee1222a35')
test_url = 'https://httpbin.org/ip'

print("🔍 Testing ScraperAPI connection...")
print(f"API Key: {api_key[:10]}...{api_key[-5:]}")
print("")

try:
    response = requests.get(
        'http://api.scraperapi.com/',
        params={'api_key': api_key, 'url': test_url},
        timeout=30
    )

    if response.status_code == 200:
        print("✅ ScraperAPI is WORKING!")
        print(f"Status Code: {response.status_code}")
        print("")
        print("You can now continue with the CLI test:")
        print("  cd /var/www/leadfinder")
        print("  source venv/bin/activate")
        print("  export MAX_SEARCH_RESULTS=3")
        print("  python3 main.py")
        print("")
    else:
        print(f"❌ ScraperAPI returned error")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        print("")
        print("ScraperAPI is still experiencing issues.")
        print("Please wait and try again later.")
        print("")
except requests.exceptions.Timeout:
    print("❌ ScraperAPI request timed out")
    print("Service may still be experiencing issues.")
except Exception as e:
    print(f"❌ ScraperAPI test failed: {str(e)}")
    print("Service is not available yet.")

print("")
print("Check ScraperAPI status: https://status.scraperapi.com/")
PYEND
