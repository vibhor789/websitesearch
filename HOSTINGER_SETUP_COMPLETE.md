# Complete Hostinger VPS Setup Guide
# NO GOOGLE AUTHENTICATION ISSUES - GUARANTEED!

This guide will help you set up your LeadFinder SaaS on Hostinger VPS with ZERO authentication headaches.

---

## 🎯 IMPORTANT: Avoiding Google Auth Issues

Your concern about Google authentication (like in n8n) is valid. Here's how we AVOID those problems:

### ✅ What We DO (No Auth Issues):
1. **ScraperAPI** - Handles Google searches (no Google auth needed!)
2. **CSV Export** - Simple file downloads (no Google Sheets auth!)
3. **User's Own API Keys** - They manage their own OpenAI/Claude keys
4. **SQLite Database** - No external database auth

### ❌ What We DON'T Use:
1. ~~Google Sheets API~~ - This causes your reconnection issues
2. ~~Google OAuth~~ - Tokens expire every hour
3. ~~Google Search API~~ - Rate limits and auth
4. ~~Service accounts~~ - Complex and breaks often

**Result: Your app runs 24/7 without any reconnection issues!**

---

## PART 1: Buy Hostinger VPS (5 minutes)

### Step 1.1: Choose Your Plan

Go to: https://www.hostinger.com/vps-hosting

**Recommended for beginners:**
- **KVM 2** - $11.99/month
  - 2 CPU cores
  - 8 GB RAM
  - 100 GB SSD
  - Perfect for 50+ users

**Budget option:**
- **KVM 1** - $5.99/month
  - 1 CPU core
  - 4 GB RAM
  - 50 GB SSD
  - Good for testing (10-20 users)

### Step 1.2: Configure VPS

During setup:
1. **Operating System**: Select **Ubuntu 22.04 64bit**
2. **Location**: Choose closest to your target customers
   - US East (New York) - For North America
   - Europe (Amsterdam) - For Europe
   - Asia (Singapore) - For Asia
3. **Server name**: `leadfinder-prod` (or anything you like)
4. **Set root password**: Create a STRONG password and SAVE IT!

### Step 1.3: Get Your VPS Details

After purchase, you'll receive:
1. **IP Address** (e.g., 123.45.67.89)
2. **Root password** (the one you just created)
3. **SSH port**: 22 (default)

**Save these somewhere safe!**

---

## PART 2: Connect to Your VPS (5 minutes)

### For Windows Users:

#### Option A: Using Built-in SSH (Windows 10/11)

1. Press `Windows Key + R`
2. Type `cmd` and press Enter
3. In the black window, type:
   ```
   ssh root@YOUR_IP_ADDRESS
   ```
   Replace `YOUR_IP_ADDRESS` with your actual IP

4. You'll see: "Are you sure you want to continue connecting?"
   - Type `yes` and press Enter

5. Enter your root password (you won't see it typing - that's normal!)

#### Option B: Using PuTTY (if above doesn't work)

1. Download PuTTY: https://www.putty.org/
2. Open PuTTY
3. In "Host Name": Enter your IP address
4. Port: 22
5. Click "Open"
6. Login as: `root`
7. Password: (your root password)

### For Mac/Linux Users:

1. Open Terminal (Command + Space, type "terminal")
2. Type:
   ```bash
   ssh root@YOUR_IP_ADDRESS
   ```
3. Type `yes` when asked
4. Enter your password

**You're now connected to your VPS!** You'll see a command prompt like:
```
root@vps-123:~#
```

---

## PART 3: Automated Setup (10 minutes)

Now the easy part - automated setup!

### Step 3.1: Download Setup Scripts

In your VPS terminal, paste this:

```bash
cd ~
wget https://raw.githubusercontent.com/YOUR_USERNAME/websitesearch/main/scripts/vps_setup.sh
chmod +x vps_setup.sh
```

### Step 3.2: Run Setup Script

```bash
bash vps_setup.sh
```

**What this does:**
- Updates your server
- Installs Python, Nginx, Redis
- Sets up firewall
- Installs all dependencies
- Takes 5-10 minutes

**You'll see lots of text scrolling. This is normal!**

When done, you'll see:
```
✓ Base system setup complete!
```

---

## PART 4: Upload Your Code (5 minutes)

