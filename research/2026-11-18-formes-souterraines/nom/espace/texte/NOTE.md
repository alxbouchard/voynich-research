# Les deux derniers mots des légendes voisines réapparaissent-ils ensemble ?

**L’exemple de f89r2 est retrouvé dans la transcription de Takahashi. Aucun nouveau cas ne se présente sur les huit autres panneaux**, dans les deux éditions et avec les deux conventions de séparation. Au total, le contrôle externe porte sur 13 rangées de 57 fragments comportant 44 voisinages physiques et sur 130 lignes de prose. [Prédiction fixée au commit 3c15bdf](../PREDICTION.md)

## Ce qui se lit sur f89r2

Takahashi (IT2a, H) sépare les groupes `saloiin.sheol` sur la légende f89r2.4. Le dernier groupe est donc `sheol`. En ZL3b, la même inscription donne `saloiinsheol`, même lorsque les espaces douteux sont séparés. Sur la légende suivante, f89r2.5, les deux éditions lisent `opcheor`.

Dans la prose de **f89r2.22**, les deux éditions donnent bien `sheol` au **rang 2** et `opcheor` au **rang 5**. Les deux groupes intercalés sont `qokeoefy` et `sheey`. L’incertitude porte donc sur la séparation des mots dans la première légende. La géométrie distingue aussi deux lieux. Les deux fragments appartiennent à la première rangée, dont le paragraphe occupe les lignes 6–8. La ligne 22 ouvre le paragraphe de la troisième rangée. Dans le paragraphe attribué à la première rangée, aucune reprise de cette paire n’apparaît.

Les 15 étiquettes du panneau source forment 11 voisinages dans quatre rangées, dont dix admissibles pour chaque édition et convention. Sur les 14 lignes P0 du panneau, le rapprochement relevé en H est l’unique reprise. Sur les trois paragraphes géométriquement attribués, aucune des sept paires admissibles dotées d’un paragraphe ne se retrouve dans son propre paragraphe. L’ordre inverse ne produit aucun cas.

## Transfert à huit autres panneaux

Les deux mots terminaux devaient être lisibles, distincts et longs d’au moins trois unités EVA. Les deux étiquettes devaient être physiquement voisines dans la table des rangées. Une étiquette incertaine garde sa place. Ainsi, le dernier mot incertain de f89r1.26 en ZL écarte les deux voisinages f89r1.25/.26 et f89r1.26/.27. Les deux fragments de part et d’autre du milieu restent distants. L’inscription en deux lignes de f99r.6 et .7 est traitée comme une seule étiquette.

| Édition et convention | Paires admissibles / 44 | Paires avec paragraphe local | Comparaisons paire–ligne sur le panneau | Comparaisons paire–ligne dans son paragraphe | Reprises directes ou inverses |
|---|---:|---:|---:|---:|---:|
| H, blancs joints | 40 | 27 | 673 | 152 | 0 |
| H, blancs séparés | 40 | 27 | 673 | 152 | 0 |
| ZL, blancs joints | 36 | 26 | 613 | 144 | 0 |
| ZL, blancs séparés | 34 | 25 | 579 | 138 | 0 |

Sur les 44 voisinages externes, 35 sont admissibles dans les deux éditions aux blancs joints et 34 aux blancs séparés. Les deux derniers mots concordent exactement entre éditions dans 23 et 24 voisinages respectivement. Parmi eux, 15 et 17 disposent d’un paragraphe local dans la table. La différence entre conventions vient des groupes découpés par des espaces incertains.

Les 130 lignes externes offrent respectivement 2 535 fenêtres dont les deux extrémités sont lisibles en H, 2 234 en ZL aux blancs joints et 2 494 en ZL aux blancs séparés. Chaque fenêtre contient deux à quatre positions sur la même ligne. Les neuf rangées pour lesquelles la table désigne un paragraphe local couvrent 52 lignes de prose distinctes. Dans cette partie locale, les trois effectifs sont de 1 030, 897 et 1 008 fenêtres. Les paires ont été comparées exclusivement avec leur panneau, puis avec leur propre paragraphe.

Les [résultats complets](resultats.json) donnent chaque paire de fragments avec ses positions, ses deux lectures intégrales, son admissibilité et ses lignes de paragraphe. Le [programme](examiner.py) vérifie les empreintes des transcriptions et de la table de rangées. Pour rejouer le calcul dans ce dossier, exécuter `python3 -B examiner.py`. [Table géométrique utilisée](../../../../2026-11-18-paires-ingredients/rangees/rangees.tsv)
