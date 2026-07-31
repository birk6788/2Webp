# 2Webp

Convertisseur WebP libre pour Windows, pensé pour les usages WordPress et PrestaShop.

## Principes

- traitement 100 % local ;
- aucune connexion réseau ;
- aucune télémétrie ;
- JPG, JPEG et PNG en entrée ;
- WebP dans le même dossier ;
- fichiers originaux conservés ;
- 8 presets entièrement modifiables ;
- 22 langues européennes en alphabet latin.

## Lancer depuis les sources

```powershell
py -m pip install -r requirements.txt
py app.py
```

## Compiler

```powershell
powershell -ExecutionPolicy Bypass -File .\build.ps1
```

Le dossier `release` contient le ZIP distribuable et son empreinte SHA-256.

## Données locales

Les préférences sont conservées dans `%APPDATA%\2Webp` :

- `presets.json`
- `settings.json`

## Licence

MIT. Le code peut être lu, modifié et redistribué selon les termes du fichier `LICENSE`.

## Destination

Par défaut, les WebP sont enregistrés à côté des originaux. Une destination personnalisée peut être choisie et reste mémorisée tant que le dossier existe. Les fichiers existants ne sont jamais écrasés silencieusement.
