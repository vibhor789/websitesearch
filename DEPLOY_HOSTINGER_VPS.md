# Deploy to Hostinger VPS - Step by Step Guide

This guide will walk you through deploying your LeadFinder app to Hostinger VPS so you can sell it as a service.

---

## Table of Contents

1. [Buy Hostinger VPS](#1-buy-hostinger-vps)
2. [Connect to Your VPS](#2-connect-to-your-vps)
3. [Install Required Software](#3-install-required-software)
4. [Upload Your Code](#4-upload-your-code)
5. [Configure the Application](#5-configure-the-application)
6. [Set Up Domain & SSL](#6-set-up-domain--ssl)
7. [Run in Production](#7-run-in-production)
8. [Set Up Background Workers](#8-set-up-background-workers)
9. [Monitor & Maintain](#9-monitor--maintain)

---

## 1. Buy Hostinger VPS

### Step 1.1: Choose a Plan

1. Go to: https://www.hostinger.com/vps-hosting
2. Click "Get Started"
3. **Recommended plan**: KVM 2 (~$10-15/month)
   - 2 CPU cores
   - 8GB RAM
   - 100GB SSD
   - This can handle 50+ concurrent users

### Step 1.2: Configure VPS

During checkout:
- **Operating System**: Ubuntu 22.04 64bit
- **Location**: Choose closest to your customers
- **Set root password**: Remember this!

### Step 1.3: Get Your VPS Details

After purchase, you'll get:
- IP Address (e.g., 123.45.67.89)
- Root password
- SSH port (usually 22)

---

## 2. Connect to Your VPS

### Windows Users (PuTTY)

1. Download PuTTY: https://www.putty.org/
2. Open PuTTY
3. Enter IP address
4. Click "Open"
5. Login as: `root`
6. Enter your password

### Mac/Linux Users (Terminal)

```bash
ssh root@YOUR_IP_ADDRESS
# Enter your password when prompted
```

**Example:**
```bash
ssh root@123.45.67.89
```

---

## 3. Install Required Software

Once connected to VPS, run these commands:

### Step 3.1: Update System

```bash
apt update && apt upgrade -y
```

### Step 3.2: Install Python

```bash
apt install python3 python3-pip python3-venv -y
```

### Step 3.3: Install Playwright Dependencies

```bash
apt install -y libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libdbus-1-3 libxcb1 libxkbcommon0 libatspi2.0-0 libx11-6 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2
```

### Step 3.4: Install Nginx (Web Server)

```bash
apt install nginx -y
```

### Step 3.5: Install Redis (For Background Tasks)

```bash
apt install redis-server -y
systemctl enable redis-server
systemctl start redis-server
```

### Step 3.6: Install Git

```bash
apt install git -y
```

---

## 4. Upload Your Code

### Option A: Using Git (Recommended)

```bash
# Create app directory
mkdir -p /var/www/leadfinder
cd /var/www/leadfinder

# Clone your repository
git clone YOUR_GITHUB_REPO_URL .
```

### Option B: Using SFTP (Manual Upload)

1. Use FileZilla or WinSCP
2. Connect to VPS with SFTP
3. Upload all files to `/var/www/leadfinder/`

### Step 4.1: Set Up Virtual Environment

```bash
cd /var/www/leadfinder
python3 -m venv venv
source venv/bin/activate
```

### Step 4.2: Install Python Dependencies

```bash
pip install -r requirements_web.txt
```

### Step 4.3: Install Playwright Browser

```bash
playwright install chromium
```

---

## 5. Configure the Application

### Step 5.1: Create Environment File

```bash
cd /var/www/leadfinder/webapp
nano .env
```

Add these settings (press Ctrl+X, then Y to save):

```bash
# Flask Settings
SECRET_KEY=your-very-long-random-secret-key-change-this-123456789
DATABASE_URL=sqlite:////var/www/leadfinder/webapp/websearch.db
FLASK_ENV=production

# Redis
REDIS_URL=redis://localhost:6379/0

# Your API Keys (for testing - users will add their own)
OPENAI_API_KEY=sk-your-default-key
ANTHROPIC_API_KEY=
SCRAPER_API_KEY=your-scraper-api-key
```

**Generate a secure secret key:**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### Step 5.2: Initialize Database

```bash
cd /var/www/leadfinder/webapp
source ../venv/bin/activate
python3 app.py
# Press Ctrl+C after database is created
```

### Step 5.3: Set Permissions

```bash
chown -R www-data:www-data /var/www/leadfinder
chmod -R 755 /var/www/leadfinder
```

---

## 6. Set Up Domain & SSL

### Step 6.1: Point Domain to VPS

1. Go to your domain registrar (GoDaddy, Namecheap, etc.)
2. Add A record:
   - Type: A
   - Name: @ (or your subdomain)
   - Value: YOUR_VPS_IP_ADDRESS
   - TTL: 3600

Wait 5-30 minutes for DNS propagation.

### Step 6.2: Configure Nginx

```bash
nano /etc/nginx/sites-available/leadfinder
```

Paste this configuration:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_read_timeout 60s;
    }

    location /static {
        alias /var/www/leadfinder/webapp/static;
    }
}
```

Replace `yourdomain.com` with your actual domain.

### Step 6.3: Enable Site

```bash
ln -s /etc/nginx/sites-available/leadfinder /etc/nginx/sites-enabled/
nginx -t  # Test configuration
systemctl restart nginx
```

### Step 6.4: Install SSL Certificate (HTTPS)

```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Follow the prompts. Certbot will automatically configure HTTPS!

---

## 7. Run in Production

### Step 7.1: Create Systemd Service

```bash
nano /etc/systemd/system/leadfinder.service
```

Paste:

```ini
[Unit]
Description=LeadFinder Web Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/leadfinder/webapp
Environment="PATH=/var/www/leadfinder/venv/bin"
ExecStart=/var/www/leadfinder/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

### Step 7.2: Start the Service

```bash
systemctl daemon-reload
systemctl enable leadfinder
systemctl start leadfinder
```

### Step 7.3: Check Status

```bash
systemctl status leadfinder
```

Should show "active (running)"

### Step 7.4: Test Your Site

1. Open browser
2. Go to: https://yourdomain.com
3. You should see your LeadFinder landing page!

---

## 8. Set Up Background Workers

For running actual searches (heavy processing), you need background workers.

### Step 8.1: Create Celery Worker Service

```bash
nano /etc/systemd/system/leadfinder-worker.service
```

Paste:

```ini
[Unit]
Description=LeadFinder Celery Worker
After=network.target redis.service

[Service]
User=www-data
WorkingDirectory=/var/www/leadfinder/webapp
Environment="PATH=/var/www/leadfinder/venv/bin"
ExecStart=/var/www/leadfinder/venv/bin/celery -A tasks worker --loglevel=info
Restart=always

[Install]
WantedBy=multi-user.target
```

### Step 8.2: Start Worker

```bash
systemctl enable leadfinder-worker
systemctl start leadfinder-worker
```

**Note**: You'll need to create a `tasks.py` file for actual search processing. This is a separate module I can help you create.

---

## 9. Monitor & Maintain

### Check Logs

```bash
# Application logs
journalctl -u leadfinder -f

# Nginx logs
tail -f /var/log/nginx/error.log
```

### Restart Services

```bash
systemctl restart leadfinder
systemctl restart leadfinder-worker
systemctl restart nginx
```

### Update Application

```bash
cd /var/www/leadfinder
git pull
source venv/bin/activate
pip install -r requirements_web.txt
systemctl restart leadfinder
systemctl restart leadfinder-worker
```

### Database Backups

```bash
# Create backup
cp /var/www/leadfinder/webapp/websearch.db /root/backups/websearch_$(date +%Y%m%d).db

# Set up automatic backups (crontab)
crontab -e
# Add this line:
0 2 * * * cp /var/www/leadfinder/webapp/websearch.db /root/backups/websearch_$(date +\%Y\%m\%d).db
```

---

## Costs Summary

### Hostinger VPS

- **Basic (KVM 1)**: ~$6/month
  - Good for: 1-10 users
  - Can handle: ~100 searches/day

- **Standard (KVM 2)**: ~$12/month
  - Good for: 10-50 users
  - Can handle: ~500 searches/day

- **Advanced (KVM 4)**: ~$20/month
  - Good for: 50-200 users
  - Can handle: ~2000 searches/day

### Other Costs

- Domain: $10-15/year
- SSL: FREE (Let's Encrypt)
- API costs: Paid by users (you set your margin)

### Total Monthly Cost

**To run your SaaS:**
- Basic setup: ~$10/month
- With domain: ~$11/month

**Very affordable to start!**

---

## Security Checklist

- [ ] Change default SSH port
- [ ] Set up firewall (UFW)
- [ ] Use strong passwords
- [ ] Keep system updated
- [ ] Monitor for suspicious activity
- [ ] Regular backups
- [ ] SSL certificate (HTTPS)

### Basic Security Commands

```bash
# Set up firewall
ufw allow ssh
ufw allow 'Nginx Full'
ufw enable

# Update system regularly
apt update && apt upgrade -y
```

---

## Troubleshooting

### Site not loading

```bash
# Check if app is running
systemctl status leadfinder

# Check Nginx
systemctl status nginx
nginx -t

# Check logs
journalctl -u leadfinder -n 50
```

### 502 Bad Gateway

Usually means the Flask app isn't running:
```bash
systemctl restart leadfinder
```

### Permission denied errors

```bash
chown -R www-data:www-data /var/www/leadfinder
chmod -R 755 /var/www/leadfinder
```

### Database errors

```bash
cd /var/www/leadfinder/webapp
source ../venv/bin/activate
python3 -c "from app import db, create_tables; create_tables()"
```

---

## Next Steps After Deployment

1. ✅ VPS is running
2. ✅ App is accessible at yourdomain.com
3. ✅ SSL is configured (HTTPS)
4. ☐ Set up payment processing (Stripe)
5. ☐ Add terms of service & privacy policy
6. ☐ Set up email notifications
7. ☐ Monitor usage and costs
8. ☐ Start marketing!

---

## Need Help?

- Hostinger has 24/7 support chat
- Check `/var/log/` for error logs
- Test locally before deploying changes

---

**Congratulations!** Your LeadFinder SaaS is now live! 🚀

Users can:
1. Register accounts
2. Add their API keys
3. Run searches
4. Export leads
5. Pay you for the service!
