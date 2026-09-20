# 2Webp v0.8.5 — Notes de version

2Webp v0.8.5 ajoute le mode **Custom** au même niveau que WordPress / Web et PrestaShop.

## Nouveau

- saisie directe du bord long en pixels ;
- saisie directe de la qualité WebP ;
- valeurs mémorisées entre deux ouvertures ;
- valeurs par défaut : 1800 px et qualité 82 ;
- aucune modification du choix de destination, du glisser-déposer ou du résultat de conversion ;
- traductions Custom ajoutées aux 22 langues.

## Fichiers Windows attendus

- `2Webp-v0.8.5-portable.exe` ;
- `2Webp-v0.8.5-windows-x64.zip` ;
- `2Webp-v0.8.5-setup.exe` ;
- `SHA256SUMS.txt`.

## Sécurité

Les binaires restent non signés tant qu’aucun certificat de signature de code n’est configuré. Windows SmartScreen peut afficher un avertissement au premier lancement.

- Splash de démarrage 2Webp sur la version portable onefile.
- Correction des chemins absolus PyInstaller avec `--specpath`.
