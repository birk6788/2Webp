$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$Version = "0.8.0"
Write-Host "=== 2Webp v$Version ===" -ForegroundColor Cyan

py -c "from PIL import Image; from PySide6.QtWidgets import QApplication; import PyInstaller; print('Dépendances OK')"
py -m py_compile .\app.py .\core.py
py .\tests\test_translations.py
py .\tests\test_presets.py
py .\tests\test_preset_ui.py
py .\tests\test_business_groups.py
py .\tests\test_conversion.py
py .\tests\test_conversion_ui.py
py .\tests\test_settings_ui.py
py .\tests\smoke_test.py
py .\tests\test_clean_branding.py
py .\tests\test_windows_icon.py

Remove-Item .\build -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item .\dist -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item .\release -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item .\2Webp.spec -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path .\release | Out-Null

py -m PyInstaller `
  --noconfirm `
  --clean `
  --windowed `
  --onedir `
  --name "2Webp" `
  --icon ".\assets\brand\2Webp-taskbar-round.ico" `
  --add-data ".\assets;assets" `
  --add-data ".\translations;translations" `
  ".\app.py"

Copy-Item .\README.md .\dist\2Webp\README.md
Copy-Item .\LICENSE .\dist\2Webp\LICENSE
$Archive = ".\release\2Webp-v$Version-windows-x64.zip"
$TempPackage = Join-Path $env:TEMP "2Webp-v$Version-package"
Remove-Item $TempPackage -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $TempPackage | Out-Null

$Copied = $false
for ($Attempt = 1; $Attempt -le 5; $Attempt++) {
  try {
    Copy-Item .\dist\2Webp\* $TempPackage -Recurse -Force
    $Copied = $true
    break
  } catch {
    if ($Attempt -eq 5) { throw }
    Start-Sleep -Seconds 2
  }
}

if (-not $Copied) { throw "Impossible de préparer le dossier temporaire de distribution." }
Compress-Archive -Path "$TempPackage\*" -DestinationPath $Archive -Force
Remove-Item $TempPackage -Recurse -Force -ErrorAction SilentlyContinue
$Hash = Get-FileHash $Archive -Algorithm SHA256
"$($Hash.Hash.ToLower())  2Webp-v$Version-windows-x64.zip" | Set-Content ".\release\2Webp-v$Version-windows-x64.zip.sha256" -Encoding ascii

Write-Host "" 
Write-Host "Build terminé" -ForegroundColor Green
Write-Host "$PSScriptRoot\dist\2Webp\2Webp.exe"
Write-Host "$PSScriptRoot\release\2Webp-v$Version-windows-x64.zip"
Write-Host "$PSScriptRoot\release\2Webp-v$Version-windows-x64.zip.sha256"
