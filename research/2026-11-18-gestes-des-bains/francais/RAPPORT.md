# Que prédit une liste française de bains dans le Voynich ?

**Au f. 84r, dix groupes successifs suivent le même ordre de répétitions qu’une liste médiévale d’eaux. Les deux suites proposées par cette liste échouent dès le onzième groupe.** Les signes sont visibles sur la même ligne et les formes prédites figurent un peu plus à gauche, ce qui permet de les comparer dans la main du même scribe. La première épreuve, sur des emplacements fixés à l’avance, n’a produit aucune position que l’on puisse à la fois prédire et lire selon son critère strict. Aucune valeur française de groupe n’est établie. [Planche du f. 84r](f84r/planche.jpg) · [Prédictions initiales](PREDICTIONS.json.gz) · [Résultats de l’épreuve principale](CONTROLE.json.gz)

## Ce que teste la méthode

Supposons qu’un groupe entier du Voynich remplace un mot entier. À l’intérieur du passage, un mot répété doit reprendre le même groupe, et deux mots français différents doivent avoir deux groupes différents. Une suite du type « A B C A B D » peut alors être reconnue sans connaître une seule valeur. Pour obtenir une prédiction vérifiable, il faut que la suite du français réemploie un mot de l’amorce. Un mot nouveau ne donne aucune forme Voynich attendue. On garde tous les rapprochements proposés par le corpus. [Protocole](PROTOCOLE.md) · [Règles de comparaison](mots.py)

Le corpus de comparaison réunit les cinq pages du *Régime du corps* d’Aldebrandin de Sienne consacrées à l’exercice et au bain dans l’édition de 1911. L’algorithme obtient **884 mots pour le bain et 610 pour l’exercice** après effacement des accents et découpe aux apostrophes. Le compte éditorial, qui garde les apostrophes internes, est respectivement de 854 et 591. La restitution d'une lacune d’après un second manuscrit est isolée, et les fenêtres ne la franchissent pas. [Corpus](CORPUS.json) · [Sources et transcription des deux chapitres](TRANSCRIPTION.md)

## L’épreuve principale et le dessin de f75r

Dans les **721 loci** de prose P0 du cahier 13, les départs sont placés aux rangs 1, 9, 17, etc., dès que six groupes peuvent être examinés. Sur **670 départs**, **305** donnent la même amorce de six groupes dans les deux translittérations et les deux conventions de petits espaces. **4** de ces amorces contiennent deux types distincts de groupes répétés, le seuil principal. **2** amorces supplémentaires satisfont le seuil assoupli. Une seule des quatre amorces principales, celle de **f75r.26**, admet des rapprochements, quatre avec le bain et un avec l’exercice. Aucune des deux amorces supplémentaires n’en admet. [Prédictions par emplacement](PREDICTIONS.json.gz) · [Contrôle des deux positions suivantes](CONTROLE.json.gz)

À f75r.26, les six groupes sont `dain ol sheol dain ol qoly`. Deux des quatre rapprochements avec le bain attendent `dain`, l’un au rang 7, l’autre au rang 8. Les deux autres rapprochements du bain et celui de l’exercice ne prédisent aucune des deux positions. Dans les quatre lectures strictes, le dessin interrompt la fenêtre avant les cibles. **Le résultat principal est une abstention, avec zéro position testable.** En contrôle supplémentaire, on a autorisé la reprise du texte après la grande surface verte. La photographie montre à droite des formes lues `dar ady` ou `dar ajy`, avec une coupure incertaine. Aucune des deux ne reproduit le `dain` visible deux fois à gauche. Si l’on fusionne les deux formes comme chez Friedman, le groupe fusionné diffère également et il n’y a pas de huitième groupe. [Règle du contrôle supplémentaire](COMPLEMENT.md) · [Planche des deux côtés du dessin](f75r/planche.jpg) · [Collation du f. 75r](f75r/RAPPORT.md)

## Recherche rétrospective à tous les départs

La recherche dans toutes les positions, avec des amorces plus longues et potentiellement chevauchantes, a donné les résultats suivants. Les colonnes « bains » et « exercice » donnent le nombre d’emplacements admettant au moins un début compatible, suivi du nombre total de rapprochements. Permettre de franchir un seul blanc de dessin après l’amorce ne change aucun de ces décomptes. Les comparaisons automatiques exigeaient toujours le même découpage des cibles dans les quatre lectures. [Résultats détaillés](COMPLEMENTS.json.gz)

| Longueur de l’amorce | Emplacements ayant deux types répétés | Bains, emplacements / rapprochements | Exercice, emplacements / rapprochements |
| --- | ---: | ---: | ---: |
| 6 | 10 | 1 / 4 | 1 / 1 |
| 8 | 17 | 2 / 5 | 1 / 1 |
| 10 | 11 | 1 / 2 | 1 / 1 |

À **f84r.32**, les rangs 1–10 s’accordent avec deux passages successifs de la même liste des eaux (départs aux rangs 39 et 49 du paragraphe). « Sont gissees autres ki ont nature de fer autres ki » fait attendre « ont nature », soit `olkedy qotedy` d’après les équivalences ajustées sur ces dix mots. « Sont ameres autres ki ont nature de salnitre autres ki » fait attendre « sont », soit `qotar`, puis un groupe dont la forme est inconnue. Une fenêtre du chapitre de l’exercice partage aussi cette structure de dix mots. Les correspondances de huit et dix groupes au sein d’une même ligne et d’une même énumération ne constituent pas des répétitions indépendantes de l’expérience. [Suites déposées avant la vérification visuelle](F84R-PREDICTION.md) · [Deux dictionnaires et leurs prédictions](F84R.json)

