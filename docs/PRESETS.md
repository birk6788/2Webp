# Fonctionnement des presets

## WordPress / Web

Les quatre presets utilisent `long_edge`.

- le rapport largeur/hauteur est conservé ;
- aucune image plus petite n'est agrandie ;
- la valeur correspond au bord le plus long ;
- le format de sortie est WebP.

## PrestaShop

### Adapter au cadre (`contain`)

L'image entière est visible dans un canevas fixe. Les zones restantes sont blanches ou transparentes selon l'image.

### Recadrer pour remplir (`cover`)

L'image remplit entièrement le format cible. Un recadrage centré peut avoir lieu.

## Réglages utilisateur

Chaque preset peut modifier :

- nom ;
- largeur ;
- hauteur ;
- qualité ;
- mode.

La roulette ne doit pas modifier les valeurs par accident. Les champs numériques sont saisis directement.

## Persistance

Les presets sont enregistrés dans `%APPDATA%\2Webp\presets.json`.

## Future carte Custom

Custom utilisera une valeur unique de bord long et une qualité. Il ne doit pas ajouter de recadrage ou d'autres options dans la première version.
