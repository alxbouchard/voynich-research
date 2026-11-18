# Une même suite de signes peut-elle prédire les mots qui l’entourent ?

Une grande plante et un panneau de fragments partagent les deux groupes `qokol daiin`. Sur la grande plante (f18v.7), le troisième groupe reprend le premier. Sur le panneau de fragments (f102r2.18), le troisième devient `oky`. Le rapprochement de ces passages a servi à choisir la question. Nous avons ensuite testé deux conséquences sur des données réservées. [Critères et limites fixés avant ces vérifications](AVANT.md)

## Peut-on prévoir la suite sur d’autres feuillets ?

Cinq occurrences de `qokol daiin` sont présentes hors des deux feuillets de départ. Deux ont un voisin suivant qui satisfait les critères stricts communs aux quatre lectures. Sur la grande plante f22v.8, on attendait `qokol` et on lit `dam`. Sur le panneau f89v1.10, on attendait `oky` et on lit `chekal`. En acceptant le groupe suivant au même rang dans les quatre transcriptions malgré les barrières de l’alignement, on ajoute `sol` sur f23v.7 et `soleeg` sur f3r.16. La cinquième occurrence termine une ligne en f104v.11. Bilan de la prédiction par section, zéro sur deux en lecture stricte et zéro sur quatre avec l’élargissement prévu.

Parmi les suites strictement lisibles après `daiin` précédé d’un autre groupe, `qokol` revient 0 fois sur 164 dans les grandes plantes, 0 sur 30 dans les panneaux et 0 sur 93 ailleurs. Pour `oky`, les nombres sont respectivement 1, 0 et 0. Si l’on prédit plus généralement que le groupe précédant `daiin` va se répéter, 199 des 313 annonces sont évaluables. On observe quatre répétitions, contre 3,53 attendues quand on redistribue les voisins en conservant la face et la position finale ou intérieure. Sur 9 999 redistributions, 4 960 donnent au moins quatre répétitions. [Annonces des répétitions](REPETITIONS-ANNONCEES.json.gz) · [Relevé par lieu, contrôles et simulations](REPETITIONS-OUVERTES.json.gz)

## Peut-on lire les mots autour de ces passages ?

Dans sept corpus connus, nous avons cherché deux passages qui commencent par les mêmes mots X Y. Il fallait que le troisième soit à nouveau X dans un passage, et un autre mot Z dans l’autre. Chaque paire de lieux et chaque choix cohérent de valeurs par signe sont comptés à part. Plusieurs phrases ou découpages peuvent ainsi produire la même prédiction au même lieu. Les quatre groupes réservés du Voynich se lisent, dans l’ordre, `chod` et `dar` à gauche et à droite du premier triplet, puis `sheey` et `oky` autour du second. [Hypothèses avant ouverture](INTERPRETATIONS.json.gz) · [Voisins ouverts et scores](VOISINS.json.gz)

| Ouvrage ou corpus | Paires de passages | Prédictions de groupes par mots | Ajustements par signes | Prédictions de groupes par signes |
|---|---:|---:|---:|---:|
| Celse | 699 | 69 | 13 | 0 |
| Macer | 17 | 0 | 0 | 0 |
| Mayence, extrait de 1485 | 0 | 0 | 0 | 0 |
| RIDGES | 494 | 42 | 44 | 0 |
| Martino | 929 | 171 | 39 | 33 |
| *Régime du corps*, extrait | 8 | 0 | 0 | 0 |
| *Viandier* | 285 | 72 | 3 | 1 |
| **Total** | **2 432** | **354** | **99** | **34** |

**Aucune des 354 prédictions par mots et aucune des 34 prédictions par signes ne retrouve le voisin attendu.** Le modèle par mots ne pouvait annoncer à l’avance un groupe entier que lorsqu’un des trois mots déjà attribués revenait dans le texte connu. Les 99 ajustements par signes représentent 28 tables distinctes ; chacun suppose que `o` puisse être muet et que `ii` (57 ajustements) ou `aiin` (42) compte comme une unité. Les deux modèles peuvent s’abstenir. Pour une table partielle, l’encodeur propose les écritures formées de valeurs non vides déjà apprises ; il ne réinsère pas arbitrairement les signes muets. Le contrôle inverse vérifie directement les signes du voisin connu en permettant les nouveaux signes et en appliquant la convention du signe muet. Aucune des 376 confrontations individuelles disposant d’un voisin historique ne permet cette extension.

