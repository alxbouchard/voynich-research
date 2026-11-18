# L’emplacement du paragraphe sous une rangée peut-il être retrouvé ?

Sur **f88v, f89r1 et f99v**, les trois pages qui permettent une comparaison interne en dehors de l’exemple connu, **aucun des 25 couples « rangée, mot de fragment » retenus ne revient en prose sur la même page**. Il est alors impossible d’en déduire lequel des paragraphes reprend le contenu de la rangée. La comparaison accepte les mots entiers d’au moins trois signes lus dans les deux éditions sur le même fragment, avec les blancs douteux joints. Une rangée peut avoir plusieurs mots, et le même mot sur plusieurs de ses objets compte une seule fois. [Protocole fixé avant décompte](PROTOCOLE.md) · [Matrices et emplacements](RESULTATS.json)

## Ce qui se passe sur la page connue

Sur **f89r2**, deux mots passent d'une légende à la prose. Les paragraphes où ils reparaissent se trouvent sous deux rangées différentes de celles des légendes. Ils se croisent dans l'ordre suivant.

| Mot dans les éditions H et ZL | Légende | Reprise en prose sur cette page | Place dans la ligne |
|---|---|---|---|
| `opcheor` | f89r2.5, rangée 1 | f89r2.22, paragraphe sous la rangée 3 | 5 en H et ZL |
| `cheody` | f89r2.19, rangée 3 | f89r2.8, paragraphe sous la rangée 1 | 14 en H, 12 en ZL |

À l'échelle du manuscrit, `opcheor` en prose P0 n’a qu’une occurrence dans chacune de ces éditions. `cheody` en compte 77 en H et 75 en ZL pour les mêmes blancs joints. Chacun des deux mots a une seule occurrence parmi les mots des légendes de fragments dans ces éditions. Le caractère exceptionnel de la reprise en prose diffère donc beaucoup entre l'un et l'autre. Une lecture ancienne du cinquième groupe de f89r2.22 est `opchear`. Les deux éditions principales utilisent le même parchemin. La description de Stolfi place quatre dessins dans la première rangée et six dans la troisième, dont le dernier sans légende assignable. Les lignes de prose traversent le pli du dépliant. Leur position laisse ouverte la possibilité d'un renvoi sur la page, sans établir quel organe, objet ou action désigne le mot. [Positions sur le parchemin](../../2026-11-18-formes-souterraines/nom/photo/REPRISE.md) · [Description de Stolfi](https://www.ic.unicamp.br/~stolfi/voynich/Notes/102/work/Notes/040/html/f89r2.htm) · [Transcriptions du panneau](https://www.voynich.nu/q15/f089r2_tr.txt) · [Dépliant de Yale](https://collections.library.yale.edu/iiif/2/1006233/full/2000,/0/default.jpg)

Échanger les paragraphes 1 et 3 de f89r2 explique les deux reprises d'un coup. Cette hypothèse apparaît après l’observation. Sur les trois autres pages avec plusieurs paragraphes admissibles, aucun mot de trois signes n’a permis d’en éprouver la correspondance dans l’analyse principale.

## Les huit permutations des trois pages

La table de géométrie antérieure contient 17 rangées sur neuf pages. Douze disposent d'un paragraphe local. Deux blocs indiqués par ZL en f102v1 et f102v2 sont scindés en deux dans H. Ils sortent du test de paragraphe entier. La seule rangée admissible de f88r garde son inventaire mais n'offre aucun choix entre deux paragraphes sur la même page. Restent six rangées et six paragraphes sur trois pages dans le test principal, auxquels s'ajoutent trois paires rangée–paragraphe en réintégrant f89r2. La matrice de chaque page conserve les longueurs de ses paragraphes et toutes les répétitions de ses mots lors du mélange. [Table et justification des rangées](../../2026-11-18-paires-ingredients/rangees/README.md)

| Convention, taille minimale | Couples rangée–mot hors f89r2 | Couples présents en prose sur leur page | Score observé | Scores des 8 permutations |
|---|---:|---:|---:|---|
| Espaces douteux joints, 3 signes | 25 | 0 | 0 | 8 scores nuls |
| Joints, 1 signe | 26 | 0 | 0 | 8 scores nuls |
| Espaces douteux séparés, 3 signes | 29 | 2 | 1 | 4 scores de 1 et 4 de 2 |
| Séparés, 1 signe | 30 | 2 | 1 | 4 scores de 1 et 4 de 2 |

Dans les deux dernières lignes, `chol` des légendes de la deuxième rangée de f89r1 apparaît dans les deux paragraphes candidats. `oldy` d’une légende de la première rangée de f99v se trouve uniquement dans le second paragraphe. Ainsi aucune de ces lectures ne désigne exclusivement le bon paragraphe. En réintroduisant f89r2 avec les paramètres principaux, 33 couples sont admissibles. Deux reviennent en prose sur leur page. Le score de la mise en page est nul. Sur 48 permutations, 24 obtiennent zéro, 16 obtiennent un et huit obtiennent deux. Aux blancs joints avec un seuil d’un signe, `dy` de la deuxième rangée de f89r2 revient sous la troisième. Un score nul n’établit pas que ces auteurs ignoraient les plantes figurées. Une autre forme grammaticale du nom ou une autre fonction des étiquettes échappe à la copie littérale testée ici.

Le contrôle construit à trois pages avec mots propres et mots partagés donne le bon ordre comme unique maximum sur huit permutations. Échanger les deux paragraphes d'une page diminue le score de deux et un contrôle où tous les mots sont partagés donne le même score pour les huit ordres. Pour refaire l’extraction et l’énumération, exécuter `python3 -B comparer.py` dans ce dossier. Le fichier JSON conserve les pourtours de paragraphes, tous les objets, mots et lignes comparés, les quatre variantes et les distributions. [Calcul](comparer.py)
