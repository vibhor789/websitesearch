#!/bin/bash
# VPS Resource Health Check
# Run this to see if you have capacity for LeadFinder

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================"
echo "VPS Resource Health Check"
echo "======================================${NC}"
echo ""

# Get system info
CORES=$(nproc)
TOTAL_RAM=$(free -m | awk '/^Mem:/{print $2}')
USED_RAM=$(free -m | awk '/^Mem:/{print $3}')
RAM_PERCENT=$(free | grep Mem | awk '{printf "%.1f", $3/$2 * 100.0}')

TOTAL_DISK=$(df -h / | tail -1 | awk '{print $2}')
USED_DISK=$(df -h / | tail -1 | awk '{print $3}')
DISK_PERCENT=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')

CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')

# Display current usage
echo -e "${YELLOW}Current Resource Usage:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# CPU
echo -e "${BLUE}CPU:${NC}"
echo "  Cores: $CORES"
printf "  Usage: %.1f%%\n" "$CPU_USAGE"
if (( $(echo "$CPU_USAGE > 80" | bc -l) )); then
    echo -e "  ${RED}⚠️  HIGH CPU USAGE${NC}"
elif (( $(echo "$CPU_USAGE > 60" | bc -l) )); then
    echo -e "  ${YELLOW}⚠️  Moderate CPU usage${NC}"
else
    echo -e "  ${GREEN}✓ CPU usage is healthy${NC}"
fi
echo ""

# RAM
echo -e "${BLUE}RAM:${NC}"
echo "  Total: ${TOTAL_RAM} MB"
echo "  Used: ${USED_RAM} MB"
printf "  Usage: %.1f%%\n" "$RAM_PERCENT"
if (( $(echo "$RAM_PERCENT > 80" | bc -l) )); then
    echo -e "  ${RED}⚠️  HIGH RAM USAGE${NC}"
elif (( $(echo "$RAM_PERCENT > 60" | bc -l) )); then
    echo -e "  ${YELLOW}⚠️  Moderate RAM usage${NC}"
else
    echo -e "  ${GREEN}✓ RAM usage is healthy${NC}"
fi
echo ""

# Disk
echo -e "${BLUE}Disk:${NC}"
echo "  Total: $TOTAL_DISK"
echo "  Used: $USED_DISK"
echo "  Usage: ${DISK_PERCENT}%"
if (( $DISK_PERCENT > 80 )); then
    echo -e "  ${RED}⚠️  HIGH DISK USAGE${NC}"
elif (( $DISK_PERCENT > 60 )); then
    echo -e "  ${YELLOW}⚠️  Moderate disk usage${NC}"
else
    echo -e "  ${GREEN}✓ Disk usage is healthy${NC}"
fi
echo ""

# Load Average
echo -e "${BLUE}Load Average:${NC}"
LOAD=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')
echo "  1 min: $LOAD (threshold: $CORES)"
if (( $(echo "$LOAD > $CORES" | bc -l) )); then
    echo -e "  ${RED}⚠️  System is overloaded${NC}"
else
    echo -e "  ${GREEN}✓ Load is healthy${NC}"
fi
echo ""

# Top processes
echo -e "${YELLOW}Top 5 Processes by RAM:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ps aux --sort=-%mem | head -6 | tail -5 | awk '{printf "  %-20s %5.1f%% RAM %5.1f%% CPU\n", $11, $4, $3}'
echo ""

# Recommendation
echo -e "${BLUE}======================================"
echo "RECOMMENDATION"
echo "======================================${NC}"
echo ""

# Calculate available resources
AVAILABLE_RAM=$(echo "$TOTAL_RAM - $USED_RAM" | bc)
AVAILABLE_RAM_PERCENT=$(echo "100 - $RAM_PERCENT" | bc)
AVAILABLE_CPU=$(echo "100 - $CPU_USAGE" | bc)