### Option A: Using Git (Recommended)

In your VPS terminal:

```bash
cd /var/www/leadfinder
git clone https://github.com/YOUR_USERNAME/websitesearch.git .
```

**Note the dot (.) at the end - it's important!**

### Option B: Using SFTP (If you prefer GUI)

1. Download **FileZilla**: https://filezilla-project.org/
2. Open FileZilla
3. Click "File" → "Site Manager"
4. Click "New Site"
5. Settings:
   - Protocol: SFTP
   - Host: Your IP address
   - Port: 22
   - Logon Type: Normal
   - User: root
   - Password: Your root password
6. Click "Connect"
7. On the right side, navigate to: `/var/www/leadfinder`
8. On the left side, find your websitesearch folder
9. Drag all files from left to right

---

## PART 5: Deploy Application (5 minutes)

### Step 5.1: Run Deployment Script

```bash
cd /var/www/leadfinder
bash scripts/deploy.sh
```

**What this does:**
- Sets up Python environment
- Installs all packages
- Creates database
- Starts the application

### Step 5.2: Configure API Keys

The script created a `.env` file. Now edit it:

```bash
nano webapp/.env
```

**Add your API keys:**

```bash
# Change these lines:
OPENAI_API_KEY=sk-your-actual-openai-key-here
SCRAPER_API_KEY=your-scraperapi-key-here
```

**How to edit:**
1. Use arrow keys to navigate
2. Type to add text
3. Press `Ctrl + X` to exit
4. Press `Y` to save
5. Press `Enter` to confirm

### Step 5.3: Restart Application

```bash
systemctl restart leadfinder
```

### Step 5.4: Check It's Running

```bash
systemctl status leadfinder
```

You should see:
```
● leadfinder.service - LeadFinder Web Application
   Active: active (running)
```

Press `Q` to exit.

**If you see errors**, show me the output and I'll help!

---

## PART 6: Set Up Your Domain (10 minutes)

### Step 6.1: Buy a Domain (if you don't have one)

**Cheap domain registrars:**
- Namecheap: https://www.namecheap.com/ (~$10/year)
- Porkbun: https://porkbun.com/ (~$8/year)
- GoDaddy: https://www.godaddy.com/ (~$12/year)

**Good domain names:**
- leadfinder.com
- businessleads.io
- chatleads.ai
- prospectai.com

### Step 6.2: Point Domain to VPS

1. Log in to your domain registrar
2. Go to DNS settings
3. Add **A Record**:
   - Type: `A`
   - Name: `@` (or leave blank)
   - Value: Your VPS IP address (e.g., 123.45.67.89)
   - TTL: `3600`

4. Add **CNAME Record** (for www):
   - Type: `CNAME`
   - Name: `www`
   - Value: Your domain (e.g., leadfinder.com)
   - TTL: `3600`

5. Click "Save"

**Wait 5-30 minutes for DNS to update**

### Step 6.3: Configure Domain on VPS

On your VPS, run:

```bash
bash /var/www/leadfinder/scripts/setup_domain.sh
```

**It will ask you:**

1. **Domain name**: Enter your domain (e.g., `leadfinder.com`)
2. **Have you configured DNS?**: Type `yes` (after waiting 5-30 min)
3. **Email**: Your email for SSL notifications

**This script:**
- Configures Nginx
- Installs FREE SSL certificate (HTTPS)
- Sets up auto-renewal

---

## PART 7: Test Your Site! (2 minutes)

### Step 7.1: Visit Your Site

Open your browser and go to:
```
https://yourdomain.com
```

**You should see the LeadFinder landing page!**

### Step 7.2: Create Your Admin Account

1. Click "Sign Up"
2. Create your account
3. Log in
4. Go to Settings
5. Add your API keys:
   - OpenAI API key
   - ScraperAPI key

### Step 7.3: Run a Test Search

1. Click "New Search"
2. Enter: `"restaurants in New York"`
3. Set to 5 websites
4. Choose your AI provider
5. Click "Start Search"

**If it works, congratulations! Your SaaS is LIVE!** 🎉

---

## PART 8: Make It Ready to Sell

### Step 8.1: Edit Landing Page

Edit the homepage to match your branding:

```bash
nano /var/www/leadfinder/webapp/templates/index.html
```

