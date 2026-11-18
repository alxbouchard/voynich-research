# Photographies Yale et cartes de lecture

Les cinq JPEG natifs dans `originaux/` et les fichiers de `cartes-Q/` permettent un rejeu hors ligne. Le fichier `sites-et-temoins.json` conserve la table de repérage fixée avant lecture, avec URL publiques IIIF, tailles, hachages et coordonnées. Les chemins des cinq images sont relatifs à ce dossier. L’empreinte SHA-256 du registre local avant remplacement des cinq chemins par leurs équivalents portables était `68994591557c8cc722b36a74585a8d208e709d70d8f8a5646a194ef176bacd27`. Le programme portable utilise les JPEG fournis dans ce dossier. La clé en clair `cle-cartes.json` réserve un numéro par observation, sans multiplier le nombre de témoins au motif que deux orientations et deux contrastes sont disponibles. Seul le dossier `cartes-Q/` est destiné aux lecteurs. Les noms Q ont été mélangés avec Python Random, graine 5927164301. La clé fige le résultat de cette permutation.

Avec Python 3 et Pillow (12.2.0 pour l'archive), exécuter depuis ce dossier :

```sh
python3 rejouer.py /tmp/rejeu-photos-yale
diff -qr cartes-Q /tmp/rejeu-photos-yale/cartes-Q
cmp mesures-srgb.json /tmp/rejeu-photos-yale/mesures-srgb.json
```

Le programme vérifie le hachage des originaux, la dimension de chaque photo, son profil couleur, puis les hachages des cartes recréées. Si la compression PNG d'une autre version diffère, il compare aussi les pixels décodés à ceux de la carte archivée. Le rejeu dans l'environnement indiqué a reproduit à l'octet près les quatorze cartes, les consignes et le relevé sRGB. `mesures-srgb.json` fournit les médianes indépendantes R/V/B des 49, 149 et 377 pixels des disques de rayons 4, 7, 11, sans retouche sur les couleurs. L'éclaircissement de la version en niveaux de gris de certaines présentations Q est réservé à la lecture des traces.

Pour le témoin de lecture, les éditions IT2a-n (ligne 53) et ZL3b-n (ligne 94) s'accordent sur `olsheey.daiildy` à la fin de f2r.8. Les fichiers sont présents dans `../../../voynich_20261028/data/`. La proportion d'encre dans le disque varie avec le rayon, surtout à f4r et f9v. Le champ `T` indique un point géométrique dans la zone de la trace. À f9v, l'intérieur `I` appartient à un pétale extérieur au site de la trace. Les croquis matérialisent chaque repère au niveau de la page. La mosaïque des points donne leur contexte immédiat, recadré sur 71 × 71 pixels natifs. Chaque échantillon chromatique, beaucoup plus petit que la fenêtre de la mosaïque, est circulaire.
