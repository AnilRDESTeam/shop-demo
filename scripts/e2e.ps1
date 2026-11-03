# Run browser tests (starts its own server on port 8099).
# Run: powershell -ExecutionPolicy Bypass -File scripts\e2e.ps1
Set-Location (Join-Path $PSScriptRoot "..")

.venv\Scripts\python.exe -m pytest -m e2e
exit $LASTEXITCODE
