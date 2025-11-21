import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from celery import Celery
from webapp.app import db, Search, Lead, app
from google_searcher_improved import GoogleSearcherImproved
from chatbox_detector import ChatboxDetector
from business_analyzer import BusinessAnalyzer
import logging

logger = logging.getLogger(__name__)

# Initialize Celery
celery_app = Celery('leadfinder',
                    broker='redis://localhost:6379/0',
                    backend='redis://localhost:6379/0')

@celery_app.task(bind=True)
def execute_search_task(self, search_id):
    """Execute a search in the background with customizable criteria"""

    with app.app_context():
        try:
            search = db.session.get(Search, search_id)
            if not search:
                logger.error(f"Search {search_id} not found")
                return

            # Update status
            search.status = 'running'
            db.session.commit()

            # Initialize components
            searcher = GoogleSearcherImproved()
            detector = ChatboxDetector(use_ai=True)
            analyzer = BusinessAnalyzer()

            # Search Google
            logger.info(f"Searching for: {search.query}")
            results = searcher.search(search.query, max_results=search.max_results)

            if not results:
                search.status = 'completed'
                search.error_message = 'No search results found'
                db.session.commit()
                return

            # Analyze each result
            leads_found = 0
            for result in results:
                try:
                    # Detect chatbox and collect contact info
                    analysis = detector.analyze_website(result['url'], collect_contacts=True)

                    # Check if this site matches the search criteria
                    matches_criteria = check_criteria_match(
                        analysis,
                        search.missing_chatbox,
                        search.missing_whatsapp,
                        search.missing_call_button
                    )

                    if matches_criteria:
                        # Analyze business
                        business_analysis = analyzer.analyze_business(
                            result['url'],
                            result['title'],
                            result['snippet'],
                            analysis
                        )

                        # Extract contact info
                        contact_info = analysis.get('contact_info', {})
                        emails_str = ', '.join(contact_info.get('emails', []))
                        phones_str = ', '.join(contact_info.get('phones', []))
                        social = contact_info.get('social_links', {})

                        # Create lead
                        lead = Lead(
                            search_id=search.id,
                            domain=result['url'],
                            url=result['url'],
                            business_description=result['title'],
                            business_type=business_analysis.get('business_type', 'Unknown'),
                            missing_features=', '.join(business_analysis.get('missing_features', [])),
                            recommended_features=business_analysis.get('recommendations', ''),
                            priority=business_analysis.get('priority', 'Medium'),
                            has_chatbox=analysis.get('has_chatbox', False),
                            has_whatsapp=analysis.get('has_whatsapp', False),
                            has_call_button=analysis.get('has_call_button', False),
                            # Contact information
                            emails=emails_str,
                            phones=phones_str,
                            contact_name=contact_info.get('contact_name'),
                            linkedin=social.get('linkedin', ''),
                            facebook=social.get('facebook', ''),
                            twitter=social.get('twitter', ''),
                            instagram=social.get('instagram', '')
                        )
                        db.session.add(lead)
                        leads_found += 1

                        logger.info(f"✓ Lead found: {result['title']} - {emails_str[:50]}")

                except Exception as e:
                    logger.error(f"Error analyzing {result['url']}: {e}")
                    continue

            # Update search status
            search.status = 'completed'
            search.leads_found = leads_found
            db.session.commit()

            logger.info(f"Search {search_id} completed. Found {leads_found} leads.")

        except Exception as e:
            logger.error(f"Search task failed: {e}")
            if search:
                search.status = 'failed'
                search.error_message = str(e)
                db.session.commit()

def check_criteria_match(analysis, need_missing_chatbox, need_missing_whatsapp, need_missing_call):
    """
    Check if a website matches the search criteria.
    Returns True if the site is missing the required features.
    """
    has_chatbox = analysis.get('has_chatbox', False)
    has_whatsapp = analysis.get('has_whatsapp', False)
    has_call_button = analysis.get('has_call_button', False)

    # Check each criterion
    criteria_met = []

    if need_missing_chatbox:
        criteria_met.append(not has_chatbox)  # Must NOT have chatbox

    if need_missing_whatsapp:
        criteria_met.append(not has_whatsapp)  # Must NOT have WhatsApp

    if need_missing_call:
        criteria_met.append(not has_call_button)  # Must NOT have call button

    # All selected criteria must be met
    return all(criteria_met) if criteria_met else False
