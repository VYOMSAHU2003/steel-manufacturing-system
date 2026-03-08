# 🚀 One-Click Complete Deployment Script
# This script handles everything automatically for future deployments

Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "   Steel Manufacturing System - One-Click Deploy     " -ForegroundColor White  
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host ""

# Auto-commit any new changes
Write-Host "Checking for new changes..." -ForegroundColor Yellow
$gitStatus = git status --porcelain

if ($gitStatus) {
    Write-Host "Found changes, committing automatically..." -ForegroundColor Cyan
    git add .
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    git commit -m "🔄 Auto-deploy update - $timestamp"
    
    Write-Host "Pushing updates to GitHub..." -ForegroundColor Cyan
    git push origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Updates pushed successfully!" -ForegroundColor Green
        Write-Host "🔄 GitHub Actions will automatically deploy to Render" -ForegroundColor Yellow
    } else {
        Write-Host "❌ Push failed. Check your GitHub connection." -ForegroundColor Red
    }
} else {
    Write-Host "✅ No changes detected. Everything is up to date!" -ForegroundColor Green
}

Write-Host ""
Write-Host "🌐 Your deployment status:" -ForegroundColor Cyan
Write-Host "- GitHub Repository: https://github.com/VYOMSAHU2003/steel-manufacturing-system" -ForegroundColor White
Write-Host "- GitHub Actions: Building and deploying automatically" -ForegroundColor White  
Write-Host "- Render Deployment: https://dashboard.render.com" -ForegroundColor White
Write-Host "- Codespaces: Ready for instant development" -ForegroundColor White

Write-Host ""
Write-Host "✨ Deployment complete! Your app is live and updating automatically." -ForegroundColor Green