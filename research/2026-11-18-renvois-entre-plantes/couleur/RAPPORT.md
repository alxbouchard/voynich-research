# Le petit signe de f99v prédit-il la couleur ?

La quatrième racine du troisième rang de f99v est le fragment **112**. Sa partie charnue à trois pointes est peinte en brun rouge. Une petite trace sombre se retrouve dans sa moitié gauche sur les numérisations de 2004 et 2014. Je ne distingue de façon sûre ni la boucle ni la hampe qui permettraient de trancher entre les lectures *p* et *r* proposées par Zandbergen. Les deux prises de vue en lumière visible ne déterminent pas si le trait précède la peinture. Une seule lecture visuelle IA a comparé les deux numérisations. [Deux clichés de la racine](f99v-deux-cliches.jpg) · [Catalogue du cahier 19](https://www.voynich.nu/q19/index.html#f99v) · [Provenance des numérisations](https://www.voynich.nu/gallery.html)

Le témoin historique est le manuscrit de Vicence, Biblioteca civica Bertoliana, 362/1, daté de 1426–1475 par le catalogue. Au f34r, on peut lire *rot* juste au-dessus d’une corolle rouge orangé. Au f39r, *gel* figure près d’une partie jaune de la racine. Ce sont des mots comparables à des indications au peintre, dont on peut contrôler la lecture et la couleur séparément. Les deux occurrences et les essais antérieurs sur *g* et *rot* dans le Voynich avaient déjà été documentés. La nouvelle question est celle du transfert du p/r présumé de f99v. [Photographie du f34r reproduite p. 14](https://www.voynich.nu/papers/Voynich100_RZ_2012.pdf#page=14) · [Photographie du f39r](https://viridisgreen.blogspot.com/2017/04/vicenza-ms-362-liber-herbarius-herba.html) · [Dossier antérieur](../../2026-11-18-consignes-de-couleur/RAPPORT.md)

## Contrôle du brun rouge

La prédiction inscrite avant la réouverture des comparaisons était que les endroits proposés comme portant le même signe présentent la famille de brun rouge du fragment 112. Les sites étaient déjà publiés et leurs dessins déjà connus des travaux antérieurs. Il s’agit d’une confrontation rétrospective. Les médianes sont calculées sur 61 × 61 pixels sRGB des JPEG de Yale, sans étalonnage des pigments. Sur f99v, la racine donne **156, 104, 83** et le parchemin voisin **193, 174, 153**. [Prédiction](AVANT.md) · [Origine des trois repères p](https://herculeaf.wordpress.com/2023/09/20/what-about-the-other-marginal-writings/) · [Autres lectures proposées](https://www.voynich.nu/writing.html)

| Lieu | Lecture proposée | Zone du signe et organe visible | Médiane R, V, B |
|---|---|---|---|
| f9v | p ou r | Fleur peinte en bleu, avec du parchemin apparent | 120, 135, 137 |
| f20r | p ou r | Petit trait à proximité de ramifications pâles et de bandes vert olive | 192, 171, 149 |
| f32r | p | Zone peu peinte entre deux éléments bleus, au-dessus du jaune | 193, 180, 165 |
| f29r | r | Signe plus net dans une longue racine beige, légèrement ocrée | 191, 168, 145 |

Aucun des trois repères *p* ne retrouve le brun rouge couvrant la racine 112. L’autre racine proposée pour *r* est beaucoup plus claire. Une même instruction aurait pu rester inexécutée, ou les formes représenter des signes distincts. Ces possibilités ne fournissent aucune prédiction réussie de couleur ici. [Comparaisons photographiques](quatre-comparaisons.jpg) · [Coordonnées, fenêtres et empreintes des sources](sources-et-mesures.json)

## Le mot extérieur

La légende placée à droite de la tige est **olky**, f99v.30. Le repère 112 du catalogue a été ajouté par le transcripteur ZL. Le petit signe intérieur est physiquement distinct du mot manuscrit. La recherche littérale du groupe complet trouve **un seul emplacement, ce même f99v.30, parmi 194 entrées Lf** dans chacune des deux éditions et avec les deux traitements des blancs. Aucune des 19 lignes de prose sur f99v ne contient *olky*. Le groupe revient ailleurs en prose à 17 emplacements communs aux quatre lectures, plus deux emplacements sensibles aux blancs. La répétition en prose ne localise pas un autre dessin de racine rouge. Il n’y avait donc pas de seconde étiquette permettant l’épreuve annoncée. Le mot et la marque intérieure restent de sens inconnu. [Inventaire détaillé](frequences.json) · [Cliché intégral f99v](https://collections.library.yale.edu/iiif/2/1006247/full/full/0/default.jpg)

Les corpus IT2a-n et ZL3b-n se trouvent dans le dépôt. Depuis ce répertoire, exécuter `python3 relever.py` pour les comptages. Pour les planches et les mesures, réunir dans un répertoire les cinq JPEG et vingt tuiles indiqués dans le fichier des sources, renommés selon `python3 relever.py --help`, puis utiliser `--photos DOSSIER`. Le script retire le seul numéro éditorial de fragment en début de légende avant la recherche. Les lectures incertaines restent exclues du décompte des mots lisibles. [Script](relever.py)
