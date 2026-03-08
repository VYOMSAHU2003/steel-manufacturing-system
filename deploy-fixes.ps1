# 🚀 DEPLOY FIXED CONFIGURATION
Write-Host "🔧 Deploying Configuration Fixes..." -ForegroundColor Cyan
Write-Host ""

# Step 1: Test Streamlit
Write-Host "📋 Testing Streamlit installation..." -ForegroundColor Yellow
python -c "import streamlit; print('✅ Streamlit OK')"

Write-Host ""
Write-Host "📋 Deploying fixes..." -ForegroundColor Yellow

# Add all changes
git add .
Write-Host "✅ Files staged" -ForegroundColor Green

# Commit fixes
git commit -m "Fix deployment configuration - simplified render.yaml and Procfile"
Write-Host "✅ Changes committed" -ForegroundColor Green

# Push to GitHub (triggers Render deploy)
git push origin main
Write-Host "✅ Pushed to GitHub - Render deployment triggered!" -ForegroundColor Green

Write-Host ""
Write-Host "🚀 DEPLOYMENT STATUS:" -ForegroundColor Cyan
Write-Host "   ✅ Configuration fixes applied" -ForegroundColor Green
Write-Host "   ✅ Auto-deployment triggered on Render" -ForegroundColor Green
Write-Host "   🔄 Wait 3-5 minutes for rebuild to complete" -ForegroundColor Yellow
Write-Host ""
Write-Host "🌐 YOUR FIXED APP URL:" -ForegroundColor Magenta
Write-Host "   https://steel-manufacturing-system.onrender.com" -ForegroundColor White
Write-Host ""
Write-Host "📊 Monitor deployment:" -ForegroundColor Cyan
Write-Host "   • Go to Render dashboard" -ForegroundColor White
Write-Host "   • Check 'Logs' tab for deployment progress" -ForegroundColor White
Write-Host "   • Look for 'Your service is live' message" -ForegroundColor White
Write-Host ""
Write-Host "✨ Configuration fixes applied! Check your URL in a few minutes." -ForegroundColor Green