# Les sept étoiles de f68r3 peuvent-elles donner un premier nom lisible ?

Sur le dépliant f68r3 du Voynich, sept petites étoiles partagent une seule inscription, transcrite `doaro` ou `doary`. À gauche, une étoile isolée porte sa propre légende. Si le premier dessin reproduit les Pléiades avec une certaine fidélité, la position de quatre étoiles devrait permettre de prédire où le scribe a tracé les trois autres. **Aucune position prédite ne tombe à moins de 10,7 pixels d’une des trois marques réservées, la tolérance fixée.** Sur la gravure des Pléiades de Galilée, le même principe retrouve les deux étoiles réservées. [Détail du Voynich à Yale](https://collections.library.yale.edu/iiif/2/1006196/4840,1190,1440,920/full/0/default.jpg) · [Positions prédites et observées](geometrie/positions-predites.png)

## Que peut-on demander au dessin ?

Mary D’Imperio rapporte dès 1978 l’identification des sept étoiles aux Pléiades. En 2014, Marco Ponzi rapproche l’amas et l’étoile solitaire des troisième et quatrième mansions lunaires, les Pléiades et Aldébaran. Le feuillet ne numérote aucune mansion. L’inscription intermédiaire `oalcheol` longe une courbe qui relie l’amas au médaillon central. L’étiquette de l’étoile solitaire est distincte et comporte une terminaison transcrite `dal` ou `day`. Une autre interprétation publiée voit dans les sept étoiles les sept planètes. [Dessin et inscriptions, avec l’historique des propositions](voynich/LIEN.md)

Trois références ont été fixées avant le calcul. Ce sont les sept astres les plus brillants parmi les neuf noms usuels des Pléiades, le Grand Chariot et le Petit Chariot. Les positions célestes viennent du catalogue Hipparcos. Le programme reçoit quatre centres anonymes alternés d’après leur abscisse. Il peut tourner, déplacer, agrandir uniformément et retourner chaque forme. Il essaie 840 attributions dans chaque sens et choisit la figure la plus proche sur ces quatre points. Les trois positions prédites sont enregistrées avant le calcul des écarts. Pour réussir, l’écart quadratique moyen de calage doit rester sous 7,5 % du diamètre des quatre points, ou l’égaler. Chacun des trois centres réservés doit tomber à 10 % de ce diamètre au plus de sa prédiction. [Protocole](PROTOCOLE.md) · [Catalogue céleste](catalogue/SOURCES.md) · [Prédictions enregistrées](geometrie/PREDICTIONS.json)

## Quatre points permettent-ils d’en prédire d’autres ?

| Feuillet ou planche | Meilleur modèle sur quatre points | Écart quadratique sur ces quatre | Plus grand écart sur les positions réservées, seuil 10 % | Meilleur modèle après ajustement à tous les centres et écart quadratique |
|---|---|---:|---:|---|
| Voynich, f68r3 | Petit Chariot | 4,67 % | 149,53 % | Pléiades, 20,32 % sur sept. Identités inconnues |
| Grande Ourse de Samarcande, vers 1430–1440 | Grand Chariot | 2,53 % | 55,92 % | Grand Chariot, 2,81 % sur sept. Sept identités retrouvées |
| Grande Ourse de Bayer, 1603 | Pléiades | 3,22 % | 57,02 % | Grand Chariot, 3,51 % sur sept. Sept identités retrouvées |
| Pléiades de Galilée, 1610 | Pléiades | 6,54 % | 5,86 % | Pléiades, 5,78 % sur six. Six identités retrouvées |

Les deux colonnes de prédiction utilisent le diamètre des quatre points connus. La dernière colonne donne l’ajustement descriptif sur l’ensemble du dessin, rapporté au diamètre de tous ses centres. Le programme y essaie les 5 040 permutations des sept étoiles dans les deux sens, ou 720 permutations pour la gravure à six. Ce diagnostic a été ajouté une fois constaté que les quatre points de Bayer favorisaient une mauvaise carte. [Résultats sur f68r3 et Bayer](geometrie/RESULTATS.json) · [Ajustements à sept](geometrie/GLOBAL7.json) · [Calcul sur Samarcande](medieval/RESULTATS.json) · [Calcul sur Galilée](geometrie/GALILEE-RESULTATS.json)

- **Voynich.** En imposant les Pléiades, l’écart sur les quatre points tombe à 5,81 %. Après appariement un à un, les écarts atteignent 88,0, 75,3 et 69,2 pixels, sur un diamètre de calage de 107,2 pixels. La plus petite des neuf distances entre une position prédite et une marque réservée est de 29,6 pixels. Les sept « sœurs » mythologiques prises comme autre liste améliorent l’ajustement descriptif à 15,39 %, mais leur plus grande erreur en réserve atteint 98,63 %. Une troisième liste, qui fond Atlas et Pléioné en un seul point lumineux, donne 82,67 % en réserve. [Mesures du parchemin](voynich/f68r3-centres.json) · [Résultats par liste](geometrie/RESULTATS.json)
- **Samarcande.** Sur le f. 28r du *Livre des étoiles fixes* d’al-Ṣūfī, copié pour Ulugh Beg, la tradition du catalogue donne une identité aux sept disques du Chariot. Avec quatre centres, la méthode choisit le bon groupe et retrouve une seule des trois identités en réserve. Avec les sept, l’attribution optimale restitue précisément les sept noms documentés. La BnF date cette copie de vers 1430–1440. [Feuillet, relevé et datation](medieval/TEMOIN.md)
- **Bayer et Galilée.** Chez Bayer, si on fournit le vrai groupe, les quatre centres connus prédisent les trois autres dans la tolérance et avec les bonnes identités. Le choix automatique sur quatre préfère néanmoins les Pléiades. Galilée, lui, a distingué six étoiles brillantes et précise que la septième apparaît rarement. En comparant six points à six, les positions prévues pour Alcyone et Taygète tombent à 35,6 et 55,2 pixels de leurs centres, sous la limite de 94,2 pixels. Leurs identités viennent d’une comparaison astronomique publiée de l’ensemble de la gravure. [Planches, tables et identification des étoiles](etalons/SOURCES.md) · [Prédictions sur Galilée](geometrie/GALILEE-PREDICTIONS.json)

## Fréquence des ressemblances

Le test a été repris sur chacun des 35 choix possibles de quatre centres parmi sept. Sur le Voynich, le modèle sélectionné sur les quatre centres ne parvient, pour **aucun des 35 choix**, à prédire les trois autres centres dans les tolérances. Sur Bayer, huit choix sur 35 passent les seuils et 25 retrouvent les sept identités. Ces essais réemploient les mêmes points. Dans 1 000 répétitions où chaque coordonnée du parchemin varie de ±4 ou ±5 pixels selon son incertitude de lecture, le choix sur quatre change souvent et aucun essai ne réussit. [Partages des positions](geometrie/RESULTATS.json) · [Erreurs de pointage et simulations](geometrie/SENSIBILITE.json)

Avec sept points tirés uniformément au hasard, 1 761 dessins sur 2 000 dans un disque et 1 750 sur 2 000 dans un carré s’ajustent à l’une des trois cartes au moins aussi bien que le Voynich. Aucun des 4 000 n’égale Bayer sur ce critère. Aucun ne franchit non plus les seuils de la prédiction à trois positions. Ces fréquences décrivent les deux modes de tirage simulés. Un dessin conventionnel des Pléiades, une grappe décorative ou un autre sujet auraient pu suivre d’autres règles de disposition. [Simulations sur les sept positions](geometrie/GLOBAL7.json) · [Simulations en prédiction](geometrie/SENSIBILITE.json)

Les positions réservées ont été cachées au calcul d’ajustement. La photographie est publique et le responsable avait reçu les sept positions approximatives du Voynich avant l’enregistrement du protocole. Les relevés de l’image, du catalogue et des témoins ont été répartis entre agents IA. La réserve contrôle le calcul, sans constituer une observation indépendante d’un nouveau feuillet. Les attributions historiques des trois cartes témoins étaient connues. [Ordre des décisions](PROTOCOLE.md) · [Diagnostic ajouté après le choix sur Bayer](geometrie/DIAGNOSTIC.md)

## Le nom de l’amas et celui de l’étoile voisine

Sur une carte de Samarcande datée vers 1430–1440, un scribe a écrit **الثريا** (les Pléiades) près de quatre disques d’or sur le dos du Taureau et **الدبران** (Aldébaran) près de son œil. On peut donc vérifier sur la même figure que ces traditions donnaient un nom au groupe et un autre à l’étoile. Dans le manuscrit d’Oxford d’al-Ṣūfī, le passage correspondant énumère les quatre étoiles cataloguées, puis décrit deux ou trois étoiles supplémentaires à l’intérieur. Le nombre sept du Voynich reste compatible avec cette description. [Les deux inscriptions de Samarcande et le passage d’Oxford](medieval/NOMS-ARABES.md)

La prédiction lexicale porte sur X.1 (l’amas) puis X.3 (l’étoile voisine). Un signe doit garder sa valeur d’un nom à l’autre. Il peut écrire une seule lettre, plusieurs lettres, ou, dans un essai séparé, être muet. Par exemple, dans la lecture directe de `doaro`, le deuxième signe est identique au dernier. Pour lui faire produire toute la fin du nom arabe **الثريا**, sa valeur devrait se terminer par un *alif*. Or les seuls *alif* de ce nom sont sa première et sa dernière lettre. Si chaque signe se prononce, le premier signe a déjà consommé l’initiale et il ne reste aucun *alif* intérieur pour le premier `o`. La forme alternative `doary` évite cette difficulté particulière. Elle a donc aussi été essayée.

| Noms cibles dans leur témoin | Étendue du test | Tables permettant de lire les deux étiquettes |
|---|---|---:|
| Arabe sur la figure, **الثريا** et **الدبران** | 196 configurations avec les deux articles écrits, dont 172 avec un signe muet | 0 |
| Arabe, variantes construites en enlevant l’article à l’un des noms ou aux deux | 588 configurations | 0 |
| Castillan alphonsin, *açoraya* et *addauaran*, et latin imprimé en 1507, *Athoraye* et *Aldebaran* | 96 configurations à valeurs non vides et 344 avec un signe muet | 0 |
| Autres noms ou gloses attestés dans ces mêmes textes castillan et latin | 912 configurations à valeurs non vides | 0 |

Pour les deux mots arabes tels qu’ils sont écrits sur la carte, 16 configurations permettent d’ajuster chaque mot pris isolément. Aucune ne permet de faire les deux lectures avec la même table. La calibration synthétique retrouve les lettres partagées des noms connus. Une lecture du Soleil et de la Lune par transfert aurait exigé une table commune à figer, aussi ce transfert reste-t-il sans résultat à mesurer. [Calcul arabe](lecture/arabe/LECTURE.md) · [Castillan et latin, y compris la proposition de Ponzi](lecture/LECTURE.md) · [Essai avec un signe muet](lecture/silence/LECTURE.md)

## Que peut-on lire aujourd’hui ?

Le dessin de f68r3 pourrait évoquer les Pléiades de manière conventionnelle. Ni les positions relatives ni la lecture conjointe des deux légendes avec ces règles ne permettent de traduire `doaro` ou `doary`. Les quatre transcriptions sont des lectures du même original. Les graphies et leurs variantes éclairent ce test précis, sans déterminer la langue du Voynich.

Une comparaison botanique précise pourquoi l’idée que le texte décrit les dessins mérite d’être poursuivie. À f89r2, deux transcriptions lisent `opcheor` auprès d’un fragment végétal et dans le paragraphe de la même page. Une ancienne lecture donne `opchear` dans ce paragraphe. Ce rapprochement fournit un endroit précis où chercher si le scribe reprend le nom d’une plante, d’une partie ou d’une préparation. Dans un herbier lisible de 1485, la même image d’éléphant ouvre un chapitre sur l’ivoire et un autre sur l’os brûlé. Une image peut donc rendre le sujet reconnaissable tout en laissant le mot précis à découvrir dans le texte. [Les deux inscriptions à f89r2](../2026-11-18-formes-souterraines/nom/second/NOTE.md) · [Les deux pages de l’herbier de 1485](../2026-11-18-mots-et-dessins/herbier_1485/BOIS_REEMPLOYES.md) · [Comparaison des légendes de racines, de plantes, d’étoiles et de figures](../2026-11-18-mots-des-images/RAPPORT.md)

## Reproduire les calculs

Depuis le répertoire de ce rapport, avec Python et NumPy, exécuter les commandes suivantes. Le tracé des positions utilise également Matplotlib. Les trois calculs de lecture n’utilisent que la bibliothèque standard de Python.

```sh
python3 catalogue/construire.py
python3 geometrie/preparer.py
python3 geometrie/prevoir.py
python3 geometrie/evaluer.py
python3 geometrie/global7.py
python3 geometrie/sensibilite.py
python3 geometrie/galilee.py predire
python3 geometrie/galilee.py evaluer
python3 geometrie/samarcande.py predire
python3 geometrie/samarcande.py evaluer
python3 geometrie/figure.py
python3 lecture/essai.py
python3 lecture/silence/verifier.py
python3 lecture/arabe/lire.py
```
