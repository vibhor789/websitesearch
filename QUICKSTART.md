# Quick Start Guide - 5 Minutes to Your First Results

This is the absolute fastest way to get started, even if you've never coded before!

## Prerequisites

Just install Python 3.9+: https://www.python.org/downloads/

## 5-Minute Setup

### Step 1: Install Dependencies (2 minutes)

Open terminal/command prompt in the project folder and run:

```bash
pip install -r requirements.txt
playwright install chromium
```

This installs all the software the app needs.

### Step 2: Get OpenAI API Key (2 minutes)

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in (use Google/Microsoft account for quick signup)
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. You get $5 free credit - plenty for testing!

### Step 3: Configure (30 seconds)

```bash
# Copy example configuration
cp .env.example .env
```

Edit `.env` file (use Notepad/TextEdit/nano) and add your key:
```
OPENAI_API_KEY=sk-paste-your-key-here
```

Save the file. That's it!

### Step 4: Run! (30 seconds)

```bash
python main.py "restaurants in New York"
```

## What You'll See

The app will:
1. Search Google for "restaurants in New York"
2. Visit the top 10 websites
3. Check each for chatboxes, WhatsApp, call buttons
4. For businesses WITHOUT these features:
   - Analyze what kind of business it is
   - Identify what's missing
   - Recommend what would help them
   - Save to a CSV file

## Results

Check the `output/` folder for:
- `leads_[timestamp].csv` - All your leads in a spreadsheet
- `screenshots/` - Screenshots of each website

Open the CSV in Excel/Google Sheets to see all the details!

## Example Output

```
Domain: example-restaurant.com
Business Type: Restaurant
Missing Features: Live Chat, WhatsApp
Priority: High
Recommendation: Adding WhatsApp would help with reservations and customer inquiries
```

## Next Steps

### Try Different Searches

```bash
python main.py "dental clinics in Texas"
python main.py "law firms in California"
python main.py "plumbers in Chicago"
python main.py "yoga studios in Seattle"
```

### Find More Results

Edit `.env`:
```
MAX_SEARCH_RESULTS=20
```

### Add IP Rotation (Recommended)

To avoid getting blocked by Google:

1. Sign up for ScraperAPI: https://www.scraperapi.com/ (5,000 free requests/month!)
2. Get your API key
3. Add to `.env`:
   ```
   USE_SCRAPER_API=true
   SCRAPER_API_KEY=your-api-key-here
   ```

### Export to Google Sheets

See [SETUP.md](SETUP.md#google-sheets-setup) for instructions.

## Troubleshooting

### "Command not found: python"

Try `python3` instead:
```bash
python3 main.py "your query"
```

### "ModuleNotFoundError"

Install dependencies:
```bash
pip install -r requirements.txt
playwright install chromium
```

### "Invalid API key"

- Check you copied the entire key from OpenAI
- Make sure you saved the `.env` file
- Key should start with `sk-`

### "No results found"

- Check your internet connection
- Try a different search query
- Make sure Google isn't blocking your IP (use ScraperAPI)

## Cost

For 100 websites analyzed:
- OpenAI: ~$2-5
- ScraperAPI: Free (up to 5,000/month)

Total: **Less than a coffee!** ☕

## Tips

1. **Start small** - Try 5 results first
2. **Use ScraperAPI** - Prevents Google blocks
3. **Backup your data** - CSV files are saved automatically
4. **Check costs** - Monitor at https://platform.openai.com/usage

## Need Help?

1. Run the test script: `python test_setup.py`
2. Check `websitesearch.log` for errors
3. See [SETUP.md](SETUP.md) for detailed instructions

---

That's it! You now have a fully automated lead generation tool. 🚀

Happy searching!
