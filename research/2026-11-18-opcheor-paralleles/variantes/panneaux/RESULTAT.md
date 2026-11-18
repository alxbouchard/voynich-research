# Cette relation entre légende et prose revient-elle sur un troisième panneau ?

**Sur 15 panneaux de fragments végétaux, la règle retrouve les deux exemples qui ont servi à la formuler. Elle n’en retrouve aucun troisième.** Les 130 légendes entières retenues se répartissent sur six panneaux du cahier O et neuf du cahier S. Seuls trois de ces panneaux contiennent une paire de prose admissible. Les quatre emplacements de ces paires se répartissent sur deux feuillets physiques, f89 et f100. [Règle fixée avant le dépouillement](PROTOCOLE.md) · [Tous les lieux et toutes les comparaisons](resultats.json)

| Panneau de prose | Paires contiguës r puis l dans les quatre lectures | Résultat avec les légendes du panneau |
|---|---|---|
| f89r2 | `opcheor opcheol` en .22 | La légende f89r2.5, `opcheor`, donne exactement le premier mot. |
| f100v | `okeor okeol` en .16 | La légende f100v.10, `okcheor`, donne le premier mot en retirant une seule unité `ch`. [Photographies du fragment et de la ligne](../photo-f100v/LECTURE.md) |
| f100r | `chor chol` en .15 et .23 | Aucune des 13 légendes entières ne donne `chor`, soit directement, soit après retrait de `ch`. |

Sur les douze autres panneaux, la prose manque d’une paire lisible avec ce critère. Toute paire doit partager un préfixe d’au moins deux unités EVA. Une légende compte seulement si elle est lisible comme un groupe entier identique en H et ZL sous les deux conventions de blancs. Le premier et le second groupe de prose doivent être directement consécutifs au même locus dans les quatre lectures. Un dessin, une interruption ou un signe illisible empêche de raccorder les mots à travers lui.

| Comparaison | Couples de panneaux | Couples ayant une légende et une paire utilisables | Comparaisons d’une légende avec une paire | Succès exact | Succès après retrait de ch |
|---|---:|---:|---:|---:|---:|
| Légendes et prose du même panneau | 15 | 3 | 46 | 1 | 1 |
| Légendes et prose de panneaux différents du même cahier | 102 | 21 | 262 | 0 | 0 |

Changer les légendes de panneau ne donne aucune autre rencontre, y compris entre f100r et f100v. Le seul panneau supplémentaire où la règle pouvait effectivement réussir est le recto du feuillet qui porte déjà l’un des exemples de départ. Il reste donc très peu de possibilités de vérification indépendante. La suppression de `ch` représente une opération comparative choisie après la découverte, dont la fonction historique reste inconnue.

Depuis ce dossier, `python3 -B verifier.py` reconstruit les deux tableaux à partir des transcriptions intégrales conservées dans le dépôt. Les lieux, leurs rangs dans les quatre lectures et les groupes source de toutes les rencontres figurent dans le JSON. [Programme](verifier.py)
