# La paire de cinq signes communs revient-elle sur une autre page ?

Dans la prose de f89r2.22, `opcheor` précède `opcheol`. Les deux transcriptions principales placent le premier mot au cinquième rang. Les cinq unités communes sont `o · p · ch · e · o`. **En excluant tout le feuillet physique 89, aucune paire de mots voisins ne présente ailleurs un préfixe identique d’au moins cinq unités et les finales opposées `r` et `l`.** Ce constat vaut pour les deux ordres en prose, dans les cercles et dans les autres inscriptions, sous les quatre conventions étudiées. Avec un préfixe de quatre unités, on retrouve un exemple très proche sur une autre page pharmaceutique. [Protocole](PROTOCOLE.md) · [Données, rangs et lieux](resultats.json)

## Un deuxième passage pharmaceutique

En f100v.16, les deux éditions donnent la suite `okeor okeol`. Les mots occupent les rangs 8–9 chez Takahashi et en ZL avec blancs douteux joints, puis 9–10 en ZL avec séparation du blanc plus tôt dans la ligne. Le contexte immédiat concordant autour du couple est `ches okeor okeol dy`. Comme à f89r2.22, les deux groupes se terminent respectivement en `eor` et `eol`. Le début de f100v présente `o-k` à la place de `o-p-ch`. Cela fournit une seconde paire où éprouver des valeurs proposées pour `e`, `o`, `r` et `l`. Ces feuillets appartiennent au même manuscrit et le deuxième passage a été repéré en cherchant cette forme. [Texte de Zandbergen–Landini](../../../voynich_20261028/data/ZL3b-n.txt) · [Texte de Takahashi](../../../voynich_20261028/data/IT2a-n.txt)

Les quatre conventions se rejoignent au même locus pour 35 couples de prose ayant au moins deux unités communes. 24 ont un préfixe de longueur deux, sept de longueur trois et quatre de longueur quatre. Ces quatre derniers sont `okeor okeol` à f100v.16, `qokar qokal` à f107v.14 et f81v.19, puis `okchal okchar` dans l’autre sens à f52r.5. Hors prose, les conventions concordent pour `dal dar` au locus radial f69r.26. Le tableau détaillé conserve les rangs et les écarts de segmentation. [Inventaire des couples](resultats.json)

## Observations et effectif attendu hors f89

| Lecture de la prose P0 | Voisinages lisibles | r→l / l→r, préfixe ≥2 | Attendu par sens, ordre mélangé | Attendu par sens, longueurs également fixes | r→l / l→r, préfixe ≥5 | Attendu par sens ≥5, ordre mélangé / longueurs fixes |
|---|---:|---:|---:|---:|---:|---:|
| Takahashi, deux conventions | 28 124 | 26 / 20 | 19,03 | 22,47 | 0 / 0 | 0,40 / 0,25 |
| ZL, blancs joints | 25 167 | 19 / 20 | 15,38 | 18,00 | 0 / 0 | 0,325 / 0 |
| ZL, blancs séparés | 27 476 | 21 / 21 | 17,99 | 21,04 | 0 / 0 | 0,20 / 0 |

Dans la prose ZL avec blancs joints, 1 253 voisinages réunissent deux mots de même longueur d’au moins six unités. Parmi eux, 12 présentent déjà les finales r→l et 5 les finales l→r. Aucun ne partage en outre son préfixe entier. En ne gardant que la longueur de la paire de départ, exactement six unités par mot, on obtient 928 paires de même longueur, dont 11 r→l et 4 l→r. L’effectif attendu sous permutation vaut déjà moins de un pour la condition de préfixe long. Son absence sur les autres pages reste compatible avec la rareté des formes disponibles.

| Prose ZL avec blancs joints, hors f89 | Voisinages lisibles | r→l / l→r, préfixe ≥2 | Attendu par sens à longueurs fixes |
|---|---:|---:|---:|
| Grandes plantes, code H | 7 845 | 12 / 14 | 10,63 |
| Section pharmaceutique, code P | 1 287 | 3 / 0 | 1,10 |
| Cahier final, code du cahier T | 8 663 | 2 / 2 | 2,35 |
| Autres pages avec prose P0 | 7 372 | 2 / 4 | 3,92 |

Les douze panneaux du zodiaque n’ont pas de locus P0. Leurs 36 lignes circulaires donnent 745 voisinages lisibles dans ZL avec blancs joints et les 299 légendes en donnent 34. Aucun n’atteint deux unités de préfixe commun avec l’alternance. Les comptes par type, édition et espace figurent dans le relevé.

## Comment interpréter la comparaison

Le calcul conserve des tronçons de groupes lisibles au sein d’une même ligne. Un groupe incertain, un code de dessin ou un blanc explicitement signalé comme large interrompt le tronçon. Les espaces douteux ordinaires sont joints ou séparés. Les deux conventions Takahashi sont identiques pour ce corpus. Une unité de transcription peut réunir plusieurs traits et sa valeur phonétique est inconnue. Une transcription ancienne donne `opchear` au premier mot et une autre `opiol` au second. La longueur de cinq repose donc sur la lecture des deux éditions principales. [Photographie et anciennes variantes](../../2026-11-18-legendes-et-paragraphes/lecture/LECTURE.md)

Pour un tronçon de *n* mots dont *a* finissent par r et *b* par l après un préfixe donné, la permutation uniforme des mots y produit *ab/n* voisinages attendus dans chaque sens. Le deuxième contrôle fixe également la longueur à chaque position. S’il y a *m* mots de la longueur examinée et *s* créneaux adjacents de cette même longueur, la contribution du préfixe est *s·a·b/[m(m−1)]*. Les cas avec moins de deux mots correspondants ont une contribution nulle. Le programme vérifie les deux formules sur toutes les permutations de petits exemples avant de traiter le manuscrit. Les effectifs attendus sont des moyennes conditionnelles. Les deux transcriptions et les variantes de blancs ne sont pas des échantillons indépendants.

Depuis ce dossier, exécuter `python3 -B compter.py` pour recalculer l’inventaire. Les entrées sont les deux transcriptions IVTFF incluses et vérifiées par empreinte dans le dépôt. [Programme](compter.py)
