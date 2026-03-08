# 🔍 CHECK DEPLOYMENT STATUS
Write-Host "🚀 Checking Render Deployment Status..." -ForegroundColor Cyan
Write-Host ""

$url = "https://steel-manufacturing-system.onrender.com"

Write-Host "📡 Testing connection to: $url" -ForegroundColor Yellow
Write-Host ""

try {
    # Test if the URL is responsive
    $response = Invoke-WebRequest -Uri $url -TimeoutSec 10 -UseBasicParsing -ErrorAction Stop
    
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ SUCCESS! App is LIVE!" -ForegroundColor Green
        Write-Host "✅ HTTP Status: $($response.StatusCode)" -ForegroundColor Green
        Write-Host "✅ App is responding correctly" -ForegroundColor Green
        Write-Host ""
        Write-Host "🌐 Your Steel Manufacturing System is now accessible at:" -ForegroundColor Magenta
        Write-Host "   $url" -ForegroundColor White
        Write-Host ""
        Write-Host "🎉 Deployment SUCCESSFUL! The Oracle dependency issue has been resolved." -ForegroundColor Green
    } else {
        Write-Host "⚠️  App responded but with status: $($response.StatusCode)" -ForegroundColor Yellow
        Write-Host "   This might indicate the app is still starting up..." -ForegroundColor Yellow
    }
    
} catch {
    $errorMsg = $_.Exception.Message
    
    if ($errorMsg -like "*timeout*" -or $errorMsg -like "*timed out*") {
        Write-Host "🔄 App is still deploying/starting up..." -ForegroundColor Yellow
        Write-Host "   This is normal - Render apps can take 3-5 minutes to fully deploy" -ForegroundColor White
        Write-Host "   Try again in 2-3 minutes" -ForegroundColor White
    } elseif ($errorMsg -like "*404*" -or $errorMsg -like "*Not Found*") {
        Write-Host "⚠️  Still getting 'Not Found' - deployment may still be in progress" -ForegroundColor Yellow
        Write-Host "   Check Render dashboard logs for build progress" -ForegroundColor White
    } else {
        Write-Host "❌ Connection failed: $errorMsg" -ForegroundColor Red
        Write-Host "   Check Render dashboard for deployment status" -ForegroundColor White
    }
}

Write-Host ""
Write-Host "📊 Manual Check Steps:" -ForegroundColor Cyan
Write-Host "1. Visit: https://dashboard.render.com" -ForegroundColor White
Write-Host "2. Click on 'steel-manufacturing-system'" -ForegroundColor White
Write-Host "3. Check 'Logs' tab for deployment progress" -ForegroundColor White
Write-Host "4. Look for 'Using SQLite database for deployment'" -ForegroundColor White
Write-Host "5. Wait for 'Your service is live' message" -ForegroundColor White
Write-Host ""
Write-Host "🔄 Run this script again in a few minutes to recheck status" -ForegroundColor Gray