# Tests

## Tests automatisés

- syntaxe Python ;
- cohérence de version ;
- traductions ;
- presets ;
- noms de métiers ;
- conversion Pillow ;
- destinations sûres ;
- mise en page structurale ;
- écran de résultat ;
- branding ;
- icône Windows ;
- smoke test Qt.

## Commande complète

```powershell
python -m py_compile app.py core.py
python scripts/check_version.py
Get-ChildItem .\tests\test_*.py | ForEach-Object { python $_.FullName }
python .\tests\smoke_test.py
```

## QA manuelle

- lancement source ;
- lancement onefile ;
- lancement installé ;
- glisser un JPG ;
- glisser plusieurs fichiers ;
- glisser un dossier ;
- tester une destination personnalisée ;
- supprimer ce dossier puis relancer ;
- vérifier le retour au dossier d'origine ;
- vérifier un doublon ;
- vérifier les 5 secondes de confirmation ;
- changer de langue ;
- modifier un preset ;
- restaurer les réglages ;
- contrôler l'icône barre des tâches ;
- contrôler 100 %, 125 %, 150 %.
