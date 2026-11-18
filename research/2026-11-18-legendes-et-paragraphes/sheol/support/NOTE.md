# Une partie du feuillage visible au verso vient-elle du recto ?

**Oui, les formes et les emplacements concordent.** Une fois le recto retourné et calé sur les accidents du parchemin, le grand feuillage lobé du fragment 35 tombe sur la plage verte pâle qui s'étend au-dessus des candidats 2 et 3 au verso. Ses festons et le creux entre les deux lobes inférieurs suivent la bordure pâle. La racine renflée et les deux longs prolongements du 35 ont une autre disposition que les racines brun foncé du candidat 2. Le rapprochement initial des feuillages s'explique ainsi par la présence de couleur sur l’autre face du même parchemin. Les photographies en lumière visible ne permettent pas de départager la transparence optique et la pénétration du pigment. [Superposition](superposition.jpg) · [Comparaison initiale des dessins](../DESSINS.md)

## Recalage indépendant de la couleur

Les deux sources sont les photographies de la Beinecke Rare Book and Manuscript Library, Yale University Library. Le JPEG du recto, **1006233**, mesure 9 078 × 3 777 pixels et réunit trois pages logiques. Le JPEG du verso, **1006234**, mesure 4 204 × 3 809 pixels. Les deux faces ont été photographiées avec des ouvertures différentes. L’identifiant f89r2 désigne ici le texte et les dessins qui traversent le dernier pli du dépliant. L’analyse utilise uniquement la feuille concernée. Les fichiers de repères donnent les empreintes des JPEG natifs. [Recto de Yale](https://collections.library.yale.edu/iiif/2/1006233/full/full/0/default.jpg) · [Verso de Yale](https://collections.library.yale.edu/iiif/2/1006234/full/full/0/default.jpg) · [Description du dépliant par Stolfi](https://www.ic.unicamp.br/~stolfi/voynich/Notes/102/work/Notes/040/html/f89r2.htm)

Après réflexion horizontale du recto, les deux coins gauches de la feuille active, une encoche de son bord inférieur et un trou de l’ancienne couture fixent six coefficients d'une transformation affine par moindres carrés. Le coin supérieur sur le verso est plus délicat à repérer car il repose sur d’autres feuilles. Les dessins et les mots n'interviennent pas dans l'ajustement. Le tracé et le soupçon de transparence étaient connus du lecteur. La sélection des repères matériels et du contrôle principal a précédé le calcul. [Règle fixée](REGLE.md) · [Les quatre repères de calage et les quatre réserves](points-du-parchemin.jpg) · [Coordonnées](REPERES.json)

| Contrôle tenu à l'écart | Écart entre position prédite et observée |
|---|---:|
| Décrochement du bord gauche, aux trois quarts de la hauteur | **7,3 pixels** |
| Coin du trou triangulaire au début de la couture centrale | 9,0 pixels |
| Extrémité droite de la fente cousue | 4,2 pixels |
| Petite entaille secondaire au bord inférieur | 29,3 pixels |

L’erreur de 29,3 pixels renseigne sur les écarts matériels entre les prises de vue et la difficulté de pointer la même partie d’un bord recourbé. Deux mesures sur la même couture ne constituent pas des témoins matériels indépendants. À la hauteur du feuillage, trois mesures du bord supérieur de la **feuille active** donnent des écarts verticaux absolus de 6,7, 10,6 et 9,5 pixels, respectivement. Il s'agit de distances verticales au bord, pas de trois positions identifiées en deux dimensions. [Sortie du calcul et points projetés](RESULTATS.json)

## Combien de vert se retrouve à la position prédite ?

Le masque part de la plus grande plage contiguë de vert dans le rectangle du feuillage au recto. Le programme conserve les pixels dont la composante chromatique *a* dans CIELAB après un filtre médian 11 × 11 passe un seuil. Au verso, il retient tous les pixels répondant au seuil dans la région contrôlée. Le seuil diffère entre recto et verso parce que l'intensité est plus faible à travers la feuille. Les seuils sont des choix descriptifs arrêtés après inspection des couleurs. La proportion mesurée est la fraction du masque du recto qui rencontre du vert au verso. Une zone verte plus grande peut donc aussi capter un contour mal placé. Ni l'éclairage ni les valeurs colorimétriques du parchemin et des pigments n’ont été calibrés.

| Seuils du canal *a*, recto et verso (échelle OpenCV de 0 à 255) | Décalage −500 px | −250 px | Position du parchemin | +250 px | +500 px |
|---|---:|---:|---:|---:|---:|
| 123 et 124 | 14,5 % | 24,3 % | **38,8 %** | 27,2 % | 23,7 % |
| 125 et 126 | 29,0 % | 56,6 % | **89,9 %** | 64,3 % | 45,6 % |
| 127 et 128 | 32,4 % | 61,7 % | **95,7 %** | 68,4 % | 49,6 % |

Au réglage central, 205 824 des 228 940 pixels projetés de la couronne tombent sur du vert pâle. La superposition permet en outre de comparer les contours, jusque dans les lobes de la feuille. Les essais décalés conservent les mêmes pixels, la même couleur et le même modèle. Ces déplacements ont été fixés avant le calcul et restent un contrôle descriptif local. [Masque reporté sur la photographie](superposition.jpg)

## Deux petites feuilles au-dessus du candidat 4

**Cette comparaison supplémentaire a été choisie après inspection de la première superposition.** À droite de la couronne dans le recto retourné, deux petites feuilles dentées forment un motif en diagonale. Projetées avec les mêmes coefficients et les mêmes seuils, elles recouvrent les deux taches vertes situées au-dessus des racines du candidat 4, le fragment 53 au verso. Les contours bleus de la planche sont calculés à partir du recto. Les rectangles d’extraction des deux feuilles se rencontrent au col qui les relie. Le bord rectiligne de séparation à cet endroit vient du recadrage.

Au réglage central, la feuille basse recouvre du vert sur 86,2 % de sa surface projetée et la haute sur 89,9 %. Pour la feuille basse, les décalages de −500, −250, +250 et +500 pixels donnent respectivement 54,8 %, 53,2 %, 6,8 % et 2,5 %. Pour la haute, un déplacement de 500 pixels à gauche **atteint 97,1 %** car il la fait tomber dans la grande plage verte. Les deux taches en diagonale et leur position correspondent visuellement au motif du recto. Le seul taux de couverture de la feuille haute ne distingue pas sa vraie position de toute autre surface verte. Les traits des tiges et des racines visibles au verso conservent leur propre disposition. Le feuillage pâle ne fournit donc pas une seconde représentation indépendante de la plante 35 ou d'une plante portant le mot `sheol`.

Pour rejouer avec Python, NumPy, OpenCV et Pillow, télécharger les deux JPEG natifs ci-dessus puis exécuter `python3 recaler.py chemin/recto-1006233.jpg chemin/verso-1006234.jpg`. Le script contrôle leurs empreintes, rend les deux planches et enregistre les valeurs numériques. [Programme](recaler.py)
