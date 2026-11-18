# Six noms vrais permettent-ils d'en lire un autre ?

Une clé partielle correcte a lu de bout en bout **deux noms nouveaux sur six**, *Aristologia longa* et *Altea*. Sur les 82 lettres des six désignations réservées, elle a fourni **78 lettres justes**, laissé quatre blancs et produit zéro lettre erronée. L'expérience utilise les rubriques réellement imprimées des chapitres I à XII du *Gart der Gesundheit* (Mayence, 1485, exemplaire de Munich). Nous avons appliqué nous-mêmes une substitution lettre pour lettre à ces noms connus. Elle reproduit un cas favorable où les frontières, la position des lettres et six noms clairs corrects sont donnés. [Rubrique d'*Aristologia longa*](rubrique-33.jpg) · [Photographie de Munich](https://www.digitale-sammlungen.de/view/bsb00032739?page=33) · [Rubrique d'*Altea*](rubrique-35.jpg) · [Photographie de Munich](https://www.digitale-sammlungen.de/view/bsb00032739?page=35)

Les douze titres sont consécutifs et commencent tous par A. Les six premiers ont appris les lettres des formes *Arthemisia*, *Abrotanum*, *Absinthium*, *Allium*, *Agrimonia* et *Apium*. L’entrée du décodeur pour les six suivants contient les suites opaques et leurs espaces. Il restitue les lettres apprises à leurs positions sans consulter un dictionnaire. Les formes claires de la réserve sont alors comparées à la prédiction enregistrée. Le générateur de défi et l'évaluateur connaissent la substitution artificielle. La séparation concerne les entrées de la fonction de lecture ; un historien indépendant n'a pas constitué ces douze énigmes. [Protocole figé](PROTOCOLE.md) · [Défi masqué](DEFI.json) · [Prédictions avant dépouillement](PREDICTIONS.json) · [Graphies et périmètre des rubriques](GRAPHIES.md)

| Chapitre | Lecture sans le corrigé | Nom latin de la rubrique, normalisé |
|---|---|---|
| VII | apium sil?estre | Apium silvestre |
| VIII | apium rusti?um | Apium rusticum |
| IX | apium emoroi?arum | Apium emoroidarum |
| X | aristologia rotun?a | Aristologia rotunda |
| XI | aristologia longa | Aristologia longa |
| XII | altea | Altea |

Le calcul principal prévu sur le seul premier mot restitue les six premiers mots réservés (42 lettres sur 42). Les trois premières occurrences sont toutefois des reprises exactes d’*Apium*, déjà donné au chapitre VI. Les trois autres, *Aristologia* deux fois et *Altea* une fois, sont des lectures exactes de deux formes distinctes nouvelles (27 lettres sur 27 occurrences). Le score par désignation entière tient compte des qualificatifs, sans assimiler une reprise du seul premier mot à la lecture d’un nom complet inédit. La lecture triviale consistant à émettre le A initial et des blancs restitue 6 lettres sur 82, et aucun nom complet.

La transcription de travail développe notamment les finales abrégées en *-um*. En réunissant en plus les caractères u et v dans tous les noms, la lacune de *siluestre* disparaît, portant le total à 79 lettres sur 82 et trois noms exacts sur six. C'est une convention distincte, fixée avant le calcul. En cachant successivement chacun des douze titres et en donnant les onze autres, la clé retrouve 10 des 12 noms complets et 129 lettres sur 131 dans la convention principale. Les répétitions alphabétiques et le recouvrement des lots rendent ce dernier résultat plus facile. [Toutes les lectures et les deux conventions](RESULTATS.json)

Parmi les 720 permutations des six appariements d'apprentissage, 716 échouent dès la comparaison des longueurs. Sur les quatre encore possibles, trois exigent des valeurs incompatibles pour les lettres et la permutation correcte reste seule. Ce contrôle mesure surtout à quel point les six longueurs imposent déjà l’appariement dans cette petite série. Il ne mesure pas la probabilité générale de déchiffrer un texte inconnu par hasard.

Pour reproduire, exécuter dans ce répertoire, avec Python 3 et sans dépendance externe :

```sh
python3 controler.py preparer
python3 controler.py predire --titres chemin-inexistant
python3 controler.py verifier
```

Les sources et empreintes des photographies sont consignées dans [l'inventaire des douze titres](TITRES.json). Les deux détails exposés proviennent des vues 33 et 35, en coordonnées de la reproduction à 1 400 pixels de large, respectivement (222, 1213, 1022, 1310) et (205, 1315, 333, 1380). L’édition et la façon de segmenter les titres sont explicites. Appliquer cette mesure à une proposition sur le Voynich demanderait de justifier séparément les appariements, l'unité de signe, les sons et les limites de mots.
