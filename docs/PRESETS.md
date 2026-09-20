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

## Custom — v0.8.5

Custom utilise toujours `long_edge` et ne propose que deux valeurs directes :

- bord long : 100 à 10 000 px, valeur par défaut 1800 px ;
- qualité WebP : 1 à 100, valeur par défaut 82.

Les proportions sont conservées et les petites images ne sont jamais agrandies. Custom n'ajoute ni hauteur, ni contain, ni cover, ni recadrage.

## Réglages utilisateur

Chaque preset WordPress ou PrestaShop peut modifier :

- nom ;
- largeur ;
- hauteur ;
- qualité ;
- mode.

La roulette ne doit pas modifier les valeurs par accident. Les champs numériques sont saisis directement.

## Persistance

- les huit presets sont enregistrés dans `%APPDATA%\2Webp\presets.json` ;
- les valeurs Custom sont enregistrées dans `%APPDATA%\2Webp\settings.json`, sous `custom_export`.
