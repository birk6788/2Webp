# Administration du dépôt GitHub

Dépôt prévu : `birk6788/2Webp`  
Visibilité prévue : publique.

## Première publication

Depuis la racine du dépôt local :

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\publish-github.ps1
```

Le script utilise GitHub CLI `gh`, crée le dépôt s'il n'existe pas, pousse `main` et les tags.

## Protection recommandée

- branche `main` protégée ;
- pull request obligatoire ;
- workflow CI obligatoire ;
- suppression des branches après merge ;
- Dependabot activé ;
- GitHub Actions avec permissions minimales.

## Release

Le push d'un tag `vX.Y.Z` déclenche `.github/workflows/release-windows.yml`.
