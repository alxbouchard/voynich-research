# Reproduction de la phase 44

Python 3.9 ou ultérieur et Pillow (version utilisée : 11.3.0). Depuis la racine du dépôt :

```sh
python3 voynich_phase44/src/verify.py
python3 voynich_phase44/src/replay.py
```

Le premier script vérifie les empreintes figées, les métadonnées des trois images, les pixels natifs des sept cartes et les réponses archivées. Il extrait le locus publié dans les deux transcriptions. La comparaison des pixels utilise les lignes brutes des images décodées plutôt que de recréer les cadrages avec la fonction crop.

Le second copie les sources, les réponses et le vérificateur dans un dossier temporaire neuf. Il exige que COLLATION.json et verification.json soient identiques à l'octet aux résultats archivés. Il ne contacte aucun service, ne relance aucun agent et ne mesure aucune précision paléographique. La reproductibilité de la collation ne signifie pas reproductibilité ni justesse des lectures IA.

Les fichiers des lecteurs restent inchangés. FREEZE.json atteste les entrées antérieures aux lectures ; MANIFEST.json inventorie l'ensemble de la livraison après les lectures. [Résultat du rejeu](results/replay.json).
