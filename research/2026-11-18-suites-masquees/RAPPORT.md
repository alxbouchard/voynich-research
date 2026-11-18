# Peut-on compléter sur un autre feuillet une suite de trois groupes qui se répète ?

La suite `chol daiin chkaiin` figure aux feuillets **f21r.12** et **f28v.5** dans les deux transcriptions EVA. Avant d’ouvrir le cinquième groupe de **f20v.10**, nous y avons annoncé `chkaiin` après `chol daiin`. Les deux transcripteurs donnent **`chy`**. Sur une autre page, f100r.25, le même début mène à `ctheol`. Le début est reconnaissable et la suite varie.

## Les suites trouvées dans l’apprentissage

Sur 73 feuillets d’apprentissage (1 268 lignes retenues), les transcriptions EVA de Takahashi et Zandbergen–Landini concordent sur 6 170 suites distinctes de trois groupes dans le périmètre retenu. **Onze** de ces suites sont attestées sur au moins deux feuillets numérotés différents. En exigeant aussi les mêmes groupes en v101 chez Claston aux positions correspondantes, il subsiste **deux** suites répétées sur les 3 712 suites distinctes de ce sous-ensemble. [Catalogue complet des répétitions et de leurs emplacements](REPETITIONS.json)

| Suite vérifiée dans les deux notations | v101 | Feuillets et positions de départ (base 1) |
|---|---|---|
| `qoky shedy qokaiin` | `4oh9 2c89 4oham` | f82v.29, groupe 3 et f103v.6, groupe 7 |
| `sheey qokol cheol` | `2C9 4ohoe 1coe` | f86v6.9, groupe 4 et f89v1.6, groupe 2 |

## Les quatre prévisions enregistrées

Le [protocole](PROTOCOLE.md) a été fixé au commit `f3bdd2c`, les trois programmes au commit `67644ad`. Le commit `6c7b221` conserve les [annonces avant la comparaison](ANNONCES.json). Chaque réponse proposée était appuyée par la suite complète sur deux feuillets d’apprentissage distincts. Le tableau est ordonné par numéro de feuillet. Les crochets indiquent la case qui a été cachée.

| Lieu et rang (base 1) | Contexte visible | Annonce en EVA | Groupe effectivement lu dans les deux transcriptions EVA |
|---|---|---|---|
| f20v.10, groupe 5 | `chol daiin [ ]` | `chkaiin` | `chy` |
| f83v.2, groupe 1 | `[ ] shedy qokedy` | `ol` | `dol` |
| f83v.5, groupe 3 | `shedy [ ] chedy` | `qokaiin` | `qotain` |
| f100r.25, groupe 5 | `chol daiin [ ]` | `chkaiin` | `ctheol` |

Ces rapprochements n’avaient droit qu’à une réponse entière par case. La ressemblance entre `ol` et `dol` ne compte donc pas comme un succès partiel. Les écritures v101 vérifiées aux quatre emplacements, dans l’ordre du tableau, sont `19`, `8oe`, `4okan` et `Kcoe`. Le modèle croisé n’avait annoncé aucune de ces réponses.

## Couverture et témoins

La réserve contient 208 lignes sur 15 feuillets numérotés. Sur les 317 cases masquées sans consulter leur contenu, 295 étaient lisibles en accord entre IT et ZL et 221 satisfaisaient aussi les critères du relevé GC. La règle EVA a proposé quatre réponses sur trois feuillets et s’est abstenue sur les 291 autres cases lisibles. **Les quatre réponses étaient fausses.** Écrire systématiquement le groupe le plus fréquent de l’apprentissage, `daiin`, donne également zéro sur ces quatre emplacements.

Le test croisé s’est abstenu sur chacune des 221 cases lisibles. Aucun des contextes visibles autour d’une case masquée n’a permis de proposer l’une des deux suites selon les critères fixés. Cette absence d’annonce ne donne pas de taux de succès pour le modèle croisé.

La comparaison directe des trois fichiers a confirmé les quatre réponses et les deux suites du tableau. Elle a aussi révélé une limite du filtre de ligne entière. Chez Claston, les groupes correspondant à `chol daiin chkaiin` sont `1oe 8am 1ham` aux deux emplacements d'apprentissage. Une virgule dans un autre groupe, tout à la fin de f28v.5, suffit à exclure cette ligne du premier calcul croisé. L'accord au niveau du passage justifie un [complément sur des lignes distinctes](PROTOCOLE-LOCAL.md).

Dans les 5 000 redistributions des réponses sur leur propre face et à la même place relative dans la ligne (début, intérieur ou fin), le score attendu et observé pour les quatre annonces EVA reste zéro. Les groupes annoncés étaient absents des réponses masquées disponibles dans les quatre ensembles de comparaison concernés. Ce témoin apporte peu d’information pour départager les méthodes sur un si petit nombre d’annonces. [Résultats et lectures à chaque emplacement](RESULTATS.json)

## Deuxième épreuve sur des passages localement concordants

