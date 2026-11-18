# Reproduction des résultats

Utiliser Python 3.10 ou ultérieur, en exécutant les commandes **depuis le dossier de ce fichier**. Les transcriptions ZL et IT se trouvent dans `../../voynich_phase46/sources` et les graphies d’Agrippa dans le dossier voisin `../2026-11-17-f69v-mansions`. Les fichiers d’entrée de Sachau et des Walters sont déjà inclus. Le rapport donne les liens vers les fac-similés originaux.

```sh
python3 -B run.py
python3 -B exception_bound.py
python3 -B exact_coverage.py
python3 -B compare_sachau.py
python3 -B compare_arabic.py
python3 -B verification/check_witness.py
python3 -B verification/audit_triple.py
python3 -B verification/circle_audit.py
python3 -B verification/verify_circle.py
python3 -B verification/exact_coverage.py
python3 -B verification/verify_exact_coverage.py
python3 -B walters/verify.py
```

Le premier programme exécute ses contrôles avant de charger les entrées du manuscrit. Il vérifie les empreintes de ZL et IT. Le fichier `orientations.json.gz` donne les orientations et les lignes refusées par les contraintes locales. Les programmes de vérification du cercle reconstruisent les domaines avec leur propre méthode. Les fichiers JSON et leurs copies comprimées sont lisibles en bibliothèque standard. Les empreintes de scripts dans les audits correspondent aux copies portables livrées ici.

Les meilleurs ajustements dans les fichiers de calcul sont des témoins mathématiques. Les lettres affichées après substitution ne disposent d’aucune confirmation linguistique.
