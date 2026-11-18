# Quelle chance de rencontrer une paire dans le cahier 20 ?

Dans les deux transcriptions, le score observé est le même. Parmi les 128 paires possibles, une seule apparaît à huit positions ou moins dans un tronçon commun, une seule fois : `opchy`–`otol` sur f112v. En redistribuant les mots à l’intérieur de leur page et de leur catégorie de position sur la ligne, **au moins une des 128 paires apparaît dans 63,16 % des tirages en H et 36,88 % en ZL**. Pour la seule paire `opchy`–`otol`, les probabilités exactes sont de 9,18 % en H et 9,78 % en ZL. Ce contrôle a été choisi après l’observation de la rencontre.

## Résultats

Chaque case est la probabilité d’obtenir **au moins une** rencontre dans l’ensemble du cahier. La fenêtre autorise sept segments intercalés au maximum, dans n’importe quel ordre et à l’intérieur du même tronçon. Les pourcentages exacts proviennent d’une énumération indépendante. Les estimations de la famille par face reposent sur 49 999 tirages chacune. Leur erreur-type de Monte-Carlo vaut 0,22 point de pourcentage en H comme en ZL.

| Redistribution des mots | Paire fixée, H | Une quelconque des 128, H | Paire fixée, ZL | Une quelconque des 128, ZL |
| --- | ---: | ---: | ---: | ---: |
| Par face et catégorie de position de ligne | 9,18 % exact | 63,16 % (31 581/49 999) | 9,78 % exact | 36,88 % (18 438/49 999) |
| Par tronçon et catégorie de position de ligne | 45,00 % exact | 65,95 % exact | 47,43 % exact | 47,43 % exact |

Pour la paire fixée, seuls f106r, f106v et f112v contiennent les deux mots dans chaque édition. Chacune de ces faces a un exemplaire de chaque forme. Le calcul exact examine tous les placements possibles des deux occurrences dans leurs catégories observées et combine les trois probabilités indépendantes. Les simulations correspondantes donnent 4 648/49 999 en H et 4 886/49 999 en ZL pour la redistribution par face.

Quand la fréquence de chaque mot est conservée au sein de son tronçon, f112v.42–44 est la seule unité où la paire fixée peut réussir. Dans cette unité, 270 des 600 placements légaux réussissent en H et 240 des 506 en ZL. En étendant la recherche aux 128 paires, H autorise aussi `oror`–`otol` dans le tronçon commençant sur f113v.10, avec une probabilité de 8/21. Les deux événements indépendants portent la probabilité exacte de la famille H à 277/420. En ZL, aucune autre paire ne possède deux formes attestées dans un même tronçon.

## Construction

La table de départ est `conditions["accord/joint/strict"]` dans [predictions_pots_elargis.json](../../predictions_pots_elargis.json), avec la relecture de `otol` sur l’objet `f102v2.7` de la première rangée. Après recalcul des paires de cette rangée et suppression des doublons, la famille comporte 128 paires non ordonnées, pour 54 formes distinctes. Douze paires ont leurs deux membres présents sur au moins une même face en H, dix en ZL. Les données, les fréquences et les espaces sont ceux de chaque édition séparément. Les espaces incertains sont joints et toutes les positions sont comptées, y compris celles qui contiennent un mot de lecture incertaine.

Les 297 tronçons sont les intersections contiguës des paragraphes H et ZL calculées par `deux_feuilles.overlap`. Ils comportent 10 682 positions en H, dont 200 occupées par une des formes d’intérêt, et 10 082 en ZL, dont 183. Chaque ligne, sa longueur et les bornes des tronçons sont conservées pendant la redistribution. Une occurrence en début de ligne reste dans un emplacement initial de sa face, une occurrence intérieure dans un emplacement intérieur et une finale dans un emplacement final. Une ligne d’un seul mot possède sa propre catégorie. Dans la variante par tronçon, les occurrences restent également dans leur tronçon d’origine. Les associations entre mots et lignes individuelles peuvent changer à l’intérieur de ces contraintes.

Le mélange des positions se fait uniformément, sans remise, dans chaque catégorie. Les formes d’intérêt conservent leurs effectifs exacts dans chacune. On peut ignorer l’identité des autres mots une fois leurs positions réservées. Le score demande si une quelconque paire autorisée atteint le seuil et traite les nombreuses comparaisons dans le même tirage. La permutation des dessins (101/171), qui déplace les étiquettes entre rangées en conservant le texte tel quel, pose une autre question. Ces deux probabilités ne se combinent pas. Le contrôle par page ne préserve pas un éventuel sujet propre à chaque paragraphe. Le contrôle par tronçon fixe d’emblée la présence commune des formes qui s’y trouvent. Aucun des deux n’estime la probabilité que les mots désignent des ingrédients.

## Reproduction

Depuis ce dossier, exécuter `python3 melanger.py`, puis `python3 exacte.py`. Le premier script utilise NumPy avec PCG64 et des graines distinctes inscrites dans les résultats. Sur NumPy 2.4.6, deux exécutions intégrales ont produit le même fichier de résultats de simulation. Le second programme énumère les placements de la paire fixe et, pour le modèle par tronçon, de toute la famille. Il vérifie l’accord avec les simulations.

[Simulations et scores observés](resultats.json) · [Énumérations exactes par face](exacte.json) · [Programme de simulation](melanger.py) · [Programme d’énumération](exacte.py)
