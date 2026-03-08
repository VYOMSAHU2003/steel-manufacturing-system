# Simple Render URL Finder

Write-Host "Steel Manufacturing System - Render URL Finder" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Your GitHub repository: https://github.com/VYOMSAHU2003/steel-manufacturing-system" -ForegroundColor Green
Write-Host ""

Write-Host "To get your Render URL:" -ForegroundColor Yellow
Write-Host "1. Go to: https://dashboard.render.com" -ForegroundColor Cyan
Write-Host "2. Sign in with GitHub" -ForegroundColor White
Write-Host "3. Look for 'steel-manufacturing-system'" -ForegroundColor White
Write-Host "4. Click on it to see your live URL" -ForegroundColor White
Write-Host ""

Write-Host "If not deployed yet:" -ForegroundColor Yellow
Write-Host "1. Click 'New +' -> 'Web Service'" -ForegroundColor White
Write-Host "2. Select your repository" -ForegroundColor White
Write-Host "3. Click 'Deploy'" -ForegroundColor White
Write-Host "4. Wait 3-5 minutes" -ForegroundColor White
Write-Host ""

Write-Host "Opening Render dashboard..." -ForegroundColor Cyan
Start-Process "https://dashboard.render.com"

Write-Host ""
Write-Host "Your URL format: https://steel-manufacturing-system-XXXX.onrender.com" -ForegroundColor Green
Write-Host ""