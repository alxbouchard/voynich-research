# Phase 22 — correction prudente des mots fusionnés

La phase 22 conserve les clés et toutes les séparations trouvées par la phase 21.
Elle autorise des coupures supplémentaires soutenues par le contexte de lettres,
puis vérifie séparément les fusions corrigées et les fausses coupures ajoutées.
Aucun essai sur Voynich n'est prévu dans cette phase.

## Développement et gel

Le classifieur apprend uniquement sur les textes d'entraînement de phase 10
(César, puis Inferno/Purgatorio). Les 48 anciens passages des phases 20 et 21
servent au réglage : 24 configurations, à lettres connues. Le choix figé est
seuil 0,90 et poids 1 : six fusions corrigées, aucune fausse coupure ajoutée
sur ce développement. Ce seuil n'est pas une garantie de 90 % de justesse.

`PROTOCOL.json`, le code et les résultats de développement sont enregistrés
dans un commit avant de sélectionner les nouveaux passages et générer leurs clés.
Il s'agit d'un gel local vérifiable, pas d'un préenregistrement externe.

La validation utilise 12 nouvelles substitutions monoalphabétiques sans espaces
(6 latin, 6 italien), des passages disjoints des deux phases précédentes avec une
marge de 50 mots, et un transfert de 500 lettres minimum pour chaque clé.
La recherche des clés ne reçoit que le texte chiffré d'ajustement.
Les deux segmentations comparées utilisent exactement les mêmes lettres déchiffrées.

L'objectif strict est de corriger au moins une fusion dans chaque langue et de
n'ajouter aucune fausse coupure sur les passages de transfert. Le seuil général
reste au moins 95 % de lettres correctes et F1 des frontières au moins 0,90 dans
chacun des 12 cas. Les résultats avec la vraie clé sont des diagnostics séparés.

## Reproduction

Python 3 avec NumPy et compilateur C++17 ; Matplotlib pour les figures.
Les données d'entraînement et les sources historiques doivent être disponibles
aux chemins dont les empreintes sont fixées dans `PROTOCOL.json`.

```sh
python3 voynich_phase22/src/develop.py
# Le gel Git doit intervenir ici, avant prepare.
python3 voynich_phase22/src/study.py prepare
python3 voynich_phase22/src/study.py fit
python3 voynich_phase22/src/study.py evaluate
python3 voynich_phase22/src/verify.py
```

`prepare` refuse d'écraser une série de contrôles existante. Pour reproduire les
contrôles publiés, utiliser une copie de travail propre au commit de gel.
Les modèles et exécutables sont reconstruits dans `tmp/`, non redistribué.
Les commandes, empreintes d'entrées, résultats et vérités d'évaluation sont archivés.

Le programme Python indépendant recalcule les scores et les optima contraints.
Le développement inclut aussi des vérifications exhaustives sur de petites chaînes
et un contrôle indépendant de 256 contextes du classifieur. Il ne s'agit pas
d'une réplication par une équipe extérieure.

Les dérivations des phases 20 et 21 restent sous CC BY-SA 4.0 ; voir `NOTICE.md`.
