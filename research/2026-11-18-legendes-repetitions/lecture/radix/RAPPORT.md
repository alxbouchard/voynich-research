# Si otaly se lisait radix, que lirait-on sur les autres feuillets ?

La proposition `otaly` = *radix* fixe cinq valeurs, dans l’ordre **o → r, t → a, a → d, l → i, y → x**. Une fois appliquée aux autres feuillets, elle rend **2 graphies sur 49** qui se rencontrent à l’identique dans l’herbier latin, soit **37 occurrences sur 512**. Elle produit *iri* à partir de `lol` (30 fois) et *diri* à partir de `alol` (7 fois). À elles seules, ces deux concordances ne permettent pas de lire « racine » sur les dessins. [Prédiction déposée avant le calcul](../PREDICTION-RADIX.md) · [Tous les résultats](resultats.json)

## Les cinq sorties les plus fréquentes

| Voynich | Lecture calculée | Occurrences | Premier lieu | Emploi vérifié |
|---|---|---:|---|---|
| `otal` | *radi* | 102 | f9v.7 | Absent du *Macer*. Morpheus propose le verbe *rado* et le nom *radius*. Le Lévitique 14,41 emploie *radi* pour l’action de racler la paroi d’une maison. |
| `oty` | *rax* | 91 | f6v.5 | Absent du *Macer*. Morpheus ne renvoie aucune analyse. |
| `otol` | *rari* | 58 | f1r.21 | Absent du *Macer*. Flexion de *rarus*, attestée sur des nageurs épars dans l’*Énéide*, I, 118. |
| `oly` | *rix* | 50 | f3v.1 | Absent du *Macer*. Morpheus ne renvoie aucune analyse. |
| `lol` | *iri* | 30 | f1v.6 | Présent dans le *Macer* aux vers 70 et 1456. Les deux emplois concernent l’iris dans le poème. Le second ouvre sa notice et parle de la couleur de ses fleurs. |

