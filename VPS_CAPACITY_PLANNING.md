# VPS Capacity Planning - Should You Share or Buy New?

## 🎯 Quick Answer First

**RECOMMENDED: Use your existing KVM 4 for now, buy separate VPS later when you hit 50+ customers.**

**Why?**
- ✅ Save $12/month initially
- ✅ KVM 4 can easily handle 3 applications
- ✅ Easy to migrate later when needed
- ✅ Test and validate business first
- ✅ Only pay for new VPS when making money

**When to buy separate VPS:**
- You have 50+ active customers
- RAM usage consistently above 80%
- CPU usage consistently above 70%
- You're making $500+/month (can afford it!)

---

## 📊 YOUR CURRENT KVM 4 SPECS

**Hostinger KVM 4:**
- **CPU**: 4 cores
- **RAM**: 16 GB
- **Disk**: 200 GB SSD
- **Cost**: ~$20/month

**This is a POWERFUL server!**

---

## 💻 RESOURCE REQUIREMENTS BREAKDOWN

### Your Current Apps:

**n8n:**
- CPU: 0.5-1 core (idle)
- RAM: 500 MB - 2 GB
- Disk: 2-5 GB
- Network: Low

**Your Other Software:**
- Estimate: 1 core, 2-4 GB RAM

**Total Current Usage: ~2 cores, 3-6 GB RAM**

### LeadFinder Requirements:

**At Launch (1-10 customers):**
- CPU: 1 core (idle), 2 cores (during searches)
- RAM: 2-3 GB
- Disk: 10-20 GB
- Network: Moderate

**At 50 customers:**
- CPU: 2-3 cores
- RAM: 4-6 GB
- Disk: 30-50 GB

**At 100+ customers:**
- CPU: 3-4 cores (need separate VPS)
- RAM: 8-12 GB (need separate VPS)
- Disk: 50-100 GB

---

## 🔍 CHECK YOUR CURRENT USAGE

### Step 1: Connect to Your KVM 4

```bash
ssh root@YOUR_KVM4_IP
```

### Step 2: Run These Commands

#### Check CPU Usage:
```bash
# Current CPU usage
top -bn1 | grep "Cpu(s)" | awk '{print $2}' | awk -F'%' '{print $1}'

# More detailed view
htop
# Press Q to quit
```

#### Check RAM Usage:
```bash
# Simple view
free -h

# Detailed percentage
free | grep Mem | awk '{printf("%.2f%%\n", $3/$2 * 100.0)}'
```

#### Check Disk Usage:
```bash
# Disk space
df -h

# Show in percentages
df -h | grep -v tmpfs | awk '{print $5 " " $6}'
```

#### Check Running Processes:
```bash
# See what's using resources
ps aux --sort=-%mem | head -10
ps aux --sort=-%cpu | head -10
```

---

## 📊 DECISION MATRIX

### ✅ USE EXISTING KVM 4 IF:

**Current Usage:**
- CPU usage < 50% ✓
- RAM usage < 60% ✓
- Disk usage < 50% ✓
- You have < 10 GB used

**Business Stage:**
- Just launching ✓
- Testing the market ✓
- 0-20 customers ✓
- Revenue < $500/month ✓

**Benefits:**
- Save $144/year ($12/month)
- Easier management (one server)
- Plenty of resources available
- Can always migrate later

### ❌ BUY SEPARATE KVM 2 IF:

**Current Usage:**
- CPU usage > 70% consistently
- RAM usage > 75% consistently
- Disk usage > 70%
- Server feels slow

**Business Stage:**
- 50+ active customers
- Making $500+/month (can afford it)
- High search volume (1000+ searches/day)
- Need isolation for security/performance

**Benefits:**
- Dedicated resources
- Isolated environments
- Better security (separate databases)
- Easier to sell business later

---

## 🎯 MY RECOMMENDATION FOR YOU

### **Phase 1: Launch on KVM 4 (Months 1-3)**

**Why?**
- You have plenty of resources (16 GB RAM!)
- Save money while validating business
- Easy to set up
- Can run 3-4 apps easily

**Expected Usage:**
- n8n: 2 GB RAM, 1 core
- Other software: 3 GB RAM, 1 core
- LeadFinder: 3 GB RAM, 1 core
- **Total: 8 GB RAM (50%), 3 cores (75%)**

**Still have 8 GB RAM free!**

### **Phase 2: Monitor & Grow (Months 3-6)**

Once you hit:
- 20+ customers
- $200+/month revenue
- RAM usage > 70%

**Then buy separate KVM 2 for LeadFinder**

### **Phase 3: Scale (Month 6+)**

When you hit:
- 100+ customers
- $2000+/month revenue

**Upgrade LeadFinder to its own KVM 4**

---

## 🔧 RESOURCE MONITORING SCRIPT

