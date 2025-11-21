# Deploy Enhanced Features - Quick Guide

## What's New:

✨ **Customizable Search Criteria**
- Choose what features to look for missing (chatbox, WhatsApp, call button)
- Flexible lead generation based on your pitch

✨ **Contact Information Extraction**
- Automatically extracts: Emails, Phone numbers, Contact names
- Social media links: LinkedIn, Facebook, Twitter, Instagram
- All data ready for personalized outreach

✨ **Enhanced CSV Export**
- All contact info included
- Ready for cold email campaigns

---

## Deployment Steps:

### 1. Pull Latest Code

```bash
cd /var/www/leadfinder

# Stash any local changes
git stash

# Pull new features
git pull origin claude/google-search-chatbox-finder-011CUxSyfgooJxS6g5u6dNE8

# Check files were updated
ls -la contact_scraper.py webapp/migrate_db.py
```

### 2. Update Database Schema

```bash
cd /var/www/leadfinder
source venv/bin/activate

# Run migration to add new fields
python3 webapp/migrate_db.py webapp/websearch.db
```

Expected output:
```
✓ Added missing_chatbox to search table
✓ Added missing_whatsapp to search table
✓ Added missing_call_button to search table
✓ Added emails to lead table
✓ Added phones to lead table
... (and 5 more fields)
✅ Database migration completed successfully!
```

### 3. Restart Services

```bash
# Restart web application
sudo systemctl restart leadfinder

# Restart worker
sudo systemctl restart leadfinder-worker

# Check status
sudo systemctl status leadfinder --no-pager | head -10
sudo systemctl status leadfinder-worker --no-pager | head -10
```

### 4. Test New Features

1. **Go to:** http://72.60.221.243/new-search

2. **You'll see new section:** "🎯 Search Criteria"
   - Checkboxes for: Chatbox, WhatsApp, Call Button
   - All checked by default (find businesses missing ALL three)

3. **Create a test search:**
   - Query: "dental clinics in Austin"
   - Max Results: 5
   - Uncheck "WhatsApp" if you only want to find businesses missing chatbox and call button
   - Click "Start Search"

4. **Check results:**
   - Export CSV will now include: Emails, Phones, Contact Name, Social Links
   - Perfect for personalized cold outreach!

---

## How It Works:

### Before (Old System):
- ❌ Finds businesses missing ANY support feature
- ❌ No contact information
- ❌ Can't customize what you're looking for

### After (New System):
- ✅ **Choose your criteria**: Missing chatbox? Missing WhatsApp? Missing both?
- ✅ **Gets contact info**: Emails, phones, names, social media
- ✅ **Ready for outreach**: All data in CSV for personalized emails

---

## Example Use Cases:

**Use Case 1: Pitch WhatsApp Integration**
- ✅ Check "Missing WhatsApp" only
- ❌ Uncheck "Missing Chatbox"
- ❌ Uncheck "Missing Call Button"
- **Result:** Finds businesses that HAVE chatbox/call button but NO WhatsApp

**Use Case 2: Pitch Complete Support Suite**
- ✅ Check all three (default)
- **Result:** Finds businesses missing ALL support features

**Use Case 3: Pitch Live Chat Only**
- ✅ Check "Missing Chatbox" only
- ❌ Uncheck others
- **Result:** Finds businesses that might have WhatsApp/phone but no live chat

---

## Troubleshooting:

**Migration fails:**
```bash
# Check if database is locked
sudo systemctl stop leadfinder leadfinder-worker
python3 webapp/migrate_db.py webapp/websearch.db
sudo systemctl start leadfinder leadfinder-worker
```

**CSV export error:**
- Already fixed in this update (BytesIO issue resolved)
- Just restart services after pulling code

**Contact scraping not working:**
- Check chatbox_detector imported contact_scraper
- Run: `python3 -c "from contact_scraper import ContactScraper; print('OK')"`

---

## What Gets Extracted:

### Contact Information:
- **Emails**: Up to 5 most relevant emails found
- **Phones**: Up to 3 phone numbers
- **Contact Name**: Owner/CEO name if found
- **LinkedIn**: Company LinkedIn profile
- **Facebook**: Facebook page
- **Twitter**: Twitter handle
- **Instagram**: Instagram account

### Business Analysis (existing):
- Business type
- Missing features
- Recommendations
- Priority level

---

## Need Help?

Check logs:
```bash
# Web app logs
sudo journalctl -u leadfinder -f

# Worker logs
sudo journalctl -u leadfinder-worker -f
```

All set! Your lead generation tool is now WAY more powerful! 🚀
