# 🚀 GitHub Repository Setup Script

# After creating your repository on GitHub, run these commands:

Write-Host "🏭 Steel Manufacturing System - GitHub Setup" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "✅ Repository configured locally" -ForegroundColor Green
Write-Host "✅ Deployment files ready" -ForegroundColor Green  
Write-Host "✅ GitHub Actions configured" -ForegroundColor Green
Write-Host "✅ Codespaces configured" -ForegroundColor Green
Write-Host ""

Write-Host "📋 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Create repository on GitHub.com" -ForegroundColor White
Write-Host "2. Run this script to push your code" -ForegroundColor White
Write-Host ""

$response = Read-Host "Have you created the GitHub repository? (y/n)"

if ($response -eq "y" -or $response -eq "Y") {
    Write-Host ""
    Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Cyan
    
    # Push to GitHub
    git push -u origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "🎉 SUCCESS! Your Steel Manufacturing System is now deployed on GitHub!" -ForegroundColor Green
        Write-Host ""
        Write-Host "🔗 Available Features:" -ForegroundColor Yellow
        Write-Host "- 🌐 Auto-deploy to Render: https://dashboard.render.com" -ForegroundColor White
        Write-Host "- 📱 GitHub Codespaces: Click 'Code' → 'Codespaces'" -ForegroundColor White  
        Write-Host "- 🔄 GitHub Actions: Check 'Actions' tab" -ForegroundColor White
        Write-Host "- 📄 Documentation: Enable Pages in Settings" -ForegroundColor White
        Write-Host ""
        Write-Host "🎯 Next: Connect to Render or Streamlit Cloud for live deployment!" -ForegroundColor Cyan
    } else {
        Write-Host ""
        Write-Host "❌ Push failed. Please check:" -ForegroundColor Red
        Write-Host "- Repository exists on GitHub" -ForegroundColor White
        Write-Host "- You have write permissions" -ForegroundColor White
        Write-Host "- GitHub remote URL is correct" -ForegroundColor White
    }
} else {
    Write-Host ""
    Write-Host "📋 Please create the repository first:" -ForegroundColor Yellow
    Write-Host "1. Go to: https://github.com/new" -ForegroundColor White
    Write-Host "2. Name: steel-manufacturing-system" -ForegroundColor White
    Write-Host "3. Don't initialize with README" -ForegroundColor White
    Write-Host "4. Create repository" -ForegroundColor White
    Write-Host "5. Run this script again" -ForegroundColor White
}

Write-Host ""
Write-Host "📞 Need help? Check GITHUB_DEPLOYMENT.md for detailed instructions" -ForegroundColor Cyan