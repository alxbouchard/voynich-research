# Reproduire la phase 40

Python 3.9.6 ; bibliothèque standard pour les équations et les calculs. Pillow 11.3.0 est utilisé par le contrôle des images et la préparation des recadrages. Toutes les entrées nécessaires sont incluses ; aucun accès réseau n'est nécessaire pour la reproduction.

Depuis ce dossier :

```sh
python3 -B src/verify.py
python3 -B src/complete_labels.py
python3 -B src/replay.py
```

Le vérificateur contrôle les 26 fichiers figés, les témoins de transcription et les pixels des recadrages. Il réénumère intégralement les modèles de 1 016 jeux d'équations avec une implémentation distincte. Le complément contrôle l'ensemble des 64 loci de type Ls dans chaque transcription. La réexécution copie les fichiers figés dans un dossier temporaire neuf, relance les calculs, la vérification et le complément, puis compare huit sorties à l'octet.

`study.py` refuse d'écraser un dossier de résultats existant. `prepare.py` refuse d'écraser les entrées après le gel. Les résultats principaux, leur méthode et les 11 contrôles mécaniques restent identiques au gel ; seul le supplément déclaré dans ADDENDUM.md élargit la projection des légendes.

`MANIFEST.json` recense tous les fichiers du dossier sauf lui-même et les caches Python. Les sources historiques conservent leurs fins de ligne et leurs droits. Le solveur de phase30 est copié à l'identique ; ses empreintes et celles des données figurent dans SOURCES.json et FREEZE.json. Ni la reproduction ni une solution unique d'équations ne constituent une traduction validée.
