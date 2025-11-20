import time
import random
import requests
from typing import List, Dict
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from config import Config
import logging

logger = logging.getLogger(__name__)

class GoogleSearcherImproved:
    """
    Improved Google searcher with better error handling and fallback methods.
    """

    def __init__(self):
        self.session = requests.Session()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        ]

    def search_with_scraper_api(self, query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """
        Search Google using ScraperAPI with optimized parameters.
        """
        logger.info(f"Searching with ScraperAPI: {query}")

        results = []
        search_url = f"https://www.google.com/search?q={quote_plus(query)}&num={max(max_results, 10)}"

        # Try ScraperAPI with different configurations
        configurations = [
            {
                'api_key': Config.SCRAPER_API_KEY,
                'url': search_url,
                'render': 'false',  # Faster, no JS rendering
                'country_code': 'us'
            },
            {
                'api_key': Config.SCRAPER_API_KEY,
                'url': search_url,
                'render': 'true',  # Fallback with JS rendering
                'country_code': 'us'
            }
        ]

        for i, params in enumerate(configurations, 1):
            try:
                logger.info(f"Attempt {i}/{len(configurations)} with render={params.get('render')}")

                response = requests.get(
                    'http://api.scraperapi.com/',
                    params=params,
                    timeout=90  # Increased timeout
                )

                if response.status_code == 200:
                    results = self._parse_google_results(response.text, max_results)
                    if results:
                        logger.info(f"Found {len(results)} results")
                        return results
                    else:
                        logger.warning(f"Attempt {i}: Got 200 but parsed 0 results")
                else:
                    logger.warning(f"Attempt {i}: Status {response.status_code}")

                # Wait between attempts
                if i < len(configurations):
                    time.sleep(5)

            except requests.exceptions.Timeout:
                logger.warning(f"Attempt {i}: Request timed out")
                if i < len(configurations):
                    time.sleep(5)
                continue
            except Exception as e:
                logger.error(f"Attempt {i} failed: {str(e)}")
                if i < len(configurations):
                    time.sleep(5)
                continue

        logger.error("All ScraperAPI attempts failed")
        return results

    def _parse_google_results(self, html: str, max_results: int) -> List[Dict[str, str]]:
        """
        Parse Google search results from HTML with multiple strategies.
        """
        results = []
        soup = BeautifulSoup(html, 'html.parser')

        # Strategy 1: Standard search result divs
        search_divs = soup.find_all('div', class_='g')
        logger.info(f"Strategy 1: Found {len(search_divs)} divs with class='g'")

        for div in search_divs[:max_results]:
            try:
                # Find title and link
                link_tag = div.find('a', href=True)
                if not link_tag:
                    continue

                url = link_tag['href']

                # Filter out non-website URLs
                if not url.startswith('http'):
                    continue
                if 'google.com' in url or 'youtube.com' in url:
                    continue

                # Get title
                title_tag = div.find('h3')
                title = title_tag.get_text() if title_tag else "No title"

                # Get snippet
                snippet_tag = div.find('div', {'data-sncf': '1'}) or div.find('span')
                snippet = snippet_tag.get_text() if snippet_tag else "No description"

                if url and title:
                    results.append({
                        'title': title.strip(),
                        'url': url.strip(),
                        'snippet': snippet.strip()[:200]
                    })

            except Exception as e:
                logger.debug(f"Error parsing result: {e}")
                continue

        # Strategy 2: If first strategy didn't work, try alternative selectors
        if not results:
            logger.info("Strategy 2: Trying alternative selectors")

            # Look for all links
            all_links = soup.find_all('a', href=True)

            for link in all_links:
                href = link.get('href', '')
                if href.startswith('http') and 'google.com' not in href:
                    title = link.get_text().strip()
                    if title and len(title) > 10:  # Reasonable title length
                        results.append({
                            'title': title[:100],
                            'url': href,
                            'snippet': f"Link from {href}"
                        })

                        if len(results) >= max_results:
                            break

        logger.info(f"Parsed {len(results)} results from HTML")
        return results

    def search(self, query: str, max_results: int = None) -> List[Dict[str, str]]:
        """
        Main search method.
        """
        if max_results is None:
            max_results = Config.MAX_SEARCH_RESULTS

        logger.info(f"Searching Google for: '{query}' (max {max_results} results)")

        # Add delay
        delay = random.uniform(2, 4)
        time.sleep(delay)

        if Config.USE_SCRAPER_API:
            results = self.search_with_scraper_api(query, max_results)
        else:
            logger.error("Direct search not supported - please enable ScraperAPI")
            results = []

        return results
