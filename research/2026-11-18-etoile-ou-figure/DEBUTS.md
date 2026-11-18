# Une inscription de figure retrouve-t-elle sa place dans la prose ?

**Sur les cinq emplois réservés de `dshedy`, le mot est le premier de la ligne.** Deux sont sur le recto et le verso d’un même feuillet botanique. Les trois autres se trouvent sur trois feuillets du dernier cahier. Les photos permettent de voir le signe supplémentaire au début ainsi qu’une ligne où la prévision l’ajoute à tort. [Annonces avant ouverture](https://github.com/alxbouchard/voynich-research/tree/02f28f5/research/2026-11-18-etoile-ou-figure) · [Étiquette et six débuts de ligne sur photographies](debuts-photo/RAPPORT.md)

## Du dessin à la prédiction

Sur f84r.12, la graphie se trouve au-dessus d’une figure et près d’un écoulement. L’analyse des bains a repéré quinze emplois de ce mot dans la prose de même main et de classe B de Currier. On pouvait aligner un mot à sa droite aux quinze endroits, et un mot à sa gauche à un seul. Cette dissymétrie pouvait venir des espaces, d’un dessin ou du début d’une ligne. Nous avons ensuite annoncé sa place dans l’herbier et le dernier cahier, et masqué la présence du premier d pour toutes les occurrences de `dshedy` ou `shedy` de ces deux lots. [Constat initial sur les voisins](VOISINS-ANNONCES.json) · [Hypothèses et témoins](DEBUT-AVANT.md)

| Lot de prose | Occurrences de dshedy | Dont premier mot | Occurrences de shedy | Dont premier mot | Règle « d au premier mot » | Toujours shedy |
|---|---:|---:|---:|---:|---:|---:|
| Bains, main 2, Currier B, lot de départ | 15 | 14 | 173 | 3 | — | — |
| Herbier, même main et classe | 2 | 2 | 21 | 2 | 21/23 | 21/23 |
| Dernier cahier, réserve distincte | 3 | 3 | 105 | 1 | 107/108 | 105/108 |

Dans l’herbier, deux insertions correctes compensent deux fausses insertions. Dans le dernier cahier, les quatre places initiales contiennent trois `dshedy` et un `shedy`. En les comparant aux places strictement intérieures sur la même face, seulement deux faces sont informatives pour le contraste avec `shedy` (probabilité conditionnelle unilatérale 0,083). Les trois faces sont informatives pour le contraste plus large avec les autres finales en `edy` (0,00070). Les deux orthographes restent susceptibles d’avoir des fonctions ou des sens distincts. [Résultats par lieu et conditionnement sur la face](DEBUT-RESULTATS.json)

Les effets de position à l’échelle d’une ligne étaient déjà documentés. Les nouvelles annonces vérifient ici cinq emplois précis d’une graphie également présente dans une légende. [Bowern et Lindemann, sections 4 et 5](https://alumniacademy.yale.edu/sites/default/files/2021-07/The%20Linguistics%20of%20the%20Voynich%20Manuscript.pdf)

## Lire un mot de plus

Sur f43r.9, la ligne commence par `dshedy qotedy`. Sur f43v.13, elle commence par `dshedy tedy`. La prédiction tirée des bains, `qokedy` à droite, échoue des deux côtés. Les trois autres feuillets ont alors servi à une seconde épreuve. Les possibilités exactes `qotedy` et `tedy` ont été annoncées avant vérification. Les voisins réellement écrits sont `qoedaiin` sur f105v.3, `qoteey` sur f106r.44 et `qotshedy` sur f115r.16. Les trois manquent la finale prévue de quatre unités. L’un des 96 voisins lisibles à droite de la forme courte `shedy` répond à la règle. Les signes après le premier mot de f43 ne suffisent donc pas à lire la suite ailleurs. [Prédiction de la paire](suites/AVANT.md) · [Les trois dévoilements et les 96 mots témoins](suites/RESULTATS.json)

Pour toutes les graphies en `edy` relevées près des personnes, les modèles de voisins appris dans les bains donnent un premier choix exact sur 52 places testables en prose botanique. Le modèle qui utilise seulement la finale en retrouve deux et le modèle ignorant le mot de départ en retrouve une. [Annonces et règle](VOISINS-AVANT.md) · [Toutes les comparaisons](VOISINS-RESULTATS.json)

## Ce que la finale révèle ailleurs

La prédiction portait sur la présence de `edy` dans plus de la moitié des pages de plantes de la même main et de la même classe que les bains. Elle se vérifie sur **20 faces sur 20**, soit 241 mots sur 1 723. Dans la prose des 19 faces des bains classées de la même manière, 1 318 mots sur 4 708 portent la finale. Dans les pages botaniques attribuées à la main 1 et à la classe A, la finale ne figure que 4 fois sur 6 029 mots, répartis sur 4 faces sur 95. Le sujet « plantes » admet donc des fréquences radicalement différentes. La main et la classe coïncident dans ces deux ensembles. La longueur, les habitudes d’écriture, le livre ou le sujet peuvent contribuer à la différence. Les catégories de Currier s’appuient déjà sur des régularités du texte. [Annonce sur le transfert](SUFFIXE-AVANT.md) · [Comptages, y compris les autres mains et les mots de cinq signes](SUFFIXE.json)
