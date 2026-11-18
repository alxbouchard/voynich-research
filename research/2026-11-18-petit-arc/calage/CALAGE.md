# Repérage des groupes dans les photos

Les coordonnées des mots proviennent du Voynichese Project. Chaque mot de Takahashi a été apparié dans l'ordre de la page à la séquence de l'archive XML. Nous avons récupéré, pour le même indice, le rectangle dans la version 2 du visualiseur. Le texte des trois sources concorde à chacun des 107 emplacements d'épreuve. Le groupe qui précède concorde également aux 97 emplacements qui ont un prédécesseur sur la même ligne. Les 10 autres sont en tête de ligne. [Archive XML des coordonnées, Voynichese Project](https://www.voynichese.com/1/data/folio/voynichese_data.zip) · [Visualiseur du projet](https://www.voynichese.com/) · [Photos du manuscrit, Yale](https://collections.library.yale.edu/catalog/2002046)

Le cadrage des images du visualiseur et celui des originaux de Yale diffèrent. Nous avons apparié les points SIFT entre chaque vue couleur version 2 et sa photo Yale, puis estimé une transformation affine robuste par RANSAC. Sur les 22 faces d'épreuve, 856 à 1 982 points d'appariement concordent par face. Le 95e centile de l'erreur entre points homologues varie de 2,95 à 5,28 pixels du JPEG Yale selon la face. Cette mesure porte sur le recalage des images. La précision des contours des mots dépend aussi du pointage original du Voynichese Project. Le rectangle de chaque vignette comporte une marge de 10 pixels à gauche et à droite, 42 en haut et 17 en bas à la résolution native Yale, afin de préserver les marques au-dessus du groupe.

Les 107 rectangles centraux d'épreuve mesurent entre 127 et 195 pixels de large. Les 14 cartes témoins sont produites par le même recadrage ; leurs positions ont été comparées aux observations indépendantes sur la photographie. La transcription IT2a inscrit `daiir` à f5v.3#6. L’ancienne description du contrôle donne `daiin` à cet emplacement. Les deux désignent le même groupe sur la photo. Le point d’ancrage f2r.10#9 a été vérifié sur le recadrage natif.

`reserve.json` et `controles.json` donnent les rectangles et les empreintes des originaux et des extraits. Les quatre coordonnées de `yale_bbox` et `crop_bbox` sont gauche, haut, droite exclue et bas exclu. Les rectangles des visualiseurs `xml_box` et `layout_box` sont exprimés en x, y, largeur et hauteur dans leurs repères propres. Chaque entrée de `transformations.json` fournit les URL des sources, leurs empreintes et la matrice qui transforme les coordonnées de la version 2 en pixels natifs de Yale. Le script `recadrer.py` régénère les 121 PNG et contrôle leurs empreintes.

```sh
python3 recadrer.py --photos yale --sortie reproduction --telecharger
```

Dépendance de ce rejeu, Pillow 12.2.0. Si les JPEG de Yale sont déjà dans le répertoire des photos, la commande fonctionne hors ligne sans l’option de téléchargement. Les indices de mots dans les lignes sont comptés à partir de 1. L'indice du visualiseur est compté à partir de 0.
