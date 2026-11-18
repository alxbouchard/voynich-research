# Après chedy, trouve-t-on qokeey plus souvent que prévu ?

**Les trois transcriptions confirment la paire sur deux autres feuillets, f111v et f116r. Sa fréquence après `chedy` ne dépasse pas de façon statistiquement convaincante celle attendue sur des pages et à des positions comparables.** Le lot principal, tenu hors de l’apprentissage des triplets précédents, compte zéro succès sur onze annonces vérifiables. Le lot complémentaire en compte deux sur 72, pour 0,975 attendu au hasard. Ces lectures désignent uniquement des suites de signes.

## Ce qui a été annoncé

La règle annonce le groupe entier `qokeey` chez Takahashi et Zandbergen–Landini, `4ohC9` chez Claston, immédiatement après `chedy` / `1c89`, sur la même ligne. Les cinq feuillets où la paire était apparue dans l’étude qui a motivé ce test sont exclus en entier (81, 82, 103, 112 et 113). Le [protocole](PROTOCOLE.md) figure au commit `0cea07f`, les programmes au commit `c68173f`, et les [96 positions annoncées](ANNONCES.json) au commit `92d8218`, avant l’ouverture des successeurs. Le programme d’annonce ne recevait que les emplacements. Le projet avait déjà travaillé sur ces transcriptions publiques.

| Lot, emplacement et rang du successeur (base 1) | Takahashi (IT) | Zandbergen–Landini (ZL) | Claston (GC, v101) | Vérification |
|---|---|---|---|---|
| Principal, f26v.3, groupe 10, exemple annoncé avant ouverture | `ytedy` | `ytedy` | `9kc89` | Échec |
| Complément, f111v.5, groupe 7 | `qokeey` | `qokeey` | `4ohC9` | Succès |
| Complément, f116r.8, groupe 4 | `qokeey` | `qokeey` | `4ohC9` | Succès |
| Complément, f111r.30, groupe 10 | `qokeey` | `qokeey` | `4ohcc9` | Indéterminé pour l’égalité stricte dans les trois relevés |

La forme `4ohcc9` figure telle quelle chez Claston. Le protocole annonçait `4ohC9` et respectait la casse. Considérer ces deux graphies comme équivalentes demanderait une justification distincte. [Détail des trois lectures à chaque emplacement](RESULTATS.json) · [Origine des transcriptions](https://www.voynich.nu/transcr.html)

## Résultats et comparaison au hasard

| Lot | Annonces | Vérifiables | Succès | Échecs | Indéterminées | Succès attendus par face et place dans la ligne | Probabilité unilatérale d’en obtenir au moins autant |
|---|---:|---:|---:|---:|---:|---:|---:|
| Principal | 11 | 11 | 0 | 11 | 0 | 0,184 | 1,000 |
| Complément | 85 | 72 | 2 | 70 | 13 | 0,975 | 0,255 |

Les 11 annonces du lot principal sont réparties sur quatre des 22 feuillets retenus. Aucune des trois éditions ne donne la forme annoncée à ces emplacements. La cible est rare dans les pages concernées. Même sous le modèle de hasard, la probabilité d’observer **zéro** succès est de **82,8 %**. Un résultat nul sur onze annonces a donc peu de capacité à écarter un effet modeste.

Dans le complément, les 85 annonces concernent 21 des 69 feuillets retenus. Le score de 2/72 (2,78 %) est environ le double de l’espérance conditionnelle. Cependant, une répartition au hasard à l’intérieur des mêmes faces, en conservant les fréquences et la distinction entre fin et intérieur de ligne, atteint au moins deux succès dans **25,5 %** des cas. Le seuil de 5 % fixé à l’avance pour le lot principal n’est pas atteint dans ce complément non plus. Treize annonces restent indéterminées. Le détail par relevé est de 3 lectures conformes sur 81 disponibles pour IT, 3 sur 77 pour ZL et 2 sur 78 pour GC. Les dénominateurs diffèrent et ces lectures concernent le même manuscrit.

Le contrôle plus local redistribue les cibles dans chaque ligne à place comparable. Il donne 0,286 succès attendu dans le lot principal (probabilité unilatérale 1) et 1,013 dans le complément (probabilité 0,268). Les positions déjà occupées par `chedy` restent fixes dans les deux calculs. Les lois de hasard sont calculées exactement. Une deuxième implémentation fondée sur SciPy a retrouvé les quatre probabilités à moins de 10⁻¹² près. Un autre agent du projet a relu les trois fichiers IVTFF avec son propre programme et retrouvé les 96 positions et leurs résultats. Le rejeu dans un dossier temporaire a reproduit à l’octet les annonces, les résultats et le bilan d’extraction. Ces vérifications portent sur les mêmes transcriptions.

## Portée et reproduction

L’extraction porte sur les lignes P0 de prose avec rangs localement alignables et lectures retenues dans trois relevés. Une séparation incertaine neutralise une zone de la ligne. Une interruption par un dessin ou un nombre de champs différent peut écarter la ligne entière. Les fins de ligne ne fournissent aucun successeur (une ancre en lot principal, sept en complément). Ces critères limitent la portée du test. Le lot complémentaire a déjà contribué à l’apprentissage de l’étude qui a suggéré la paire. [Périmètre et empreintes des sources](EXTRACTION.json)

Depuis le dossier de ce rapport, avec Python 3 et les fichiers des deux transcriptions EVA inclus au dépôt. Le fichier v101 utilisé a pour SHA-256 `b09570cb6c993bc2d87134d115e60a978650a8a6495483ddbb1f6005a586096f`.

```sh
atelier=$(mktemp -d)
curl -fsSL https://www.voynich.nu/data/GC2a-n.txt -o "$atelier/GC2a-n.txt"
python3 -B emplacements.py ../../voynich_20261028/data/IT2a-n.txt ../../voynich_20261028/data/ZL3b-n.txt "$atelier/GC2a-n.txt" "$atelier"
python3 -B annoncer.py "$atelier/ancres.json" "$atelier/annonces.json"
python3 -B noter.py "$atelier/annonces.json" 5fd3bb5f6ff63236a78d62abb1220137e11ef85bd2a8e30ee49485cb14fa462a "$atelier/lignes.json" "$atelier/resultats.json"
cmp "$atelier/annonces.json" ANNONCES.json
cmp "$atelier/resultats.json" RESULTATS.json
cmp "$atelier/extraction.json" EXTRACTION.json
```
