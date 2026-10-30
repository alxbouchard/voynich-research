# Phase 21 — mots inconnus et nouveaux contrôles

Cette phase corrige une limite de phase 20 : les mots absents du dictionnaire
étaient obligatoirement découpés en formes connues, parfois en lettres
isolées. Le nouveau modèle permet une forme inconnue entière de 1 à 24
lettres. Il reste un modèle de substitution bijective sur 26 lettres,
avec langue fournie, sans application automatique au Voynich.

## Développement puis évaluation réservée

Les **24 passages de phase 20 deviennent des données de développement**.
Leur texte clair sert à choisir un réglage de segmentation, sans prétendre
que ce choix constitue un résultat réservé. La grille fixée avant les
calculs comprend 16 couples : coefficient d'orthographe 0,25/0,5/0,75/1,
pénalité de mot inconnu 0/2/4/6. Le meilleur F1 moyen des limites de mots
sur ces 24 passages choisit un seul couple pour les deux langues ; en cas
d'égalité, les coefficients les plus grands sont préférés.

Le couple retenu est **coefficient 1, pénalité 0**, avec F1 de développement
0,91777364. Les 16 résultats sont conservés dans
[la grille](results/development/grid.json). Le [plan de développement](DEVELOPMENT_PLAN.json)
décrit cette sélection. Ce résultat exploite des lettres connues : il ne
mesure pas la récupération d'une clé inconnue.

Avant de choisir les nouveaux extraits ou de chercher leurs clés, le
[protocole](PROTOCOL.json), le moteur, le prétraitement et le vérificateur
sont figés localement dans Git. Ce gel n'est pas une préinscription externe.
Les sources historiques ont déjà été vues dans le projet : les nouveaux
extraits sont réservés à cette correction, pas inconnus de tout travail antérieur.

## Ce qui change dans le modèle

Les corpus d'entraînement restent César pour le latin, *Inferno/Purgatorio*
pour l'italien. Aucun mot de Pline ou du *Paradiso* n'enrichit le dictionnaire.
Les graphies normalisées de phase 10 sont conservées (`j→i`, `k→c`, `w→uu`).

Les mots présents au moins deux fois dans l'entraînement constituent le
dictionnaire. Les formes présentes une seule fois sont remplacées par une
classe de mot inconnu pour apprendre les probabilités lexicales à trois
mots. Une forme inconnue proposée reçoit en plus :

- un score de suites de quatre caractères internes au mot, avec début et
  fin explicites, appris en donnant le même poids à chaque type de mot
  d'entraînement ;
- un score de longueur appris sur les formes d'entraînement présentes une
  seule fois, lissé par 0,5 pour chaque longueur de 1 à 24 ;
- le coefficient et la pénalité sélectionnés sur les anciens contrôles.

Le modèle de caractères internes utilise un repli récursif de force 5
et un pseudo-compte de base de 0,1. Le score global conserve les poids
0,95 pour les mots et 0,05 pour les caractères avec espaces de phase 20,
puis ajoute les contributions des mots inconnus. **C'est un score pondéré,
pas une probabilité normalisée d'un texte** ; les informations de longueur
et de terminaison se recouvrent partiellement.

Le découpage dynamique examine tous les mots possibles jusqu'à 24 lettres,
sans faisceau tronqué. Ses états conservent les deux classes lexicales
précédentes et la distinction entre dernier mot d'une lettre ou plus long.
Cette distinction est nécessaire : deux mots inconnus ont le même identifiant
lexical mais peuvent laisser des contextes de caractères différents.

La comparaison oppose donc deux configurations complètes : le modèle fermé
de phase 20 et ce modèle ouvert. Elle n'isole pas causalement un seul changement,
puisque le vocabulaire et les probabilités lexicales sont aussi réappris.

## Nouveaux contrôles et règle de passage

Six extraits par langue, environ 250, 500 et 1 000 lettres pour apprendre la
clé, deux extraits par taille. Chaque clé est ensuite appliquée sans changement
à environ 500 autres lettres, séparées du premier passage par 50 mots.
Les nouveaux passages sont disjoints entre eux et excluent les passages de
phase 20 avec une marge de 50 mots. Les positions sont tirées parmi tous les
débuts admissibles de six intervalles disjoints dans chaque œuvre ; aucun
score ne choisit les textes. Les douze nouvelles clés diffèrent aussi de
celles de phase 20.

L'initialisation reprend le code figé de phase 20 : 16 recherches de
60 000 propositions avec score de quatre caractères. Jusqu'à deux clés
distinctes **sur les signes effectivement observés** initialisent chaque
bras. Cette règle évite de compter plusieurs clés équivalentes sur le texte
visible. Les deux bras évaluent tous les 325 échanges de deux lettres, au
plus deux fois par point de départ ; ils s'arrêtent si aucun n'améliore le
score. Le budget est réduit face aux quatre départs/six tours de phase 20,
et identique pour les deux bras de cette nouvelle expérience. Un pilote
de durée sur un ancien contrôle a précédé le gel.

Seul le premier passage chiffré entre dans la recherche de clé. Les clés
finales des deux bras sont enregistrées avant lecture des vérités d'évaluation.
L'évaluation recalcule aussi les espaces avec les lettres correctes, après
les ajustements, pour séparer les limites de clé de celles du découpage.

Le modèle ouvert doit atteindre **sur chacun des douze passages de transfert** :
au moins 95 % de lettres correctes et F1 des espaces d'au moins 0,90.
Un échec interdit une application interprétée au Voynich avec cette
configuration. Même un succès dans cette famille demanderait encore une
comparaison aux générateurs sans message et une validation des hypothèses
sur les unités graphiques. Aucun script de cette phase ne lance de calcul
sur le manuscrit.

## Vérification et reproduction

Les 32 tests courts de développement vérifient le moteur C++, un programme
dynamique Python distinct et une énumération exhaustive de 4 096 découpages.
L'étude réservée est ensuite contrôlée par reconstruction des chiffrés,
nouveau calcul des scores et métriques, recomposition exacte des extraits
sources et recalcul Python des optimums de segmentation du modèle ouvert.
Les données et modèles restent communs : ce n'est pas une réplication externe.

Python 3, NumPy et C++17 suffisent. Matplotlib sert au rapport graphique.

```sh
python3 tools/hydrate.py
python3 voynich_phase21/src/study.py prepare
python3 voynich_phase21/src/study.py fit
python3 voynich_phase21/src/study.py evaluate
python3 voynich_phase21/src/verify.py
```

`prepare` reconstruit les modèles et chiffrés sans modifier les fichiers de
phase 20. Pour refaire les recherches de clé, utiliser une copie du dépôt
et y déplacer préalablement `voynich_phase21/results/controls/`.
Une sortie déjà présente n'est relue que si les empreintes du protocole,
du modèle, du programme et des entrées concordent. Les modèles et exécutables
restent dans `tmp/`, exclu de Git.

## Attribution

Adaptation du travail de phase 20 et du score combiné de Bradley Hauer,
Ryan Hayward et Grzegorz Kondrak,
[« Solving Substitution Ciphers with Combined Language Models », COLING 2014](https://aclanthology.org/C14-1218/).
Le programme ajoute ici une représentation de mot inconnu et une nouvelle
calibration ; il ne reproduit pas leur MCTS. Les nouveaux scripts sont sous
CC BY-SA 4.0, comme les adaptations de phase 20. Voir les
[attributions d'origine](../voynich_phase20/README.md#licence-et-attribution)
et la [notice du dépôt](../NOTICE.md). Aucun nouveau corpus externe n'est
téléchargé pour cette expérience.
