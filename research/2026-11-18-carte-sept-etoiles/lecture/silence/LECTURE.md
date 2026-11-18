# Un seul signe muet dans les deux noms de mansions

**Aucune table commune ne restitue les deux noms**, même en autorisant un signe à ne rien produire dans toute la paire. Dans chaque transcription, tous les signes présents ont été essayés à tour de rôle comme signe muet. Les autres signes pouvaient produire une suite non vide de lettres de longueur quelconque. L’ordre et la graphie des noms restent ceux de leur propre témoin. [Formes historiques, transcriptions et sources](../LECTURE.md) · [Protocole enregistré avant calcul](01-regles.json)

| Paire attendue | Choix de lecture, de sens, d’unité et de signe muet | Choix où chaque nom admet au moins une table isolée | Paires de tables isolées à comparer | Tables communes |
|---|---:|---:|---:|---:|
| `açoraya` et `addauaran` | 172 | 39 | 9 662 | 0 |
| `Athoraye` et `Aldebaran` | 172 | 21 | 12 754 | 0 |

Dans 60 configurations, il est donc possible d’expliquer les deux noms séparément. Dès qu’on exige la même valeur pour chaque signe partagé, les 22 416 appariements de tables isolées échouent. Ces nombres incluent les variantes documentaires ou méthodologiques répétées. Deux calculs ont donné les mêmes nombres de tables communes dans chacune des 344 configurations. Le premier prolonge la table du premier nom sur le second. Le second découpe indépendamment chaque cible puis vérifie l’égalité des valeurs communes. Un contrôle artificiel avec `ch` muet récupère la table `ch→∅, d→a`. [Résultats détaillés](resultats.json) · [Code](verifier.py)

Le transfert prévu demandait une table commune à figer avant de lire l’autre partie du dépliant. Cette condition n’a été remplie dans aucune des deux traditions. **Les quatre disques et les légendes stellaires témoins n’ont donc pas été testés.** Aucun taux de couverture ni de confusion Soleil/Lune n’est calculable. L’inventaire fixé comportait six loci sur quatre disques, en IT2a et ZL3b, avec les seules cibles `sol` et `luna`, toutes deux attestées p. 219 de l’édition castillane. Aucun nom n’a été inféré pour le trait. [Inventaire des disques](../../../2026-11-18-sept-astres/sources/LUMINAIRES.md) · [Témoin castillan, p. 219](https://www.e-rara.ch/download/pdf/698074.pdf#page=8)

Empreinte SHA-256 des règles communiquée avant calcul `43228b5b6a717c776d9d34b00cbe9e0e2685eacefc3a2fd9aa204356522338b1`. Pour reproduire le résultat depuis ce répertoire, exécuter `python3 verifier.py`.
