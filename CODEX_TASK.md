# CODEX_TASK.md — Reprise du projet 2Webp

## Mission permanente

Maintenir et faire évoluer 2Webp sans perdre ses règles produit, son design ou sa sécurité.

## Démarrage obligatoire

1. Lire `AGENTS.md`.
2. Lire `docs/PROJECT_HANDOVER.md`.
3. Lire `docs/DECISIONS.md`.
4. Lire `docs/ROADMAP.md`.
5. Afficher `git status` et la dernière version taguée.
6. Exécuter les tests avant modification.

## Version actuelle

2Webp v0.8.0 est la base stable. Ne pas reconstruire depuis une version antérieure.

## Prochain chantier validé

Créer une branche `feature/custom-mode` et ajouter une troisième carte **Custom** après WordPress et PrestaShop.

Custom doit contenir seulement :

- une saisie de dimension du bord long en pixels ;
- une saisie de qualité WebP.

Contraintes :

- proportions conservées ;
- pas d'agrandissement ;
- valeurs mémorisées ;
- récapitulatif mis à jour ;
- destination inchangée ;
- résultat temporaire inchangé ;
- 22 traductions maintenues ;
- aucune modification visuelle non nécessaire ailleurs.

## Fin de tâche

- tests réussis ;
- contrôle Windows ;
- documentation mise à jour ;
- changelog mis à jour ;
- rapport des fichiers modifiés ;
- aucun tag sans validation humaine finale.
