# Reproduire la phase 39

Les calculs emploient Python 3.9.6 et sa bibliothèque standard. Les JSON nécessaires sont inclus. Pour contrôler aussi leur conversion depuis les Parquet originaux, `polars` 1.35.2 est utilisé.

Depuis ce dossier :

```sh
python3 -B src/convert.py
python3 -B src/verify.py
python3 -B src/replay.py
```

La première commande, optionnelle pour relancer les calculs, compare les 1 879 lignes du Parquet au JSON dérivé et contrôle la partition. Les autres ne nécessitent pas polars. La réexécution copie les 22 fichiers figés, réapprend le modèle avec les seules données d'apprentissage, calcule les prédictions et scores réservés, les vérifie puis refait le diagnostic. Elle compare six sorties à l'octet et confirme que les fichiers d'apprentissage reconstruits n'ont pas changé.

`study.py` refuse d'écraser un résultat existant. Utiliser `replay.py` pour préserver la livraison. Le résultat de la réexécution figure dans `results/replay.json`.

`FREEZE.json` est le gel effectif, antérieur aux résultats. `development/PREFREEZE_ABORTED.json` est la trace d'une préparation interrompue avant exécution ; les différences sont expliquées dans `development/NOTES.md`. La carte tierce originale conserve ses fins de ligne CRLF ; ne pas les normaliser pour satisfaire un contrôle de style.

`MANIFEST.json` couvre toute la livraison, sauf lui-même et les caches Python. Le vérificateur, le diagnostic, la réexécution et les rapports ont été ajoutés après les résultats. Ils n'altèrent pas les paramètres figés.

La reproductibilité arithmétique ne valide ni la qualité philologique de l'alignement automatique ni une lecture du Voynich.
