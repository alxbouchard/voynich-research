# « Baies » ou « feuilles » dans la prose des deux panneaux ?

À partir des grappes dessinées sur f17v et f96v et des rapprochements du catalogue avec deux fragments, nous avons prédit qu’une des deux graphies `ctheor` ou `ctheol` reparaîtrait sur f99r et f100r. **La prose des deux panneaux porte `ctheol`**, à f99r.29 et f100r.25. Dans les deux cas, c’est le cinquième mot d’une ligne de dix. Ce rang commun a été découvert en ouvrant les lignes. Les deux légendes directement voisines des fragments donnent d’autres groupes. La même graphie peut donc conduire d’un dessin au texte d’un autre panneau, sans que le lien entre le cinquième mot et le fruit représenté soit assuré. Dans le même cahier, six paires de panneaux sur 36 présentent l’une ou l’autre des deux graphies sur chaque panneau. [Photographies des deux panneaux, des inscriptions et des lignes](../fleurs/deux-panneaux.jpg) · [Prédiction et contrôles](../fleurs/RAPPORT.md)

## La lecture du sixième mot

Nous avons supposé que `ctheor` et `ctheol` représentent deux formes de *bacca*, « baie », avec une même table attribuant une ou deux lettres à chaque signe. Nous avons répété l’essai avec « racine », « feuille » et « fleur ». Les mots suivant chacune des formes latines dans Celse et dans le *Macer* fournissent les prédictions. Cinquante tables peuvent donner deux formes distinctes de « baie » attestées dans le corpus ; 88 conviennent si l’on autorise tout le paradigme défini, y compris *baca* avec un seul c. Aucun voisin latin principal n’était entièrement encodable avec les valeurs déjà apprises. [Règles avant l’ouverture des voisins](AVANT.md) · [Tables et mots latins annoncés](ANNONCES.json)

| Nom essayé | Tables sur les formes attestées | Voisin latin le plus fréquent | f99r.29, sixième mot `qokey` | f100r.25, sixième mot `olcheol` |
|---|---:|---|---|---|
| Baie, *bacca* | 50 | *aut* | Aucun voisin compatible | Aucun voisin compatible |
| Racine, *radix* | 68 | *ejus* | Aucun | Aucun |
| Feuille, *folium* | 24 | *ejus* | *violae*, en ajoutant trois valeurs | Aucun |
| Fleur, *flos* | 68 | *junci* | Aucun | Aucun |

Le tableau donne tous les voisins encore possibles du corpus, même en accordant aux nouveaux signes des valeurs nouvelles. Aucune table ne convient aux deux panneaux. Dans le fichier de résultats, la première position de `possible_par_lieu` correspond à f99r.29, la seconde à f100r.25. Le programme traite les deux cibles dans cet ordre ; le tri alphabétique des clés JSON affiche f100r avant f99r dans l’objet séparé `lieux`. [Mots observés et résultats](OUVERTURE.json) · [Ordre des cibles dans le programme](lire_baies.py)

**On peut suivre jusqu’au mot qui échoue la seule lecture encore possible.** Dans la notice de la violette du *Macer*, le poète écrit *foliis violae cum melle*, « avec les feuilles de violette et du miel » dans cette préparation. À f99r.29, une seule extension donne *foliis violae* pour `ctheol qokey` : elle ajoute `q` = *v*, `k` = *o* et `y` = *ae* aux valeurs déjà fixées. Le septième mot est `ckhol`. Sa fin comporte `o` = *i* et `l` = *is*, donc la sortie se termine obligatoirement par *iis*. Aucune valeur du premier signe `ckh` ne produit *cum*. C’est un contrôle rétrospectif sur la ligne déjà ouverte. [Notice latine de la violette](../../../2026-11-18-opcheor-paralleles/latin/vers.tsv) · [Ligne et variantes des deux éditions](OUVERTURE.json) · [Contrôle du troisième mot et table exacte](VIOLETTE.json)

## Les baies du laurier dans deux témoins du XVe siècle

La copie du *Macer* de 1478 donne *cum baccis lauri*, « avec des baies de laurier », dans la notice du **poivre**. L’édition employée pour le calcul écrit *cum lauri baccis*. Sur une image titrée *Laurus* de l’herbier de Mayence de 1485, les baies rondes restent difficiles à isoler, mais la prose donne bien « la graine ou le fruit ». L’organe employé dans la préparation et la plante nommée par la rubrique peuvent donc être différents. [Comparaison des deux témoins et des photographies](temoin/RAPPORT.md)

Sept tables donnent précisément *baccis* pour `ctheol`. Nous avons réessayé les deux ordres historiquement attestés. Sur f99r et f100r, déjà ouverts, aucun des deux voisins ne convient. Sur f88r.7, la prédiction *cum … lauri* a précédé l’ouverture des mots à gauche et à droite de `ctheol`. L’encre transcrite donne `dorsheoy ctheol qockhey`. Aucun des sept jeux de valeurs ne permet de lire les mots prévus, même d’un seul côté, dans l’ordre de la copie ou dans celui de l’édition. [Prédiction sur ce troisième lieu](COPIE-AVANT.md) · [Deux ordres testés aux trois lieux](COPIE.json)

Les deux lignes de départ ont respectivement quatre et trois **autres** mots finissant par les signes `e o l`. Nous avons prédit au moins deux autres finales de ce type sur f88r.7, où la même forme est deuxième. Parmi les sept mots lisibles sur huit, aucune autre ne se présente. Le mot incertain pourrait en apporter une au maximum. Parmi les 26 lignes témoins de même longueur, cinq en ont au moins deux de façon certaine. Le double succès de localisation reste acquis. Les traductions « baie », « racine », « feuille » et « fleur » proposées ici n’ont pas permis de lire les deux passages. [Contrôle annoncé des finales](FINALES-AVANT.md) · [Effectifs et incertitudes](FINALES.json)

Depuis ce dossier, reproduire les tests avec `python3 -B lire_baies.py annoncer celsus.xml`, puis `python3 -B lire_baies.py ouvrir celsus.xml`, `python3 -B copie.py` `python3 -B finales.py` et `python3 -B violette.py`. [Contrôle des deux leçons latines](copie.py) · [Comptage par ligne](finales.py)
