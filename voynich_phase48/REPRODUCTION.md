# Reproduction hors ligne

Depuis la racine du dépôt, avec Python, NumPy, pandas et matplotlib :

```bash
python3 voynich_phase48/src/analyse.py --out chemin-local/voynich-phase48-replay
python3 voynich_phase48/src/provenance_audit.py
python3 voynich_phase48/src/verify_independent.py
```

L'analyse vérifie les 15 empreintes du gel avant exécution. Elle charge les fonctions du code public dans un répertoire temporaire, avec une adaptation d'un octet de commentaire. Elle n'appelle ni le modèle BERT, ni le pilote complet, ni les fonctions de graphique et n'effectue aucune requête réseau. La version Python employée est 3.9.6 ; le README tiers recommande 3.10 ou supérieur. Le cœur étudié s'exécute dans cet environnement.

Les six sorties attendues du programme principal sont `EXECUTION.json`, `VOCABULARY.json`, `CONTROLS.json`, `PUBLISHED_AUDIT.json`, `DIAGNOSTICS.json` et `SUMMARY.json`. Deux exécutions locales ont produit exactement les mêmes octets ; [empreintes](results/REPLAY.json). L'audit de provenance est descriptif et postérieur aux scores. Le vérificateur indépendant ne prend pas l'analyse principale comme oracle ; consulter sa sortie pour la portée des recalculs.

Le téléchargement public, uniquement si les sources doivent être reacquises, est séparé : `python3 voynich_phase48/src/acquire.py`. Il utilise le commit fixé et refuse un fichier dont la taille ou le SHA Git diffère.

Le gel porte sur les sources, le protocole et le programme principal, avant calcul. Le manifeste final couvre aussi les rapports et vérifications ultérieurs. Aucun fichier de sortie ne démontre un sens ou une traduction.
