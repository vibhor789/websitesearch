#!/bin/bash
# Deploy LeadFinder on EXISTING VPS (with other apps already running)
# This script safely installs alongside n8n and other software

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

print_success() { echo -e "${GREEN}✓ $1${NC}"; }
print_error() { echo -e "${RED}✗ $1${NC}"; }
print_info() { echo -e "${YELLOW}→ $1${NC}"; }
print_header() { echo -e "${BLUE}$1${NC}"; }

clear
echo "============================================"
print_header "LeadFinder Deployment on Existing VPS"
echo "============================================"
echo ""
print_info "This will install LeadFinder alongside your existing apps"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Please run as root: sudo bash deploy_existing_vps.sh"
    exit 1
fi

# ============================================
# 1. CHECK CURRENT RESOURCES
# ============================================
print_header "Step 1: Checking available resources..."
echo ""

TOTAL_RAM=$(free -m | awk '/^Mem:/{print $2}')
USED_RAM=$(free -m | awk '/^Mem:/{print $3}')
AVAILABLE_RAM=$(echo "$TOTAL_RAM - $USED_RAM" | bc)
RAM_PERCENT=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')

echo "  Total RAM: ${TOTAL_RAM} MB"
echo "  Used RAM: ${USED_RAM} MB"
echo "  Available: ${AVAILABLE_RAM} MB"
echo ""

if (( $AVAILABLE_RAM < 2048 )); then
    print_error "Not enough RAM available (need 2048 MB, have ${AVAILABLE_RAM} MB)"
    print_info "Consider buying a separate VPS"
    exit 1
fi

if (( $RAM_PERCENT > 75 )); then
    print_error "RAM usage is very high (${RAM_PERCENT}%)"
    read -p "Continue anyway? (yes/no): " CONTINUE
    if [ "$CONTINUE" != "yes" ]; then
        exit 1
    fi
fi

print_success "Resources check passed"
echo ""

# ============================================
# 2. ASK FOR PORT
# ============================================
print_header "Step 2: Configure port (to avoid conflicts)"
echo ""
print_info "Your other apps might be using port 5000"
print_info "LeadFinder needs its own port"
echo ""

# Check if port 5000 is in use
if netstat -tuln | grep -q ':5000 '; then
    print_info "Port 5000 is already in use (probably n8n or other app)"
    DEFAULT_PORT=5001
else
    DEFAULT_PORT=5000
fi

read -p "Which port for LeadFinder? [${DEFAULT_PORT}]: " LEADFINDER_PORT
LEADFINDER_PORT=${LEADFINDER_PORT:-$DEFAULT_PORT}

# Check if chosen port is available
if netstat -tuln | grep -q ":${LEADFINDER_PORT} "; then
    print_error "Port ${LEADFINDER_PORT} is already in use!"
    print_info "Try another port like 5002, 5003, etc."
    exit 1
fi

print_success "Will use port ${LEADFINDER_PORT}"
echo ""

# ============================================
# 3. CREATE DIRECTORY
# ============================================
print_header "Step 3: Setting up directories..."

if [ -d "/var/www/leadfinder" ]; then
    print_info "Directory /var/www/leadfinder already exists"
    read -p "Overwrite? (yes/no): " OVERWRITE
    if [ "$OVERWRITE" != "yes" ]; then
        exit 1
    fi
    rm -rf /var/www/leadfinder
fi

mkdir -p /var/www/leadfinder
mkdir -p /var/www/leadfinder/logs
cd /var/www/leadfinder

print_success "Directories created"
echo ""

# ============================================
# 4. CHECK PYTHON
# ============================================
print_header "Step 4: Checking Python..."

if ! command -v python3 &> /dev/null; then
    print_info "Installing Python..."
    apt update -qq
    apt install -y python3 python3-pip python3-venv python3-dev build-essential
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
print_success "Python ${PYTHON_VERSION} ready"
echo ""

# ============================================
# 5. DOWNLOAD CODE
# ============================================
print_header "Step 5: Downloading application code..."
echo ""

print_info "How do you want to upload the code?"
echo "  1. Git clone (recommended)"
echo "  2. I'll upload manually"
echo ""
read -p "Choose (1/2): " UPLOAD_METHOD

if [ "$UPLOAD_METHOD" = "1" ]; then
    if ! command -v git &> /dev/null; then
        print_info "Installing git..."
        apt install -y git
    fi

    read -p "Enter your GitHub repository URL: " REPO_URL
    git clone "$REPO_URL" .
    print_success "Code downloaded"
elif [ "$UPLOAD_METHOD" = "2" ]; then
    print_info "Upload your files to: /var/www/leadfinder"
    print_info "Then press Enter to continue..."
    read
else
    print_error "Invalid option"
    exit 1
fi
echo ""

# ============================================
# 6. INSTALL DEPENDENCIES
# ============================================
print_header "Step 6: Installing dependencies..."

print_info "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

print_info "Installing Python packages..."
pip install --upgrade pip -q
pip install -r requirements_web.txt -q

print_info "Installing Playwright browser..."
playwright install chromium

print_success "Dependencies installed"
echo ""

