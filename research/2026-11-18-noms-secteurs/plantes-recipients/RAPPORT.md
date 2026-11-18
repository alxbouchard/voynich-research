# Auprès des fragments végétaux et des récipients

Sur les feuillets autres que 88, 89, 99 et 101, **une seule inscription se prête à la lecture proposée dans une seule des deux éditions**. Il s’agit de la légende du cinquième végétal de la première rangée de f102v2, près d’une petite feuille. Zandbergen–Landini lit `okol`, Takahashi lit `otol`. Les trois entrées de l’interlinéaire ancien de Stolfi à cette position lisent également `otol`. Le dessin rend plausible l’appartenance de l’inscription à un fragment végétal. Il ne tranche ni la forme du deuxième signe ni le sens du mot. [Catalogue du panneau, fragment 218](https://www.voynich.nu/q19/index.html#f102v2) · [Interlinéaire, lieu L1.5](https://www.voynich.nu/q19/f102v2_tr.txt) · [Fac-similé Yale](https://collections.library.yale.edu/catalog/2002046?child_oid=1006252)

## Le lot hors des feuillets d’origine

Les deux candidats, `otoldy` et `okol`, avaient été repérés sur les feuillets 88, 89, 99 ou 101. Nous avons fixé l’exclusion de ces **feuillets physiques entiers** avant de calculer les nouvelles proportions. Le feuillet 100 porte des récipients dessinés, mais ses deux faces ont uniquement des étiquettes de fragments dans les éditions. Seul le feuillet 102 offre des étiquettes des deux types. Il s’agit de plusieurs panneaux d’un même feuillet, conjugué du 99. L’analyse antérieure des fragments avait déjà parcouru une partie du matériel de ce lot. [Règle enregistrée](PROTOCOLE.md) · [Anatomie des feuillets 99 et 102](https://www.voynich.nu/q19/f102v2_tr.txt) · [Comparaison antérieure](../../2026-11-18-mots-et-dessins/RAPPORT.md)

Une touche signifie qu’une ligne lisible comporte au moins un des deux mots entiers, y compris dans une légende de plusieurs mots. Le tableau exclut les faces où l’une des deux classes n’a aucune ligne lisible dans la convention concernée.

| Lecture | Panneaux comparables | Touches / lignes de fragments | Touches / lignes de récipients |
|---|---:|---:|---:|
| Accord intégral H et ZL | 1 | 0/11 | 0/1 |
| Takahashi | 2 | 0/17 | 0/6 |
| Zandbergen–Landini | 4 | 1/26 | 0/9 |

La seule touche de ZL tombe sur un panneau où cette édition offre 16 lignes lisibles de fragments et 3 de récipients. En permutant la position du mot sur ce panneau, il tomberait près d’un fragment **16 fois sur 19**, soit **84,2 %**. Contrôler le nombre de mots de chaque ligne donne le même résultat. Toutes les lignes comptées dans ce lot ont un seul mot, hormis une ligne de récipient à deux mots chez Takahashi. Séparer les espaces douteux laisse le tableau inchangé. En lecture concordante, le corpus hors origine ne départage donc pas les deux usages supposés. [Effectifs, mots disponibles et réattributions exactes](resultats.json) · [Loci individuels](loci.tsv)

## En incluant les exemples d’origine

Avec accord intégral et espaces douteux joints, les neuf panneaux qui comportent les deux classes lisibles donnent **5/96** lignes de fragments (103 mots) et **0/21** lignes de récipients (21 mots). Les cinq touches sont sur des feuillets déjà utilisés. La réattribution sur les mêmes faces attend en moyenne **4,01 des 5** près de fragments. Elle donne cinq touches végétales dans **32,2 %** des réattributions. En conservant aussi la longueur des lignes, cette proportion atteint **40,3 %**. Avec espaces séparés, les comptes deviennent 5/99 contre 0/21. Les catégories décrivent les objets voisins et aucune ne sépare racine, feuille et plante entière. [Toutes les conventions et probabilités](resultats.json)

| Groupe | Lignes de fragments concordantes sur faces mixtes | Lignes de récipients concordantes |
|---|---|---:|
| `otoldy` | f89r1.4, f99r.14, f99v.2 | 0 |
| `okol` | f88r.15, f89r2.10 | 0 |

La lecture d’un récipient illustre la fragilité du zéro. À f89r2.9, Takahashi donne `otoldy`. ZL encode deux lectures, `otold` et `otoldy`. La règle stricte écarte ce locus dans ZL et dans le calcul concordant. Au locus suivant, f89r2.10, les deux éditions placent `okol` dans une inscription de fragment. Hors des faces comparables, f101v.10 porte aussi `okol` près d’un fragment. Aucun récipient étiqueté ne permet un contrôle sur cette face. Le vieux relevé alphabétique et l’interlinéaire emploient une autre numérotation. À f99v, l’interlinéaire place une étiquette de récipient distincte avant l’inscription `otoldy` de la rangée. Les dossiers photographiques montrent la proximité du récipient et de la racine à cet endroit. [Inventaire de Stolfi](https://www.ic.unicamp.br/~stolfi/EXPORT/projects/voynich/00-EXPORT/98-02-01-lotsa-labels/labels-a.html) · [Interlinéaire de f99v](https://www.voynich.nu/q19/f099v_tr.txt) · [Photographies de f99](../../2026-11-18-mots-des-images/racines/photos/F99_NOTICE.md)

## Sources et reproduction

L’IVTFF fournit l’attribution aux objets indépendamment du programme qui recherche les deux mots. Les codes spécialisés Lf et Lc désignent respectivement une légende de fragment végétal et une légende de récipient. Le simple numéro de la ligne ne donne aucune information de ce genre. À f102v2, le catalogue compte 19 lignes de fragments et 3 de récipients, réparties auprès de 19 fragments et **deux** récipients dessinés. Une ligne permet donc de compter le texte disponible. Plusieurs lignes peuvent se rapporter au même objet. Les deux éditions partagent une partie de ces annotations et la même image. [Définition IVTFF, tableaux 8 et 9](https://www.voynich.nu/software/ivtt/IVTFF_format.pdf#page=22) · [Cahier 15](https://www.voynich.nu/q15/index.html) · [Cahier 19](https://www.voynich.nu/q19/index.html) · [Takahashi](https://www.voynich.nu/data/IT2a-n.txt) · [Zandbergen–Landini](https://www.voynich.nu/data/ZL3b-n.txt)

Pour reproduire les tableaux, exécuter `python3 compter.py` depuis ce dossier. Le programme énumère la distribution hypergéométrique dans chaque strate puis combine les distributions par convolution exacte. Le fichier des résultats contient les empreintes des éditions et du protocole, ainsi que les distributions rationnelles. Le protocole gelé avant décompte a pour empreinte `f4deb14978a38358e8a8417cd2296d73ba062c3e890dfb8b1750ecd261291e56`. [Calcul](compter.py) · [Données par locus](loci.tsv)

## Les deux lectures revues sur les photographies de Yale

Sur f102v2.7, deux lecteurs IA ont classé séparément le signe contesté parmi des témoins anonymisés. Ils y voient tous les deux une boucle à gauche et une à droite, et choisissent `t`. Ils reconnaissent le témoin `k` et laissent indéterminé l’autre témoin `t`. Cela favorise `otol` sur la feuille nº 218. Sur f89r2.9, une relecture informée retrouve une descente pâle après `d`. La position, près du couvercle, correspond à celle de la légende du pot de la rangée supérieure. La plante voisine a sa propre légende. Cela favorise `otoldy` auprès du pot, avec une incertitude sur la finale. [Carte de la feuille et votes](graphie218/NOTE.md) · [Deux rangées avec les pots](pot89/NOTE.md)

Le tableau ci-dessous réintègre uniquement ces deux lignes à la série concordante à espaces joints. Le total comprend les feuillets d’origine et la fréquence cumulée des deux candidats (`otoldy`, `okol`). Le sens des mots reste ouvert dans les quatre cas. La dernière colonne est la proportion exacte de redistributions qui atteignent au moins le nombre observé de rencontres végétales, à face et longueur de légende conservées.

| Lecture f102v2.7 | Lecture f89r2.9 | Fragments | Pots | Proportion |
|---|---|---:|---:|---:|
| `otol` | `otoldy` | 5/97 | 1/22 | 70,7 % |
| `otol` | `otold` | 5/97 | 0/22 | 40,3 % |
| `okol` | `otoldy` | 6/97 | 1/22 | 67,5 % |
| `okol` | `otold` | 6/97 | 0/22 | 37,2 % |

La première ligne correspond aux graphies favorisées sur photographie. Avec ces deux lectures, les taux sont respectivement 5,2 % et 4,5 %. Le peu de récipients et la dépendance entre feuillets limitent la précision. Aucune des quatre lectures ne fournit d’argument solide pour réserver ces graphies aux végétaux. [Quatre calculs exacts](variantes_photo.json) · [Reproduction](variantes_photo.py)
