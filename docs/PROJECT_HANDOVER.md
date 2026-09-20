# Reprise complète du projet 2Webp

## État au 20 septembre 2026

Version en production : **0.8.5** (build Windows du 5 août 2026)
Dernière version taguée : **v0.8.0**
Branche de travail : **main**
Plateforme cible : **Windows 10 / 11 x64**
Auteur : **Jean-Philippe Bloch**

Ce document permet de reprendre le projet sans accès aux conversations historiques.

## 1. Objectif

2Webp convertit des images JPG, JPEG ou PNG en WebP avec une interface simple. Le public n'a pas besoin de connaître les détails de compression, de recadrage ou de redimensionnement.

Le produit propose trois workflows :

- WordPress / Web ;
- PrestaShop ;
- Custom.

Les noms WordPress / Web et PrestaShop sont personnalisables. Custom reste un workflow fixe et volontairement minimal.

## 2. Parcours actuel

1. L'utilisateur ouvre 2Webp.
2. Il choisit WordPress / Web, PrestaShop ou Custom.
3. WordPress / PrestaShop affichent quatre presets ; Custom affiche deux cartes directes de 124 px.
4. Custom demande uniquement un bord long en pixels et une qualité WebP sur 100.
5. Le bandeau inférieur résume format, mode, qualité et destination.
6. L'utilisateur conserve la destination d'origine ou sélectionne un autre dossier.
7. Il glisse les images ou utilise le bouton de sélection.
8. La conversion s'exécute dans un thread.
9. Un écran de réussite remplace temporairement la zone de dépôt pendant cinq secondes.
10. L'écran normal revient avec la destination et les valeurs Custom conservées.

## 3. Règles métier

- originaux conservés ;
- aucun écrasement silencieux ;
- nom de sortie suffixé selon le réglage de l'utilisateur, `_{long}` par
  défaut : `photo_1600.webp` ; un suffixe vide conserve `photo.webp` ;
- le nom d'origine précède toujours le suffixe ;
- suffixe numérique en cas de doublon strict : `photo_1600-2.webp` ;
- bord long sans agrandissement pour WordPress et Custom ;
- contain ou cover pour PrestaShop ;
- profil ICC transmis à Pillow quand il existe ;
- orientation EXIF corrigée avant traitement ;
- valeurs Custom bornées à 100–10 000 px et qualité 1–100.

## 4. Interface verrouillée

- colonne gauche sombre ;
- logo exact ;
- Convertir ;
- Languages ;
- Réglages ;
- pas de langue visible avant clic ;
- pas de maximisation ;
- pas de plein écran ;
- cartes de presets et cartes Custom à 124 px ;
- trois cartes de workflow sur la même ligne ;
- bloc éditorial compact inchangé ;
- espacement de 18 px avant la zone de dépôt ;
- bandeau inférieur fixe de 50 px ;
- zone de dépôt dominante de 258 à 286 px ;
- notifications intégrées, pas de boîte blanche native.

## 5. Persistance

`%APPDATA%\2Webp\settings.json` : langue, destination, noms de métiers,
`custom_export` et `name_suffix`.
`%APPDATA%\2Webp\presets.json` : huit presets WordPress / PrestaShop.

Valeurs Custom par défaut : 1800 px et qualité 82. Si un dossier personnalisé n'existe plus, l'application revient au dossier d'origine.

## 6. Arborescence utile

- `app.py` : interface, navigation, persistance, orchestration ;
- `core.py` : presets, Custom, traitement Pillow, destinations uniques ;
- `translations/` : 22 JSON, index des langues et `custom.json` ;
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

## 9. État de la v0.8.5

La v0.8.5 a été construite le 5 août 2026 et installée en production
(`%LOCALAPPDATA%\Programs\2Webp`). Le code correspondant est sur `main`.
Les douze tests automatisés passent sur Python 3.14.

Reste administratif : tag Git `v0.8.5` et release GitHub associée.

## 10. Ordre de reprise

1. `git status` dans le dépôt ;
2. lire `AGENTS.md` ;
3. exécuter les douze tests ;
4. créer une branche dédiée avant toute modification.

Voir `docs/VALIDATION_v0.8.0.md` pour l'historique de validation de la base précédente.
