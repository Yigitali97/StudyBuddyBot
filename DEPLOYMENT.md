# 🚀 Deployment Guide - StudyBuddy Telegram Bot

This guide covers deploying StudyBuddy bot to various platforms, with a focus on Render.com (free tier).

## 📋 Table of Contents

- [Render.com Deployment (Recommended)](#rendercom-deployment-recommended)
- [Railway Deployment](#railway-deployment)
- [VPS Deployment](#vps-deployment)
- [Docker Deployment](#docker-deployment)
- [Environment Variables](#environment-variables)
- [Database Migration](#database-migration)
- [Monitoring & Maintenance](#monitoring--maintenance)

---

## 🌐 Render.com Deployment (Recommended)

Render.com offers a free tier perfect for running Telegram bots.

### Prerequisites

- GitHub account
- Render.com account (free)
- Your bot token from @BotFather

### Step 1: Prepare Your Repository

1. **Push your code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/studybuddy-bot.git
   git push -u origin main
   ```

2. **Ensure these files are in your repo**:
   - `requirements.txt`
   - `main.py`
   - All source code
   - `.env.example` (but NOT `.env`)

### Step 2: Create a Render Account

1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Authorize Render to access your repositories

### Step 3: Create a New Web Service

1. Click **"New +"** → **"Background Worker"** (not Web Service)
   - Bot doesn't need HTTP server, so Background Worker is perfect

2. **Connect your repository**:
   - Select your GitHub repository
   - Click "Connect"

3. **Configure the service**:
   - **Name**: `studybuddy-bot`
   - **Environment**: `Python 3`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`

4. **Select plan**:
   - Choose **"Free"** tier ($0/month)
   - Note: Free tier sleeps after 15 minutes of inactivity
   - For 24/7 operation, upgrade to Starter ($7/month)

### Step 4: Set Environment Variables

In the Render dashboard:

1. Go to **"Environment"** tab
2. Click **"Add Environment Variable"**
3. Add these variables:

   | Key | Value | Description |
   |-----|-------|-------------|
   | `BOT_TOKEN` | `your_bot_token` | From @BotFather |
   | `DATABASE_URL` | `sqlite:///studybuddy.db` | SQLite for free tier |
   | `LOG_LEVEL` | `INFO` | Logging level |
   | `REMINDER_INTERVAL_MINUTES` | `60` | Reminder check interval |
   | `PYTHON_VERSION` | `3.11.0` | Python version |

4. Click **"Save Changes"**

### Step 5: Deploy

1. Click **"Create Background Worker"**
2. Render will:
   - Clone your repository
   - Install dependencies
   - Start your bot
3. Monitor the **Logs** tab to see deployment progress

### Step 6: Verify Deployment

1. Check the logs for:
   ```
   Bot started: @your_bot_username
   Starting polling...
   ```

2. Test in Telegram:
   - Send `/start` to your bot
   - Should receive welcome message

### ⚠️ Important Notes for Render Free Tier

**Limitations**:
- Service sleeps after 15 minutes of inactivity
- 750 hours/month of runtime (enough for continuous use)
- Disk storage is ephemeral (resets on restart)

**Solutions**:
- **For sleeping**: Keep bot awake with cron-job.org pinging a health endpoint
- **For storage**: Migrate to PostgreSQL (see below)

---

## 🚂 Railway Deployment

Railway is another excellent option with generous free tier.

### Quick Deploy

1. Go to [railway.app](https://railway.app)
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository
5. Add environment variables:
   - `BOT_TOKEN`
   - `DATABASE_URL`
   - `LOG_LEVEL`
6. Deploy!

Railway offers:
- $5 free credit/month
- Automatic HTTPS
- Built-in PostgreSQL
- No sleep time

---

## 💻 VPS Deployment

For full control, deploy to a VPS (DigitalOcean, Linode, AWS EC2, etc.).

### Prerequisites

- VPS with Ubuntu 20.04+ or Debian 11+
- SSH access
- Sudo privileges

### Deployment Steps

#### 1. Connect to VPS

```bash
ssh user@your-server-ip
```

#### 2. Install Python 3.11

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev -y

# Install pip
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11
```

#### 3. Create Bot User

```bash
# Create dedicated user for bot
sudo useradd -m -s /bin/bash studybuddy
sudo su - studybuddy
```

#### 4. Clone Repository

```bash
git clone https://github.com/yourusername/studybuddy-bot.git
cd studybuddy-bot
```

#### 5. Setup Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### 6. Configure Environment

```bash
cp .env.example .env
nano .env
# Add your BOT_TOKEN and other settings
```

#### 7. Create Systemd Service

Exit to root user and create service file:

```bash
exit  # Exit studybuddy user
sudo nano /etc/systemd/system/studybuddy.service
```

**Service file content**:

```ini
[Unit]
Description=StudyBuddy Telegram Bot
After=network.target

[Service]
Type=simple
User=studybuddy
WorkingDirectory=/home/studybuddy/studybuddy-bot
Environment="PATH=/home/studybuddy/studybuddy-bot/venv/bin"
ExecStart=/home/studybuddy/studybuddy-bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 8. Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable studybuddy

# Start service
sudo systemctl start studybuddy

# Check status
sudo systemctl status studybuddy
```

#### 9. View Logs

```bash
# Real-time logs
sudo journalctl -u studybuddy -f

# Last 100 lines
sudo journalctl -u studybuddy -n 100

# Today's logs
sudo journalctl -u studybuddy --since today
```

#### 10. Manage Service

```bash
# Stop bot
sudo systemctl stop studybuddy

# Restart bot
sudo systemctl restart studybuddy

# Disable autostart
sudo systemctl disable studybuddy
```

---

## 🐳 Docker Deployment

### Dockerfile

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run bot
CMD ["python", "main.py"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  bot:
    build: .
    container_name: studybuddy-bot
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./data:/app/data
    environment:
      - DATABASE_URL=sqlite:///data/studybuddy.db
```

### Deploy

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild after changes
docker-compose up -d --build
```

---

## 🗄️ Database Migration

### SQLite to PostgreSQL

When scaling beyond free tier, migrate to PostgreSQL:

#### 1. Create PostgreSQL Database

**On Render**:
1. Create new PostgreSQL database
2. Copy Internal Database URL

**On Railway**:
1. Add PostgreSQL plugin
2. Copy DATABASE_URL

#### 2. Update Environment Variable

```env
DATABASE_URL=postgresql://user:password@host:5432/database
```

#### 3. Install PostgreSQL Adapter

Add to `requirements.txt`:
```
asyncpg==0.29.0
```

#### 4. Update Database Code

In `database/db.py`, add PostgreSQL support:

```python
import os
from urllib.parse import urlparse

db_url = os.getenv("DATABASE_URL")
parsed = urlparse(db_url)

if parsed.scheme == "postgresql":
    # Use asyncpg for PostgreSQL
    import asyncpg
    # Update connection logic
else:
    # Use aiosqlite for SQLite
    import aiosqlite
```

#### 5. Redeploy

Push changes and redeploy. Database will initialize automatically.

---

## 📊 Monitoring & Maintenance

### Health Checks

Add health check endpoint (optional):

```python
# In main.py
from aiohttp import web

async def health_check(request):
    return web.Response(text="OK")

app = web.Application()
app.router.add_get('/health', health_check)
```

### Logging

**View logs on Render**:
- Go to your service
- Click "Logs" tab
- Enable "Auto-scroll"

**View logs on VPS**:
```bash
sudo journalctl -u studybuddy -f
```

### Backup Database

**SQLite**:
```bash
# Backup
cp studybuddy.db studybuddy.db.backup

# Automated daily backup
crontab -e
# Add: 0 2 * * * cp /path/to/studybuddy.db /path/to/backups/studybuddy-$(date +\%Y\%m\%d).db
```

**PostgreSQL**:
```bash
# Backup
pg_dump $DATABASE_URL > backup.sql

# Restore
psql $DATABASE_URL < backup.sql
```

### Update Bot

**On Render**:
1. Push changes to GitHub
2. Render auto-deploys (if enabled)
3. Or manually trigger deploy

**On VPS**:
```bash
sudo su - studybuddy
cd studybuddy-bot
git pull
source venv/bin/activate
pip install -r requirements.txt
exit
sudo systemctl restart studybuddy
```

---

## 🔒 Security Best Practices

1. **Never commit `.env`** file to Git
2. **Use environment variables** for all secrets
3. **Rotate bot token** periodically
4. **Update dependencies** regularly:
   ```bash
   pip list --outdated
   pip install --upgrade package_name
   ```
5. **Monitor logs** for suspicious activity
6. **Limit database access** to bot only
7. **Use HTTPS** for all API calls (built-in with Render/Railway)

---

## 🆘 Troubleshooting

### Bot Not Starting

**Check logs for**:
- Missing `BOT_TOKEN`
- Import errors
- Database connection issues

**Solutions**:
```bash
# Verify environment variables
echo $BOT_TOKEN

# Check Python version
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Database Errors

**SQLite locked**:
- Stop any other instances of the bot
- Delete `studybuddy.db` and restart (loses data)

**PostgreSQL connection timeout**:
- Check database is running
- Verify DATABASE_URL is correct
- Check firewall rules

### Reminders Not Sending

1. Check bot has been running for at least reminder interval
2. Verify system time is correct
3. Check APScheduler is running in logs
4. Test reminder manually

---

## 📈 Scaling Considerations

### Free Tier → Paid

When you outgrow free tier:

1. **Render Starter** ($7/month)
   - No sleep time
   - Better performance
   - More memory

2. **Railway Pro** ($5/month)
   - Higher limits
   - Better uptime

3. **VPS** ($5-10/month)
   - Full control
   - Unlimited usage
   - More configuration needed

### Performance Optimization

- Use PostgreSQL for better concurrency
- Implement connection pooling
- Add Redis for caching (future)
- Use CDN for media (if added)

---

## ✅ Deployment Checklist

Before going live:

- [ ] Bot token configured
- [ ] Environment variables set
- [ ] Database initialized
- [ ] Logs accessible
- [ ] `/start` command works
- [ ] `/add` task flow works
- [ ] `/list` displays tasks
- [ ] `/delete` removes tasks
- [ ] Reminders scheduled
- [ ] Error handling tested
- [ ] Backup strategy in place
- [ ] Monitoring enabled

---

**🎉 Your bot is now deployed and ready to help students!**

For questions or issues, check the logs first, then refer to the main README.md or open an issue on GitHub.