# ============================================
# 7. CONFIGURE APPLICATION
# ============================================
print_header "Step 7: Configuring application..."

if [ ! -f webapp/.env ]; then
    print_info "Creating .env file..."

    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

    cat > webapp/.env <<EOF
# Flask Settings
SECRET_KEY=${SECRET_KEY}
DATABASE_URL=sqlite:////var/www/leadfinder/webapp/websearch.db
FLASK_ENV=production

# Redis
REDIS_URL=redis://localhost:6379/0

# API Keys (users will add their own)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
SCRAPER_API_KEY=

# App Settings
USE_SCRAPER_API=true
MAX_SEARCH_RESULTS=10
SCREENSHOT_ENABLED=false
EOF

    print_success ".env file created"
else
    print_info ".env file already exists"
fi
echo ""

# ============================================
# 8. INITIALIZE DATABASE
# ============================================
print_header "Step 8: Initializing database..."

cd webapp
python3 -c "from app import db, app; app.app_context().push(); db.create_all(); print('Database initialized')"
cd ..

print_success "Database ready"
echo ""

# ============================================
# 9. SET PERMISSIONS
# ============================================
print_header "Step 9: Setting permissions..."

chown -R www-data:www-data /var/www/leadfinder
chmod -R 755 /var/www/leadfinder
chmod 644 webapp/.env 2>/dev/null || true
chmod 664 webapp/websearch.db 2>/dev/null || true

print_success "Permissions set"
echo ""

# ============================================
# 10. CREATE SYSTEMD SERVICE
# ============================================
print_header "Step 10: Creating system service..."

cat > /etc/systemd/system/leadfinder.service <<EOF
[Unit]
Description=LeadFinder Web Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/leadfinder/webapp
Environment="PATH=/var/www/leadfinder/venv/bin"
ExecStart=/var/www/leadfinder/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:${LEADFINDER_PORT} --timeout 120 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable leadfinder

print_success "Service created"
echo ""

# ============================================
# 11. START APPLICATION
# ============================================
print_header "Step 11: Starting application..."

systemctl start leadfinder
sleep 3

if systemctl is-active --quiet leadfinder; then
    print_success "Application is running on port ${LEADFINDER_PORT}!"
else
    print_error "Application failed to start"
    print_info "Check logs: journalctl -u leadfinder -n 50"
    exit 1
fi
echo ""

# ============================================
# 12. CONFIGURE NGINX
# ============================================
print_header "Step 12: Nginx configuration..."
echo ""

print_info "Do you want to configure Nginx now?"
echo "  1. Yes - set up domain/subdomain"
echo "  2. No - I'll do it manually later"
echo ""
read -p "Choose (1/2): " NGINX_CONFIG

if [ "$NGINX_CONFIG" = "1" ]; then
    read -p "Enter your domain/subdomain (e.g., leads.yourdomain.com): " DOMAIN

    cat > /etc/nginx/sites-available/leadfinder <<EOF
server {
    listen 80;
    server_name ${DOMAIN};

    location / {
        proxy_pass http://127.0.0.1:${LEADFINDER_PORT};
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        proxy_connect_timeout 300;
        proxy_send_timeout 300;
        proxy_read_timeout 300;
    }

    location /static {
        alias /var/www/leadfinder/webapp/static;
        expires 30d;
    }
}
EOF

    ln -sf /etc/nginx/sites-available/leadfinder /etc/nginx/sites-enabled/

    if nginx -t; then
        systemctl reload nginx
        print_success "Nginx configured for ${DOMAIN}"

        print_info "Install SSL certificate? (requires domain DNS to be configured)"
        read -p "Install SSL now? (yes/no): " INSTALL_SSL

        if [ "$INSTALL_SSL" = "yes" ]; then
            read -p "Enter your email: " EMAIL
            certbot --nginx -d ${DOMAIN} --non-interactive --agree-tos --email ${EMAIL}
            print_success "SSL installed!"
        fi
    else
        print_error "Nginx configuration error"
    fi
fi
echo ""

# ============================================
# DONE!
# ============================================
echo ""
echo "============================================"
print_success "Installation Complete!"
echo "============================================"
echo ""

print_info "Application Details:"
echo "  Port: ${LEADFINDER_PORT}"
echo "  Directory: /var/www/leadfinder"
echo "  Service: leadfinder.service"
echo ""

print_info "Access your app:"
if [ "$NGINX_CONFIG" = "1" ]; then
    echo "  https://${DOMAIN}"
else
    echo "  http://YOUR_IP:${LEADFINDER_PORT}"
fi
echo ""

print_info "Next steps:"
echo "  1. Add your API keys in webapp/.env"
echo "  2. Restart: systemctl restart leadfinder"
echo "  3. Test the application"
echo ""

print_info "Check status:"
echo "  systemctl status leadfinder"
echo ""

print_info "View logs:"
echo "  journalctl -u leadfinder -f"
echo ""

print_info "Monitor resources:"
echo "  bash scripts/check_resources.sh"
echo ""

print_success "Your LeadFinder SaaS is now running alongside your other apps!"
