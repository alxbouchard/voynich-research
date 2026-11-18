# Préparation historique du banc

**Exécution désormais terminée : voir [rapport](RAPPORT.md). Le texte ci-dessous décrit le protocole avant lancement.**

Ce banc compare deux préfixes de la même configuration native : 1 puis 10 pas,
avec `num_steps=3000` et `num_anneal_steps=2000` inchangés. Il ne lit que le TSV
d'apprentissage, le lexique connu et les sources autorisées de phase 51. Aucune
réserve, annotation vraie ou métrique linguistique n'est utilisée.

Le candidat conserve les constructeurs, convolutions et dropout. Il détache
uniquement les deux tenseurs de contexte renvoyés par `_get_repr`. Un certificat
préalable doit établir que les quatre gradients natifs des convolutions sont
présents, finis et nuls sur les dix pas. Le candidat applique ensuite une règle
fixe de matérialisation des zéros avant clipping ; il ne lit pas les valeurs de
la trajectoire native pendant ses propres pas.

Les processus sont séparés et leurs états initiaux doivent coïncider exactement.
Aucun poids, état d'optimiseur ou RNG n'est resynchronisé après l'initialisation.
Les deux seules différences structurelles attendues sont les deux drapeaux
`requires_grad` des contextes et les quatre gradients `None` avant matérialisation.
Toutes les autres différences enregistrées font échouer l'équivalence, sans
tolérance. Cette preuve porterait sur les octets et métadonnées capturés, pas
sur l'identité de tous les objets Python ou du graphe autograd.

La préparation autorise uniquement une analyse syntaxique/AST. Après revue et
réservation effective d'un créneau, les commandes futures sont :

```sh
python3 run_pair.py --execute --seed 51001 --python chemin-local/python
python3 run_pair.py --execute --seed 51002 --python chemin-local/python
```

Elles sont indiquées ici, **elles n'ont pas été exécutées**. Garder au maximum
deux jobs de modèle, phase 51 comprise. Chaque `RUN.json` non terminal réserve
un créneau pendant toutes les étapes, même entre entraînement et inférence.
Un JSON incomplet ou manquant dans un dossier existant conserve la réservation.
Les PID ne servent qu'au diagnostic ; un refus de permission signifie une
activité non vérifiable, jamais un créneau libre. Le marqueur
`HOLD_NEW_TRIALS.json` est obligatoire tant que les cinq runs natifs ne sont pas
terminaux : il faut aussi retarder leurs graines encore non démarrées.
Ces gardes ne constituent pas un verrou partagé avec le lanceur de phase 51.
Le verrou propre au banc empêche
deux paires simultanées ; chaque paire déroule natif, certificat, candidat,
comparaison de façon séquentielle.

`compare.py` importe seulement la bibliothèque standard et `common.py`, jamais
Torch ou le modèle. Il compare les hashes de chaque tenseur et les états RNG.
Les checkpoints complets aux pas 1 et 10 restent disponibles pour un diagnostic
ultérieur explicitement autorisé. Les temporisations incluent l'instrumentation
et ne démontrent aucun facteur d'accélération.

Un échec laisse toutes les traces disponibles. Aucun essai n'est relancé
automatiquement, et les sources phase 51 ne sont jamais modifiées.
