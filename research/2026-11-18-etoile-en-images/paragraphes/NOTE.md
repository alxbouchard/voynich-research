# Otor et les lignes d'ouverture dans le cahier final

**Les quatre occurrences de `otor` sur des lignes qui ouvrent un paragraphe sont compatibles avec la répartition des places disponibles.** Le calcul tient compte du nombre d'occurrences propre à chaque face. Sur les mots de même silhouette, la probabilité d'en obtenir au moins quatre atteint 4/15 chez Takahashi et 17/30 chez Zandbergen–Landini. Ces deux transcriptions portent sur le même manuscrit. [Règle fixée avant le calcul des probabilités](PROTOCOLE.md) · [Relevé pour chaque face et chaque convention](PAR_FACE.tsv)

Les quatre ouvertures sont f104r.19, f106v.34, f107r.1 et f113v.10. Parmi les huit lignes communes aux deux éditions, les quatre autres sont intérieures. Takahashi lit une neuvième occurrence à f105v.31, également intérieure. Les mots peuvent se trouver loin du début de la ligne. Sur les 24 faces du cahier, 23 ont des lignes P0. Les deux éditions marquent 285 lignes d'ouverture ; elles donnent respectivement 1 079 et 1 080 lignes P0 au total. [Loci et rangs de tous les mots](RESULTATS.json)

| Édition et espaces | Positions d'ouverture / toutes positions lisibles | Otor sur ligne d'ouverture | Moyenne attendue par face, additionnée | Probabilité d'au moins 4 |
|---|---:|---:|---:|---:|
| H, joints ou séparés | 3 020 / 10 654 (28,35 %) | 4 / 9 | 2,765 | 0,2857 |
| ZL, joints | 2 767 / 9 866 (28,05 %) | 4 / 8 | 2,429 | 0,1986 |
| ZL, séparés | 2 990 / 10 662 (28,04 %) | 4 / 8 | 2,437 | 0,2004 |

| Édition et espaces | Positions d'ouverture / positions de silhouette o·X·o·Y | Otor sur ligne d'ouverture | Moyenne attendue par face, additionnée | Probabilité d'au moins 4 |
|---|---:|---:|---:|---:|
| H, joints ou séparés | 18 / 58 (31,03 %) | 4 / 9 | 2,933 | 0,2667 |
| ZL, joints | 14 / 41 (34,15 %) | 4 / 8 | 3,600 | 0,5667 |
| ZL, séparés | 14 / 46 (30,43 %) | 4 / 8 | 3,600 | 0,5667 |

Une part du résultat vient de la disposition des occasions sur quelques faces. Chez ZL, l'unique position de même silhouette sur f104r appartient à une ligne d'ouverture. Sur f107r, les deux seules positions de cette silhouette appartiennent également à des lignes d'ouverture dans les deux éditions. Dès que l'on fixe les présences de `otor` sur ces faces, un début y est inévitable. Parmi les formes du même patron de fréquence comprise entre la moitié et le double de celle d'`otor`, celui-ci se classe premier sur trois chez H. Chez ZL, `otol` a une probabilité unilatérale plus faible ; deux formes, en incluant `otor`, atteignent son rang sur trois avec les espaces joints et sur quatre avec les espaces séparés. [Valeurs pour chaque forme](RESULTATS.json)

Le modèle distribue les mots sans remise à l'intérieur de chaque face, en conservant son nombre total d'occurrences. Le rang de chaque mot dans la ligne et la syntaxe réelle ne sont pas modélisés. Le mot avait été sélectionné sur un autre cahier. Le choix d'examiner les ouvertures vient de l'observation des huit lignes communes du cahier final. Cette analyse rétrospective porte sur le marqueur de paragraphe textuel ; la présence d'une étoile en marge a été vérifiée séparément sur les photographies.

Le programme se relance depuis ce dossier avec `python3 -B compter.py`. Les huit probabilités ont aussi été vérifiées par énumération directe des combinaisons de nombres d'occurrences par face et sommation de leurs multiplicités entières. [Code](compter.py) · [Distributions et fractions exactes](RESULTATS.json)
