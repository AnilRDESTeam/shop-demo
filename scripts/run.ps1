# Start the shop on 127.0.0.1 (local only). Set $env:PORT to change the port.
# Run: powershell -ExecutionPolicy Bypass -File scripts\run.ps1
Set-Location (Join-Path $PSScriptRoot "..")

$port = if ($env:PORT) { $env:PORT } else { "8080" }
Write-Host "Open http://localhost:$port"
.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port $port --reload
