# AGENTS.md — Règles permanentes du projet 2Webp

Ce fichier doit être lu avant toute modification par un humain, Codex, Claude Code ou un autre agent.

## 1. Source de vérité

Le dépôt Git est la source de vérité. Ne jamais reconstruire le projet à partir d'une ancienne archive si le dépôt contient une version plus récente.

La version stable actuelle est définie dans `VERSION` et doit correspondre à :

- `APP_VERSION` dans `app.py` ;
- `$Version` dans `build.ps1` ;
- la version de release ;
- le tag Git.

Exécuter `python scripts/check_version.py` avant chaque release.

## 2. Mission du logiciel

2Webp est un convertisseur WebP Windows simple, local et auditable.

Entrées :

- JPG ;
- JPEG ;
- PNG.

Sortie :

- WebP uniquement ;
- destination choisie par l'utilisateur ;
- originaux conservés ;
- aucun écrasement silencieux.

## 3. Contraintes absolues

Interdit sans décision explicite documentée :

- connexion réseau ;
- télémétrie ;
- analytics ;
- compte utilisateur ;
- publicité ;
- suppression d'originaux ;
- écrasement d'un fichier existant ;
- popup Windows blanche pour les notifications courantes ;
- maximisation ou plein écran ;
- reconstruction approximative du logo ;
- dépendance lourde non justifiée.

## 4. Stack

- Python 3.13 recommandé ;
- PySide6 ;
- Pillow ;
- PyInstaller ;
- Inno Setup pour l'installateur Windows ;
- GitHub Actions pour les builds de release.

## 5. Design à préserver

- interface sombre ;
- accent orange ;
- colonne gauche fixe ;
- trois entrées : Convertir, Languages, Réglages ;
- Languages reste toujours écrit en anglais ;
- pas de langue affichée en permanence ;
- fenêtre compacte ;
- pas de scroll horizontal ;
- cartes de presets de 124 px de hauteur ;
- valeurs de dimensions visuellement importantes ;
- zone de dépôt dominante ;
- barre de destination centrée et limitée ;
- bandeau inférieur comme récapitulatif avant export.

Les assets validés se trouvent dans `assets/brand/`. Ne pas les redessiner.

## 6. Traductions

- 22 langues ;
- un JSON UTF-8 par langue ;
- mêmes clés partout ;
- aucun champ vide ;
- placeholders cohérents ;
- `Languages` n'est pas traduit ;
- les noms personnalisés par l'utilisateur restent inchangés lors d'un changement de langue.

## 7. Persistance

Les données utilisateur restent hors du dépôt :

```text
%APPDATA%\2Webp\presets.json
%APPDATA%\2Webp\settings.json
```

Ne jamais versionner ces fichiers.

## 8. Méthode de travail

1. Lire `docs/PROJECT_HANDOVER.md`.
2. Vérifier l'état Git.
3. Créer une branche dédiée.
4. Faire une modification ciblée.
5. Ajouter ou adapter les tests.
6. Exécuter tous les tests.
7. Contrôler visuellement Windows à 100 %, 125 % et 150 %.
8. Mettre à jour `CHANGELOG.md` et la documentation concernée.
9. Ne taguer qu'une version testée.

## 9. Tests obligatoires

```powershell
python -m py_compile app.py core.py
python scripts/check_version.py
python tests/test_translations.py
python tests/test_presets.py
python tests/test_preset_ui.py
python tests/test_business_groups.py
python tests/test_conversion.py
python tests/test_conversion_ui.py
python tests/test_settings_ui.py
python tests/smoke_test.py
python tests/test_clean_branding.py
python tests/test_windows_icon.py
```

## 10. Release

Une release stable doit contenir :

- exécutable portable unique ;
- archive ZIP `onedir` ;
- installateur Windows ;
- `SHA256SUMS.txt` ;
- notes de version ;
- source taguée.

Les binaires non signés peuvent déclencher SmartScreen. Ne jamais prétendre qu'ils sont signés s'ils ne le sont pas.

## 11. Prochaine fonctionnalité verrouillée

Le prochain chantier est **Custom** :

- troisième carte métier après WordPress et PrestaShop ;
- deux champs seulement : dimension du bord long en px et qualité WebP ;
- aucun changement au reste du parcours de conversion ;
- la destination, le résultat temporaire, les traductions et le récapitulatif restent identiques.

Voir `docs/ROADMAP.md`.
