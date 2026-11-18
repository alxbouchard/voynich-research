# Peut-on prédire le dernier mot d’une formule thérapeutique ?

**Sur le latin chiffré du livre des bains de Pierre d’Éboli, nous prédisons trois fois sur trois le mot caché *opem*, « secours ». Sur 44 fins de lignes vérifiables du Voynich où les mêmes règles annonçaient *opem*, aucune ne donne ce mot.** Une autre prédiction, indépendante du latin, retrouve le groupe exact `qokedy` à f81v.18, une fois sur dix essais.

## Une formule qui fonctionne sur le livre thermal

Dans la notice d’*Astrunis*, l’eau « apporte du secours » aux yeux malades. Dans celle de *Prato*, l’expression concerne le corps tout entier. À *Bracula*, elle clôt le vers consacré aux troubles énumérés dans le passage. Tous trois finissent littéralement en **prestat opem**. Le verbe *prestat* apparaît cinq fois dans le poème. Le latin du test est celui du texte édité et transcrit dans le dépôt. [Vers originaux, références et mesures](SECOURS.json) · [Provenance du texte](../../2026-11-18-baigneuses-et-conduits/lecture/SOURCE.json)

Nous chiffrons toutes les lettres par une substitution commune au livre. Le programme qui cherche les formules reçoit les mots chiffrés et une occurrence de référence dans une autre notice. Il doit découvrir la correspondance des signes et écrire à l’avance le mot chiffré attendu. Pour *opem*, il produit `nszv` et retrouve cette graphie aux trois endroits, chacun à son tour hors apprentissage. Ces notices ont servi à choisir la formule latine à étudier. L’épreuve vérifie ce qu'on peut transmettre d'une occurrence à une autre sous une clé stable. [Épreuve du secours](SECOURS.md) · [Calcul](secours.py)

Dans les bains du Voynich, 563 lignes présentent une pénultième position concordante et une dernière position à vérifier. En autorisant chaque signe EVA à représenter une ou deux lettres, 45 fins de ligne sur les 276 lisibles où l’on peut ajuster *prestat* acceptent un ajustement local aux deux mots. Vingt et un des 40 autres mots latins de quatre lettres attestés en fin de vers produisent autant d'accords ou davantage. Les trois bifeuillets impairs donnent 284 tables pour les deux mots. Avec ces tables figées, la pénultième position de 46 lignes de deux autres bifeuillets se lit entièrement *prestat* selon au moins une table. Quarante-quatre mots finaux sont vérifiables. **Aucun ne donne *opem* avec la même table.** Trois mots témoins, *amat*, *erit* et *fuit*, réussissent chacun une fois selon cette même procédure. La transposition de la fin du vers latin à la fin de la ligne manuscrite est une hypothèse supplémentaire. [Tables et prévisions avant ouverture du dernier mot](SECOURS-PREDICTIONS.json.gz) · [Toutes les réponses et faux accords](SECOURS.json)

## Une lecture précise éliminée à f75v.48

Le verbe *tollit*, « enlève », apparaît treize fois dans le livre. Dans la notice *Fons Episcopi* (XXVII, vers 3), **tollit genus omne podagre** signifie que le bain enlève toute espèce de goutte. Dans *Sol et Luna* (XXVI, vers 3), l’édition donne « Omne genus gutte tollit; genus omne doloris ». Une ponctuation forte sépare ici *tollit* et *genus*. Le triplet de mots est identique une fois cette ponctuation effacée ; sa construction grammaticale diffère. Deux autres passages témoins permettent un contrôle, *breve nomen habet* (« il porte un nom bref ») et *splene tumente iecur* (passages qui rapprochent la rate enflée et le foie), chacun dans trois notices. [Vers complets et épreuves sur le latin chiffré](LATIN.json)

Une seule amorce de deux mots dans les bains satisfait exactement la structure littérale de **tollit genus** avec une substitution bijective entre unités EVA et lettres. C’est **ycheedy saino**, au cinquième groupe de f75v.48. Le premier mot commence et finit par y, comme *tollit* par t, et les deux e successifs peuvent prendre les deux l. Après ces deux mots, nous avons inscrit **omne** dans le registre de prédictions. Le mot suivant sur la page est **ol**. Ses deux unités excluent les quatre lettres annoncées avec ce modèle. [Transcription interlinéaire et photographie de f75v](https://www.voynich.nu/q13/index.html#f75v) · [Prévisions figées pour les quatre formules](PREDICTIONS.json.gz)

| Deux mots de départ | Mot caché prédit | Voynich, successeurs compatibles si l’on complète les clés | Lectures confirmées sur un autre bifeuillet avec la clé acquise |
|---|---|---:|---:|
| tollit genus | omne | 9 sur 267 | 0 |
| breve nomen | habet | 7 sur 201 | 0 |
| splene tumente | iecur | 2 sur 194 | 0 |
| et si | forte | 0 sur 8 | 0 |

La table porte sur le cas souple, une ou deux lettres par unité et un alignement concordant de la ligne entière. Pour *omne*, 104 des 130 autres mots de quatre lettres du livre font au moins autant d’accords locaux. L’alignement plus permissif au voisinage immédiat conserve le résultat, avec 11 accords sur 412 pour *omne* et aucun transfert. [Tous les dénominateurs et témoins](RESULTATS.json.gz)

## Un troisième groupe prédit sans attribuer de langue

Sur 792 lignes de prose des bains, l’alignement des deux transcriptions et des deux lectures de l’espacement retient 2 106 positions où les deux premiers groupes concordent. L’alignement limité au voisinage immédiat en retient 3 668. Il exige que la même amorce n'apparaisse qu’une fois dans chacune des quatre lectures de la ligne. Une ligne du manuscrit ne vaut pas un vers latin. [Protocole de choix des amorces](PROTOCOLE.md)

| Règle d’alignement | Amorce choisie et troisième mot de f75v.47 | Résultat sur les autres bifeuillets |
|---|---|---|
| Toute la ligne | `shedy qokedy → qokeedy` | 0 sur 8, une neuvième position en désaccord |
| Deux mots contigus et uniques sur la ligne | `ol shedy → qokedy` | 1 sur 10, à f81v.18 |

En prenant toutes les amorces répétées sur plusieurs bifeuillets, on obtient une réussite sur 173 essais avec l’alignement de la ligne entière, et sept sur 364 avec l’alignement local. Les nombres attendus après réaffectation des successeurs sur chaque face sont respectivement 1,95 et 4,41. Pour l’unique succès de l’amorce `ol shedy`, des permutations des derniers mots sur les faces concernées atteignent au moins ce résultat dans environ 27 % des essais. Il s’agit d’un mot réellement prévu sur une autre feuille. Le compte demeure compatible avec sa fréquence habituelle sur ces pages. [Prévisions et lieux](PREDICTIONS.json.gz) · [Vérifications et permutations](RESULTATS.json.gz)

Pour reproduire, lancer depuis ce dossier `python3 -B epreuve.py calibrer CACHE`, `python3 -B epreuve.py predire`, `python3 -B verifier.py CACHE`, `python3 -B secours.py predire CACHE` et `python3 -B secours.py verifier CACHE`, avec le répertoire contenant le texte latin `vers.json` de l’étude des bains. NumPy est nécessaire aux permutations. [Préparation et contrôle latin](epreuve.py) · [Vérification des triplets](verifier.py)
