#!/usr/bin/env python3
"""
Cost Calculator - Estimate costs before running searches
Helps you understand what your search will cost
"""

from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)

# Pricing (as of 2024, approximate)
PRICES = {
    'gpt4o_vision': 0.01,      # Per image analysis
    'gpt4o_mini_text': 0.0002, # Per text analysis
    'claude_vision': 0.008,     # Per image analysis
    'claude_text': 0.00015,     # Per text analysis
    'scraperapi': 0.0,          # Free tier: 5000/month
}

def calculate_cost(num_websites, with_screenshots=True, ai_provider='openai',
                   chatbox_percentage=30):
    """
    Calculate estimated cost

    Args:
        num_websites: Number of websites to analyze
        with_screenshots: Whether screenshots are enabled
        ai_provider: 'openai' or 'anthropic'
        chatbox_percentage: % of sites that already have chatboxes (won't be analyzed)
    """

    # How many sites need full analysis (don't have chatboxes)
    sites_to_analyze = int(num_websites * (chatbox_percentage / 100.0))

    # Cost per site
    if ai_provider == 'openai':
        vision_cost = PRICES['gpt4o_vision'] if with_screenshots else 0
        text_cost = PRICES['gpt4o_mini_text']
    else:  # anthropic
        vision_cost = PRICES['claude_vision'] if with_screenshots else 0
        text_cost = PRICES['claude_text']

    cost_per_site = vision_cost + text_cost

    # Total
    total_cost = sites_to_analyze * cost_per_site

    return {
        'total_sites': num_websites,
        'sites_with_chatbox': num_websites - sites_to_analyze,
        'sites_to_analyze': sites_to_analyze,
        'cost_per_site': cost_per_site,
        'total_cost': total_cost,
        'vision_cost': vision_cost,
        'text_cost': text_cost
    }

