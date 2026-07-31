# Architecture

## Vue générale

2Webp est volontairement monolithique côté interface, avec un noyau de traitement séparé.

```text
app.py
  ├─ interface PySide6
  ├─ traduction
  ├─ persistance utilisateur
  ├─ thread de conversion
  └─ orchestration

core.py
  ├─ modèles Preset et BusinessGroup
  ├─ presets par défaut
  ├─ collecte des fichiers
  ├─ redimensionnement
  ├─ contain / cover
  ├─ destination unique
  └─ conversion Pillow
```

## Flux de conversion

1. `MainWindow._receive_paths()` reçoit les chemins.
2. `iter_image_files()` filtre JPG, JPEG et PNG.
3. Le preset actif et la destination sont figés pour le batch.
4. Un `ConversionWorker` s'exécute dans un `QThread`.
5. `convert_one()` ouvre, corrige l'orientation, transforme et enregistre.
6. Le worker retourne le chemin de sortie et les poids avant/après.
7. L'interface affiche la progression puis le résultat temporaire.

## Modèles

### Preset

- `key` ;
- `title` ;
- `title_custom` ;
- `width` ;
- `height` ;
- `quality` ;
- `mode`.

Modes :

- `long_edge` ;
- `contain` ;
- `cover`.

### BusinessGroup

- `key` ;
- `title` ;
- `title_custom`.

## Ressources

PyInstaller embarque :

- `assets/` ;
- `translations/`.

`resource_dir()` résout les chemins en source et en bundle PyInstaller.

## Persistance

Les JSON utilisateur sont séparés du code afin qu'une mise à jour de l'application ne détruise pas les réglages.

## Pourquoi pas de base de données

Le volume de données est faible, local et strictement utilisateur. Deux fichiers JSON suffisent et gardent le projet auditable.
