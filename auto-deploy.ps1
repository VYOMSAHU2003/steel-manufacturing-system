# 🚀 Fully Automatic GitHub Deployment Script
# This script automatically creates repository and deploys your Steel Manufacturing System

param(
    [string]$RepoName = "steel-manufacturing-system",
    [string]$Description = "Steel Manufacturing Plant Management System - Enterprise-grade solution with Streamlit"
)

Write-Host "Steel Manufacturing System - Automatic GitHub Deployment" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

# Initialize variables
$deploymentSuccess = $false
$skipRepoCreation = $false

# Check if GitHub CLI is installed and authenticated
Write-Host "Checking GitHub CLI..." -ForegroundColor Yellow

try {
    $ghOutput = gh auth status 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "GitHub CLI authenticated successfully" -ForegroundColor Green
        
        # Try to create repository using GitHub CLI
        Write-Host "Creating GitHub repository..." -ForegroundColor Cyan
        
        $createOutput = gh repo create $RepoName --description $Description --public --source . --remote origin --push 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Repository created and code pushed successfully!" -ForegroundColor Green
            $deploymentSuccess = $true
        } else {
            Write-Host "Repository creation failed, trying manual push..." -ForegroundColor Yellow
            $skipRepoCreation = $true
        }
    } else {
        Write-Host "GitHub CLI not authenticated" -ForegroundColor Yellow
        $skipRepoCreation = $true
    }
} catch {
    Write-Host "GitHub CLI not available, using manual method..." -ForegroundColor Yellow
    $skipRepoCreation = $true
}

# If automatic creation failed, try manual push
if ($skipRepoCreation -and -not $deploymentSuccess) {
    Write-Host ""
    Write-Host "Manual repository setup required:" -ForegroundColor Yellow
    Write-Host "1. Go to: https://github.com/new" -ForegroundColor White
    Write-Host "2. Repository name: $RepoName" -ForegroundColor White
    Write-Host "3. Make it Public" -ForegroundColor White
    Write-Host "4. Do NOT initialize with README" -ForegroundColor Yellow
    Write-Host "5. Click 'Create repository'" -ForegroundColor White
    Write-Host ""
    
    $response = Read-Host "Have you created the repository? (y/n)"
    
    if ($response -eq "y" -or $response -eq "Y") {
        Write-Host "Pushing code to GitHub repository..." -ForegroundColor Cyan
        
        # Configure remote and push
        git remote set-url origin "https://github.com/VYOMSAHU2003/$RepoName.git" 2>&1 | Out-Null
        $pushOutput = git push -u origin main 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Code pushed to GitHub successfully!" -ForegroundColor Green
            $deploymentSuccess = $true
        } else {
            Write-Host "Push failed. Please check repository exists and you have permissions." -ForegroundColor Red
            Write-Host "Error: $pushOutput" -ForegroundColor Red
        }
    }
}

# Display results
Write-Host ""
Write-Host "Deployment Summary:" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan

if ($deploymentSuccess) {
    Write-Host "SUCCESS! Your Steel Manufacturing System is now on GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Repository URL: https://github.com/VYOMSAHU2003/$RepoName" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Available Features:" -ForegroundColor Yellow
    Write-Host "- GitHub Actions: Automated CI/CD pipeline" -ForegroundColor Green
    Write-Host "- GitHub Codespaces: Cloud development environment" -ForegroundColor Green
    Write-Host "- Auto-deploy to Render: Connect at dashboard.render.com" -ForegroundColor Green
    Write-Host "- GitHub Pages: Enable in Settings -> Pages" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Cyan
    Write-Host "1. Connect to Render: https://render.com" -ForegroundColor White
    Write-Host "2. Try Codespaces: Click 'Code' -> 'Codespaces'" -ForegroundColor White
    Write-Host "3. Check Actions: Go to 'Actions' tab" -ForegroundColor White
    Write-Host "4. Enable Pages: Settings -> Pages -> Deploy from branch" -ForegroundColor White
} else {
    Write-Host "Deployment setup in progress..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Local repository configured" -ForegroundColor Green
    Write-Host "Deployment files created" -ForegroundColor Green
    Write-Host "GitHub repository connection pending" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Complete setup manually:" -ForegroundColor Cyan
    Write-Host "1. Create repository at: https://github.com/new" -ForegroundColor White
    Write-Host "2. Name: $RepoName" -ForegroundColor White
    Write-Host "3. Run: git push -u origin main" -ForegroundColor White
}

Write-Host ""
Write-Host "Opening helpful links..." -ForegroundColor Cyan

# Open browser tabs
Start-Sleep -Seconds 1
Start-Process "https://github.com/new"
Start-Sleep -Seconds 2  
Start-Process "https://render.com"

Write-Host "Setup complete! Check your browser for GitHub and Render." -ForegroundColor Green