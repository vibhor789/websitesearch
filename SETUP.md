# Setup Guide - Website Search & Chatbox Finder

This guide will walk you through setting up the application, even if you've never built an app before!

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Quick Start (Simplest Method)](#quick-start)
3. [Detailed Setup](#detailed-setup)
4. [API Keys & Services](#api-keys--services)
5. [IP Rotation Setup](#ip-rotation-setup)
6. [Google Sheets Setup](#google-sheets-setup)
7. [Running the Application](#running-the-application)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

1. **Python 3.9 or higher**
   - Download from: https://www.python.org/downloads/
   - During installation, CHECK "Add Python to PATH"

2. **Git** (optional, for cloning)
   - Download from: https://git-scm.com/downloads

### Check if Python is installed:
```bash
python --version
# or
python3 --version
```

---

## Quick Start

### Simplest Method (CSV Output, No IP Rotation)

This method requires minimal setup and saves results to a CSV file:

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

2. **Create `.env` file:**
   ```bash
   cp .env.example .env
   ```

3. **Edit `.env` and add ONLY your OpenAI API key:**
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

4. **Run the app:**
   ```bash
   python main.py "restaurants in New York"
   ```

That's it! Results will be saved to `output/leads_[timestamp].csv`

---

## Detailed Setup

### Step 1: Clone or Download the Repository

```bash
# Option A: Using Git
git clone <your-repo-url>
cd websitesearch

# Option B: Download ZIP
# Download the ZIP file, extract it, and navigate to the folder in terminal
```

### Step 2: Create Virtual Environment (Recommended)

This keeps your dependencies isolated:

```bash
# Create virtual environment
python -m venv venv

# Activate it:
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers (required for website analysis)
playwright install chromium
```

This will install:
- Web automation tools (Playwright, Selenium)
- AI libraries (OpenAI, Anthropic)
- Google Sheets integration
- Utilities for IP rotation

### Step 4: Configure Environment Variables

```bash
# Copy example file
cp .env.example .env

# Edit .env with your favorite text editor
# On Windows: notepad .env
# On Mac: open -e .env
# On Linux: nano .env
```

---

## API Keys & Services

### Required: AI API (Choose ONE)

#### Option 1: OpenAI (Recommended for beginners)

1. Go to: https://platform.openai.com/
2. Sign up or log in
3. Go to "API Keys" section
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)
6. Add to `.env`:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

**Cost**: ~$0.01-0.05 per website analyzed (very cheap!)

#### Option 2: Anthropic Claude

1. Go to: https://console.anthropic.com/
2. Sign up and get API access
3. Create an API key
4. Add to `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

**Cost**: Similar to OpenAI

### Optional: Google Sheets Integration

See [Google Sheets Setup](#google-sheets-setup) section below.

---

## IP Rotation Setup

To avoid being flagged by Google, you have 3 options:

### Option 1: ScraperAPI (Recommended for Beginners)

**Easiest method** - handles everything automatically!

1. Sign up at: https://www.scraperapi.com/
2. Get 5,000 free API calls per month!
3. Copy your API key
4. Add to `.env`:
   ```
   USE_SCRAPER_API=true
   SCRAPER_API_KEY=your-api-key-here
   ```

That's it! ScraperAPI automatically rotates IPs and handles blocks.

**Pricing**: Free tier includes 5,000 requests/month

### Option 2: Manual Proxy List

If you have your own proxies:

1. Create `proxies.txt` in the project folder
2. Add one proxy per line:
   ```
   proxy1.example.com:8080
   proxy2.example.com:8080
   username:password@proxy3.example.com:8080
   ```

3. Update `.env`:
   ```
   USE_PROXY=true
   PROXY_LIST_FILE=proxies.txt
   PROXY_TYPE=http  # or socks5
   ```

**Where to get proxies:**
- https://www.webshare.io/ (Free tier available)
- https://brightdata.com/
- https://smartproxy.com/

### Option 3: No IP Rotation (Not Recommended)

For testing only! Use small numbers of searches.

Just don't enable any proxy settings in `.env`.

**Warning**: Google may temporarily block your IP if you search too much.

---

## Google Sheets Setup

### Step 1: Create Google Cloud Project

1. Go to: https://console.cloud.google.com/
2. Click "Select a Project" → "New Project"
3. Name it "Website Search App"
4. Click "Create"

### Step 2: Enable Google Sheets API

1. In Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Google Sheets API"
3. Click on it and press "Enable"
4. Also enable "Google Drive API"

### Step 3: Create Service Account

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Name: "websitesearch-bot"
4. Click "Create and Continue"
5. Role: "Editor"
6. Click "Done"

### Step 4: Create Key

1. Click on the service account you just created
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Choose "JSON"
5. Save the downloaded file as `credentials.json` in your project folder

### Step 5: Create Google Sheet & Share

1. Go to: https://sheets.google.com/
2. Create a new spreadsheet
3. Name it "Website Search Leads"
4. Copy the Sheet ID from the URL:
   ```
   https://docs.google.com/spreadsheets/d/[THIS-IS-THE-SHEET-ID]/edit
   ```
5. Click "Share" button
6. Add the service account email (found in `credentials.json` under `client_email`)
7. Give it "Editor" access

### Step 6: Update .env

```
GOOGLE_SHEETS_CREDENTIALS=credentials.json
GOOGLE_SHEET_ID=your-sheet-id-here
```

---

## Running the Application

### Basic Usage

```bash
# Run with command line argument
python main.py "restaurants in New York"

# Or run interactively
python main.py
# Then enter your search query when prompted
```

### Examples

```bash
# Find law firms without chatboxes
python main.py "law firms in California"

# Find dental clinics
python main.py "dental clinics in Texas"

# Find real estate agents
python main.py "real estate agents in Miami"

# Find SaaS companies
python main.py "B2B SaaS companies"
```

### Customizing Number of Results

Edit `.env`:
```
MAX_SEARCH_RESULTS=20  # Analyze 20 websites
```

### Output

Results are saved to:
- **Google Sheets**: If configured, automatically added to your sheet
- **CSV File**: Always saved to `output/leads_[timestamp].csv`
- **Screenshots**: Saved to `output/screenshots/` (if enabled)
- **Logs**: Saved to `websitesearch.log`

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'playwright'"

Solution:
```bash
pip install -r requirements.txt
playwright install chromium
```

### "playwright executable doesn't exist"

Solution:
```bash
playwright install chromium
```

### "API key is invalid"

Solution:
- Check your `.env` file
- Make sure you copied the entire API key
- Verify the key is active in OpenAI/Anthropic dashboard

### "Google Sheets permission denied"

Solution:
- Make sure you shared the sheet with the service account email
- Check that the service account has "Editor" access
- Verify the Sheet ID is correct in `.env`

### "Rate limit exceeded" or "Too many requests"

Solution:
- Increase delays in `.env`:
  ```
  SEARCH_DELAY_MIN=5
  SEARCH_DELAY_MAX=10
  ```
- Use ScraperAPI or proxies
- Reduce MAX_SEARCH_RESULTS

### "Timeout loading page"

Solution:
- Increase timeout in `.env`:
  ```
  PAGE_LOAD_TIMEOUT=60
  ```
- Some websites are just slow or blocking automated access
- The app will skip these and continue

### Application crashes or freezes

Solution:
- Check `websitesearch.log` for error details
- Try with a smaller number of results first
- Make sure you have stable internet connection

---

## Best Practices

### 1. Start Small
Test with 5-10 results before running large searches:
```
MAX_SEARCH_RESULTS=5
```

### 2. Use ScraperAPI
For reliability, use ScraperAPI instead of manual proxies.

### 3. Monitor Costs
- OpenAI: Check usage at https://platform.openai.com/usage
- ScraperAPI: Check dashboard at https://dashboard.scraperapi.com/

### 4. Respect Rate Limits
Don't set delays too low. Recommended minimum:
```
SEARCH_DELAY_MIN=2
SEARCH_DELAY_MAX=5
```

### 5. Backup Results
CSV files are automatically saved in `output/` folder.

---

## Need Help?

1. Check `websitesearch.log` for detailed error messages
2. Make sure all API keys are correctly set in `.env`
3. Try the Quick Start method first to verify basic functionality
4. Test with simple queries like "restaurants in New York" before complex ones

---

## Next Steps

Once everything is working:

1. **Customize searches** for your target industries
2. **Analyze results** in Google Sheets or CSV
3. **Export leads** for outreach campaigns
4. **Monitor costs** and adjust settings as needed

Happy searching! 🚀
