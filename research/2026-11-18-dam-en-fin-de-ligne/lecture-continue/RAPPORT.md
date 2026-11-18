# Peut-on lire deux ou trois mots consécutifs avec les tables de Celse ?

**Aucune des deux tables ne restitue une suite de deux mots attestée chez Scribonius Largus.** Après retrait des mots de départ, le manuscrit offre 65 paires adjacentes entièrement déchiffrables avec les six signes attribués. Quatre passages permettent d'aller jusqu'à trois mots. Aucune des 1 440 permutations distinctes des valeurs ne donne davantage de correspondances continues. La comparaison a donc peu de pouvoir pour départager ces tables. [Protocole antérieur au calcul](PROTOCOLE.md) · [Résultat complet et lieux de toutes les fenêtres](RESULTATS.json.gz)

À **f54r.7**, les deux transcriptions donnent `dam dam` à la droite d'une interruption du dessin. Les deux groupes se suivent dans le même tronçon. La seconde table les lit *tum tum*. Chacun des mots, pris isolément, est attesté chez Scribonius. La suite *tum tum* n'y apparaît pas. Le texte latin possède en revanche *tum cum*, au début d'une ligne de la préparation 95. La même table aurait exigé `dam sam`. C'est un exemple concret de la différence entre reconnaître deux formes latines et retrouver les mots successifs d'un texte. [Scribonius, préparation 95, édition Helmreich](https://archive.org/details/cuascriboniilarg00scri/page/n50/mode/1up)

## De quelles lectures disposait-on ?

| Groupe de départ | Valeurs de o, l, d, a, m, s, dans cet ordre | Meilleur résultat attesté selon la règle de départage | Occurrences isolées compatibles | Paires attestées / 65 | Triples attestés / 4 |
|---|---|---|---:|---:|---:|
| `oldam` → *ducenda* | d · uc · e · nd · a · i | `d` → *e*, f1r.13 | 20 (6 graphies EVA) | 0 | 0 |
| `oldam` → *ortum* | o · r · t · u · m · c | `dam` → *tum*, f1v.4 | 164 (6 graphies EVA) | 0 | 0 |

Le meilleur résultat atteint un seul mot. Ces attributions restent conditionnelles aux clés et ne constituent pas des traductions. Dans la première table, les six sorties isolées présentes dans le latin sont *e, id, dei, de, a, ea*. Dans la seconde, ce sont *tum, cur, cum, cor, tu, o*. Les mots courts se rencontrent aisément. La seconde table produit *tum* à 55 emplacements simplement parce que `dam` y est écrit 55 fois. [Clés originales, entrées de largeur deux à valeurs distinctes](../lecture/MODELES.json.gz) · [Positions individuelles](RESULTATS.json.gz)

Les quatre suites maximales observées sont entièrement données ici. Les espaces entre les mots sont obligatoires dans les deux langues.

| Lieu | Trois groupes EVA | Table *ducenda* | Table *ortum* |
|---|---|---|---|
| f23r.5 | `ol ol dol` | duc duc educ | or or tor |
| f24r.15 | `ol dal s` | duc enduc i | or tur c |
| f24r.16 | `dal dam dal` | enduc enda enduc | tur tum tur |
| f78r.37 | `osal ol s` | dinduc duc i | ocur or c |

## Corpus et contrôles

Les 3 884 lignes de prose P0 communes aux deux transcriptions ont donné 3 812 lignes avec les mêmes marques d'interruption dans H et ZL. Dans celles-ci, 25 775 positions conservent le même mot et le même statut de bord dans les quatre lectures. Parmi elles, 1 317 mots s'écrivent entièrement avec les six signes attribués. Les trois occurrences de l'ancre `oldam` sont retirées. Les deux autres ancres n'avaient aucune occurrence admissible en prose. Restent **1 314 mots** (114 graphies), **65 paires** (50 distinctes) et **4 triples** (4 distincts). Supprimer une ancre ou un mot illisible sépare ses anciens voisins. La contiguïté de chaque fenêtre est vérifiée dans chacune des quatre lectures, sans franchir de ligne ni de dessin.

