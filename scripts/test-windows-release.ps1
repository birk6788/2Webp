param(
  [string]$Repository = "birk6788/2Webp",
  [string]$Ref = "main"
)

$ErrorActionPreference = "Stop"
$Workflow = "release-windows.yml"
$StartedAt = (Get-Date).ToUniversalTime().AddSeconds(-10)

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
  throw "GitHub CLI est requis."
}

& gh auth status *> $null
if ($LASTEXITCODE -ne 0) {
  throw "Connectez GitHub CLI avec : gh auth login"
}

Write-Host "Lancement du test Windows sur $Ref..." -ForegroundColor Cyan
& gh workflow run $Workflow --repo $Repository --ref $Ref
if ($LASTEXITCODE -ne 0) {
  throw "Impossible de lancer le workflow $Workflow."
}

$Run = $null
for ($Attempt = 1; $Attempt -le 20; $Attempt++) {
  Start-Sleep -Seconds 3

  $Json = & gh run list `
    --repo $Repository `
    --workflow $Workflow `
    --event workflow_dispatch `
    --branch $Ref `
    --limit 20 `
    --json databaseId,createdAt,status,conclusion

  if ($LASTEXITCODE -ne 0) {
    throw "Impossible de récupérer la liste des workflows."
  }

  $Runs = @($Json | ConvertFrom-Json)
  $Run = $Runs |
    Where-Object { ([datetime]$_.createdAt).ToUniversalTime() -ge $StartedAt } |
    Sort-Object { [datetime]$_.createdAt } -Descending |
    Select-Object -First 1

  if ($Run) {
    break
  }
}

if (-not $Run) {
  throw "Le workflow a été demandé mais son identifiant n'a pas été retrouvé. Consultez GitHub > Actions."
}

$RunId = [string]$Run.databaseId
Write-Host "Run détecté : $RunId" -ForegroundColor Green
Write-Host "Le run est conservé, même en cas d'échec, afin de préserver les logs." -ForegroundColor DarkGray

& gh run watch $RunId --repo $Repository --exit-status
$WatchExitCode = $LASTEXITCODE

if ($WatchExitCode -ne 0) {
  Write-Host "" 
  Write-Host "=== LOGS DES ÉTAPES EN ÉCHEC ===" -ForegroundColor Red
  & gh run view $RunId --repo $Repository --log-failed
  Write-Host "" 
  Write-Host "Run échoué conservé : $RunId" -ForegroundColor Yellow
  exit $WatchExitCode
}

Write-Host "Build Windows validé : run $RunId" -ForegroundColor Green
