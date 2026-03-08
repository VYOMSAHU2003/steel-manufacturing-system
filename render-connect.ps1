# Connect Repository to Render - Step by Step Guide

Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "   Connect GitHub Repository to Render               " -ForegroundColor White
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Your repository: steel-manufacturing-system" -ForegroundColor Green
Write-Host "GitHub URL: https://github.com/VYOMSAHU2003/steel-manufacturing-system" -ForegroundColor Green
Write-Host ""

Write-Host "STEP 1: Go to Render Dashboard" -ForegroundColor Yellow
Write-Host "1. Visit: https://dashboard.render.com" -ForegroundColor White
Write-Host "2. Sign in with your GitHub account" -ForegroundColor White
Write-Host ""

Write-Host "STEP 2: Create New Web Service" -ForegroundColor Yellow
Write-Host "1. Click 'New +' button (top right)" -ForegroundColor White
Write-Host "2. Select 'Web Service'" -ForegroundColor White
Write-Host ""

Write-Host "STEP 3: Connect Repository" -ForegroundColor Yellow
Write-Host "1. Find 'steel-manufacturing-system' in the list" -ForegroundColor White
Write-Host "2. Click 'Connect' next to it" -ForegroundColor White
Write-Host ""
Write-Host "If you don't see your repo:" -ForegroundColor Red
Write-Host "- Click 'Configure GitHub App'" -ForegroundColor White
Write-Host "- Grant access to your repositories" -ForegroundColor White
Write-Host "- Return and refresh" -ForegroundColor White
Write-Host ""

Write-Host "STEP 4: Verify Configuration" -ForegroundColor Yellow
Write-Host "Render should auto-fill these settings:" -ForegroundColor Green
Write-Host "- Name: steel-manufacturing-system" -ForegroundColor White
Write-Host "- Environment: Python" -ForegroundColor White
Write-Host "- Build Command: pip install -r requirements.txt" -ForegroundColor White
Write-Host "- Start Command: (from your render.yaml)" -ForegroundColor White
Write-Host ""

Write-Host "STEP 5: Deploy" -ForegroundColor Yellow
Write-Host "1. Click 'Create Web Service'" -ForegroundColor White
Write-Host "2. Wait 3-5 minutes for deployment" -ForegroundColor White
Write-Host "3. Get your live URL!" -ForegroundColor White
Write-Host ""

Write-Host "Opening Render dashboard now..." -ForegroundColor Cyan
Start-Process "https://dashboard.render.com"

Write-Host ""
Write-Host "Manual Configuration (if needed):" -ForegroundColor Yellow
Write-Host "Name: steel-manufacturing-system" -ForegroundColor Cyan
Write-Host "Environment: Python 3" -ForegroundColor Cyan
Write-Host "Build: pip install -r requirements.txt" -ForegroundColor Cyan
Write-Host "Start: streamlit run app.py --server.port `$PORT --server.address 0.0.0.0 --server.headless true" -ForegroundColor Cyan
Write-Host ""

$response = Read-Host "Press Enter after connecting (or type 'done' when deployed)"

Write-Host ""
if ($response -eq "done") {
    Write-Host "Excellent! Your Steel Manufacturing System should now be live!" -ForegroundColor Green
    Write-Host "Check your Render dashboard for the live URL" -ForegroundColor Cyan
} else {
    Write-Host "Continue with the steps above at: https://dashboard.render.com" -ForegroundColor Yellow
}
Write-Host ""
Write-Host "Your app will be available at: https://steel-manufacturing-system-XXXX.onrender.com" -ForegroundColor Green
Write-Host "Repository connection complete!" -ForegroundColor Cyan