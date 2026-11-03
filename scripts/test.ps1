# Run unit + API tests.
# Run: powershell -ExecutionPolicy Bypass -File scripts\test.ps1
Set-Location (Join-Path $PSScriptRoot "..")

.venv\Scripts\python.exe -m pytest
exit $LASTEXITCODE
