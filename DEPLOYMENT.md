# 🏭 Steel Manufacturing System Deployment Guide

## 🚀 Deployment Options

This guide covers multiple deployment options for the Steel Manufacturing Plant Management System.

---

## 1. 🌟 Streamlit Cloud (Recommended)

### Prerequisites
- GitHub repository (public or private)
- Streamlit Cloud account

### Steps
1. **Push to GitHub** (completed ✅)
2. **Connect to Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "Deploy an app"
   - Select your repository: `steel-manufacturing-system`
   - Set main file path: `app.py`
   - Click "Deploy"

### Environment Variables (Optional)
```env
ORACLE_HOST=your_oracle_host
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=your_service
ORACLE_USER=your_user
ORACLE_PASSWORD=your_password
```

### Notes
- ✅ Automatically handles Python dependencies
- ✅ Free SSL certificate
- ✅ Auto-deploys on git push
- ✅ Scales automatically

---

## 2. 🐋 Docker Deployment

### Dockerfile (included in project)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run
```bash
# Build image
docker build -t steel-manufacturing-system .

# Run container
docker run -p 8501:8501 steel-manufacturing-system
```

### Docker Compose (for production)
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - ORACLE_HOST=${ORACLE_HOST}
      - ORACLE_USER=${ORACLE_USER}
      - ORACLE_PASSWORD=${ORACLE_PASSWORD}
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

---

## 3. 🚂 Railway Deployment

### Prerequisites
- GitHub repository
- Railway account

### Steps
1. **Connect Repository**:
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select `steel-manufacturing-system`

2. **Configure Settings**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

3. **Environment Variables**:
   ```env
   PORT=8501
   ORACLE_HOST=your_host
   ORACLE_USER=your_user
   ORACLE_PASSWORD=your_password
   ```

### Notes
- ✅ $5/month for hobby tier
- ✅ Custom domains available
- ✅ Automatic HTTPS
- ✅ Git-based deployments

---

## 4. ☁️ Heroku Deployment

### Prerequisites
- GitHub repository
- Heroku account
- Heroku CLI

### Required Files (included)
- `Procfile`
- `requirements.txt`
- `runtime.txt`

### Steps
```bash
# Install Heroku CLI and login
heroku login

# Create Heroku app
heroku create steel-manufacturing-app

# Configure environment
heroku config:set ORACLE_HOST=your_host
heroku config:set ORACLE_USER=your_user  
heroku config:set ORACLE_PASSWORD=your_password

# Deploy
git push heroku main
```

### Notes
- ✅ Free tier available (with limitations)
- ✅ Add-ons for databases
- ✅ Easy scaling

---

## 5. 🌐 Vercel Deployment

### Prerequisites
- GitHub repository
- Vercel account

### Steps
1. **Connect Repository**:
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Configure build settings:
     - Build Command: `pip install -r requirements.txt`
     - Output Directory: `./`

2. **Environment Variables**:
   Add in Vercel dashboard or via CLI

### Notes
- ✅ Excellent for frontend (Next.js part)
- ⚠️ Serverless functions for Python (limitations)
- ✅ Global CDN

---

## 6. 🖥️ VPS/Cloud Server Deployment

### Prerequisites
- Linux server (Ubuntu/CentOS)
- SSH access
- Domain name (optional)

### Setup Script
```bash
#!/bin/bash
# Server setup script

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Clone repository
git clone https://github.com/yourusername/steel-manufacturing-system.git
cd steel-manufacturing-system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python scripts/init_db.py

# Install and configure Nginx (optional)
sudo apt install nginx -y

# Install PM2 for process management
npm install -g pm2

# Start application with PM2
pm2 start "streamlit run app.py --server.port 8501" --name steel-manufacturing

# Configure PM2 startup
pm2 startup
pm2 save
```

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 🔧 Production Configuration

### Environment Variables
Create `.env` file for local development:
```env
# Database Configuration
ORACLE_HOST=your_oracle_host
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=ORCL
ORACLE_USER=steel_admin
ORACLE_PASSWORD=secure_password

# Security
SECRET_KEY=your_secret_key_here
DEBUG_MODE=false

# Application
APP_NAME=Steel Manufacturing System
APP_VERSION=1.0.0
```

### Security Checklist
- [ ] Change default passwords
- [ ] Set up HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Set up database backups
- [ ] Configure monitoring
- [ ] Set up error logging

---

## 📊 Monitoring & Analytics

### Application Monitoring
```python
# Add to app.py for production monitoring
import logging
import streamlit as st

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add performance tracking
@st.cache_data(ttl=3600)
def monitor_performance():
    # Track application metrics
    pass
```

### Health Check Endpoint
```python
# Add health check for load balancers
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }
```

---

## 🎯 Recommended Deployment

For **development/portfolio**: **Streamlit Cloud**
- Free and easy
- Perfect for showcasing

For **small business**: **Railway** 
- Affordable ($5/month)
- Professional features

For **enterprise**: **VPS/Cloud Server**
- Full control
- Custom configurations
- Enhanced security

---

## 📞 Deployment Support

If you need help with deployment:

1. 📚 Check the [troubleshooting section](README.md#troubleshooting)
2. 🐛 Create an [issue](https://github.com/yourusername/steel-manufacturing-system/issues)
3. 💬 Join our [discussions](https://github.com/yourusername/steel-manufacturing-system/discussions)

---

**Happy Deploying! 🚀**