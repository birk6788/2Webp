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

& gh auth status
if ($LASTEXITCODE -ne 0) {
  throw "Connectez GitHub CLI avec : gh auth login"
}

if ((git status --porcelain).Length -gt 0) {
  throw "Le dépôt contient des modifications non commitées."
}

$RemoteUrl = "https://github.com/$Repository.git"
$Remotes = @(git remote)
if ($LASTEXITCODE -ne 0) {
  throw "Impossible de lire les remotes Git."
}

if ($Remotes -contains "origin") {
  git remote set-url origin $RemoteUrl
} else {
  git remote add origin $RemoteUrl
}
if ($LASTEXITCODE -ne 0) {
  throw "Impossible de configurer le remote origin."
}

Write-Host "Synchronisation avec $Repository..." -ForegroundColor Cyan

git fetch origin main:refs/remotes/origin/main --tags
$FetchMainSucceeded = ($LASTEXITCODE -eq 0)

if ($FetchMainSucceeded) {
  $RemoteMain = (git rev-parse refs/remotes/origin/main).Trim()
  if ($LASTEXITCODE -ne 0 -or -not $RemoteMain) {
    throw "Impossible de déterminer la branche main distante."
  }
  git push "--force-with-lease=main:$RemoteMain" origin main
} else {
  # Cas d'un dépôt GitHub réellement vide : aucun main distant à protéger.
  git fetch origin --tags
  git push --force origin main
}
if ($LASTEXITCODE -ne 0) {
  throw "Échec du push de la branche main."
}

git push origin --tags --force
if ($LASTEXITCODE -ne 0) {
  throw "Échec du push des tags."
}

Write-Host "Dépôt publié : https://github.com/$Repository" -ForegroundColor Green
Write-Host "Les tags de version déclenchent la construction Windows et la Release GitHub." -ForegroundColor Green
