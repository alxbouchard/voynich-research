# Origine des quatre extraits

Les quatre rectangles ont été découpés directement dans deux JPEG originaux de la Beinecke. Les dessins sont centrés dans chaque vue. Les traits, les inscriptions voisines et les couleurs du parchemin sont conservés. Sur f89r1, certaines formes transparaissent et des parties des dessins voisins entrent dans le cadre. Les pieds de la figure 113 sont visibles en entier jusqu’aux deux pointes recourbées. Les images ont été redimensionnées à des échelles différentes pour rendre chaque dessin lisible. [Planche](quatre-dessins.jpg) · [Cliché Yale f89r1](https://collections.library.yale.edu/iiif/2/1006233/full/full/0/default.jpg) · [Cliché Yale f99v](https://collections.library.yale.edu/iiif/2/1006247/full/full/0/default.jpg)

| Vue Yale | Fragment, locus, graphie EVA | Cadre natif en pixels (gauche, haut, droite, bas) |
|---|---|---|
| 1006233 | 24 · f89r1.3 · oldam | 3282, 137, 3864, 910 |
| 1006233 | 30 · f89r1.25 · saldam | 3150, 2532, 3798, 3643 |
| 1006247 | 113 · f99v.31 · doldam | 2223, 1535, 2685, 2302 |
| 1006247 | 111 · f99v.29 · okeodor | 1362, 1647, 1912, 2184 |

Les deux premières graphies ont servi à formuler la prédiction avant de rechercher d’autres étiquettes. La recherche a donné une seule nouvelle position concordante. Sur la planche anonyme, deux lecteurs IA séparés ont classé les fragments 113 et 111 parmi les dessins à deux bras. Le feuillet f99v avait déjà été photographié et étudié dans le projet. Les cinq dessins de cette rangée ont été présentés aux lecteurs dans un ordre mélangé, avec les inscriptions masquées. Le fragment 111 montre que deux bras peuvent aussi accompagner un mot avec une autre terminaison. Le test porte sur l’aspect de ces objets et laisse ouverte la valeur de lecture de la finale. [Prédiction](../PREDICTION.md) · [Résultats de recherche](../LIEUX.json) · [Premier lecteur](../E-1.json) · [Second lecteur](../E-2.json) · [Attributions dans la rangée](../PREPARATION-E.md)

Pour reproduire la planche avec Pillow, exécuter `python3 assembler.py 1006233.jpg 1006247.jpg`. Le script vérifie l’empreinte de chaque original avant découpe. [Script](assembler.py)
