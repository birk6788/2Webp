# Changelog

## 0.8.0

- En-tête compacté sans réduire la hauteur des cartes.
- Titre d’usage agrandi, remonté et rapproché des presets.
- Valeurs 800 px, 1600 px, 1920 px et 2560 px renforcées.
- Mention Bord long / Adapter au cadre / Recadrer pour remplir maintenue.
- Zone de dépôt agrandie et typographie renforcée.
- Barre de destination centrée et limitée à environ 48 % de la zone.
- Bouton Modifier la destination conservé.
- Bandeau inférieur transformé en récapitulatif avant export.
- Le récapitulatif inclut format, mode, qualité et destination.
- Après conversion, le chemin réel est affiché pendant cinq secondes.
- Icône Windows chargée depuis le fichier ICO multirésolution.
- Dépôt Git autonome documenté pour une reprise sans contexte.
- Pipeline GitHub Actions pour portable EXE, ZIP, installateur et SHA-256.
- Roadmap Custom consignée.


## 0.7.9

- Bandeau inférieur simplifié : « Prêt à convertir : 800 px WebP · Qualité 78 ».
- Suppression complète du badge « Sortie WebP uniquement ».
- Le résumé inférieur varie automatiquement selon le preset actif.
- En-tête éditorial resserré sans réduire les cartes de presets.
- Hauteur des cartes conservée à 124 px.
- Dimensions agrandies et mode ajouté : Bord long, Adapter au cadre ou Recadrer pour remplir.
- Puces blanches sur les cartes inactives et orange sur la carte active.
- Barre de destination centrée et limitée à 50 % de la zone de dépôt.
- Libellé « Modifier la destination ».
- Bouton « Choisir des fichiers » rendu plus lisible.
- Icône Windows reconstruite avec marge transparente et plusieurs résolutions.


## 0.7.8

- Titre raccourci : « Vos images prêtes pour le web ».
- Choix d’un dossier de destination mémorisé tant qu’il existe.
- Retour immédiat au dossier des originaux avec le bouton « Par défaut ».
- Destination affichée directement dans la zone de dépôt.
- Aucun écrasement silencieux : suffixes -2, -3, etc. en cas de doublon.
- Statut et badge WebP regroupés dans un bandeau fixe en bas.
- Écran temporaire de réussite pendant 5 secondes après conversion.


## 0.7.7

- Les deux noms de métiers sont maintenant modifiables dans Réglages.
- Exemple : remplacement de PrestaShop par Shopify sans modifier le code.
- Les noms personnalisés sont repris sur les cartes principales, les titres de sections et le choix d’usage.
- Les noms sont enregistrés localement et conservés lors d’un changement de langue.
- Restaurer les réglages remet WordPress / Web et PrestaShop.


## 0.7.6

- Languages devient un bouton unique : aucune langue affichée en permanence.
- La liste des 22 langues apparaît uniquement au clic, avec Français en premier.
- Cartes WordPress/PrestaShop renforcées avec titres plus grands et plus gras.
- Cartes de presets raccourcies et noms mieux mis en valeur.
- Zone de dépôt agrandie et rendue plus importante visuellement.
- Icône Windows agrandie dans la barre des tâches à partir du logo rond validé.
- Création du ZIP final déplacée dans un dossier temporaire pour éviter les verrouillages OneDrive.


## 0.7.5

- Icône ronde 2Webp forcée dans la barre des tâches Windows.
- Ajout d’un AppUserModelID Windows dédié pour éviter l’icône générique Python/Qt.
- Icône globale définie au niveau de QApplication et de la fenêtre principale.
- Nouveau fichier ICO multi-résolutions utilisé par PyInstaller.


## 0.7.4

- Réglages numériques remplacés par des champs de saisie simples.
- Suppression des flèches et des modifications accidentelles à la roulette.
- Sélecteurs protégés contre les changements à la roulette.
- Entête et bandeau d’actions fixes dans Réglages.
- Seules les cartes défilent.
- Ascenseur vertical toujours visible.
- Boutons Restaurer et Enregistrer rendus plus lisibles.


## 0.7.3

- Bloc Languages simplifié.
- Sélecteur placé directement sous le libellé Languages.
- Espacement renforcé entre Convertir, Languages et Réglages.
- Sélecteur rendu plus discret pour préserver le rythme de la colonne gauche.


## 0.7.2

- Repositionnement du chevron du sélecteur Languages.
- Zone de flèche rentrée de 5 px dans le composant.
- Marge interne augmentée pour éviter le chevauchement avec le texte.
- Contour arrondi conservé sans débordement du sous-contrôle.


## 0.7.1

- projet complet rebâti sous le nom 2Webp ;
- logo et icône validés intégrés ;
- réglages fonctionnels des 8 cartes ;
- 22 langues ;
- maximisation et plein écran bloqués ;
- notifications intégrées ;
- tests et génération SHA-256.
