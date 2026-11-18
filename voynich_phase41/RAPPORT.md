# Phase 41 — un cercle répété fournit-il une clé ?

**Aucune clé ni traduction validées.** Le cercle de f57v fournit une répétition graphique et des variantes locales inspectables. Il ne permet pas d'attribuer des valeurs phonétiques aux signes, ni de traiter sans autre justification ses emplacements comme les lettres distinctes d'un alphabet.

Le résultat utile pour la suite est une hypothèse locale : les formes EVA `f` et `p` occupent la même place dans les répétitions. Cette observation, déjà publiée par Stolfi, est retrouvée dans les cinq lectures EVA examinées. Elle peut devenir une branche d'un test de déchiffrement ; elle ne justifie pas une fusion automatique dans tout le manuscrit.

## Sources et unités

L'[image Yale de f57v](https://collections.library.yale.edu/catalog/2002046?child_oid=1006187) est conservée dans sa résolution native, 3 028 × 3 769 pixels. Son empreinte correspond à celle de l'archive visuelle antérieure. Les [bandes d'inspection](PLANCHES.md) rendent les formes comparables sans les retoucher.

Les six lectures sont ZL, IT, un [extrait GC en v101](https://voynich.nu/data/GC2a-n.txt) et les trois versions H/V/U de l'[archive originale de Stolfi](https://www.ic.unicamp.br/en/~stolfi/EXPORT/voynich/98-12-28-interln16e6/). **Ce sont des lectures du même cercle, pas six manuscrits ni six expertises indépendantes.** IT et H partagent notamment une histoire de transcription. L'image a été examinée par le même opérateur IA, qui connaissait ces lectures.

Le fichier GC complet a renvoyé HTTP406 lors du téléchargement direct ; seul le locus consultable par le navigateur documentaire est archivé, avec cette limite explicite. ZL et IT sont des copies exactes des fichiers de phase40. L'archive historique originale a bien été téléchargée.

Les unités primaires sont celles séparées par les délimiteurs publiés. Les symboles rares, les groupes de caractères, les alternatives et les inconnues sont conservés. `?` n'est jamais traité comme une lettre identique aux autres `?`. Aucun alphabet EVA n'est converti en v101 sur la seule ressemblance de ses codes latins.

| Lecture | Nombre d'entrées des quatre répétitions | Total |
|---|---|---|
| ZL | 17, 17, 17, 17 | 68 |
| IT | 17, 17, 17, 18 | 69 |
| GC | 17, 17, 17, 16 | 67 |
| H, archive historique | 17, 17, 17, 18 | 69 |
| V, archive historique | 17, 17, 17, 17 | 68 |
| U, archive historique | 17, 17, 17, 17 | 68 |

Le découpage des transcriptions explique des différences de compte. Dans ZL, `@169;v` est une entrée composée : la scinder donne 18 entrées par répétition. Dans GC, le début `oe` du dernier cycle est joint : le scinder donne quatre cycles de 17. Dans IT, regrouper les deux entrées finales `r,n` donne également quatre cycles de 17. Ces trois possibilités sont calculées séparément, **sans les adopter comme lectures historiques correctes**. Compter 17 ou 18 unités ne détermine donc pas, à lui seul, la taille d'un alphabet linguistique.

## Ce qui empêche d'utiliser directement la suite comme alphabet

Dans ZL, la même unité `r` figure aux positions 4 et 12 de chaque répétition. Cette duplication contredit le modèle précis d'une liste qui contiendrait chaque signe transcrit une seule fois. Dans l'ensemble, 23 des 24 lectures de cycles possèdent au moins une duplication certaine ; le premier cycle GC est l'exception. Ce compte décrit des observations dépendantes, pas un vote statistique.

Cela ne réfute pas toute fonction alphabétique possible : une transcription peut réunir des formes que le scribe distinguait, ou le diagramme peut obéir à une autre organisation. Il interdit simplement de remplacer automatiquement les 17 positions par 17 lettres différentes.

Une seconde analyse suppose, à titre conditionnel, que les positions correspondantes représentent le même élément. Elle conserve alors les rapprochements suivants :

| Lecture | Variantes réunies à une même position | Conséquence problématique entre positions |
|---|---|---|
| ZL | `f/p` ; `I/c` | Les positions 4 et 12 partagent `r` |
| IT | `f/p` ; `k/m` | Les positions 4/12 et 7/8 seraient réunies |
| V | `f/p` ; forme notée `*{&I}` / `c` | Les positions 4 et 12 partagent `r` |
| U | `d/j` ; `f/p` ; `*{&I}` / `c` | Les positions 4 et 12 partagent `r` |

Les cycles de longueur différente de 17 sont exclus de cette seule analyse de positions ; ils restent intégralement présents dans la collation et les alignements. H donne le même rapprochement `k/m` qu'IT. GC, dans son propre alphabet, conserve d'autres distinctions et variantes ; elles sont détaillées dans [ANALYSIS.json](results/ANALYSIS.json).

Sous cette hypothèse, on obtient 16 classes de positions pour ZL, V, U et GC, mais 15 pour IT et H. **Ces classes ne sont pas des lettres déchiffrées.** Deux classes séparées dans ce graphe ne prouvent pas non plus l’existence de deux sons différents. Le désaccord sur les positions 7/8 montre pourquoi apprendre toutes les équivalences depuis une seule transcription risquerait de propager ses erreurs ou ses conventions dans une clé globale.

La [Note034 de Stolfi](https://www.ic.unicamp.br/~stolfi/EXPORT/voynich/Notes/034/Note-034.html) avait déjà attiré l'attention sur ces séquences. Notre ajout est leur collation reproductible entre les six lectures et l'explicitation des limites de l'inférence. Aucune découverte de la répétition elle-même n'est revendiquée.

## Vérification et décision

Le [protocole descriptif](PROTOCOL.json) et 18 fichiers ont été figés au commit `f6eb034170f661e19c69df6c297c5dd2a46d483d`. Les sources avaient déjà été consultées : ce gel n'est pas une expérience aveugle. Les 409 entrées sont reconstruites depuis les sources. Un autre calcul vérifie les 36 distances d'édition et leurs nombres d'alignements optimaux, les doublons et les six graphes de relations. Les correspondances avec une inconnue sont admises pour l'alignement mais ne prouvent jamais l'identité des signes.

Le contrôle des images compare 1 464 000 pixels de la bande géométrique à leur position dans l'original. Cinq sorties sont reproduites à l'octet en dossier neuf. Cela valide les calculs et la traçabilité des images, sans constituer une expertise paléographique ou une confirmation linguistique. [Reproduction](REPRODUCTION.md).

Le cercle ne sera donc pas transformé en clé alphabétique. La variante `f/p` reste une hypothèse locale à tester ailleurs. La [source de Stolfi](https://www.ic.unicamp.br/~stolfi/EXPORT/voynich/Notes/034/Note-034.html) signale aussi cinq chiffres ordinaires près de la suite marginale de f49v. Le prochain test pertinent consiste à vérifier les images et à chercher une règle de comptage capable de prédire le reste de cette suite, en conservant une branche avec `f/p` distincts et une autre avec `f/p` rapprochés. La date des annotations et leur valeur comme indice resteront à établir ; ce test n'a pas été exécuté dans cette phase. L'objectif demeure le déchiffrement du manuscrit, toujours non atteint.
