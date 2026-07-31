param(
  [string]$Repository = "birk6788/2Webp",
  [ValidateSet("public", "private")]
  [string]$Visibility = "public"
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
  throw "Le dépôt contient des modifications non commitée(s). Committez-les avant publication."
}

$RemoteExists = $false
gh repo view $Repository *> $null
if ($LASTEXITCODE -eq 0) {
  $RemoteExists = $true
}

if (-not $RemoteExists) {
  Write-Host "Création du dépôt $Repository..." -ForegroundColor Cyan
  gh repo create $Repository `
    --$Visibility `
    --source . `
    --remote origin `
    --description "Convertisseur WebP local, libre et multilingue pour Windows"
  if ($LASTEXITCODE -ne 0) { throw "Échec de création du dépôt GitHub." }
} elseif (-not (git remote get-url origin 2>$null)) {
  git remote add origin "https://github.com/$Repository.git"
}

git push -u origin main
if ($LASTEXITCODE -ne 0) { throw "Échec du push de main." }

git push origin --tags
if ($LASTEXITCODE -ne 0) { throw "Échec du push des tags." }

Write-Host "Dépôt publié : https://github.com/$Repository" -ForegroundColor Green
Write-Host "Le tag v$(Get-Content .\VERSION -Raw) déclenchera la release Windows." -ForegroundColor Green
