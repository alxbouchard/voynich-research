# `arol` permet-il de lire « fourchu » ?

**La seule nouvelle graphie de trois signes prédite est `aro`.** Elle provient d’une hypothèse anglo-normande dans laquelle `arol` représenterait *furche*, « fourche », et `aro` la variante *furc*. Certaines clés prédisent à sa place `ar`, qui ne compte que deux signes. Aucune des trois formes `arol`, `aro` et `ar` n’apparaît comme mot entier dans les **98 mots de 94 légendes de fragments végétaux intégralement concordantes sur d’autres feuillets**. Quarante-neuf autres légendes sur les 143 restent incertaines. Le tri des illustrations fourchues est réalisé à part avec les lecteurs de l’étude. Toute légende lisible de cette réserve conduit donc au même verdict pour les lectures testées. [Annonce préalable](PREDICTIONS.json) · [Vérification](VERIFICATION.json)

### Ce qu’écrivaient les auteurs

- **Latin.** Chez Pline, *lacertis bifida et pilosa* qualifie la langue du lézard. Cet emploi antique atteste le féminin *bifida*. Dans le traité botanique de Lonitzer, paru en **1551**, l’imprimé montre *bifidi* au sujet des pousses de *Lithospermum*, et *bifido* dans la description de la coque de la noix. Les deux formes ont été contrôlées sur les photographies de l’imprimé. Ce témoin botanique est postérieur au Voynich. Aucun de ces trois passages ne nomme la racine de f99v. [Pline, livre XI](https://penelope.uchicago.edu/Thayer/L/Roman/Texts/Pliny_the_Elder/11%2A.html) · [Lonitzer, fol. 223r](https://mateo.uni-mannheim.de/camenaref/lonitzer/loni1/jpg/s223a.html) · [Fol. 29v](https://mateo.uni-mannheim.de/camenaref/lonitzer/loni1/jpg/s029b.html)
- **Anglo-normand.** Une citation du XIIe siècle conservée dans un manuscrit du début du XIIIe donne *el furc d’un arbre*, la fourche d’un arbre. Dans une autre, *une furche de fer* désigne un outil. La graphie *furches* est également attestée. Ce sont des noms, et les deux emplois diffèrent. [Citations médiévales, Anglo-Norman Dictionary, sens 1 et 6](https://www.anglo-norman.net/entry/furche)
- **Moyen anglais.** Dans le prologue des *Contes de Canterbury*, Chaucer décrit le marchand avec *a forked berd*, « une barbe fourchue ». Le qualificatif est attesté à la fin du XIVe siècle. L’exemple ne porte pas sur une plante. [Chaucer, prologue, vers 270](https://chaucer.fas.harvard.edu/pages/general-prologue-0)

### Ce que les quatre signes permettent de prédire

Les signes `a r o l` reçoivent chacun une ou deux lettres stables, avec des valeurs distinctes et sans signe muet. Aucune autre lettre n’est ajoutée pour lire la réserve. Les 19 tables sont compatibles avec les seules quatre équivalences proposées, prises séparément. Le lecteur ne peut en choisir une d’après le seul dessin. [Règles et limites de l’essai](PROTOCOLE.md)

| Lecture supposée de `arol` | Tables | Autres formes historiques demandées | Graphies EVA annoncées |
|---|---:|---|---|
| *bifida* | 6 | *bifidi*, *bifido* | Aucune |
| *furche* | 6 | *furc*, *furches* | `ar` ou `aro` pour *furc* |
| *furc* | 1 | *furche*, *furches* | Aucune |
| *forked* | 6 | Les mots voisins *a* et *berd* | Aucune |

Par exemple, si les quatre signes valent `fu · r · c · he`, la graphie de *furc* devient `aro`. Avec `fu · rc · h · e`, le même mot devient `ar`. À longueur égale, une seule position de la réserve porte un mot de trois unités, `shol`, et une seule en porte un de deux, `dy`. On compte 23 positions à quatre unités, soit la longueur de `arol`. Les blancs incertains et la nécessité d’un accord complet entre transcriptions limitent la couverture. L’absence des formes du modèle autorise à écarter leur répétition systématique dans les légendes lisibles ; elle laisse ouvertes d’autres graphies ou l’emploi de noms propres. [Effectifs par longueur et par lieu](VERIFICATION.json)

**Les mots de prose autour de `arol` n’ont pas produit de seconde lecture.** Le groupe avait déjà été signalé en f40v.18, f106r.16 et f113v.45. Dans la première, le groupe immédiatement antérieur est `okair`. Cet ajout ne permet de lire aucun des quatre vrais couples de mots historiques avec une table commune. Le groupe suivant, `qokey`, est séparé de l’ancre par une interruption du texte, d’où l’abstention. Les deux autres passages donnent `aiin arol ocheedy` et `polaiin arol shear`. Aucun mot de ces passages ne valide une annonce de voisin chiffré, car aucune graphie des voisins historiques n’était encodable. La présence déjà connue de `arol` dans ces lignes ne distingue pas les langues. [Essai antérieur sur les deux cressons](../../2026-11-18-du-dessin-au-paragraphe/cressons/RAPPORT.md)

**Contrôle positif.** Sous une substitution secrète par lettre, la seule ancre latine *bifida* donne exactement le code de *bifidi* dans la citation de Lonitzer. Le *o* de *bifido* reste inconnu. Sous un autre code expérimental à quatre signes, le modèle retrouve le code anglo-normand correct de *furc* parmi deux candidats. Ces contrôles portent sur deux textes connus, dont l’un a précisément servi à sélectionner la forme grammaticale ; ils vérifient le calcul. [Programme](tester.py)

Pour reproduire, exécuter `python3 -B tester.py annoncer` puis `python3 -B tester.py verifier` depuis ce dossier. La SHA-256 des annonces est `86206f2d6bc51e8f8db6ba99d9b01128115ff1f57184be625b3eb15b679b9cbd`. Après le dépouillement des images, `python3 -B tester.py lieux fXXr.N …` classe une liste de lieux publiés par les lecteurs. Une légende incertaine reste indécidable. Les comptages séparés des objets annotés sont repris dans le rapport général.
