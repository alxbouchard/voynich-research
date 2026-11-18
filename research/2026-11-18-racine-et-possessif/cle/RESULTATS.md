# D’une clé qui lit trois mots au quatrième mot d’une phrase

La formule d’essai rapproche *radix eius* (« sa racine ») de *de foliis eius* (« de ses feuilles ») dans les vers sur la chélidoine. La copie de 1478 écrit *foleis*. Le programme reçoit les deux noms et *eius* puis laisse la clé lire le mot précédant « feuilles ». Les cinq mots latins et la distance d’une à six lignes sont fixés avant la sélection des passages du Voynich. La position des lignes n’impose aucune identité entre vers latin et ligne graphique du manuscrit. [Protocole](PROTOCOLE.md) · [Concordance historique](../temoin/RAPPORT.md)

## Contrôle sur un livre dont on peut vérifier chaque mot

Nous avons chiffré les 77 notices avec trois alphabets. La fonction qui cherche les passages ignore les valeurs de ces alphabets et le nom de la plante attendue. Chaque essai est répété en employant la graphie de l’édition puis en remplaçant *foliis* par *foleis* au seul vers 1707. Il s’agit de deux variantes du même texte, l’édition conserve ailleurs ses propres graphies.

| Alphabet ayant produit le cryptogramme | Localisations qui satisfont les trois mots | Résultat du mot masqué au bon endroit |
|---|---:|---|
| Une lettre par signe | 1 sur tout le poème | La bonne table et le mot *de* sont imposés aux vers 1704 et 1707. |
| Un signe peut représenter di, iu, fo ou is | 14 | Les signes du mot précédent ne sont pas tous appris. Même la vraie table partielle laisse le mot indéterminé. |
| Un signe peut représenter ra, fo ou is | 10 | Le bon lieu est le seul admettant *de*. Les mêmes indices y autorisent aussi *ade*. |

Les effectifs sont les mêmes dans chacune des deux variantes orthographiques. Avec 99 redistributions des mots à l’intérieur de chaque vers et l’alphabet simple, une conserve un passage rendant *de*. C’est la **localisation véritable** du poème qui subsiste dans ce tirage. Les deux lectures de contraste *ed* et *in* n’apparaissent dans aucun des six calculs sur les textes non mélangés. [Résultats par chiffrage et tirages](calibration.json)

## Les paragraphes de 64 feuillets botaniques

Les 1 569 lignes P0 communes aux deux éditions se répartissent entre 128 faces. Une paire de mots contigus doit être présente au même lieu dans les deux éditions sous les deux traitements du blanc douteux. Les interruptions physiques et les signes douteux arrêtent les paires. Pour les premiers et seconds couples de mots, on exige une distance d’une à six lignes sur la même face. La fenêtre peut donc franchir un changement de paragraphe. Un même triplet de graphies aux mêmes deux lignes ne compte qu’une fois, même s’il admet plusieurs clés.

Avec une lettre par signe, sept fenêtres respectent les longueurs et aucune n’admet la lecture. Avec une ou deux lettres, 359 fenêtres respectent les longueurs, 64 peuvent lire les deux premiers mots et cinq localisations admettent aussi le troisième. Aucune ne lit le mot *de* avec les valeurs apprises. Dans deux cas, le mot antérieur fait défaut au sens du protocole. Dans les trois autres, des signes manquent dans la table et le groupe compte déjà plus de deux unités. Lui donner des valeurs non vides ne pourrait pas produire *de*. [Tables complètes des cinq passages](voynich.json)

| Premier et second couple | Groupe proposé pour « racine », « de cette plante », « feuilles » | Graphie et nombre de tables | Mot avant « feuilles » |
|---|---|---|---|
| f11r.3, f11r.5 | chol, cthy, daiin | foliis, 6 | Groupe incertain |
| f15r.3, f15r.5 | chol, cthy, daiin | foliis, les mêmes 6 | Coupure physique par la tige |
| f15r.3, f15r.7 | chol, cthy, shkaiin | foliis, 3 | daiin |
| f43v.12, f43v.16 | dar, chey, qoky | foliis, 18, ou foleis, 18 | oteos |
| f47r.3, f47r.7 | ckhey, chol, cthaiin | foliis, 18 | kchor |

Le code *cth* représente l’unité composée EVA. Le mot *radix* est ici la valeur proposée à `chol` dans certaines affectations, il n’est pas observé en alphabet latin sur les pages. Les chiffres ci-dessus incluent les graphies *foliis* et *foleis* sans compter deux fois f43v dans les localisations. [Photographies des deux passages qui partagent six tables](../photos/NOTE.md)

