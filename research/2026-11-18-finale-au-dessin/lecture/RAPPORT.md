# Peut-on lire le même mot avec et sans le signe final ?

Dans les 130 légendes végétales concordantes d’un seul groupe (124 graphies distinctes), seule la paire `otal` et `otaly` répond au critère fixé. `otal` se trouve en f99v.27 et `otaly` en f99v.6 et f88r.6. Les transcriptions montrent donc les deux formes sur un même feuillet. Leur voisinage avec des fragments végétaux laisse ouverte la question de ce qu’elles nomment. [Inventaire par lieu](PREDICTIONS.json) · [Protocole enregistré avant le dépouillement](PROTOCOLE.md)

## Deux lectures mises à l’épreuve

**Lecture nahuatl de Jules Janick et Arthur Tucker.** La table imprimée en 2018 donne `ātlocâ` pour `otal`, puis `ātlocâi` ou `ātlocây` pour `otaly`. Le *Gran Diccionario Náhuatl* de l’UNAM renvoie zéro fiche pour chacune des trois graphies normalisées `atloca`, `atlocai`, `atlocay`, toutes dates confondues. Le même accès exact retrouve 13 entrées du XVIe siècle pour *atl* et 10 pour *xochitl* (23 et 19 toutes dates). La chaîne témoin inventée donne zéro. Cette recherche porte sur les graphies entières indexées. Un mot fléchi, une variante orthographique ou un nom local peut manquer à l’index. [Table de 2018, p. 141](https://doi.org/10.1007/978-3-319-77294-3_5) · [Relevé signe par signe](../../2026-11-18-deux-legendes-botaniques/histoire/table.json) · [Réponses des 37 requêtes, dates et numéros de fiches](gdn.json)

**Abréviation latine expérimentale du projet.** Les six clés élaborées sur des passages antérieurs donnent `us` au signe final. Toutes laissent indéterminé le `t` de `otal`. Nous avons fixé une extension après la sélection de la paire et avant le dépouillement du lexique. Chacune des six clés pouvait attribuer à `t` une ou deux lettres quelconques, en conservant ses autres valeurs. Dans les 77 notices du *Macer floridus*, aucune extension ne produit même la forme courte comme mot entier. Le poème contient pourtant 16 paires de mots W et W+us, dont *ei* et *eius*, ainsi que 24 occurrences de *radix* et 33 de *foliis* sur 13 967 mots. Deux mots attestés avec les bonnes lettres peuvent appartenir à des lemmes différents, comme *sol* « soleil » et *solus* « seul ». Un autre essai du projet, `otaly` = *radix*, avait rencontré cette difficulté avec *radi* et *radix*. [Extension fixée avant consultation](VALEUR-MANQUANTE.md) · [Six clés d’origine](../../2026-11-18-racine-et-possessif/cle/RESULTATS.md) · [Texte de référence](../../2026-11-18-opcheor-paralleles/latin/SOURCE.md) · [Essai *radix*](../../2026-11-18-legendes-repetitions/lecture/radix/RAPPORT.md)

## Prédictions sur d’autres illustrations

La première catégorie réservée (48 légendes d’étoiles) ne comportait aucune paire admissible. La suivante (171 légendes zodiacales) en comportait cinq, toujours en excluant tout mot déjà présent parmi les 130 légendes végétales. Voici toutes les lectures directes de Janick et Tucker, après retrait des diacritiques. Deux possibilités dans une cellule correspondent aux deux choix constants `y` = *i* ou `y` = *y*. Les valeurs alternatives des autres signes du tableau n’ajoutent aucune sortie sur ces cinq paires.

| Signes courts et longs | Avec `y` lu *i* | Avec `y` lu *y* |
|---|---|---|
| `okal` et `okaly` | atloca, atlocai | atloca, atlocay |
| `okeeol` et `okeeoly` | atlaaaca, atlaaacai | atlaaaca, atlaaacay |
| `okyd` et `okydy` | atlich, atlichi | atlych, atlychy |
| `oteod` et `oteody` | atlaach, atlaachi | atlaach, atlaachy |
| `yteod` et `yteody` | itlaach, itlaachi | ytlaach, ytlaachy |

Le dictionnaire donne zéro fiche pour les 17 graphies directes distinctes et les 17 graphies distinctes obtenues en inversant l’ordre des signes. Ces résultats incluent le test végétal. L’inversion aboutit au même bilan, sans permettre de choisir le sens d’écriture. `okal/okaly` et `otal/otaly` ont exactement les mêmes sorties, car les auteurs lisent `k` et `t` de la même façon. Cette répétition apporte une nouvelle observation manuscrite et aucune vérification lexicale indépendante. Dans les six clés latines d’origine, il manque au moins un signe pour chacune des cinq paires réservées. [Relevé par lieu et par clé](PREDICTIONS.json) · [Résultats et témoins](resultats.json)

Nous n’obtenons aucune lecture lexicale pour la paire végétale ou pour une autre paire à l’aide de ces tables fixes. La valeur du signe final et le sens de ces légendes restent ouverts. L’inventaire ne couvre que les légendes simples retenues par l’accord des transcriptions dans le projet. Il ne permet pas de décider si les passages en prose décrivent les parties des plantes.

Depuis ce répertoire, `python3 -B paires.py` reproduit les prédictions et les résultats à partir des réponses archivées. Pour renouveler la consultation de l’index en ligne, exécuter `python3 -B interroger_gdn.py`, puis `python3 -B paires.py`. [Calcul](paires.py) · [Collecte de l’index](interroger_gdn.py)