echo -e "${GREEN}Available Resources:${NC}"
echo "  RAM: ${AVAILABLE_RAM} MB (${AVAILABLE_RAM_PERCENT}%)"
printf "  CPU: %.1f%%\n" "$AVAILABLE_CPU"
echo ""

# LeadFinder requirements
LEADFINDER_RAM=2048  # 2 GB in MB
LEADFINDER_CPU=25    # 25% of one core

echo -e "${YELLOW}LeadFinder Needs (at launch):${NC}"
echo "  RAM: 2048 MB (2 GB)"
echo "  CPU: ~25% (1 core at 25%)"
echo "  Disk: 10-20 GB"
echo ""

# Decision
CAN_FIT=true

if (( $AVAILABLE_RAM < $LEADFINDER_RAM )); then
    echo -e "${RED}✗ NOT ENOUGH RAM available${NC}"
    CAN_FIT=false
fi

if (( $(echo "$RAM_PERCENT > 70" | bc -l) )); then
    echo -e "${YELLOW}⚠️  RAM usage already high - may need separate VPS${NC}"
fi

if (( $(echo "$CPU_USAGE > 70" | bc -l) )); then
    echo -e "${YELLOW}⚠️  CPU usage already high - may need separate VPS${NC}"
fi

if (( $DISK_PERCENT > 70 )); then
    echo -e "${YELLOW}⚠️  Disk usage high - monitor closely${NC}"
fi

echo ""
echo -e "${BLUE}======================================"
echo "VERDICT"
echo "======================================${NC}"
echo ""

if [ "$CAN_FIT" = true ] && (( $(echo "$RAM_PERCENT < 70" | bc -l) )) && (( $(echo "$CPU_USAGE < 70" | bc -l) )); then
    echo -e "${GREEN}✓ YOU CAN INSTALL LEADFINDER ON THIS VPS${NC}"
    echo ""
    echo "You have enough resources:"
    echo "  • Available RAM: ${AVAILABLE_RAM} MB > 2048 MB needed ✓"
    printf "  • Available CPU: %.1f%% > 25%% needed ✓\n" "$AVAILABLE_CPU"
    echo ""
    echo -e "${GREEN}RECOMMENDATION: Use this VPS, save $12/month${NC}"
    echo ""
    echo "Install with:"
    echo "  cd /var/www/leadfinder"
    echo "  bash scripts/deploy.sh"
elif [ "$CAN_FIT" = true ] && (( $(echo "$RAM_PERCENT < 80" | bc -l) )); then
    echo -e "${YELLOW}⚠️  YOU CAN INSTALL BUT SHOULD MONITOR CLOSELY${NC}"
    echo ""
    echo "Resources are tight but workable:"
    echo "  • Install LeadFinder on this VPS"
    echo "  • Monitor resource usage weekly"
    echo "  • Plan to buy separate VPS when you hit 50+ customers"
    echo ""
    echo -e "${YELLOW}RECOMMENDATION: Start here, upgrade when making $500+/month${NC}"
else
    echo -e "${RED}✗ CONSIDER BUYING SEPARATE VPS${NC}"
    echo ""
    echo "Your VPS is already heavily used:"
    echo "  • RAM usage: ${RAM_PERCENT}% (>70% is high)"
    printf "  • CPU usage: %.1f%% (>70%% is high)\n" "$CPU_USAGE"
    echo ""
    echo -e "${YELLOW}RECOMMENDATION: Buy separate KVM 2 for $12/month${NC}"
    echo "  • Dedicated resources"
    echo "  • Better performance"
    echo "  • Isolated environment"
fi

echo ""
echo -e "${BLUE}======================================"
echo "MONITORING"
echo "======================================${NC}"
echo ""
echo "Run this script weekly to monitor:"
echo "  bash check_resources.sh"
echo ""
echo "Watch for:"
echo "  • RAM > 75%"
echo "  • CPU > 80%"
echo "  • Disk > 80%"
echo ""
echo "When you see these, consider separate VPS!"
