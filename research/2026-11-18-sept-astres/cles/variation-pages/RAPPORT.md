# La graphie changerait-elle d’une page à l’autre ?

Cet ajout exploratoire compare les sept inscriptions directement aux sept autres. Il examine si une table d’écriture différente d’un feuillet à l’autre pourrait rendre compte des rapprochements publiés. **Les trois rapprochements choisis pour leurs débuts communs ne suffisent pas à construire une telle table.** Avec une table constante, le maximum atteint deux des sept paires publiées. Aucune des 5 040 réaffectations des partenaires ne couvre les sept. [Résultats par paire et par édition](variation.json)

Une seule des trois paires montre d’où vient la difficulté. Sur f67r2.31, `opcholdy` a sept unités EVA, dont la ligature `ch`. Sur f72r3.27, `opalal` en a six. Développer chaque unité de la première inscription en au moins une unité de la seconde produirait un mot trop long. En sens inverse, `opalal` se termine par deux `al` identiques. Toute table constante développerait ces deux groupes de signes en deux séquences identiques. Le dernier signe de la séquence devrait donc apparaître au moins deux fois dans `opcholdy`, où le `y` final est unique. Les deux éditions s’accordent sur ces deux graphies.

| Règle commune | Maximum des sept paires publiées, premiers groupes | Maximum, inscriptions entières | Tables sur les trois paires des préfixes |
|---|---:|---:|---:|
| Un glyphe distinct pour un glyphe | 1 | 1 | 0 |
| Un glyphe de f67r2 donne 1 à 3 glyphes de f72r3 | 2 | 2 | 0 |
| Un glyphe de f72r3 donne 1 à 3 glyphes de f67r2 | 1 | 1 | 0 |

Ces maxima autorisent les variantes des deux éditions à chaque lieu. Les premiers groupes et les inscriptions entières concaténées sont traités séparément, avec les espaces douteux joints ou séparés et la segmentation en glyphes EVA ou en caractères ASCII. Les trois paires fixées à l’avance sont f72r3.27, .28 et .30 avec f67r2.31, .47 et .37 respectivement. Aucune clé construite sur ces trois positions n’atteint l’étape des quatre paires réservées.

Dans chacun des trois témoins synthétiques, les trois positions d’apprentissage imposent une table unique qui donne l’écriture exacte des quatre autres positions. Altérer le dernier signe d’un seul mot réservé conserve la table des trois et fait échouer ce mot. Les six autres paires restent lisibles.

L’essai borne une classe précise de variations entre pages. Il laisse ouvertes, entre autres, des flexions différentes, des mots apparentés ou une modification de certains fragments seulement. Il ne permet d’assigner un nom d’astre à aucune inscription.

Depuis la racine du dépôt, exécuter `python3 research/2026-11-18-sept-astres/cles/variation-pages/variation.py`. Le [programme](variation.py) enregistre pour chaque variante les sous-ensembles maximaux, les résultats sur les trois paires et les éventuels appariements complets.
