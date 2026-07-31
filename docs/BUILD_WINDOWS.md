# Build Windows

## Prérequis

- Windows 10 ou 11 x64 ;
- Python 3.13 ;
- pip ;
- Inno Setup 6 pour l'installateur complet.

## Installation

```powershell
py -m pip install -r requirements.txt
```

## Build développeur

```powershell
powershell -ExecutionPolicy Bypass -File .\build.ps1
```

## Build complet de release

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-release.ps1
```

Le script :

1. vérifie la version ;
2. exécute les tests ;
3. construit la version `onedir` ;
4. construit l'exécutable `onefile` ;
5. prépare l'archive ZIP ;
6. compile l'installateur si `ISCC.exe` est disponible ;
7. calcule les SHA-256.

## Résultats

```text
release/2Webp-v0.8.0-portable.exe
release/2Webp-v0.8.0-windows-x64.zip
release/2Webp-v0.8.0-setup.exe
release/SHA256SUMS.txt
```

## OneDrive

OneDrive peut verrouiller temporairement `base_library.zip`. Les archives sont donc préparées dans `%TEMP%` avant d'être copiées dans `release`.
