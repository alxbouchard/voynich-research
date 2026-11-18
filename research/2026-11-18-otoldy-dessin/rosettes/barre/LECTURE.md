# Le trait entre les deux croissants

Sur f48v.9, une ligne brune joint nettement le sommet des deux petits signes du premier mot de S12. Sur le dépliant, à l’emplacement correspondant du premier mot de S37, deux croissants restent visibles. Je ne peux pas suivre une ligne continue de l’un à l’autre. Le haut du signe initial, certaines portions du grand signe à deux hampes et la queue finale sont eux aussi très pâles. Une partie du tracé a pu devenir invisible. La photographie ne révèle ni son état primitif ni la cause de sa faible visibilité. [Comparaison en couleur](comparaison-couleur.png)

| Témoin du dépliant | Observation dans le cliché Yale |
|---|---|
| 31:3, transcrit `ofchedaiin` par Placa | Même passage que la cible. Après le grand signe, un trait brun joint deux éléments courts. Cette portion de l’inscription est mieux encrée que S37. |
| 11:19 et 11:21, transcrits `okchdy` et `oteedy` | Sur l’anneau voisin, le premier présente une liaison continue. Dans le second, deux petits croissants se suivent avec du fond visible entre eux. Le groupe intermédiaire 11:20 permet de vérifier leur ordre. [Les trois groupes dans leur contexte](sequence-anneau.png) |
| 14:28, transcrit `qotchdy` | Ce groupe est précédé de 14:27 et suivi du court 14:29 sur un autre anneau. Son orientation diffère d’environ 6° de celle de S37. Le deuxième petit signe est plus massif que le premier. La continuité de la barre est difficile à établir sur l’image couleur, même à cet emplacement annoté `ch`. |

La silhouette de S37 ressemble à celle du témoin 11:21. L’absence d’un pont aussi net qu’en 11:19 reste compatible avec une liaison devenue trop pâle pour être lue. La couche textuelle publiée par Placa dérive de ZL3b. Ses coordonnées situent les mots et leur orientation. La photographie permet de constater une différence de visibilité avec f48v.9 et laisse ouvertes les lectures `ee` et `ch` pour le segment de S37. Ces témoins ne fournissent aucun seuil permettant de reconstituer un trait disparu.

## Repérage des extraits

Les positions de Placa ont guidé la recherche. Les groupes ont ensuite été repérés dans la photographie par leurs grands signes, les voisins et leur place sur l’anneau ou dans le passage entre les dessins. Les rectangles ci-dessous sont exprimés en pixels de l’original Yale, de gauche à droite et de haut en bas, avant rotation. Les PNG natifs conservent les couleurs et les pixels du JPEG décodé. Sur la planche, l’agrandissement est de 2×. Seules les vignettes de l’anneau 11 requièrent une rotation oblique avec rééchantillonnage. [Photo Yale du dépliant](https://collections.library.yale.edu/iiif/2/1006231/full/full/0/default.jpg) · [Photo Yale de f48v](https://collections.library.yale.edu/iiif/2/1006169/full/full/0/default.jpg) · [Positions et transcriptions de Placa, version examinée](https://github.com/alessandroplaca-uro/voynich-spatial-data/blob/7580dafa624cf23a63665f4819022003f8d128ef/rosettes/tokens_f85v_86r.csv)

| Extrait | Rectangle Yale (x0, y0, x1, y1) | Orientation du PNG natif |
|---|---|---|
| [S12, f48v](f48v-natif.png) | 1856, 1127, 2027, 1208 | Originale |
| [S37, dépliant](fRos-natif.png) | 6568, 2593, 6709, 2672 | Demi-tour |
| [31:3](31-3-natif.png) | 6035, 2613, 6276, 2729 | Demi-tour |
| [14:28](14-28-natif.png) | 6487, 4395, 6703, 4495 | Demi-tour |
| [11:19](11-19-natif.png) | 6078, 1846, 6338, 2106 | Originale |
| [11:21](11-21-natif.png) | 5866, 1606, 6126, 1866 | Originale |

Avec les JPEG natifs du dépliant et de f48v, dans cet ordre, puis un dossier de sortie, [le programme](reproduire.py) refait les huit images. L’option `--police` accepte Arial en TTF pour reproduire également la typographie de la planche.