Save this to check your server health:

```bash
#!/bin/bash
# Save as: check_resources.sh
# Run with: bash check_resources.sh

echo "======================================"
echo "VPS Resource Check"
echo "======================================"
echo ""

# CPU Usage
echo "CPU Usage:"
top -bn1 | grep "Cpu(s)" | awk '{print "  Average: " $2}'
echo ""

# RAM Usage
echo "RAM Usage:"
free -h | grep Mem | awk '{printf "  Used: %s / %s (%.1f%%)\n", $3, $2, $3/$2*100}'
echo ""

# Disk Usage
echo "Disk Usage:"
df -h / | tail -1 | awk '{printf "  Used: %s / %s (%s)\n", $3, $2, $5}'
echo ""

# Top Processes by RAM
echo "Top 5 Processes by RAM:"
ps aux --sort=-%mem | head -6 | tail -5 | awk '{printf "  %s: %.1f%% RAM\n", $11, $4}'
echo ""

# Top Processes by CPU
echo "Top 5 Processes by CPU:"
ps aux --sort=-%cpu | head -6 | tail -5 | awk '{printf "  %s: %.1f%% CPU\n", $11, $3}'
echo ""

# Load Average
echo "Load Average (should be < number of cores):"
uptime | awk -F'load average:' '{print "  " $2}'
echo ""

# Check if resources are healthy
RAM_PERCENT=$(free | grep Mem | awk '{print $3/$2 * 100.0}')
if (( $(echo "$RAM_PERCENT > 80" | bc -l) )); then
    echo "⚠️  WARNING: RAM usage above 80%!"
else
    echo "✓ RAM usage is healthy"
fi
```

**Run it:**
```bash
wget https://raw.githubusercontent.com/vibhor789/websitesearch/main/scripts/check_resources.sh
bash check_resources.sh
```

---

## 📈 SCALING PLAN

### **Stage 1: Launch (0-10 customers)**
- **VPS**: Use KVM 4
- **Cost**: $0 extra
- **Setup**: Install on KVM 4 using different port
- **Expected RAM**: 3 GB
- **Expected CPU**: 1 core

### **Stage 2: Growth (10-50 customers)**
- **VPS**: Still KVM 4
- **Cost**: $0 extra
- **Monitor**: Check resources weekly
- **Expected RAM**: 4-6 GB
- **Expected CPU**: 2 cores

### **Stage 3: Scaling (50-100 customers)**
- **VPS**: Buy separate KVM 2
- **Cost**: +$12/month
- **Revenue at this stage**: $500-2000/month
- **Why separate**: Better performance, isolation
- **Migration**: 30 minutes downtime

### **Stage 4: Established (100+ customers)**
- **VPS**: Upgrade to KVM 4 or KVM 8
- **Cost**: +$20-40/month
- **Revenue at this stage**: $5000+/month
- **Why upgrade**: Handle high volume, faster responses

---

## 🚀 HOW TO INSTALL ON EXISTING KVM 4

### Option 1: Different Port (Recommended)

**LeadFinder runs on port 5001 instead of 5000:**

1. **Install in separate directory:**
```bash
mkdir -p /var/www/leadfinder
cd /var/www/leadfinder
git clone https://github.com/vibhor789/websitesearch.git .
```

2. **Run setup:**
```bash
bash scripts/deploy.sh
```

3. **Edit service to use different port:**
```bash
nano /etc/systemd/system/leadfinder.service
```

Change this line:
```
ExecStart=/var/www/leadfinder/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5001 app:app
```

4. **Configure Nginx:**
```bash
nano /etc/nginx/sites-available/leadfinder
```

Point to port 5001:
```nginx
location / {
    proxy_pass http://127.0.0.1:5001;
    ...
}
```

### Option 2: Different Domain/Subdomain

**Use subdomain: leads.yourdomain.com**

Same setup as above, but use subdomain in Nginx config.

---

## 📊 RESOURCE CALCULATOR

### Your Current Apps:

| App | RAM | CPU | Disk |
|-----|-----|-----|------|
| n8n | 2 GB | 1 core | 5 GB |
| Other Software | 3 GB | 1 core | 10 GB |
| System | 1 GB | 0.5 core | 10 GB |
| **Subtotal** | **6 GB** | **2.5 cores** | **25 GB** |

### Adding LeadFinder:

| Customers | +RAM | +CPU | +Disk |
|-----------|------|------|-------|
| 0-10 | 2 GB | 0.5 core | 10 GB |
| 10-50 | 4 GB | 1.5 cores | 20 GB |
| 50-100 | 6 GB | 2.5 cores | 40 GB |

### Total on KVM 4:

