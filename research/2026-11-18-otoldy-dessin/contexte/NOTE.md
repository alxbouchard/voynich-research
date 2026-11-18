# Une légende du dépliant des rosettes revient dans la prose botanique

**La suite entière `otchdy.otoldy` apparaît deux fois dans l'édition Zandbergen–Landini (ZL).** Elle forme une courte inscription du grand dépliant des neuf rosettes, fRos.45. Elle apparaît aussi aux positions 9 et 10 d'une ligne sur la planche botanique f48v.9, juste après une interruption de l’écriture par le dessin. Les deux mots se suivent sans interruption sur les deux pages. Chez Glen Claston, la même paire se retrouve dans son autre alphabet aux deux emplacements. Les deux systèmes représentent les formes de l’écriture. Cette concordance ne fixe ni leurs sons ni le référent de la légende. [Ligne f48v.9 de ZL](../../../voynich_20261028/data/ZL3b-n.txt#L2087) · [Légende des rosettes](../../../voynich_20261028/data/ZL3b-n.txt#L5314) · [Témoins et empreintes](TEMOINS.json)

Ce rapprochement a été remarqué en vérifiant la couverture des éditions après avoir enregistré le test sur les voisins botaniques de `otoldy`. Son examen est exploratoire. L'ancien inventaire des occurrences dans le projet reconnaissait les folios à identifiants numériques. Le code spécial `fRos` lui échappait. Le même mot peut donc aussi entrer dans une inscription sur un grand diagramme. Les données antérieures sur les fragments isolés gardent leur périmètre. [Version antérieure du calcul](https://github.com/alxbouchard/voynich-research/blob/643672ab060dad9ddc2ec5fecc4b9814f83a7df0/research/2026-11-18-mots-des-images/racines/recherche_racines.py#L52) · [Calcul corrigé](../../2026-11-18-mots-des-images/racines/recherche_racines.py)

## Les deux témoins

| Édition | Ligne botanique à f48v.9 | Dépliant |
|---|---|---|
| Takahashi (H) | `otchdy.otoldy` | Cette édition ne couvre aucun des loci du grand dessin intérieur |
| Zandbergen–Landini | `otchdy.otoldy` | La légende entière fRos.45 donne `otchdy.otoldy`. Le commentaire de localisation est `7:9` |
| Glen Claston (v101 natif) | `ok179.okoe89` dans la ligne 1172, unité `48v.9` | `ok179.okoe89` au milieu d'une unité de quatre groupes, ligne 2911, `rose.east_labels` |
| Glen Claston (même transcription remise en ordre au format IVTFF) | `ok179.okoe89` | `ok179.okoe89` sur la seule ligne fRos.45 |
| Référence RF, synthèse automatisée de GC et ZL | `otch@152;y.otoldy` en EVA étendu | Même écriture étendue. L'EVA simplifié donne `otchdy.otoldy` aux deux lieux |

L’édition ZL classe `7:9` comme le neuvième repère associé à la rosette 7 dans la numérotation de Petersen. La rosette 7 se situe en haut à droite de sa grille. Les noms géographiques de l'original Claston délimitent ses propres régions. Le groupe appartenant à `rose.east_labels` est distinct de son unité `rose.neast_labels`. Ces identifiants seuls ne décrivent pas précisément la position du mot par rapport à un élément dessiné. Le rattachement à un objet demande l’image. [Grille et explication de ZL](../../../voynich_20261028/data/ZL3b-n.txt#L5253) · [Description de la face entière](https://www.voynich.nu/q14/index.html#fRos) · [Origine et remaniement des éditions](https://www.voynich.nu/data/000_README.txt)

La ligne botanique était déjà publiée en EVA sur une page de Jorge Stolfi datée du 6 mai 1998. Une correspondance de 2006 atteste la publication de la transcription de Claston cette année-là. Nous avons contrôlé dans le fichier que l'éditeur distribue comme l'original non modifié que le couple y figure aux deux endroits, avant la mise en correspondance moderne des numéros de ligne. En mars 2017, Wladimir D rapprochait déjà plusieurs légendes portant `otoldy` et envisageait la désignation d’un ingrédient. Nous n'avons établi aucune priorité pour avoir relevé cette séquence de deux mots. [Ancienne page de Stolfi](https://ic.unicamp.br/~stolfi/voynich/Notes/015/pages-html-old/f48v.html) · [Correspondance sur la publication de Claston](https://www.as.up.krakow.pl/jvs/library/1-1-2007-05-05/3JVSlibKI3U.htm) · [Fichier original v101](https://www.voynich.nu/data/voyn_101.txt) · [Hypothèse de Wladimir D, 21 mars 2017](https://www.voynich.ninja/thread-159-page-6.html)

## À quelle fréquence une autre légende entière donne-t-elle le même résultat ?

Nous avons ensuite comparé toutes les inscriptions courtes de deux groupes simples du même dépliant aux suites de deux mots contigus des 1 608 lignes de prose botanique sur 128 faces. Le corpus comprend exactement 137 lignes d’étiquettes pour 160 loci du dépliant en ZL. Les critères de longueur et de lisibilité gardent 18 légendes quand on sépare les espaces incertains et 10 quand on les joint. Une seule légende se retrouve en entier dans la prose botanique dans chaque calcul, à f48v.9. L'ordre inverse `otoldy.otchdy` ne se retrouve sur aucune ligne de H ou de ZL. [Toutes les occurrences et comparaisons](RESULTATS.json)

Pour donner l'échelle de cette comparaison, on peut garder chaque premier mot à sa place et redistribuer les deuxièmes mots entre ces étiquettes. Parmi les 18 × 18 appariements individuels possibles, 8 forment une paire présente dans la prose botanique. Lors d'une redistribution complète au hasard, la probabilité exacte qu'au moins une paire quelconque y figure est de 7 079/18 360, soit 38,6 %. Avec les espaces joints, 1 des 10 × 10 appariements existe et la probabilité est de 1/10. Les choix de la section, de la longueur des légendes et du mot qui a dirigé l'attention ont été faits en connaissant le rapprochement. Ces probabilités conditionnelles ne mesurent pas la probabilité que la légende désigne une plante ou une racine. [Conditions du complément](COMPLEMENTS.md)

## Les cinq emplois dans la prose botanique

| Lieu | Main et groupe de Currier | Position H / ZL dans la ligne | Voisin immédiat avant | Voisin immédiat après |
|---|---|---|---|---|
| f22r.11 | 1, A | 5/10 dans les deux | `oky` | `yty` |
| f28r.7 | 1, A | 5/8 dans les deux | `shocthy` | `dshor`, après interruption par le dessin |
| f44v.1 | 1, A | 9/9 et 10/10 | `qotshol` | fin de ligne, première ligne du paragraphe |
| f48v.9 | 5, B | 10/12 dans les deux | `otchdy` | `ytam` |
| f53v.13 | 1, A | 2/2 dans les deux | `ycthodaiin` H, `yckhodaiin` ZL | fin de paragraphe |

Aucun voisin immédiat ne réapparaît du même côté sur une autre de ces cinq faces. Dix paires de faces permettent une comparaison à gauche, trois à droite. Si l'on s'arrête aussi aux interruptions par les dessins, dix paires restent comparables à gauche et une à droite. À deux mots de distance, `dol` se retrouve à droite aux lieux f22r.11 et f28r.7. Ce rapprochement franchit le dessin à f28r.7. Les deux éditions et les deux conventions de découpage donnent les mêmes constats. L'indication de paragraphe reste distincte d'une fin de phrase dans une langue identifiée.

Le contrôle fixé avant le calcul demandait un autre mot de fréquence cinq, sur cinq faces distinctes, avec les quatre emplois de la main 1 / Currier A et l'emploi de la main 5 / Currier B. Aucun mot témoin ne remplit tous ces critères dans les quatre traitements. Le score brut de la cible est donc exposé sans rang comparatif pour les cinq faces ensemble. [Protocole antérieur au calcul](PROTOCOLE.md)

Dans le seul sous-corpus de la main 1 / Currier A, un calcul complémentaire permet une comparaison sur quatre faces. Chez Takahashi, 47 des 48 mots témoins de fréquence quatre sur quatre faces ont, comme la cible, zéro reprise de voisin immédiat. Chez ZL, c’est le cas pour 41 témoins sur 44 avec les blancs douteux séparés et 41 sur 43 avec les blancs joints. Les témoins présentant aussi le même nombre d’emplois initiaux, finaux et intérieurs ont tous un score nul (1, 1 et 2 mots témoins respectivement). La variation des voisins est donc fréquente pour des mots aussi peu attestés. La présence ou l'absence d'un article, d'un verbe ou d'une flexion demeure indéterminée.

Exécuter `python3 compter.py` pour recalculer les voisinages, les dénominateurs, les témoins et les redistributions exactes. Le calcul utilise la bibliothèque standard et les transcriptions H/ZL du dépôt. La somme SHA-256 du protocole avant calcul est `50ecfac51b531275e5517e24ab9c8237b38ad2849c4c2a218a08f60a4255a6ca`. Pour les témoins documentaires, `python3 verifier_temoin.py dossier_des_huit_editions chemin/vers/voyn_101.txt` reconstitue les courts extraits et les hachages à partir des fichiers indiqués dans le registre. [Programme des calculs](compter.py) · [Programme pour les sources documentaires](verifier_temoin.py) · [Lignes et empreintes des sources originales](TEMOINS.json)

## Sensibilité à la lecture oteedy de fRos.45

Deux lecteurs IA des photographies anonymisées ont envisagé `ee` dans le premier groupe de la légende fRos.45. Nous avons repris les calculs après réception de ces lectures, avec une seule substitution à cette ligne dans une copie de travail des données ZL. Le texte botanique, la deuxième forme de la légende et tous les autres loci sont conservés à l'identique. Le programme ne réécrit aucune transcription source. [Script de substitution](variante_rosette.py) · [Lieux, positions et comparaisons](VARIANTE_ROSETTE.json)

| Lecture | `otchdy.otoldy` sur une même ligne | `oteedy.otoldy` | Étiquettes à deux mots reprises en prose botanique, espaces douteux séparés / joints |
|---|---|---|---|
| Takahashi, fichier publié | f48v.9, mots 9–10 | 0 | Dépliant absent de cette édition |
| ZL, fichier publié | f48v.9, mots 9–10, et fRos.45, mots 1–2 | 0 | 1/18 et 1/10 |
| ZL, variante locale `ee` | f48v.9, mots 9–10 | fRos.45, mots 1–2 | 0/18 et 0/10 |

Les deux ordres inverses, `otoldy.otchdy` et `otoldy.oteedy`, ont chacun zéro occurrence dans les trois cas et les deux conventions d'espacement. Le premier signe litigieux suffit donc à faire disparaître tout le rapprochement exact entre ces deux groupes successifs. Le second groupe `otoldy` reste partagé dans les deux lectures.

**Qui a effectivement écrit quoi dans sa transcription ?** ZL écrit `otchdy` en toutes lettres EVA. Le v101 natif de Glen Claston écrit `ok179` aux deux lieux. Deux étiquettes d'un seul mot dans ce même dépliant illustrent la distinction interne à son alphabet. À fRos.50, `otchdy` en ZL correspond à `ok189` chez Claston. À fRos.63, `oteedy` correspond à `okcc89`. La cible présente la même unité interne `1` qu'à .50 et une variante de la forme suivante (`7`/ `8`). Ces deux comparaisons soutiennent la lecture avec `ch`, sans constituer une table de conversion universelle entre les alphabets. Dans les huit éditions IVTFF du registre, seuls ZL, GC et les deux rendus dérivés RF couvrent fRos.45. Aucune n'y propose `ee`. Dans les données d'Alessandro Placa, les mots 31:1 et 31:2 sont `otchdy` et `otoldy`. Leur positionnement est son propre relevé et l'auteur précise que la couche textuelle du dépliant dérive de ZL3b. Elle ne constitue donc pas une troisième lecture indépendante de `ch`. L'alternative `ee` vient ici des lecteurs de l'image. [Relevés ZL/GC et témoins locaux](TEMOINS.json) · [Attribution des couches de Placa](https://github.com/alessandroplaca-uro/voynich-spatial-data#license-and-attribution)

Pour reproduire ce complément avec les fichiers du dépôt, exécuter `python3 variante_rosette.py` depuis ce dossier.
