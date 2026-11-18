# Une expression fixe peut-elle annoncer la place d’un nom de plante ?

Sur les six panneaux du cahier 15, neuf combinaisons d’une graphie fixe et d’une direction signalent au moins une reprise de légende végétale juste à côté. **Aucune ne retrouve deux noms différents sur deux feuillets.** Les neuf combinaisons ont néanmoins été cherchées sur les neuf panneaux du cahier 19. Cinq y signalent ensemble 32 positions. La cible est lisible de la même manière dans les quatre lectures à 24 de ces positions. Aucune de ces 24 graphies ne reprend un mot de légende végétale locale. [Protocole et seuil fixé](PROTOCOLE.md) · [Apprentissage et positions gelées](PREDICTIONS-15.json) · [Résultats](VERIFICATION-15.json)

## Prédire la position avant d’examiner le mot

On prend pour indice une graphie qui n’apparaît qu’une fois sur sa ligne dans chaque lecture. Une règle comme « regarder le mot juste après kosar » désigne un emplacement par son rang dans la ligne. Si une lecture diverge sur le mot cible ou sur la séparation, la prédiction reste comptée et sa vérification est marquée incertaine. Les légendes considérées sont seulement celles de fragments végétaux qui sont lisibles dans les deux transcriptions et avec les deux traitements des petits espaces. Le cahier 15 fournit six panneaux étiquetés, répartis sur deux feuillets physiques, f88 et f89. Le cahier 19 fournit neuf panneaux sur quatre feuillets, f99 à f102. L’apprentissage et la réserve portent sur la même main et la même variété de Currier. Le choix du cahier écarte les panneaux voisins du même feuillet de l’autre lot. Les pages étaient déjà connues du projet. Les quatre lectures portent sur le même parchemin. [Inventaire et conventions de sélection](../../2026-11-18-legendes-et-paragraphes/comparer.py)

| Apprentissage → épreuve | Distance du nom à la graphie fixe | Règles ayant au moins un succès à l’entraînement | Règles répondant au seuil de deux noms sur deux feuillets | Règles émettant un appel en réserve | Appels en réserve, dont lisibles | Reprises exactes |
|---|---:|---:|---:|---:|---:|---:|
| 15 → 19 | 1 | 9 | 0 | 5 | 32, dont 24 | 0 |
| 15 → 19 | 2 | 4 | 0 | 3 | 18, dont 10 | 0 |
| 19 → 15 | 1 | 6 | 0 | 3 | 7, dont 5 | 0 |
| 19 → 15 | 2 | 5 | 0 | 1 | 1, lisible | 0 |

Le test principal s’abstient dès l’entraînement. Le résultat en réserve du tableau est un diagnostic plus généreux qui garde **toutes** les règles ayant un succès d’apprentissage. Chaque appel compte pour la règle qui l’a produit. Ces totaux ne sont pas un nombre de positions indépendantes. À distance deux on maintient un seul mot intermédiaire dans la même ligne et on exige que le mot intermédiaire et la cible concordent dans les quatre lectures.

Une version permissive déposée à l’avance retenait uniquement la meilleure règle, même sur un seul succès. À f89v2.7, la graphie que les deux éditions lisent juste après `kosar` est `sheol`, également présente dans l’étiquette f89v2.5. La règle « après kosar » se classe à égalité avec « avant opcheol ». Le départage alphabétique choisit la première. Elle n’émet aucun appel lisible ou incertain dans l’autre cahier. La règle permissive à distance deux, « deux positions après qokeoefy », s’arrête aussi sans appel. Dans le sens inverse, les règles permissives retenues sont « avant cheekey » et « deux positions avant ckhy ». Chacune reste sans appel. Le test principal et ces sélections n’ont donc prédit aucun nom unique dans la réserve. [Prédictions dans le sens inverse](PREDICTIONS-19.json) · [Épreuve inverse](VERIFICATION-19.json)

Sur le fond des positions voisines lisibles du cahier 19, on compte trois reprises de légende pour 573 cibles à droite et trois pour 574 à gauche, tous marqueurs admissibles confondus. Les deux directions peuvent porter sur le même mot réel. À titre de contrôle exploratoire, en gardant les 32 appels du tableau en place et en réaffectant les paquets de légendes entre les neuf panneaux, 282 240 des 362 880 affectations donnent elles aussi zéro reprise nouvelle, soit sept sur neuf. Dans le sens inverse, 600 des 720 affectations donnent zéro. Ce test sur des cibles rares a donc peu de pouvoir pour exclure un effet modeste.

## Deux mots fixes comme dans « sucus de [nom] »

Le contrôle sur l’imprimé allemand de 1485 a motivé une seconde spécification, enregistrée après l’épreuve à un mot et avant ce nouveau dépouillement. On cherche une paire de mots fixes qui précède ou suit le nom. Dans les deux cahiers, cinq paires orientées rencontrent un nom de légende à l’entraînement. Chacune n’y réussit que sur **un seul feuillet**. Parmi ces dix règles orientées, une seule désigne un emplacement exploitable dans l’autre cahier. [Règle complémentaire](DEUX-MOTS.md) · [Toutes les paires et leurs emplacements](DEUX-MOTS.json)

Sur f89r2.8, on lit `daiin oky cheody`. La dernière graphie se retrouve dans la légende f89r2.19. Sur f102r2.18, le groupe qui suit `daiin oky` est `oky` lui-même. Les deux éditions s’accordent sur ces trois derniers mots aux rangs 9, 10 et 11 de la ligne. Ce second `oky` ne figure pas dans les légendes végétales admissibles du panneau. Le premier exemple fournissait un emplacement à vérifier. La relation entre l’expression et la légende a échoué à l’emplacement suivant.

Dans un témoin artificiel, deux feuillets d’entraînement contiennent « sucus de [nom] » avec deux noms de plante distincts. La même construction introduit quatre noms différents sur quatre feuillets de réserve. La règle à un mot choisit « après de » et la règle à deux mots retrouve « après sucus de ». Toutes deux retrouvent les quatre cibles, puis une permutation cyclique retire les quatre correspondances. Une seule des 24 affectations du témoin conserve quatre succès pour « après de ». Ce témoin vérifie la capacité de trouver une expression fixe quand le texte et les légendes en contiennent une. [Données du témoin](TEMOIN.json)

Les preuves portent sur les reprises exactes de graphies de trois signes au moins. Une flexion différente, une abréviation, un nom en plusieurs mots dont aucun élément ne reste identique, ou une légende partiellement illisible peuvent empêcher le comptage. Une reprise à l’intérieur du panneau peut aussi renvoyer à un autre dessin. Le corpus n’identifie le sens d’aucun mot de la formule.

## Reproduction

Depuis ce dossier, exécuter dans cet ordre les commandes ci-dessous. Le premier fichier de prédictions, déposé avant confrontation aux noms du cahier 19, a pour empreinte SHA-256 `9d762d436b4b007923652abdc18a6072d901f3cb9da4f9203894a79804ea9717`. Le sens inverse constitue une sensibilité. Les listes complètes des règles apprises et leurs ex æquo figurent dans les deux fichiers de prédictions.

```sh
python3 -B formules.py predire 15
python3 -B formules.py verifier 15
python3 -B formules.py predire 19
python3 -B formules.py verifier 19
python3 -B paires.py
```
