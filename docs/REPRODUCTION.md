# Reproduire et vérifier

## 1. Vérifier l'édition

Depuis la racine du dépôt :

```bash
python3 tools/verify_snapshot.py
python3 tools/hydrate.py
```

Le premier programme recalcule les SHA-256 des fichiers de l'inventaire initial des phases 1 à 17, en décompressant les gros fichiers en mémoire si nécessaire. Il ne couvre pas les ajouts ultérieurs de phase 18. Le second restaure ces fichiers à leur chemin historique. Il refuse d'écraser un fichier existant différent. Les octets restaurés sont identiques à ceux des archives sources.

Les empreintes historiques conservées dans chaque phase couvrent parfois des images omises ici. Une différence de périmètre avec ces manifestes n'est pas nécessairement une altération. L'inventaire de cette édition est `artifacts/file_index.json`.

## 2. Environnement

Python 3.12 a servi aux expériences. Le compilateur g++ avec C++17 est nécessaire aux solveurs C++. Node est nécessaire à l'audit de phase 11. Poppler sert à rendre les rapports PDF.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

Les versions racines décrivent l'environnement de consolidation. Les fichiers `ENVIRONMENT.json`, `requirements.txt` et notices de chaque phase font autorité pour leur exécution historique. Le parcours des optimiseurs peut varier avec le compilateur ou les arrondis ; ne pas confondre cela avec une validation de lecture.

## 3. Choisir une phase

Lire d'abord son `README.txt` ou `LISEZ_MOI.txt`, puis son protocole et ses addenda. Les dossiers restent voisins. Certains scripts partent de leur dossier, d'autres du dossier parent : suivre les commandes de la notice de la phase.

Exemples de vérifications rapides, sans nouveau déchiffrement :

```bash
python3 voynich_phase15/src/controls.py
python3 voynich_phase17/src/crib_scan.py
```

Ces commandes réécrivent leurs résultats. Pour préserver la référence, travailler dans une copie ou une branche dédiée. Les commandes d'optimisation complètes sont plus longues. Certaines réutilisent des résultats présents : vérifier les options `--force` ou les instructions de suppression dans une copie avant de revendiquer une nouvelle exécution.

## 4. Phase 18

La phase 18 se reproduit séparément, sans téléchargement ni modification des phases précédentes :

```bash
python3 voynich_phase18/src/experiment.py prepare
python3 -m unittest discover -s voynich_phase18/src -p 'test_*.py' -v
python3 voynich_phase18/src/experiment.py controls --workers 4
python3 voynich_phase18/src/experiment.py real --workers 4
python3 voynich_phase18/src/verify.py
```

Elle nécessite Python, NumPy et C++17 ; Matplotlib sert à reconstruire la figure. Les résultats présents sont réutilisés après contrôle de leurs empreintes. Pour une nouvelle optimisation, déplacer le dossier `voynich_phase18/results/` dans **une copie du dépôt** avant les commandes de calcul. Voir [la notice de phase 18](../voynich_phase18/README.md).

## 5. Images, modèles et ressources externes

Les sources photographiques Yale, les TIFF multispectraux et certaines matrices binaires ne sont pas inclus dans Git. Leur inventaire est dans `artifacts/omitted_binary_assets.json`. Les sources officielles sont décrites dans `docs/SOURCES.md` et les manifestes d'origine. Certaines petites figures dérivées sont également omises ; elles peuvent être régénérées lorsque les données sources correspondantes sont présentes.

Les archives de reproduction complètes déjà produites restent les ensembles les plus simples pour reproduire une phase dépendant d'images. Les modèles de langue binaires régénérables se reconstruisent avec les scripts de préparation de chaque phase. Aucun téléchargement de TIFF ou recalcul coûteux ne se lance automatiquement.

Pour la phase 17, la cryptanalyse utilise les deux fichiers IVTFF inclus. L'analyse spectrale requiert en plus `data/f116v_native_roi_22bands.npz`, ou les captures brutes référencées. Ne pas annoncer une reproduction spectrale si seule la cryptanalyse a été exécutée.

## 6. Portée de la validation de cette migration

La migration vérifie les archives ZIP utilisées, les octets des fichiers sélectionnés, les rapports PDF et les chemins de documentation. Elle ne réexécute pas les 17 séries de calculs. Les comptes rendus de vérification historique sont archivés dans chaque dossier `results/`.

La copie locale ZIP de phase 5 était illisible au moment de la consolidation. Les 285 fichiers de phase 5 présents dans l'archive valide de phase 6 ont servi de source de récupération. La provenance de chaque fichier est enregistrée, et le PDF de phase 5 a été conservé séparément. Aucun contenu absent n'a été inventé.
