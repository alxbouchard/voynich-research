# Une clé de lecture dans la marge de f66r ?

**La colonne de signes de f66r ne fournit pas une table fixe des initiales des lignes de prose voisines.** Le signe transcrit `x` en donne un exemple vérifiable sur la photographie. Au rang 24, les deux lignes de prose voisines commencent par `s`. Au rang 32, elles commencent par `d` et `sh`. Les deux éditions s’accordent sur ces lectures. Une table qui attribue toujours la même initiale à cette marque rencontre deux exigences incompatibles. Les lettres EVA désignent ici le tracé des signes, sans hypothèse phonétique. [Deux détails photographiques](../../docs/PIECES_REFERENCES.md#piece-091302e59a7574) · [Page entière à Yale](https://collections.library.yale.edu/iiif/2/1006192/full/full/0/default.jpg)

## Une prédiction sur le Voynich

Le feuillet présente une colonne de 15 mots brefs, une colonne de 34 marques, puis 32 lignes de prose. D’Imperio a évoqué pour ce type de liste une fonction d’index ou de clé. Stolfi a examiné le rapport entre colonnes, y compris la possibilité que les signes se lisent par paires. Nous avons posé une question plus étroite. En voyant la marque, peut-on annoncer l’initiale de la ligne voisine, par copie ou avec une correspondance apprise sur le haut de la page ? [Étude de D’Imperio](https://www.nsa.gov/portals/75/documents/about/cryptologic-heritage/historical-figures-publications/publications/misc/voynich_manuscript.pdf) · [Note de Stolfi](https://www.ic.unicamp.br/~stolfi/EXPORT/voynich/Notes/034/Note-034.html)

Deux lecteurs IA ont mesuré séparément la position de l’encre sur la photographie native, en tenant compte de l’inclinaison des lignes. Les rangs 1 à 22 des marques formaient le lot d’apprentissage. Les rangs 23 à 34 étaient réservés. Le protocole a été consigné dans le commit local `881fb67`, et les prédictions dans `ffbe160` avant de dévoiler les initiales du bas. Les pages et les éditions étaient déjà publiques et partiellement connues du projet. [Protocole](PROTOCOLE.md) · [Séparation des lots](LOTS.md) · [Prédictions originales](PREDICTIONS.json) · [Mesures photographiques](../../docs/PIECES_REFERENCES.md#piece-9ba189f70848c2)

| Rang de la marque | Emplacement de la cible | Copie prédite | Initiale observée dans les deux éditions |
|---:|---|---|---|
| 32 | Prose f66r.78 | `x` | `d` |
| 24 | Mot de gauche f66r.11 | `x` | `d` |
| 29 | Mot de gauche f66r.13 | `r` | `q` |

Les trois prédictions échouent. Deux autres rangées de prose avaient un alignement commun mais une lecture de marque discordante ou incomplète. Pour la règle apprise, nous demandions au moins deux exemples de la même marque avec la même initiale et aucun contre-exemple dans les rangs d’apprentissage. Aucune entrée n’a rempli ce critère, sur les 11 couples recevables en prose et les 8 couples des mots de gauche de l’analyse principale. Le témoin qui prédit l’initiale majoritaire échoue également sur ces trois rangées. Une fois les lectures incertaines retirées, **la taille de la réserve était trop petite pour qu’une règle atteigne le seuil préfixé de trois succès par destination**. [Valeurs d’apprentissage](APPRENTISSAGE.json) · [Résultats de réserve](RESULTATS.json)

En conservant tous les alignements nominaux et les lectures communes aux deux éditions, le relevé A donne 0/10 en prose et le relevé B, 1/10. Ce succès dépend du dernier rang, pour lequel les deux géométries retiennent deux lignes différentes. Huit lignes de prose distinctes sont représentées dans chacun de ces dix couples. En permutant leurs initiales par ligne physique, la probabilité d’égaler ou dépasser le score du relevé B est de 0,518. Pour les mots de gauche, les deux relevés donnent 0/4. Aucun test ne valide la règle. Les cas artificiels montrent que le programme retrouve 12 initiales sur 12 lorsqu’une table cohérente a été implantée et qu’il apprend assez d’exemples de chaque signe. [Contrôles artificiels](CALIBRATION.json) · [Recomptage indépendant](../../docs/PIECES_REFERENCES.md#piece-02aa673deb2b2b)

## Jusqu’où une erreur d’alignement change-t-elle le verdict ?

Après avoir constaté le peu de rangées univoques et avant de dévoiler la réserve, nous avons consigné un contrôle supplémentaire dans `995d4ed`. Pour chaque marque, nous avons admis les voisins plausibles du premier relevé, les variantes du second et ses deux plus proches lignes, même quand elles sont dans un interligne. Chaque rang a pu choisir la ligne qui arrangeait le mieux l’hypothèse. Une ligne ou une marque illisible ne peut établir une contradiction. [Règle du contrôle](COMPLEMENT.md)

Sur les douze dernières marques, la copie de l’initiale de prose est compatible **à un rang**, incompatible **à neuf**, et indéterminée **à deux**. En élargissant la question à **toutes les marques** du feuillet et en autorisant une table inconnue, cinq d’entre elles aboutissent à des ensembles d’initiales sans élément commun.

| Marque répétée | Premier rang et initiales possibles | Autre rang et initiales possibles |
|---|---|---|
| `d` | 6 · `d` ou `y` | 12 · `q` ou `sh` |
| `o` | 7 · `d` ou `t` | 18 · `p` ou `sh` |
| `t` | 25 · `s` ou `y` | 30 · `d` ou `q` |
| `x` | 24 · `s` | 32 · `d` ou `sh` |
| `y` | 5 · `q` ou `y` | 14 · `d` ou `p` |

Les cinq conflits persistent si l’on recommence dans Zandbergen–Landini seul ou dans Takahashi seul. Cette conclusion suppose que les occurrences lisibles d’une même marque codent toutes l’initiale d’une ligne voisine. Une fonction de repère, une lecture séquentielle ou une valeur dépendante du contexte restent ouvertes. Aucun mot du manuscrit ne reçoit une lecture linguistique de cet essai. [Voisinages et contre-exemples complets](VOISINS.json) · [Deux éditions des signes et initiales](INITIALES_ET_MARQUES.json)

## Contrôle historique sur un chiffre du XVe siècle

Une expérience distincte a testé ce qu’une clé partielle permet réellement de lire. Dans le manuscrit chiffré de **Giovanni Fontana** (Munich, Cod.icon. 242, f34v), un opérateur a rapproché des signes de deux lignes déjà déchiffrées puis a annoncé **`ping?tur colore`** pour les deux premiers mots de la dernière ligne. La transcription de contrôle de Schulte, conservée dans un cahier séparé daté de 1910, donne **`pingitur colore`**. Sur les 14 positions réservées, il y a 13 lettres prédites et confirmées, une abstention, zéro erreur et un mot complet exact sur deux. La plausibilité du latin a aidé au choix du `c` de *colore*. Les mots réservés viennent du même paragraphe et étaient absents des deux lignes utilisées pour établir la mini-clé. Le chiffrement, la langue et le clair de contrôle appartiennent au manuscrit de Fontana. [Prédiction Fontana avant dévoilement](fontana/PREDICTION.json) · [Planche chiffre et clair](../../docs/PIECES_REFERENCES.md#piece-5647e7d6c478a9) · [Rapport et sources de Munich](fontana/RAPPORT.md)

## Reproduire les résultats

Dans ce dossier, `python3 -B aligner.py` reconstitue les couples depuis les deux relevés. `python3 -B tester.py calibrer` vérifie les contrôles et `python3 -B tester.py rejouer` refait le score à partir des données archivées et des prédictions fixées. `python3 -B verifier_voisins.py` refait le test des contre-exemples. Les quatre commandes utilisent uniquement la bibliothèque standard. [Script de prédiction et de score](tester.py) · [Script des voisinages](verifier_voisins.py)
