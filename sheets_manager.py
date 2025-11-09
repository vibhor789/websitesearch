import logging
import csv
import os
from typing import List, Dict
from datetime import datetime
from config import Config

logger = logging.getLogger(__name__)

class SheetsManager:
    """
    Manages output to Google Sheets or CSV files.
    Supports both Google Sheets API and local CSV export.
    """

    def __init__(self, use_google_sheets: bool = None):
        """
        Initialize sheets manager.

        Args:
            use_google_sheets: If True, use Google Sheets. If False, use CSV.
                              If None, auto-detect based on config.
        """
        if use_google_sheets is None:
            use_google_sheets = bool(Config.GOOGLE_SHEET_ID)

        self.use_google_sheets = use_google_sheets
        self.worksheet = None
        self.csv_path = None

        if self.use_google_sheets:
            self._init_google_sheets()
        else:
            self._init_csv()

    def _init_google_sheets(self):
        """Initialize Google Sheets connection"""
        try:
            import gspread
            from google.oauth2.service_account import Credentials

            logger.info("Initializing Google Sheets connection...")

            # Define scopes
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]

            # Authenticate
            creds = Credentials.from_service_account_file(
                Config.GOOGLE_SHEETS_CREDENTIALS,
                scopes=scopes
            )
            client = gspread.authorize(creds)

            # Open spreadsheet
            spreadsheet = client.open_by_key(Config.GOOGLE_SHEET_ID)

            # Get or create worksheet
            try:
                self.worksheet = spreadsheet.worksheet("Lead Results")
            except gspread.exceptions.WorksheetNotFound:
                self.worksheet = spreadsheet.add_worksheet(
                    title="Lead Results",
                    rows=1000,
                    cols=15
                )
                self._setup_headers()

            logger.info(f"Connected to Google Sheet: {spreadsheet.title}")

        except FileNotFoundError:
            logger.error(f"Credentials file not found: {Config.GOOGLE_SHEETS_CREDENTIALS}")
            logger.info("Falling back to CSV export")
            self.use_google_sheets = False
            self._init_csv()
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets: {e}")
            logger.info("Falling back to CSV export")
            self.use_google_sheets = False
            self._init_csv()

    def _init_csv(self):
        """Initialize CSV file"""
        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.csv_path = os.path.join(Config.OUTPUT_DIR, f"leads_{timestamp}.csv")
        logger.info(f"Will save results to CSV: {self.csv_path}")

        # Create file with headers
        self._write_csv_headers()

    def _setup_headers(self):
        """Set up spreadsheet headers"""
        headers = [
            'Timestamp',
            'Domain',
            'URL',
            'Business Type',
            'Business Description',
            'Has Chatbox',
            'Has WhatsApp',
            'Has Call Button',
            'Detected Widgets',
            'Missing Features',
            'Recommended Features',
            'Priority',
            'Recommendations',
            'Potential Impact',
            'Screenshot'
        ]

        if self.use_google_sheets:
            self.worksheet.update('A1:O1', [headers])
            # Format header row
            self.worksheet.format('A1:O1', {
                'textFormat': {'bold': True},
                'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
            })
        else:
            self.headers = headers

    def _write_csv_headers(self):
        """Write CSV headers"""
        headers = [
            'Timestamp',
            'Domain',
            'URL',
            'Business Type',
            'Business Description',
            'Has Chatbox',
            'Has WhatsApp',
            'Has Call Button',
            'Detected Widgets',
            'Missing Features',
            'Recommended Features',
            'Priority',
            'Recommendations',
            'Potential Impact',
            'Screenshot'
        ]

        with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

    def add_lead(self, search_result: Dict, chatbox_result: Dict,
                 business_analysis: Dict):
        """
        Add a lead to the sheet.

        Args:
            search_result: Result from Google search
            chatbox_result: Result from chatbox detection
            business_analysis: Result from business analysis
        """
        from urllib.parse import urlparse

        # Extract domain
        domain = urlparse(search_result['url']).netloc

        # Prepare row data
        row = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            domain,
            search_result['url'],
            business_analysis.get('business_type', 'Unknown'),
            business_analysis.get('business_description', ''),
            'Yes' if chatbox_result.get('has_chatbox') else 'No',
            'Yes' if chatbox_result.get('has_whatsapp') else 'No',
            'Yes' if chatbox_result.get('has_call_button') else 'No',
            ', '.join(chatbox_result.get('detected_widgets', [])),
            ', '.join(business_analysis.get('missing_features', [])),
            ', '.join(business_analysis.get('recommended_features', [])),
            business_analysis.get('priority', 'Medium'),
            business_analysis.get('recommendations_explanation', ''),
            business_analysis.get('potential_impact', ''),
            chatbox_result.get('screenshot_path', '')
        ]

        if self.use_google_sheets:
            try:
                self.worksheet.append_row(row)
                logger.info(f"Added lead to Google Sheet: {domain}")
            except Exception as e:
                logger.error(f"Failed to add row to Google Sheet: {e}")
                # Fallback to CSV
                self._append_to_csv(row)
        else:
            self._append_to_csv(row)

    def _append_to_csv(self, row: List):
        """Append row to CSV file"""
        try:
            with open(self.csv_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(row)
            logger.info(f"Added lead to CSV: {row[1]}")  # row[1] is domain
        except Exception as e:
            logger.error(f"Failed to write to CSV: {e}")

    def get_summary(self) -> Dict:
        """Get summary of leads collected"""
        if self.use_google_sheets and self.worksheet:
            try:
                all_rows = self.worksheet.get_all_values()
                total_leads = len(all_rows) - 1  # Subtract header row
                return {
                    'total_leads': total_leads,
                    'output_type': 'Google Sheets',
                    'location': f"Sheet ID: {Config.GOOGLE_SHEET_ID}"
                }
            except Exception as e:
                logger.error(f"Failed to get summary: {e}")

        if self.csv_path and os.path.exists(self.csv_path):
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                total_leads = sum(1 for _ in f) - 1  # Subtract header row
            return {
                'total_leads': total_leads,
                'output_type': 'CSV',
                'location': self.csv_path
            }

        return {
            'total_leads': 0,
            'output_type': 'Unknown',
            'location': 'N/A'
        }


# For testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    manager = SheetsManager(use_google_sheets=False)  # Force CSV for testing

    # Test data
    search_result = {
        'url': 'https://example-business.com',
        'title': 'Example Business - Quality Products',
        'snippet': 'We sell quality products'
    }

    chatbox_result = {
        'has_chatbox': False,
        'has_whatsapp': False,
        'has_call_button': True,
        'detected_widgets': ['call_button']
    }

    business_analysis = {
        'business_type': 'E-commerce',
        'business_description': 'Online store selling quality products',
        'missing_features': ['Live Chat', 'WhatsApp'],
        'recommended_features': ['Live Chat Widget', 'WhatsApp Business'],
        'recommendations_explanation': 'Adding live chat would help customers get instant support',
        'priority': 'High',
        'potential_impact': 'Could increase conversion rate by 15-20%'
    }

    manager.add_lead(search_result, chatbox_result, business_analysis)

    summary = manager.get_summary()
    print(f"\nSummary:")
    print(f"Total Leads: {summary['total_leads']}")
    print(f"Output Type: {summary['output_type']}")
    print(f"Location: {summary['location']}")
