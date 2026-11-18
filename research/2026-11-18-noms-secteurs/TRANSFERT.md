# Les légendes des deux autres roues reparaissent-elles sur les rayons ?

Sur **f67v1**, aucun groupe de légende n’est répété à l’identique dans les rayons étudiés, même en comparant chaque cartouche à toutes les destinations. Sur **f69r**, la lecture prudente de Zandbergen–Landini ne donne aucune reprise dans la case attendue. Takahashi en donne deux dans des rayons strictement en face et une troisième lorsque les rayons de frontière sont admis. Les trois occurrences dépendent de la lecture ou de la séparation des signes. Aucune légende entière ne se retrouve sur un rayon associé, dans les deux éditions et les variantes testées. [Cartes fixées avant lecture](geometrie/README.md) · [Résultats complets](transfert.json)

| Panneau et attribution | Édition | Légendes comparables | Exact | Base | Trois premières unités |
|---|---|---:|---:|---:|---:|
| f69r, rayons intérieurs | ZL | 12/16 | 0 | 0 | 0 |
| f69r, rayons intérieurs | IT | 12/16 | 2 | 2 | 0 |
| f69r, frontières admises | ZL | 16/16 | 0 | 0 | 0 |
| f69r, frontières admises | IT | 16/16 | 3 | 3 | 1 |
| f67v1, axe dans le cadre | ZL | 12/12 | 0 | 0 | 0 |
| f67v1, axe dans le cadre | IT | 11/12 | 0 | 0 | 0 |

Le tableau emploie les espaces douteux joints, écarte les groupes à lecture incertaine, décompose les signes selon EVA et porte sur toutes les positions. Sur f69r, 13 rayons intérieurs desservent 12 cases et neuf rayons de frontière portent deux attributions possibles chacun. Sur f67v1, le cartouche .6 est illisible en partie dans IT. L’ajout du rayon qui effleure le douzième cartouche conserve tous les scores locaux de cette page.

### Les trois cas de f69r

| Groupe dans IT | Légende et rayon | Ce qui change dans ZL |
|---|---|---|
| `ar` | .14, groupe 2 → .33, groupe 4 | La fin du rayon se lit `a[r:s]`. Le choix de la première variante restitue l’accord. |
| `al` | .18, groupe 2 → .39, groupe 2 (également .38, groupe 2 à la frontière) | La légende se lit `dair,alody`. Même en séparant l’espace douteux, la seconde partie est `alody`. |
| `dar` | .7, groupe 2 → .24, groupe 4 à la frontière | Les deux espaces de `al,dair,dar` sont douteux. Leur séparation isole le dernier groupe. |

Sur les 16 rotations de la couronne de f69r, trois égalent ou dépassent les deux accords exacts intérieurs d’IT. En attribuant librement les 16 destinations, cette proportion vaut 21,0 %. Elle vaut 29,7 % si l’on permute uniquement les 12 légendes et les 12 destinations comparables. En incluant les frontières, huit rotations sur 16 et 52,0 % des permutations égalent ou dépassent les trois accords. Dans cette dernière matrice, chacune des trois légendes retrouve au moins un de ses groupes dans plusieurs cases. Les deux roues démontrent une organisation spatiale. Ces accords ne permettent d’identifier ni le nom d’un secteur ni la fonction grammaticale du groupe.

Les trois règles, les deux écritures informatiques (EVA et ASCII), les deux traitements de l’espacement, trois traitements des variantes et les fenêtres de huit groupes ou de la totalité des rayons ont été repris de l’essai sur f67r2. Sur f69r, les alternatives de ZL portent le score exact jusqu’à 1/12 en strict et 2/16 avec les frontières. La meilleure proportion nominale de permutations pour l’ensemble des lectures, règles et panneaux est de 21,0 %. Les 576 combinaisons réutilisent les mêmes inscriptions. Pour f67v1, la matrice exacte complète reste nulle dans les deux éditions pour toutes les variantes. La position réelle ne discrimine donc aucune destination par identité sur ce panneau.

Le fichier JSON donne, pour chaque scénario, la matrice binaire sous forme de masques, toutes les rotations, la distribution des scores de toutes les permutations et les loci des rencontres locales. Les zéros de la géométrie stricte sont conservés dans les rotations et dans la distribution sur l’ensemble des cases. Une seconde distribution conditionne sur les cases dont les deux côtés sont comparables. Les positions se lisent dans l’ordre des loci donné par `ordre_loci`. Les scénarios dont les sorties sont identiques partagent le même enregistrement. Le calcul vérifie la distribution sur de petites matrices par énumération directe et contrôle chaque moyenne de permutation à partir de la somme des rotations. [Programme](transfert.py) · [Règles originales](secteurs.py) · [Protocole](PROTOCOLE.md)
