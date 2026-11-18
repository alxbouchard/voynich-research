# « Nous appelons X, que les Grecs… »

Une formule d’appellation du *Macer* permet de tenter une lecture précise dans le Voynich. Le meilleur rapprochement se trouve à **f102r1.5** : `ytol sheol she olaiin`. Si l’on attribue aux deux mots qui entourent `sheol` les valeurs latines *dicimus* (« nous appelons ») et *quam* (« que »), quatre clés conviennent. Elles permettent toutes de lire entièrement le mot central. Leurs deux seules réponses sont **quamimus** et **quammus**. Aucune ne figure parmi les 13 967 mots du livre latin. Le mot qui suit ne peut donner ni *Graecus*, graphie de l’édition, ni *grecus*, graphie de la copie de 1478. [Clés, emplacements et lectures du mot central](RESULTATS.json) · [Vérification de la variante manuscrite](LECTURE-1478.json)

**L’étiquette `sheol` appartient à un autre panneau**, à f89v2.5 auprès du fragment 53. Elle revient en prose sur son propre panneau à f89v2.7, puis dans le passage examiné à f102r1.5. Les quatre lectures s’accordent à f102r1 sur les mots utiles. La contrainte se voit dans leur écriture : `sheol` commence par `she`, qui devrait donc rendre *quam*, et finit par `ol`, qui forme aussi la fin de `ytol` et devrait rendre *imus* ou *mus*. Cette lecture ne dépend d’aucune identification botanique du fragment 53. [Trois inscriptions photographiées de l’étude antérieure](../../2026-11-18-legendes-et-paragraphes/sheol/trois-inscriptions.png) · [Fac-similé de f102r1](https://www.voynich.nu/q19/index.html#f102r1)

## La formule dans une copie du XVe siècle

Au f. 3r du manuscrit italien Wellcome MS.458, copié en 1478, le vers qui suit la rubrique *De urtica* se lit *Dicimus urticā quam grecus acalife dicit*. Le trait sur la dernière voyelle d’*urticam* abrège le m. L’auteur nomme l’ortie et donne ensuite le nom que lui attribuent les Grecs. L’édition de calcul transcrit *Graecus* et *acalyphe*. Les deux i de `olaiin`, au Voynich, devraient fournir deux fois le même groupe de lettres au latin ; les graphies *graecus* et *grecus* sont chacune entièrement composées de lettres différentes. [Détail du manuscrit de 1478](urtica-1478.jpg) · [Original Wellcome](https://iiif.wellcomecollection.org/image/b19209113_ms_458_0009.JP2/409,1404,2827,624/1500,/0/default.jpg)

La formule revient, au vers 711, avec *acidulam*, nom de plante à l’accusatif comme *urticam*. Au vers 1489, *Enula* est à la première place, suivi lui aussi de *quam Graecus*. Le nom grec et le verbe qui l’introduit peuvent permuter. Nous avons donc choisi pour prévision le mot stable **GRAECUS**, situé deux mots après le nom de la plante. [Trois vers de l’édition avec leurs références](PREDICTIONS.json) · [Provenance et limites de l’édition du poème](../../2026-11-18-opcheor-paralleles/latin/SOURCE.md)

Nous avons chiffré tout le poème avec la même substitution alphabétique, dont la clé restait cachée au programme de lecture. Celui-ci a reçu un exemple dans une autre notice et la graphie chiffrée exacte, fléchie, du nom recherché. Il a annoncé **enrqpbh** pour *Graecus* dans trois notices réservées successivement et a retrouvé cette graphie trois fois. Si l’on conserve seulement le mot chiffré correspondant à *quam* sans tenir compte du nom de plante juste avant, 2 annonces sur 25 réussissent dans chacun des essais. Les trois vers ont servi à choisir la formule ; ce contrôle vérifie qu’elle se transmet sous une clé stable et avec un nom déjà repéré. [Réponses chiffrées et lieux](PREDICTIONS.json)

## Les reprises dans le Voynich

Les 15 panneaux examinés contiennent 213 lignes de prose ordinaire. Les 130 étiquettes de fragments d’un mot concordant représentent 124 graphies distinctes. Le calcul compte chaque place de prose une seule fois et sépare les reprises sur le panneau du dessin d’avec les mots qui figurent en légende sur un autre panneau. Les transcriptions sont celles de Takahashi et Zandbergen–Landini ; elles ont été comparées avec deux traitements des espaces douteux. [Protocole](PROTOCOLE.md)

| Emplacements de prose | Même panneau que l’étiquette | Étiquette sur un autre panneau |
|---|---:|---:|
| Occurrences concordantes de l’ancre | 10 | 101 |
| Deux mots suivants tous deux lisibles | 4 | 53 |
| Premier voisin compatible avec *quam*, une à deux lettres par unité EVA | 1 | 28 |
| Parmi ces cas, deuxième voisin vérifiable | 0 | 17 |
| Deux mots donnant *quam Graecus* ou *quam grecus* sous une même clé | 0 | 0 |

À **f88r.19**, le mot de la légende locale `okol` est suivi de `cheol`, compatible avec *quam*. La ligne s’arrête là. Le mot avant `okol` se lit `qockhoy` dans une transcription et `qockhol` dans l’autre. Nous avons aussi retrouvé `cheol` après `qkol` à f102v1.13, mais l’absence de deuxième voisin dans la ligne de f88r empêche d’y apprendre une graphie à prédire sur l’autre feuillet. À **f99r.18**, l’étiquette reprise `okeoly` est entourée deux fois du même mot `daiin`. Une table stable ne peut faire lire *dicimus* d’un côté et *quam* de l’autre. [Les dix positions et leurs voisins](RESULTATS.json) · [Prédiction du groupe suivant et raison de l’abstention](COPIE-DU-VOISIN.md)

Dans les 17 séquences de comparaison où le deuxième voisin est lisible après un premier voisin ajusté à *quam*, 37 mots de sept lettres et 78 de six lettres effectivement attestés chez Macer peuvent s’ajuster au moins une fois. *Graecus* et *grecus* n’y arrivent jamais. Aucune table du cahier 15 ne permettait de prédire la lecture complète d’un deuxième mot sur un autre feuillet du cahier 19. Cette absence renseigne sur la formule, les limites de ligne et les tables essayées. [Résultats de l’édition](RESULTATS.json) · [Lecture du manuscrit de 1478](MANUSCRIT.md)

Reproduction depuis ce dossier : `python3 -B appellation.py predire`, `python3 -B reporter.py predire`, `python3 -B appellation.py verifier`, `python3 -B reporter.py verifier`, puis `python3 -B appellation.py manuscrit`. [Alignement et contrôle latin](appellation.py) · [Transfert du troisième groupe EVA](reporter.py)
