# 2Webp

![2Webp](assets/brand/2Webp-logo-exact.png)

Convertisseur WebP libre pour Windows, conçu pour transformer rapidement des images JPG, JPEG et PNG en fichiers WebP prêts pour le web.

La version stable documentée dans ce dépôt est **2Webp v0.8.0**.

## Pourquoi 2Webp

2Webp vise un usage simple et professionnel : sélectionner un contexte, choisir un preset, déposer les images, récupérer les WebP. Aucun réglage technique n'est imposé à l'utilisateur, mais les huit presets restent entièrement personnalisables.

Principes non négociables :

- traitement 100 % local ;
- aucune connexion réseau ;
- aucune télémétrie ;
- aucune publicité ;
- originaux toujours conservés ;
- aucun écrasement silencieux ;
- interface Windows sombre, compacte et lisible ;
- 22 langues européennes en alphabet latin.

## Fonctionnalités v0.8.0

- entrées JPG, JPEG et PNG ;
- sortie WebP ;
- glisser-déposer de fichiers ou d'un dossier ;
- destination par défaut à côté des originaux ;
- destination personnalisée mémorisée tant qu'elle existe ;
- renommage automatique en cas de doublon (`image-2.webp`, `image-3.webp`, etc.) ;
- quatre presets WordPress / Web ;
- quatre presets PrestaShop ;
- noms des deux métiers personnalisables ;
- dimensions, qualité et mode des huit presets modifiables ;
- écran temporaire de réussite après conversion ;
- récapitulatif avant export : format, mode, qualité et destination ;
- maximisation et plein écran désactivés pour préserver la mise en page ;
- icône Windows multirésolution.

## Presets fournis

### WordPress / Web

| Preset | Dimension | Qualité | Mode |
|---|---:|---:|---|
| Petit bloc | 800 px | 78 | Bord long |
| Web / devis | 1600 px | 80 | Bord long |
| Page silo | 1920 px | 82 | Bord long |
| Galerie HD | 2560 px | 85 | Bord long |

Le mode Bord long ne redimensionne jamais une image déjà plus petite.

### PrestaShop

| Preset | Dimensions | Qualité | Mode |
|---|---:|---:|---|
| Produit carré | 1200 × 1200 px | 84 | Adapter au cadre |
| Produit carré HD | 2000 × 2000 px | 85 | Adapter au cadre |
| Bannière catégorie | 1920 × 600 px | 82 | Recadrer pour remplir |
| Bannière accueil | 1920 × 800 px | 82 | Recadrer pour remplir |

## Installation depuis les sources

Prérequis : Windows 10 ou 11 et Python 3.13 recommandé.

```powershell
py -m pip install -r requirements.txt
py app.py
```

Ou utiliser :

```text
LANCER_2WEBP.bat
```

## Build développeur

```powershell
powershell -ExecutionPolicy Bypass -File .\build.ps1
```

Le build développeur produit :

- `dist\2Webp\2Webp.exe` ;
- `release\2Webp-v0.8.0-windows-x64.zip` ;
- l'empreinte SHA-256 correspondante.

## Build de release complet

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-release.ps1
```

Le build de release produit :

- un exécutable portable unique ;
- une archive ZIP de la version `onedir` ;
- un installateur Windows Inno Setup ;
- un fichier `SHA256SUMS.txt`.

Voir [docs/BUILD_WINDOWS.md](docs/BUILD_WINDOWS.md) et [docs/INSTALLER.md](docs/INSTALLER.md).

## Données locales

Les préférences sont stockées dans :

```text
%APPDATA%\2Webp
```

Fichiers :

- `presets.json` ;
- `settings.json`.

Aucune donnée n'est envoyée ailleurs.

## Dépôt et reprise de contexte

Toute personne ou agent qui reprend le projet doit lire, dans cet ordre :

1. [AGENTS.md](AGENTS.md) ;
2. [docs/PROJECT_HANDOVER.md](docs/PROJECT_HANDOVER.md) ;
3. [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) ;
4. [docs/DECISIONS.md](docs/DECISIONS.md) ;
5. [docs/ROADMAP.md](docs/ROADMAP.md) ;
6. [CHANGELOG.md](CHANGELOG.md).

## Prochaine évolution prévue

La prochaine évolution fonctionnelle est un troisième mode **Custom**, placé après WordPress et PrestaShop. Il doit proposer uniquement :

- une saisie directe de la dimension du bord long en pixels ;
- une saisie directe de la qualité WebP.

Le reste de l'application ne change pas. Détails dans [docs/ROADMAP.md](docs/ROADMAP.md).

## Sécurité et confidentialité

Voir [SECURITY.md](SECURITY.md) et [PRIVACY.md](PRIVACY.md).

## Licence

MIT — Copyright © 2026 Jean-Philippe Bloch.
