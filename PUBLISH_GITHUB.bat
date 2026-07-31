@echo off
cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File ".\scripts\publish-github.ps1"
pause
