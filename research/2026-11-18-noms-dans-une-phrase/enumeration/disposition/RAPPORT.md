# La légende se retrouve-t-elle dans le paragraphe juste au-dessus ?

Sur f99r, la légende de dessin `okeoly` est juste sous la dernière ligne du paragraphe qui contient le même mot. **La disposition ne se répète dans aucune des quatre rangées intérieures réservées lorsqu’on exige des mots entiers dont la lecture et la coupure concordent.** À quantité de texte égale, les huit formes de ces rangées ont été cherchées dans 74 positions au-dessus et 74 au-dessous. Les deux côtés donnent zéro reprise. Une lecture moins stricte retrouve un mot d’étiquette sur f89r1, trois fois au-dessus et une fois au-dessous. [Prédiction antérieure au calcul](PROTOCOLE.md) · [Résultats, légendes et limites des paragraphes](RESULTATS.json) · [Photographie du cas initial](../photo/rang-10.jpg)

## Les quatre rangées réservées

Le registre de géométrie permet une comparaison lorsque l’on connaît à la fois le paragraphe immédiatement au-dessus et celui immédiatement au-dessous. Les limites des deux paragraphes devaient aussi être reconnues aux mêmes lignes dans les transcriptions H et ZL. Les pots sont exclus des légendes, ainsi que tout le feuillet 99. Sur les treize inscriptions de fragments des quatre rangées admises, sept livrent au moins une forme entière de trois unités EVA ou davantage dans les deux éditions et les deux traitements du blanc incertain. Elles fournissent huit mots à chercher. Les positions prises en compte dans la prose sont celles où le mot entier concorde au même rang dans les quatre lectures. [Table photographique des rangées](../../../2026-11-18-paires-ingredients/rangees/rangees.tsv) · [Description des panneaux](../../../2026-11-18-paires-ingredients/rangees/README.md)

| Panneau et rang du dessin | Lignes au-dessus | Lignes au-dessous | Mots de légende comparés | Places recevables au-dessus / au-dessous | Places comparées de chaque côté à longueur égale |
|---|---|---|---|---:|---:|
| f88v, 2 | 6–10 | 15–20 | `cheosdy`, `okaiin` | 16 / 25 | 16 |
| f89r1, 2 | 6–10 | 15–18 | `otorain` | 28 / 13 | 13 |
| f89r2, 2 | 6–8 | 12–15 | `okol`, `shol` | 13 / 32 | 13 |
| f89r2, 3 | 12–15 | 22–28 | `sodar`, `cheys`, `cheody` | 32 / 38 | 32 |
| **Total** | | | **8** | **89 / 108** | **74** |

Les paragraphes entiers donnent également zéro des deux côtés. La dernière ligne du paragraphe supérieur livre treize positions recevables pour les quatre rangées réunies, la première du paragraphe inférieur en livre vingt-cinq. Aucune des deux ne porte de reprise. La comparaison des cinq places recevables les plus proches de chaque côté donne 0/20 et 0/20. La première ligne supérieure et la dernière inférieure donnent elles aussi zéro, sur dix-sept et deux places recevables respectivement. L’écart des dénominateurs tient à la longueur des lignes et au nombre de mots dont la lecture et le rang concordent. En autorisant un mot à changer de rang entre les éditions **dans une même ligne**, les quatre lectures ne fournissent toujours aucun mot de légende en commun avec cette ligne. [Mesures de proximité et résultats par ligne](RESULTATS.json)

Dans le registre élargi, le rang inférieur de f102v2 est bordé par les blocs 17–23 et 30–39. Les deux lectures de f102v2.27 et .28 donnent `okeeoraiin` et `okockhy`. H divise le bloc inférieur après la ligne 36, tandis que ZL le laisse entier. Son ajout porte le total équilibré à 96 places de chaque côté, sans reprise. [Table par pot](../../../2026-11-18-paires-ingredients/rangees/pots_elargis.tsv) · [Limites et mesures du panneau supplémentaire](RESULTATS.json)

## L’effet d’un blanc incertain à f89r1.12

Après le résultat principal, nous avons levé l’exigence de concordance et relu ces quatre rangées dans chaque édition séparément. En H la première légende de la deuxième rangée de f89r1 est `chol.ches` et en ZL `chol,ches`. Le point marque une coupure, la virgule un blanc incertain. Quand `chol` forme un mot, il revient deux fois à la ligne 8 et une fois à la ligne 10 du paragraphe **au-dessus**. On le lit également une fois à la ligne 16 **au-dessous**. Les mots de prose existent à ces trois lignes dans H comme dans ZL. C’est la coupure de la légende qui décide de cette comparaison. Les deux groupes réunis dans ZL ne reparaissent dans aucun des deux paragraphes. Sur f89r2, H ajoute une correspondance au-dessous de la rangée 2, avec `shol` à la ligne 13. À cette même place, ZL lit `chol`. [Détail des vérifications par transcription](RESULTATS.json) · [Calcul reproductible](comparer.py)

| Lecture séparée | Places de prose au-dessus / au-dessous, paragraphes entiers | Reprises au-dessus | Reprises au-dessous |
|---|---:|---:|---:|
| H, blancs incertains joints ou séparés | 194 / 258 dans chaque traitement | 3 | 2 |
| ZL, blancs incertains joints | 174 / 220 | 0 | 0 |
| ZL, blancs incertains séparés | 188 / 242 | 3 | 1 |

Le programme retrouve bien le cas initial `okeoly` au huitième rang de f99r.18 dans les quatre lectures. Les quatre rangées du test strict, elles, occupent trois panneaux de seulement deux feuillets matériels. À f89r2 les deux rangées partagent même un paragraphe. Les données de rangées situent les dessins et la prose dans le sens vertical, sans indiquer si un mot se trouve à l’aplomb d’un dessin particulier. Avec ces limites, le cas de f99r reste une observation locale et la coupure de f89r1.12 autorise une reprise de part et d’autre. [Vérification visuelle de f99r.18](../photo/NOTE.md) · [Reproduction avec `python3 comparer.py`](comparer.py)
