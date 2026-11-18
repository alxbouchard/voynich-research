# Phase 51 — reproduction de la calibration gelée

Ce document décrit les commandes de préparation, d'exécution et d'évaluation. Il ne rapporte pas leurs résultats. Les sources et les données sont décrites dans [NOTICE.md](NOTICE.md); les paramètres et critères de décision figurent dans [PROTOCOL.json](PROTOCOL.json).

## État de référence et environnement

Le commit du dépôt de recherche gelé avant entraînement est `b38fa082fcc9e732114a54a636a68a8e64026888`. Son dossier `voynich_phase51/` contient les scripts, les 103 blobs amont, les sources IE-CoR et les données préparées. Les copies générées de `runtime/` ne sont pas versionnées; leurs empreintes font partie des 242 fichiers de [FREEZE.json](../docs/PIECES_REFERENCES.md#piece-d2b0a8f7459a01). `REGISTRATION.json`, lorsqu'il accompagne les résultats, rapporte la vérification du commit avant les premiers entraînements.

L'environnement existant est `chemin-local/python`. [ENVIRONMENT.json](../docs/PIECES_REFERENCES.md#piece-e658c0b21b9c44) enregistre Python 3.9.6 sur macOS 27.0.1 ARM64, PyTorch 2.8.0, NumPy 1.26.4, pandas 1.5.3 et ipapy 0.0.9.0, ainsi que les autres versions observées. Ce venv hérite de `system-site-packages`; une installation entièrement propre n'a pas été validée. `requirements_runtime.txt` est un inventaire de versions utiles, pas une garantie de résolution sur toute plateforme. `requirements_added.txt` décrit les ajouts du venv. Le conflit déclaré entre l'outil hérité `inflect` et la version locale de `typeguard` concerne un outil non utilisé ici; aucun environnement Python global n'a été modifié.

Les exemples suivants supposent que ce venv existe encore et que le dépôt local possède le commit indiqué. Sur une autre machine, il faut reconstituer et documenter l'environnement avant de revendiquer une reproduction; les mêmes graines ne garantissent pas à elles seules des résultats numériques identiques entre plateformes.

## Copie isolée et reconstruction du moteur

Créer une nouvelle copie depuis le commit gelé, sans réutiliser un dossier contenant des entraînements. Adapter seulement le chemin du dépôt si nécessaire :

```sh
PHASE51_REPRO="$(mktemp -d chemin-local/voynich-phase51-reproduction.XXXXXX)"
git -C la copie locale du dépôt archive b38fa082fcc9e732114a54a636a68a8e64026888 voynich_phase51 | tar -x -C "$PHASE51_REPRO"
cd "$PHASE51_REPRO/voynich_phase51"
export PHASE51_PYTHON=chemin-local/python
PYTHONDONTWRITEBYTECODE=1 "$PHASE51_PYTHON" build_runtime.py
PYTHONDONTWRITEBYTECODE=1 "$PHASE51_PYTHON" prepare.py
```

`build_runtime.py` copie `upstream/xib` et `upstream/dev_misc` dans `runtime/`, puis applique exactement les quatre substitutions enregistrées dans `COMPATIBILITY.json`. Il ne lance ni `setup.py` ni un entraînement. Les pins amont sont `50dd1d4133ad154d89f37c476ad7a4adff06e970` pour xib et `8cb3c73bebe444dd22da25e44a3fe05d13aff8c5` pour dev_misc.

`prepare.py` authentifie les quinze sources IE-CoR par taille, SHA de blob Git et SHA-256, puis les 103 blobs du moteur et les quatre modifications. Il importe le parseur original depuis `runtime/`. Il s'arrête devant une transformation phonémique inattendue; il ne remplace pas les données problématiques par une transcription improvisée.

La préparation régénère `data/train.tsv`, `data/test.tsv`, `data/vocab.words`, `data/GOLD.json` et `data/INPUTS.json`. Le tri SHA-256 de `phase51-test-v1|` suivi du FormID réserve les 31 premières formes et conserve les 92 autres pour l'apprentissage. Chaque partition est mélangée indépendamment avec la graine 51101 ou 51102, puis regroupée par deux. Le lexique contient 166 candidats canoniques. Les fichiers moteur n'incluent ni les FormID ni les frontières internes réelles; la langue inconnue est sérialisée `unk` et la langue connue `non`.

Vérifier les empreintes **après** reconstruction, avant tout entraînement :

```sh
"$PHASE51_PYTHON" - <<'PY'
from pathlib import Path
import hashlib, json
root = Path.cwd()
freeze = json.loads((root / "FREEZE.json").read_text())
bad = []
for relative, expected in freeze["files"].items():
    path = root / relative
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        bad.append(relative)
assert not bad, bad
print("Empreintes vérifiées :", len(freeze["files"]))
PY
"$PHASE51_PYTHON" evaluator.py --self-test
```

Un écart doit être expliqué avant de poursuivre. Ne pas recalculer `FREEZE.json` simplement pour rendre un environnement divergent acceptable. Les commandes de reconstruction ci-dessus sont destinées à une copie neuve, pas au répertoire d'une expérience en cours.

## Cinq graines, deux tâches simultanées au maximum

Pour une graine, la commande est `"$PHASE51_PYTHON" run.py 51001 --python "$PHASE51_PYTHON"`. Le lanceur vérifie le gel et refuse un dossier `runs/<graine>` préexistant. Pour exécuter les cinq graines sans dépasser deux tâches concurrentes, lancer une seule fois le bloc suivant dans la copie neuve :

```sh
"$PHASE51_PYTHON" - <<'PY'
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import os, subprocess
python = os.environ["PHASE51_PYTHON"]
assert not Path("runs").exists(), "Utiliser une copie neuve; conserver les anciens calculs."
seeds = [51001, 51002, 51003, 51004, 51005]
def run_seed(seed):
    result = subprocess.run([python, "run.py", str(seed), "--python", python])
    return seed, result.returncode
failed = []
with ThreadPoolExecutor(max_workers=2) as pool:
    futures = [pool.submit(run_seed, seed) for seed in seeds]
    for future in as_completed(futures):
        seed, code = future.result()
        print({"seed": seed, "returncode": code}, flush=True)
        if code:
            failed.append(seed)
assert not failed, {"incomplete_or_failed_seeds": failed}
PY
```

Chaque graine utilise deux threads CPU et 3 000 étapes d'apprentissage. `run.py` exécute successivement `train`, `initial`, puis `final`. L'inférence « initiale » relit le point de contrôle initial sauvegardé avant l'optimisation; son exécution après l'entraînement ne change pas les poids évalués. L'inférence finale utilise le point de contrôle de l'étape 3 000. Aucun modèle externe préentraîné n'initialise l'expérience.

Les deux inférences emploient les mêmes réglages fixes de score : insertion/suppression 3,5, température 0,2 et baseline globale `1e-8`, avec les mêmes alphabets et candidats. Tous les oracles sont désactivés. La longueur maximale des mots est 9; celle des séquences admises est 18, supérieure au maximum observé de 14. Les bornes couvrent les entrées sans en exclure silencieusement.

Le plafond est de 3 600 secondes pour l'apprentissage d'une graine et de 300 secondes par inférence. Un échec ou dépassement conserve les journaux et interrompt les étapes restantes de cette graine. Il rend l'expérience incomplète; ce n'est pas un résultat scientifique négatif. Ne pas supprimer les sorties pour masquer un échec, sélectionner la meilleure graine, ni ajuster les paramètres après lecture des résultats. La limite de deux tâches est assurée par le bloc ci-dessus, pas globalement par `run.py`.

## Évaluation indépendante des vingt fichiers

Après achèvement des cinq graines, il doit exister exactement les combinaisons suivantes : cinq graines × deux états (`initial`, `final`) × deux partitions (`train`, `test`). Les fichiers sont `runs/<graine>/<état>/PREDICTIONS_<partition>.json`. Le bloc suivant contrôle les statuts et transmet explicitement les vingt chemins :

```sh
"$PHASE51_PYTHON" - <<'PY'
from pathlib import Path
import itertools, json, os, subprocess
seeds = [51001, 51002, 51003, 51004, 51005]
for seed in seeds:
    status = json.loads((Path("runs") / str(seed) / "RUN.json").read_text())
    assert status["status"] == "complete", (seed, status["status"])
paths = [Path("runs") / str(seed) / stage / f"PREDICTIONS_{partition}.json"
         for seed, stage, partition in itertools.product(
             seeds, ["initial", "final"], ["train", "test"])]
assert len(paths) == 20 and all(path.is_file() for path in paths)
subprocess.run([os.environ["PHASE51_PYTHON"], "evaluator.py",
                "--gold", "data/GOLD.json", "--prediction-files",
                *map(str, paths), "--output", "results/EVALUATION.json"], check=True)
PY
```

`evaluator.py` n'importe pas le modèle. Il vérifie les identités, la réserve et les positions, puis exige la frontière complète du mot source (indices Unicode inclusifs) et une cible appartenant à sa classe IPA acceptable. Le dénominateur du rappel est 19 dans la réserve et 63 dans l'apprentissage. La précision annotée compte tous les segments prédits, y compris les segments partiels, les croisements et les formes sans cognat annoté. Les scores natifs calculés avec les annotations factices du TSV ne sont pas utilisés.

L'évaluateur effectue 9 999 permutations, graine 51999, des ensembles de cibles dans les blocs de longueur source 3–4, 5–6 et 7–9. Il conserve les ensembles vides et partage chaque permutation entre graines et états. Le seuil gelé exige un gain moyen strictement positif, un gain pour au moins quatre graines sur cinq, et des valeurs p ≤ 0,01 pour le score final et le gain. Aucune de ces conditions ne doit être déclarée satisfaite avant lecture de `results/EVALUATION.json` et vérification de la provenance d'exécution.

## Pièces à conserver

Conserver le commit gelé, `FREEZE.json`, `PROTOCOL.json`, les sources et leurs reçus, l'environnement effectivement utilisé, et tout `runs/`. Chaque graine fournit `RUN.json`; chaque étape fournit `JOB.json`, stdout, stderr et les fichiers natifs. Les inférences produisent `MODEL_INPUTS.json` dans leur sous-dossier `native/`, les prédictions, `ALIGNMENT.json` avec axes étiquetés et les empreintes des points de contrôle. Les marqueurs `TRAINING_COMPLETE.json` et `INFERENCE_COMPLETE.json` complètent cette traçabilité. Enfin, conserver `results/EVALUATION.json`, les vingt entrées utilisées et leurs empreintes.

`GOLD.json` est séparé des arguments et lectures du moteur, mais reste accessible dans le système de fichiers : il s'agit d'une séparation fonctionnelle contrôlable dans le code, pas d'un isolement informatique. Une éventuelle réussite ne démontrerait que la récupération partielle de cognats dans cette calibration lexicale. Elle ne validerait ni une traduction ni une clé phonétique complète.
