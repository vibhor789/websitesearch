#!/usr/bin/env python3
"""
Test script to verify your setup is correct.
Run this before using the main application.
"""

import os
import sys
from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)

def print_header(text):
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}{text}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

def print_success(text):
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")

def print_error(text):
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")

def print_warning(text):
    print(f"{Fore.YELLOW}⚠ {text}{Style.RESET_ALL}")

def test_python_version():
    """Test Python version"""
    print_header("Checking Python Version")
    version = sys.version_info
    if version >= (3, 9):
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} - Need 3.9 or higher")
        return False

def test_dependencies():
    """Test if required packages are installed"""
    print_header("Checking Dependencies")

    required_packages = [
        ('playwright', 'Playwright'),
        ('requests', 'Requests'),
        ('beautifulsoup4', 'BeautifulSoup4'),
        ('openai', 'OpenAI'),
        ('anthropic', 'Anthropic'),
        ('gspread', 'GSpread'),
        ('colorama', 'Colorama'),
        ('tqdm', 'TQDM'),
        ('dotenv', 'Python-dotenv'),
    ]

    all_installed = True
    for package, name in required_packages:
        try:
            __import__(package)
            print_success(f"{name}")
        except ImportError:
            print_error(f"{name} - Not installed")
            all_installed = False

    if not all_installed:
        print(f"\n{Fore.YELLOW}Install missing packages with:{Style.RESET_ALL}")
        print("pip install -r requirements.txt")

    return all_installed

def test_playwright():
    """Test Playwright browser"""
    print_header("Checking Playwright Browser")
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            browser.close()
        print_success("Playwright Chromium browser is installed")
        return True
    except Exception as e:
        print_error(f"Playwright browser not installed: {e}")
        print(f"\n{Fore.YELLOW}Install with:{Style.RESET_ALL}")
        print("playwright install chromium")
        return False

def test_env_file():
    """Test .env file configuration"""
    print_header("Checking Configuration (.env)")

    if not os.path.exists('.env'):
        print_error(".env file not found")
        print(f"\n{Fore.YELLOW}Create .env file with:{Style.RESET_ALL}")
        print("cp .env.example .env")
        return False

    print_success(".env file exists")

    # Load .env
    from dotenv import load_dotenv
    load_dotenv()

    # Check API keys
    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')

    has_ai = False
    if openai_key and openai_key != 'your_openai_api_key_here':
        print_success("OpenAI API key configured")
        has_ai = True
    elif anthropic_key and anthropic_key != 'your_anthropic_api_key_here':
        print_success("Anthropic API key configured")
        has_ai = True
    else:
        print_error("No AI API key configured")
        print(f"\n{Fore.YELLOW}Add to .env:{Style.RESET_ALL}")
        print("OPENAI_API_KEY=sk-your-key-here")
        print("or")
        print("ANTHROPIC_API_KEY=sk-ant-your-key-here")

    # Check optional configurations
    if os.getenv('USE_SCRAPER_API', 'false').lower() == 'true':
        if os.getenv('SCRAPER_API_KEY') and os.getenv('SCRAPER_API_KEY') != 'your_scraper_api_key_here':
            print_success("ScraperAPI configured")
        else:
            print_warning("ScraperAPI enabled but no key found")

    if os.getenv('GOOGLE_SHEET_ID'):
        if os.path.exists(os.getenv('GOOGLE_SHEETS_CREDENTIALS', 'credentials.json')):
            print_success("Google Sheets configured")
        else:
            print_warning("Google Sheet ID set but credentials file not found")
    else:
        print_warning("Google Sheets not configured (will use CSV)")

    return has_ai

def test_network():
    """Test network connectivity"""
    print_header("Checking Network")
    try:
        import requests
        response = requests.get('https://www.google.com', timeout=5)
        if response.status_code == 200:
            print_success("Internet connection working")
            return True
        else:
            print_error("Cannot reach Google")
            return False
    except Exception as e:
        print_error(f"Network error: {e}")
        return False

def test_ai_api():
    """Test AI API connection"""
    print_header("Testing AI API")

    from dotenv import load_dotenv
    load_dotenv()

    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')

    if openai_key and openai_key != 'your_openai_api_key_here':
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)
            # Simple test call
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "Say 'test successful'"}],
                max_tokens=10
            )
            print_success("OpenAI API is working!")
            return True
        except Exception as e:
            print_error(f"OpenAI API error: {e}")
            return False

    elif anthropic_key and anthropic_key != 'your_anthropic_api_key_here':
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=anthropic_key)
            response = client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=10,
                messages=[{"role": "user", "content": "Say 'test successful'"}]
            )
            print_success("Anthropic API is working!")
            return True
        except Exception as e:
            print_error(f"Anthropic API error: {e}")
            return False

    print_warning("Skipping API test - no API key configured")
    return False

def main():
    print(f"{Fore.CYAN}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║           Setup Verification Test                        ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"{Style.RESET_ALL}")

    results = {
        'Python Version': test_python_version(),
        'Dependencies': test_dependencies(),
        'Playwright': test_playwright(),
        'Configuration': test_env_file(),
        'Network': test_network(),
    }

    # Only test AI API if configuration is good
    if results['Configuration']:
        results['AI API'] = test_ai_api()

    # Summary
    print_header("Summary")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        if result:
            print_success(test_name)
        else:
            print_error(test_name)

    print(f"\n{Fore.CYAN}Passed: {passed}/{total}{Style.RESET_ALL}\n")

    if passed == total:
        print(f"{Fore.GREEN}✓ All tests passed! You're ready to go!{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Run the app with:{Style.RESET_ALL}")
        print(f'{Fore.CYAN}python main.py "restaurants in New York"{Style.RESET_ALL}\n')
        return 0
    else:
        print(f"{Fore.RED}✗ Some tests failed. Please fix the issues above.{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}See SETUP.md for detailed instructions.{Style.RESET_ALL}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
