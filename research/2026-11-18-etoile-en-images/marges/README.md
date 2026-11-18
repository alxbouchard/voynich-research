# Repérer une ligne dans la marge du cahier final

Les neuf lignes prédites et leurs neuf témoins occupent sept faces. Le lecteur reçoit [les 18 cartes mélangées](CONTACT.jpg) ou les PNG S01 à S18. Deux traits violets, à gauche et à droite de la photographie, marquent la ligne visée. Les marques bleu-vert indiquent les limites à mi-distance entre les lignes. La première ligne du folio a pour limite supérieure le haut de la photographie. Chaque carte préserve la couleur et les proportions de l'original. Le bord droit s'arrête dans les premiers caractères pour permettre l'alignement visuel.

## Du premier mot à la carte

Les coordonnées proviennent des boîtes de mots du Voynichese Project. Pour chaque ligne cible et pour chacune de ses voisines physiques, le premier et le deuxième groupe d'IT2a concordent avec la suite de l'archive XML et avec le texte de la boîte version 2 de même indice. Une comparaison ordonnée porte sur la face entière. Le calage de l'image emploie la photographie du visualiseur version 2 à laquelle correspondent ces dernières boîtes. [Archive XML](https://www.voynichese.com/1/data/folio/voynichese_data.zip) · [Manuscrit original à Yale](https://collections.library.yale.edu/catalog/2002046)

Une transformation affine robuste ajuste les points SIFT de chaque vue Voynichese sur la photographie de Yale. Le nombre d'appuis RANSAC varie de 1 719 à 3 978 par face. Le 95e centile de l'écart géométrique sur ces appuis varie de 2,29 à 6,19 pixels natifs selon la face. Parmi les 30 appuis les plus proches du premier mot de chaque ligne prise en compte, le même indicateur varie de 2,22 à 8,50 pixels. Le rayon nécessaire pour réunir ces 30 points est consigné pour chaque ligne. Les erreurs peuvent aussi dépendre des contours tracés dans le visualiseur et de la déformation du parchemin. [Coordonnées, matrices, URL et empreintes des trois sources par face](calages.json)

Une mesure locale sur les pixels de l'écriture situe le bas du corps des signes dans les 370 premiers pixels de chaque ligne. Elle repose sur des fenêtres de 35 pixels, la densité verticale d'encre et le 85e centile de l'encre du corps du signe dans chaque fenêtre. La pente de chaque ligne est estimée par la médiane des pentes entre points écartés d'au moins 75 pixels. La médiane des pentes des lignes voisines du même bloc détermine l'inclinaison commune. Chaque ligne conserve la médiane de ses propres résidus verticaux pour fixer sa hauteur. Les deux limites passent à mi-distance des axes voisins au même x dans la marge. Les graduations vont jusqu'au bord gauche de l'image. Leurs emplacements dans le blanc du parchemin résultent d'une extrapolation.

Les écarts internes au 90e centile entre les points d'encre et les axes de pente commune vont de 1,19 à 11,55 pixels selon la ligne. En employant la pente propre à chacune des lignes voisines, le plus grand déplacement d'une limite atteint 22,90 pixels à une extrémité du cadrage. L'écart varie linéairement le long du bord. Ce sont deux mesures de sensibilité géométrique. La clef permet de les calculer à l'abscisse de tout détail photographié. [Quadrilatères natifs, axes, variantes de pente, points d'encre et empreinte de chaque carte](cle.json)

## Correction avant lecture définitive

Le contrôle de la dispersion et la vue des premiers mots seuls ont signalé une hampe de la ligne suivante dans la fenêtre du deuxième groupe de f105v.31. La fenêtre de ce groupe a été bornée verticalement à y = 2310–2349 dans le JPEG Yale. Le 90e centile des écarts absolus au tracé commun de cette ligne est ainsi passé de 45,70 à 2,70 pixels. Seules S01 et S08 ont changé. Leurs limites ont bougé verticalement de 1,64 à 13,45 pixels selon le bord et l'abscisse. Les deux tracés sont publiés avec leurs empreintes. [Sensibilité au choix de la fenêtre](sensibilite_calage.json)

## Deux vérifications après ouverture de la clef

Le panneau conserve une bande continue de la page entre la marge et le dernier groupe de la ligne. Deux agrandissements reprennent la marge et le groupe encadré. Le cinquième groupe de f107r.1 et le dixième de f104r.19 se lisent `otor` dans IT2a et dans le dictionnaire de coordonnées. Les rectangles natifs des agrandissements des groupes sont respectivement [1064, 147, 1230, 271] et [1979, 1430, 2138, 1535] en pixels Yale, dans l'ordre gauche, haut, droite exclue, bas exclu. [Panneau de vérification](CONTEXTE.jpg) · [Quadrilatères, détails et sources](contexte.json) · [Photo f107r](https://collections.library.yale.edu/iiif/2/1006262/full/full/0/default.jpg) · [Photo f104r](https://collections.library.yale.edu/iiif/2/1006256/full/full/0/default.jpg)

## Reproduire

Depuis ce répertoire, avec Python 3, NumPy, OpenCV, Pillow et curl, exécuter les commandes suivantes. Le premier script peut télécharger les JPEG Yale et Voynichese, les boîtes de la version 2 et l'archive XML dans le cache local. La transcription IT2a et les prédictions sont lues depuis le dépôt. Les trois scripts acceptent `--photos CHEMIN` pour employer des originaux déjà téléchargés. Le JPEG de contexte publié utilise la police Arial de macOS. Les PNG anonymes utilisent la police fournie par Pillow.

```sh
python3 localiser.py
python3 cartes.py
python3 contexte.py
shasum -a 256 -c empreintes.sha256
python3 cartes.py --placement-initial --sortie cache/placement-initial
```

La réalisation emploie OpenCV 5.0.0, NumPy 2.5.1 et Pillow 12.2.0. Un second passage complet depuis les JPEG, boîtes et XML reproduit les sept transformations, les 18 PNG, les deux versions de CONTACT, la clef définitive et le JPEG de contexte. Le site et le témoin sont mélangés en classant les identifiants de ligne par empreinte salée de façon reproductible. Les versions finales de CONTACT et des PNG sont comprises dans le manifeste de contrôle.
