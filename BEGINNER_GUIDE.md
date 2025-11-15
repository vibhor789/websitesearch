# Complete Beginner's Setup Guide - Step by Step

This guide assumes you've NEVER built an app before. I'll explain every single step!

---

## 💰 COST BREAKDOWN FIRST

### Cost Per Website Analyzed

The $0.05 cost is **VARIABLE** (not fixed). Here's how it breaks down:

**What affects the cost:**
1. **Number of websites** - More websites = more cost (linear)
2. **AI usage** - Each website needs 2-3 AI calls
3. **Screenshots** - If enabled, uses AI vision (more expensive)

**Typical Costs:**

| Websites | With Screenshots | Without Screenshots |
|----------|------------------|---------------------|
| 10 sites | $0.50 - $1.00 | $0.20 - $0.40 |
| 50 sites | $2.50 - $5.00 | $1.00 - $2.00 |
| 100 sites | $5.00 - $10.00 | $2.00 - $4.00 |

**How to REDUCE costs:**
- Disable screenshots: Set `SCREENSHOT_ENABLED=false` in config → Saves ~60%
- Use Anthropic instead of OpenAI → Saves ~20-30%
- Analyze fewer websites: Set `MAX_SEARCH_RESULTS=5` → Direct reduction

**How costs can INCREASE:**
- Slow websites (timeout = more retries)
- Complex pages (more AI analysis needed)
- Screenshots enabled (uses expensive vision models)

**FREE CREDITS:**
- OpenAI: $5 free when you sign up → ~100 websites analyzed FREE
- ScraperAPI: 5,000 free requests/month → Covers IP rotation for FREE
- Total: Your first 100 websites could be COMPLETELY FREE!

---

## PART 1: INSTALL PYTHON (10 minutes)

### Step 1.1: Download Python

**What is Python?** It's the programming language the app is written in. You need it installed to run the app.

1. Open your web browser
2. Go to: https://www.python.org/downloads/
3. Click the big yellow "Download Python 3.x.x" button
4. Wait for download to complete (about 30 MB)

### Step 1.2: Install Python

**Windows:**
1. Find the downloaded file (usually in Downloads folder)
2. Double-click the installer
3. **IMPORTANT:** Check the box "Add Python to PATH" at the bottom
4. Click "Install Now"
5. Wait 2-3 minutes for installation
6. Click "Close" when done

**Mac:**
1. Find the downloaded .pkg file
2. Double-click to open
3. Click "Continue" through all screens
4. Click "Install"
5. Enter your Mac password if asked
6. Click "Close" when done

**Linux:**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### Step 1.3: Verify Python is Installed

**What this does:** Confirms Python installed correctly

1. Open Terminal/Command Prompt:
   - **Windows:** Press Windows Key + R, type `cmd`, press Enter
   - **Mac:** Press Command + Space, type `terminal`, press Enter
   - **Linux:** Press Ctrl + Alt + T

2. Type this command and press Enter:
   ```bash
   python --version
   ```

3. **Expected result:** You should see something like `Python 3.11.5`
   - If you see "command not found" or "not recognized", try: `python3 --version`
   - If still doesn't work, reinstall Python and CHECK the "Add to PATH" box

---

## PART 2: DOWNLOAD THE APP (5 minutes)

### Step 2.1: Get the Code

**What this does:** Downloads all the app files to your computer

**Option A: Using Git (if you have it)**
```bash
git clone <your-repo-url>
cd websitesearch
```

**Option B: Download ZIP (easier for beginners)**
1. Go to your GitHub repository page in browser
2. Click the green "Code" button
3. Click "Download ZIP"
4. Find the ZIP file in Downloads
5. Right-click → "Extract All"
6. Choose where to extract (like Desktop or Documents)
7. Remember this location!

### Step 2.2: Open the Folder

1. Open the extracted folder
2. You should see files like:
   - `main.py`
   - `requirements.txt`
   - `README.md`
   - And others

### Step 2.3: Open Terminal in This Folder

**Windows:**
1. Hold Shift + Right-click in the folder
2. Click "Open PowerShell window here" or "Open Command Prompt here"

**Mac:**
1. Open Terminal (Command + Space, type "terminal")
2. Type `cd ` (with a space after cd)
3. Drag the websitesearch folder into the Terminal window
4. Press Enter

