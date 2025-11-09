import time
import random
import os
import requests
from typing import List, Dict
from urllib.parse import quote_plus, urljoin
from bs4 import BeautifulSoup
from config import Config
import logging

logger = logging.getLogger(__name__)

class GoogleSearcher:
    """
    Performs Google searches with IP rotation to avoid being flagged.
    Supports multiple methods: direct scraping, proxy rotation, and ScraperAPI.
    """

    def __init__(self):
        self.session = requests.Session()
        self.proxies_list = []
        self.current_proxy_index = 0

        # Load proxies if enabled
        if Config.USE_PROXY:
            self._load_proxies()

        # User agents rotation to appear more human-like
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        ]

    def _load_proxies(self):
        """Load proxies from file"""
        try:
            if os.path.exists(Config.PROXY_LIST_FILE):
                with open(Config.PROXY_LIST_FILE, 'r') as f:
                    self.proxies_list = [line.strip() for line in f if line.strip()]
                logger.info(f"Loaded {len(self.proxies_list)} proxies")
            else:
                logger.warning(f"Proxy file not found: {Config.PROXY_LIST_FILE}")
        except Exception as e:
            logger.error(f"Error loading proxies: {e}")

    def _get_next_proxy(self) -> Dict[str, str]:
        """Get next proxy from rotation"""
        if not self.proxies_list:
            return None

        proxy = self.proxies_list[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies_list)

        return {
            'http': f'{Config.PROXY_TYPE}://{proxy}',
            'https': f'{Config.PROXY_TYPE}://{proxy}'
        }

    def _get_random_user_agent(self) -> str:
        """Get random user agent"""
        return random.choice(self.user_agents)

    def search_with_scraper_api(self, query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """
        Search Google using ScraperAPI (recommended for beginners - handles IP rotation automatically)
        Sign up at: https://www.scraperapi.com/
        """
        logger.info(f"Searching with ScraperAPI: {query}")

        results = []
        search_url = f"https://www.google.com/search?q={quote_plus(query)}&num={max_results}"

        # ScraperAPI endpoint
        api_url = f"http://api.scraperapi.com/?api_key={Config.SCRAPER_API_KEY}&url={quote_plus(search_url)}"

        try:
            response = requests.get(api_url, timeout=60)
            response.raise_for_status()

            results = self._parse_google_results(response.text, max_results)
            logger.info(f"Found {len(results)} results")

        except Exception as e:
            logger.error(f"ScraperAPI search failed: {e}")

        return results

    def search_with_proxies(self, query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """Search Google using proxy rotation"""
        logger.info(f"Searching with proxies: {query}")

        results = []
        search_url = f"https://www.google.com/search?q={quote_plus(query)}&num={max_results}"

        max_retries = min(3, len(self.proxies_list)) if self.proxies_list else 1

        for attempt in range(max_retries):
            try:
                headers = {'User-Agent': self._get_random_user_agent()}
                proxies = self._get_next_proxy() if Config.USE_PROXY else None

                logger.debug(f"Attempt {attempt + 1}/{max_retries}")

                response = self.session.get(
                    search_url,
                    headers=headers,
                    proxies=proxies,
                    timeout=30
                )
                response.raise_for_status()

                results = self._parse_google_results(response.text, max_results)
                logger.info(f"Found {len(results)} results")
                break

            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff

        return results

    def _parse_google_results(self, html: str, max_results: int) -> List[Dict[str, str]]:
        """Parse Google search results from HTML"""
        soup = BeautifulSoup(html, 'lxml')
        results = []

        # Find all search result divs
        search_results = soup.find_all('div', class_='g')

        for result in search_results[:max_results]:
            try:
                # Extract title
                title_elem = result.find('h3')
                title = title_elem.get_text() if title_elem else ''

                # Extract URL
                link_elem = result.find('a')
                url = link_elem.get('href') if link_elem else ''

                # Extract description/snippet
                snippet_elem = result.find('div', class_=['VwiC3b', 'IsZvec'])
                snippet = snippet_elem.get_text() if snippet_elem else ''

                if url and url.startswith('http'):
                    results.append({
                        'title': title.strip(),
                        'url': url.strip(),
                        'snippet': snippet.strip()
                    })
            except Exception as e:
                logger.debug(f"Error parsing result: {e}")
                continue

        return results

    def search(self, query: str, max_results: int = None) -> List[Dict[str, str]]:
        """
        Main search method - automatically chooses best available method
        """
        if max_results is None:
            max_results = Config.MAX_SEARCH_RESULTS

        logger.info(f"Searching Google for: '{query}' (max {max_results} results)")

        # Add random delay to appear more human-like
        delay = random.uniform(Config.SEARCH_DELAY_MIN, Config.SEARCH_DELAY_MAX)
        logger.debug(f"Waiting {delay:.1f}s before search...")
        time.sleep(delay)

        # Choose search method
        if Config.USE_SCRAPER_API:
            results = self.search_with_scraper_api(query, max_results)
        else:
            results = self.search_with_proxies(query, max_results)

        return results


# For testing
if __name__ == "__main__":
    import os
    logging.basicConfig(level=logging.INFO)

    searcher = GoogleSearcher()
    results = searcher.search("best restaurants in New York", max_results=5)

    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   Snippet: {result['snippet'][:100]}...")