Le texte de contrôle est celui des *Compositiones* de Scribonius, écrit au Ier siècle, dans l'édition latine de Georg Helmreich publiée à Leipzig en 1887. L’encodage XML utilisé est daté de 2021. Préface et notices fournissent **290 paragraphes**, 22 193 positions de mots, 17 568 paires et 13 710 triples dans les frontières retenues. Les paires et triples distincts sont respectivement 13 305 et 12 939. Les divisions de ligne imprimée ne coupent pas à elles seules le texte latin. En revanche, la ponctuation, les nombres, les mesures, le grec et les interventions éditoriales interrompent les fenêtres. Un token anormalement apostrophé comme *e't* dans la préparation 260 reste indivisible et exclu ; ses morceaux ne reçoivent pas le statut de mots. Le corpus avait déjà servi à une étude de recettes. Les deux clés de Celse étaient fixées indépendamment de ce texte. [XML du texte de Scribonius](https://raw.githubusercontent.com/lascivaroma/additional-texts/master/data/phi1011/phi001/phi1011.phi001.lascivaroma-lat1.xml) · [Édition numérisée](https://archive.org/details/cuascriboniilarg00scri)

**Permutations.** Chaque table attribue six valeurs distinctes à six signes. Pour chacun des deux jeux de valeurs, les 720 attributions possibles donnent exactement zéro paire et zéro triple ; 720 sur 720 égalent donc la clé proposée à chacun des deux niveaux. Les jeux de valeurs diffèrent, il n'existe aucune clé commune aux deux ensembles. Les suites de mots disponibles et le texte latin restent identiques pour toutes les clés.

**Contrôle positif annoncé.** La première suite admissible du texte indépendant est *et ob hoc*, préface, premier paragraphe. Avec six valeurs attribuées pour ce témoin artificiel, elle se recode `ds mo aml`. Le détecteur restitue les trois mots, les deux paires et le triple. Si on coupe après `mo`, il conserve la première paire et perd le triple. [Préface dans l'édition Helmreich](https://archive.org/details/cuascriboniilarg00scri/page/n9/mode/1up) · [Contrôle exécuté](tester.py)

**Vérification supplémentaire après calcul.** En partant du latin et en gardant seulement des mots d'au moins deux lettres, combien de suites entières les vraies tables pouvaient-elles écrire, même dans un manuscrit idéal ? Pour la première, deux paires seulement, *deinde ea* (§ 200, `odsad dm`) et *ad ea* (§ 271, `mo dm`). Pour la seconde, deux paires également, *ut cum* (§ 20, `ad sam`) et *tum cum* (§ 95, `dam sam`). Avec cette longueur minimale, aucune des deux clés ne pouvait reproduire un triple du corpus latin. Le détecteur a retrouvé les quatre paires lorsqu'elles lui ont été fournies sous leurs formes recodées. Ces résultats localisent une limite de l'expérience dans la faible partie de l'alphabet déchiffrable et dans le choix d'un seul texte de comparaison. [Préparation 20](https://archive.org/details/cuascriboniilarg00scri/page/n19/mode/1up) · [Préparation 271](https://archive.org/details/cuascriboniilarg00scri/page/n114/mode/1up) · [Détail des recodages](RESULTATS.json.gz)

## Reproduction

Télécharger le XML lié ci-dessus. Son SHA-256 est `903823a2c00454deccb2e30ffc3651b1d204d53b4bce1c8b9128275e79dc9687`. Exécuter `python3 -B tester.py /chemin/vers/phi1011.phi001.lascivaroma-lat1.xml` depuis ce dossier avec Python et lxml. L'archive produite contient les fenêtres EVA et leurs coordonnées, les correspondances exactes dans les deux textes, les distributions des permutations et les contrôles positifs. Les coordonnées EVA sont le locus, puis le numéro du tronçon et le rang du premier mot dans ce tronçon selon H (espaces joints). Les coordonnées latines sont la notice, le paragraphe, le segment séparé par une barrière et le rang dans le segment. [Programme](tester.py)
