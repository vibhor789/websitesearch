# Quick Start Checklist - Get Live in 1 Hour!

Follow this checklist to get your LeadFinder SaaS running on Hostinger VPS.

---

## ☐ BEFORE YOU START (5 minutes)

### Get These Ready:

- [ ] Hostinger account (sign up: https://www.hostinger.com)
- [ ] Credit card for VPS purchase (~$12/month)
- [ ] OpenAI account with $5 free credit (https://platform.openai.com)
- [ ] ScraperAPI account (FREE tier: https://www.scraperapi.com)
- [ ] Domain name (optional but recommended, ~$10/year)
- [ ] Text editor for saving passwords/keys

---

## ☐ STEP 1: Buy VPS (5 minutes)

- [ ] Go to https://www.hostinger.com/vps-hosting
- [ ] Choose **KVM 2 plan** ($11.99/month)
- [ ] Select **Ubuntu 22.04 64bit**
- [ ] Choose location closest to your customers
- [ ] Set strong root password and **SAVE IT**
- [ ] Complete purchase
- [ ] Write down your **IP ADDRESS**

**Your IP:**: ________________

---

## ☐ STEP 2: Get API Keys (10 minutes)

### OpenAI:
- [ ] Go to https://platform.openai.com/signup
- [ ] Sign up (use Google for quick signup)
- [ ] Verify your email
- [ ] Add phone number for $5 free credit
- [ ] Go to https://platform.openai.com/api-keys
- [ ] Click "Create new secret key"
- [ ] **COPY AND SAVE THE KEY** (starts with sk-)

**OpenAI Key**: sk-___________________________________

### ScraperAPI:
- [ ] Go to https://www.scraperapi.com/signup
- [ ] Sign up (FREE - no credit card needed)
- [ ] Copy your API key from dashboard

**ScraperAPI Key**: ____________________________________

---

## ☐ STEP 3: Connect to VPS (5 minutes)

### Windows:
- [ ] Press Windows + R
- [ ] Type: `cmd` and press Enter
- [ ] Type: `ssh root@YOUR_IP_ADDRESS`
- [ ] Type `yes` when asked
- [ ] Enter your root password

### Mac/Linux:
- [ ] Open Terminal
- [ ] Type: `ssh root@YOUR_IP_ADDRESS`
- [ ] Type `yes` when asked
- [ ] Enter your root password

**Connected?** You should see: `root@vps-xxx:~#`

---

## ☐ STEP 4: Run Automated Setup (10 minutes)

### Copy/paste these commands one at a time:

```bash
# Download setup script
cd ~
apt update && apt install -y wget
wget https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/websitesearch/main/scripts/vps_setup.sh
chmod +x vps_setup.sh

# Run setup
bash vps_setup.sh
```

- [ ] Wait 5-10 minutes for installation
- [ ] Should see: "✓ Base system setup complete!"

**Any errors?** Take a screenshot and ask for help.

---

## ☐ STEP 5: Upload Code (5 minutes)

### Option A: Using Git (Easier)

```bash
cd /var/www/leadfinder
git clone https://github.com/YOUR_GITHUB_USERNAME/websitesearch.git .
```

- [ ] Code downloaded successfully

### Option B: Using FileZilla

- [ ] Download FileZilla
- [ ] Connect with SFTP to your VPS IP
- [ ] Upload all files to `/var/www/leadfinder`

---

## ☐ STEP 6: Deploy Application (5 minutes)

```bash
cd /var/www/leadfinder
bash scripts/deploy.sh
```

- [ ] Wait for deployment (3-5 minutes)
- [ ] Should see: "✓ Deployment complete!"

---

## ☐ STEP 7: Add Your API Keys (3 minutes)

```bash
nano webapp/.env
```

- [ ] Find `OPENAI_API_KEY=`
- [ ] Paste your OpenAI key after the `=`
- [ ] Find `SCRAPER_API_KEY=`
- [ ] Paste your ScraperAPI key after the `=`
- [ ] Press Ctrl + X, then Y, then Enter to save

```bash
systemctl restart leadfinder
```

- [ ] App restarted

---

## ☐ STEP 8: Test Without Domain (2 minutes)

```bash
curl http://localhost:5000
```

- [ ] Should see HTML output (means app is running!)

**Check status:**
```bash
systemctl status leadfinder
```

- [ ] Should show "active (running)"

---

## ☐ STEP 9: Set Up Domain (10 minutes)

### Buy Domain (if needed):
- [ ] Go to Namecheap/Porkbun/GoDaddy
- [ ] Buy domain (~$10/year)

**Your domain**: ___________________________.com

### Point DNS:
- [ ] Log in to domain registrar
- [ ] Go to DNS settings
- [ ] Add A record:
  - Type: `A`
  - Name: `@`
  - Value: YOUR_VPS_IP
  - TTL: `3600`
- [ ] Add CNAME record:
  - Type: `CNAME`
  - Name: `www`
  - Value: your domain
- [ ] Save changes
- [ ] **Wait 10-30 minutes**

### Configure on VPS:
```bash
bash /var/www/leadfinder/scripts/setup_domain.sh
```

- [ ] Enter your domain
- [ ] Type `yes` for DNS configured
- [ ] Enter your email
- [ ] SSL certificate installed

---

## ☐ STEP 10: Visit Your Site! (1 minute)

- [ ] Open browser
- [ ] Go to: `https://yourdomain.com`
- [ ] See LeadFinder landing page! 🎉

---

## ☐ STEP 11: Create Admin Account (2 minutes)

- [ ] Click "Sign Up"
- [ ] Create your account
- [ ] Log in
- [ ] Go to Settings
- [ ] Add your API keys:
  - [ ] OpenAI API key
  - [ ] ScraperAPI key
- [ ] Save settings

---

## ☐ STEP 12: Run Test Search (3 minutes)

- [ ] Click "New Search"
- [ ] Enter: `"restaurants in Miami"`
- [ ] Set to 5 websites
- [ ] Screenshots: OFF (to save money)
- [ ] AI Provider: OpenAI
- [ ] Click "Start Search"
- [ ] Wait 2-3 minutes
- [ ] See results!

**Did it work?** ✅ Your SaaS is LIVE!

---

## ☐ STEP 13: Prepare to Sell (optional, 30 minutes)

### Customize Branding:
- [ ] Edit landing page (change "LeadFinder" to your brand)
- [ ] Add your logo
- [ ] Create Terms of Service
- [ ] Create Privacy Policy

### Set Up Payments:
- [ ] Create Stripe account
- [ ] Get Stripe API keys
- [ ] Add to your app

### First Customer:
- [ ] Find 10 prospects on LinkedIn
- [ ] Send personalized messages
- [ ] Offer free trial (5 leads)
- [ ] Close first sale!

---

## 🎯 YOUR SETUP IS COMPLETE WHEN:

- ✅ Site loads at https://yourdomain.com
- ✅ You can register and log in
- ✅ You can run a search successfully
- ✅ Results show leads without chatboxes
- ✅ You can export to CSV

---

## 💰 COSTS SUMMARY

| Item | Cost | When |
|------|------|------|
| Hostinger VPS | $12/month | Monthly |
| Domain | $10/year | Yearly |
| OpenAI API | $5 FREE credit | Pay as you go |
| ScraperAPI | FREE (5000/month) | FREE |
| SSL Certificate | FREE | Auto-renews |

**Total startup cost: $12/month**

---

## 🆘 TROUBLESHOOTING

### App not running:
```bash
systemctl status leadfinder
journalctl -u leadfinder -n 50
```

### Site not loading:
```bash
systemctl status nginx
nginx -t
```

### SSL errors:
```bash
certbot renew --dry-run
```

### Database errors:
```bash
cd /var/www/leadfinder/webapp
source ../venv/bin/activate
python3 -c "from app import db, app; app.app_context().push(); db.create_all()"
```

---

## 📞 NEED HELP?

If stuck, check:
1. `journalctl -u leadfinder -n 100` for app errors
2. `/var/log/nginx/error.log` for web server errors
3. `systemctl status leadfinder` for service status

---

## 🚀 WHAT'S NEXT?

After your site is live:

**Week 1:**
- [ ] Customize branding
- [ ] Set up Stripe
- [ ] Create marketing materials

**Week 2:**
- [ ] Find 20 potential customers on LinkedIn
- [ ] Send cold outreach messages
- [ ] Offer free trials

**Week 3:**
- [ ] Close first paying customer
- [ ] Get testimonial
- [ ] Create case study

**Week 4:**
- [ ] Scale to 5 customers
- [ ] Earning $250-500/month
- [ ] Keep growing!

---

**REMEMBER: NO GOOGLE AUTH ISSUES!**

Unlike n8n, this setup:
- ✅ Never asks for re-authentication
- ✅ Runs 24/7 without stopping
- ✅ No OAuth token expires
- ✅ No workflows breaking
- ✅ Set it and forget it!

---

**Total time: ~1 hour**
**Result: A live SaaS ready to make money!**

Let's go! 🚀💰
