# 🌐 Render Deployment Guide

## 🚀 Deploy Steel Manufacturing System on Render

This guide will help you deploy your Steel Manufacturing Plant Management System on Render.

### ✅ Prerequisites
- GitHub account with your code repository
- Render account (free tier available)

### 📋 Pre-deployment Checklist
- ✅ `requirements.txt` is present
- ✅ `Procfile` is configured  
- ✅ `runtime.txt` specifies Python version
- ✅ `render.yaml` is created
- ✅ Code is pushed to GitHub

---

## 🎯 Step-by-Step Deployment

### 1. **Prepare Your Repository**
Make sure your code is pushed to a GitHub repository:
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. **Connect to Render**
1. Go to [render.com](https://render.com)
2. Sign in with your GitHub account
3. Click **"New +"** → **"Web Service"**

### 3. **Configure the Service**
1. **Connect Repository**: Select your GitHub repository
2. **Name**: `steel-manufacturing-system` (or your preferred name)
3. **Region**: Choose your preferred region
4. **Branch**: `main` (or your default branch)
5. **Root Directory**: Leave blank (unless your app is in a subdirectory)

### 4. **Build & Deploy Settings**
```
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
```

### 5. **Environment Variables (Optional)**
If you want to use Oracle database, add these environment variables:
```
ORACLE_HOST=your_oracle_host
ORACLE_PORT=1521  
ORACLE_SERVICE_NAME=your_service_name
ORACLE_USER=your_username
ORACLE_PASSWORD=your_password
```

*Note: The app will automatically fallback to SQLite if Oracle is not available.*

### 6. **Deploy**
1. Click **"Create Web Service"**
2. Wait for the build to complete (5-10 minutes)
3. Your app will be available at: `https://your-app-name.onrender.com`

---

## 🔧 Troubleshooting

### Common Issues & Solutions

#### 1. **Build Failed - cx-Oracle Error**
**Problem**: Oracle client libraries not available on Render
```
Solution: App automatically falls back to SQLite - no action needed
```

#### 2. **Port Binding Error**
**Problem**: Streamlit not binding to the correct port
```
Solution: Ensure Procfile uses $PORT variable (✅ already configured)
```

#### 3. **App Not Starting**
**Problem**: Missing dependencies or configuration
```
Check build logs in Render dashboard
Verify all files are committed to repository
```

#### 4. **Slow First Load** 
**Problem**: Free tier services sleep after inactivity
```
Solution: 
- Keep the app active by visiting it regularly, or
- Upgrade to a paid plan for 24/7 uptime
```

---

## 🎮 Demo Features to Test

After deployment, test these features:

### 📊 **Dashboard**
- Real-time manufacturing metrics
- Interactive charts and graphs
- System status overview

### 📦 **Raw Materials** 
- Add new materials
- Track inventory levels
- View material analytics

### 🏗️ **Production Planning**
- Create production orders
- Monitor progress
- Track order status

### ✅ **Quality Assurance**
- Record inspections
- View quality metrics
- Track compliance

### 🚚 **Logistics & Shipment**
- Track deliveries
- Monitor shipment status
- View logistics analytics

---

## 🚀 Performance Optimization

### For Production Use:
1. **Upgrade to Paid Plan**: For better performance and 24/7 uptime
2. **Add Database**: Consider PostgreSQL add-on for production data
3. **CDN**: Enable for faster asset loading
4. **Custom Domain**: Add your own domain name
5. **SSL**: Automatically provided by Render

---

## 📞 Support

### If you encounter issues:
1. Check [Render documentation](https://render.com/docs)
2. Review build logs in Render dashboard
3. Verify all environment variables are set correctly
4. Ensure your repository is public or properly connected

---

## 🏆 Success! 

Your Steel Manufacturing System should now be live on Render!

**Next Steps:**
- Share the URL with stakeholders
- Test all functionalities
- Monitor performance in Render dashboard
- Consider upgrading for production use

**URL Format**: `https://your-app-name.onrender.com`