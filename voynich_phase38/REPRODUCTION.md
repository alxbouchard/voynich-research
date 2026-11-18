# Reproduire la phase 38

Python 3.9.6 et bibliothèque standard suffisent aux calculs. La lecture initiale du PDF a utilisé pdfplumber et PyMuPDF ; ils ne sont pas nécessaires à la reproduction. Les données nécessaires sont incluses, sans téléchargement ni dépendance à un autre dossier de phase.

Depuis ce dossier :

```sh
python3 -B src/verify.py
python3 -B src/replay.py
```

Le premier programme recalcule indépendamment les lectures et les scores et écrit `results/verification.json`. Le second copie les entrées figées dans un nouveau dossier temporaire, refait les contrôles, le calcul et la vérification, puis compare les sorties à l'octet. Il écrit `results/replay.json` dans la livraison d'origine. Aucun générateur historique ni collecte web n'est relancé.

Résultat du 17 novembre 2026 : **11 fichiers reproduits à l'octet**, comprenant les quatre jeux de données construits, cinq sorties du calcul, le vérificateur JSON et le CSV. Les 40 empreintes figées restent identiques, y compris après les contrôles mécaniques relancés.

Les résultats existants sont protégés : `src/study.py` refuse d'écraser `results/SUMMARY.json`. Pour une exécution manuelle, utiliser une copie des seuls fichiers énumérés dans `FREEZE.json`, ajouter `FREEZE.json`, puis lancer `src/checks.py` et `src/study.py`. Ne pas effacer les résultats archivés pour relancer le calcul.

`FREEZE.json` couvre les 40 fichiers antérieurs aux mesures. `MANIFEST.json` couvre la livraison finale, à l'exception de lui-même. Le vérificateur, la réexécution, le rapport et le statut ont été ajoutés après les résultats ; ils ne changent aucune règle figée. Le programme expérimental et le vérificateur n'ont pas d'import commun de modèle ou de calcul.

Les valeurs lexicales sont des compatibilités, pas des probabilités de traduction. Les classements contre des permutations ne sont pas des tests statistiques corrigés pour la sélection historique de la clé. La réexécution prouve la reproductibilité des calculs avec ces entrées, pas la vérité de l'hypothèse linguistique.
