@echo off
setlocal
cd /d "%~dp0"
echo.
echo Lancement du build des 3 versions de 2Webp UI fix...
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0BUILD_3_VERSIONS_UI_FIX.ps1"
if errorlevel 1 (
    echo.
    echo ERREUR : le build a echoue.
    pause
)
endlocal
