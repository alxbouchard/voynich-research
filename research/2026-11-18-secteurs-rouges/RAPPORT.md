# Peut-on lire douze mois ou douze signes dans les secteurs rouges de f67r2 ?

Sur ce feuillet, les douze rubriques rouges, les douze visages et leurs douze légendes se correspondent matériellement, secteur par secteur. Dans les deux transcriptions, aucune des trois tables d’écriture essayées ne permet de lire ces inscriptions comme une des listes latines testées, même en essayant tous les points de départ. La fonction des secteurs et la langue de la page restent ouvertes. [Photographie de Yale](https://collections.library.yale.edu/catalog/2002046?child_oid=1006194) · [Protocole déposé avant le calcul](PROTOCOLE.md)

## Ce qu’un livre du XVe siècle permet réellement de lire

Sur le feuillet 14v des *Très Riches Heures*, les cartouches qui accompagnent une figure féminine, un couple et une balance portent respectivement *Virgo*, *Gemini* et *Libra*. On peut ainsi vérifier sur un témoin lisible ce qu’un scribe a voulu nommer. Les douze cartouches et les douze noms de mois de l’anneau voisin ont été relevés sur l’image. Douze rubriques d’un livre d’heures de Bruges donnent une seconde série pour les mois. On a conservé deux lectures possibles des lettres de mars et de mai à Chantilly, ainsi que la graphie *Scorpius*. [Témoins photographiés et transcription](temoin/NOTICE.md) · [Vérification de la balance sur une autre roue](temoin/COUPLES-DESSIN-MOT.md)

## Ce qu’exigent les signes sur f67r2

Les douze noms sont disposés en cercle. On essaie les douze origines dans chacun des deux sens. À chaque emplacement, le nom peut occuper un ou plusieurs groupes écrits consécutifs et comporter d’autres groupes avant ou après. Une même table doit fonctionner partout. Le test porte sur les noms entiers et sur leurs trois premières lettres. Les listes imposent l’ordre, sans imposer une sonorité aux groupes EVA. Les deux modèles à longueur variable permettent même à des signes distincts de partager une valeur. [Calcul](tables.py) · [Listes historiques](sources/listes-historiques.json)

| Emplacements | Édition | Positions d’apprentissage exploitables sur 8 | Positions réservées exploitables sur 4 | Orientations retenues à l’apprentissage |
|---|---|---:|---:|---:|
| Douze rubriques rouges | Takahashi | 7 | 4 | 0 |
| Douze rubriques rouges | Zandbergen–Landini | 8 | 3 | 0 |
| Douze légendes intérieures | Takahashi | 8 | 4 | 0 |
| Douze légendes intérieures | Zandbergen–Landini | 8 | 4 | 0 |

Le calcul croise deux séries, deux éditions, deux découpages des signes, deux traitements des espaces incertains, huit listes avec leurs variantes, deux longueurs de nom et trois familles de tables. Cela donne 768 combinaisons, chacune examinée dans 24 orientations. Ces 18 432 essais se recouvrent, plusieurs listes ou découpages donnant exactement les mêmes contraintes. Les quatre positions réservées n’ont servi à éliminer aucune table. [Détail des essais et transcriptions exactes](manuscrit.json)

Un second programme a examiné chaque exclusion séparément. Pour 15 356 orientations, un seul secteur d’apprentissage suffit à produire une contradiction. Pour les 3 076 autres, deux secteurs sont nécessaires et suffisants. Par exemple, si on place le Bélier au secteur 10 en sens horaire chez Zandbergen–Landini, il faut lire *Cancer* au secteur 1 et *Aquarius* au secteur 8. Avec un signe pour une à trois lettres, la première inscription impose soit `k` pour *a*, soit `a` pour *c*. Dans la seconde, `k` doit donner *qu* et `a` doit donner *i*, *iu* ou *u*. Le conflit peut se vérifier avec ces deux seules inscriptions. [Tous les certificats](contrepreuve.json) · [Algorithme indépendant](contrepreuve.py)

**Sensibilité aux lectures.** On a ensuite autorisé le choix de l’édition et du type de blanc séparément à chaque emplacement, en omettant entièrement les deux rubriques rouges qui comportent un signe non résolu dans l’une des éditions. Les dix rubriques restantes et les douze légendes intérieures échouent encore à l’apprentissage dans les trois familles. Une vérification plus restrictive retire ensuite tous les emplacements où les deux transcriptions diffèrent, ainsi que la rubrique 2, dont les blancs sont discutés sur photo. Il ne reste alors que trois rubriques (5, 8, 9) ou six légendes intérieures (1, 4, 5, 9, 10, 11). Sur ces petits sous-ensembles, certaines tables de lettres rendues par plusieurs signes deviennent compatibles avec des noms abrégés. Elles ne prédisent pas les autres secteurs. La solidité de l’exclusion dépend donc des graphies retenues. [Recalcul de sensibilité](variantes.json) · [Programme](variantes.py)

## Contrôle sur une clé inconnue

Une permutation a masqué les noms latins des mois, avec janvier à la place 5 et l’ordre inversé. À partir de huit positions, le solveur retrouve le seul départ et le seul sens compatibles. Sur les quatre noms cachés, la table apprise lit *martius*, *september*, *iunius* et *?ecember*. La lettre initiale de décembre manque dans les huit exemples d’apprentissage. Cela fait 29 lettres exactes sur 30. Dans l’essai avec des mots ajoutés et des noms coupés, les mêmes suites sont retrouvées parmi plusieurs délimitations possibles. L’ordre mélangé échoue. Les deux contrôles construits pour les tables à longueur variable admettent la vraie orientation et échouent avec la bijection seule. Cette calibration est artificielle. [Lectures gelées et réponses connues](etalonnage.json)

## Ce que confirment les photographies

Deux lecteurs IA séparés ont jugé chacun 14 cartes d’encre rouge et 12 secteurs anonymisés. Les sept inscriptions sombres isolées ont été retrouvées par les deux lecteurs aux mêmes sept endroits, puis rattachées aux secteurs 1, 3, 5, 6, 7, 8 et 11 après ouverture de la clé. Les lecteurs n’ont proposé aucune lecture EVA intégrale des rubriques rouges. Sur la carte de la rubrique 2, les deux préfèrent deux groupes, tandis que les deux éditions en donnent trois. Le premier juge les deux découpages plausibles. Une autre difficulté porte sur le petit groupe central du secteur 1. Les résultats du calcul portent donc sur des éditions explicites du texte. [Votes A](photos/vote-A.json) · [Votes B](photos/vote-B.json) · [Planches, témoins et alignements](photos/README.md)

Pour les sept inscriptions isolées, les signes d’exaltation des sept astres et les sept mois de 31 jours retrouvent chacun six emplacements sur sept au meilleur départ. En essayant les deux hypothèses et toutes les orientations sur les 792 façons de marquer sept cases parmi douze, 648 font au moins aussi bien. Aucun des deux modèles n’explique à lui seul le septième emplacement. [Sources du XVe siècle et inventaire](sources/inventaire-f67r2.md) · [Toutes les orientations ex æquo](sources/sept-resultats.json)

Les essais laissent ouvertes des descriptions, des rubriques comptant une formule ou des noms spécifiques différents, des abréviations médiévales et d’autres langues ou systèmes d’écriture. Attribuer une valeur à un signe demanderait qu’elle s’applique à d’autres inscriptions dont l’image contraint le sens.

## Reproduction

Depuis ce dossier avec Python 3, les commandes suivantes régénèrent le contrôle synthétique, le calcul sur les transcriptions du dépôt, les certificats et l’analyse secondaire.

```sh
python3 -B tables.py etalonnage
python3 -B tables.py manuscrit
python3 -B contrepreuve.py
python3 -B variantes.py
```

Les calculs sur les sept emplacements, les scripts de cadrage et les références de chaque témoin figurent dans leurs notices. [Géométrie des sept secteurs](sources/comparer_sept.py) · [Photographies du Voynich](photos/README.md) · [Manuscrits lisibles](temoin/NOTICE.md)
