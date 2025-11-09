# Usage Guide - Getting the Most Out of Your Lead Finder

This guide shows you how to use the Website Search & Chatbox Finder effectively.

## Basic Usage

### Simple Search

```bash
python main.py "your search query"
```

### Interactive Mode

```bash
python main.py
# You'll be prompted to enter your search query
```

### Using Convenience Scripts

```bash
# Mac/Linux
./run.sh "restaurants in New York"

# Windows
run.bat "restaurants in New York"
```

## Search Query Tips

### Target Industries

Good examples:
- `"restaurants in [city]"` - Food & hospitality
- `"law firms in [state]"` - Legal services
- `"dental clinics in [city]"` - Healthcare
- `"real estate agents [location]"` - Real estate
- `"plumbers in [city]"` - Home services
- `"yoga studios [location]"` - Fitness & wellness
- `"boutique hotels [location]"` - Hospitality
- `"veterinary clinics [city]"` - Pet services
- `"accounting firms [location]"` - Professional services

### Business Types by Priority

**High Priority** (businesses that really need chat support):
- E-commerce stores
- SaaS companies
- Service businesses (plumbers, electricians)
- Healthcare providers
- Real estate
- Legal services

**Medium Priority**:
- Restaurants
- Retail stores
- Educational institutions
- Consulting firms

**Lower Priority**:
- Manufacturing
- Warehouses
- Government sites

### Advanced Search Operators

Use Google search operators for better targeting:

```bash
# Find specific types of sites
python main.py "dental clinic site:.com"

# Exclude certain results
python main.py "restaurant -chain -franchise"

# Find sites in a location
python main.py "boutique hotel near:miami"

# Find sites with specific keywords
python main.py '"spa" "massage" location:california'
```

## Configuration Options

Edit `.env` to customize behavior:

### Search Settings

```bash
# How many websites to analyze
MAX_SEARCH_RESULTS=10

# Delay between searches (seconds)
SEARCH_DELAY_MIN=2
SEARCH_DELAY_MAX=5

# How long to wait for pages to load
PAGE_LOAD_TIMEOUT=30

# Enable/disable screenshots
SCREENSHOT_ENABLED=true
```

### Performance Tuning

**Fast & Cheap** (fewer websites, less accurate):
```bash
MAX_SEARCH_RESULTS=5
SEARCH_DELAY_MIN=1
SEARCH_DELAY_MAX=2
SCREENSHOT_ENABLED=false
```

**Thorough & Accurate** (more websites, better analysis):
```bash
MAX_SEARCH_RESULTS=20
SEARCH_DELAY_MIN=3
SEARCH_DELAY_MAX=6
SCREENSHOT_ENABLED=true
```

**Balanced** (recommended):
```bash
MAX_SEARCH_RESULTS=10
SEARCH_DELAY_MIN=2
SEARCH_DELAY_MAX=5
SCREENSHOT_ENABLED=true
```

## Understanding Results

### CSV Output

Results are saved to `output/leads_[timestamp].csv` with these columns:

- **Timestamp** - When the lead was found
- **Domain** - Website domain
- **URL** - Full website URL
- **Business Type** - Industry/category (e.g., "Restaurant", "Law Firm")
- **Business Description** - Brief description
- **Has Chatbox** - Yes/No
- **Has WhatsApp** - Yes/No
- **Has Call Button** - Yes/No
- **Detected Widgets** - List of widgets found
- **Missing Features** - What they don't have
- **Recommended Features** - What they should add
- **Priority** - High/Medium/Low urgency
- **Recommendations** - Why they need these features
- **Potential Impact** - Business value explanation
- **Screenshot** - Path to screenshot file

### Priority Levels

- **High**: Business would significantly benefit, likely ready to buy
- **Medium**: Could benefit but not critical
- **Low**: Nice to have but not urgent

Focus your outreach on "High" priority leads first!

## Best Practices

### 1. Start with a Test Run

```bash
# Test with just 3 results
# Edit .env: MAX_SEARCH_RESULTS=3
python main.py "test search restaurants"
```

Verify:
- CSV is created
- Screenshots are saved
- No errors in log
- Results look good

### 2. Use Specific Locations

✅ Good: `"dental clinics in Austin Texas"`
❌ Too broad: `"dental clinics"`

Specific locations give you:
- More relevant results
- Local businesses (better leads)
- Easier to target with outreach

### 3. Batch by Industry

Run separate searches for each industry:

```bash
python main.py "restaurants in Miami"
python main.py "yoga studios in Miami"
python main.py "law firms in Miami"
```

This helps you:
- Tailor your outreach message
- Understand industry-specific needs
- Compare different markets

### 4. Monitor Your Costs

Check regularly:
- OpenAI: https://platform.openai.com/usage
- ScraperAPI: https://dashboard.scraperapi.com/

Typical costs:
- 10 websites: ~$0.50
- 50 websites: ~$2-3
- 100 websites: ~$5

### 5. Use IP Rotation

