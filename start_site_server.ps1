# D1 Softball Stats Server Starter
Write-Host "Starting D1 Softball Stats Server..." -ForegroundColor Green

# Get the script directory and navigate to the site folder
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$siteDir = Join-Path $scriptDir "apps\drill_down\site"

Write-Host "Script directory: $scriptDir" -ForegroundColor Yellow
Write-Host "Site directory: $siteDir" -ForegroundColor Yellow

# Check if the site directory exists
if (-not (Test-Path $siteDir)) {
    Write-Host "ERROR: Site directory not found at $siteDir" -ForegroundColor Red
    Write-Host "Please make sure the hybrid site has been generated." -ForegroundColor Red
    pause
    exit 1
}

# Check if index.html exists
$indexFile = Join-Path $siteDir "index.html"
if (-not (Test-Path $indexFile)) {
    Write-Host "ERROR: index.html not found in site directory" -ForegroundColor Red
    Write-Host "Please run the hybrid site generator first." -ForegroundColor Red
    pause
    exit 1
}

# Change to the site directory
Set-Location $siteDir
Write-Host "Current directory: $(Get-Location)" -ForegroundColor Green

# Check if port 8080 is already in use
$portCheck = netstat -ano | findstr :8080
if ($portCheck -and $portCheck -notmatch "TIME_WAIT") {
    Write-Host "WARNING: Port 8080 appears to be in use. Stopping existing process..." -ForegroundColor Yellow
    $processes = Get-NetTCPConnection -LocalPort 8080 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
    foreach ($pid in $processes) {
        Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
        Write-Host "Stopped process $pid" -ForegroundColor Yellow
    }
}

Write-Host "Starting HTTP server on port 8080..." -ForegroundColor Green
Write-Host "Visit http://localhost:8080" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the server
python -m http.server 8080 