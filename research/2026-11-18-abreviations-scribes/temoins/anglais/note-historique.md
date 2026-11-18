# Une abréviation nasale anglaise du XVe siècle

Dans le manuscrit HM 128 de la Huntington Library, le trait au-dessus d’une voyelle signale souvent la disparition d’un *m* ou d’un *n*. Doubler la consonne qui suit le trait permet de lire certains mots. Deux passages d’un même feuillet montrent où la règle échoue. Les éditeurs datent la copie de *Piers Plowman* du début du XVe siècle. Le fragment Hm2 et la copie longue Hm sont deux témoins distincts reliés dans le même volume. [Notice de l’édition](https://piers.chass.ncsu.edu/texts/Hm/intro)

## Règle et réserves

Le choix initial, annoncé avant consultation des feuillets, portait sur la découverte au f.95r du fragment Hm2 et son contrôle au f.96r. Le premier contient un seul mot à expansion balisée, *eu[er]y*. En seconde lecture, aucun des 331 mots du f.96r n’a la forme de base *euy*. La prédiction n’a donc rencontré aucune occasion. Les sept autres expansions du f.96r restent hors règle. [Fragment Hm2, transcription](https://piers.chass.ncsu.edu/texts/xml/Hm2Whole.xml)

Pour la copie longue, le f.113r a servi à choisir une règle, les f.114r, 115r et 116r ayant été réservés avant ce choix. Lorsqu’une voyelle porte un trait nasal devant un *m* ou un *n* encore visible, prédire une copie de cette consonne. Le f.113r fournit huit cas parmi dix-huit expansions encodées. Sur les trois faces réservées, seules deux des cinquante-sept expansions remplissent la condition de position. Les deux prédictions correspondent à l’édition, *su[m]me* au f.114r (Hm.P.94) et *wo[m]men* au f.116r (Hm.1.33). Les deux lettres sont des *m*. Une prédiction constante de *m* ferait aussi bien sur ces deux mots. Les trois faces totalisent 120 vers et 1 123 unités selon la segmentation du script. [Transcription Hm](https://piers.chass.ncsu.edu/texts/xml/HmWhole.xml)

Les photos du f.114r, du f.115r et du f.116r ont servi à constituer un contrôle visuel de six mots, choisis pour présenter deux cas positifs et quatre mots proches sans trait. La sélection ciblée ne permet aucune estimation du taux de faux positifs à l’échelle du texte. Les photos et la transcription sont consultables gratuitement. L’archive réserve les fichiers à l’étude personnelle. Les coordonnées en pixels constituent la référence reproductible. [Conditions de l’archive](https://piers.chass.ncsu.edu/materials/)

Après la lecture des trois faces réservées et avant le dépouillement suivant, j’ai étendu la règle inchangée à toutes les autres faces du poème à partir de 117r, jusqu’à 205r. La méthode parcourt les vers du témoin en écartant les variantes d’autres manuscrits, les notes, le texte supprimé et les formes normalisées. Le marqueur XML désigne les lettres ajoutées par les éditeurs. Il indique le lieu d’une expansion sans encoder la silhouette de la marque d’encre. Cette mesure porte donc sur toutes les expansions en position compatible. La forme du signe se vérifie séparément sur les photos.

| Épreuve | Expansions | Prédictions | Accord éditorial | Hors condition |
| --- | ---: | ---: | ---: | ---: |
| Apprentissage, 113r | 18 | 8 | 8 | 10 |
| Première réserve, 114r, 115r et 116r | 57 | 2 | 2 | 55 |
| Réserve supplémentaire, 177 faces | 3 081 | 88 | 70 | 2 993 |

Sur la réserve supplémentaire, la règle réussit 70 fois sur 88 (79,5 %), contre 45 sur 88 (51,1 %) en prédisant systématiquement *m*. Parmi les prédictions *m*, la lecture éditoriale donne 40 *m*, 5 *er* et 1 *ne*. Parmi les prédictions *n*, elle donne 30 *n*, 5 *m* et 7 *au*. En particulier, plusieurs des 18 désaccords peuvent appartenir à d’autres abréviations, ce qui limite l’interprétation de ce taux comme mesure d’un signe visuel.

## Un contre-exemple visible

Au f.120v, *su[m]nors* (Hm.2.170) et *sy[n]ne* (Hm.2.175) portent un trait courbe sur la voyelle devant un *n* visible. La même opération propose *n* dans les deux cas. Elle échoue sur le premier et réussit sur le deuxième. Le contexte du mot et la langue font donc partie de la décision éditoriale. Les rectangles dans l’image originale de 3 300 pixels de hauteur sont respectivement [359, 428, 512, 523] et [1061, 710, 1199, 818], dans l’ordre gauche, haut, droite, bas. Deux autres exemples de cette difficulté, *buxu[m]nesse* (117r, Hm.1.108) et *su[m]ne* (120r, Hm.2.159), ont également été vérifiés sur les photographies. [Photographie du f.120v](https://piers.chass.ncsu.edu/media/images/manuscripts/B/Hm/folios/Hm120v.jpg)

Les empreintes des transcriptions, photographies et scripts figurent dans `sources.sha256`. Les réponses du contrôle visuel, les références des vers et les coordonnées en pixels des mots se trouvent dans `answer-key.json`. Le script `assess_hm.py` génère les observations du premier contrôle à partir de `HmWhole.xml`. La fonction `process` prend aussi une liste explicite de faces pour reproduire l’épreuve supplémentaire. Les statistiques portent sur des annotations de l’édition, comparées localement à des photographies. Les lecteurs qui reconnaissent le signe doivent encore identifier si la consonne visible est *m* ou *n* pour pouvoir appliquer la règle à une autre écriture.
