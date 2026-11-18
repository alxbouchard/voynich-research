# Reproduction de la phase 45

Python 3.9 ou ultérieur et Pillow. Depuis la racine du dépôt :

```sh
python3 voynich_phase45/src/analyse.py
python3 voynich_phase45/src/verify.py
python3 voynich_phase45/src/replay.py
```

Le calcul utilise des fractions exactes et énumère les 24 permutations de bifolios ; aucun tirage aléatoire ni modèle de langue ne participe aux scores. Le vérificateur séparé n'importe pas le programme d'analyse. Il contrôle les sources figées, les images, le parsage et les résultats numériques avec une implémentation distincte.

Le rejeu copie les entrées et les programmes dans un dossier temporaire neuf et compare cinq sorties à l'octet. Il ne contacte aucun site et ne réévalue pas les rapprochements iconographiques. Les versions ZL/IT ne sont pas de nouveaux témoins historiques indépendants.

[Résultats du contrôle](results/verification.json) · [Résultats du rejeu](results/replay.json) · [Protocole](PROTOCOL.json).
