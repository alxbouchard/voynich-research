# La colonne du mot permet-elle de choisir le bon paragraphe ?

La légende `opcheor` du feuillet f89r2 permet de prédire le troisième paragraphe si on choisit le paragraphe où la distance horizontale au mot le plus proche, mesurée sur chaque ligne, a la plus petite médiane. **Ce paragraphe contient bien `opcheor`**, au cinquième rang de sa première ligne, f89r2.22. Mais le centre de la légende désignait le douzième mot de cette ligne, `sheodal`. L’essai retrouve le bon passage sans retrouver le bon mot. Ce cas de reprise était connu avant que la règle géométrique soit posée. [Classements publiés avant vérification](https://github.com/alxbouchard/voynich-research/blob/ec70b18/research/2026-11-18-du-dessin-au-paragraphe/passages/PREDICTIONS.json.gz) · [Tous les mots ouverts](RESULTATS.json.gz)

## Dénominateurs et comparaison

Les quinze panneaux pharmaceutiques qui portent des légendes ont été examinés. On garde les étiquettes autonomes d’un seul groupe d’au moins trois signes dont la forme concorde dans les deux transcriptions et les deux traitements des petits blancs. La carte est obtenue en rattachant les mots du visualiseur aux loci de Takahashi. Elle conserve seulement les coordonnées pour la prose. Le choix du paragraphe est fait avant d’ouvrir son texte. Pour chaque ligne, on prend le centre de mot le plus proche dans le sens horizontal, puis on compare la médiane de ces écarts entre paragraphes, en corrigeant l’inclinaison de l’écriture. [Règle](PROTOCOLE.md) · [Carte de la prose sans les mots](CARTE-MASQUEE.json.gz)

| Délimitation des paragraphes en concurrence | Panneaux | Paragraphes | Légendes comparées | Légendes reprises dans un passage au même rang dans les quatre lectures | Bon paragraphe prédit par la colonne | Mot prédit à la bonne place sur sa ligne |
|---|---:|---:|---:|---:|---:|---:|
| Limites strictement identiques dans les deux transcriptions | 11 | 33 | 92 | 4 | 1 | 0 / 250 annonces vérifiables |
| Regroupement aux limites communes lorsque l’une des éditions subdivise le passage | 13 | 37 | 107 | 6 | 1 | 0 / 312 annonces vérifiables |

Dans la première comparaison, 25 autres légendes se trouvent sur trois panneaux pour lesquels il ne reste qu’un paragraphe admis. Ce choix forcé trouve une reprise. Dans la seconde, les dix légendes restantes d’un panneau à paragraphe unique ne donnent aucune reprise. La carte de f101v place de nombreux mots de gauche au bord du cliché partiel et empêche le classement automatique. Une nouvelle mesure sur le dépliant complet y a permis de sélectionner le premier paragraphe pour la légende `okol` et de vérifier la lecture à proximité du pli. [Découpages concurrents des blocs de f102](DECOUPAGES.md) · [Récupération photographique de f101v](f101/RAPPORT.md)

| Légende | Bloc réellement porteur du mot, parmi les blocs réunis | Prévision de la colonne |
|---|---:|---:|
| `okol`, f88r.15 | 2 sur 3 | 1 |
| `opcheor`, f89r2.5 | 3 sur 3 | **3** |
| `sheol`, f89v2.5 | 1 sur 3 | 3 |
| `okeoly`, f99r.25 | 1 sur 4 | 3 |
| `okeody`, f102v1.3 | 2 sur 2 | 1 |
| `cheor`, f102v2.11 | 2 sur 2 | 1 |

Sur f102 les deux mots de prose sont presque à la verticale de leur propre inscription lorsqu’on connaît leur ligne et la rangée de dessins. Pourtant, le premier bloc a plus régulièrement des mots dans cette colonne au fil de ses lignes. La règle choisit ce premier bloc dans les deux cas, alors que c’est le second qui contient le mot recherché. Le résultat reste le même en prenant les paragraphes de chacune des transcriptions séparément. [Mesures antérieures sur les deux lignes](../../2026-11-18-noms-dans-une-phrase/enumeration/verticale/RAPPORT.md)

## Ce que prédisent les autres repères

Nous avons permuté les graphies entre les emplacements des légendes de chaque panneau. Les paragraphes, leurs longueurs, leurs vraies reprises et la disposition de toutes les cases restent ainsi identiques. Sur les 107 légendes, les noms permutés donnent en moyenne 2,48 bons paragraphes par la colonne. La seule réussite observée est atteinte ou dépassée dans 96,59 % des attributions. Dans la comparaison stricte, l’espérance est 1,69 et la proportion 90 %. Les étiquettes sont peu nombreuses à revenir sous la forme exacte admise. [Calcul exact des permutations](verifier.py)

| Repère prédéfini | Bons blocs parmi les six reprises | Moyenne en permutant les étiquettes |
|---|---:|---:|
| Colonne des mots dans l’ensemble des lignes | 1 | 2,48 |
| Distance verticale à la ligne la plus proche | 2 | 2,24 |
| Colonne du tout premier mot du bloc | 4 | 3,97 |
| Colonne du tout dernier mot | 1 | 2,39 |
| Bloc contenant le plus de mots | 3 | 3,00 |

Si le même groupe peut se trouver à des rangs différents dans les deux éditions pourvu qu’il figure sur la même ligne, le nombre d’étiquettes reprises monte de six à huit. Avec la seule lecture Takahashi, il monte à neuf. La règle de colonne conserve une seule réussite dans les deux cas. Pour les prédictions mot à mot, le choix de la case voisine décalée vers la droite donne également zéro sur 324 annonces vérifiables. Plusieurs annonces visent la même case et plusieurs panneaux sont sur le même feuillet.

## Reproduction

Les quinze cartes sources sont désignées par leur URL et leur empreinte. Dans `CACHE`, les nommer f88r.json, f88v.json, etc. Pour le feuillet 101, le fichier du visualiseur s’appelle f101v2.js et sa copie locale f101v.json. Exécuter `python3 -B preparer.py CACHE`, `python3 -B predire.py` et `python3 -B verifier.py` depuis ce dossier. Le deuxième calcul ne lit aucun mot des paragraphes. Les quatre combinaisons de lecture proviennent de deux transcriptions d’un même manuscrit. [Bibliothèque des cartes](SOURCES.json) · [Repérage des loci](preparer.py) · [Classements](predire.py) · [Ouverture des réponses](verifier.py)
