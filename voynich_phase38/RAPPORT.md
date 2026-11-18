# Phase 38 — ce que permet une clé publiée

17 novembre 2026. **NOT_TRANSLATION : aucun mot du manuscrit n'est déclaré traduit par cette expérience. L'objectif de déchiffrement reste ouvert.**

La table partielle tirée de Caspari et Faccini produit plus de correspondances italiennes que les 198 variantes de clé testées, dans les trois modes et les deux transcriptions. Cependant, les six textes générés sans message source choisi produisent des taux comparables. Ce résultat justifie de conserver la table comme hypothèse examinable ; il ne permet ni d'identifier la langue ni de lire des phrases.

## Question et périmètre

Après l'échec de fiabilité de phase 37, cette phase examine une autre famille : une proposition de valeurs de signes déjà publiée. Elle mesure les contraintes que cette table impose réellement, avant toute reconstruction libre du sens. Il ne s'agit pas d'appliquer au manuscrit le normalisateur refusé en phase 37.

La source est [A Key to the Voynich Manuscript, Caspari et Faccini (2025)](https://doi.org/10.31235/osf.io/8b4we_v1), [PDF archivé](../docs/PIECES_REFERENCES.md#piece-9187d133c5fcee), table 1, pages 5–8. Les auteurs proposent des valeurs multiples, des groupes de signes et des développements d'abréviations. Notre code formalise une partie de cette table en EVA ; cette correspondance EVA est notre interprétation des images. Les auteurs ne fournissent pas ce codebook EVA. Les annexes annoncées n'ont pas été récupérées aux liens publics consultés ; cela ne démontre pas leur inexistence. Cet audit ne constitue pas une réplication intégrale de leurs lectures.

Le [protocole](PROTOCOL.json), la [clé](KEY.json), les sources, le logiciel expérimental et les contrôles mécaniques ont été figés avant les mesures sur le corpus entier : 40 fichiers, commit `2291d0d2ff7e08db26cb2e18e07fe3b9c1886ccb`, le 17 novembre 2026 à 16:09:57 UTC. Le papier et quelques loci de légendes avaient déjà été examinés. Aucune page n'est présentée comme historiquement inconnue de l'analyste.

## Méthode effectivement exécutée

Toutes les segmentations compatibles avec la table sont conservées : par exemple `ar` peut être une unité ou `a+r`, et `ee` une unité ou `e+e`. Les valeurs multiples restent multiples. Un signe non reconnu donne une abstention ; aucun signe n'est deviné. Le plafond préétabli de 4 096 chaînes par mot n'est jamais atteint ; le maximum observé est 32. Les variantes d'espaces entre mots ne sont pas explorées ici.

Deux lexiques contiennent chacun **7 030 formes**, avec exactement le même nombre de formes à chaque longueur de 2 à 14 lettres. Ils proviennent de références normalisées de Dante et César déjà archivées. Ce sont des vocabulaires littéraires incomplets, pas des dictionnaires exhaustifs. L'égalité des tailles ne contrôle ni le genre ni la morphologie. Dante ayant aussi informé les auteurs, cette comparaison n'est pas une validation indépendante de la langue proposée.

Trois modes sont calculés séparément :

- **Exact** : chaîne présente dans le lexique.
- **Voyelles** : insertion de voyelles seulement, sans effacer ni remplacer les lettres observées.
- **Deux lettres** : insertion d'au plus deux lettres quelconques, sans effacement ni remplacement.

Dans **chacun** de ces modes, un seul préfixe exact parmi `o`, `qo`, `d`, `ex`, `ol` peut aussi être retiré. Cette hypothèse est identique pour les deux langues et toutes les clés. « Exact » ne signifie donc pas toujours « chaîne entière inchangée ». Aucun retrait récursif, réordonnancement ou choix de traduction selon l'illustration n'est autorisé. Les contractions plus longues de l'hypothèse originale ne sont pas couvertes.

La clé proposée est comparée à 99 permutations de son alphabet de sortie et à 99 permutations conservant séparément les classes voyelles/consonnes. Les entrées, longueurs, chevauchements et ambiguïtés des règles sont préservés. Ces classements sont descriptifs : la clé a été développée sur le manuscrit, et ces 198 permutations n'épuisent pas les clés possibles.

Les données sont les **29 016 occurrences ZL** et **33 941 occurrences IT** retenues par l'extraction littérale de phase 23, prose et étiquettes réunies. Ce filtrage exclut certains éléments du manuscrit ; ZL et IT décrivent le même objet historique. Les témoins sont six sorties archivées du générateur Timm, graines 81–86, de 3 000 mots chacune après exclusion des 500 premiers. Le générateur n'a pas été relancé et hérite de la structure du Voynich. Il n'a pas reçu de passage littéraire à chiffrer.

## Résultats

Pourcentage de toutes les occurrences retenues ayant **au moins un candidat dans le lexique**, y compris les occurrences non analysables dans le dénominateur :

| Corpus | Italien exact | Italien voyelles | Italien deux lettres | Latin exact | Latin voyelles | Latin deux lettres |
|---|---:|---:|---:|---:|---:|---:|
| ZL | 14,08 % | 37,85 % | 55,87 % | 4,80 % | 29,46 % | 44,70 % |
| IT | 14,46 % | 39,54 % | 57,18 % | 5,06 % | 30,73 % | 46,21 % |
| Timm 81 | 14,97 % | 40,40 % | 51,13 % | 4,37 % | 29,37 % | 44,67 % |
| Timm 82 | 12,53 % | 41,43 % | 54,93 % | 4,40 % | 27,80 % | 47,00 % |
| Timm 83 | 15,73 % | 47,73 % | 59,83 % | 5,30 % | 33,80 % | 53,57 % |
| Timm 84 | 10,73 % | 38,23 % | 48,80 % | 3,70 % | 28,90 % | 45,33 % |
| Timm 85 | 15,30 % | 43,03 % | 56,20 % | 4,97 % | 33,30 % | 47,43 % |
| Timm 86 | 15,43 % | 41,57 % | 49,83 % | 4,90 % | 30,13 % | 42,57 % |

Les valeurs exactes, effectifs et clés sont dans [RESULTATS.csv](RESULTATS.csv) : **9 552 lignes** pour 199 clés, huit corpus, deux langues et trois modes.

L'avantage italien sur le latin existe sous ces règles et ces références. Sur ZL et IT, aucune des 198 clés concurrentes n'égale la clé proposée en italien, quel que soit le mode. Ce constat ne s'étend pas à tous les scores latins. Surtout, les témoins Timm obtiennent également de nombreuses correspondances italiennes : le score ne distingue pas ici un message source d'un texte généré. Cela ne prouve pas que le Voynich est dépourvu de sens.

La table produit au moins une chaîne pour 97,50 % des occurrences ZL et 96,48 % des occurrences IT. Cette couverture graphique est distincte de la lecture d'une langue. Déjà avant toute insertion, 57,21 % des occurrences ZL et 55,17 % des occurrences IT ont plusieurs chaînes possibles.

En italien avec deux lettres ajoutées, les **16 210 occurrences ZL compatibles** se répartissent entre **3 894 à un seul candidat lexical** et **12 316 à plusieurs candidats**. Les candidats uniques représentent seulement 13,42 % de toutes les occurrences ZL. Un candidat unique dans un lexique incomplet n'est pas une signification établie.

## Exemples pour comprendre la limite

Ces sorties sont des possibilités formelles et **ne sont pas des traductions proposées** :

| Entrée EVA | Chaînes de la table | Conséquence dans ce test |
|---|---|---|
| `daiin` | `tmo` | Avec deux insertions : seul candidat italien `tumor`, seul candidat latin `timor`. L'unicité dépend du lexique choisi. |
| `cholar` | `folar`, `foln`, `polar`, `poln` | Les quatre lectures restent possibles. L'absence d'un nom propre dans notre vocabulaire littéraire ne réfute pas ce nom. |
| `otor` | `ocor` | Après retrait autorisé de `o`, un candidat italien exact, quatre avec voyelles et quatorze avec deux insertions. |
| `ypchy` | `essfe`, `esspe`, `exfe`, `expe` | Trente-sept candidats italiens avec deux insertions et les préfixes autorisés. Aucun sens astronomique n'est sélectionné. |

Le panneau [f1r non validé](results/F1R_UNVALIDATED.json) conserve 171 occurrences, leurs lieux et leurs alternatives. Il ne contient pas de prose française inventée. [PROPOSED_WORDS.json](../docs/PIECES_REFERENCES.md#piece-99440392ac5ee6) enregistre les nombres complets de candidats ; les exemples affichés y sont limités à vingt par case, avec un indicateur explicite, sans tronquer les calculs.

## Vérification et portée

Un second programme n'importe ni le modèle ni le moteur expérimental. Il utilise une propagation vers l'avant pour analyser les signes et reconstruit les compatibilités lexicales en supprimant des positions des mots clairs. Il a vérifié **9 998 formes d'entrée, 199 clés, 9 552 lignes de scores, 96 classements et les 171 occurrences de f1r**, ainsi que les empreintes des 40 fichiers figés. Résultat : [verification.json](results/verification.json).

Les 200 allers-retours à clé connue vérifient seulement le logiciel. Ils ne prouvent ni la récupération d'une clé inconnue ni le sens d'un texte. Le vérificateur et la réexécution ont été réalisés par le même opérateur : ce n'est pas une expertise paléographique ou linguistique indépendante. La procédure de reproduction et le contrôle à l'octet sont décrits dans [REPRODUCTION.md](REPRODUCTION.md) et [replay.json](results/replay.json).

Cette expérience ne fournit donc aucune phrase déchiffrée, aucune langue identifiée et aucune clé validée historiquement. Une suite utile devra contraindre les valeurs et les abréviations par des éléments indépendants, puis prédire des passages sans les retoucher. Augmenter uniquement le nombre de mots reconnaissables ne lèverait pas l'ambiguïté observée ici.

Les sources tierces conservent leurs droits : [NOTICE.md](NOTICE.md). Livraison locale uniquement ; objectif utilisateur non atteint.