Le dernier voisin du panneau forme un **doublet** : on lit `qokol daiin oky oky`. Sur les 2 295 paires pour lesquelles le manuscrit ou le texte historique fournit un quatrième mot, aucune ne présente la répétition de Z à cet endroit. Sur les 2 432 paires, 128 peuvent recevoir après coup un dictionnaire par mots compatible avec les endroits disponibles. Toutes manquent du quatrième mot historique. Sur les 1 970 avec les quatre voisins disponibles, aucune ne survit.

**En retirant après coup le doublet**, 1 777 des 2 090 paires ayant les trois autres voisins disponibles peuvent recevoir un dictionnaire libre cohérent. Sur ces trois positions, en incluant aussi les références où un autre voisin manque, 219 annonces par mots et deux par signes étaient possibles avant ouverture. Toutes échouent. Le test inverse par signes échoue aussi dans les 281 confrontations encore disponibles. Retirer le doublet change donc fortement la compatibilité d’un dictionnaire ajusté librement. Les deux prédictions restantes par signes offrent à elles seules une puissance limitée. [Détail des dénominateurs](SENSIBILITE.json) · [Recalcul](sensibilite.py)

## Un témoin où « fleur » change de sens

Le texte italien de Martino réalise le motif *del fiore del* et *del fiore et*. Ces deux expressions sont réellement visibles dans un manuscrit du XVe siècle. En f29v, *fiore* appartient au fenouil utilisé pour une sauce au verjus. En f22r, le cuisinier fait un bouillon de pois chiches et emploie la fleur de farine. La table ajustée à *del, fiore, et* rend bien les trois mots de départ. À gauche du premier triplet elle propose `ky` pour *et*. On lit `chod`. Même les deux sens attestés de *fiore* dans le témoin laisseraient la traduction incertaine. [Photographies et lectures des quatre recettes](temoin/RAPPORT.md)

## Contrôle à clé cachée

Dans le *De medicina* de Celse, les deux suites *rursus et sanies et pus* (5.26) et *si et sanies profluit et* (6.7) permettent une épreuve positive. Nous avons choisi ces extraits parce que les trois mots d’ajustement contiennent toutes les lettres des quatre voisins, dont trois sont des mots nouveaux. Un générateur chiffre les lettres avec une substitution tirée au hasard. Le décodeur reçoit seulement les trois groupes chiffrés et les 699 candidats de Celse ; il ignore la clé, le numéro des bons passages et les quatre groupes à prédire. Il utilise le même découpage de signes, le même ajustement injectif d’une à deux lettres et le même encodage inverse que l’essai sur le Voynich. Pour chacune des trois clés, il ne reste qu’une solution et celle-ci prédit exactement les quatre voisins. Ces trois répétitions emploient le même texte. Elles contrôlent le fonctionnement du programme sur un cas de substitution simple où les bonnes phrases figurent dans son corpus. Elles ne mesurent pas ses chances de retrouver la langue d’un manuscrit inconnu. [Résultat par clé](CALIBRATION.json) · [Reproducteur](calibrer.py) · [Texte de Celse, XML Perseus](https://raw.githubusercontent.com/PerseusDL/canonical-latinLit/669d3657637ee44fb0aed2c37dd0f95c2b062193/data/phi0836/phi002/phi0836.phi002.perseus-lat5.xml)

Le résultat porte sur deux courts passages et des ouvrages de tailles, d’époques et de genres différents. Les fenêtres suivent les unités conservées par chaque source, allant d’une phrase à une notice. L’essai présuppose des équivalences répétables entre groupes ou entre signes, et recherche des formulations effectivement présentes dans les références. Il laisse ouverte l’hypothèse d’un texte décrivant les illustrations dans d’autres termes.

## Reproduction

Depuis ce dossier, utiliser `python3 -B calibrer.py` et `python3 -B sensibilite.py` pour reproduire les deux contrôles supplémentaires à partir des fichiers archivés. Les calculs principaux sont dans `lecture.py` et `repeter.py`. Le premier prend, après `annoncer`, les chemins du XML de Celse, du HTML du *Viandier* et du HTML de Martino, dans cet ordre. Son action `ouvrir` relit les annonces. Le second admet les mêmes actions sans sources externes. Les empreintes des trois fichiers téléchargés figurent dans `INTERPRETATIONS.json.gz`. [Provenance des corpus](../../2026-11-18-phrase-et-doublets/lecture/RESULTAT.md) · [Sources vernaculaires](../../2026-11-18-d-initial-et-formules/vernaculaire/RAPPORT.md)
