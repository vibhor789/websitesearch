import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""

    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

    # Google Sheets
    GOOGLE_SHEETS_CREDENTIALS = os.getenv('GOOGLE_SHEETS_CREDENTIALS', 'credentials.json')
    GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID')

    # Proxy Settings
    USE_PROXY = os.getenv('USE_PROXY', 'false').lower() == 'true'
    PROXY_LIST_FILE = os.getenv('PROXY_LIST_FILE', 'proxies.txt')
    PROXY_TYPE = os.getenv('PROXY_TYPE', 'http')

    # ScraperAPI
    USE_SCRAPER_API = os.getenv('USE_SCRAPER_API', 'false').lower() == 'true'
    SCRAPER_API_KEY = os.getenv('SCRAPER_API_KEY')

    # Search Settings
    MAX_SEARCH_RESULTS = int(os.getenv('MAX_SEARCH_RESULTS', 10))
    SEARCH_DELAY_MIN = int(os.getenv('SEARCH_DELAY_MIN', 2))
    SEARCH_DELAY_MAX = int(os.getenv('SEARCH_DELAY_MAX', 5))

    # Website Analysis
    PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', 30))
    SCREENSHOT_ENABLED = os.getenv('SCREENSHOT_ENABLED', 'true').lower() == 'true'

    # Output
    OUTPUT_DIR = 'output'
    SCREENSHOTS_DIR = os.path.join(OUTPUT_DIR, 'screenshots')

    @staticmethod
    def validate():
        """Validate required configuration"""
        errors = []

        if not Config.OPENAI_API_KEY and not Config.ANTHROPIC_API_KEY:
            errors.append("Either OPENAI_API_KEY or ANTHROPIC_API_KEY must be set")

        if Config.GOOGLE_SHEET_ID and not os.path.exists(Config.GOOGLE_SHEETS_CREDENTIALS):
            errors.append(f"Google Sheets credentials file not found: {Config.GOOGLE_SHEETS_CREDENTIALS}")

        if Config.USE_SCRAPER_API and not Config.SCRAPER_API_KEY:
            errors.append("SCRAPER_API_KEY must be set when USE_SCRAPER_API=true")

        return errors
