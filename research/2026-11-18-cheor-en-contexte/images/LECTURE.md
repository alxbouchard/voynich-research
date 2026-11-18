# Le fragment 222 et les trois reprises de cheor sur f102v2

Le parchemin porte quatre inscriptions qu’on peut transcrire `cheor`. Une seule, f102v2.11, se trouve sous le fragment 222. Les trois autres sont sur les lignes 3, 4 et 10 du second paragraphe, sous **un autre récipient et une autre rangée de fragments**. La mise en page autorise à les classer « même feuillet ». Elle ne permet pas de les attribuer au dessin 222. [Page entière annotée](page-annotee.jpg) · [Photographie de Yale, Beinecke MS 408, image 1006252](https://collections.library.yale.edu/catalog/2002046?child_oid=1006252)

## Du dessin aux deux paragraphes

Le premier récipient accompagne deux rangées de sept dessins chacune, numérotés 214–220 et 221–227. Le 222 est le deuxième dessin de la deuxième rangée. Une bande verte porte des lobes arrondis disposés en peigne. Une partie étroite descend à gauche. La légende tient sous la bande verte. Ce dessin seul ne permet d’identifier ni une racine ni l’organe que nommerait la légende. L’interlinéaire le décrit comme une feuille en peigne. Les dessins voisins 221 et 223 portent respectivement `okody` et `okoroeey` dans Takahashi et Zandbergen–Landini. [Agrandissements](quatre-lectures.jpg) · [Légendes anciennes, section L2](https://www.voynich.nu/q19/f102v2_tr.txt)

Sous ces deux rangées viennent les sept lignes .17–.23. Aucun `cheor` entier ne s’y trouve dans les deux éditions. La première ligne comporte cependant le groupe ressemblant `sheor` chez Zandbergen–Landini et `sheos` chez Takahashi. Un second récipient et cinq dessins, 229–233, séparent ce premier paragraphe du paragraphe inférieur .30–.39. La numérotation de Th. Petersen saute le 228. Elle sert à repérer les dessins et ne constitue pas une lecture des quatre inscriptions. [Plan et numérotation du feuillet](https://www.voynich.nu/q19/index.html#f102v2) · [Texte ZL3b](https://www.voynich.nu/data/ZL3b-n.txt) · [Texte IT2a](https://www.voynich.nu/data/IT2a-n.txt)

## Vérification des signes et des blancs

Les coordonnées en pixels délimitent les encadrements de la planche sur le JPEG de 2 981 × 3 795 pixels, origine en haut à gauche. Elles comprennent une marge autour de l’encre. Les numéros de ligne de l’ancienne collation ne reprennent pas le décompte IVTFF moderne.

| Lieu IVTFF | Repère ancien | Rectangle x₁, y₁, x₂, y₂ | Lecture dans son contexte |
|---|---|---|---|
| .11 | L2.2 | 879, 975, 1080, 1054 | Inscription isolée sous le 222. H, V et U donnent `cheor`. |
| .32 | P2.11 | 827, 2485, 982, 2565 | Ligne 3 du bas. `dar` précède `cheor`. À droite, Takahashi et H donnent `sheor`, ZL, F et U `shoar`. Plus loin sur la même ligne apparaît `cheeor`. |
| .33 | P2.12 | 1321, 2564, 1501, 2639 | Ligne 4 du bas. Les deux éditions modernes notent l’initiale incertaine du groupe précédent, `?keeeos`. Elles s’accordent sur `cheor` et divergent sur les espaces qui suivent. |
| .39 | P2.18 | 985, 2987, 1165, 3075 | Ligne 10 du bas. Les deux éditions donnent `yotaiin cheor cheekey orain`. F diffère sur le dernier groupe de la ligne et donne `oraiin`. |

À .32, le départ du troisième groupe comporte une marque au-dessus de la ligne, présente dans les deux lectures de `sh`. Les petits traits au milieu de ce groupe sont accolés. Leur forme laisse subsister l’alternative `sheor/shoar`. Le mot entier `cheor` juste avant et le groupe `cheeor` plus loin gardent leurs graphies distinctes dans les deux éditions. [Photographie locale](quatre-lectures.jpg) · [Interlinéaire, P2.11](https://www.voynich.nu/q19/f102v2_tr.txt)

À .33, le blanc après le dernier trait de `cheor` mesure environ 55 pixels sur l’original. Les deux blancs suivants mesurent chacun environ 20 pixels, entre le petit cercle, le signe recourbé et le début de `al`. Ces largeurs sont estimées à l’œil sur le fac-similé, au bord visible de l’encre. Elles distinguent une grande séparation de deux petites sans imposer une frontière de mot entre ces trois éléments. Takahashi donne `os.al`. ZL écrit `o,s,al`, avec deux blancs incertains. Dans l’ancienne collation, H a `os.al`, F a `os!al` et U a `or.al`. Le signe `!` sert à l’alignement des lectures. La variante ancienne de U touche aussi l’identité du signe central. [Photographie locale](quatre-lectures.jpg) · [Collation ancienne, P2.12](https://www.voynich.nu/q19/f102v2_tr.txt)

Les trois lignes de prose portent toutes `cheor` chez H, F et U. H est la lecture de Takeshi Takahashi, reprise dans IT2a. Le feuillet est attribué à la main 1 dans le classement de Lisa Fagin Davis repris au catalogue. Plusieurs lectures d’un même parchemin corroborent ici la graphie. L’étiquette attache le groupe à un dessin. Pour savoir ce que le groupe désigne, il faudrait un indice permettant de choisir entre le fragment entier, une partie, un nom propre à cette plante ou un autre renseignement. Les trois reprises du bas laissent ces possibilités ouvertes. [Histoire des transcriptions](https://www.voynich.nu/transcr.html) · [Notice du feuillet et attribution de main](https://www.voynich.nu/q19/index.html#f102v2)

Les deux planches se régénèrent avec Pillow en donnant le JPEG original à `python3 cadrer.py 1006252.jpg`. Le script vérifie son empreinte SHA-256 avant d’extraire les vues. [Script et rectangles de prélèvement](cadrer.py) · [JPEG natif de Yale](https://collections.library.yale.edu/iiif/2/1006252/full/full/0/default.jpg)