## Ce que ces six tables font lire après « ses feuilles »

Toutes les six font lire *ei* à l’unité `cth` et *us* à `y`. Trois font lire *f* à `d`, trois *fo*. Le groupe `dy` est séparé à f15r.5 et les six tables donnent donc comme lectures complètes *fus* ou *fous*. Aucun de ces deux mots ne figure parmi les 13 967 mots de l’édition du poème, ni parmi les cinq mots réellement placés après *foliis eius* (*factum*, *tritis*, *elixis*, *triginta*, *contusis*). La séparation de `dy` à f11r.5 reste incertaine. [Prédiction de transfert](PREDICTION-DY.md) · [Positions et résultats](suite.json)

Sur les **124 autres faces** de l’herbier Voynich, nous avons appliqué chaque table à toutes les suites de deux ou trois mots contigus dont chaque mot comprend au moins deux unités de signe. Chaque table lit 379 paires (246 graphies de paires) et 89 triplets (86 graphies de triplets). Trois paires différentes figurent dans le *Macer*, totalisant 15 occurrences du côté du Voynich. Ce sont les deux couples de l’ajustement et l’un de ces couples en ordre inverse. **Aucun triplet** n'est attesté dans le même ordre dans le poème. L’absence d’une phrase dans cet ouvrage délimite la comparaison avec lui.

Sur ces mêmes faces, parmi 8 665 occurrences de mots accordées par ligne dans les quatre lectures, on trouve 187 `chol`, 74 `cthy` et 406 `daiin`. Dans les 13 849 mots latins des notices hors chélidoine, *radix*, *eius* et *foliis* ont 23, 125 et 32 occurrences. Ces dénominateurs comptent davantage de mots latins rares alors que la concordance des transcriptions peut privilégier les mots fréquents et plus lisibles. Dans chaque transcription intégrale les proportions des trois groupes restent consultables séparément. [Chiffres et contextes](suite.json)

À f10r.7, la forme courte découverte après examen du transfert (`daiin cth`) donnerait *foliis ei* avec chacune de ces tables. Le poème contient trois occurrences de *ei* et aucune de cette paire. Sous sa lecture pronominale, *ei* peut être le datif « à lui / à elle », *eius* est le génitif « de lui / d’elle ». L’ordre et le contexte syntaxique importent. Une lecture *ei* ne fournit donc pas le possessif attendu par le simple retrait de *us*. Sur les faces de réserve, `cth` isolé concorde à f10r.7 et à f96v.3, chaque fois contre une partie du dessin. L’association avec le bord mérite de rester distincte de cette tentative latine. [Deux recadrages et contrôle des formes longues](../transfert/RAPPORT.md) · [Paradigme latin de is, ea, id](https://dcc.dickinson.edu/grammar/latin/demonstrative-pronouns-paradigms)

## Le rapprochement des lignes 3 et 5 est-il fréquent ?

Dans l’ensemble de l’herbier, une seule combinaison du type A M puis B M deux lignes plus loin, où les trois mots diffèrent, se retrouve sur deux feuillets distincts dans les paires concordantes. Il s’agit précisément de `chol cthy` puis `daiin cthy`, sur f11r et f15r. Dans les deux cas les lignes sont numérotées 3 et 5. Nous avons recherché tous les motifs ainsi définis après avoir remarqué celui-ci. En permutant les lignes entières de chaque face, 291 des 999 tirages donnent un motif quelconque répété à deux lignes d’écart sur au moins deux feuillets. Dans 42 tirages, un tel motif possède **aussi le même numéro de ligne de départ** aux deux endroits. Aucun de ces 42 ne reproduit les trois graphies particulières du cas observé. Ces chiffres ne tiennent pas compte de toutes les distances et de tous les autres mécanismes envisagés au cours du projet. Le mélange détruit les débuts et les fins de paragraphes. [Protocole du contrôle](CONTROLE-POSITIONS.md) · [Tous les tirages groupés](positions.json)

Les scripts se rejouent hors ligne depuis ce dossier avec `python3 -B chercher.py`, puis `python3 -B suite.py` et `python3 -B positions.py`. Le premier vérifie la vraie clé des trois alphabets sur les deux versions du texte de contrôle. [Recherche de clés](chercher.py) · [Transfert](suite.py) · [Permutations des lignes](positions.py)
