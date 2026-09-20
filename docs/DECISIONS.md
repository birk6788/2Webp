# Décisions de conception

## D-001 — Traitement 100 % local

Aucun réseau, aucune télémétrie. Motif : confidentialité, simplicité, auditabilité.

## D-002 — PySide6 + Pillow

PySide6 fournit l'interface Windows ; Pillow fournit un pipeline d'image fiable et lisible.

## D-003 — Originaux intacts

L'application ne supprime jamais les sources et n'écrase jamais un WebP existant.

## D-004 — Presets métiers

Le produit commence par WordPress / Web et PrestaShop. Les noms sont personnalisables afin de couvrir Shopify ou d'autres usages sans changer le code.

## D-005 — Traductions JSON

Un fichier par langue, contrôlé par tests. Motif : simplicité de contribution et audit.

## D-006 — Pas de maximisation

La mise en page est conçue comme un outil compact. Le plein écran dégrade l'équilibre visuel.

## D-007 — Notifications intégrées

Les messages de succès et d'erreur restent dans l'interface sombre.

## D-008 — Trois formats de distribution

- onefile pour l'usage portable immédiat ;
- ZIP onedir pour la fiabilité et l'audit ;
- installateur pour le grand public.

## D-009 — Branding exact

Les assets validés sont utilisés tels quels. Aucun logo reconstruit par code.

## D-010 — Custom minimal

Le futur mode Custom aura seulement dimension du bord long et qualité. Le but est de rester compréhensible et de ne pas transformer 2Webp en éditeur d'image complexe.

## D-011 — Suffixe de nom libre plutôt que liste de formats

Validation produit du 20 septembre 2026, demandée explicitement comme le
prévoit `AGENTS.md` §11.

Le suffixe des fichiers produits est un champ de saisie libre dans les
Réglages, pas une liste déroulante de formats figés. Motif : c'est un champ
comme les noms de métiers juste au-dessus, donc cohérent avec ce qui existe,
et une liste fermée n'aurait jamais couvert les conventions de nommage
réelles.

Le champ porte le suffixe seul, pas un modèle complet : le nom d'origine
reste devant par construction. Un modèle complet aurait permis de supprimer
`{nom}` et de replier tout un lot sur un seul nom de sortie.
