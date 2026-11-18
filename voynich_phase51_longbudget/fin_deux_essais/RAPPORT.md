# Phase 51 en pause après les deux entraînements engagés

Les essais 51001 et 51002 ont chacun enregistré leur modèle final après **3 000 étapes**. Les deux évaluations avant et après entraînement sont disponibles pour chaque essai. Les fichiers ont été relus et leurs empreintes vérifiées sur la copie durable. [Bilan des essais et empreintes](STATUS.json)

| Essai | Entraînement natif | Première difficulté d’export | Prédictions vérifiées après correction |
| --- | --- | --- | --- |
| 51001 | 3 000 étapes en 6 010 s | État final | Avant et après entraînement sur les 46 séquences d’apprentissage et les 16 réservées |
| 51002 | 3 000 étapes en 6 010 s | État initial | Avant et après entraînement sur les 46 séquences d’apprentissage et les 16 réservées |

La phase compare des formes gothiques à un lexique vieil-islandais. Les deux pilotes d’origine ont quitté avec une erreur de sérialisation des indices entiers NumPy. Leurs journaux et statuts d’échec ont été conservés. Une copie distincte du programme, limitée à l’inférence, convertit les deux bornes des segments en entiers Python. Elle a relu les modèles initiaux et finaux enregistrés. Le modèle, les données, les limites de temps et les paramètres de calcul proviennent des essais gelés. [Modification exacte](../../docs/PIECES_REFERENCES.md#piece-5eea98a8297afd) · [Reçu de la correction](export_recovery_two/EXPORT_EDITION.json)

Les huit fichiers de prédictions ont été vérifiés sur l’identité du modèle chargé, les séquences attendues, les positions des segments et le vocabulaire autorisé. Les deux fichiers initiaux précédemment produits avec succès et les trois matrices déjà disponibles sont identiques octet pour octet après le nouvel export. Les exemples réservés portent sur 31 formes réunies en 16 séquences.

Les trois autres essais (51003, 51004, 51005) sont restés en attente. Le critère scientifique fixé exige cinq essais. Son score global et ses tests par permutation restent indéterminés. Le manuscrit Voynich n’entre pas dans cette calibration.

À la demande d’Alex, l’ordonnanceur et son superviseur ont été arrêtés après la vérification des fichiers. La liste des processus a été relue et les trois essais en attente ne possèdent aucun dossier d’exécution. Les modèles natifs, y compris les états initiaux et finaux, restent dans la copie durable. [État de pause vérifié](PAUSE_APRES_DEUX.json)
