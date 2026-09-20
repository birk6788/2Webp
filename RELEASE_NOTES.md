# 2Webp v0.8.6 — Notes de version

2Webp v0.8.6 corrige un blocage sur les conversions successives et nomme
désormais les fichiers produits d'après leur taille réelle.

## Correction

Après une première conversion, déposer une nouvelle série ne déclenchait
plus rien : il fallait fermer et rouvrir l'application. Le thread de
conversion était détruit à la fin du lot sans que sa référence soit libérée,
et le contrôle qui vérifie si une conversion est en cours échouait
silencieusement. Les lots s'enchaînent maintenant sans redémarrage.

## Nouveau

Le nom du fichier produit porte le bord long réel :

- `photo.jpg` en preset 1600 px devient `photo_1600.webp` ;
- `produit.jpg` en 1200 × 1200 Adapter au cadre devient `produit_1200.webp` ;
- `banniere.jpg` en 1920 × 600 Recadrer pour remplir devient `banniere_1920.webp`.

La valeur est celle du fichier obtenu, pas celle du preset : une source de
1200 px traitée avec le preset 1600 px n'étant jamais agrandie, elle sort en
`photo_1200.webp`.

Deux tailles différentes de la même source cohabitent donc sans se gêner. Le
suffixe numérique `-2`, `-3` ne sert plus qu'aux conversions strictement
identiques.

Sur un dossier déjà traité avec une version antérieure, les anciens
`photo.webp` subsistent à côté des nouveaux `photo_1600.webp`. Aucun fichier
n'est écrasé.

## Inchangé

Interface, presets, workflows, destination, écran de résultat, 22 langues :
rien n'a bougé. Aucune connexion réseau, aucune télémétrie, originaux
toujours conservés.

## Fichiers Windows

- `2Webp-v0.8.6-portable.exe` ;
- `2Webp-v0.8.6-windows-x64.zip` ;
- `2Webp-v0.8.6-setup.exe` ;
- `SHA256SUMS.txt`.

## Sécurité

Les binaires restent non signés tant qu'aucun certificat de signature de
code n'est configuré. Windows SmartScreen peut afficher un avertissement au
premier lancement.
