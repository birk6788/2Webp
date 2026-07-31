param(
  [string]$Repository = "birk6788/2Webp"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  throw "Git est requis."
}
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
  throw "GitHub CLI est requis : https://cli.github.com/"
}

gh auth status
if ($LASTEXITCODE -ne 0) {
  throw "Connectez GitHub CLI avec : gh auth login"
}

if ((git status --porcelain).Length -gt 0) {
  throw "Le dépôt contient des modifications non commitées."
}

$RemoteUrl = "https://github.com/$Repository.git"
$ExistingOrigin = git remote get-url origin 2>$null
if ($LASTEXITCODE -eq 0) {
  git remote set-url origin $RemoteUrl
} else {
  git remote add origin $RemoteUrl
}

Write-Host "Synchronisation avec $Repository..." -ForegroundColor Cyan
git fetch origin main --tags 2>$null

# Le dépôt GitHub vient d'être initialisé avec un README. Le dépôt local est
# l'historique de référence complet ; le remplacement de main est volontaire.
git push --force-with-lease origin main
if ($LASTEXITCODE -ne 0) {
  throw "Échec du push de la branche main."
}

git push origin --tags --force
if ($LASTEXITCODE -ne 0) {
  throw "Échec du push des tags."
}

Write-Host "Dépôt publié : https://github.com/$Repository" -ForegroundColor Green
Write-Host "Le tag v0.8.0 déclenche la construction Windows et la Release GitHub." -ForegroundColor Green
