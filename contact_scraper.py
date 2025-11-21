"""
Contact Information Scraper
Extracts emails, phone numbers, and social media links from websites
"""

import re
import logging
from typing import Dict, List, Set
from urllib.parse import urlparse
from playwright.sync_api import Page

logger = logging.getLogger(__name__)

class ContactScraper:
    """Extract contact information from web pages"""

    # Regex patterns
    EMAIL_PATTERN = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
    PHONE_PATTERN = re.compile(r'(\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')

    # Social media patterns
    SOCIAL_PATTERNS = {
        'linkedin': re.compile(r'linkedin\.com/(?:company|in)/([a-zA-Z0-9-]+)'),
        'facebook': re.compile(r'facebook\.com/([a-zA-Z0-9.]+)'),
        'twitter': re.compile(r'twitter\.com/([a-zA-Z0-9_]+)'),
        'instagram': re.compile(r'instagram\.com/([a-zA-Z0-9_.]+)')
    }

    # Common spam/generic emails to exclude
    EXCLUDE_EMAILS = {
        'example.com', 'test.com', 'mail.com', 'email.com',
        'noreply@', 'no-reply@', 'donotreply@'
    }

    def __init__(self):
        pass

    def extract_from_page(self, page: Page, url: str) -> Dict:
        """
        Extract all contact information from a page

        Returns:
            dict with keys: emails, phones, social_links, contact_name
        """
        result = {
            'emails': [],
            'phones': [],
            'social_links': {},
            'contact_name': None
        }

        try:
            # Get page content
            body_text = page.inner_text('body')
            html_content = page.content()

            # Extract emails
            emails = self._extract_emails(body_text, url)
            result['emails'] = list(emails)[:5]  # Limit to 5 most relevant

            # Extract phone numbers
            phones = self._extract_phones(body_text)
            result['phones'] = list(phones)[:3]  # Limit to 3

            # Extract social media links
            result['social_links'] = self._extract_social_links(html_content)

            # Try to find contact person name
            result['contact_name'] = self._extract_contact_name(page, body_text)

            logger.info(f"Extracted: {len(result['emails'])} emails, "
                       f"{len(result['phones'])} phones from {url}")

        except Exception as e:
            logger.error(f"Error extracting contacts from {url}: {e}")

        return result

    def _extract_emails(self, text: str, url: str) -> Set[str]:
        """Extract and filter email addresses"""
        emails = set()
        domain = urlparse(url).netloc.replace('www.', '')

        for match in self.EMAIL_PATTERN.findall(text):
            email = match.lower().strip()

            # Skip excluded patterns
            if any(ex in email for ex in self.EXCLUDE_EMAILS):
                continue

            # Prefer emails from the same domain
            if domain in email:
                emails.add(email)
            elif len(emails) < 3:  # Add others if we don't have many
                emails.add(email)

        return emails

    def _extract_phones(self, text: str) -> Set[str]:
        """Extract and clean phone numbers"""
        phones = set()

        for match in self.PHONE_PATTERN.findall(text):
            # Join tuple if pattern captured groups
            phone = ''.join(match) if isinstance(match, tuple) else match
            phone = phone.strip()

            # Clean up formatting
            phone = re.sub(r'[^\d+()-]', '', phone)

            # Only keep if it looks valid (has at least 10 digits)
            if len(re.sub(r'\D', '', phone)) >= 10:
                phones.add(phone)

        return phones

    def _extract_social_links(self, html: str) -> Dict[str, str]:
        """Extract social media profile links"""
        social_links = {}

        for platform, pattern in self.SOCIAL_PATTERNS.items():
            matches = pattern.findall(html)
            if matches:
                # Get the first match (usually the main profile)
                username = matches[0]
                social_links[platform] = f"https://{platform}.com/{username}"

        return social_links

    def _extract_contact_name(self, page: Page, text: str) -> str:
        """Try to find contact person name"""
        try:
            # Look for common contact page patterns
            contact_selectors = [
                'h1:has-text("Contact")',
                'h2:has-text("Contact")',
                '.contact-name',
                '[itemprop="name"]',
                '.team-member h3',
                '.owner-name'
            ]

            for selector in contact_selectors:
                try:
                    element = page.query_selector(selector)
                    if element:
                        name = element.inner_text().strip()
                        # Basic validation - name should be 2-50 chars
                        if 2 <= len(name) <= 50 and not name.lower().startswith('contact'):
                            return name
                except:
                    continue

            # Fallback: look for "CEO", "Owner", "Founder" in text
            ceo_pattern = re.compile(r'(?:CEO|Owner|Founder)[:\s]+([A-Z][a-z]+\s+[A-Z][a-z]+)')
            match = ceo_pattern.search(text)
            if match:
                return match.group(1)

        except Exception as e:
            logger.debug(f"Could not extract contact name: {e}")

        return None

    def format_for_csv(self, contact_data: Dict) -> Dict[str, str]:
        """Format contact data for CSV export"""
        return {
            'emails': ', '.join(contact_data.get('emails', [])),
            'phones': ', '.join(contact_data.get('phones', [])),
            'contact_name': contact_data.get('contact_name') or '',
            'linkedin': contact_data.get('social_links', {}).get('linkedin', ''),
            'facebook': contact_data.get('social_links', {}).get('facebook', ''),
            'twitter': contact_data.get('social_links', {}).get('twitter', ''),
            'instagram': contact_data.get('social_links', {}).get('instagram', '')
        }
