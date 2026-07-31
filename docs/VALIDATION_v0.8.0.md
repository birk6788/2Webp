# Validation réelle de la v0.8.0

Date : 31 juillet 2026

## Validé dans l'environnement de préparation

- cohérence de version `0.8.0` ;
- syntaxe de `app.py`, `core.py` et `scripts/check_version.py` ;
- 22 traductions et 87 clés cohérentes ;
- presets par défaut ;
- titres personnalisables ;
- conversion Pillow ;
- destinations sûres et renommage des doublons ;
- structure de la page Convertir ;
- structure de la page Réglages ;
- branding 2Webp sans ancienne référence ;
- icône ICO multirésolution ;
- dépôt Git propre ;
- tag annoté ;
- pipeline de release Windows documenté.

## Non exécuté dans cet environnement

- smoke test Qt, car PySide6 n'est pas installé dans le runtime de préparation ;
- compilation Windows PyInstaller ;
- compilation Inno Setup ;
- test visuel Windows à 100 %, 125 % et 150 % ;
- signature de code, aucun certificat n'étant configuré.

Ces contrôles sont exécutés par GitHub Actions ou sur le poste Windows avant publication finale des binaires.
