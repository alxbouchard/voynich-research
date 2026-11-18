# Que portent les étiquettes des étoiles du Voynich ?

**Dans les 53 emplacements associés à une étoile sur f68r1 et f68r2, chaque étiquette lisible d’un seul mot a une forme différente.** H donne 52 mots distincts pour 52 étiquettes d’un seul mot. ZL en donne 51 pour 51. Une étiquette de deux mots est reconnue par les deux transcriptions et ZL signale une lecture alternative à un autre emplacement. La prédiction d’un même nom générique autonome répété dans la majorité des cas échoue sur chacun des deux panneaux. [Voir le dépliant à Yale](https://collections.library.yale.edu/catalog/2002046?child_oid=1006196)

| Groupe | Transcription | Emplacements | Étiquettes lisibles | Étiquettes d’un mot | Formes distinctes d’un mot | Fréquence maximale |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Étoiles, f68r1 | H / ZL | 29 / 29 | 29 / 29 | 29 / 29 | 29 / 29 | 1 / 1 |
| Étoiles, f68r2 | H / ZL | 24 / 24 | 24 / 23 | 23 / 22 | 23 / 22 | 1 / 1 |
| Étoiles, deux panneaux | H / ZL | 53 / 53 | 53 / 52 | 52 / 51 | 52 / 51 | 1 / 1 |
| Fragments végétaux, f99r | H / ZL | 29 / 29 | 29 / 25 | 27 / 24 | 25 / 23 | 2 / 2 |
| Fragments végétaux, f100r | H / ZL | 17 / 17 | 17 / 14 | 16 / 14 | 16 / 14 | 1 / 1 |
| Fragments végétaux, deux pages | H / ZL | 46 / 46 | 46 / 39 | 43 / 38 | 41 / 37 | 2 / 2 |

Dans H comme dans ZL, zéro forme autonome passe d’un panneau stellaire à l’autre, et zéro passe des étoiles aux étiquettes de fragments végétaux de ces deux pages. Le décompte retrouve néanmoins une répétition matérielle chez les témoins. H et ZL donnent `oky` à f99r.4 et f99r.24, respectivement près des fragments 70 et 84 dans le catalogue des images. Les deux groupes n’offrent aucune traduction pour cette forme. À f68r1.8 et f68r1.9, deux emplacements stellaires successifs, H et ZL s’accordent sur deux formes différentes, `okodaly` et `odchecthy`. Les points indiquent un numéro de locus. [Fac-similé de f99r](https://collections.library.yale.edu/catalog/2002046?child_oid=1006246) · [Inventaire des fragments](https://www.voynich.nu/q19/index.html#f99r)

Avec douze étiquettes choisies par classe selon leurs positions, H donne onze formes distinctes pour onze étiquettes stellaires d’un seul mot et ZL dix pour dix. Les témoins donnent respectivement douze pour douze et dix pour dix. Aucune forme ne se répète entre classes. Les numéros de loci du sous-échantillon ont été calculés avant toute exclusion.

| Page | Six loci du sous-échantillon |
| --- | --- |
| f68r1 | 8, 13, 19, 24, 30, 36 |
| f68r2 | 7, 11, 16, 20, 25, 30 |
| f99r | 2, 8, 14, 24, 35, 46 |
| f100r | 1, 4, 7, 10, 17, 21 |

## Vérification matérielle et limites

Sur le cliché Yale, les deux panneaux sélectionnés se trouvent à gauche et au milieu du dépliant. De petites étoiles à rayons sont suivies ou flanquées de courtes inscriptions. Plusieurs étoiles périphériques du panneau central sont dépourvues de légende. Les textes autour du Soleil et de la Lune et le troisième panneau ont été écartés. Sur f99r et f100r, des inscriptions courtes apparaissent parmi les dessins de végétaux. Les rangées sont séparées par du texte suivi et accompagnées de récipients. Les codes `Ls` et `Lf` permettent de sélectionner le même genre de pièce écrite dans les deux sections. Les deux lignes f99r.6–7 sont rattachées au même fragment numéroté 72 dans ZL. D’où 29 emplacements végétaux sur f99r pour 30 lignes de transcription. Sur ces pages, « fragment végétal » couvre des feuilles, des racines et des parties composites. [Cliché des étoiles](https://collections.library.yale.edu/iiif/2/1006196/full/1350,/0/default.jpg) · [Cliché de f99r](https://collections.library.yale.edu/iiif/2/1006246/full/1350,/0/default.jpg) · [Cliché de f100r](https://collections.library.yale.edu/iiif/2/1006248/full/1350,/0/default.jpg) · [Définition des codes, IVTFF, tableaux 8 et 9](https://www.voynich.nu/software/ivtt/IVTFF_format.pdf#page=22)

Parmi les 52 emplacements stellaires entièrement lisibles dans les deux transcriptions, 40 ont la même lecture complète. Chez les végétaux, cet accord porte sur 34 des 39 emplacements comparables. La conclusion sur l’absence de répétition stellaire se retrouve dans chaque transcription. Les deux panneaux appartiennent au même dépliant. Les témoins proviennent de la main 1 et les étoiles de la main 4 selon le classement de Davis rapporté dans les notices des cahiers. Le résultat concerne les mots entiers inscrits à côté de ces dessins. Les noms propres, les variantes de forme, un élément plus court signifiant « étoile », les emplois en prose et les autres images du manuscrit constituent d’autres hypothèses. [Description du cahier astronomique](https://www.voynich.nu/q09/index.html#f68r1) · [Description du cahier pharmaceutique](https://www.voynich.nu/q19/index.html#f99r)

## Reproduction

Exécuter `python3 compter.py` dans ce dossier. Le script relit les 100 lignes brutes de `sources.tsv`, les regroupe en 99 étiquettes, vérifie le nombre d’emplacements de chacune des quatre pages et régénère `resultats.json`. Ce fichier contient les fréquences de toutes les formes, les lectures comparables et les identifiants retenus. Les lectures alternatives et les espaces incertains restent consultables dans `sources.tsv`. Les graphèmes étendus codés `@nnn;` de ZL gardent leur identité. Les marqueurs d’alignement `!` de H sont ignorés conformément à la documentation IVTFF.

Pour recréer l’extrait à partir des fichiers complets, passer `--extract CHEMIN/LSI_ivtff_0d_original.txt CHEMIN/ZL.txt`. Le script vérifie leurs empreintes SHA-256, puis extrait uniquement les lignes signées `;H` du premier fichier et les lignes correspondantes du second. Le fichier `PREREGISTRATION.md` a été figé avant la lecture des chaînes de ces pages, avec l’empreinte `e909ea0801e226b562c738b9b14dd19536576d28e5043008a08c8a000ef56082`. Il s’agit d’une consignation locale, sans horodatage par un tiers.