Après le dixième groupe `dar`, les transcripteurs lisent **`or oly`**, Zandbergen signalant un espace incertain. La lecture fusionnée `oroly` échoue elle aussi. Il n’y a aucun dessin ou changement de paragraphe à cette position. **Zéro des deux rapprochements français prédit la suite immédiate.** Sur les 16 autres faces de bifeuillets retenues dans le cahier 13, chacun des deux dictionnaires couvre 112 occurrences de groupes isolés et 4 occurrences de paires adjacentes. Dans les autres cahiers, il couvre 317 occurrences isolées et 3 paires adjacentes. Les deux dictionnaires couvrent les mêmes emplacements. On ne les additionne pas. **Aucun triplet entier n’y est lisible** sous ces dictionnaires. La possibilité de vérifier un nouvel enchaînement de trois mots français reste donc nulle. [Photographie et lectures de f84r](f84r/RAPPORT.md) · [Vérification sur les autres bifeuillets et cahiers](F84R.json)

## Ce que montrent les contrôles

**Deux copies d’un ouvrage qu’on sait lire.** Dans le manuscrit Sloane 2435, copié vers 1265–1270 selon la British Library, deux cuves figurent dans la grande initiale du f. 8v. Avant d’ouvrir la suite, nous avons prédit d’après l’édition le mot du corps immédiatement avant le verbe « laver », puis une forme réfléchie avant « nettoyer ». Au f. 9r, *son cors laver et soi natoier des ordures* confirme l’ordre des gestes et leurs compléments. En regard, l’édition imprime *sen cors laver et soi netiier de l’ordure*. Une relation textuelle authentique peut conserver une instruction et en modifier les formes écrites. [Prédiction](SLOANE-PREDICTION.md) · [Détail du parchemin](laver.jpg) · [Étude du témoin et notice de la bibliothèque](SLOANE.md)

**Texte chiffré par remplacement de mots entiers.** Nous remplaçons secrètement les mots français par des groupes arbitraires et tentons de retrouver les deux cibles à partir de six groupes. Dans le premier contrôle, le texte source figure dans le corpus. Dans le second, les groupes encodent quatre passages de Sloane (209 mots normalisés), et les rapprochements proviennent toujours du chapitre imprimé. Le tableau compte séparément les fenêtres qui ont une proposition et les positions où les propositions renseignées s’accordent sur un seul groupe. Une « compatibilité intégrale » porte sur la configuration des huit mots et au moins une prévision formulée. Elle ne rend pas lisibles les mots nouveaux. [Transcription de Sloane](SLOANE.json) · [Résultats et exemples des contrôles chiffrés](COMPLEMENTS.json.gz)

| Texte encodé | Fenêtres admissibles | Avec au moins une proposition | Avec compatibilité intégrale et prévision | Positions de consensus correctes / prédites |
| --- | ---: | ---: | ---: | ---: |
| Le chapitre imprimé du bain | 15 | 14 | 6 | **6 / 22** |
| Quatre passages de Sloane | 8 | 8 | 2 | **2 / 14** |

Parmi les deux fenêtres de Sloane compatibles jusqu’au bout, une retrouve le passage des étuves, des cuves et de l’eau. Dans la copie, on lit *en estuve et en cuve et en iaue*. L’édition porte *en estuves et en cuves et en ewe*. L’autre fenêtre associe une mention d’eaux douces à une partie de l’énumération qui parle d’eaux salées et amères. Les mots répétés gardent le même ordre dans les deux fenêtres, mais seule la première retrouve le même passage. [Détail des fenêtres et de leurs lectures](COMPLEMENTS.json.gz)

L’altération d’une cible initialement prédite correctement élimine l’alignement correspondant dans chacun des **4 cas sur le texte imprimé** et des **2 cas sur Sloane** où cette altération a pu être testée. Un autre rapprochement incorrect peut néanmoins survivre à la corruption dans 3 des 14 fenêtres ayant une proposition pour l’édition et 1 des 8 pour Sloane. Les fenêtres se chevauchent, notamment dans l’énumération des eaux. Ces petits effectifs décrivent l’essai réalisé. [Calcul de calibration](eprouver.py) · [Comptes complets](COMPLEMENTS.json.gz)

**Mots mélangés.** Parmi 499 redistributions des mots à l’intérieur des passages du bain, 320 ne produisent aucune amorce alignable aux quatre emplacements principaux, 163 en produisent une et 16 en produisent deux. Seules **2 sur 499** produisent une position simultanément prédite par consensus et lisible selon le protocole, et aucune des deux prédictions ne réussit. Le texte authentique a lui aussi zéro position testable au contrôle strict. Cette expérience ne donne donc pas de seuil statistique exploitable pour la rencontre de f84r. Le contrôle qui aurait redistribué les seules fins de phrases entre amorces identiques exige plusieurs suites évaluables. Ce dénominateur manque ici. [Règle et graine fixées](COMPLEMENT.md) · [Distributions des trois comptes](COMPLEMENTS.json.gz)

## Reproduire les résultats

Depuis ce dossier dans la copie complète du dépôt, exécuter les commandes ci-dessous. La première enregistre les prédictions avant que la deuxième ne vérifie les cibles. Les deux dernières reproduisent les contrôles et l’essai de transfert. Les quatre résultats conservés ont été recalculés et confrontés aux fichiers publiés. [Lecture des mots et épreuve principale](mots.py) · [Contrôles et permutations](eprouver.py) · [Transfert des deux dictionnaires](transfert.py)

```sh
python3 mots.py predire
python3 mots.py verifier
python3 eprouver.py
python3 transfert.py
```
