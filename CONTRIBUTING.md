# Contribuer à 2Webp

## Avant de commencer

Lire `AGENTS.md` et `docs/PROJECT_HANDOVER.md`.

## Branches

- `main` : version stable ;
- `feature/...` : nouvelle fonctionnalité ;
- `fix/...` : correction ;
- `docs/...` : documentation.

## Règles

- une modification fonctionnelle par pull request ;
- tests obligatoires ;
- aucune dépendance ajoutée sans justification ;
- aucune fonction réseau ;
- pas de modification du branding sans validation ;
- mise à jour de `CHANGELOG.md` pour tout changement visible.

## Validation

```powershell
python -m py_compile app.py core.py
python scripts/check_version.py
python tests/test_translations.py
python tests/test_presets.py
python tests/test_conversion.py
python tests/smoke_test.py
```

Les modifications d'interface doivent aussi être vérifiées sous Windows à 100 %, 125 % et 150 % de mise à l'échelle.
