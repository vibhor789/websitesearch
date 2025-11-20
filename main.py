#!/usr/bin/env python3
"""
Website Search & Chatbox Finder
Searches Google, analyzes websites for chatboxes, and generates leads for businesses
without proper customer support features.
"""

import logging
import sys
import time
from typing import List, Dict
from colorama import Fore, Style, init as colorama_init
from tqdm import tqdm

from config import Config
try:
    from google_searcher_improved import GoogleSearcherImproved as GoogleSearcher
except ImportError:
    from google_searcher import GoogleSearcher
from chatbox_detector import ChatboxDetector
from business_analyzer import BusinessAnalyzer
from sheets_manager import SheetsManager

# Initialize colorama for colored output
colorama_init(autoreset=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('websitesearch.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class WebsiteSearchApp:
    """Main application orchestrator"""

    def __init__(self):
        self.searcher = GoogleSearcher()
        self.detector = ChatboxDetector(use_ai=True)
        self.analyzer = BusinessAnalyzer()
        self.sheets_manager = SheetsManager()

        self.stats = {
            'total_searched': 0,
            'leads_found': 0,
            'has_support': 0,
            'errors': 0
        }

    def search_and_analyze(self, query: str, max_results: int = None):
        """
        Main workflow: Search Google and analyze results.

        Args:
            query: Google search query
            max_results: Maximum number of results to analyze
        """
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}Starting Website Search & Analysis")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}Query: {query}")
        print(f"Max Results: {max_results or Config.MAX_SEARCH_RESULTS}{Style.RESET_ALL}\n")

        # Step 1: Search Google
        print(f"{Fore.GREEN}[1/3] Searching Google...{Style.RESET_ALL}")
        search_results = self.searcher.search(query, max_results)

        if not search_results:
            print(f"{Fore.RED}No search results found. Please check your query or network connection.{Style.RESET_ALL}")
            return

        print(f"{Fore.GREEN}Found {len(search_results)} results{Style.RESET_ALL}\n")

        # Step 2: Analyze each website
        print(f"{Fore.GREEN}[2/3] Analyzing websites...{Style.RESET_ALL}\n")

        for result in tqdm(search_results, desc="Analyzing", unit="site"):
            self._analyze_website(result)
            # Small delay between sites
            time.sleep(1)

        # Step 3: Show summary
        print(f"\n{Fore.GREEN}[3/3] Analysis Complete!{Style.RESET_ALL}\n")
        self._print_summary()

    def _analyze_website(self, search_result: Dict):
        """Analyze a single website"""
        url = search_result['url']
        self.stats['total_searched'] += 1

        try:
            # Detect chatbox
            chatbox_result = self.detector.analyze_website(url)

            if chatbox_result.get('error'):
                logger.warning(f"Error analyzing {url}: {chatbox_result['error']}")
                self.stats['errors'] += 1
                return

            # Check if has support widget
            has_support = self.detector.has_support_widget(chatbox_result)

            if has_support:
                self.stats['has_support'] += 1
                logger.info(f"✓ {url} - Has support features, skipping")
            else:
                # This is a lead! Analyze business
                logger.info(f"★ {url} - No support features, analyzing business...")

                business_analysis = self.analyzer.analyze_business(
                    url=url,
                    page_title=search_result.get('title', ''),
                    snippet=search_result.get('snippet', ''),
                    chatbox_result=chatbox_result
                )

                # Add to sheet
                self.sheets_manager.add_lead(
                    search_result=search_result,
                    chatbox_result=chatbox_result,
                    business_analysis=business_analysis
                )

                self.stats['leads_found'] += 1

                # Print lead info
                self._print_lead(search_result, business_analysis)

        except Exception as e:
            logger.error(f"Error processing {url}: {e}", exc_info=True)
            self.stats['errors'] += 1

    def _print_lead(self, search_result: Dict, business_analysis: Dict):
        """Print lead information"""
        print(f"\n{Fore.YELLOW}{'─'*70}")
        print(f"{Fore.GREEN}★ NEW LEAD FOUND!")
        print(f"{Fore.YELLOW}{'─'*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Domain:{Style.RESET_ALL} {search_result['url']}")
        print(f"{Fore.CYAN}Type:{Style.RESET_ALL} {business_analysis.get('business_type', 'Unknown')}")
        print(f"{Fore.CYAN}Priority:{Style.RESET_ALL} {business_analysis.get('priority', 'Medium')}")
        print(f"{Fore.CYAN}Missing:{Style.RESET_ALL} {', '.join(business_analysis.get('missing_features', []))}")
        print(f"{Fore.YELLOW}{'─'*70}{Style.RESET_ALL}\n")

    def _print_summary(self):
        """Print final summary"""
        sheet_summary = self.sheets_manager.get_summary()

        print(f"{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}SUMMARY")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
        print(f"{Fore.GREEN}Websites Analyzed:{Style.RESET_ALL} {self.stats['total_searched']}")
        print(f"{Fore.GREEN}Leads Found:{Style.RESET_ALL} {self.stats['leads_found']} {Fore.YELLOW}★")
        print(f"{Fore.BLUE}Already Have Support:{Style.RESET_ALL} {self.stats['has_support']}")
        print(f"{Fore.RED}Errors:{Style.RESET_ALL} {self.stats['errors']}\n")

        print(f"{Fore.CYAN}Output:{Style.RESET_ALL}")
        print(f"  Type: {sheet_summary['output_type']}")
        print(f"  Location: {sheet_summary['location']}")
        print(f"  Total Leads Saved: {sheet_summary['total_leads']}\n")

        if self.stats['leads_found'] > 0:
            print(f"{Fore.GREEN}✓ {self.stats['leads_found']} potential leads saved!")
            print(f"{Fore.YELLOW}Check your output file for detailed analysis.{Style.RESET_ALL}\n")


def main():
    """Main entry point"""
    print(f"{Fore.CYAN}")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║        Website Search & Chatbox Finder                           ║")
    print("║        Find businesses without proper customer support           ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print(f"{Style.RESET_ALL}")

    # Validate configuration
    errors = Config.validate()
    if errors:
        print(f"\n{Fore.RED}Configuration errors:{Style.RESET_ALL}")
        for error in errors:
            print(f"  {Fore.RED}✗{Style.RESET_ALL} {error}")
        print(f"\n{Fore.YELLOW}Please check your .env file and fix the above errors.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}See SETUP.md for configuration instructions.{Style.RESET_ALL}\n")
        sys.exit(1)

    # Get search query
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
    else:
        print(f"\n{Fore.YELLOW}Enter your search query:{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Examples:{Style.RESET_ALL}")
        print("  - restaurants in New York")
        print("  - law firms in California")
        print("  - real estate agents in Miami")
        print("  - dental clinics in Texas\n")

        query = input(f"{Fore.GREEN}Query:{Style.RESET_ALL} ").strip()

        if not query:
            print(f"{Fore.RED}No query provided. Exiting.{Style.RESET_ALL}")
            sys.exit(1)

    # Create app and run
    app = WebsiteSearchApp()

    try:
        app.search_and_analyze(query)
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Process interrupted by user.{Style.RESET_ALL}")
        app._print_summary()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n{Fore.RED}Fatal error occurred. Check websitesearch.log for details.{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