| Customers | Total RAM | Total CPU | Total Disk | Status |
|-----------|-----------|-----------|------------|--------|
| 0-10 | 8 GB (50%) | 3 cores (75%) | 35 GB (18%) | ✅ Excellent |
| 10-50 | 10 GB (63%) | 4 cores (100%) | 45 GB (23%) | ⚠️ Getting full |
| 50-100 | 12 GB (75%) | 5 cores (125%) | 65 GB (33%) | ❌ Need separate |

**At 50 customers, CPU will be maxed out = Time for separate VPS!**

---

## 🎯 WHEN TO SPLIT

### Split When You See:

1. **Revenue**: Making $500+/month (can afford $12)
2. **Performance**: Searches taking > 5 minutes
3. **RAM**: Above 75% consistently
4. **CPU**: Above 80% for more than 1 hour
5. **Customers**: 50+ active users
6. **Complaints**: Users saying "it's slow"

### Don't Split If:

- Just launching (0-20 customers)
- Revenue < $200/month
- Current usage < 60%
- Everything runs smoothly

---

## 💡 COST ANALYSIS

### Scenario 1: Use Existing KVM 4

**Months 1-6:**
- VPS cost: $0 extra
- Lost revenue from slowness: $0 (not busy yet)
- **Total: $0**

**At 50 customers:**
- Then buy KVM 2: +$12/month
- Revenue: ~$1000/month
- **Net profit: $988/month**

### Scenario 2: Buy KVM 2 Now

**Months 1-6:**
- VPS cost: $72 ($12 × 6 months)
- Extra revenue: $0 (same performance at low usage)
- **Total: -$72 wasted**

**Verdict: Wait to buy separate VPS!**

---

## 🔍 MONITORING COMMANDS

### Daily Quick Check:
```bash
# One-line health check
echo "CPU: $(top -bn1 | grep 'Cpu(s)' | awk '{print $2}') | RAM: $(free | grep Mem | awk '{printf "%.0f%%", $3/$2*100}') | Disk: $(df -h / | tail -1 | awk '{print $5}')"
```

### Weekly Deep Check:
```bash
# Detailed resource report
bash check_resources.sh
```

### Set Up Alerts:
```bash
# Install monitoring
apt install -y htop nethogs iotop

# Check in real-time
htop  # Press F10 to quit
```

---

## 🎯 FINAL RECOMMENDATION

### **NOW (Month 1):**

✅ **Use your existing KVM 4**

**Installation:**
1. Use separate directory: `/var/www/leadfinder`
2. Use different port: 5001
3. Use subdomain: `leads.yourdomain.com`
4. Total time: 1 hour
5. Extra cost: $0

**Monitoring:**
- Run `bash check_resources.sh` weekly
- Watch for RAM > 70%
- Watch for CPU > 80%

### **LATER (When you hit 50 customers):**

✅ **Buy separate KVM 2**

**By then:**
- Revenue: $500-1000/month (can afford $12)
- VPS pays for itself in 1 day!
- Better performance for customers
- Easy migration (30 min downtime)

---

## 📝 DECISION CHECKLIST

Use existing KVM 4 if you check ✅ on most:

- [ ] Currently using < 60% RAM
- [ ] Currently using < 70% CPU
- [ ] Have < 20 customers
- [ ] Making < $500/month
- [ ] Just launching/testing
- [ ] Want to save money initially
- [ ] Easy to migrate later if needed

Buy separate KVM 2 if you check ✅ on most:

- [ ] Currently using > 75% RAM
- [ ] Currently using > 80% CPU
- [ ] Have 50+ customers
- [ ] Making $500+/month
- [ ] Experiencing performance issues
- [ ] Want complete isolation
- [ ] Planning serious scale

---

## 🚀 NEXT STEPS FOR YOU

1. **Right now - Check your usage:**
```bash
ssh root@YOUR_KVM4_IP
free -h
htop
df -h
```

2. **If you have resources (likely you do):**
   - Install LeadFinder on KVM 4
   - Use port 5001
   - Save $12/month

3. **Monitor weekly:**
   - Run resource check script
   - Watch for 70%+ usage

4. **Buy separate VPS when:**
   - 50+ customers
   - RAM > 75%
   - Making $500+/month

---

## 💰 THE MATH

**Using KVM 4 now:**
- Months 1-3: $0 extra cost
- Revenue at month 3: ~$500
- **Saved: $36**

**Buying KVM 2 at month 4:**
- When making $500+/month
- $12/month is only 2.4% of revenue
- Easy to afford!

**Buying KVM 2 now:**
- Paying $12/month while making $0-100
- **Wasted: $36-72 in first 3 months**

---

## ✅ SUMMARY

**Your KVM 4 can EASILY handle:**
- n8n
- Your other software
- LeadFinder
- 20-50 customers

**You have 16 GB RAM and 4 cores - that's plenty!**

**Start on KVM 4, buy separate VPS when you're making money!**

Smart resource management = More profit! 💰
