# Phase 27 — reproduction locale

Lire [RAPPORT.md](RAPPORT.md), [PROTOCOL.json](PROTOCOL.json) et [METHODS_EN.md](METHODS_EN.md). Les résultats ne constituent ni un déchiffrement ni une identification de langue.

Python 3 suffit pour les calculs et vérifications ; Matplotlib est utilisé uniquement pour la figure. Sources copiées, versions, graines, paquets, clés de contrôle et résultats sont fournis. Aucun accès réseau ni dépôt voisin n'est nécessaire au vérificateur et à la reproduction.

Depuis le parent du dossier :

```sh
python3 -B voynich_phase27/src/verify.py
python3 -B voynich_phase27/src/replay.py
```

Adapter seulement `voynich_phase27` si le dossier livré a été renommé. `verify.py` réécrit son compte rendu déterministe ; `replay.py` crée une nouvelle copie de calcul sous `/private/tmp` et compare tous les fichiers générés. Il ne mesure pas de nouvelles données indépendantes. Aucun résultat existant n'est effacé. Le compte rendu de replay garde des sorties déterministes, sans utiliser le nom aléatoire du répertoire.

Pour lancer manuellement le pipeline dans une copie neuve contenant uniquement les fichiers du gel et `FREEZE.json` :

```sh
python3 -B voynich_phase27/src/checks.py
python3 -B voynich_phase27/src/study.py prepare
python3 -B voynich_phase27/src/study.py controls
python3 -B voynich_phase27/src/study.py real
```

Les commandes de production refusent d'écraser les résultats existants. L'étape `real` respecte le blocage de calibration. Aucun score n'est optimisé, aucune clé Voynich n'est cherchée, aucun texte n'est présenté comme traduit.

`data/references/`, `data/cases/`, `data/real/` contiennent les paquets JSON compressés déterministes. `sealed/` contient les seules clés et informations de génération des contrôles, non fournies au mesureur. Ce nom ne constitue pas une revendication de secret vis-à-vis de l'opérateur. `results/RESULTATS.csv` rassemble les 150 valeurs principales. Les JSON conservent aussi les 18 cellules conditionnelles et 22 entropies marginales par paquet.

`FREEZE.json` documente le gel prospectif, commit `84805ce`. `SHA256SUMS.json` est un manifeste après expérience, excluant seulement lui-même, les fichiers temporaires et le bytecode. La vérification des anciennes phases est dans `results/preservation.json`.

Aucun push, publication, déploiement ou envoi. Les travaux antérieurs restent inchangés ; les mises à jour du dépôt concernent la phase 27 et ses liens de navigation.
