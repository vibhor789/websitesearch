import time
import base64
import logging
from typing import Dict, List, Optional
from playwright.sync_api import sync_playwright, Page, TimeoutError as PlaywrightTimeout
from config import Config
import os

try:
    from contact_scraper import ContactScraper
    CONTACT_SCRAPER_AVAILABLE = True
except ImportError:
    CONTACT_SCRAPER_AVAILABLE = False

logger = logging.getLogger(__name__)

class ChatboxDetector:
    """
    Detects chatboxes, support widgets, WhatsApp buttons, and call buttons on websites.
    Uses AI vision to analyze screenshots and HTML structure analysis.
    """

    def __init__(self, use_ai: bool = True):
        self.use_ai = use_ai
        self.ai_client = None

        # Initialize AI client if available
        if use_ai:
            self._init_ai_client()

        # Common chatbox indicators
        self.chatbox_keywords = [
            'chat', 'support', 'help', 'whatsapp', 'messenger', 'intercom',
            'tawk', 'crisp', 'zendesk', 'livechat', 'drift', 'olark',
            'tidio', 'chatbot', 'live-chat', 'customer-support'
        ]

        self.whatsapp_indicators = [
            'whatsapp', 'wa.me', 'api.whatsapp.com', 'web.whatsapp.com'
        ]

        self.call_indicators = [
            'tel:', 'call', 'phone', 'contact-us', 'click-to-call'
        ]

    def _init_ai_client(self):
        """Initialize AI client for vision analysis"""
        try:
            if Config.OPENAI_API_KEY:
                from openai import OpenAI
                self.ai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
                self.ai_provider = 'openai'
                logger.info("Using OpenAI for chatbox detection")
            elif Config.ANTHROPIC_API_KEY:
                from anthropic import Anthropic
                self.ai_client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)
                self.ai_provider = 'anthropic'
                logger.info("Using Anthropic for chatbox detection")
        except Exception as e:
            logger.warning(f"Failed to initialize AI client: {e}")
            self.use_ai = False

    def analyze_website(self, url: str, collect_contacts: bool = True) -> Dict:
        """
        Analyze a website for chatboxes and support widgets.
        Optionally collect contact information.

        Returns detection results with confidence scores and contact info.
        """
        logger.info(f"Analyzing: {url}")

        result = {
            'url': url,
            'has_chatbox': False,
            'has_whatsapp': False,
            'has_call_button': False,
            'detected_widgets': [],
            'confidence': 0.0,
            'screenshot_path': None,
            'error': None,
            'contact_info': {}
        }

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
                )
                page = context.new_page()

                # Navigate to page
                logger.debug(f"Loading page: {url}")
                page.goto(url, wait_until='networkidle', timeout=Config.PAGE_LOAD_TIMEOUT * 1000)

                # Wait a bit for dynamic content (chat widgets often load after page)
                time.sleep(3)

                # Scroll to trigger lazy-loaded elements
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(1)
                page.evaluate("window.scrollTo(0, 0)")

                # Get page HTML
                html_content = page.content()

                # Take screenshot if enabled
                screenshot_path = None
                if Config.SCREENSHOT_ENABLED:
                    screenshot_path = self._save_screenshot(page, url)
                    result['screenshot_path'] = screenshot_path

                # Analyze HTML structure
                html_analysis = self._analyze_html(html_content, page)
                result.update(html_analysis)

                # Use AI vision if enabled and we have a screenshot
                if self.use_ai and screenshot_path:
                    ai_analysis = self._analyze_with_ai(screenshot_path)
                    # Combine HTML and AI analysis
                    result = self._combine_analyses(result, ai_analysis)

                # Extract contact information if requested
                if collect_contacts and CONTACT_SCRAPER_AVAILABLE:
                    try:
                        scraper = ContactScraper()
                        contact_data = scraper.extract_from_page(page, url)
                        result['contact_info'] = contact_data
                        logger.info(f"Collected {len(contact_data.get('emails', []))} emails, "
                                  f"{len(contact_data.get('phones', []))} phones")
                    except Exception as e:
                        logger.warning(f"Could not extract contacts: {e}")

                browser.close()

        except PlaywrightTimeout:
            logger.error(f"Timeout loading: {url}")
            result['error'] = 'Page load timeout'
        except Exception as e:
            logger.error(f"Error analyzing {url}: {e}")
            result['error'] = str(e)

        return result

    def _analyze_html(self, html: str, page: Page) -> Dict:
        """Analyze HTML structure for chatbox indicators"""
        result = {
            'has_chatbox': False,
            'has_whatsapp': False,
            'has_call_button': False,
            'detected_widgets': [],
            'confidence': 0.0
        }

        html_lower = html.lower()

        # Check for chatbox widgets
        for keyword in self.chatbox_keywords:
            if keyword in html_lower:
                result['has_chatbox'] = True
                if keyword not in result['detected_widgets']:
                    result['detected_widgets'].append(keyword)

        # Check for WhatsApp
        for indicator in self.whatsapp_indicators:
            if indicator in html_lower:
                result['has_whatsapp'] = True
                if 'whatsapp' not in result['detected_widgets']:
                    result['detected_widgets'].append('whatsapp')

        # Check for call buttons
        for indicator in self.call_indicators:
            if indicator in html_lower:
                result['has_call_button'] = True
                if 'call_button' not in result['detected_widgets']:
                    result['detected_widgets'].append('call_button')

        # Try to find visible chat widgets using selectors
        try:
            chat_selectors = [
                '[class*="chat"]',
                '[id*="chat"]',
                '[class*="support"]',
                '[id*="support"]',
                'iframe[src*="crisp"]',
                'iframe[src*="tawk"]',
                'iframe[src*="intercom"]',
                'iframe[src*="drift"]',
                '[class*="whatsapp"]',
                '[id*="whatsapp"]'
            ]

            for selector in chat_selectors:
                elements = page.query_selector_all(selector)
                if elements:
                    # Check if element is visible
                    for elem in elements:
                        if elem.is_visible():
                            result['has_chatbox'] = True
                            break

        except Exception as e:
            logger.debug(f"Error checking selectors: {e}")

        # Calculate confidence based on number of indicators
        if result['detected_widgets']:
            result['confidence'] = min(len(result['detected_widgets']) * 0.3, 0.9)

        return result

    def _analyze_with_ai(self, screenshot_path: str) -> Dict:
        """Use AI vision to analyze screenshot for chatboxes"""
        logger.debug("Using AI vision analysis")

        try:
            # Read and encode image
            with open(screenshot_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')

            prompt = """Analyze this website screenshot and identify:
1. Is there a chatbox or chat widget visible? (usually at bottom right)
2. Is there a WhatsApp button or widget?
3. Is there a phone/call button visible?
4. What support/contact widgets do you see?

Respond in this exact JSON format:
{
    "has_chatbox": true/false,
    "has_whatsapp": true/false,
    "has_call_button": true/false,
    "detected_widgets": ["list", "of", "widgets"],
    "confidence": 0.0-1.0,
    "explanation": "brief explanation"
}"""

            if self.ai_provider == 'openai':
                response = self.ai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{image_data}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=500
                )
                response_text = response.choices[0].message.content

            elif self.ai_provider == 'anthropic':
                response = self.ai_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=500,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": "image/png",
                                        "data": image_data
                                    }
                                },
                                {
                                    "type": "text",
                                    "text": prompt
                                }
                            ]
                        }
                    ]
                )
                response_text = response.content[0].text

            # Parse JSON response
            import json
            # Extract JSON from response (might be wrapped in markdown)
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0]
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0]

            ai_result = json.loads(response_text.strip())
            logger.info(f"AI analysis: {ai_result.get('explanation', 'No explanation')}")
            return ai_result

        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return {}

    def _combine_analyses(self, html_result: Dict, ai_result: Dict) -> Dict:
        """Combine HTML and AI analysis results"""
        if not ai_result:
            return html_result

        # Merge results - AI takes precedence but we combine detected widgets
        combined = {
            'has_chatbox': html_result['has_chatbox'] or ai_result.get('has_chatbox', False),
            'has_whatsapp': html_result['has_whatsapp'] or ai_result.get('has_whatsapp', False),
            'has_call_button': html_result['has_call_button'] or ai_result.get('has_call_button', False),
            'detected_widgets': list(set(html_result['detected_widgets'] + ai_result.get('detected_widgets', []))),
            'confidence': max(html_result['confidence'], ai_result.get('confidence', 0)),
            'ai_explanation': ai_result.get('explanation', ''),
            'screenshot_path': html_result['screenshot_path'],
            'url': html_result['url']
        }

        return combined

    def _save_screenshot(self, page: Page, url: str) -> str:
        """Save screenshot of the page"""
        try:
            os.makedirs(Config.SCREENSHOTS_DIR, exist_ok=True)

            # Create filename from URL
            from urllib.parse import urlparse
            domain = urlparse(url).netloc.replace('.', '_')
            timestamp = int(time.time())
            filename = f"{domain}_{timestamp}.png"
            filepath = os.path.join(Config.SCREENSHOTS_DIR, filename)

            page.screenshot(path=filepath, full_page=False)
            logger.debug(f"Screenshot saved: {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Failed to save screenshot: {e}")
            return None

    def has_support_widget(self, analysis_result: Dict) -> bool:
        """Check if website has any support widget"""
        return (
            analysis_result.get('has_chatbox', False) or
            analysis_result.get('has_whatsapp', False) or
            analysis_result.get('has_call_button', False)
        )


# For testing
if __name__ == "__main__":
    import os
    logging.basicConfig(level=logging.INFO)

    detector = ChatboxDetector(use_ai=True)

    # Test with a few websites
    test_urls = [
        "https://www.intercom.com",  # Has chatbox
        "https://example.com",  # No chatbox
    ]

    for url in test_urls:
        print(f"\n{'='*60}")
        result = detector.analyze_website(url)
        print(f"URL: {result['url']}")
        print(f"Has Chatbox: {result['has_chatbox']}")
        print(f"Has WhatsApp: {result['has_whatsapp']}")
        print(f"Has Call Button: {result['has_call_button']}")
        print(f"Widgets: {result['detected_widgets']}")
        print(f"Confidence: {result['confidence']:.2f}")
        if result.get('ai_explanation'):
            print(f"AI Explanation: {result['ai_explanation']}")
