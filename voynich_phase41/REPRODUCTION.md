# Reproduire la phase 41

Les entrées sont incluses. Le calcul descriptif utilise Python3.9.6 et sa bibliothèque standard. Le vérificateur d'images utilise Pillow11.3.0. La préparation des vues géométriques utilisait également NumPy1.26.4 ; cette dépendance n'est pas nécessaire pour refaire les analyses ou vérifier les images déjà conservées.

Depuis ce dossier :

```sh
python3 -B src/verify.py
python3 -B src/replay.py
```

Le vérificateur reconstruit les 409 unités, contrôle 24 lectures de cycles, recalcule les 36 distances et nombres d'alignements par une récursion distincte, et vérifie les six graphes par une structure d'union d'ensembles. Il vérifie tous les pixels du dépliage géométrique avec un calcul scalaire, puis les quatre bandes.

La réexécution copie les 18 fichiers figés et le vérificateur dans un dossier neuf, relance le calcul descriptif et la vérification, puis compare cinq sorties à l'octet. `study.py` refuse d'écraser les résultats existants. `images.py` refuse de modifier les vues après le gel. `MANIFEST.json` couvre tous les fichiers, sauf lui-même et les caches Python.

Les données GC restent un extrait documentaire, pas une copie intégrale du fichier source. Les regroupements alternatifs sont des scénarios de comptage, non des corrections introduites dans les analyses principales. Le contrôle logiciel ne résout pas le choix des unités historiques ni leur sens.
