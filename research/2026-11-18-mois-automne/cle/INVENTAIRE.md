# Couverture des légendes et des cercles

Sur le panneau réservé à octobre (f72v1), **23 des 30 légendes** donnent un mot entier identique dans les quatre lectures. Les sept autres présentent chacune deux graphies concurrentes, soit 14 graphies exclues. Dans les trois cercles, 39 graphies sont communes et 60 sont exclues. Un mot peut apparaître à des rangs différents dans les lectures d’un même cercle.

| Panneaux | Inscriptions | Loci avec accord / examinés | Graphies utilisables | Graphies exclues |
|---|---|---:|---:|---:|
| Octobre | Légendes Lz | 23 / 30 | 23 | 14 |
| Octobre | Cercles Cc | 3 / 3 | 39 | 60 |
| Les douze | Légendes Lz | 171 / 299 | 171 | 328 |
| Les douze | Cercles Cc | 36 / 36 | 531 | 735 |

Le comptage prend chaque graphie normalisée une fois par locus, même si un cercle la répète. Deux variantes au même endroit comptent pour deux graphies. Le fichier donne aussi le nombre de graphies utilisables distinctes de chaque panneau.

L’inventaire regroupe les graphies exclues selon quatre positions, dans l’ordre Takahashi blancs joints, Takahashi blancs séparés, Zandbergen–Landini blancs joints, Zandbergen–Landini blancs séparés. Le caractère `+` indique une lecture admissible, `.` une graphie absente, `?` un caractère hors de l’alphabet admis et `m` un mot alphabétique dans une légende découpée en plusieurs mots. Ainsi à f72v1.16, `okyl` a le code `++..` et `okal` le code `..++`. La rubrique `utilisables` donne les graphies admises dans les quatre lectures au même locus. [Inventaire par locus](INVENTAIRE.json)

Depuis ce répertoire, exécuter `python3 -B inventaire.py`. Le script régénère le JSON et vérifie chaque graphie retenue, ses emplacements et le nombre de loci contre le vocabulaire employé dans l’épreuve. [Script](inventaire.py) · [Déchiffreur](dechiffrer.py)
