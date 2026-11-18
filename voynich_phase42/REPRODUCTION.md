# Reproduire la phase42

Python3.9 ou ultérieur ; Pillow pour vérifier les cadrages. Exécution vérifiée ici avec Python3.9.6 et Pillow11.3.0. Aucune connexion réseau nécessaire après acquisition des sources.

Depuis la racine du dépôt :

```sh
python3 voynich_phase42/src/controls.py > voynich_phase42/results/controls.json
python3 voynich_phase42/src/study.py
python3 voynich_phase42/src/verify.py
python3 voynich_phase42/src/replay.py
```

Le programme reconstruit 52 associations ligne/signe dans les deux sources et énumère tous les comptes autorisés par les variantes marquées. Le vérificateur d'un agent séparé n'importe pas le programme d'étude : il utilise un autre parseur, toutes les paires de signes répétés et des certificats de Bézout. Il confirme 13 088 PGCD égaux à1, les empreintes des13 fichiers figés et les pixels des trois cadrages.

La reproduction en dossier neuf copie les fichiers figés et le vérificateur, puis recalcule sept fichiers : lignes, ensembles de comptes, analyse, candidats, résumé, contrôles et vérification. Ils sont identiques à l'octet. Ces contrôles prouvent la traçabilité et l'arithmétique de la famille définie ; ils ne vérifient aucune traduction ni aucune valeur phonétique.

[Protocole](PROTOCOL.json) · [Résultat de vérification](results/verification.json) · [Résultat de reproduction](results/replay.json)
