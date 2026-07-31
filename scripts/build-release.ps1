param(
  [switch]$SkipTests
)

$ErrorActionPreference = "Stop"
if ($PSVersionTable.PSVersion.Major -ge 7) {
  $PSNativeCommandUseErrorActionPreference = $true
}

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$Version = (Get-Content .\VERSION -Raw).Trim()
$ReleaseDir = Join-Path $Root "release"
$OnedirDist = Join-Path $Root "dist\onedir"
$OnefileDist = Join-Path $Root "dist\onefile"
$Python = (Get-Command python -ErrorAction Stop).Source

function Invoke-Python {
  param(
    [Parameter(Mandatory = $true)]
    [string[]]$Arguments
  )

  & $Python @Arguments
  if ($LASTEXITCODE -ne 0) {
    throw "Python a échoué avec le code $LASTEXITCODE : $($Arguments -join ' ')"
  }
}

Write-Host "=== 2Webp release v$Version ===" -ForegroundColor Cyan
Write-Host "Python utilisé : $Python" -ForegroundColor DarkGray
Invoke-Python -Arguments @(
  "-c",
  "from PIL import Image; from PySide6.QtWidgets import QApplication; import PyInstaller; print('Dependances OK')"
)
Invoke-Python -Arguments @(".\scripts\check_version.py")
Invoke-Python -Arguments @("-m", "py_compile", ".\app.py", ".\core.py")

if (-not $SkipTests) {
  $env:QT_QPA_PLATFORM = "offscreen"
  $Tests = @(
    "test_translations.py",
    "test_presets.py",
    "test_preset_ui.py",
    "test_business_groups.py",
    "test_conversion.py",
    "test_conversion_ui.py",
    "test_settings_ui.py",
    "smoke_test.py",
    "test_clean_branding.py",
    "test_windows_icon.py"
  )
  foreach ($Test in $Tests) {
    Invoke-Python -Arguments @(".\tests\$Test")
  }
}

Remove-Item .\build -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item .\dist -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item $ReleaseDir -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $ReleaseDir | Out-Null
New-Item -ItemType Directory -Path .\build\specs | Out-Null

Write-Host "Build onedir..." -ForegroundColor Yellow
Invoke-Python -Arguments @(
  "-m", "PyInstaller",
  "--noconfirm",
  "--clean",
  "--windowed",
  "--onedir",
  "--name", "2Webp",
  "--distpath", $OnedirDist,
  "--workpath", ".\build\onedir",
  "--specpath", ".\build\specs",
  "--icon", ".\assets\brand\2Webp-taskbar-round.ico",
  "--add-data", ".\assets;assets",
  "--add-data", ".\translations;translations",
  ".\app.py"
)

$OnedirApp = Join-Path $OnedirDist "2Webp"
if (-not (Test-Path $OnedirApp)) {
  throw "Le build onedir attendu n'existe pas : $OnedirApp"
}
Copy-Item .\README.md $OnedirApp
Copy-Item .\LICENSE $OnedirApp
Copy-Item .\PRIVACY.md $OnedirApp
Copy-Item .\SECURITY.md $OnedirApp
Copy-Item .\RELEASE_NOTES.md $OnedirApp

Write-Host "Build portable onefile..." -ForegroundColor Yellow
$PortableName = "2Webp-v$Version-portable"
Invoke-Python -Arguments @(
  "-m", "PyInstaller",
  "--noconfirm",
  "--clean",
  "--windowed",
  "--onefile",
  "--name", $PortableName,
  "--distpath", $OnefileDist,
  "--workpath", ".\build\onefile",
  "--specpath", ".\build\specs",
  "--icon", ".\assets\brand\2Webp-taskbar-round.ico",
  "--add-data", ".\assets;assets",
  "--add-data", ".\translations;translations",
  ".\app.py"
)

$PortableSource = Join-Path $OnefileDist "$PortableName.exe"
$PortableTarget = Join-Path $ReleaseDir "$PortableName.exe"
if (-not (Test-Path $PortableSource)) {
  throw "L'exécutable portable attendu n'existe pas : $PortableSource"
}
Copy-Item $PortableSource $PortableTarget -Force

Write-Host "Archive ZIP..." -ForegroundColor Yellow
$Archive = Join-Path $ReleaseDir "2Webp-v$Version-windows-x64.zip"
$TempPackage = Join-Path $env:TEMP "2Webp-v$Version-package"
Remove-Item $TempPackage -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $TempPackage | Out-Null

$Copied = $false
for ($Attempt = 1; $Attempt -le 5; $Attempt++) {
  try {
    Copy-Item "$OnedirApp\*" $TempPackage -Recurse -Force
    $Copied = $true
    break
  } catch {
    if ($Attempt -eq 5) { throw }
    Start-Sleep -Seconds 2
  }
}
if (-not $Copied) {
  throw "Impossible de préparer le dossier temporaire de distribution."
}
Compress-Archive -Path "$TempPackage\*" -DestinationPath $Archive -Force
Remove-Item $TempPackage -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Installateur Inno Setup..." -ForegroundColor Yellow
$IsccCandidates = @(
  "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
  "$env:ProgramFiles\Inno Setup 6\ISCC.exe"
)
$Iscc = $IsccCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $Iscc) {
  throw "Inno Setup 6 est requis. Installez-le puis relancez ce script."
}
& $Iscc "/DMyAppVersion=$Version" ".\installer\2Webp.iss"
if ($LASTEXITCODE -ne 0) {
  throw "Inno Setup a échoué avec le code $LASTEXITCODE."
}

$Setup = Join-Path $ReleaseDir "2Webp-v$Version-setup.exe"
if (-not (Test-Path $Setup)) {
  throw "L'installateur attendu n'a pas été créé : $Setup"
}

Write-Host "Empreintes SHA-256..." -ForegroundColor Yellow
$Assets = @($PortableTarget, $Archive, $Setup)
$HashLines = foreach ($Asset in $Assets) {
  $Hash = Get-FileHash $Asset -Algorithm SHA256
  "$($Hash.Hash.ToLower())  $([IO.Path]::GetFileName($Asset))"
}
$HashLines | Set-Content (Join-Path $ReleaseDir "SHA256SUMS.txt") -Encoding ascii
Copy-Item .\RELEASE_NOTES.md (Join-Path $ReleaseDir "RELEASE_NOTES.md") -Force

Write-Host ""
Write-Host "Release prête :" -ForegroundColor Green
Get-ChildItem $ReleaseDir | ForEach-Object { Write-Host $_.FullName }
