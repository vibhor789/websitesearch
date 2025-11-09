# Setup Checklist

Use this checklist to make sure everything is configured correctly.

## ✅ Installation

- [ ] Python 3.9+ installed (`python --version`)
- [ ] Git installed (optional)
- [ ] Project downloaded/cloned

## ✅ Python Dependencies

- [ ] Virtual environment created (optional but recommended)
  ```bash
  python -m venv venv
  source venv/bin/activate  # Mac/Linux
  venv\Scripts\activate     # Windows
  ```
- [ ] Dependencies installed
  ```bash
  pip install -r requirements.txt
  ```
- [ ] Playwright browser installed
  ```bash
  playwright install chromium
  ```

## ✅ Configuration

- [ ] `.env` file created (copy from `.env.example`)
- [ ] At least ONE AI API key configured:
  - [ ] OpenAI API key (`OPENAI_API_KEY=sk-...`) OR
  - [ ] Anthropic API key (`ANTHROPIC_API_KEY=sk-ant-...`)

## ✅ Optional Features

### IP Rotation (Highly Recommended)

- [ ] ScraperAPI account created (https://www.scraperapi.com/)
- [ ] ScraperAPI key added to `.env`
  ```
  USE_SCRAPER_API=true
  SCRAPER_API_KEY=your-key-here
  ```

OR

- [ ] Proxy list created (`proxies.txt`)
- [ ] Proxy settings configured in `.env`
  ```
  USE_PROXY=true
  PROXY_LIST_FILE=proxies.txt
  ```

### Google Sheets Export

- [ ] Google Cloud project created
- [ ] Google Sheets API enabled
- [ ] Google Drive API enabled
- [ ] Service account created
- [ ] Service account key downloaded (`credentials.json`)
- [ ] Google Sheet created and shared with service account
- [ ] Sheet ID added to `.env`
  ```
  GOOGLE_SHEET_ID=your-sheet-id
  ```

## ✅ Testing

- [ ] Run setup test
  ```bash
  python test_setup.py
  ```
- [ ] All tests pass
- [ ] Try a small test search
  ```bash
  python main.py "test search"
  ```

## ✅ Final Verification

- [ ] Search completes successfully
- [ ] Results saved to CSV (check `output/` folder)
- [ ] Screenshots captured (check `output/screenshots/`)
- [ ] No errors in `websitesearch.log`
- [ ] (Optional) Results appear in Google Sheet

## 🎉 Ready to Use!

You're all set! Try some real searches:

```bash
python main.py "restaurants in New York"
python main.py "law firms in California"
python main.py "dental clinics in Texas"
```

## 📊 Monitor Usage

- [ ] OpenAI usage dashboard: https://platform.openai.com/usage
- [ ] ScraperAPI dashboard: https://dashboard.scraperapi.com/
- [ ] Check costs regularly to avoid surprises

## 🔧 Customization

Want to customize? Edit `.env`:

- `MAX_SEARCH_RESULTS=20` - Analyze more websites
- `SEARCH_DELAY_MIN=5` - Slower but safer
- `PAGE_LOAD_TIMEOUT=60` - For slow websites
- `SCREENSHOT_ENABLED=false` - Disable screenshots to save space

## 📝 Troubleshooting

If something doesn't work:

1. [ ] Check `websitesearch.log` for errors
2. [ ] Run `python test_setup.py` again
3. [ ] Review [SETUP.md](SETUP.md#troubleshooting)
4. [ ] Verify all API keys are correct
5. [ ] Check internet connection
6. [ ] Try with smaller `MAX_SEARCH_RESULTS` (e.g., 3)

## 🚀 Next Steps

Once everything works:

- [ ] Experiment with different search queries
- [ ] Analyze your target industries
- [ ] Export leads for outreach
- [ ] Set up automated runs (cron/Task Scheduler)
- [ ] Integrate with your CRM

---

Happy searching! 🎯
