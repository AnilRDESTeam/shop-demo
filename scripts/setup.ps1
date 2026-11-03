# First-time setup: venv, dependencies, Playwright browser.
# Run: powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Creating virtual environment (.venv) ..."
    python -m venv .venv
}

Write-Host "Installing dependencies ..."
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt

Write-Host "Installing Chromium for browser tests ..."
.venv\Scripts\python.exe -m playwright install chromium
if ($LASTEXITCODE -ne 0) {
    Write-Host "Chromium download blocked. Set `$env:SHOP_BROWSER_CHANNEL='msedge' to use Edge instead."
    $global:LASTEXITCODE = 0
}

Write-Host "Setup done. Next: scripts\run.ps1"