Always use ScraperAPI or proxies to avoid:
- Getting blocked by Google
- IP bans
- CAPTCHA challenges

Without IP rotation, you'll likely get blocked after 20-30 searches.

## Workflow Examples

### Example 1: Local Business Lead Gen

Goal: Find 50 restaurant leads in New York

```bash
# Configure
# Edit .env: MAX_SEARCH_RESULTS=50, USE_SCRAPER_API=true

# Run search
python main.py "restaurants in New York"

# Results
# - 50 websites analyzed
# - ~20-30 leads found (businesses without chat)
# - Saved to output/leads_[timestamp].csv

# Next steps
# 1. Open CSV in Excel/Google Sheets
# 2. Sort by Priority (High first)
# 3. Filter for specific features (e.g., no WhatsApp)
# 4. Export for outreach campaign
```

### Example 2: Multi-City Campaign

Goal: Find dental clinics without chat in major cities

```bash
python main.py "dental clinics in New York"
python main.py "dental clinics in Los Angeles"
python main.py "dental clinics in Chicago"
python main.py "dental clinics in Houston"
python main.py "dental clinics in Phoenix"
```

Then combine all CSVs for a master lead list.

### Example 3: Niche Targeting

Goal: Find high-end service businesses

```bash
python main.py "boutique hotels in Miami"
python main.py "luxury spa in Miami"
python main.py "private practice doctors Miami"
python main.py "high end restaurants Miami"
```

These typically have higher budgets for tools like chat widgets.

## Analyzing Results

### In Excel/Google Sheets

1. Open the CSV file
2. Sort by "Priority" column (High → Low)
3. Filter by "Business Type" for industry-specific lists
4. Use "Missing Features" to segment by need
5. Create pivot tables for analysis

### Key Metrics to Track

- **Conversion Rate**: % of searched sites that become leads
- **Average Missing Features**: How many features per lead
- **High Priority %**: What % are high priority
- **Industry Breakdown**: Which industries have most opportunities

### Sample Analysis

```
Total Sites Analyzed: 50
Leads Found: 32 (64% conversion)

By Priority:
- High: 12 (38%)
- Medium: 15 (47%)
- Low: 5 (15%)

Missing Features:
- Live Chat: 30 sites (94%)
- WhatsApp: 25 sites (78%)
- Call Button: 10 sites (31%)

Top Industries:
- Restaurants: 12
- Healthcare: 8
- Legal: 7
- Retail: 5
```

## Automation Ideas

### Scheduled Searches (Linux/Mac)

Use cron to run searches automatically:

```bash
# Edit crontab
crontab -e

# Run every Monday at 9am
0 9 * * 1 cd /path/to/websitesearch && python main.py "restaurants in New York"

# Run daily at different times for different industries
0 9 * * * cd /path/to/websitesearch && python main.py "law firms in Texas"
0 10 * * * cd /path/to/websitesearch && python main.py "dental clinics in California"
```

### Scheduled Searches (Windows)

Use Task Scheduler:

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily/Weekly
4. Action: Start a program
5. Program: `C:\Python39\python.exe`
6. Arguments: `main.py "your search query"`
7. Start in: `C:\path\to\websitesearch`

## Troubleshooting

### No Leads Found

Possible reasons:
- Search query too broad
- All sites already have chat support
- Industry with high chat adoption

Try:
- Different industry/location
- More specific queries
- Increase MAX_SEARCH_RESULTS

### Too Many Errors

Check `websitesearch.log` for details.

Common causes:
- Slow/broken websites
- Too aggressive timeout settings
- Network issues

Solutions:
- Increase PAGE_LOAD_TIMEOUT
- Use better proxies/ScraperAPI
- Check internet connection

### Rate Limits Hit

Symptoms:
- "Rate limit exceeded" errors
- 429 status codes

Solutions:
- Increase delays in .env
- Reduce MAX_SEARCH_RESULTS
- Wait and try again later
- Check API quotas

## Tips & Tricks

### 1. Save API Costs

- Use `SCREENSHOT_ENABLED=false` if you don't need screenshots
- Reduce MAX_SEARCH_RESULTS for initial testing
- Use Anthropic (cheaper) instead of OpenAI for analysis

### 2. Improve Lead Quality

- Target specific geographic areas
- Focus on industries you understand
- Filter results by Priority in CSV
- Only export High priority leads

### 3. Scale Up

- Run multiple searches in sequence
- Use different API keys to avoid rate limits
- Set up automated scheduled runs
- Export to CRM automatically

### 4. Verify Leads

Before outreach:
- Visit the website manually
- Confirm they don't have chat
- Check if business is active
- Verify contact information

## Next Steps

Once you have leads:

1. **Qualify**: Review CSV, keep high-priority leads
2. **Research**: Visit websites, understand business
3. **Personalize**: Use AI recommendations for custom messages
4. **Outreach**: Email/call with value proposition
5. **Follow up**: Track responses, iterate

---

Happy lead hunting! 🎯
