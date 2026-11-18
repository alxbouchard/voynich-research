# Jusqu’où deux à quatre mots identiques permettent-ils de restituer le suivant ?

Dans la partie où les deux transcriptions du Voynich s’accordent sur toute la ligne, le procédé a proposé un mot à une seule des 368 positions masquées. Sa prévision à f9v.10 était `chaiin`. La ligne porte `kyty`. Les deux versions plus étendues ont chacune permis de retrouver un mot. Dans les deux cas, regarder le seul mot précédent suffisait à le prévoir également.

## L’épreuve principale à f9v.10

Le cinquième mot de la ligne avait été masqué. Son contexte était `oty kchol chol chy`. Trois feuillets d’apprentissage donnaient une suite après `chol chy`. Aux lignes f4r.3 et f47r.3 le quatrième mot est `chaiin`. À f28v.3, le quatrième mot est `choiin`. La procédure a choisi la forme la plus fréquente, `chaiin`, avant l’ouverture des réponses. Les deux transcriptions donnent la même ligne de réserve, `oty kchol chol chy kyty`.

Les loci et les quatre mots cibles correspondants ont été relus dans les fichiers IVTFF du dépôt. Les numéros de ligne du fichier ZL3b-n.txt sont 187 (f4r.3), 450 (f9v.10), 1179 (f28v.3) et 2018 (f47r.3). Dans IT2a-n.txt, ils sont respectivement 107, 267, 716 et 1237.

## Résultats sur les folios réservés

| Lecture | Positions masquées | Annonces | Mots retrouvés parmi les annonces | Bigramme exact sur les mêmes annonces | Mot global exact sur les mêmes annonces | Bigramme exact sur toutes les positions | Mot global exact sur toutes les positions |
|---|---:|---:|---:|---:|---:|---:|---:|
| Lignes en accord, test principal | 368 | 1 | 0/1 | 0/1 | 0/1 | 10/368 | 12/368 |
| ZL | 1 246 | 16 | 1/16 | 1/16 | 0/16 | 38/1 246 | 34/1 246 |
| IT | 1 337 | 9 | 1/9 | 1/9 | 0/9 | 38/1 337 | 25/1 337 |

En comptant les abstentions, le procédé à contexte long a ainsi restitué 0/368, 1/1 246 et 1/1 337 mots, respectivement. Toutes ses annonces portaient sur un contexte de deux mots. Aucune suite de trois ou quatre mots disponible à une position masquée ne remplissait les critères d’annonce. Sur les positions couvertes, les deux modèles ont obtenu exactement les mêmes succès et échecs dans chaque vue. Le test apparié unilatéral et son contrôle par folio donnent chacun p = 1 dans les trois vues. Une seule annonce dans l’épreuve principale laisse une grande incertitude sur la précision du procédé.

Les feuillets de réserve ont des numéros divisibles par trois. Le jeu principal comprend 699 lignes d’apprentissage et 368 positions masquées sur 33 folios. Six autres lignes des folios réservés ne comportaient aucune position recevable. Les lignes où un champ diffère entre éditions sont entièrement écartées de ce jeu. Cette sélection rend son dénominateur et sa couverture différents de ceux de chaque transcription prise isolément.

## Les deux restitutions observées

- En ZL, au quatrième mot de f78r.37, le contexte `ol s` a permis de retrouver `aiin`. La même suite `ol s aiin` s’observe au quatrième mot de f55v.10 et au dixième de f94v.9. Le contexte seul se retrouve avec une suite lisible sur trois folios d’apprentissage, dont deux donnant `aiin`. Une divergence de lecture plus loin à f78r.37 exclut toute cette ligne du jeu principal.
- En IT, au troisième mot de f78r.18, la méthode a retrouvé `qokain` après `ol chedy`. Ce contexte apparaît onze fois avec un mot suivant sur huit folios d’apprentissage. La continuation gagnante apparaît deux fois, sur les deux faces du folio physique 80, au sixième mot de f80r.16 et de f80v.31. L’admissibilité dépend du nombre de folios portant le contexte. La transcription ZL marque des coupures incertaines au début de f78r.18.

Les succès se trouvent sur le même feuillet physique et concernent deux lignes différentes. Ils constituent des observations sur les transcriptions EVA. Leur sens et leur fonction dans le manuscrit restent inconnus.

## Contrôles

Une grammaire artificielle détermine le mot correct selon le premier de deux mots, le second étant toujours identique. La formule restitue ses douze mots masqués, contre six pour le bigramme. Une fois les réponses de ce même test décalées d’une place, elle obtient zéro succès sur douze, contre six pour le bigramme. Cette calibration mesure la capacité à repérer une règle construite sans contenu linguistique.

Pour chacune des trois vues, 99 mélanges des mots à l’intérieur des passages lisibles de chaque ligne d’apprentissage conservent leur quantité et leurs fréquences. Les positions de réserve restent fixes et les modèles sont réappris à chaque fois. Le tableau donne les probabilités descriptives corrigées de un pour les mélanges donnant un résultat au moins aussi élevé que le corpus ordonné.

| Lecture | Annonces, observation et étendue sur les mélanges | p pour les annonces | Mots retrouvés, observation et étendue | p pour les succès | Gain observé contre bigramme | p pour le gain |
|---|---|---:|---|---:|---:|---:|
| Lignes en accord | 1, de 0 à 3 | 0,13 | 0, toujours 0 | 1,00 | 0 | 1,00 |
| ZL | 16, de 0 à 8 | 0,01 | 1, de 0 à 1 | 0,16 | 0 | 0,97 |
| IT | 9, de 0 à 10 | 0,03 | 1, de 0 à 1 | 0,19 | 0 | 0,93 |

L’ordre d’origine donne davantage d’occasions de proposer un mot dans chaque transcription étendue que dans la plupart des mélanges. Le nombre de mots retrouvés reste compatible avec ce contrôle. Plusieurs comparaisons sont présentées à titre descriptif et les deux transcriptions dépendent du même manuscrit.

Le fichier des prédictions annoncé avant le dévoilement porte l’empreinte SHA-256 `3b11e0fd2135762e4fe95662afd445527d81d4e4d175c8306b7f19432f2c1be3`. Le protocole, les prédictions, les résultats par vue, les exemples et les 297 réplications sont reproductibles avec `formules.py` et les commandes de `REPRODUCTION.md`.
