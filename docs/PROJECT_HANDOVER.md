# Reprise complète du projet 2Webp

## État au 31 juillet 2026

Version stable : **0.8.0**  
Tag attendu : **v0.8.0**  
Plateforme cible : **Windows 10 / 11 x64**  
Auteur : **Jean-Philippe Bloch**

Ce document permet de reprendre le projet sans accès aux conversations historiques.

## 1. Objectif

2Webp convertit des images JPG, JPEG ou PNG en WebP avec une interface simple. Le public n'a pas besoin de connaître les détails de compression, de recadrage ou de redimensionnement.

Le produit vise deux usages initiaux :

- WordPress / Web ;
- PrestaShop.

Les noms des deux usages sont personnalisables, par exemple PrestaShop peut devenir Shopify.

## 2. Parcours actuel

1. L'utilisateur ouvre 2Webp.
2. Il choisit WordPress / Web ou PrestaShop.
3. Il choisit un preset.
4. Le bandeau inférieur résume format, mode, qualité et destination.
5. Il conserve la destination d'origine ou sélectionne un autre dossier.
6. Il glisse les images ou utilise le bouton de sélection.
7. La conversion s'exécute dans un thread.
8. Un écran de réussite remplace temporairement la zone de dépôt pendant cinq secondes.
9. L'écran normal revient avec la destination conservée.

## 3. Règles métier

- originaux conservés ;
- aucun écrasement silencieux ;
- suffixe numérique en cas de doublon ;
- bord long sans agrandissement pour les presets WordPress ;
- contain ou cover pour les presets PrestaShop ;
- profil ICC transmis à Pillow quand il existe ;
- orientation EXIF corrigée avant traitement.

## 4. Interface verrouillée

- colonne gauche sombre ;
- logo exact ;
- Convertir ;
- Languages ;
- Réglages ;
- pas de langue visible avant clic ;
- pas de maximisation ;
- pas de plein écran ;
- cartes de presets à 124 px ;
- bandeau inférieur visible et rassurant ;
- zone de dépôt dominante ;
- notifications intégrées, pas de boîte blanche native.

## 5. Persistance

`%APPDATA%\2Webp\settings.json` : langue, destination, noms de métiers.  
`%APPDATA%\2Webp\presets.json` : huit presets.

Si un dossier personnalisé n'existe plus, l'application revient au dossier d'origine.

## 6. Arborescence utile

- `app.py` : interface, navigation, persistance, orchestration ;
- `core.py` : presets, traitement Pillow, destinations uniques ;
- `translations/` : 22 JSON + index des langues ;
- `assets/brand/` : logo et icônes validés ;
- `assets/icons/` : pictogrammes de bénéfices ;
- `tests/` : tests structuraux et fonctionnels ;
- `installer/` : script Inno Setup ;
- `scripts/` : build release, contrôle de version, publication GitHub ;
- `.github/workflows/` : CI et release Windows ;
- `docs/` : documentation complète.

## 7. Build

Build rapide : `build.ps1`.  
Build complet release : `scripts/build-release.ps1`.

Le build complet doit produire portable EXE, ZIP onedir, installateur et hashes.

## 8. Limites connues

- les binaires ne sont pas signés ;
- SmartScreen peut avertir ;
- les traductions sont structurées et testées mais méritent une relecture native ;
- le test visuel final doit être fait sous Windows ;
- le mode dossier lit les fichiers compatibles présents directement dans le dossier, pas les sous-dossiers ;
- la version portable onefile peut démarrer plus lentement que la version installée.

## 9. Prochaine étape décidée

Ajouter une troisième carte **Custom** après WordPress et PrestaShop.

Custom ne doit présenter que deux réglages :

1. dimension du bord long en pixels ;
2. qualité WebP.

Le reste du parcours ne change pas. La destination, le bandeau, les notifications, le résultat de cinq secondes et les protections restent identiques.

## 10. Validation de la version

Voir `docs/VALIDATION_v0.8.0.md` pour distinguer les tests réellement exécutés des contrôles Windows restant à faire.

## 11. Ordre de reprise recommandé

1. `git status` ;
2. lire `AGENTS.md` ;
3. exécuter les tests ;
4. lancer `py app.py` sous Windows ;
5. vérifier la V0.8.0 visuellement ;
6. créer une branche `feature/custom-mode` ;
7. implémenter Custom sans modifier les deux modes existants.
