# Satoshi Sentinel — one-command local demo (Windows).
# Double-click this file or run: powershell -ExecutionPolicy Bypass -File start.ps1
$root = $PSScriptRoot
Write-Host "Starting backend (FastAPI :8000)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location -LiteralPath `"$root\backend`"; python -m uvicorn app.main:app --reload"
Write-Host "Starting frontend (Vite :5173)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location -LiteralPath `"$root\frontend`"; npm run dev"
Write-Host "Waiting for servers, then opening browser..." -ForegroundColor Green
Start-Sleep -Seconds 8
Start-Process "http://localhost:5173"
Write-Host "Done. Keep both server windows open. Backend health: http://localhost:8000/api/health" -ForegroundColor Green
