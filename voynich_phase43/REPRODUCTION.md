# Reproduction de la phase43

Python3.9 ou ultérieur, bibliothèque standard uniquement. Depuis la racine du dépôt :

```sh
python3 voynich_phase43/src/audit.py
python3 voynich_phase43/src/verify.py
python3 voynich_phase43/src/replay.py
```

L'audit charge les deux modules publics inspectés, redirige leurs fichiers de sortie vers des dossiers temporaires et modifie seulement des objets en mémoire. Il ne lance pas reproduce.sh ni le programme principal du vérificateur botanique, dont les chemins visent une machine tierce. Seule sa fonction pure apply_r14 et ses deux tables sont exécutées, après extraction de l'arbre syntaxique.

Le contrôle séparé n'importe aucun module audité. Il reconstruit les calculs depuis les constantes, inspecte les conditions exactes des verdicts et vérifie les16 empreintes figées, les10 fichiers Git, les lignes sources et les tableaux publiés. La reproduction en dossier neuf obtient AUDIT.json et verification.json identiques à l'octet. Aucun réseau, modèle de langue ni décodeur complet externe ne participe à cette reproduction.

Les fichiers tiers restent inchangés, y compris leurs fins de ligne CRLF et espaces Markdown. Les contrôles de format s'appliquent aux fichiers ajoutés par notre étude ; les empreintes garantissent l'intégrité des originaux.

[Protocole](PROTOCOL.json) · [Vérification](results/verification.json) · [Reproduction](results/replay.json)
