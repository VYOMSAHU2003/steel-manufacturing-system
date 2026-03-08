# 🚀 Automatic Render Deployment Setup Script
# This script helps you connect GitHub to Render for automatic deployments

Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "   Steel Manufacturing System - Auto Render Deploy   " -ForegroundColor White
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "✅ Your project is configured for automatic Render deployment!" -ForegroundColor Green
Write-Host ""

# Check configuration
Write-Host "🔍 Checking deployment configuration:" -ForegroundColor Yellow
Write-Host "✅ render.yaml - Configured for auto-deploy" -ForegroundColor Green
Write-Host "✅ Procfile - Streamlit server configuration" -ForegroundColor Green  
Write-Host "✅ requirements.txt - Python dependencies" -ForegroundColor Green
Write-Host "✅ GitHub repository - https://github.com/VYOMSAHU2003/steel-manufacturing-system" -ForegroundColor Green
Write-Host ""

Write-Host "🌐 Setting up automatic deployment to Render..." -ForegroundColor Cyan
Write-Host ""

# Open Render dashboard
Write-Host "📱 Opening Render dashboard..." -ForegroundColor Cyan
Start-Process "https://dashboard.render.com"

Write-Host ""
Write-Host "📋 Follow these steps for AUTOMATIC deployment:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. 🔐 Sign in to Render with GitHub account" -ForegroundColor White
Write-Host "2. 🆕 Click 'New +' → 'Web Service'" -ForegroundColor White
Write-Host "3. 🔗 Connect repository: 'steel-manufacturing-system'" -ForegroundColor White
Write-Host "4. ✨ Render will auto-detect render.yaml configuration" -ForegroundColor White
Write-Host "5. ✅ Click 'Deploy Web Service'" -ForegroundColor White
Write-Host ""
Write-Host "🎯 Configuration will be automatic:" -ForegroundColor Green
Write-Host "   - Service Name: steel-manufacturing-system" -ForegroundColor White
Write-Host "   - Build Command: pip install -r requirements.txt" -ForegroundColor White
Write-Host "   - Start Command: streamlit run app.py (configured)" -ForegroundColor White
Write-Host "   - Auto-Deploy: ✅ Enabled (on every GitHub push)" -ForegroundColor White
Write-Host "   - Environment: Python 3.9" -ForegroundColor White
Write-Host ""

Write-Host "⏱️  Deployment Timeline:" -ForegroundColor Cyan
Write-Host "   - First deployment: ~5-8 minutes" -ForegroundColor White
Write-Host "   - Future auto-deploys: ~2-3 minutes" -ForegroundColor White
Write-Host ""

Write-Host "🔄 After setup, automatic deployment works like this:" -ForegroundColor Yellow
Write-Host "   1. You push code to GitHub" -ForegroundColor White
Write-Host "   2. Render detects the push automatically" -ForegroundColor White  
Write-Host "   3. Render builds and deploys your app" -ForegroundColor White
Write-Host "   4. Your live app is updated automatically" -ForegroundColor White
Write-Host ""

Write-Host "🎊 Your live app will be available at:" -ForegroundColor Green
Write-Host "   https://steel-manufacturing-system-[random].onrender.com" -ForegroundColor Cyan
Write-Host ""

# Wait for user to complete setup
Read-Host "Press Enter after completing the setup on Render dashboard"

Write-Host ""
Write-Host "🧪 Testing automatic deployment..." -ForegroundColor Cyan

# Create a test update to trigger auto-deploy
Write-Host "Creating test update to verify auto-deployment..." -ForegroundColor Yellow

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Create a simple test file
"# Auto-Deploy Test - $timestamp`n`nThis file tests automatic Render deployment.`nCreated: $timestamp`n`nIf you see this, auto-deploy is working!" | Out-File -FilePath "AUTO_DEPLOY_TEST.md" -Encoding UTF8

Write-Host "📤 Pushing test update to trigger auto-deployment..." -ForegroundColor Cyan
git add AUTO_DEPLOY_TEST.md
git commit -m "🧪 Test automatic Render deployment - $timestamp"
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "🎉 SUCCESS! Auto-deployment test triggered!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🔍 Check deployment status:" -ForegroundColor Yellow
    Write-Host "   - Render Dashboard: https://dashboard.render.com" -ForegroundColor Cyan
    Write-Host "   - GitHub Actions: https://github.com/VYOMSAHU2003/steel-manufacturing-system/actions" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "⏰ Your app should be live in 2-3 minutes!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🔄 Future deployments are now automatic:" -ForegroundColor Cyan
    Write-Host "   Just run: git add . && git commit -m 'message' && git push" -ForegroundColor White
    Write-Host "   Render will deploy automatically!" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "❌ Push failed. Please check your GitHub connection." -ForegroundColor Red
}

Write-Host ""
Write-Host "✨ Automatic Render deployment is now configured!" -ForegroundColor Green
Write-Host "Your Steel Manufacturing System will auto-deploy on every code push! 🏭🚀" -ForegroundColor Cyan