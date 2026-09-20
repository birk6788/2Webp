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

## Version en cours

2Webp **v0.8.5** est la version candidate développée sur `feature/v0.8.5-custom`.
La dernière version taguée reste v0.8.0 tant que la validation Windows n'est pas terminée.

## Fonctionnalité livrée dans la candidate

Une troisième carte **Custom** est placée après WordPress / Web et PrestaShop.

Custom contient seulement :

- une saisie de dimension du bord long en pixels ;
- une saisie de qualité WebP sur 100.

Contraintes respectées :

- proportions conservées ;
- pas d'agrandissement ;
- valeurs mémorisées ;
- récapitulatif mis à jour immédiatement ;
- destination inchangée ;
- résultat temporaire inchangé ;
- 22 traductions maintenues ;
- hauteurs, espacements, hero, cartes, zone de dépôt et footer conservés.

## Fin de tâche v0.8.5

- tests automatiques réussis ;
- contrôle visuel Windows à 100 %, 125 % et 150 % ;
- build Windows vert ;
- validation humaine du mode Custom ;
- merge sur `main` ;
- tag seulement après validation humaine finale.
