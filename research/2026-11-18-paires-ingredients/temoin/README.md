# Deux ingrédients peuvent-ils identifier une recette médiévale ?

Dans le *Liber de coquina*, épinard et aneth permettent de retrouver le pâté de hareng ou de sardine parmi **168 préparations** d'une copie du XVe siècle. La graphie de l'épinard passe de `spinnarchia` à `spinarchia` entre les deux témoins. Deux autres paires illustrent l'ambiguïté des associations. Le couple pois chiche et poivre désigne trois préparations et le couple marjolaine et romarin en désigne quatre, y compris quand on impose l'ordre des mots.

## Témoins et vérification sur le feuillet

Francesca Cupelloni a préparé les deux éditions numériques pour AtLiTeG. Le texte A est celui du manuscrit Paris, BnF, latin 7131, daté de 1308–1314. Le texte O est celui du Vatican, Pal. lat. 1768, daté de **1461–1465**. Deux copies transmettent une même œuvre latine. La forte proximité de leurs recettes facilite le test. [Fiche et datation de A](https://corpus.atliteg.org/opera/liber-de-coquina-a/93) · [Fiche et datation de O](https://corpus.atliteg.org/opera/liber-de-coquina-o/92).

Le pâté figure en A au f. 98v et en O au f. 188r. La recette inclut l'épinard, l'aneth, des noisettes, des noix et du poivre. Sur l'image du Vatican, le passage contenant l'épinard et l'aneth se trouve au milieu du feuillet, entre deux grandes initiales rouges. Sous la deuxième, la préparation de poisson farci contient marjolaine et romarin, le second nom partagé entre deux lignes. Le fac-similé confirme la localisation et les expressions. Les transcriptions numériques développent des abréviations. La comparaison exacte ci-dessous porte sur les mots de l'édition. [Texte A, f. 98v](https://corpus.atliteg.org/testi/liber-de-coquina-a/93?p=98v) · [Texte O, f. 188r](https://corpus.atliteg.org/testi/liber-de-coquina-o/92?p=188r) · [Image du f. 188r, Bibliothèque vaticane](https://digi.vatlib.it/iiifimage/MSS_Pal.lat.1768/Pal.lat.1768_0393_fa_0188r.jp2/full/1200,/0/default.jpg).

## Choix des requêtes

Deux séries ont été choisies à titre exploratoire dans A, celle des pois chiches et celle des harengs ou sardines. L'étude conserve toutes leurs préparations contiguës, soit sept et quatre. Les deux premières plantes nommées dans chaque corps fournissent la requête. On compte les noms de fruits et d'épices, y compris dans un ingrédient composé. On écarte les termes collectifs et les produits dont la source végétale reste implicite, comme l'huile, le vin et le sucre. Ainsi le lait d'amandes apporte le nom de l'amande.

Les rubriques de O et la position dans les séries déterminent les onze correspondances attendues. Avant de lire les corps de O, le fichier [protocole.json](protocole.json) a fixé ces correspondances, les graphies exactes de A, les flexions, les variantes de graphie et l'équivalence entre *crocus* et *safranum*. Son empreinte SHA-256 est `214e99616e0de232079b54b9174a543e87b95cbabbca0d93ab5afff5c7ef4b8e`. L'essai porte sur les corps seuls de O. La page de l'œuvre annonce 192 entrées. Dans la page de texte intégral, 192 éléments de rubrique appartiennent aux groupes de recettes, dont 24 intitulés sans numéro et 168 rubriques numérotées de 1 à 168, chacune suivie d'un corps. Chaque requête est confrontée à ces 168 corps. [Texte intégral de A](https://corpus.atliteg.org/testi/liber-de-coquina-a/93) · [Texte intégral de O](https://corpus.atliteg.org/testi/liber-de-coquina-o/92).

## Résultats

Les 11 requêtes donnent 1 848 comparaisons par règle. Une « bonne cible seule » signifie que parmi les 168 préparations une seule satisfait la requête et qu'il s'agit de l'homologue attendu. La précision compte les cibles correctes parmi les réponses. Le rappel compte les cibles présentes parmi les onze attendues. Une même paire végétale peut correspondre à plusieurs demandes distinctes.

| Règle | Ordre imposé | Bonnes cibles / toutes les réponses | Bonnes cibles / 11 attendues | Bonnes cibles seules |
|---|---|---:|---:|---:|
| Formes exactes de A | Non ou oui | 7/20 (35 %) | 7/11 | 2 |
| Flexions prédéfinies | Non ou oui | 7/21 (33 %) | 7/11 | 2 |
| Flexions et graphies prédéfinies | Non | 8/23 (35 %) | 8/11 | 3 |
| Flexions et graphies prédéfinies | Oui | 8/22 (36 %) | 8/11 | 3 |
| Même règle, en réunissant les deux noms du safran | Non | 8/25 (32 %) | 8/11 | 2 |
| Même règle, en réunissant les deux noms du safran | Oui | 8/24 (33 %) | 8/11 | 2 |

L'ordre impose qu'une occurrence du premier mot précède une occurrence du second. Ils peuvent être séparés par d'autres mots. Le tableau suivant donne tous les candidats pour la règle « flexions et graphies prédéfinies », sans l'équivalence additionnelle du safran et sans ordre imposé.

| Numéro A | Numéro O attendu | Paire issue de A | Numéros O retrouvés |
|---:|---:|---|---|
| 21 | 25 | Pois chiche, châtaigne (condition) | **25**, 26 |
| 22 | 26 | Pois chiche, poivre | **26**, 27, 29 |
| 23 | 27 | Pois chiche, poivre | 26, **27**, 29 |
| 24 | 28 | Pois chiche, amande | **28** |
| 25 | 29 | Pois chiche, poivre | 26, 27, **29** |
| 26 | 30 | Pois chiche, safran | 26 |
| 27 | 31 | Pois chiche, safran (option) | 26 |
| 10 | 146 | Épinard, aneth | **146** |
| 11 | 147 | Marjolaine, romarin | 51, 53, **147**, 153 |
| 12 | 148 | Poivre, safran (*crocus*) | **148** |
| 13 | 149 | Deux agrumes (alternatives) | 69, 84, 142 |

Dans O, la cible 146 apparaît quand on autorise le *n* simple de `spinarchia`. La cible 148 figure seule avec poivre et *crocus* sous la règle de graphies, puis partage sa paire avec deux autres recettes quand on accepte l'autre nom du safran. Les deux fausses identifications « pois chiche et safran » s'expliquent par une variante absente des règles prédéfinies. O écrit `zafrano` et `zafranum` dans les cibles 30 et 31. Les retours vers la recette 26 illustrent qu'un candidat unique peut être erroné.

La dernière paire est coordonnée par le latin *vel*, « ou ». L'instruction permet deux jus de fruits différents. Les compter tous deux comme ingrédients nécessairement présents introduirait une erreur. De plus, le second agrume change de forme lexicale en O. La requête n'atteint pas sa cible. Si l'on écarte cette instruction alternative, les flexions et graphies donnent **8 bonnes cibles pour 20 réponses** sur dix requêtes, dont trois bonnes cibles seules, avec ou sans ordre. Les recettes 25 et 31 gardent leur qualification conditionnelle ou facultative.

Les sept préparations de pois chiches dépendent d'une même série et plusieurs requêtes reprennent le même couple. Les pourcentages décrivent ces deux séries. L'expérience mesure le repérage lexical d'homologues dans deux témoins apparentés, avec la langue et le sens des mots déjà connus. Elle fournit un exemple vérifié de spécificité et des concurrents mesurables pour d'autres paires.

## Reproduire les calculs

Le fichier [index_O.json](index_O.json) contient, pour chacun des 168 corps, la suite des seules formes détectables par les règles fixées, dans leur ordre initial. Il permet de rejouer le calcul avec la bibliothèque standard de Python 3.

```sh
python3 verifier.py --rejouer index_O.json --sortie /tmp/coquina-rejeu
```

Pour repartir des deux éditions institutionnelles, Python 3 et `beautifulsoup4` sont nécessaires. Les pages HTML incluent des éléments de présentation susceptibles d'évoluer.

```sh
curl -fsSL 'https://corpus.atliteg.org/testi/liber-de-coquina-a/93' -o /tmp/coquina-a.html
curl -fsSL 'https://corpus.atliteg.org/testi/liber-de-coquina-o/92' -o /tmp/coquina-o.html
python3 verifier.py /tmp/coquina-a.html /tmp/coquina-o.html --sortie /tmp/coquina-sources
```

La première exécution par lecture directe et le rejeu ont donné des fichiers identiques octet pour octet. [Appariements et liste de tous les candidats](appariements.tsv) · [Effectifs pour chaque règle, avec et sans l'alternative](totaux.tsv) · [Formes détectées dans O](formes.tsv) · [Programme](verifier.py).
