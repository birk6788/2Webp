@echo off
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\publish-github.ps1"
if errorlevel 1 (
  echo.
  echo Publication interrompue. Lisez le message ci-dessus.
  pause
  exit /b 1
)
echo.
echo Publication terminee.
pause
