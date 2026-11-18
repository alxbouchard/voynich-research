# Deux plantes à baies et un groupe retrouvé sur les panneaux prédits

La proposition latine *flos florum*, « fleur des fleurs », à f52v.4 suggère une fleur dans le dessin. Nous avons testé si les mots `ctheor` ou `ctheol` annonçaient une corolle sur d’autres pages de plantes. Une autre ressemblance, les baies visibles aux bras de deux plantes, a ensuite permis de prédire un mot entier dans la prose de **deux panneaux choisis à partir de leur dessin**. [Prédiction initiale](AVANT.md) · [Les quatre plantes entières et leurs détails](quatre-plantes.jpg)

## Où devrait-on voir une corolle ?

Après retrait de f52, les deux mots apparaissent quatre fois dans les 8 533 positions concordantes de prose des 126 faces botaniques avec au moins un mot lisible. Les quatre lectures doivent retrouver la forme entière à la même position matérielle. La table donne tous les cas.

| Page, rang dans la ligne | Forme | Observation |
|---|---|---|
| f17v.11, 3 | `ctheol` | Grappes de petites baies. Dans les 45 pages déjà cotées à l’aveugle, deux lecteurs avaient répondu « non » à la corolle en rosette. |
| f28r.2, 5 | `ctheol` | Tige portant des formes striées et une extrémité ocre et rouge. Statut floral indéterminé. |
| f96r.6, 6 | `ctheor` | Gros organe pendant, à bords recourbés. Statut floral indéterminé. |
| f96v.10, 1 | `ctheor` | Deux tiges pendantes portent des grappes arrondies. Aucune corolle ouverte visible. |

Dans les 45 pages du premier registre, il y avait 11 corolles en rosette, 28 absences et 6 cas sans consensus. Seul f17v porte un mot cible. Hors de ce registre, le critère admettait aussi une corolle ouverte non circulaire. Un lecteur IA qui a reçu uniquement les détails anonymisés a considéré indéterminées les deux structures singulières et reconnu les deux grappes sans corolle. Les notices publiées de f17v et de f96v signalent les baies, celle de f28r laisse ouverte l’alternative entre fleur et fruit, celle de f96r décrit un bulbe. Les mêmes dessins peuvent évidemment accompagner un texte qui parle d’organes absents de l’image. En lecture moins stricte, f22r.9 donnerait aussi `ctheor`, mais ZL indique `ctheo,r` et le groupe se scinde lorsqu’on sépare ce blanc. Les deux votes antérieurs de f22r étaient « non ». [Tous les comptes et votes antérieurs](RESULTATS.json) · [Quatre détails anonymes](organes-anonymes.jpg) · [Bulletin du lecteur](LECTURE-ANONYME.json) · [Description de f28r](https://www.voynich.nu/q04/index.html#f28r) · [Description de f96r](https://www.voynich.nu/q17/index.html#f96r)

## Les deux panneaux désignés par le rapprochement visuel

Le catalogue rapproche la plante de f17v de celle de f96v et du fragment inférieur de f99r. La notice de f96v précise son numéro, 94, et renvoie aussi au fragment 116 sur f100r. Nous avions déjà ouvert les quatre grandes plantes. Avant de rechercher les mots sur ces deux panneaux, nous avons annoncé pour chacun `ctheol` ou `ctheor` dans la légende du fragment et dans la prose du panneau. Ces dessins et leurs inscriptions figuraient déjà dans les recherches antérieures. Les annonces documentent l’ordre de ce nouveau test. [Notice de f17v](https://www.voynich.nu/q03/index.html#f17v) · [Deux renvois de f96v](https://www.voynich.nu/q17/index.html#f96v) · [Annonce pour le fragment 94](BAIES-AVANT.md) · [Annonce pour le fragment 116](DEUXIEME-FRAGMENT-AVANT.md)

| Fragment | Légende sur le scan | Prose du panneau |
|---|---|---|
| 94, au bas de f99r | `tolsasy`, f99r.46 | `ctheol` au **5e mot** de f99r.29, environ 938 pixels plus haut que la légende. |
| 116, en haut de f100r | `sochorcfhy`, f100r.2 | `ctheol` au **5e mot** de f100r.25, environ 2 462 pixels plus bas que la légende. |

La prédiction réussit pour les deux panneaux en prose et échoue pour les deux légendes. Les deux pages sont de hauteur voisine de 3 760 pixels. Les changements de rangée entre dessin et mot rendent l’attache à un fragment précis incertaine. On voit des grappes pendantes sous le fragment 94. Le 116 porte des feuilles triangulaires et sa tige se recourbe. Ces indices de comparaison visuelle n’imposent ni l’identité botanique des dessins ni une lecture « baie ». [Pages entières, légendes et agrandissements des deux lignes de dix mots](deux-panneaux.jpg) · [Attributions des étiquettes aux fragments](../../../2026-11-18-noms-dans-les-notices/registre/registre.json)

Sur les 15 panneaux associant fragments et lignes de prose, cinq portent au moins une des deux formes. Dix des 105 paires de panneaux les portent donc sur les deux faces. Dans le seul cahier de f99r et f100r, six des 36 paires remplissent ce critère. En redistribuant les quatre occurrences de ce cahier parmi ses 738 positions lisibles, la probabilité que les deux faces visées en reçoivent chacune au moins une est de 15,0 %. Ce calcul tient compte de leurs longueurs (123 et 73 positions), tandis que les regroupements par ligne ou par sujet peuvent modifier cette fréquence. Ces références sont descriptives. [Comptages et calcul exact](PANNEAUX.json)

Le cinquième rang a été découvert après avoir vu les deux lignes. Avant de rechercher les autres occurrences, nous l’avons annoncé sur les onze panneaux restants, en retirant les feuillets 99 et 100 entiers. La seule autre occurrence de `ctheol` est **deuxième** sur f88r.7. L’autre forme `ctheor` est **sixième ou septième** sur f102v2.34, selon les transcriptions. La prédiction du cinquième rang échoue donc à toutes les occurrences sur des feuillets distincts. Sur ces 819 places lisibles, 64 sont des cinquièmes rangs et 89 des premières places. En ne gardant que les lignes de dix mots aux quatre lectures, comme les deux lignes de découverte, il reste 70 places, dont 8 cinquièmes et 5 premières. Aucune ne porte les mots cherchés. [Annonce sur les autres feuillets](CINQUIEME-AVANT.md) · [Les cinq occurrences, les rangs dans la ligne et les deux contrôles](PANNEAUX.json)

Les calculs se reproduisent avec Python 3 depuis ce dossier par `python3 -B compter.py` puis `python3 -B panneaux.py`. Télécharger les six vues natives de Yale sous le nom du panneau suivi de `-n.jpg`, puis exécuter `python3 -B planches.py /chemin/vers/les/images` avec Pillow. Le programme vérifie les empreintes du registre de Yale. [Sources, coordonnées des mots et dimensions](SOURCES.json) · [Calcul sur les panneaux](panneaux.py) · [Montage des photographies](planches.py)
