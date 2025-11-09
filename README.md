# Website Search & Chatbox Finder

Automatically search Google, analyze websites for chatboxes and support widgets, and generate qualified leads for businesses that could benefit from better customer support tools.

## What Does This Do?

This application:
1. Searches Google for your target businesses (e.g., "restaurants in NYC")
2. Visits each website from the search results
3. Uses AI to check if they have:
   - Live chat widgets
   - WhatsApp integration
   - Call buttons
   - Other support features
4. For businesses WITHOUT these features:
   - Analyzes their business type
   - Identifies what they're missing
   - Recommends which support features would help them
   - Saves everything to Google Sheets or CSV

Perfect for:
- Lead generation for chat widget/support software companies
- Market research on customer support adoption
- Finding businesses that need better customer engagement tools

## Key Features

- **Smart Google Search** with IP rotation (won't get blocked!)
- **AI-Powered Detection** using GPT-4 Vision or Claude
- **Business Analysis** to understand what each business needs
- **Automatic Lead Saving** to Google Sheets or CSV
- **Screenshot Capture** for verification
- **Rate Limiting** to stay within API limits
- **Beautiful Console Output** with progress tracking

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt
playwright install chromium

# 2. Set up your API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 3. Run it!
python main.py "restaurants in New York"
```

Results will be saved to `output/leads_[timestamp].csv`

## Full Setup

See [SETUP.md](SETUP.md) for detailed instructions on:
- Getting API keys (OpenAI, Anthropic)
- Setting up IP rotation (ScraperAPI, proxies)
- Configuring Google Sheets integration
- Troubleshooting common issues

## Example Usage

```bash
# Find law firms
python main.py "law firms in California"

# Find dental clinics
python main.py "dental clinics in Texas"

# Find real estate agents
python main.py "real estate agents in Miami"

# Find SaaS companies
python main.py "B2B SaaS companies"
```

## Output Example

The app will find businesses and save details like:

| Domain | Business Type | Missing Features | Priority | Recommendation |
|--------|---------------|------------------|----------|----------------|
| example-restaurant.com | Restaurant | Live Chat, WhatsApp | High | Adding WhatsApp would help with reservations and customer inquiries |
| law-firm-example.com | Legal Services | Live Chat | Medium | Live chat would help capture leads during business hours |

## Configuration

Edit `.env` to customize:

```bash
# Required: AI API (choose one)
OPENAI_API_KEY=sk-your-key-here
# or
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Optional: IP Rotation (recommended)
USE_SCRAPER_API=true
SCRAPER_API_KEY=your-key-here

# Optional: Google Sheets
GOOGLE_SHEET_ID=your-sheet-id
GOOGLE_SHEETS_CREDENTIALS=credentials.json

# Search settings
MAX_SEARCH_RESULTS=10
SEARCH_DELAY_MIN=2
SEARCH_DELAY_MAX=5
```

## How It Works

### 1. Google Search Module (`google_searcher.py`)
- Searches Google with your query
- Supports three methods:
  - **ScraperAPI**: Automatic IP rotation (recommended)
  - **Proxy Rotation**: Use your own proxy list
  - **Direct**: Simple requests (testing only)
- Includes random delays and user agent rotation

### 2. Chatbox Detector (`chatbox_detector.py`)
- Loads each website using Playwright (real browser)
- Analyzes HTML for chatbox indicators
- Takes screenshots
- Uses AI vision to confirm findings
- Detects: chat widgets, WhatsApp, call buttons

### 3. Business Analyzer (`business_analyzer.py`)
- Uses AI to understand the business type
- Identifies missing support features
- Recommends specific improvements
- Generates outreach messages

### 4. Sheets Manager (`sheets_manager.py`)
- Saves leads to Google Sheets or CSV
- Organizes data in clean, readable format
- Includes all analysis and recommendations

## Requirements

- Python 3.9+
- OpenAI API key or Anthropic API key
- (Optional) ScraperAPI key for IP rotation
- (Optional) Google Sheets credentials

## Project Structure

```
websitesearch/
├── main.py                  # Main application
├── config.py                # Configuration management
├── google_searcher.py       # Google search with IP rotation
├── chatbox_detector.py      # AI-powered chatbox detection
├── business_analyzer.py     # Business analysis & recommendations
├── sheets_manager.py        # Google Sheets & CSV export
├── requirements.txt         # Python dependencies
├── .env.example            # Example environment variables
├── SETUP.md                # Detailed setup guide
└── README.md               # This file
```

## Cost Estimates

Based on analyzing 100 websites:

- **OpenAI API**: ~$2-5 (using GPT-4o and GPT-4o-mini)
- **ScraperAPI**: Free tier includes 5,000 requests/month
- **Alternative proxies**: $5-15/month for residential proxies

Total: Can run for **free** on the free tiers, or ~$5-10/month for heavy usage.

## Best Practices

1. **Start small**: Test with 5-10 results first
2. **Use ScraperAPI**: Easier than managing proxies yourself
3. **Monitor costs**: Check your OpenAI usage dashboard
4. **Respect rate limits**: Don't set delays too low
5. **Backup results**: CSV files auto-save to `output/` folder

## Limitations

- Google may still block you without IP rotation
- Some websites block automated browsers
- AI detection is ~90-95% accurate (not 100%)
- Rate limits apply to all APIs
- Some pages load very slowly

## Troubleshooting

See [SETUP.md](SETUP.md#troubleshooting) for solutions to common issues.

## Legal & Ethical Considerations

This tool is for:
- ✅ Legitimate lead generation
- ✅ Market research
- ✅ Business development

Please:
- Respect robots.txt
- Use reasonable rate limits
- Follow terms of service for all APIs
- Use collected data ethically

## License

MIT License - feel free to modify and use for your needs.

## Contributing

This is a starter project! Feel free to:
- Add new detection methods
- Improve AI prompts
- Add support for more output formats
- Optimize performance

## Support

For issues:
1. Check `websitesearch.log`
2. Review [SETUP.md](SETUP.md)
3. Make sure all API keys are correctly configured

## Future Enhancements

Potential improvements:
- [ ] Detect more widget types (Facebook Messenger, etc.)
- [ ] Multi-language support
- [ ] Batch processing mode
- [ ] Custom AI prompts
- [ ] Email finder integration
- [ ] LinkedIn company matching
- [ ] CRM integration (HubSpot, Salesforce)

---

Made with ❤️ for finding better business opportunities
