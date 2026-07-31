$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
py -m pip install --upgrade pip
py -m pip install -r .\requirements.txt
Write-Host "Dépendances 2Webp installées." -ForegroundColor Green
