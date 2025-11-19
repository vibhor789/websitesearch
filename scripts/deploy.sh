#!/bin/bash
# Application Deployment Script
# Run this after uploading your code to /var/www/leadfinder

set -e

echo "============================================"
echo "LeadFinder Application Deployment"
echo "============================================"
echo ""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_success() { echo -e "${GREEN}✓ $1${NC}"; }
print_error() { echo -e "${RED}✗ $1${NC}"; }
print_info() { echo -e "${YELLOW}→ $1${NC}"; }

# Change to app directory
cd /var/www/leadfinder

# ============================================
# 1. SET UP PYTHON ENVIRONMENT
# ============================================
print_info "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
print_success "Virtual environment created"

# ============================================
# 2. INSTALL DEPENDENCIES
# ============================================
print_info "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements_web.txt
print_success "Dependencies installed"

# ============================================
# 3. INSTALL PLAYWRIGHT
# ============================================
print_info "Installing Playwright browser..."
playwright install chromium
print_success "Playwright installed"

# ============================================
# 4. CREATE .ENV FILE (IF NOT EXISTS)
# ============================================
if [ ! -f webapp/.env ]; then
    print_info "Creating .env file..."

    # Generate secret key
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

    cat > webapp/.env <<EOF
# Flask Settings
SECRET_KEY=${SECRET_KEY}
DATABASE_URL=sqlite:////var/www/leadfinder/webapp/websearch.db
FLASK_ENV=production

# Redis
REDIS_URL=redis://localhost:6379/0

# Default API Keys (Users will add their own in settings)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
SCRAPER_API_KEY=

# App Settings
USE_SCRAPER_API=true
MAX_SEARCH_RESULTS=10
SCREENSHOT_ENABLED=false
EOF

    print_success ".env file created"
    print_info "IMPORTANT: Edit webapp/.env and add your API keys!"
else
    print_info ".env file already exists, skipping..."
fi

# ============================================
# 5. INITIALIZE DATABASE
# ============================================
print_info "Initializing database..."
cd webapp
python3 -c "from app import db, app;
with app.app_context():
    db.create_all();
print('Database initialized')"
cd ..
print_success "Database ready"

# ============================================
# 6. SET PERMISSIONS
# ============================================
print_info "Setting file permissions..."
chown -R www-data:www-data /var/www/leadfinder
chmod -R 755 /var/www/leadfinder
chmod 644 webapp/.env
chmod 664 webapp/websearch.db 2>/dev/null || true
print_success "Permissions set"

# ============================================
# 7. CREATE SYSTEMD SERVICE
# ============================================
print_info "Creating systemd service..."

cat > /etc/systemd/system/leadfinder.service <<EOF
[Unit]
Description=LeadFinder Web Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/leadfinder/webapp
Environment="PATH=/var/www/leadfinder/venv/bin"
ExecStart=/var/www/leadfinder/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5000 --timeout 120 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable leadfinder
print_success "Service created"

# ============================================
# 8. START APPLICATION
# ============================================
print_info "Starting application..."
systemctl restart leadfinder
sleep 3

if systemctl is-active --quiet leadfinder; then
    print_success "Application is running!"
else
    print_error "Application failed to start. Check logs with: journalctl -u leadfinder -n 50"
    exit 1
fi

# ============================================
# DONE!
# ============================================
echo ""
echo "============================================"
print_success "Deployment complete!"
echo "============================================"
echo ""
print_info "Next steps:"
echo "1. Configure Nginx with your domain (run: bash scripts/setup_domain.sh)"
echo "2. Add your API keys in webapp/.env"
echo "3. Restart service: systemctl restart leadfinder"
echo ""
print_info "Check status: systemctl status leadfinder"
print_info "View logs: journalctl -u leadfinder -f"
