# Traductions

## Langues

FR, EN, DE, IT, ES, PT, NL, DA, SV, FI, ET, LV, LT, PL, CS, SK, SL, HR, HU, RO, GA, MT.

## Structure

- `translations/languages.json` : code et nom natif ;
- `translations/<code>.json` : textes de l'interface.

## Contraintes

- UTF-8 ;
- mêmes clés dans les 22 fichiers ;
- aucun champ vide ;
- placeholders identiques ;
- noms personnalisés non retraduits ;
- `Languages` reste écrit en anglais.

## Test

```powershell
python tests/test_translations.py
```

Le test vérifie le nombre de fichiers, les clés et les placeholders.
