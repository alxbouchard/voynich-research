# Deux légendes de plantes permettent-elles de lire la troisième ?

Les deux premières inscriptions de f89r2 autorisent une substitution qui donne deux titres latins successifs du *Macer*. Tous les signes de la troisième inscription sont déjà dans la clé. Ils donnent **thpiu**. La suite de titres annonçait **aloë**. C’est un cas où le parchemin permet de trancher entre une lecture prometteuse et une coïncidence. [Photographie des trois dessins](photos/LECTURE.md) · [Prédictions déposées](PREDICTIONS.json.gz) · [Résultats par bloc](VERIFICATION.json.gz)

## Constituer les séries

Les répertoires de départ contiennent 77 titres latins du *Macer* dans l’ordre de l’édition de calcul, 53 rubriques de plantes **illustrées** recensées dans l’herbier des Carrara et 108 rubriques latines du *Gart der Gesundheit*. Ce dernier est représenté par cinq séries continues, I–XII, 42–65, 84–107, 128–151 et 171–194. Les 75, 51 et 98 fenêtres de trois entrées respectent ces limites. Les noms de plusieurs mots restent dans leur série. Une telle entrée ne peut servir d’amorce d’un seul mot. Les noms des Carrara sont extraits de la compilation de Sarah R. Kyle publiée dans le catalogue de la British Library, avec retrait des articles et prépositions introductifs et des accents pour le calcul. La notice crédite cette compilation. [Macer et provenance de sa transcription](../../2026-11-18-opcheor-paralleles/latin/SOURCE.md) · [Herbier des Carrara et crédits du catalogue](https://searcharchives.bl.uk/catalog/032-001982947) · [53 entrées avec leur folio](CARRARA.json) · [Les 96 nouvelles rubriques du Gart](../temoin/NOMS.json)

Les cahiers 15 et 19 donnent 63 blocs physiques de trois dessins successifs. Nous avons gardé les cases sans légende dans le décompte. Dans 16 blocs, les deux premières légendes donnent chacune un mot unique, identique en transcription Takahashi et Zandbergen–Landini sous les deux traitements des blancs incertains. Dans 12 blocs répartis sur neuf panneaux, la troisième légende répond au même critère. Dix de ces triples ont un ordre documenté et deux des attaches discutées. Les prédictions se fondent sur les deux premières inscriptions et l’ordre des répertoires. Les troisièmes mots ne sont fournis qu’au programme de vérification. Plusieurs pages avaient déjà été étudiées dans le projet. [Inventaire des rangées](../panneaux/GEOMETRIE.md) · [Protocole](PROTOCOLE.md)

| Lettres possibles par signe | Blocs avec une amorce compatible | Tables compatibles sur deux noms | Blocs avec troisième mot évaluable et nom prédit simple | Tables évaluables | Blocs avec initiale prédite et observée | Troisièmes noms compatibles en entier |
|---|---:|---:|---:|---:|---:|---:|
| 1, substitution injective | 2 | 2 | 1 | 1 | 0 | 0 |
| 1–2, homophones permis | 5 | 149 | 4 | 148 | 2 | 0 |
| 1–3, homophones permis | 7 | 1 007 | 5 | 965 | 3 | 0 |

L’extension d’une clé est permise au troisième mot seulement pour un signe jamais rencontré dans l’amorce. Même avec cette latitude, aucun troisième nom attendu ne convient. Aucun autre nom simple du répertoire correspondant ne convient non plus dans ces comparaisons. Les centaines de clés issues d’un même couple ne fournissent pas des observations indépendantes. Une seconde implémentation par expressions régulières vérifie les positions admissibles des amorces et des triples pour les 16 blocs et trois largeurs. [Recherche des tables](comparer.py) · [Vérification indépendante](verifier_independant.py)

## Les deux prédictions à une lettre par signe

**f89r2, fragments 40–42.** Les inscriptions `sodar` et `cheys` peuvent représenter *spica* et *thus*, titres 75 et 76 dans l’édition de calcul du *Macer*. La suite demande *aloë*. Seul le premier signe, `r` pour a, pouvait être annoncé par cette clé. La légende photographiée est `cheody`. On peut appliquer les valeurs sans compléter la clé et lire successivement t, h, p, i, u. Cinq anciennes transcriptions concordent à cet emplacement. Le dessin montre une partie ocre renflée prolongée de traits minces. Son espèce demeure indéterminée. [Image du dépliant de Yale](https://collections.library.yale.edu/catalog/2002046?child_oid=1006233) · [Inscriptions et attributions sur le fac-similé](photos/LECTURE.md)

**f88v, fragments 13–15.** Les inscriptions `cheocthy` et `cpheor` autorisent *viola* et *bióm* dans la liste des plantes illustrées des Carrara. La clé suffit ici à annoncer **tout** le nom suivant, *molóm* (melon), sous la forme EVA `rocthor`, en cinq unités. La troisième inscription porte deux groupes, `otar arody`. Quatre lectures anciennes s'accordent sur le premier groupe et sur la séparation. Aucun des deux groupes ne peut représenter *molom* avec les valeurs apprises. La rubrique italienne complète *Del molom* échoue également, même avec une nouvelle clé et des espaces fixes. Le groupe `otar` contient déjà quatre unités pour les trois lettres de *del*. Une clé assouplie, entièrement neuve, permettrait de fabriquer le nom isolé dans chacun des deux groupes. Ces nouvelles clés perdent les valeurs qui avaient fourni les deux premiers noms. [Les deux légendes sur la photo](photos/LECTURE.md) · [Calcul avec et sans article](COPIE-1478.json.gz)

À Padoue, l’herbier des Carrara porte bien *Del biom* au recto et *Del molom* au verso du feuillet 161, où la plante rampante porte des fruits côtelés. La violette précédente du catalogue est au f. 94r. Deux notices textuelles intermédiaires sont directement visibles sur les deux faces suivantes, un arbre nommé *dulb* puis l’endive. La suite de trois du catalogue décrit donc l’ordre de certaines illustrations. Elle n’établit pas la succession de trois notices. [Photographies des rubriques, plantes et notices intermédiaires](carrara/LECTURE.md)

## D’une copie du Macer à l’autre

Dans la table de la copie italienne datée de 1478, l’aloès est au rang 43 entre *Bacchara* et *Verbena*. La table finit par *Spica nardi*, *Spica celtica*, *Incenso*. La place qui avait rendu possible la prédiction du premier essai dépendait de l’édition. Au début, en revanche, le témoin de 1478 et le *Gart* ont trois noms correspondants dans le même ordre, l’armoise, l’aurone et l’absinthe, avec des graphies différentes. Au quatrième rang, l’un porte *Urtica* et l’autre *Allium*. [Quatre colonnes de la table de 1478](macer1478/LECTURE.md) · [Premiers titres du Gart](../../2026-11-18-bax/etalonnage/TITRES.json)

Un agent a transcrit les 77 entrées photographiées de la table. Une lecture incertaine au rang 13 interrompt les fenêtres de comparaison. La notice Wellcome décrit 78 chapitres du corps et la table ne consacre qu’une ligne aux hellébores. Le calcul conserve les formes fléchies et les titres composés. Sur le Voynich, aucune amorce ne convient à une lettre par signe. Avec une à deux lettres on obtient 43 tables sur trois blocs, dont 31 évaluables sur deux blocs. Avec une à trois lettres on en obtient 601 sur cinq blocs, dont 556 évaluables sur quatre. Aucun troisième nom complet ne convient dans ces conditions. Les troisièmes légendes étaient déjà connues lors de cette extension rétrospective. [Relevé avec colonnes, rangs et réserves](macer1478/RUBRIQUES.json) · [Règles du contrôle](COPIE-1478.md) · [Résultats et pronostics reconstruits](COPIE-1478.json.gz)

## Ce que l’on peut réellement récupérer avec une clé inconnue

Nous avons chiffré 52 triples disjoints avec une même substitution injective et recherché leurs deux premiers noms dans les trois répertoires. Aucune position, clé ni identité de livre n’était fournie à la fonction de recherche. La source correcte était toujours dans la bibliothèque. Dans les **52 cas**, un seul nom suivant est prédit. Dans **5 cas**, tous les signes du troisième nom étaient déjà lisibles avec les seules valeurs apprises. Ainsi *eruca*, puis *papaver*, permettent de lire entièrement *cepa*. Pour *artemisia*, puis *abrotanum*, la suite du livre prédit *absinthium*, mais la clé seule donne `absint?ium`. La corruption d’un seul signe initial du troisième nom fait échouer les 52 essais. [Étalon et prédictions](ETALON-PROTOCOLE.md) · [Chaque mot réellement lu](ETALON.json)

Enfin, les deux clés strictes provenant des légendes du cahier 15 ont servi sans retouche sur les 89 légendes d’un mot concordantes du cahier 19. Cinq noms nouveaux de la bibliothèque pouvaient être écrits avec ces clés, *oliva*, *molom*, *catapucia*, *cicuta* et *cuscuta*. Aucun n’apparaît. Avec les mêmes signes disponibles, toutes les permutations des valeurs ont aussi obtenu zéro. Ce contrôle a donc trop peu de pouvoir pour classer les clés. [Noms et signes déposés avant le contrôle](NOMS-PREDITS.json) · [Lieux effectivement déchiffrables et permutations](NOMS-TRANSFERT.json)

## Reproduction

Les commandes suivantes s’exécutent depuis ce dossier. Les données d’entrée et les transcriptions historiques sont archivées dans le dépôt. Les photographies et leurs repères ont des liens vers les fac-similés institutionnels. La commande facultative `python3 -B carrara.py catalogue.html` reconstruit la liste des illustrations à partir d’une copie HTML de la notice Egerton MS 2020.

```sh
python3 -B comparer.py predire
python3 -B comparer.py verifier
python3 -B verifier_independant.py
python3 -B etalon.py predire
python3 -B etalon.py verifier
python3 -B transfert_noms.py predire
python3 -B transfert_noms.py verifier
python3 -B copie1478.py
```
