import logging
from typing import Dict, List
from config import Config

logger = logging.getLogger(__name__)

class BusinessAnalyzer:
    """
    Uses AI to analyze businesses and suggest what support widgets they should have.
    Analyzes business type, industry, and makes recommendations.
    """

    def __init__(self):
        self.ai_client = None
        self.ai_provider = None
        self._init_ai_client()

    def _init_ai_client(self):
        """Initialize AI client"""
        try:
            if Config.OPENAI_API_KEY:
                from openai import OpenAI
                self.ai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
                self.ai_provider = 'openai'
                logger.info("Using OpenAI for business analysis")
            elif Config.ANTHROPIC_API_KEY:
                from anthropic import Anthropic
                self.ai_client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)
                self.ai_provider = 'anthropic'
                logger.info("Using Anthropic for business analysis")
            else:
                logger.error("No AI API key configured")
        except Exception as e:
            logger.error(f"Failed to initialize AI client: {e}")

    def analyze_business(self, url: str, page_title: str, snippet: str,
                        chatbox_result: Dict) -> Dict:
        """
        Analyze a business and provide recommendations.

        Args:
            url: Website URL
            page_title: Page title from search results
            snippet: Snippet/description from search results
            chatbox_result: Result from chatbox detection

        Returns:
            Dict with business analysis and recommendations
        """
        logger.info(f"Analyzing business: {url}")

        if not self.ai_client:
            return self._basic_analysis(url, page_title, snippet, chatbox_result)

        try:
            # Prepare context for AI
            context = f"""
URL: {url}
Title: {page_title}
Description: {snippet}

Current Support Features:
- Has Chatbox: {chatbox_result.get('has_chatbox', False)}
- Has WhatsApp: {chatbox_result.get('has_whatsapp', False)}
- Has Call Button: {chatbox_result.get('has_call_button', False)}
- Detected Widgets: {', '.join(chatbox_result.get('detected_widgets', []))}
"""

            prompt = f"""{context}

Analyze this business and provide:
1. Business type/industry
2. Brief business description (1-2 sentences)
3. What support features are missing
4. What support features would benefit this business most
5. Priority level (High/Medium/Low) for adding support features

Respond in this exact JSON format:
{{
    "business_type": "type/industry",
    "business_description": "brief description",
    "missing_features": ["list", "of", "missing"],
    "recommended_features": ["list", "of", "recommended"],
    "recommendations_explanation": "why these features would help",
    "priority": "High/Medium/Low",
    "potential_impact": "explanation of business impact"
}}"""

            # Call AI
            if self.ai_provider == 'openai':
                response = self.ai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a business analyst expert in customer support and engagement strategies."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                response_text = response.choices[0].message.content

            elif self.ai_provider == 'anthropic':
                response = self.ai_client.messages.create(
                    model="claude-3-5-haiku-20241022",
                    max_tokens=1000,
                    temperature=0.7,
                    system="You are a business analyst expert in customer support and engagement strategies.",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                response_text = response.content[0].text

            # Parse JSON response
            import json
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0]
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0]

            analysis = json.loads(response_text.strip())
            logger.info(f"Business analysis complete: {analysis.get('business_type', 'Unknown')}")

            return analysis

        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return self._basic_analysis(url, page_title, snippet, chatbox_result)

    def _basic_analysis(self, url: str, page_title: str, snippet: str,
                       chatbox_result: Dict) -> Dict:
        """Basic analysis without AI"""
        missing = []
        if not chatbox_result.get('has_chatbox'):
            missing.append('Live Chat Widget')
        if not chatbox_result.get('has_whatsapp'):
            missing.append('WhatsApp Business')
        if not chatbox_result.get('has_call_button'):
            missing.append('Click-to-Call Button')

        return {
            'business_type': 'Unknown',
            'business_description': snippet[:200] if snippet else 'No description available',
            'missing_features': missing,
            'recommended_features': missing,
            'recommendations_explanation': 'Basic recommendation: Add missing support features',
            'priority': 'Medium',
            'potential_impact': 'Could improve customer engagement'
        }

    def generate_outreach_message(self, business_analysis: Dict, url: str) -> str:
        """
        Generate a personalized outreach message for the business.
        This can be used for sales/marketing purposes.
        """
        try:
            if not self.ai_client:
                return self._basic_outreach_message(business_analysis, url)

            prompt = f"""Based on this business analysis, write a brief, personalized outreach message
for a company that provides chat widgets and customer support solutions.

Business Type: {business_analysis.get('business_type', 'Unknown')}
Description: {business_analysis.get('business_description', '')}
Missing Features: {', '.join(business_analysis.get('missing_features', []))}
Recommended Features: {', '.join(business_analysis.get('recommended_features', []))}

Write a friendly, professional 2-3 sentence message that:
1. Shows you understand their business
2. Mentions specific missing support features
3. Highlights the potential benefit

Keep it concise and non-pushy."""

            if self.ai_provider == 'openai':
                response = self.ai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are an expert at writing personalized, helpful business outreach messages."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.8,
                    max_tokens=300
                )
                message = response.choices[0].message.content

            elif self.ai_provider == 'anthropic':
                response = self.ai_client.messages.create(
                    model="claude-3-5-haiku-20241022",
                    max_tokens=300,
                    temperature=0.8,
                    system="You are an expert at writing personalized, helpful business outreach messages.",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                message = response.content[0].text

            return message.strip()

        except Exception as e:
            logger.error(f"Failed to generate outreach message: {e}")
            return self._basic_outreach_message(business_analysis, url)

    def _basic_outreach_message(self, business_analysis: Dict, url: str) -> str:
        """Generate basic outreach message"""
        missing = ', '.join(business_analysis.get('missing_features', ['support features']))
        return f"We noticed your website could benefit from adding {missing}. " \
               f"These features could help improve customer engagement and support. " \
               f"Would you be interested in learning more?"


# For testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    analyzer = BusinessAnalyzer()

    # Test analysis
    chatbox_result = {
        'has_chatbox': False,
        'has_whatsapp': False,
        'has_call_button': True,
        'detected_widgets': ['call_button']
    }

    analysis = analyzer.analyze_business(
        url="https://example-restaurant.com",
        page_title="Best Italian Restaurant in NYC",
        snippet="Family-owned Italian restaurant serving authentic pasta and pizza",
        chatbox_result=chatbox_result
    )

    print("\nBusiness Analysis:")
    print(f"Type: {analysis['business_type']}")
    print(f"Description: {analysis['business_description']}")
    print(f"Missing: {', '.join(analysis['missing_features'])}")
    print(f"Recommended: {', '.join(analysis['recommended_features'])}")
    print(f"Priority: {analysis['priority']}")
    print(f"\nExplanation: {analysis['recommendations_explanation']}")

    message = analyzer.generate_outreach_message(analysis, "https://example-restaurant.com")
    print(f"\nOutreach Message:\n{message}")
