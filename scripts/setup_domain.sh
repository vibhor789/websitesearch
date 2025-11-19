#!/bin/bash
# Domain and SSL Setup Script

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_success() { echo -e "${GREEN}✓ $1${NC}"; }
print_error() { echo -e "${RED}✗ $1${NC}"; }
print_info() { echo -e "${YELLOW}→ $1${NC}"; }

echo "============================================"
echo "Domain & SSL Configuration"
echo "============================================"
echo ""

# Get domain from user
print_info "What is your domain name?"
read -p "Domain (e.g., leadfinder.com): " DOMAIN

if [ -z "$DOMAIN" ]; then
    print_error "Domain name is required!"
    exit 1
fi

print_info "Setting up domain: $DOMAIN"
echo ""

# ============================================
# 1. CREATE NGINX CONFIGURATION
# ============================================
print_info "Creating Nginx configuration..."

cat > /etc/nginx/sites-available/leadfinder <<EOF
server {
    listen 80;
    server_name ${DOMAIN} www.${DOMAIN};

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Increase timeouts for long searches
    proxy_connect_timeout 300;
    proxy_send_timeout 300;
    proxy_read_timeout 300;
    send_timeout 300;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        # WebSocket support (if needed later)
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location /static {
        alias /var/www/leadfinder/webapp/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Increase body size for file uploads
    client_max_body_size 10M;
}
EOF

print_success "Nginx config created"

# ============================================
# 2. ENABLE SITE
# ============================================
print_info "Enabling site..."

# Remove default site
rm -f /etc/nginx/sites-enabled/default

# Enable leadfinder site
ln -sf /etc/nginx/sites-available/leadfinder /etc/nginx/sites-enabled/

# Test configuration
if nginx -t; then
    print_success "Nginx configuration valid"
else
    print_error "Nginx configuration invalid!"
    exit 1
fi

# Reload Nginx
systemctl reload nginx
print_success "Nginx reloaded"
echo ""

# ============================================
# 3. CHECK DNS
# ============================================
print_info "Checking DNS configuration..."
echo ""
print_info "Please make sure your domain DNS has an A record pointing to:"
print_info "$(curl -s ifconfig.me)"
echo ""
read -p "Have you configured DNS? (yes/no): " DNS_CONFIGURED

if [ "$DNS_CONFIGURED" != "yes" ]; then
    echo ""
    print_info "Please configure your DNS first:"
    echo "1. Go to your domain registrar"
    echo "2. Add A record:"
    echo "   - Type: A"
    echo "   - Name: @ (or your subdomain)"
    echo "   - Value: $(curl -s ifconfig.me)"
    echo "   - TTL: 3600"
    echo "3. Wait 5-30 minutes for DNS to propagate"
    echo "4. Run this script again"
    echo ""
    exit 0
fi

# ============================================
# 4. INSTALL SSL CERTIFICATE
# ============================================
print_info "Installing SSL certificate..."
echo ""

read -p "Enter your email for SSL notifications: " EMAIL

if [ -z "$EMAIL" ]; then
    print_error "Email is required for SSL certificate!"
    exit 1
fi

# Get certificate
certbot --nginx -d ${DOMAIN} -d www.${DOMAIN} --non-interactive --agree-tos --email ${EMAIL}

if [ $? -eq 0 ]; then
    print_success "SSL certificate installed!"
else
    print_error "SSL installation failed. Check DNS and try again."
    exit 1
fi

# ============================================
# 5. SET UP AUTO-RENEWAL
# ============================================
print_info "Setting up SSL auto-renewal..."

# Test renewal
certbot renew --dry-run

if [ $? -eq 0 ]; then
    print_success "SSL auto-renewal configured"
else
    print_error "SSL auto-renewal test failed"
fi

# ============================================
# DONE!
# ============================================
echo ""
echo "============================================"
print_success "Domain setup complete!"
echo "============================================"
echo ""
print_success "Your site is now live at: https://${DOMAIN}"
echo ""
print_info "Test your site:"
echo "curl https://${DOMAIN}"
echo ""
print_info "SSL will auto-renew every 90 days"
