# Phase 45 — Plantes répétées et récurrence des étiquettes

**Aucun mot traduit. Les trois étiquettes testées sont absentes à l'identique des passages associés.** Une observation secondaire mérite néanmoins d'être conservée : après correction de la longueur des pages, les ressemblances approximatives placent l'association iconographique publiée au premier rang des douze associations distinctes comparées. Elles exigent trois ou quatre changements de caractères, sans règle de transformation démontrée.

## Trois associations fixées avant le calcul

Le [catalogue du cahier 19](https://www.voynich.nu/q19/index.html) rapproche sept fragments de grandes plantes avec une formulation plus forte que la simple ressemblance. Seuls trois disposent d'une étiquette de fragment propre dans les transcriptions utilisées. Les quatre autres, 203, 204, 205 et 206, sont exclus : une étiquette de récipient ne leur est pas réattribuée. Les rapprochements plus faibles restent hors du test. La [description du cahier 3](https://www.voynich.nu/q03/index.html) documente aussi les trois associations retenues.

| Fragment | Locus de son étiquette | Lecture ZL et IT | Page herbale associée |
|---|---|---|---|
| 212, f102r2 | f102r2.21 | `koldarod` | f18v |
| 213, f102r2 | f102r2.22 | `odalydary` | f23r |
| 240, f102v1 | f102v1.17 | `loralody` | f19r |

Les cinq photographies Yale ont été récupérées à leur résolution native et leurs empreintes correspondent à l'inventaire antérieur. L'examen des vues d'ensemble et de trois cadrages confirme la position des inscriptions près des fragments retenus. Les racines et certains motifs de feuilles présentent des ressemblances visibles ; cette inspection n'est ni une identification botanique ni une classification aveugle. Voir les [planches](PLANCHES.md) et les [sources](NOTICE.md).

Les entrées et le protocole ont été figés au commit `8958e7e6c274e0b95eef82799928094f17ef8a31`, avant le calcul de récurrence. Le programme a été écrit ensuite ; il n'était pas inclus dans ce gel. Les transcriptions et images avaient déjà été exposées dans le projet : ce n'est pas un échantillon historiquement inconnu. Nous n'avons pas établi que les rapprochements iconographiques publiés furent eux-mêmes proposés sans consulter le texte. L'expérience reste exploratoire.

## Comparaison fixée

Les seize pages du cahier 3 possèdent les mêmes valeurs des métadonnées retenues : section herbale, groupe Currier A et main 1. Nous conservons tous leurs loci de prose, les occurrences répétées et leurs positions. Les tokens comportant une lecture incertaine sont exclus en entier ; aucun signe n'est réparé. Les virgules de séparation incertaine sont traitées globalement de deux façons : couper ou joindre. ZL/couper est la configuration principale ; les trois autres sont des sensibilités.

Le test principal recherche l'étiquette entière. Pour que les pages longues ne bénéficient pas simplement de davantage d'occasions, chaque comparaison est ramenée analytiquement à K occurrences, où K est la taille de la plus courte page admissible. Si une page contient N occurrences dont c égales à l'étiquette, la probabilité d'en observer au moins une dans un sous-ensemble uniforme de taille K vaut :

`1 − C(N−c,K) / C(N,K)`.

Le score secondaire utilise la distance de Levenshtein divisée par la longueur maximale des deux chaînes. Il estime le minimum attendu dans le même sous-ensemble de K occurrences, sans tirage aléatoire. Les unités sont les caractères ASCII EVA : elles ne sont pas présumées être les véritables lettres, glyphes ou sons.

Nous comparons l'affectation réelle aux 24 permutations de quatre bifolios, en conservant leur organisation interne et le côté recto/verso. Ainsi, les deux étiquettes voisines 212/213 restent associées à une même face de bifolio. Les deux blocs non utilisés peuvent être échangés sans changer l'affectation : les 24 permutations représentent **12 associations distinctes**, chacune deux fois. La fraction de permutations aussi favorables est un rang descriptif sous cette référence, pas une probabilité calibrée d'avoir raison.

## Résultats

Aucune des trois étiquettes ne figure à l'identique dans les tokens retenus d'aucune des seize pages, dans les quatre configurations. Le score principal vaut donc zéro partout ; les 24 permutations sont à égalité.

Les plus proches tokens des pages associées sont les mêmes dans les quatre configurations :

| Étiquette recherchée | Token le plus proche | Locus | Changements de caractères | Distance normalisée |
|---|---|---|---|---|
| `koldarod` | `daror` | f18v.8 | 4 | 4/8 |
| `odalydary` | `dalory` | f23r.11 | 4 | 4/9 |
| `loralody` | `qolody` | f19r.11 | 3 | 3/8 |

Ce sont des voisins graphiques calculés, **pas des mots déclarés équivalents**. Aucune suppression, correspondance phonétique, flexion ou signification n'est déduite de ces trois rapprochements.

| Configuration | K | Distance minimale attendue moyenne, association réelle | Permutations aussi proches ou plus proches |
|---|---:|---:|---:|
| ZL, couper | 58 | 0,480376 | 2/24 |
| ZL, joindre | 55 | 0,480036 | 2/24 |
| IT, couper | 56 | 0,488837 | 2/24 |
| IT, joindre | 56 | 0,488837 | 2/24 |

Les deux lignes IT sont identiques : les deux conventions ne créent aucune différence dans ce sous-corpus. Les quatre lignes ne sont donc pas quatre confirmations indépendantes. Dans chaque configuration, la même association réelle est la meilleure des douze associations distinctes. Il reste seulement trois étiquettes, deux panneaux d'un même folio source et deux bifolios cibles ; l'effectif et les dépendances empêchent une conclusion générale.

## Ce que cela change pour le déchiffrement

Cette sélection ne fournit aucun lien lexical exact entre une étiquette et la notice de la plante supposée correspondante. Elle ne suffit donc pas pour attribuer un sens certain ou apprendre une clé. L'avantage approximatif est conservé comme observation à tester sur d'autres associations établies avant leur score, sans ajuster après coup une règle pour expliquer ces trois voisins.

Ce résultat ne réfute ni les rapprochements iconographiques, ni une langue, ni une variation de forme entre étiquette et prose. Une étiquette pourrait désigner une partie ou une propriété plutôt qu'un nom de plante. Aucune de ces possibilités n'est choisie ici.

La phase 14 comparait les étiquettes à la prose de leur propre page pharmaceutique ; la phase 15 apprenait des réécritures. Cette phase examine un lien publié vers une page herbale distante, sans réécriture apprise. Les étiquettes restent intactes pendant toutes les comparaisons.

## Contrôle et reproduction

Les [192 scores](results/SCORES.json), [96 permutations](results/ASSIGNMENTS.json), [tokens retenus et exclus](results/PARSED.json) et le [résumé](results/SUMMARY.json) sont archivés. Le contrôle séparé reconstruit le parsage et les distances, vérifie la raréfaction avec une autre formule et contrôle les pixels des cadrages. La reproduction en dossier neuf porte sur ces calculs, pas sur l'identité botanique ni sur le sens du manuscrit. Voir la [notice de reproduction](REPRODUCTION.md).
