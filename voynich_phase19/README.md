# Phase 19 — le signal des finales distingue-t-il un message ?

[Rapport et figure](RAPPORT.md) · [Protocole figé](PROTOCOL.json) ·
[Résultats structurés](results/summary.json)

Cette phase examine la spécificité du signal retenu en phase 18 : deux tables
de substitution, dont une réservée à la finale du mot, évaluées avec le modèle
de langue latin. Le latin est un modèle de score, pas une langue attribuée
au manuscrit. Aucune sortie n'est présentée comme une traduction.

Neuf corpus sont évalués : ZL/A et ZL/B ; trois générations aléatoires par
gabarit A/B ; l'échantillon publié Timm–Schinner déjà archivé. Chaque corpus
a dix-neuf mélanges réajustés et deux modèles (table unique/finale), soit
360 ajustements. Quatre contrôles latins chiffrés, évalués avec les deux
modèles, portent le total à 368.

## Reproduire

Python, NumPy et un compilateur C++17 suffisent aux calculs. Depuis la racine :

```sh
python3 tools/hydrate.py
python3 voynich_phase19/src/manifest.py
python3 -m unittest discover -s voynich_phase19/src -p 'test_*.py' -v
python3 voynich_phase19/src/study.py prepare
python3 voynich_phase19/src/study.py controls --workers 4
python3 voynich_phase19/src/study.py run --workers 4
python3 voynich_phase19/src/verify.py
```

Pour reconstruire le rapport et la figure, ajouter Matplotlib :

```sh
MPLCONFIGDIR=chemin-local/voynich-matplotlib XDG_CACHE_HOME=chemin-local/voynich-cache python3 voynich_phase19/src/report.py
```

Les résultats présents sont relus uniquement si leurs empreintes correspondent
aux entrées, au protocole, au générateur, aux scripts et au solveur. Pour refaire
les optimisations, travailler dans une copie et y déplacer préalablement le
dossier `voynich_phase19/results/`. Le vérificateur recalcule les scores et la
génération, mais ne relance pas l'optimisation. Un changement de compilateur ou
d'arrondis peut modifier le parcours heuristique. Le gel du protocole est
local, au commit `5afafb7`, avant génération des corpus étudiés ou ajustement.

Aucun téléchargement ni changement des phases précédentes n'est requis. Les
matrices, entrées entières et exécutables régénérables sont dans `tmp/`.
L'inventaire `SHA256SUMS.json` couvre les fichiers archivés de la phase 19,
à l'exclusion de ce dossier temporaire et des caches Python.

## Génération et séparation des données

Le générateur de Markov apprend, dans les seuls mots d'apprentissage qui seront
effectivement notés, les fréquences du prochain signe selon les deux signes
précédents et son rôle : initiale, intérieure, finale ou mot d'une lettre.
Un contexte rare est ramené progressivement au contexte plus court avec un
pseudo-compte de 1. Les mots sont générés indépendamment, signe après signe.
Il n'y a ni texte clair à encoder, ni dictionnaire, ni table de chiffrement.

Les caractères des pages réservées ne servent pas à ajuster le générateur.
Leurs **longueurs de mots et leur disposition** servent toutefois de gabarit.
Les textes générés héritent de statistiques du Voynich et peuvent retrouver
des mots de l'apprentissage par hasard : ce sont des substituts statistiques
conditionnels, pas des objets historiques indépendants. Les trois tirages de
chaque groupe partagent le même modèle appris ; ils ne sont pas trois corpus
indépendants.

L'échantillon Timm–Schinner est celui de la phase 6, avec sa première ligne
d'amorce retirée. Son générateur Java n'est pas réexécuté. Son texte a une
disposition artificielle ; des pages artificielles entières sont séparées
chronologiquement entre apprentissage et test. Les longueurs et cette
partition diffèrent de celles des groupes ZL : comparaison descriptive.

Les mélanges de cette phase laissent fixes tous les segments courts exclus
du score. Ils préservent **exactement les fréquences par rôle des caractères
effectivement notés**, les longueurs, les barrières et les lignes. Cette
correction ne transforme pas ces mélanges en modèles complets du manuscrit.

## Règle d'interprétation

Un corpus satisfait le critère fixé si son gain hors ajustement est positif,
dépasse chacun de ses dix-neuf mélanges et couvre au moins 99,5 % des signes
réservés par des signes vus à l'apprentissage. Le même critère s'applique
aux textes réels et générés ; il est hérité de la piste de phase 18, pas
choisi après observation de cette phase. Les amplitudes et tous les échecs
sont conservés. Aucun seuil d'équivalence d'amplitude ni test statistique
confirmatoire n'est ajouté après coup.

Un exemple généré sans message qui passe ce critère montre que le signal
n'est pas spécifique d'un texte porteur d'un message dans ce dispositif.
Il ne montre pas que le Voynich est dépourvu de sens. Une absence de tel
résultat ne validerait pas non plus une traduction.

## Fichiers et attribution

- `data/base_cases.json.gz` : neuf corpus de base avec leurs partitions.
- `data/markov_models.json` : comptes de transitions appris.
- `data/split_and_generation.json`, `data/case_inputs.json` : graines,
  feuillets, empreintes des corpus et mélanges.
- `results/*_{single,final}.json` : chaque clé, score de redémarrage,
  couverture et sortie intégrale `NOT_TRANSLATION`.
- `results/calibration.json`, `results/summary.json` : contrôles et comparaisons.
- `results/verification.json` : recalcul distinct des scores et reconstruction
  indépendante du code de génération, avec données et modèles partagés.

Le solveur C++ est identique à celui de la phase 18. Le moteur Python en
reprend l'encodage et l'objectif ; les empreintes incluent maintenant le
générateur et l'orchestrateur de phase 19. Les contrôles et observations ZL
non mélangées sont comparés à leurs résultats de phase 18.

Timm et Schinner : [dépôt officiel](https://github.com/TorstenTimm/SelfCitationTextgenerator),
[article référencé](https://doi.org/10.1080/01611194.2019.1596999),
échantillon `executable/generate/generated_text.txt`, blob
`31b5f847097d6c31e210d1ebc23ea9878f456607`. La licence MIT et les octets sources
sont conservés dans `voynich_phase6/data/`.
Il s'agit d'un nouvel examen de l'échantillon, pas d'une réplication complète
de l'article. Les sources César, Pline et les transcriptions conservent les
droits et attributions indiqués dans [NOTICE](../NOTICE.md).
