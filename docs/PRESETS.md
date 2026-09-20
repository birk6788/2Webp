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

## Nom des fichiers produits — v0.8.6

Le nom de sortie reprend le nom de la source et y ajoute le bord long
réellement produit :

- `photo.jpg` en preset 1600 px → `photo_1600.webp` ;
- `produit.jpg` en 1200 × 1200 Adapter au cadre → `produit_1200.webp` ;
- `banniere.jpg` en 1920 × 600 Recadrer pour remplir → `banniere_1920.webp`.

La valeur est celle du fichier obtenu, pas celle du preset. Une source de
1200 px traitée avec le preset 1600 px n'étant jamais agrandie, elle sort en
`photo_1200.webp`.

Deux tailles différentes de la même source cohabitent donc sans se gêner. Le
suffixe numérique `-2`, `-3` ne sert plus qu'aux conversions strictement
identiques.

### Suffixe modifiable

Le suffixe se règle dans **Réglages**, carte « Nom des fichiers produits ».
C'est un champ libre : on y tape ce qu'on veut, avec ou sans balises.

| Balise | Valeur |
|---|---|
| `{long}` | bord long réel du fichier produit |
| `{width}` | largeur réelle |
| `{height}` | hauteur réelle |
| `{quality}` | qualité WebP appliquée |

Les équivalents français `{bordlong}`, `{largeur}`, `{hauteur}` et
`{qualite}` sont acceptés. Une balise inconnue reste affichée telle quelle
dans la ligne d'exemple, ce qui la rend visible avant conversion.

Exemples : `_{long}` donne `photo_1600.webp`, `-web` donne
`photo-web.webp`, `_{width}x{height}` donne `photo_1600x1067.webp`.

Un suffixe vide est une valeur valide : le fichier produit reprend
exactement le nom de la source, `photo.webp`. Le nom d'origine précède
toujours le suffixe, donc un lot ne peut jamais se replier sur un seul nom.

Les caractères refusés par Windows dans un nom de fichier — `\ / : * ? " < >
|` — sont retirés à l'enregistrement. Le suffixe est stocké dans
`settings.json` sous `name_suffix`, et « Restaurer les réglages » le remet à
`_{long}`.

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
