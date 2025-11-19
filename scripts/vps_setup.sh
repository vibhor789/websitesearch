#!/bin/bash
# Hostinger VPS Setup Script for LeadFinder SaaS
# Run this script on your fresh Ubuntu VPS to set everything up automatically

set -e  # Exit on any error

echo "============================================"
echo "LeadFinder VPS Setup Script"
echo "============================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}→ $1${NC}"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Please run as root (use: sudo bash setup.sh)"
    exit 1
fi

print_info "Starting setup process..."
echo ""

# ============================================
# 1. UPDATE SYSTEM
# ============================================
print_info "Step 1: Updating system packages..."
apt update -y
apt upgrade -y
print_success "System updated"
echo ""

# ============================================
# 2. INSTALL PYTHON
# ============================================
print_info "Step 2: Installing Python and dependencies..."
apt install -y python3 python3-pip python3-venv python3-dev build-essential
print_success "Python installed"
echo ""

# ============================================
# 3. INSTALL NGINX
# ============================================
print_info "Step 3: Installing Nginx web server..."
apt install -y nginx
systemctl enable nginx
systemctl start nginx
print_success "Nginx installed and running"
echo ""

# ============================================
# 4. INSTALL REDIS
# ============================================
print_info "Step 4: Installing Redis for background tasks..."
apt install -y redis-server
systemctl enable redis-server
systemctl start redis-server
print_success "Redis installed and running"
echo ""

# ============================================
# 5. INSTALL PLAYWRIGHT DEPENDENCIES
# ============================================
print_info "Step 5: Installing Playwright browser dependencies..."
apt install -y \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libdbus-1-3 libxcb1 libxkbcommon0 \
    libatspi2.0-0 libx11-6 libxcomposite1 libxdamage1 \
    libxext6 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 \
    libcairo2 libasound2 libxshmfence1 fonts-liberation
print_success "Browser dependencies installed"
echo ""

# ============================================
# 6. INSTALL GIT
# ============================================
print_info "Step 6: Installing Git..."
apt install -y git
print_success "Git installed"
echo ""

# ============================================
# 7. INSTALL CERTBOT (SSL)
# ============================================
print_info "Step 7: Installing Certbot for SSL certificates..."
apt install -y certbot python3-certbot-nginx
print_success "Certbot installed"
echo ""

# ============================================
# 8. SET UP FIREWALL
# ============================================
print_info "Step 8: Configuring firewall..."
apt install -y ufw
ufw allow ssh
ufw allow 'Nginx Full'
echo "y" | ufw enable
print_success "Firewall configured"
echo ""

# ============================================
# 9. CREATE APPLICATION DIRECTORY
# ============================================
print_info "Step 9: Creating application directory..."
mkdir -p /var/www/leadfinder
mkdir -p /var/www/leadfinder/logs
mkdir -p /root/backups
print_success "Directories created"
echo ""

# ============================================
# 10. SET UP APPLICATION USER
# ============================================
print_info "Step 10: Setting permissions..."
chown -R www-data:www-data /var/www/leadfinder
print_success "Permissions set"
echo ""

# ============================================
# DONE!
# ============================================
echo ""
echo "============================================"
print_success "Base system setup complete!"
echo "============================================"
echo ""
print_info "Next steps:"
echo "1. Upload your code to /var/www/leadfinder"
echo "2. Run: bash /var/www/leadfinder/deploy.sh"
echo ""
print_info "Your VPS is ready for deployment!"