Change:
- Company name
- Tagline
- Features
- Pricing

### Step 8.2: Add Terms & Privacy

Create simple terms:

```bash
nano /var/www/leadfinder/webapp/templates/terms.html
```

Use a free generator: https://www.termsandconditionsgenerator.com/

### Step 8.3: Set Up Stripe

1. Go to: https://stripe.com
2. Create account
3. Get API keys
4. Add to your site (I can help with this)

### Step 8.4: Add Your Branding

1. Add your logo to `/var/www/leadfinder/webapp/static/`
2. Update colors in templates
3. Change "LeadFinder" to your brand name

---

## PART 9: Monitoring & Maintenance

### Check Application Logs

```bash
# View last 50 lines
journalctl -u leadfinder -n 50

# Follow logs in real-time
journalctl -u leadfinder -f
```

### Restart Services

```bash
# Restart app
systemctl restart leadfinder

# Restart nginx
systemctl restart nginx
```

### Database Backup

```bash
# Manual backup
cp /var/www/leadfinder/webapp/websearch.db /root/backups/backup-$(date +%Y%m%d).db

# Set up automatic daily backups
crontab -e
# Add this line:
0 2 * * * cp /var/www/leadfinder/webapp/websearch.db /root/backups/backup-$(date +\%Y\%m\%d).db
```

### Update Application

```bash
cd /var/www/leadfinder
git pull
source venv/bin/activate
pip install -r requirements_web.txt
systemctl restart leadfinder
```

---

## 🔥 NO GOOGLE AUTH ISSUES - HERE'S WHY

### Your n8n Problem:
- Uses Google OAuth tokens
- Tokens expire every hour
- Needs manual re-authorization
- Workflows stop when token expires
- Very frustrating!

### Our Solution:
1. **ScraperAPI for Google Search**
   - API key never expires
   - No OAuth dance
   - Works 24/7 automatically

2. **CSV Export Instead of Google Sheets**
   - No Google API authentication
   - Simple file downloads
   - Never breaks

3. **User-Managed API Keys**
   - Users add their own OpenAI/Claude keys
   - Keys stored encrypted in database
   - No token refresh needed
   - Works indefinitely

4. **SQLite Database**
   - Local file database
   - No external connections
   - Can't fail authentication

**Result: Once set up, runs FOREVER without re-authentication!**

---

## Troubleshooting

### Site Not Loading

```bash
# Check if app is running
systemctl status leadfinder

# Check nginx
systemctl status nginx

# View errors
journalctl -u leadfinder -n 50
```

### "502 Bad Gateway"

App isn't running:
```bash
systemctl restart leadfinder
systemctl status leadfinder
```

### Database Errors

```bash
cd /var/www/leadfinder/webapp
source ../venv/bin/activate
python3 -c "from app import db, app; app.app_context().push(); db.create_all()"
```

### Permission Errors

```bash
chown -R www-data:www-data /var/www/leadfinder
chmod -R 755 /var/www/leadfinder
chmod 664 /var/www/leadfinder/webapp/websearch.db
```

---

## Quick Reference Commands

```bash
# Check app status
systemctl status leadfinder

# Restart app
systemctl restart leadfinder

# View logs
journalctl -u leadfinder -f

# Edit config
nano /var/www/leadfinder/webapp/.env

# Backup database
cp /var/www/leadfinder/webapp/websearch.db ~/backup.db

# Check disk space
df -h

# Check memory usage
free -h
```

---

## Total Costs

| Item | Cost | Frequency |
|------|------|-----------|
| Hostinger VPS | $12/month | Monthly |
| Domain | $10/year | Yearly |
| SSL | FREE | - |
| ScraperAPI | FREE | 5000/month |
| OpenAI API | Pay as you go | Per use |

**Total to start: ~$12/month**

Users pay for their own API usage through your markup!

---

## Next Steps After Setup

1. ✅ VPS is running
2. ✅ App is live at your domain
3. ✅ SSL/HTTPS working
4. ☐ Add Stripe for payments
5. ☐ Customize branding
6. ☐ Get first customer!

---

**You're ready to sell!** 🚀

No Google authentication problems.
No reconnection issues.
No workflow stops.

Just reliable, 24/7 lead generation!