Le dictionnaire de Lewis et Short donne « racler » et « raser » au verbe *rado*. L’analyseur donne *radi* comme infinitif passif de ce verbe ou comme forme de *radius*. Aucune de ces analyses n’en fait une flexion de *radix*. Le nominatif pluriel *rari* est directement lisible chez Virgile. Pour *rax* et *rix*, une réponse vide d’un analyseur de latin ancien ne démontre pas qu’aucun scribe médiéval n’a écrit cette graphie. [Lewis et Short, *rado*](https://atlas.perseus.tufts.edu/dictionaries/entry/urn:cite2:scaife-viewer:dictionary-entries.atlas_v1:lat.ls.perseus-eng2-n40353/) · [Lévitique 14,41, texte de la Vulgate](https://www.bibliacatolica.com.br/vulgata-latina-vs-neo-vulgata-latina/liber-leviticus/14/) · [Lewis et Short, *rarus*](https://atlas.perseus.tufts.edu/dictionaries/entry/urn:cite2:scaife-viewer:dictionary-entries.atlas_v1:lat.ls.perseus-eng2-n40430/) · [Oxford CLASP, *Énéide*, livre I](https://clasp.ell.ox.ac.uk/db-latest/poem/%C2%A3.VERGIL.Aeneid01)

Le moteur Morpheus rattache *iri* au verbe *eo*. La lecture du vers 1456 montre pourquoi le texte d’origine est nécessaire pour interpréter une forme. Le passage donne la couleur des fleurs comme origine du nom de l’iris. Dans le poème, *diri* qualifie *morbi* au vers 1200. Nous avons interrogé le service Perseids sur les cinq formes du tableau, puis sur *diri*, *radix* et le témoin inventé *xqxqxxq*. Les huit réponses HTTP 201, leurs empreintes, les lemmes et les catégories renvoyés figurent au dossier. [Réponses et liens des huit requêtes](morpheus.json) · [Service de morphologie Perseids](https://www.perseids.org/libraries-tools/) · [Vers du *Macer* avec leur contexte](../../../2026-11-18-opcheor-paralleles/latin/vers.tsv)

## Lire deux mots de suite

Nous avons recherché toutes les paires contiguës entièrement couvertes par la clé et confirmées dans le même ordre sur la même ligne dans les quatre lectures. Chaque mot doit comporter au moins trois signes et le mot utilisé pour établir la clé reste exclu. Une rupture matérielle de la ligne interrompt la paire. Nous trouvons **11 occurrences de paires**, soit **9 paires différentes**, toutes dans les lignes ordinaires P0. **Aucune** ne donne deux formes qui figurent toutes les deux dans le *Macer*, et aucune n’y reproduit une suite exacte de deux mots. La paire la plus répétée donne *rari rax* à f9v.4, f76v.32 et f106v.44. Un autre passage donne *radi radi* à f86v6.42. Ce contrôle de contexte supplémentaire conserve le dénominateur entier. [Relevé des onze paires et lectures](voisins.tsv)

## Comparaison des clés

Les valeurs de *radix* sont toutes différentes. Parmi leurs **120 ordres**, clé essayée comprise, 5 donnent au moins 37 occurrences du *Macer*, 10 donnent au moins 2 graphies et 4 satisfont ces deux conditions à la fois. Trois ordres dépassent 37 occurrences. La meilleure permutation en produit 110 avec trois graphies. Ce classement dépend des lettres choisies grâce à l’hypothèse et n’évalue pas l’ensemble des hypothèses qui pourraient être essayées sur le manuscrit. [Scores de chaque permutation](permutations.tsv)

Pour *foliis*, les cinq découpages non vides en cinq valeurs donnent tous **0 graphie et 0 occurrence** dans le *Macer* hors feuillets de départ. Les découpages `fo/l/i/i/s` et `f/ol/i/i/s` ont chacun 60 permutations distinctes, en raison de la répétition de i. Chacun des trois autres en a 120. Pour *flos*, quatre lettres ne suffisent pas à fournir au moins une lettre à chacun des cinq signes. Il n’existe aucune clé conforme à la règle annoncée pour cette lecture. [Tables et effectifs](resultats.json)

## Ce qui est compté

Les feuillets numérotés 88 et 99 sont entièrement exclus. Tous les autres feuillets et panneaux sont admissibles. Le résultat principal couvre **4 048 loci de type P** présents avec le même code dans les éditions de Takahashi et de Zandbergen–Landini. Les blancs douteux sont successivement joints et séparés. Une graphie de trois signes ou plus parmi o, t, a, l, y est retenue avec la plus petite multiplicité observée sur la même ligne dans les quatre lectures. Le rang exact entre les mots peut varier d’une lecture à l’autre. Les signes spéciaux, alternatifs et ligatures balisées rendent le groupe inéligible. Neuf occurrences supplémentaires de `otaly` hors des deux feuillets ont été exclues comme répétitions du mot employé à établir la clé.

Les lignes ordinaires P0 seules donnent 49 graphies et 486 occurrences, dont 35 dans le *Macer* sous la clé *radix*. Les autres classes comprises dans le total sont Pt (10 lignes), Pc (17), Pr (12), P1 (72) et Pb (123). Les ensembles de signes sont petits et l’expérience ne déchiffre aucun mot qui contienne un autre signe. [Détail de toutes les lignes positives et de leur multiplicité](lignes.tsv) · [Toutes les sorties de la clé *radix*](radix.tsv) · [Transcriptions d’origine et conventions](https://www.voynich.nu/transcr.html)

## Quelle est la couverture du témoin latin ?

Quand on retire tour à tour chacune des 77 notices, les formes exactes présentes dans le vocabulaire des 76 autres couvrent **11 609 des 13 967 occurrences**, soit **83,12 %**. Selon la notice, la couverture va de 73,35 % à 94,44 %. Le décompte par graphie à l’intérieur de chaque notice donne 9 124 formes déjà vues sur 11 398, une même graphie pouvant participer à plusieurs notices. Le lexique des 77 notices réunies comporte 3 897 graphies. Ces contrôles reposent sur du texte latin continu et sur un seul ouvrage. [Les 77 tests avec leur dénominateur](couverture.tsv)

À titre de sensibilité supplémentaire, en limitant cette dernière expérience aux mots latins d’au moins trois lettres, composés uniquement de r, a, d, i, x, et distincts de *radix*, on ne dispose que de **14 occurrences**, dont 9 se retrouvent dans les autres notices. Le petit nombre de formes comparables limite l’interprétation du taux global. [Effectifs de ce second décompte](resultats.json)

Pour reproduire les tableaux et les calculs hors ligne, lancer `python3 -B verifier.py`. Le programme vérifie les empreintes des deux transcriptions et du texte latin. Le contrôle de dictionnaire conserve les analyses externes obtenues et les URL de requête. [Programme](verifier.py) · [Texte historique, crédits et normalisation](../../../2026-11-18-opcheor-paralleles/latin/SOURCE.md)
