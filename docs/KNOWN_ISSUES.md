# Problèmes et limites connus

## Binaire non signé

Windows SmartScreen peut afficher un avertissement. Une signature de code est nécessaire pour supprimer progressivement ce problème de réputation.

## Validation visuelle

Les tests de structure ne remplacent pas un contrôle réel sous Windows, notamment avec les mises à l'échelle 125 % et 150 %.

## Onefile

Le premier lancement de l'exécutable portable unique peut être plus lent, car PyInstaller extrait temporairement ses composants.

## Dossiers

Le dépôt d'un dossier traite les images compatibles directement présentes dans ce dossier. Les sous-dossiers ne sont pas parcourus récursivement dans la v0.8.0.

## Traductions

Les traductions sont structurellement validées, mais une relecture par locuteurs natifs reste souhaitable.

## Profils colorimétriques

Le profil ICC est transmis quand Pillow le fournit. La chaîne web cible sRGB, mais l'application ne convertit pas explicitement tous les profils vers sRGB dans la v0.8.0.
