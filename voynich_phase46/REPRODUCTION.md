# Reproduction de la phase 46

Python 3.9 ou ultérieur et Pillow. Depuis la racine du dépôt :

```sh
python3 voynich_phase46/src/analyse.py
python3 voynich_phase46/src/verify.py
python3 voynich_phase46/src/replay.py
```

Les calculs emploient des fractions exactes. La raréfaction est analytique : aucun sous-échantillon favorable n'est choisi. Le code d'analyse et ses entrées font partie du gel antérieur aux scores. Le contrôle séparé n'importe pas l'analyse ; il reconstruit les tokens, les groupes, les distances, les probabilités, les rangs et les moyennes.

Le rejeu copie les fichiers figés, le vérificateur et les huit détails archivés avec leurs coordonnées dans un dossier temporaire neuf. Il exige cinq résultats identiques à l'octet. Aucun réseau, modèle de langue ou lecture visuelle supplémentaire ne participe au rejeu.

Les contrôles logiciels et l'invariance à l'ordre des mots établissent le fonctionnement de ces mesures de chaînes ; ils ne fournissent pas de calibration de leur valeur sémantique. [Vérification](results/verification.json) · [Rejeu](results/replay.json).
