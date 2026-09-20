param(
    [switch]$SkipTests
)

$ErrorActionPreference = "Stop"

# Place ce script à la racine du projet 2Webp UI fix.
# Il fonctionne automatiquement sur F:, C:, D:, etc.
$Root = $PSScriptRoot
Set-Location $Root

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  2Webp UI fix - build des 3 versions" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Dossier du projet : $Root" -ForegroundColor DarkGray
Write-Host ""

$RequiredFiles = @(
    ".\app.py",
    ".\core.py",
    ".\VERSION",
    ".\requirements.txt",
    ".\scripts\build-release.ps1"
)

foreach ($File in $RequiredFiles) {
    if (-not (Test-Path $File)) {
        throw "Fichier requis introuvable : $File. Place ce script à la racine du projet 2Webp."
    }
}

$Version = (Get-Content ".\VERSION" -Raw).Trim()
Write-Host "Version détectée : $Version" -ForegroundColor Yellow

if ($Version -ne "0.8.5") {
    Write-Warning "Le fichier VERSION indique '$Version' et non '0.8.5'."
    Write-Warning "Le build utilisera la version réellement indiquée dans le projet."
}

$PythonCommand = $null
if (Get-Command py -ErrorAction SilentlyContinue) {
    $PythonCommand = "py"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $PythonCommand = "python"
} else {
    throw "Python est introuvable. Installe Python 3.14 ou ajoute-le au PATH."
}

$VenvPython = Join-Path $Root ".venv\Scripts\python.exe"

if (-not (Test-Path $VenvPython)) {
    Write-Host "Création de l'environnement virtuel .venv..." -ForegroundColor Yellow

    if ($PythonCommand -eq "py") {
        & py -3.14 -m venv ".venv"
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "Python 3.14 non trouvé via py -3.14, tentative avec Python par défaut."
            & py -m venv ".venv"
        }
    } else {
        & python -m venv ".venv"
    }

    if ($LASTEXITCODE -ne 0 -or -not (Test-Path $VenvPython)) {
        throw "Impossible de créer l'environnement virtuel .venv."
    }
}

Write-Host "Installation des dépendances..." -ForegroundColor Yellow
& $VenvPython -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw "La mise à jour de pip a échoué." }

& $VenvPython -m pip install -r ".\requirements.txt"
if ($LASTEXITCODE -ne 0) { throw "L'installation des dépendances a échoué." }

# Le script officiel appelle 'python'.
# On place donc temporairement le Python du venv en tête du PATH.
$OldPath = $env:PATH
$env:PATH = "$(Split-Path $VenvPython -Parent);$OldPath"

try {
    $Arguments = @(
        "-ExecutionPolicy", "Bypass",
        "-File", ".\scripts\build-release.ps1"
    )

    if ($SkipTests) {
        $Arguments += "-SkipTests"
    }

    Write-Host ""
    Write-Host "Lancement du build complet..." -ForegroundColor Green
    & powershell @Arguments

    if ($LASTEXITCODE -ne 0) {
        throw "Le build de release a échoué avec le code $LASTEXITCODE."
    }
}
finally {
    $env:PATH = $OldPath
}

$ReleaseDir = Join-Path $Root "release"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  BUILD TERMINÉ" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Les 3 versions sont dans :" -ForegroundColor Cyan
Write-Host $ReleaseDir -ForegroundColor White
Write-Host ""

$Expected = @(
    "2Webp-v$Version-portable.exe",
    "2Webp-v$Version-windows-x64.zip",
    "2Webp-v$Version-setup.exe",
    "SHA256SUMS.txt"
)

foreach ($Name in $Expected) {
    $Path = Join-Path $ReleaseDir $Name
    if (Test-Path $Path) {
        $SizeMb = [math]::Round((Get-Item $Path).Length / 1MB, 2)
        Write-Host "OK  $Name  ($SizeMb Mo)" -ForegroundColor Green
    } else {
        Write-Warning "Fichier attendu absent : $Name"
    }
}

Write-Host ""
Write-Host "Appuie sur Entrée pour ouvrir le dossier release..."
[void](Read-Host)
Start-Process explorer.exe $ReleaseDir
