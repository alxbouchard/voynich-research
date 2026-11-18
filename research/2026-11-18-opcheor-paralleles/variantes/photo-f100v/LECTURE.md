# Sur le parchemin, où sont écrits okeor et okeol ?

**La paire se trouve vers le bord droit de f100v, sur la troisième des neuf lignes de prose sous les fragments de plantes.** Le premier groupe se termine par un trait à crochet dont la pointe remonte. Le deuxième présente à la même place une petite boucle verticale fermée. En amont de ces deux finales, on retrouve deux fois une boucle initiale, une haute hampe à retour et de petits tracés bas. Les groupes sont séparés par du parchemin libre. Une troisième inscription beaucoup plus courte, `dy`, ferme la ligne. Le contexte et le détail permettent de contrôler l’ordre sans se fier au seul numéro de ligne moderne. [Page et trois lignes repérées](page-et-paragraphe.jpg) · [Quatre derniers groupes, pixels natifs](deux-finales.png)

Les bandes d’écriture descendent légèrement de gauche à droite sur le cliché. La ligne au-dessus commence par `sor cheey dair` et se termine avec `qokeol` puis `chotols` (ou `chotol s` si l’on sépare le blanc faible de ZL). La ligne au-dessous commence par le groupe transcrit `chockhey` en IT2a et ZL3b. Les deux éditions donnent de la ligne cible `ches okeor okeol dy` à droite. Le premier mot du couple est le 8e en IT et en ZL aux espaces faibles joints ; il devient le 9e en ZL aux espaces faibles séparés. Le changement de rang vient d’un blanc plus tôt sur la même ligne. [Transcription IT](https://www.voynich.nu/data/IT2a-n.txt) · [Transcription ZL](https://www.voynich.nu/data/ZL3b-n.txt)

Dans l’interlinéaire mis en forme par Jorge Stolfi en 1998, ces trois lignes de prose sont numérotées P.2, P.3 et P.4. Sur **P.3**, les versions H et F portent toutes deux `okeor okeol dy`. F coupe le quatrième groupe de H en deux et lit `cher` juste avant la paire, là où H donne `ches`. Sur P.4, plusieurs lectures et coupures divergent au début, dont `chockhey` chez H et `shockhey` chez F. H est la lecture de Takahashi reprise dans IT. Ces fichiers décrivent le même objet et n’apportent pas trois confirmations indépendantes de sa signification. [Anciennes lectures H et F, bloc P au bas de la notice](https://www.voynich.nu/q19/f100v_tr.txt)

## La légende végétale qui précède le paragraphe

Le premier fragment de la troisième rangée, numéroté 140 dans le catalogue, montre trois feuilles et une attache rouge prolongée de traits fins. Un mot se trouve à droite de sa base. On voit la boucle initiale, la hampe, puis immédiatement à droite de la hampe un groupe de traits bas reliés en haut. ZL, IT et les lignes H, K et V de l’ancienne notice B.1 transcrivent `okcheor`. Sur la même page, le premier des deux mots de prose comparés est `okeor`, avec une unité EVA `ch` de moins. Sur f89r2, au contraire, la légende `opcheor` et le premier mot de la paire se correspondent intégralement dans les deux éditions modernes. Les légendes de f89r2 et de f100v se distinguent elles-mêmes par `p` et `k`. Ces comparaisons sont graphiques. La position au-dessus du paragraphe ne permet pas de déterminer de quel fragment traite la troisième ligne. [Fragment 140 et légende](fragment140.jpg) · [Légende seule, pixels natifs](legende140.png) · [Catalogue du cahier 19](https://www.voynich.nu/q19/index.html#f100v)

## Source photographique et reproduction

Le manifeste de Yale décrit la vue 1006249 comme une double page « 100v and 101r ». Le verso 100 occupe la partie gauche. Le JPEG du Beinecke MS 408 mesure 7 486 × 3 715 pixels. Son SHA-256 est `72637b9770f40f7a8ff6b96a551e64775e88994ae69bafec0b43d48974364c33`. Toutes les coordonnées qui suivent sont celles du cliché complet, mesurées depuis le coin supérieur gauche. Les rectangles de fin sont exclus. [Manuscrit et vue de la double page](https://collections.library.yale.edu/catalog/2002046?child_oid=1006249) · [JPEG source](https://collections.library.yale.edu/iiif/2/1006249/full/full/0/default.jpg)

| Élément | Rectangle natif, x1, y1, x2, y2 |
|---|---|
| Bloc de prose sur la planche | 750, 2335, 2770, 3130 |
| Groupe `okeor` de f100v.16 | 2237, 2631, 2419, 2714 |
| Groupe `okeol` qui le suit | 2451, 2637, 2614, 2718 |
| PNG des quatre groupes de la ligne | 2040, 2617, 2720, 2728 |
| Premier fragment de la troisième rangée | 605, 1340, 1285, 2370 |
| PNG de sa légende | 982, 2146, 1218, 2246 |

Exécuter `python3 -B prelever.py 1006249.jpg` depuis ce dossier avec Python et Pillow. Les deux PNG conservent les pixels du JPEG natif. Les images JPEG de contexte permettent le repérage. [Script de prélèvement](prelever.py) · [Région de la paire chez Yale](https://collections.library.yale.edu/iiif/2/1006249/2040,2617,680,111/full/0/default.jpg)