Pour vérifier un passage où trois transcriptions se rejoignent même en présence d’un espace douteux plus loin dans la ligne, nous avons neutralisé la zone incertaine et gardé les parties alignables de chaque côté. Ce complément, décidé après le premier résultat, utilise **21 autres lignes**, sur huit des feuillets réservés. Les deux réserves ne partagent aucun identifiant de ligne. Le protocole a été fixé en `12e89e2`, le nouvel extracteur en `0f02665` et les [annonces locales](ANNONCES-LOCALES.json) en `390bcfc` avant ouverture. Les critères de répétition et de décision sont ceux du premier calcul.

Dans cette extraction, **cinq triplets distincts** se répètent sur plusieurs feuillets dans les deux alphabets. Une seule prédiction croisée était possible. En f113v.29, nous avons annoncé `qol` en EVA et `4oe` en v101 pour le premier groupe, précédant `chedy qokeey`. Les trois transcriptions ont permis de vérifier chaque passage directement.

| Passage | Rang du premier groupe | Takahashi et Zandbergen–Landini, en EVA | Claston, en v101 |
|---|---:|---|---|
| f81r.20, apprentissage | 2 | `qol chedy qokeey` | `4oe 1c89 4ohC9` |
| f82r.21, apprentissage | 7 | `qol chedy qokeey` | `4oe 1c89 4ohC9` |
| f113v.29, vérification | 1 | **`ykeeol`** `chedy qokeey` | **`9hCoe`** `1c89 4ohC9` |

La paire finale est bien conservée sur la troisième page. Le groupe masqué diffère dans les deux alphabets. Parmi 38 cases masquées, 25 étaient vérifiables dans les trois relevés. La règle croisée a fait une erreur et s’est abstenue sur les 24 autres cases vérifiables. Le calcul EVA de ce complément a fait la même prédiction au même endroit. La réponse du témoin de fréquence et les 5 000 redistributions obtiennent également zéro succès pour l’annonce croisée. La comparaison dans un dossier neuf a retrouvé les quatre sorties de chaque épreuve à l’octet. [Résultats du complément](RESULTATS-LOCAUX.json) · [Répétitions et emplacements](REPETITIONS-LOCALES.json) · [Exclusions et couverture](EXTRACTION-LOCALE.json)

## Portée

Les feuillets d’apprentissage et de réserve sont disjoints pour ce calcul. Des pages ont été examinées pendant des travaux antérieurs, notamment `ctheol` sur f100r.25 lors de l’étude des plantes à baies. Le programme de prédiction recevait les seules données d’apprentissage et la réserve expurgée des cibles. Les trois relevés portent sur le même manuscrit. Les lignes dont les espaces sont incertains, les interruptions de dessin, les mots ambigus et de nombreux signes spéciaux de v101 réduisent la couverture. Le test mesure une règle de répétition exacte dans la prose sélectionnée. Il n’attribue aucun son, aucune fonction grammaticale et aucun sens aux groupes. [Périmètre de l’extraction](EXTRACTION.json) · [Étude antérieure sur f100r](../2026-11-18-opcheor-suite/RAPPORT.md)

## Reproduction

Depuis le dossier de ce rapport, avec Python 3. Les deux fichiers EVA figurent dans le dépôt. Les trois empreintes sources sont indiquées dans le protocole. Les résultats sont comparés dans un répertoire temporaire.

```sh
atelier=$(mktemp -d)
curl -fsSL https://www.voynich.nu/data/GC2a-n.txt -o "$atelier/GC2a-n.txt"
python3 -B preparer.py ../../voynich_20261028/data/IT2a-n.txt ../../voynich_20261028/data/ZL3b-n.txt "$atelier/GC2a-n.txt" "$atelier"
python3 -B predire.py "$atelier/train.json" "$atelier/reserve.json" "$atelier/annonces.json"
python3 -B verifier.py "$atelier/reserve.json" "$atelier/reponses.json" "$atelier/annonces.json" 66a1c629a92908e2fd95e21d512a3cef055c82f7f24e31bb94ad91541336ebf5 "$atelier/resultats.json"
python3 -B inventorier.py "$atelier/train.json" "$atelier/repetitions.json"
cmp "$atelier/annonces.json" ANNONCES.json
cmp "$atelier/resultats.json" RESULTATS.json
cmp "$atelier/repetitions.json" REPETITIONS.json
```

Pour la seconde épreuve, dans le même atelier, avec le fichier de réserve de la première.

```sh
second="$atelier/local"
python3 -B preparer_local.py ../../voynich_20261028/data/IT2a-n.txt ../../voynich_20261028/data/ZL3b-n.txt "$atelier/GC2a-n.txt" "$atelier/reserve.json" "$second"
python3 -B predire.py "$second/train.json" "$second/reserve.json" "$second/annonces.json"
python3 -B verifier.py "$second/reserve.json" "$second/reponses.json" "$second/annonces.json" 5bbed07f0618a6ec06709a5a2423f2e2f290b7ab39f98dae99f1094d680d0af3 "$second/resultats.json"
python3 -B inventorier.py "$second/train.json" "$second/repetitions.json"
cmp "$second/annonces.json" ANNONCES-LOCALES.json
cmp "$second/resultats.json" RESULTATS-LOCAUX.json
cmp "$second/repetitions.json" REPETITIONS-LOCALES.json
```
