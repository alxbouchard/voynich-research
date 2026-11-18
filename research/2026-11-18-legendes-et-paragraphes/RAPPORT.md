# Un mot répété entre une plante et la prose peut-il servir à lire la phrase ?

**Sur f89r2, on peut ajuster quatre mots d’un herbier français du XVe siècle aux signes du Voynich. La lecture échoue au cinquième mot.** Le mot en réserve est particulièrement instructif. On peut le repérer en deux endroits du texte du feuillet 89, et au verso il constitue à lui seul la légende d’un fragment végétal. Ces emplacements donnent une prise sur la lecture de la page même si son sens reste inconnu. [Photographies des trois inscriptions](sheol/trois-inscriptions.png) · [Essai des quatre mots et du mot réservé](lecture/LECTURE.md)

## Une phrase d’herbier mise à l’épreuve

Le *Livre des simples médecines*, manuscrit français conservé à la Wellcome Collection et daté vers 1470, explique pourquoi l’aristoloche est dite longue. Sur le Voynich, la longue racine du fragment 36 et un rapprochement proposé par Ethel Voynich faisaient de cette notice une candidate. Dans sa légende on lit `opcheor`. Dans le paragraphe de f89r2.22, les positions 5 et 6 donnent `opcheor opcheol` dans les deux éditions principales. Une lecture ancienne hésite sur un signe au cinquième groupe. On peut donc tenter de lire la phrase entière, en essayant les variantes. [Photographie et texte de l’herbier français](lecture/wellcome-ouverture.jpg) · [Notice de la Wellcome Collection](https://wellcomecollection.org/works/s3rkhn4x) · [Ligne du Voynich](lecture/f89r2-22-groupes.png)

Avec zéro ou un signe muet, aucune table ne produit les couples *racine longue* ou *aristologie longue* sur la graphie principale. En remontant la ligne et en autorisant au moins quatre signes distincts à ne rien écrire, on peut produire **« aristologie longue est ainsi »** sur quatre groupes. La suite de la phrase médiévale donne une prédiction exacte, **« appellee »**. Les 183 tables distinctes qui ont permis de lire les quatre premiers mots connaissent déjà tous les signes du cinquième, `sheol`. Dans les 189 combinaisons de table et de convention, on obtient seulement `aristologiest`, `aristologieest` et `estaristologie`. Aucune ne donne le mot du témoin. Les autres transcriptions anciennes testables échouent aussi. Le rapprochement des quatre mots ne permet donc pas de lire cette phrase du manuscrit. L’incipit français était déjà connu lorsque les groupes de signes ont été répartis entre ajustement et vérification. [Règle du transfert enregistrée avant calcul](lecture/TRANSFERT.md) · [Tables, contrôles et différentes lectures de la ligne](lecture/LECTURE.md)

## Prédire une page avec toutes ses légendes

Les éditions de Takahashi et de Zandbergen–Landini distinguent les légendes de fragments végétaux (`Lf`) des lignes en paragraphe (`P0`). Les 15 panneaux qui portent les deux appartiennent aux cahiers 15 et 19. Six feuillets matériels les portent, en comptant séparément les panneaux des dépliants. La transcription contient aussi une face à texte sans légende de fragment, f101r. Une ligne centrée étiquetée `Pc` sur f101v reste hors du terrain de prose P0. Le texte fantôme f89v2.26, indiqué comme absent dans IT et omis dans ZL, a été exclu en amont. [Disposition du cahier 15](https://www.voynich.nu/q15/) · [Disposition du cahier 19](https://www.voynich.nu/q19/) · [Transcriptions sources](https://www.voynich.nu/transcr.html)

À partir de chaque paquet de légendes, on classe tous les textes concurrents du même cahier par nombre de mots distincts partagés. Une destination annoncée doit avoir au moins un mot en commun et dépasser toutes les autres. Un mot compte quand les deux éditions le retrouvent entier au même locus, avec les espaces incertains aussi bien joints que séparés. La recherche inclut toutes les lignes du panneau, quelle que soit leur distance à la figure. C’est un autre test que celui des [paires de dessins adjacents](../2026-11-18-formes-souterraines/nom/espace/RESULTAT.md). Les règles ont été enregistrées avant le calcul. [Protocole](PROTOCOLE.md)

| Résultat | Voynich, hors du panneau connu f89r2 | Livre de cuisine de Bolzano, 1461–1465 |
|---|---:|---:|
| Faces ou panneaux interrogés | 14, soit 178 légendes et 199 lignes de prose | 60, soit 168 rubriques et 8 379 positions de prose |
| Bonne destination seule | **0 sur 14** | **21 sur 60** avec tous les mots des rubriques, **15 sur 60** avec les seuls noms d’ingrédients retenus |
| Bonne destination après égalisation de la longueur des textes dans le bloc | 0 sur 14 | 18 sur 60 avec les rubriques |
| Rang moyen des bonnes destinations, 0,5 attendu par permutation | 0,482 | 0,806 avec les rubriques et 0,726 avec les ingrédients |

Le classement du Voynich donne une **fausse destination unique dans quatre cas**, une égalité positive dans six et aucun mot commun avec aucune destination dans quatre. Cinq des 14 paquets ont pourtant au moins un mot dans leur propre texte. Parmi les 43 545 600 attributions possibles au sein des deux cahiers, 26 691 392 font au moins aussi bien que la véritable disposition, soit 61,30 %. Si l’on permute seulement les panneaux d’un même feuillet, cette proportion vaut 768/1 152. À longueur de prose égale (113 positions au cahier 15 et 76 au cahier 19), les bonnes destinations ont un rang moyen de 0,442. Les quatre lectures prises séparément et l’ajout du texte sans étiquette f101r ne fournissent aucune bonne destination unique. Aucune suppression de mot d’une prédiction réussie ne s’applique. Les permutations sont des comparaisons internes à ce petit ensemble de six feuillets. [Toutes les destinations, variantes et permutations](RESULTATS.json) · [Chaque forme lisible et ses emplacements](OCCURRENCES.json)

Deux vérifications ajoutées après ce calcul traitent la dépendance matérielle et la ligne centrée de f101v. Retirer tout le feuillet 89, verso compris, laisse onze panneaux. Aucun ne retrouve seul sa page, et le rang moyen tombe à 0,420. Réintégrer la ligne centrée de f101v aux quatorze panneaux conserve le score de 0,482. [Deux calculs complémentaires](RESULTATS.json)

Au f99r, par exemple, `okor` et `okeoly` reparaissent dans la prose du panneau. Mais les textes de f102r2 reprennent **trois** formes des légendes de f99r, `choky`, `okor` et `oky`. Sur la page qui avait motivé l’expérience, les légendes de f89r2 partagent deux formes avec sa prose, `opcheor` et `cheody`. Trois formes se retrouvent avec f89v1, qui emporte le classement. [Positions de tous ces mots](OCCURRENCES.json)

Dans le témoin culinaire, deux noms de poissons, les sardines et les harengs, sont écrits en marge au f. 188r. Les mots des poissons se trouvent aussi au verso. Le terme de préparation `pastillo`, qui désigne un pâté, distingue le recto. Le test emploie les titres numérotés de l’édition savante pour les 168 recettes et contrôle leur présence matérielle sur ce seul feuillet. Ces rubriques expliquent pourquoi des mots d’objets et de préparations sont des candidats distincts pour le Voynich. L’exemple ne permet pas de décider que ce dernier serait un livre de recettes. [Photographie au Vatican, index de travail et essais de contrôle](temoin/RESULTAT.md)

## La disposition du texte sur le feuillet 89

- **Au recto**, deux répétitions se croisent. `opcheor`, près du quatrième fragment de la première rangée, revient dans le paragraphe sous la troisième. `cheody` fait le trajet opposé. Dans le reste du manuscrit, le premier est exceptionnel, tandis que la forme `cheody` compte 75 à 77 occurrences en prose P0 au total selon l’édition. Sur les trois autres panneaux où deux paragraphes géométriquement assignables permettent la vérification, aucun des 25 couples « rangée et mot » de la lecture principale ne revient dans la prose de sa page. [Matrice interne et huit permutations](rangees/RESULTAT.md)
- **Au verso**, `sheol` accompagne le fragment 53 et occupe la deuxième position du paragraphe sous sa rangée. Le même rang se rencontre sur f89r2.22. La prédiction d’une seconde place sur deux autres feuillets pharmaceutiques échoue : sur les 32 ouvertures retenues hors du feuillet 89, 24 offrent un deuxième mot lisible et aucune ne donne `sheol`. Deux autres occurrences à ce rang se trouvent dans le cahier final, à f103v.14 et f115v.8. La comparaison avec les autres rangs ne confirme pas de préférence pour la deuxième place. Dans une épreuve distincte à cinq dessins, les deux lecteurs IA ont préféré avec hésitation le fragment 51 au lieu du 53 prédit. [Légendes, photographies, rangs, lecture des dessins et limites](sheol/NOTE.md)

On peut désormais montrer dans l’encre un lien local entre la légende du fragment 53 et le texte juste en dessous. Le terme `sheol` a aussi servi à mettre en échec une proposition de déchiffrement qui produisait quatre mots de français médiéval. Il reste à identifier sa valeur et à lire un passage qui la confirme ailleurs.

## Reproduire les calculs

Depuis le dossier de ce rapport, exécuter les commandes suivantes avec Python 3. Les calculs textuels utilisent la bibliothèque standard. Le script des photographies utilise Pillow et les deux originaux indiqués dans sa note.

```sh
python3 -B comparer.py
python3 -B sheol/positions.py
python3 -B rangees/comparer.py
python3 -B temoin/verifier.py
python3 -B lecture/deux_mots.py
python3 -B lecture/voisinage.py
python3 -B lecture/transferer.py
```
