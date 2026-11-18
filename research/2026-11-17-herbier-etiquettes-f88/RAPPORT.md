# Peut-on partir des dessins de f88 pour lire les étiquettes du Voynich ?

**Sur les 22 fragments de f88, les deux lecteurs n’ont identifié aucune plante avec assez d’assurance pour s’en servir comme texte clair.** Ils ont proposé le même nom une seule fois, *Hydrocotyle*, tous deux avec une confiance faible. Même en acceptant cette conjecture, on aurait une plante sur les trois requises pour essayer une règle de lecture. Les 51 étiquettes de f99 restent disponibles pour un autre essai. [Planche de trois exemples](../../docs/PIECES_REFERENCES.md#piece-b116914d234560) · [Résultats chiffrés](RESULTATS.json)

## Ce qui a été mis à l’épreuve

Nous avons testé la première étape d’une piste de déchiffrement. Si plusieurs dessins permettent de reconnaître la plante indépendamment de l’écriture, leurs noms médiévaux peuvent servir à chercher des correspondances entre signes, puis à prédire des étiquettes entières sur un autre feuillet. Le protocole et les seuils ont été consignés avant la réception des réponses dans le commit local `b450b05`. Les 22 inscriptions de type « fragment de plante » sur f88 et les 51 sur f99 ont été inventoriées par identifiant, sans extraire leur contenu pour le calcul. L’étude antérieure sur f99 était connue du projet. [Protocole](PROTOCOLE.md) · [Inventaire des lignes](documentation/INVENTAIRE.json)

Deux agents IA ont lu les images dans des conversations distinctes, sans recherche, sans correction et sans liste de choix. Chacun a donné un nom principal ou s’est abstenu, en indiquant les traits visibles et sa confiance. Les premières réponses aux huit cartes témoins ont été enregistrées avant de leur montrer les 22 cartes de f88. Les préparateurs des images et de la clé historique ne participaient pas aux identifications. Ces deux lectures partagent une technologie et des connaissances possibles. Une concordance entre agents ne remplace pas un diagnostic de botaniste ou de spécialiste des herbiers médiévaux.

## Les lecteurs reconnaissent-ils un dessin dont le nom est connu ?

Les huit cartes témoins viennent des faces 2r à 5v du *Sloane MS 4016*, un herbier lombard daté vers 1440. Le préparateur a extrait la première plante du registre supérieur sur chaque face, masqué les inscriptions, puis conservé à part les images des légendes. L’interprétation moderne de six entrées est étayée au moins au niveau d’un groupe botanique. Deux noms historiques ont des identifications contradictoires dans des manuscrits apparentés. [Notice de la British Library](https://searcharchives.bl.uk/catalog/040-002116409) · [Détails des huit légendes](../../docs/PIECES_REFERENCES.md#piece-baf5def3542137) · [Clé et références pour chaque plante](documentation/CLE_H.json)

| Carte | Première réponse A | Première réponse B | Confrontation à la légende |
|---|---|---|---|
| H01 | *Pulsatilla*, faible | *Pulsatilla*, moyenne | *Anthora* correspond au groupe des aconits |
| H02 | *Cichorium*, faible | *Cichorium*, faible | La légende désigne une absinthe du genre *Artemisia* |
| H03 | Abstention | Abstention | La légende désigne une buglosse |
| H04 | *Smilax*, faible | Abstention | *Amomum* a plusieurs interprétations |
| H05 | *Verbascum*, moyenne | *Verbascum*, moyenne | Molène, accord confirmé pour *Andronica* |
| H06 | *Mercurialis*, moyenne | *Mercurialis*, moyenne | *Ambroxiana* a plusieurs interprétations |
| H07 | *Ranunculus*, moyenne | *Ranunculus*, moyenne | Renoncule au sens historique, qui inclut la ficaire |
| H08 | *Artemisia*, moyenne | *Artemisia*, moyenne | Armoise, accord confirmé pour *Absinthium ortense* |

Avec les noms usuels historiques, **3 témoins sur 8** sont reconnus par les deux lecteurs avec une confiance moyenne ou haute. Ils avaient donné quatre réponses communes à ces niveaux. Trois sont vérifiables et les trois concordent avec la référence. H06 reste indéterminé. **Si l’on exige un genre moderne univoque**, H07 devient également indéterminé et le résultat tombe à **2 sur 8**, en dessous du seuil de trois. Sur H02, les deux lecteurs ont choisi la même plante avec une confiance faible et la légende désigne une autre plante. [Réponses A](lecteurs/A_H.json) · [Réponses B](lecteurs/B_H.json) · [Grille historique](evaluation/H.json)

## Qu’ont-ils reconnu sur f88 ?

| Mesure | Résultat |
|---|---:|
| Cartes de fragments végétaux présentées à chacun | 22 |
| Noms proposés par A, tous de confiance faible | 6 |
| Noms proposés par B, tous de confiance faible | 4 |
| Cartes nommées par au moins un lecteur | 9 |
| Doubles abstentions | 13 |
| Même nom proposé par les deux lecteurs, toute confiance | 1 |
| Même nom proposé par les deux, confiance moyenne ou haute | **0** |

La seule concordance concerne **V19**, le dessin de droite de la troisième rangée de f88r. Les deux lecteurs décrivent des feuilles arrondies, à bords crénelés, portées par des pétioles. Le premier propose le genre *Hydrocotyle*, le second aussi. Ils ne jugent pas les caractères observés assez distinctifs pour dépasser une confiance faible. La comparaison des réponses montre également qu’ils ont évoqué *Aconitum* sur des dessins différents. Ces propositions sont archivées avec leurs raisons. [Dessin V19 et voisins](../../docs/PIECES_REFERENCES.md#piece-2a3fb6587e4dd2) · [Réponses A](lecteurs/A_V.json) · [Réponses B](lecteurs/B_V.json) · [Original f88r à Yale](https://collections.library.yale.edu/iiif/2/1037112/full/full/0/default.jpg)

Les nombres de dessins et de légendes coïncident sur f88r, mais leur répartition diffère. Les quatre rangées contiennent 5, 4, 2 et 1 dessins. Les lignes d’étiquettes de fragments se répartissent en 5, 5 et 2 entrées sur les trois premières rangées. Le dessin du bas V12 reste sans inscription adjacente visible. Sur les deux faces, sept des 22 inscriptions n’ont qu’un seul motif candidat dans leur voisinage immédiat. Quinze peuvent se rapporter à plus d’un motif. V19 jouxte l’inscription f88r.25 sans autre dessin concurrent à cet endroit. Ce fait précise où chercher si son identification devenait plus sûre. L’extraction a également tronqué une partie de V20 près d’une inscription. Les préparateurs ont conservé les limites des détourages et les incertitudes sur les traits pâles ou superposés. [Catalogue du cahier et disposition des dessins](https://www.voynich.nu/q15/index.html) · [Positions des 22 cartes](documentation/POSITIONS_V.json) · [Rattachements inscription par inscription](documentation/ATTACHES.json)

## Décision et portée

Le seuil fixé sur f88 était de trois plantes distinctes reconnues par les deux lecteurs, documentées dans un herbier historique et rattachables chacune à une inscription. Le nombre de noms communs à confiance au moins moyenne était déjà nul, avant l’examen de leur orthographe ou de la longueur de l’étiquette. Nous nous sommes donc arrêtés avant l’ajustement d’une substitution. **Aucune valeur de signe, aucune prédiction sur f99 et aucune lecture en prose ne découlent de cet essai.** Le contrôle par permutation aurait porté sur les prédictions entières de f99. Il n’y en a aucune à évaluer.

Le résultat porte sur une méthode d’identification à partir de fragments dessinés, souvent réduits à des racines et à quelques feuilles. Il demeure compatible avec des légendes qui auraient désigné une plante, une partie, une préparation ou tout autre objet pour le scribe. L’intention du scribe et la langue de son texte restent indéterminées.

## Recalcul

Exécuter `python3 compter.py` dans ce dossier. Le programme utilise les quatre séries originales et les décisions documentées dans `evaluation`. Il produit les nombres d’accords, de cas vérifiables et d’abstentions, ainsi que le résultat en exigeant des genres modernes univoques. Les images originales et les cartes individuelles figurent dans la copie locale de livraison avec leurs empreintes. [Script de comptage](compter.py) · [Décisions pour les fragments](evaluation/V.json) · [Recomptage indépendant et vérification des images](documentation/RECOMPTAGE.json)