**Linux:**
1. Right-click in the folder
2. Click "Open Terminal Here"

**Verify you're in the right place:**
Type:
```bash
ls
```
or on Windows:
```bash
dir
```

You should see the files listed above.

---

## PART 3: INSTALL APP DEPENDENCIES (10 minutes)

### Step 3.1: Install Python Packages

**What this does:** Installs all the software libraries the app needs to run

In the terminal (in your websitesearch folder), type:

```bash
pip install -r requirements.txt
```

or if that doesn't work:
```bash
pip3 install -r requirements.txt
```

**What happens:**
- You'll see lots of text scrolling
- "Collecting...", "Downloading...", "Installing..."
- Takes 2-5 minutes
- **This is normal!**

**If you see errors:**
- Try: `python -m pip install -r requirements.txt`
- Or: `python3 -m pip install -r requirements.txt`

### Step 3.2: Install Playwright Browser

**What this does:** Installs a special browser the app uses to visit websites

Type:
```bash
playwright install chromium
```

**What happens:**
- Downloads Chromium browser (~150 MB)
- Takes 2-5 minutes depending on internet speed
- You'll see a progress bar

**Expected result:** Should say "Chromium... downloaded"

---

## PART 4: GET API KEYS (15 minutes)

API keys are like passwords that let your app use AI services.

### Step 4.1: Get OpenAI API Key

**What is this?** OpenAI provides the AI that analyzes websites and businesses.

1. **Go to:** https://platform.openai.com/signup
2. **Sign up:**
   - Click "Sign up"
   - Use Google/Microsoft account (easiest)
   - Or enter email and create password
   - Verify your email

3. **Add phone number:**
   - Click your profile icon (top right)
   - Go to "Settings"
   - Add your phone number
   - Verify with code they send

4. **Get FREE credits:**
   - New accounts get $5 FREE credit
   - Enough for ~100 websites!

5. **Create API key:**
   - Go to: https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Name it: "websitesearch" (or anything you like)
   - **IMPORTANT:** Copy the key NOW (starts with `sk-...`)
   - You can't see it again!
   - Save it in a text file temporarily

6. **Monitor usage:**
   - Check usage at: https://platform.openai.com/usage
   - See how much you've spent
   - Set spending limits if you want

### Step 4.2: Get ScraperAPI Key (OPTIONAL but RECOMMENDED)

**What is this?** Prevents Google from blocking your IP address.

1. **Go to:** https://www.scraperapi.com/signup
2. **Sign up:**
   - Enter email and password
   - Or use Google sign-in
   - Verify email

3. **Get FREE tier:**
   - Free plan: 5,000 requests/month
   - No credit card needed!
   - Enough for ~500 websites per month

4. **Get API key:**
   - After signup, you're on dashboard
   - Your API key is shown at the top
   - Copy it (save in text file)

5. **Monitor usage:**
   - Dashboard shows requests used
   - Resets monthly

