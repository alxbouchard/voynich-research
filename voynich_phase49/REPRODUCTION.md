# Reproduction locale

Environnement utilisé : Python 3.9.6, Temurin OpenJDK 25.0.1, macOS. Les scripts Python emploient la bibliothèque standard. Le chemin Java est déclaré dans `src/build.py` ; pour une autre machine, adapter seulement ce chemin et conserver la modification dans un journal. Le lanceur utilise un répertoire de compilation temporaire.

Depuis la racine du dépôt :

```bash
python3 voynich_phase49/src/build.py
python3 voynich_phase49/src/run.py --out chemin-local/ctts-calibration-replay
python3 voynich_phase49/src/verify_independent.py
python3 voynich_phase49/src/manuscript_run.py --out chemin-local/ctts-voynich-replay
python3 voynich_phase49/src/verify_selection.py
python3 voynich_phase49/src/verify_manuscript.py
```

Choisir des destinations nouvelles : les programmes refusent d'écraser les résultats d'une recherche. Les huit recherches de calibration et les seize recherches de la comparaison manuscrit/générateur ont été rejouées avec les mêmes graines ; clés et sorties sont identiques à l'octet. Les fichiers `REPLAY.json` et `MANUSCRIPT_REPLAY.json` conservent les comparaisons d'empreintes.

La calibration vérifie 52 empreintes gelées. Le transfert vérifie aussi son propre gel, le statut de calibration et les empreintes des classes compilées. Pour la première exécution de calibration, la liaison source–classes est attestée par la compilation locale, le diff conservé et la relecture indépendante des copies ; les empreintes des classes ont été enregistrées ensuite, avant les essais manuscrit. Aucun changement de source compilée n'a eu lieu entre ces étapes.

`prepare.py` reconstruit les contrôles depuis l'archive de phase 10, si le dépôt complet est disponible. `manuscript_prepare.py` reconstruit les sélections depuis les copies de phase 47. Les données nécessaires aux recherches et aux calculs de score sont présentes dans ce dossier. Les vérificateurs de provenance exigent aussi le dépôt complet : l'archive compressée de phase 10 et les anciennes copies ZL/IT. Les rapports de ces vérifications sont conservés dans la livraison. `evaluate.py` et `manuscript_evaluate.py` évaluent les sorties archivées, sans réajustement de clé.

Les fichiers historiques et les séquences normalisées ne sont pas des témoins sémantiques du Voynich. La récupération des lettres des contrôles n'établit ni les unités réelles du manuscrit, ni sa langue, ni ses espaces.

`results/SUMMARY.json` conserve l'instantané de calibration antérieur au transfert, avec `manuscript_run=false`. L'état final figure dans `STATUS.json` et les résultats effectifs du transfert dans `results/MANUSCRIPT_SUMMARY.json`.
