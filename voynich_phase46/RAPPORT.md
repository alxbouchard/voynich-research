# Phase 46 — Transfert aux autres rapprochements de plantes

**L'avantage approximatif de la phase 45 n'est pas retrouvé dans ce nouvel ensemble.** Les neuf étiquettes sont absentes à l'identique des passages ciblés. Les rangs moyens de proximité approximative restent sous 0,5 dans les quatre configurations prévues, même après exclusion de l'étiquette dont la lecture diffère entre transcriptions. Aucun mot n'est traduit.

## Sélection avant calcul

Le [catalogue du cahier 19](https://www.voynich.nu/q19/index.html) propose des ressemblances plus faibles pour treize fragments, représentant quatorze liens vers de grandes plantes. Neuf fragments possèdent une étiquette isolée attribuable. Les fragments 150, 155, 168 et 209 sont exclus faute d'une telle étiquette. Le second locus associé à 110, `chor.olekor`, contient deux unités : il reste dans l'inventaire, sans choisir arbitrairement l'une de ses moitiés.

| Fragment | Locus | Étiquette ZL / IT | Page cible |
|---|---|---|---|
| 80 | f99r.20 | `oaro` | f51r |
| 94 | f99r.46 | `tolsasy` | f96v |
| 95 | f99v.2 | `otoldy` | f44r |
| 110 | f99v.27 | `otal` | f34v |
| 116 | f100r.2 | `sochorcfhy` | f96v |
| 133 | f100v.3 | `opchor` | f13v |
| 136 | f100v.6 | `ykchochdy` | f90v2 |
| 188 | f101v.7 | `otarar` / `otorar` | f37r |
| 225 | f102v2.14 | `sarol` | f36r |

Pour 188, le [relevé interlinéaire historique](https://www.voynich.nu/q19/f101v2_tr.txt) situe l'inscription entre les plantes 1,7 et 1,8, tout en signalant une incertitude introductive sur l'étiquetage. Cette attribution reste conditionnelle. Nous conservons les deux lectures et prévoyons aussi un résumé excluant 188 avant de regarder les scores.

Un agent a contrôlé la position des huit autres inscriptions sur cinq vues d'ensemble et huit détails natifs, sans consulter la prose cible. Aucun remplacement manifeste par une inscription sur récipient n'a été observé. Les zones 80, 95 et l'inscription supplémentaire de 110 restent ambiguës pour un rattachement exclusif. Le [compte rendu original](evidence/SPATIAL_REVIEW.md) est conservé ; il ne constitue pas une nouvelle lecture EVA. Le contrôle de 188 repose sur la référence documentaire et une inspection spatiale séparée, également non aveugle.

Le protocole, les paires, les groupes, les transcriptions, les six images sources, les aperçus, le compte rendu et le code d'analyse ont été figés avant le calcul dans FREEZE.json. Les copies des huit détails examinés ont été ajoutées ensuite pour archivage, avec leurs coordonnées ; cette différence de chronologie est conservée. Les sources avaient déjà été exposées dans le projet et l'origine historique des rapprochements visuels n'est pas contrôlée.

## Mesures et comparateurs

Nous reprenons les deux mesures de phase 45 : présence exacte après égalisation du nombre d'occurrences, et minimum attendu de distance de Levenshtein normalisée entre l'étiquette entière et les tokens de la page. Aucune réécriture n'est apprise. Les unités restent les caractères conventionnels EVA.

Chaque cible est comparée aux pages partageant son cahier et ses catégories de section, Currier et main dans les métadonnées. Les groupes comptent de quatre à quatorze pages. K est la taille de la plus courte page de chaque groupe après filtrage, calculée séparément pour chaque configuration. Les virgules incertaines sont globalement coupées ou jointes ; les tokens illisibles ou ambigus sont rejetés en entier, sans correction.

Les rangs incluent la page cible et partagent les égalités. **Un rang élevé est favorable ; 0,5 est neutre.** Pour la proximité approximative :

`R = (pages à distance attendue supérieure + ½ pages à égalité) / nombre de pages`.

Les deux étiquettes visant f96v sont d'abord moyennées, puis les huit cibles ont le même poids. Le sous-ensemble de huit étiquettes concordantes porte sur sept cibles. La direction est déclarée maintenue seulement si la moyenne dépasse 0,5 dans les quatre configurations principales. Ce critère descriptif a été fixé pour le transfert ; il ne correspond ni à une significativité statistique ni à un seuil de déchiffrement.

Le rang conjoint parmi douze associations de phase 45 et ces rangs moyens par page **ne sont pas numériquement comparables**. Le nouvel ensemble traverse plusieurs cahiers et emploie une référence différente. Les autres pages ne sont pas des négatifs botaniques certifiés ; les groupes et les pages apparentées restent dépendants.

## Résultats du transfert

| Configuration | Rang approximatif moyen, neuf étiquettes | Cibles au-dessus / égales / sous 0,5 | Moyenne sans 188 |
|---|---:|---:|---:|
| ZL, couper | 0,336310 | 1 / 1 / 6 | 0,321854 |
| ZL, joindre | 0,358259 | 1 / 1 / 6 | 0,346939 |
| IT, couper | 0,433780 | 2 / 1 / 5 | 0,415391 |
| IT, joindre | 0,433780 | 2 / 1 / 5 | 0,415391 |

Les deux configurations IT donnent les mêmes résultats ici ; elles ne constituent pas deux réplications indépendantes. Les moyennes restent sous 0,5 partout. Le critère directionnel échoue, y compris dans le sous-ensemble sans 188.

Aucune étiquette entière ne réapparaît dans sa page cible selon les tokens retenus. Des occurrences exactes existent ailleurs dans les groupes : en ZL/couper, `otoldy` sur f44v, `otal` sur f33r/f33v/f39r/f39v et `opchor` sur f13r. Il n'est donc pas possible de transformer la seule reconnaissance d'un token en preuve de la correspondance visuelle ciblée.

Les résultats individuels montrent pourquoi il faut conserver tous les cas. Pour f96v en ZL/couper, `tolsasy` obtient un rang approximatif de 7/8 et `sochorcfhy` de 1/8 : la moyenne pour cette cible vaut 0,5. Choisir uniquement le premier aurait donné une image trompeuse du résultat. Toutes les occurrences et tous les voisins à égalité figurent dans [TARGETS.json](results/TARGETS.json) et [SCORES.json](results/SCORES.json).

## Conséquence pour la recherche

Nous ne disposons pas d'un lien général confirmé entre ces étiquettes et les notices herbales proposées. L'observation positive, très limitée, de phase 45 ne suffit pas pour apprendre des suppressions ou attribuer des sens aux mots. Les voisinages calculés restent des ressemblances de chaînes.

Ce transfert utilise des rapprochements iconographiques plus faibles : son échec ne réfute pas les trois correspondances plus fortes de phase 45, ni toute relation entre texte et dessin. Il retire toutefois le soutien à une généralisation immédiate de cette méthode de rapprochement. Aucun nom de plante, son, langue ou traduction n'est adopté.

Les [288 comparaisons](results/SCORES.json), [36 lignes cibles](results/TARGETS.json), [tokens](../docs/PIECES_REFERENCES.md#piece-de5d6cb7349e47) et [résumé](results/SUMMARY.json) sont archivés. Le calcul indépendant et le rejeu vérifient les mesures et la traçabilité, sans valider l'identité botanique. Voir la [reproduction](REPRODUCTION.md).
