# Une étoile et le paragraphe de f68r1 portent le groupe « otor »

Les transcriptions de Takahashi (H) et de Zandbergen–Landini (ZL) lisent `otor` à côté d’une étoile et au septième emplacement de la première ligne du texte qui surmonte le dessin. Les deux autres panneaux du dépliant n’offrent aucune reprise exacte d’une de leurs propres légendes. À plusieurs reprises, une légende trouve pourtant un correspondant sur un panneau voisin. [Fac-similé de Yale](https://collections.library.yale.edu/catalog/2002046?child_oid=1006196) · [Comparaison photographique](otor.jpg)

Sur l’image, on peut comparer le grand signe à deux hampes, le petit signe arrondi qui suit et le dernier trait dans les deux groupes. Le troisième signe de la ligne est pâle. Dans l’interlinéaire historique, la lecture C donne `otar` dans le paragraphe, tandis que H, F et U y donnent `otor`. Pour la légende, H, V et U donnent `otor`. L’accord des deux éditions retenues permet de proposer cette correspondance, sans donner le sens du groupe ni la direction d’un éventuel renvoi. [Étoile](https://collections.library.yale.edu/iiif/2/1006196/276,1778,278,211/full/0/default.jpg) · [Ligne du paragraphe](https://collections.library.yale.edu/iiif/2/1006196/1585,341,198,134/full/0/default.jpg) · [Lectures historiques au même endroit](lectures-otor.txt)

## Les neuf associations annoncées

Chaque case donne les **positions de texte correspondantes / positions lisibles**. Les espaces douteux sont ici séparés. L’inventaire source contient les groupes entiers de trois unités EVA ou plus provenant de toutes les lignes de légendes d’étoiles (29, 24 et 11 lignes). Une ligne de légende peut contenir plusieurs groupes. Un mot de texte répété à deux emplacements compterait deux fois. [Prédiction déposée avant calcul, commit 29a4535](PREDICTION.md)

| Source des légendes | Texte 1, H | Texte 2, H | Texte 3, H | Texte 1, ZL | Texte 2, ZL | Texte 3, ZL |
|---|---:|---:|---:|---:|---:|---:|
| Panneau 1 | **1/32** | 0/55 | 0/46 | **1/32** | 0/54 | 1/47 |
| Panneau 2 | 0/32 | **0/55** | 1/46 | 0/32 | **0/54** | 1/47 |
| Panneau 3 | 0/32 | 0/55 | **0/46** | 1/32 | 0/54 | **0/47** |

La somme sur la diagonale est de **1/32** dans les deux éditions. Permuter les trois textes donne six affectations possibles. Deux sur six atteignent ou dépassent cette valeur chez H, quatre sur six chez ZL. Dans les deux lectures, apparier les légendes des panneaux 1, 2 et 3 aux textes 1, 3 et 2 donne un score supérieur, respectivement 1/32 + 1/46 et 1/32 + 1/47. Cette comparaison ne soutient pas la prédiction d’une reprise locale plus fréquente.

| Mot | Légende | Texte contenant le mot | Variantes concernées |
|---|---|---|---|
| `otor` | f68r1.26, mot 1 | f68r1.1, paragraphe, mot 7 | H et ZL, tous découpages |
| `chol` | f68r2.25, mot 2 | f68r3.1, cercle, mot 30 | H tous découpages et ZL espaces séparés. ZL a `chol,al`. |
| `otcheody` | f68r1.10, mot 1 | f68r3.22, cercle, mot 1 | ZL tous découpages. H a `otchody` dans le texte. |
| `oky` | f68r3.15, mot 2 | f68r1.37, cercle, mot 1 | ZL tous découpages. H lit `yky` dans la légende. |
| `oky` | f68r3.15, mot 2 | f68r2.31, cercle, mot 4 | ZL espaces joints uniquement (`o,ky`). |

## Dépendance au registre et à la lecture

| Affectations aussi bonnes que la véritable sur six | H, séparés | H, joints | ZL, séparés | ZL, joints |
|---|---:|---:|---:|---:|
| Toutes les légendes | 2 | 2 | 4 | 5 |
| Seulement les groupes lus pareil au même emplacement | 2 | 2 | 2 | 2 |

Dans les seuls paragraphes, `otor` demeure l’unique rencontre. Le troisième panneau n’a aucune ligne P0. Dans les seuls cercles, les inscriptions stellaires ont **zéro rencontre sur leur propre panneau** dans toutes les variantes. Les six permutations concernent le même dépliant et produisent des observations dépendantes. La comparaison utilise 133 positions lisibles dans chaque édition en séparant les espaces douteux, et 133 (H) ou 129 (ZL) en les joignant.

Le programme conserve les petits groupes lisibles au dénominateur et donne aussi le calcul limité aux destinations de trois unités ou plus. Les rangs du tableau de sensibilité sont identiques avec cette restriction. Il conserve les caractères numériques d’EVA étendu comme unités quand leur lecture est spécifiée. Il écarte un groupe si un caractère y est illisible ou s’il a plusieurs lectures. Il traite la coupure de dessin comme une séparation et enlève les marques éditoriales. Les chiffres après la barre dans les mesures sont les rangs des mots dans leur ligne, avant l’exclusion des groupes incertains. Les registres Pb, Ri et La sont hors de la comparaison annoncée. [Code exécutable](compter.py) · [Loci, dénominateurs et six scores de chaque variante](MESURES.json) · [Format IVTFF](https://www.voynich.nu/software/ivtt/IVTFF_format.pdf)

Après ce premier calcul, la même forme a servi à une prédiction sur les douze panneaux du zodiaque et à une recherche près des fragments végétaux. [Résultat du transfert](otor-note.md)
