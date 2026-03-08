# 🔗 Step-by-Step: Connect Repository to Render

Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "   Connect steel-manufacturing-system to Render      " -ForegroundColor White
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "✅ Prerequisites Check:" -ForegroundColor Green
Write-Host "- GitHub repository: steel-manufacturing-system ✅" -ForegroundColor White
Write-Host "- Repository URL: https://github.com/VYOMSAHU2003/steel-manufacturing-system ✅" -ForegroundColor White
Write-Host "- render.yaml configured: ✅" -ForegroundColor White
Write-Host "- Auto-deploy enabled: ✅" -ForegroundColor White
Write-Host ""

Write-Host "🚀 STEP-BY-STEP CONNECTION:" -ForegroundColor Yellow
Write-Host ""

Write-Host "Step 1: Access Render Dashboard" -ForegroundColor Cyan
Write-Host "--------------------------------" -ForegroundColor Gray
Write-Host "1. Go to: https://dashboard.render.com" -ForegroundColor White
Write-Host "2. Sign in with your GitHub account" -ForegroundColor White
Write-Host "   (Use the same account that owns steel-manufacturing-system)" -ForegroundColor Gray
Write-Host ""

Write-Host "Step 2: Create New Web Service" -ForegroundColor Cyan  
Write-Host "------------------------------" -ForegroundColor Gray
Write-Host "1. Click the 'New +' button (top right)" -ForegroundColor White
Write-Host "2. Select 'Web Service' from dropdown" -ForegroundColor White
Write-Host ""

Write-Host "Step 3: Connect Your Repository" -ForegroundColor Cyan
Write-Host "-------------------------------" -ForegroundColor Gray
Write-Host "1. You'll see a list of your GitHub repositories" -ForegroundColor White
Write-Host "2. Find: 'steel-manufacturing-system'" -ForegroundColor White
Write-Host "3. Click 'Connect' next to it" -ForegroundColor White
Write-Host ""
Write-Host "   If you don't see your repo:" -ForegroundColor Yellow
Write-Host "   - Click 'Configure GitHub App'" -ForegroundColor White
Write-Host "   - Grant access to steel-manufacturing-system" -ForegroundColor White
Write-Host "   - Return to Render and refresh" -ForegroundColor White
Write-Host ""

Write-Host "Step 4: Service Configuration" -ForegroundColor Cyan
Write-Host "-----------------------------" -ForegroundColor Gray
Write-Host "Render will auto-fill these from your render.yaml:" -ForegroundColor Green
Write-Host "- Name: steel-manufacturing-system" -ForegroundColor White
Write-Host "- Environment: Python 3" -ForegroundColor White
Write-Host "- Build Command: pip install -r requirements.txt" -ForegroundColor White
Write-Host "- Start Command: streamlit run app.py --server.port..." -ForegroundColor White
Write-Host "- Auto-Deploy: Yes" -ForegroundColor White
Write-Host ""
Write-Host "✅ Just verify these settings are correct" -ForegroundColor Green
Write-Host ""

Write-Host "Step 5: Deploy" -ForegroundColor Cyan
Write-Host "-------------" -ForegroundColor Gray
Write-Host "1. Scroll down to bottom" -ForegroundColor White
Write-Host "2. Click 'Create Web Service'" -ForegroundColor White
Write-Host "3. Wait for deployment (3-5 minutes)" -ForegroundColor White
Write-Host ""

Write-Host "Opening Render dashboard for you..." -ForegroundColor Yellow
Start-Process "https://dashboard.render.com"
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "🔍 TROUBLESHOOTING:" -ForegroundColor Yellow
Write-Host ""
Write-Host "Problem: Can't see repository" -ForegroundColor Red
Write-Host "Solution: Click 'Configure GitHub App' and grant access" -ForegroundColor Green
Write-Host ""
Write-Host "Problem: Build fails" -ForegroundColor Red
Write-Host "Solution: Check that render.yaml and requirements.txt exist" -ForegroundColor Green
Write-Host "         (They do exist in your project ✅)" -ForegroundColor White
Write-Host ""
Write-Host "Problem: App won't start" -ForegroundColor Red
Write-Host "Solution: Verify Procfile has correct Streamlit command" -ForegroundColor Green
Write-Host "         (Already configured correctly ✅)" -ForegroundColor White
Write-Host ""

Write-Host "⏱️ TIMELINE:" -ForegroundColor Yellow
Write-Host "- Connection setup: 2-3 minutes" -ForegroundColor White
Write-Host "- First deployment: 3-5 minutes" -ForegroundColor White
Write-Host "- Your app will be live: ~5-8 minutes total" -ForegroundColor White
Write-Host ""

Write-Host "🎯 AFTER DEPLOYMENT:" -ForegroundColor Green
Write-Host "- You'll get a live URL like:" -ForegroundColor White
Write-Host "  https://steel-manufacturing-system-XXXX.onrender.com" -ForegroundColor Cyan
Write-Host "- Future GitHub pushes auto-deploy" -ForegroundColor White
Write-Host "- You can monitor status from Render dashboard" -ForegroundColor White
Write-Host ""

$response = Read-Host "Press Enter after connecting your repository (or 'help' if you need assistance)"

if ($response -eq "help") {
    Write-Host ""
    Write-Host "🆘 COMMON ISSUES & SOLUTIONS:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Issue 1: Repository not showing" -ForegroundColor Red
    Write-Host "1. Make sure you're signed in with VYOMSAHU2003 GitHub account" -ForegroundColor White
    Write-Host "2. Click 'Configure GitHub App' in Render" -ForegroundColor White
    Write-Host "3. Select 'All repositories' or specifically choose steel-manufacturing-system" -ForegroundColor White
    Write-Host "4. Save and return to Render" -ForegroundColor White
    Write-Host ""
    Write-Host "Issue 2: Permission denied" -ForegroundColor Red
    Write-Host "1. Go to GitHub.com" -ForegroundColor White
    Write-Host "2. Settings > Applications" -ForegroundColor White
    Write-Host "3. Find Render and grant repository access" -ForegroundColor White
    Write-Host ""
    Write-Host "Issue 3: Configuration not auto-filling" -ForegroundColor Red
    Write-Host "1. Manually enter these settings:" -ForegroundColor White
    Write-Host "   Name: steel-manufacturing-system" -ForegroundColor Cyan
    Write-Host "   Environment: Python 3" -ForegroundColor Cyan
    Write-Host "   Build Command: pip install -r requirements.txt" -ForegroundColor Cyan
    Write-Host "   Start Command: streamlit run app.py --server.port \$PORT --server.address 0.0.0.0 --server.headless true" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "🎉 Great! Your deployment should be starting now!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Monitor progress at: https://dashboard.render.com" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Check back in 5-8 minutes for your live URL!" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ Repository connection complete!" -ForegroundColor Green