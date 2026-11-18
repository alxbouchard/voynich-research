# Deux légendes des Gémeaux mises à l’épreuve sur le Lion et le Sagittaire

La paire des Gémeaux suggérait de chercher une figure d’aspect masculin auprès de `okal`, et une figure d’aspect féminin auprès de `okaly`. La prédiction a été écrite avant la lecture ciblée de ces deux figures. Les inscriptions avaient déjà été sélectionnées par leur graphie, et les panneaux avaient déjà servi à d’autres études. [Prédiction figée, SHA-256 896165a8f475088edfc4cdb424dff5812d0a984600056e21ad61252ac7626015](PREDICTION.md)

| Lieu | Rattachement de l’inscription au dessin | Observation du préparateur, avant lecture séparée |
|---|---|---|
| Sagittaire, f73v.27, `okal` | Couronne intérieure, vers 2 h 30. Le mot est placé à droite du tronc de la figure, sous son avant-bras levé et sa main tournée vers une étoile à plusieurs pointes. La notice de 1998 la place au rang 4 de la série S2, entre les numéros 3 et 5. | Un contour courbe avec point marque la poitrine. Le carrefour des cuisses présente un trait sombre. La photo laisse son interprétation anatomique incertaine. Aucun récipient discernable. |
| Lion, f72v3.17, `okaly` | Couronne extérieure, vers 8 h 30. Le mot est à droite du tronc, sous la main dirigée vers l’étoile à plusieurs pointes. Dans la série S1 de Grove, le numéro 17 suit `okeeol` et précède `okaldy`. | Un contour courbe ponctué se voit sur la poitrine. L’encre du bassin est peu distincte près du pli. Aucun récipient discernable. |

Dans les deux fiches historiques, Takeshi Takahashi, John Grove et Jorge Stolfi donnent les mêmes graphies au lieu ciblé. IT2a reprend la lecture de Takahashi. ZL3b donne les horaires approximatifs. Sur le Lion, le locus .9 porte aussi `okaly` dans ZL, tandis que Takahashi y lit `okoly`. Ce second lieu du Lion n’entre pas dans la sélection qui exigeait l’accord des deux éditions. [Fiche du Sagittaire](https://www.voynich.nu/q12/f073v_tr.txt) · [Fiche du Lion](https://www.voynich.nu/q11/f072v3_tr.txt) · [Édition ZL](https://www.voynich.nu/data/ZL3b-n.txt) · [Édition IT](https://www.voynich.nu/data/IT2a-n.txt)

Les deux silhouettes portent un signe thoracique comparable. Le préparateur ne retrouve donc pas l’opposition attendue entre leurs torses. Le dessin du bassin laisse subsister une incertitude. Le voisinage d’une étoile et l’absence de contenant visible sont communs aux deux lieux. Les figures se trouvent dans des couronnes différentes, et le pli passe au bas du dessin du Lion. Rien dans ce contrôle ne fixe un sens à `okal`, `okaly` ou à leur `y` final. [Sagittaire avec sa légende](contexte-f73v.27.jpg) · [Lion avec sa légende](contexte-f72v3.17.jpg)

Les détails proviennent des JPEG couleur du Beinecke MS 408, Yale University Library. Le script effectue un quart de tour et prélève un rectangle contextualisé pour chaque inscription. La planche destinée au lecteur séparé masque le texte et les parties des figures qui pénètrent la bande d’écriture voisine. Elle conserve l’encre à l’intérieur du masque, puis adapte chaque image aux dimensions de la planche. Le fichier de coordonnées contient la clé, les fenêtres de prélèvement, les masques et les empreintes des JPEG. La première lecture ci-dessus a été faite avec connaissance des prédictions. [Planche réservée à la lecture séparée](silhouettes.png) · [Clé et coordonnées](coordonnees-et-cle.json) · [Région du Sagittaire chez Yale](https://collections.library.yale.edu/iiif/2/1006207/1645,1215,735,745/full/0/default.jpg) · [Région du Lion chez Yale](https://collections.library.yale.edu/iiif/2/1006204/990,1320,630,1420/full/0/default.jpg)

Pour reproduire les trois images avec Python 3 et Pillow, exécuter `python3 -B prelever.py images`, où le dossier `images` contient `1006204.jpg` et `1006207.jpg`. Les URL des fichiers intégraux se déduisent des liens institutionnels en remplaçant le rectangle par `full`. [Script](prelever.py)

## Résultat de la lecture à l’aveugle

Deux agents IA travaillant séparément ont reçu la même planche X et R, ainsi que la planche de deux autres dessins des Gémeaux. Les lecteurs ignoraient les graphies, les lieux et la règle à vérifier. Ils ont décrit chacun des quatre motifs du torse et du bassin. Les deux jugements reposent sur les mêmes pixels. [Planche présentée](silhouettes.png) · [Contre-épreuve dans les Gémeaux](../voisin/RESULTAT.md)

| Code | Légende et prédiction | Lecteur A | Lecteur B |
|---|---|---|---|
| X | `okal`, Sagittaire, apparence masculine attendue | Féminine plausible, confiance moyenne. Petit crochet ponctué sur la poitrine. Trait de l’aine ambigu. | Féminine possible, confiance modérée. Arc pointé sur le torse, pli indistinct à la cuisse. |
| R | `okaly`, Lion, apparence féminine attendue | Féminine plausible, confiance moyenne. Arc ponctué analogue. La cuisse fléchie se confond avec un trait. | Féminine possible, confiance modérée. Petit contour autour d’un point, traits superposés au bassin. |

Un des deux résultats visuels correspond à la prédiction, celui du Lion. Prédire la même apparence pour les deux figures rend les deux jugements. Ces deux occurrences forment toute la réserve hors Gémeaux selon le critère fixé de légendes entières concordantes. Leur examen ne soutient pas l’association proposée entre finale et apparence.
