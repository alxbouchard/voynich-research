# Reproduire et vérifier la phase 50

La vérification des sources et inventaires utilise seulement Python standard :

```sh
python3 audit_code.py
python3 prepare_uga.py
python3 verify_integrity.py
```

Les poids archivés proviennent uniquement des essais locaux. `verify_smoke.py` les relit et compare les tenseurs ; il ne charge aucun checkpoint provenant d'Internet. Il nécessite PyTorch et les sources runtime construites par `build_runtime.py`.

## Environnement exécuté

`ENVIRONMENT.json` donne les versions pertinentes réellement observées. `requirements_runtime.txt` est un relevé des dépendances pertinentes, pas une preuve d'installation fraîche réussie. Le test a utilisé Python 3.9.6 sur macOS et un environnement temporaire avec `--system-site-packages`; les dépendances supplémentaires de `requirements_added.txt` y ont été installées. L'ancien `ipapy` doit être adapté pour des Python plus récents. Le typeguard 2 local est incompatible avec un paquet `inflect` hérité mais non utilisé par ce parcours ; le Python global n'a pas été modifié.

Exemple de reconstruction du contexte testé, depuis ce dossier :

```sh
python3 -m venv --system-site-packages venv
venv/bin/python -m pip install -r requirements_added.txt
python3 build_runtime.py
python3 verify_integrity.py
venv/bin/python verify_smoke.py
```

Les sources originales sont authentifiées par SHA Git et tailles dans `source_manifest.json`. Les quatre changements du runtime sont exacts et vérifiables dans `COMPATIBILITY.json`. La bibliothèque Cython mentionnée dans `setup.py` n'est pas requise par le parcours exécuté ; ce fichier d'installation n'est pas lancé.

## Rejouer les trois apprentissages

Le jeu artificiel et sa vérité sont déjà présents. `prepare_smoke.py` permet de les reconstruire ; il ne génère aucun texte du Voynich. `SMOKE_PROTOCOL.json` et les empreintes conservées dans chaque `RUN.json` documentent le critère fixé avant les trois exécutions. La vérité est distincte des arguments de l'optimiseur, mais pas physiquement inaccessible au processus ; les annotations demeurent dans le TSV et leur non-influence est précisément testée.

```sh
python3 run_smoke.py base --attempt 2
python3 run_smoke.py rotated_labels --attempt 2
python3 run_smoke.py changed_unused_ipa --attempt 2
```

Chaque commande crée un dossier neuf, cinq étapes d'apprentissage et un délai maximal de 120 secondes. Les commandes originales et toutes les options sont dans `smoke_runs/*_1/RUN.json`. `run_original.py` fixe deux fils CPU et appelle l'entrée originale `xib.main` après les modifications de compatibilité. La prédiction et les métriques natives s'effectuent sur les mêmes données que l'apprentissage.

Les fichiers TensorBoard et leurs horodatages ne sont pas des sorties déterministes. La vérification porte sur les tenseurs, les prédictions, les données et les pertes, pas sur l'identité binaire des archives PyTorch ou de l'horloge. Les trois variantes testent une invariance locale ; aucun théorème général d'absence de fuite n'en découle.

Les données ougaritiques publiées et leur inventaire sont inclus. Leur conversion phonétique historique n'a pas été inventée, donc aucun entraînement ougaritique ni test Voynich n'est exécuté dans cette phase. L'évaluateur A@10 de l'expérience publiée n'est pas reconstitué.