def print_estimate():
    """Interactive cost calculator"""

    print(f"{Fore.CYAN}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║           Cost Calculator                                 ║")
    print("║           Estimate your search costs                      ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"{Style.RESET_ALL}\n")

    # Get inputs
    print(f"{Fore.YELLOW}How many websites do you want to analyze?{Style.RESET_ALL}")
    print(f"{Fore.BLUE}(Tip: Start with 10 for testing){Style.RESET_ALL}")
    num_websites = int(input(f"{Fore.GREEN}Number of websites:{Style.RESET_ALL} ") or "10")

    print(f"\n{Fore.YELLOW}Enable screenshots? (more accurate but more expensive){Style.RESET_ALL}")
    print(f"{Fore.BLUE}(Tip: Say 'no' to save ~80% on costs){Style.RESET_ALL}")
    screenshots = input(f"{Fore.GREEN}Enable screenshots? (yes/no):{Style.RESET_ALL} ").lower()
    with_screenshots = screenshots in ['yes', 'y', '']

    print(f"\n{Fore.YELLOW}Which AI provider?{Style.RESET_ALL}")
    print(f"1. OpenAI (GPT-4) - Slightly more expensive, very accurate")
    print(f"2. Anthropic (Claude) - Slightly cheaper, also accurate")
    provider_choice = input(f"{Fore.GREEN}Choose (1/2, default=1):{Style.RESET_ALL} ") or "1"
    ai_provider = 'openai' if provider_choice == '1' else 'anthropic'

    print(f"\n{Fore.YELLOW}Estimate: What % of sites already have chatboxes?{Style.RESET_ALL}")
    print(f"{Fore.BLUE}(Typical: 20-40%. Sites WITH chatboxes are free to check!){Style.RESET_ALL}")
    chatbox_pct = int(input(f"{Fore.GREEN}Percentage (default=30):{Style.RESET_ALL} ") or "30")

    # Calculate
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"CALCULATING...{Style.RESET_ALL}\n")

    result = calculate_cost(num_websites, with_screenshots, ai_provider, chatbox_pct)

    # Display results
    print(f"{Fore.GREEN}📊 Cost Estimate:{Style.RESET_ALL}\n")

    print(f"{Fore.CYAN}Websites to check:{Style.RESET_ALL} {result['total_sites']}")
    print(f"{Fore.BLUE}  - Already have chatboxes:{Style.RESET_ALL} ~{result['sites_with_chatbox']} (FREE!)")
    print(f"{Fore.YELLOW}  - Need analysis:{Style.RESET_ALL} ~{result['sites_to_analyze']}")

    print(f"\n{Fore.CYAN}Cost per analyzed site:{Style.RESET_ALL}")
    if with_screenshots:
        print(f"  - Vision analysis: ${result['vision_cost']:.4f}")
    print(f"  - Text analysis: ${result['text_cost']:.4f}")
    print(f"  {Fore.GREEN}Total per site: ${result['cost_per_site']:.4f}{Style.RESET_ALL}")

    print(f"\n{Fore.GREEN}💰 TOTAL ESTIMATED COST: ${result['total_cost']:.2f}{Style.RESET_ALL}")

    # Show comparisons
    print(f"\n{Fore.YELLOW}💡 Ways to reduce cost:{Style.RESET_ALL}")

    if with_screenshots:
        no_screenshots = calculate_cost(num_websites, False, ai_provider, chatbox_pct)
        savings = result['total_cost'] - no_screenshots['total_cost']
        pct_saved = (savings / result['total_cost']) * 100
        print(f"  • Disable screenshots: Save ${savings:.2f} ({pct_saved:.0f}%)")

    if num_websites > 10:
        fewer_sites = calculate_cost(10, with_screenshots, ai_provider, chatbox_pct)
        print(f"  • Analyze only 10 sites: ${fewer_sites['total_cost']:.2f}")

    if ai_provider == 'openai':
        with_claude = calculate_cost(num_websites, with_screenshots, 'anthropic', chatbox_pct)
        savings = result['total_cost'] - with_claude['total_cost']
        if savings > 0:
            print(f"  • Use Anthropic Claude: Save ${savings:.2f}")

    # Show scaling
    print(f"\n{Fore.CYAN}📈 Cost at different scales:{Style.RESET_ALL}")
    for scale in [50, 100, 500]:
        if scale != num_websites:
            scaled = calculate_cost(scale, with_screenshots, ai_provider, chatbox_pct)
            print(f"  • {scale} websites: ${scaled['total_cost']:.2f}")

    # Free credits
    print(f"\n{Fore.GREEN}🎁 FREE CREDITS:{Style.RESET_ALL}")
    print(f"  • OpenAI new accounts: $5 free")
    if result['cost_per_site'] > 0:
        free_websites = int(5.0 / result['cost_per_site'])
        print(f"    → Can analyze ~{free_websites} websites FREE!")
    print(f"  • ScraperAPI: 5,000 requests/month FREE")
    print(f"    → Covers IP rotation at no cost")

    # Show if this search is free
    if result['total_cost'] < 5.0:
        print(f"\n{Fore.GREEN}✨ This search is covered by OpenAI's $5 free credit!{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")

    # Configuration recommendation
    print(f"\n{Fore.YELLOW}💾 Recommended .env settings for this search:{Style.RESET_ALL}\n")
    print(f"MAX_SEARCH_RESULTS={num_websites}")
    print(f"SCREENSHOT_ENABLED={'true' if with_screenshots else 'false'}")
    print(f"{'OPENAI_API_KEY' if ai_provider == 'openai' else 'ANTHROPIC_API_KEY'}=your-key-here")
    print(f"USE_SCRAPER_API=true  # To avoid IP blocks")

    print(f"\n{Fore.GREEN}Ready to run? Execute:{Style.RESET_ALL}")
    print(f'{Fore.CYAN}python main.py "your search query"{Style.RESET_ALL}\n')

def show_pricing_table():
    """Show detailed pricing table"""

    print(f"\n{Fore.CYAN}Detailed Pricing (per website):{Style.RESET_ALL}\n")

    print("┌─────────────────────────────────┬──────────────┬──────────────┐")
    print("│ Configuration                   │ Cost/Website │ 100 Websites │")
    print("├─────────────────────────────────┼──────────────┼──────────────┤")

    configs = [
        ("OpenAI + Screenshots", True, 'openai'),
        ("OpenAI, No Screenshots", False, 'openai'),
        ("Claude + Screenshots", True, 'anthropic'),
        ("Claude, No Screenshots", False, 'anthropic'),
    ]

    for name, screenshots, provider in configs:
        result = calculate_cost(100, screenshots, provider, 30)
        cost_per = result['cost_per_site']
        total = result['total_cost']
        print(f"│ {name:<31} │ ${cost_per:>11.4f} │ ${total:>11.2f} │")

    print("└─────────────────────────────────┴──────────────┴──────────────┘")

    print(f"\n{Fore.YELLOW}Note: Assumes 30% of sites already have chatboxes (typical){Style.RESET_ALL}")
    print(f"{Fore.BLUE}Actual costs may vary based on website complexity{Style.RESET_ALL}\n")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--table':
        show_pricing_table()
    else:
        try:
            print_estimate()
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Calculation cancelled.{Style.RESET_ALL}\n")
        except ValueError:
            print(f"\n{Fore.RED}Invalid input. Please enter numbers only.{Style.RESET_ALL}\n")
