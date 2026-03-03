# Startup & Deployment Guide

Quick start guide for running the Steel Manufacturing System locally and deploying to production.

## Quick Start (Development)

### 1. Clone and Setup

```bash
# Clone repository
git clone <repo-url>
cd steel-manufacturing-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Database

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your database details (or leave as is for SQLite)
# ORACLE_HOST=localhost
# ORACLE_PORT=1521
# ORACLE_SERVICE_NAME=ORCL
# ORACLE_USER=steel_admin
# ORACLE_PASSWORD=your_password
```

### 3. Initialize Database

```bash
# Create tables and seed default data
python scripts/init_db.py

# Expected output:
# ✓ Tables created successfully
# ✓ Initial users created
# ✓ Database initialization complete!
```

### 4. Run Application

```bash
# Start Streamlit app
streamlit run app.py

# App will open at http://localhost:8501
```

### 5. Login

Use any of these default accounts:
- **admin** / admin123
- **manager** / manager123
- **operator** / operator123
- **quality** / quality123
- **logistics** / logistics123

## Development Workflow

### Running with Auto-Reload

```bash
streamlit run app.py --logger.level=debug
```

### Debugging

Add debug prints in code:

```python
st.write("[DEBUG] Variable value:", my_var)
```

Check Streamlit logs:
```bash
tail -f .streamlit/logs/*
```

## Database Selection

### Using SQLite (Default - for Development)

No additional setup needed. The system automatically falls back to SQLite if Oracle connection fails.

Data stored in: `manufacturing.db`

### Switching to Oracle

1. Install Oracle client libraries
2. Configure `.env` with Oracle credentials
3. Set up Oracle schema (see [ORACLE_SETUP.md](./ORACLE_SETUP.md))
4. Run `python scripts/init_db.py` to create tables

## Production Deployment

### Prerequisites

- Linux/Unix server (Ubuntu 20.04+ recommended)
- Python 3.8+
- Systemd (for service management)
- Nginx or Apache (reverse proxy)
- SSL certificate (Let's Encrypt recommended)

### Step 1: Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3.10 python3.10-venv python3-pip
sudo apt install -y nginx supervisor

# Create application directory
sudo mkdir -p /opt/steel-manufacturing
sudo chown $USER:$USER /opt/steel-manufacturing
```

### Step 2: Deploy Application

```bash
# Clone repository
cd /opt/steel-manufacturing
git clone <repo-url> .

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env with production settings
cp .env.example .env
# Edit .env with production database and settings
nano .env
```

### Step 3: Initialize Database

```bash
# Initialize database
python scripts/init_db.py

# Verify tables created
python -c "from config.database import engine; engine.connect(); print('✓ DB OK')"
```

### Step 4: Configure Supervisor

Create `/etc/supervisor/conf.d/steel-mfg.conf`:

```ini
[program:steel-mfg]
directory=/opt/steel-manufacturing
command=/opt/steel-manufacturing/venv/bin/streamlit run app.py \
    --server.port=8501 \
    --server.address=127.0.0.1 \
    --logger.level=info
autostart=true
autorestart=true
stderr_logfile=/var/log/steel-mfg/error.log
stdout_logfile=/var/log/steel-mfg/access.log
user=www-data
```

Start the service:

```bash
sudo mkdir -p /var/log/steel-mfg
sudo systemctl enable supervisor
sudo systemctl restart supervisor
sudo supervisorctl restart steel-mfg
```

### Step 5: Configure Nginx

Create `/etc/nginx/sites-available/steel-mfg`:

```nginx
upstream streamlit {
    server 127.0.0.1:8501;
}

server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL certificates (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Proxy configuration
    location / {
        proxy_pass http://streamlit;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 600s;
        proxy_send_timeout 600s;
    }

    # Static files cache
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/steel-mfg /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 6: Enable HTTPS

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot certonly --nginx -d your-domain.com

# Auto-renewal
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

### Step 7: Monitoring

Check application status:

```bash
# View logs
sudo tail -f /var/log/steel-mfg/access.log
sudo tail -f /var/log/steel-mfg/error.log

# Monitor process
ps aux | grep streamlit

# Check database connection
python -c "from config.database import engine; print(engine.url)"
```

## Docker Deployment (Optional)

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port
EXPOSE 8501

# Run
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0"]
```

Build and run:

```bash
# Build image
docker build -t steel-manufacturing .

# Run container
docker run -p 8501:8501 \
    -e ORACLE_HOST=oracle-host \
    -e ORACLE_USER=steel_admin \
    -e ORACLE_PASSWORD=password \
    steel-manufacturing
```

## Troubleshooting

### Application Won't Start

```bash
# Check Python version
python --version

# Check virtual environment
which python

# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Database Connection Issues

```bash
# Test Oracle connection
python -c "from config.database import engine; engine.connect()"

# Check .env file
cat .env

# Verify Oracle service
sqlplus steel_admin@ORCL
```

### High Memory Usage

Edit `app.py`:
```python
st.set_page_config(
    ...
    initial_sidebar_state="expanded",
    layout="wide"  # Change to "centered" for less memory
)
```

### Slow Performance

1. Optimize database queries
2. Enable query caching
3. Check Nginx cache settings
4. Monitor CPU/Memory usage

## Backup & Recovery

### Daily Backups

Create `/opt/backup-script.sh`:

```bash
#!/bin/bash

BACKUP_DIR="/backups/steel-mfg"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Backup database
python /opt/steel-manufacturing/scripts/backup_db.py \
    -o $BACKUP_DIR/db_$TIMESTAMP.dump

# Backup configuration
tar -czf $BACKUP_DIR/config_$TIMESTAMP.tar.gz \
    /opt/steel-manufacturing/.env

# Keep only last 30 days
find $BACKUP_DIR -mtime +30 -delete

echo "Backup completed: $TIMESTAMP"
```

Schedule with cron:

```bash
# Add to crontab
crontab -e

# Add line for daily 2 AM backup
0 2 * * * /opt/backup-script.sh >> /var/log/backup.log 2>&1
```

## Performance Tuning

### Streamlit Configuration

Create `.streamlit/config.toml`:

```toml
[client]
showErrorDetails = false
toolbar.visible = false

[logger]
level = "info"

[server]
maxUploadSize = 200
maxMessageSize = 200
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[cache]
maxEntries = 1000
```

### Database Connection Pool

Edit `config/database.py`:

```python
engine = create_engine(
    DATABASE_URL,
    poolclass=pool.QueuePool,
    max_overflow=20,  # Increase for high traffic
    pool_size=10,
    pool_pre_ping=True,
)
```

## Monitoring & Alerts

### Health Check Script

Create `scripts/health_check.py`:

```python
#!/usr/bin/env python
import sys
from config.database import engine

try:
    with engine.connect() as conn:
        conn.execute("SELECT 1 FROM dual")
    print("✓ System healthy")
    sys.exit(0)
except Exception as e:
    print(f"✗ System error: {e}")
    sys.exit(1)
```

Monitor with cron:

```bash
# Run every 5 minutes
*/5 * * * * python /opt/steel-manufacturing/scripts/health_check.py
```

## Updates & Maintenance

### Rolling Updates

```bash
# Stop application
sudo supervisorctl stop steel-mfg

# Pull latest code
cd /opt/steel-manufacturing
git pull origin main

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt

# Run migrations if needed
python scripts/init_db.py

# Restart
sudo supervisorctl start steel-mfg
```

## Support

For issues or questions:
1. Check logs: `/var/log/steel-mfg/`
2. Review documentation: `README.md`, `ORACLE_SETUP.md`
3. Contact support team

---

**Deployment successful! 🚀**