**Do I need this?**
- Without it: Google may block you after 20-30 searches
- With it: Can search thousands of times safely
- **Recommendation:** Get it (it's FREE and takes 2 minutes)

---

## PART 5: CONFIGURE THE APP (5 minutes)

### Step 5.1: Create Configuration File

**What this does:** Creates a file where you'll put your API keys

In terminal (in websitesearch folder):

**Mac/Linux:**
```bash
cp .env.example .env
```

**Windows Command Prompt:**
```bash
copy .env.example .env
```

**Windows PowerShell:**
```bash
Copy-Item .env.example .env
```

### Step 5.2: Edit Configuration File

**What this does:** Adds your API keys to the app

1. **Open the .env file:**
   - **Windows:** Right-click `.env` → Open with → Notepad
   - **Mac:** Right-click `.env` → Open With → TextEdit
   - **Linux:** `nano .env` or use any text editor

2. **Add your OpenAI API key:**

   Find this line:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   Replace with:
   ```
   OPENAI_API_KEY=sk-your-actual-key-paste-here
   ```

   (Paste the key you copied earlier)

3. **Add ScraperAPI key (if you got one):**

   Find these lines:
   ```
   USE_SCRAPER_API=false
   SCRAPER_API_KEY=your_scraper_api_key_here
   ```

   Change to:
   ```
   USE_SCRAPER_API=true
   SCRAPER_API_KEY=paste-your-scraperapi-key-here
   ```

4. **Save the file:**
   - **Windows Notepad:** File → Save (or Ctrl+S)
   - **Mac TextEdit:** File → Save (or Command+S)
   - **Nano:** Ctrl+O, Enter, Ctrl+X

**IMPORTANT:**
- Don't add quotes around the keys
- Don't add spaces
- Just paste the key directly after the `=` sign

### Step 5.3: Optional Settings

**To save money, you can add these:**

```
# Disable screenshots to save ~60% on costs
SCREENSHOT_ENABLED=false

# Analyze fewer websites
MAX_SEARCH_RESULTS=5
```

**To analyze more websites:**
```
MAX_SEARCH_RESULTS=20
```

---

## PART 6: TEST YOUR SETUP (2 minutes)

### Step 6.1: Run the Test Script

**What this does:** Checks if everything is installed correctly

In terminal:
```bash
python test_setup.py
```

or:
```bash
python3 test_setup.py
```

### Step 6.2: Interpret Results

You should see checks like:
```
✓ Python 3.11.5
✓ Playwright
✓ OpenAI
✓ Configuration
✓ Network
✓ AI API
```

**If you see ✗ (red X):**
- Read the error message
- Common fixes:
  - "API key invalid" → Check you copied the full key
  - "Module not found" → Run `pip install -r requirements.txt` again
  - "Playwright not found" → Run `playwright install chromium` again

**If all tests pass:**
🎉 You're ready to go!

---

## PART 7: RUN YOUR FIRST SEARCH (5 minutes)

### Step 7.1: Run the App

**What this does:** Searches Google and analyzes websites!

In terminal:
```bash
python main.py "restaurants in New York"
```

or:
```bash
python3 main.py "restaurants in New York"
```

**What you'll see:**
1. "Starting Website Search & Analysis"
2. "Searching Google..." (takes 5-10 seconds)
3. "Analyzing websites..." with a progress bar
4. For each website without chat support:
   - "★ NEW LEAD FOUND!"
   - Business details
5. Final summary with statistics

**This will take:** 2-5 minutes for 10 websites

### Step 7.2: Check Your Results

After it finishes, check the `output` folder:

1. **Find the output folder:**
   - Should be in your websitesearch folder
   - Look for: `output/leads_YYYYMMDD_HHMMSS.csv`

2. **Open the CSV:**
   - **Windows:** Double-click → Opens in Excel
   - **Mac:** Double-click → Opens in Numbers or Excel
   - **Linux:** Open with LibreOffice Calc

3. **What you'll see:**
   - Each row is a lead (business without chat support)
   - Columns show: domain, business type, what's missing, recommendations
   - Sort by "Priority" to see best leads first

4. **Check screenshots (if enabled):**
   - Look in: `output/screenshots/`
   - PNG images of each website

---

## PART 8: UNDERSTANDING COSTS

### Cost Example Calculation

Let's say you search "restaurants in New York" with default settings (10 results):

**API Calls Made:**
- Google search: 1 call (if using ScraperAPI: FREE)
- Per website:
  - Chatbox detection: 1 vision call (~$0.01)
  - Business analysis: 1 text call (~$0.002)
  - Total per site: ~$0.012

**10 websites with screenshots:**
- 10 × $0.012 = $0.12
- ScraperAPI: FREE (free tier)
- **Total: ~$0.12** (not $0.50!)

**10 websites WITHOUT screenshots:**
- Vision calls not needed
- Only text analysis: ~$0.002 per site
- 10 × $0.002 = $0.02
- **Total: ~$0.02** (98% cheaper!)

### Cost Varies By:

1. **Screenshots:**
   - Enabled: ~$0.01 per site
   - Disabled: ~$0.002 per site
   - **Impact: 5x cost difference**

2. **Number of results:**
   - 5 results: ~$0.06 (with screenshots)
   - 10 results: ~$0.12
   - 50 results: ~$0.60
   - **Impact: Linear scaling**

3. **How many have chatboxes:**
   - Sites WITH chatboxes: Skip analysis (free!)
   - Sites WITHOUT: Full analysis (costs money)
   - If 80% already have chatboxes → only pay for 20%

### Monitoring Costs

**Check spending:**
1. Go to: https://platform.openai.com/usage
2. See exact costs in real-time
3. Set budget limits:
   - Go to: https://platform.openai.com/account/billing/limits
   - Set monthly limit (e.g., $10)
   - Get email alerts

**Typical monthly costs:**
- Light usage (50 sites/month): $1-3
- Medium usage (200 sites/month): $5-10
- Heavy usage (1000 sites/month): $20-40

---

## TROUBLESHOOTING

### "python: command not found"

**Solution:**
- Try: `python3` instead of `python`
- Or reinstall Python with "Add to PATH" checked

### "pip: command not found"

**Solution:**
- Try: `python -m pip install -r requirements.txt`
- Or: `python3 -m pip install -r requirements.txt`

### "Permission denied"

**Mac/Linux Solution:**
```bash
sudo pip install -r requirements.txt
# Enter your password when prompted
```

### "API key is invalid"

**Solution:**
1. Open `.env` file
2. Check there are no spaces around the `=`
3. Check you copied the FULL key (starts with `sk-`)
4. Go to OpenAI dashboard and verify key is active
5. Try creating a new key

### "No results found"

**Possible causes:**
- Internet connection issue
- Google is blocking your IP (use ScraperAPI!)
- Search query too specific

**Solution:**
- Check internet connection
- Enable ScraperAPI in `.env`
- Try a broader search query

### "Rate limit exceeded"

**What this means:** You're using the API too fast

**Solution:**
1. Wait 1 minute
2. Edit `.env` and add:
   ```
   SEARCH_DELAY_MIN=5
   SEARCH_DELAY_MAX=10
   ```
3. Try again

### App crashes or freezes

**Solution:**
1. Check `websitesearch.log` file for errors
2. Try with fewer results:
   - Edit `.env`: `MAX_SEARCH_RESULTS=3`
3. Check you have stable internet
4. Some websites are just broken - app will skip and continue

---

## NEXT STEPS

### 1. Try Different Searches

```bash
python main.py "dental clinics in Texas"
python main.py "law firms in California"
python main.py "yoga studios in Seattle"
```

### 2. Customize Settings

Edit `.env` to change:
- Number of results
- Enable/disable screenshots
- Adjust delays
- Set timeouts

### 3. Export to Google Sheets (Optional)

See SETUP.md for detailed instructions on:
- Creating Google Cloud project
- Setting up Google Sheets API
- Automatic export to sheets

### 4. Analyze Your Results

In Excel/Google Sheets:
- Sort by Priority (High first)
- Filter by Business Type
- Use formulas to calculate conversion rates
- Export high-priority leads for outreach

---

## QUICK REFERENCE

### Run the app:
```bash
python main.py "your search query"
```

### Check setup:
```bash
python test_setup.py
```

### View results:
- CSV: `output/leads_[timestamp].csv`
- Screenshots: `output/screenshots/`
- Logs: `websitesearch.log`

### Check costs:
- OpenAI: https://platform.openai.com/usage
- ScraperAPI: https://dashboard.scraperapi.com/

### Stop the app:
- Press `Ctrl + C` in terminal

---

## COST SUMMARY

**Your First 100 Websites: FREE!**
- OpenAI: $5 free credit (covers 100-500 websites depending on settings)
- ScraperAPI: 5,000 free requests/month

**After Free Credits:**
- With screenshots: ~$0.01-0.015 per website
- Without screenshots: ~$0.002-0.004 per website
- 100 websites: $0.20 - $1.50 depending on settings

**Recommended for beginners:**
```
SCREENSHOT_ENABLED=false  # Saves money
MAX_SEARCH_RESULTS=10     # Good starting point
USE_SCRAPER_API=true      # Prevents IP blocks
```

With these settings: ~$0.02-0.04 per search (10 websites)

---

## YOU'RE READY! 🚀

You now have:
- ✅ Python installed
- ✅ App downloaded and configured
- ✅ API keys set up
- ✅ Everything tested
- ✅ First search completed

Start generating leads and watch your costs in the OpenAI dashboard!

**Remember:** Start small (5-10 results), verify costs, then scale up!
