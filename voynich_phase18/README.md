# Phase 18 — clés selon la position dans le mot

Deux permutations de l'alphabet : une table pour la première lettre **ou** la
dernière lettre de chaque mot, une autre pour le reste. Les deux familles sont
testées séparément. Aucune valeur phonétique n'est attribuée aux caractères EVA.

Le [protocole figé](PROTOCOL.json) précède les optimisations de cette phase.
Le [brouillon historique](PROTOCOL_DRAFT.md) reste conservé sans modification.
Les résultats et leur interprétation figurent dans le [rapport](RAPPORT.md).
Aucune sortie de solveur n'est présentée comme une traduction.

## Reproduire

Depuis la racine du dépôt, avec Python, NumPy et un compilateur C++17 :

```sh
python3 tools/hydrate.py
python3 voynich_phase18/src/experiment.py prepare
python3 -m unittest discover -s voynich_phase18/src -p 'test_*.py' -v
python3 voynich_phase18/src/experiment.py controls --workers 4
python3 voynich_phase18/src/experiment.py real --workers 4
python3 voynich_phase18/src/verify.py
```

La préparation reconstruit les modèles de langue à partir des textes déjà
archivés en phase 10. Elle n'accède pas au réseau. Les phases 1 à 17 restent
en lecture seule. Les fichiers compilés et les matrices sont placés dans `tmp/`.

Les résultats existants sont réutilisés **uniquement** si les empreintes du
protocole, du solveur, du script, du modèle et des entrées correspondent. Un
résultat différent n'est pas écrasé silencieusement. Pour réexécuter toutes les
optimisations, travailler dans une nouvelle copie, déplacer son dossier
`voynich_phase18/results/` vers une archive, puis relancer les étapes. Le seul
appel à `verify.py` vérifie les clés enregistrées ; il ne réoptimise pas.
Les parcours heuristiques peuvent varier avec le compilateur et les arrondis.

L'inventaire de cette nouvelle phase est distinct de celui des phases 1 à 17.
Avant de régénérer des résultats, contrôler les octets archivés avec
`python3 voynich_phase18/src/manifest.py`. Il couvre aussi le rapport et les
figures ; les fichiers régénérables de `tmp/` en sont exclus.

Pour reconstruire le rapport et la figure, installer aussi Matplotlib :

```sh
MPLCONFIGDIR=/tmp/voynich-matplotlib python3 voynich_phase18/src/report.py
```

## Mesures et limites

- Contrôles : quatre clés par langue et par famille, soit seize essais sur
  **deux textes**. Le texte clair et les clés exactes ne sont jamais transmis
  au solveur. Seuils : 99 % de lettres réservées, 98 % aux positions concernées,
  99,5 % de couverture par les signes vus en apprentissage.
- Voynich : ZL/IT et groupes Currier A/B séparés ; recto et verso d'un feuillet
  physique restent ensemble. Les pages réservées ont déjà été examinées dans
  le projet antérieur. Les 24 000 premières lettres admissibles plafonnent
  l'apprentissage ; ce choix ne rend pas l'échantillon représentatif de toutes
  les sections, mains ou cahiers.
- Témoins : dix-neuf mélanges pour chaque groupe ZL et chaque langue. Les
  lettres sont permutées par feuillet et rôle (initiale, intérieure, finale,
  mot d'une lettre). Longueurs, lignes, incertitudes et fréquences par rôle
  restent fixes. Chaque témoin est réajusté ; les deux familles et langues
  utilisent les mêmes mélanges. IT est une sensibilité sur le même manuscrit.
  Les comptes par rôle sont fixes avant exclusion des segments courts ; un
  petit écart après exclusion est mesuré et expliqué dans le rapport.
- Score : bits moyens par fenêtre de quatre caractères, espaces compris.
  Un gain positif signifie un meilleur score que la permutation unique.
  Ce n'est ni un pourcentage de traduction ni une entropie par lettre.
- Un gain au-delà des mélanges montre au plus une organisation séquentielle.
  Il n'identifie ni une langue ni un message. Ce témoin ne reproduit pas
  toute la structure d'un texte naturel ou d'un générateur sans message.
- Les erreurs des contrôles et les signes absents de l'apprentissage restent
  dans les dénominateurs. Les espaces et les segments de moins de quatre
  caractères sont exclus de l'exactitude ; leurs règles sont identiques pour
  les deux modèles. Les inconnues interrompent tout calcul de voisinage.

## Traçabilité

- `data/environment.json` : versions et empreintes de l'exécutable/modèles.
- `data/split.json` : feuillets d'apprentissage et de test.
- `data/*_truth.json` : clés synthétiques, réservées à l'évaluation.
- `results/controls_summary.json` : exactitudes et passage des seuils.
- `results/real_summary.json` : scores observés et tous les témoins.
- `results/*_{single,initial,final}.json` : clés, objectifs de chaque redémarrage,
  couverture et sorties intégrales `NOT_TRANSLATION`.
- `results/verification.json` : recalcul distinct du décodage, des scores et
  des exactitudes. Il partage les données et les modèles ; ce n'est pas une
  réplication par un autre chercheur.

Le solveur dérive de `voynich_phase10/src/context_permutation.cpp`, avec une
allocation explicite des signes non observés et des contrôles d'entrée.
Les sources César, Dante, Pline et les transcriptions conservent les attributions
et droits indiqués dans [la phase 10](../voynich_phase10/README.txt) et
[NOTICE](../NOTICE.md). Aucun nouveau corpus ni image n'est acquis ici.
