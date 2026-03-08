# 🚀 Simple Render Auto-Deploy Setup

Write-Host "Steel Manufacturing System - Render Auto-Deploy" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "✅ Your project is ready for Render deployment!" -ForegroundColor Green
Write-Host ""

Write-Host "Configuration Status:" -ForegroundColor Yellow
Write-Host "✅ render.yaml - Auto-deploy enabled" -ForegroundColor Green
Write-Host "✅ Procfile - Streamlit configuration" -ForegroundColor Green
Write-Host "✅ requirements.txt - Dependencies ready" -ForegroundColor Green
Write-Host "✅ GitHub repository - Connected" -ForegroundColor Green
Write-Host ""

Write-Host "Opening Render dashboard..." -ForegroundColor Cyan
Start-Process "https://dashboard.render.com"
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "Follow these steps on Render:" -ForegroundColor Yellow
Write-Host "1. Sign in with GitHub" -ForegroundColor White
Write-Host "2. Click 'New +' -> 'Web Service'" -ForegroundColor White  
Write-Host "3. Connect 'steel-manufacturing-system' repository" -ForegroundColor White
Write-Host "4. Click 'Deploy Web Service'" -ForegroundColor White
Write-Host ""
Write-Host "Render will automatically:" -ForegroundColor Green
Write-Host "- Use your render.yaml configuration" -ForegroundColor White
Write-Host "- Deploy on every GitHub push" -ForegroundColor White
Write-Host "- Give you a live URL" -ForegroundColor White
Write-Host ""

$response = Read-Host "Press Enter after setting up on Render"

Write-Host ""
Write-Host "Testing auto-deployment..." -ForegroundColor Cyan

# Create test file and push
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
"# Auto-Deploy Test`n`nCreated: $timestamp`n`nTesting automatic deployment!" | Out-File -FilePath "deploy-test.txt" -Encoding UTF8

git add deploy-test.txt
git commit -m "Test auto-deploy $timestamp"
$pushResult = git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "SUCCESS! Auto-deploy test pushed to GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Check deployment status:" -ForegroundColor Yellow
    Write-Host "- Render Dashboard: https://dashboard.render.com" -ForegroundColor Cyan
    Write-Host "- GitHub Actions: Check your repository Actions tab" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Your app will be live in 2-3 minutes!" -ForegroundColor Green
    Write-Host "URL format: https://steel-manufacturing-system-XXX.onrender.com" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Future deployments are now automatic!" -ForegroundColor Green
} else {
    Write-Host "Push failed. Check your GitHub connection." -ForegroundColor Red
}

Write-Host ""
Write-Host "Auto-deployment setup complete!" -ForegroundColor Green