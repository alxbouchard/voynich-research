# Ce qu’une amorce permet effectivement de lire

Dans un passage latin chiffré pour cette expérience, l’amorce de trois mots a permis de lire entièrement **un voisin sur quatre**, `et`. Le dictionnaire de la notice a complété les trois autres. Une expérience en texte artificiel a par ailleurs vérifié que le programme reconnaît le voisinage voulu sur trois répétitions et détecte un voisin incompatible. [Protocole](PROTOCOLE.md) · [Données](ETALON.json)

## La première notice du Macer

La première notice de l’édition de calcul est *Artemisia*, 184 mots. Le premier mot d’au moins quatre lettres qui satisfait la règle des trois occurrences avec deux voisins et une portée de 120 mots est `dicitur`, aux rangs 27, 35 et 141. La notice a été chiffrée par une permutation des 26 lettres qui conserve les séparations entre mots. Pour déchiffrer, le programme reçoit les trois mots clairs autour du rang 27, `quae dicitur indeque`. Ces trois mots révèlent dix correspondances. La fonction de lecture reçoit le texte chiffré et l’amorce. La clé complète de construction reste en dehors de cette fonction. [Texte des vers](../../2026-11-18-opcheor-paralleles/latin/vers.tsv) · [Édition et normalisation](../../2026-11-18-opcheor-paralleles/latin/SOURCE.md)

| Voisin réservé | Lecture à clé gelée | Avec les 157 formes de la notice | Avec les 3 874 formes des 76 autres notices | Texte révélé |
|---|---|---|---|---|
| Gauche du rang 35 | `in?entri?` | inventrix | aucune | inventrix |
| Droite du rang 35 | `e?u?` | ejus | ejus | ejus |
| Gauche du rang 141 | `ru?eti?` | rubetis | aucune | rubetis |
| Droite du rang 141 | `et` | et | et | et |

Le groupe chiffré `FD` se lit `et` avec les deux correspondances apprises. La proposition inversée `te` contredit les deux. Le point d’interrogation dans les autres mots marque une lettre encore inconnue. Même la proposition unique `ejus` requiert un lexique. Le premier lexique contient par construction les mots à retrouver. Le second, ajouté comme contrôle de couverture, provient entièrement des autres notices. Il manque deux des quatre mots réservés. Le mot à gauche du rang 141 est le dernier mot du vers 23. `dicitur et` ouvre le vers 24. Les limites de vers restent visibles dans la source, et le calcul suit l’ordre continu des mots de la notice. [Vers de l’édition](https://la.wikisource.org/w/index.php?title=De_viribus_herbarum&oldid=272959)

Sur les 181 mots hors des trois mots d’amorce, **20 occurrences de 15 formes distinctes** se lisent en entier à clé gelée. Ce décompte comprend deux reprises de `dicitur` et cinq occurrences de `et`. Il inclut des mots qui n’étaient pas donnés, par exemple `diana`, `deducit`, `trita` et `cruda`. À titre d’illustration supplémentaire, le mot correspondant effectivement à « racine » dans la notice, `radix` au rang 136, se laisse lire `radi?`. Les deux lexiques donnent chacun `radix` comme unique complément. Le cinquième signe demeure inconnu à partir de l’amorce seule. Nous avons choisi cet exemple après le test des quatre voisins. [Résultats exhaustifs](ETALON.json)

## Les trois occurrences et le concurrent déplacé

Le témoin syntaxique artificiel contient trois répétitions de `peak`. Pour la première, les mots d’amorce sont `pick peak beak` avec la lecture H et `pick peak back` avec ZL. Les deux versions ont été construites avec la même table. Au milieu vient `peak at can` et à la fin `raccoon peak peeler`. Ces suites fabriquées n’ont pas de valeur historique. Le calcul apprend ses tables à partir du seul premier triplet. Dans le vocabulaire fermé, il propose `peeler` pour `cheekey` et `pelere` pour le concurrent où la deuxième copie de `e` a été déplacée à la fin. Les deux formes sont présentes dans chaque lexique, y compris dans les versions où une seule figure à côté du dernier `peak`. Les entrées isolées du lexique ne forment aucun voisinage.

| Modification du passage | Résultat aux limites d’une à deux et d’une à trois lettres par signe, pour H et ZL |
|---|---|
| Passage construit intact | Une table relie les trois rangs avec les deux voisins finaux, dont le voisin droit `peeler`. |
| Droite finale remplacée par `pelere` | Seul le concurrent déplacé satisfait les trois occurrences. |
| Gauche finale remplacée par `raccogn` | `peeler` reste prédit et rencontré, mais ses deux voisins ne passent plus ensemble. |
| Droite du milieu changée de `at can` en `at dog` | Les deux côtés de l’occurrence finale passent encore. Aucune table ne satisfait les trois rangs. |

Les seize essais emploient les fonctions `potential` et `heldout` de l’analyse du Voynich. Chaque vérification est limitée aux tables apprises du premier triplet, que le programme retrouve effectivement. Le témoin latin vérifie une propriété différente et plus simple, avec une lettre par signe, une clé bijective et une amorce exacte fournie. Aucun de ces deux contrôles n’établit que le Voynich partage cette clé ou ce mécanisme. Pour reproduire les résultats, exécuter `python3 -B etalon.py` dans ce dossier. [Programme](etalon.py) · [Méthode testée](lecture.py)
