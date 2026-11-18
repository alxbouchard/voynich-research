# Phase 20 — contrôles à clé inconnue du solveur

**Étude exécutée : 1/12 contrôle passe les deux seuils ; aucun essai Voynich.**
Voir le [rapport complet](RAPPORT.md). Le protocole fixé avant calcul reste
décrit ci-dessous ; aucun paramètre n'a été adapté aux résultats.

## Protocole fixé avant génération et ajustement

Ce test fait suite au diagnostic de développement sur la phrase anglaise
du programme de Hauer, Hayward et Kondrak. Il évalue une **adaptation** :
initialisation par quatre caractères, puis recherche de clé avec score
combiné de mots et caractères et découpage exact. Ce n'est pas une
réplication du moteur MCTS des auteurs.

Le [protocole machine](CALIBRATION_PROTOCOL.json) fixe entrées, graines,
budgets et critères. Le gel est local dans Git avant la génération des
nouveaux chiffrés ; ce n'est pas une préinscription externe. L'analyste
connaît les œuvres sources par les phases précédentes. La clé et le texte
clair ne sont jamais donnés au programme de recherche de clé.

### Corpus et partition

- Modèle latin : César, texte normalisé de phase 10. Contrôles : Pline.
- Modèle italien : *Inferno* et *Purgatorio*. Contrôles : *Paradiso*.
- Six passages distincts par langue : environ 250, 500 et 1 000 lettres,
  deux passages pour chaque taille, avec douze permutations différentes.
- Pour chaque contrôle, un second passage d'environ 500 lettres est
  réservé au transfert de la clé, après une séparation de 50 mots.
  Les douze paires ne se chevauchent pas dans leur œuvre respective.
- Les positions de début sont tirées dans six intervalles disjoints par
  langue. Les limites de passages sont des limites de mots ; les longueurs
  exactes sont conservées. Tous les espaces intérieurs sont ensuite retirés.
- Les graphies normalisées héritées de phase 10 comprennent `j→i`, `k→c`
  et `w→uu`. Les résultats ne portent pas sur les graphies historiques brutes.

Les passages Pline et Paradiso ne servent pas à apprendre les modèles de
langue, le dictionnaire ou les coefficients. Ils ont toutefois été utilisés
dans d'autres phases : réservés à ce nouvel ajustement, ils ne sont pas
totalement inconnus du projet. La langue est fournie au solveur : ce test
n'est pas une identification de langue.

### Moteur et comparaison

L'alphabet comporte 26 lettres et la clé est une permutation bijective
unique, identique pour tous les caractères et pour les deux passages.
Cette famille ne couvre ni homophonie, ni syllabes, ni unités EVA composées.

Seul le premier passage chiffré entre dans la recherche de clé. Un score de
quatre caractères, appris sans espaces, initialise 16 recherches de 60 000
propositions. Jusqu'à quatre clés distinctes, choisies sur ce score,
initialisent ensuite deux bras : découpage glouton et découpage exact.
Chaque bras examine les 325 échanges possibles de deux lettres, choisit
le meilleur et recommence au plus six fois par point de départ. Un arrêt
anticipé est permis lorsqu'aucun échange n'améliore le score. Tous les
paramètres sont fixes ; le texte clair n'intervient pas dans l'arrêt.

Les deux bras emploient les mêmes modèles et coefficients publiés :
0,05 pour les caractères et 0,95 pour les mots. Les probabilités sont
apprises ici sur le corpus de la langue indiquée, pas sur les modèles anglais
NYT. Le dictionnaire est limité aux mots d'apprentissage et aux 26 lettres
isolées ; ces dernières reçoivent un pseudo-compte de 0,1. Les unigrammes
de caractères reçoivent aussi 0,1 pour garantir un score défini. Les
bigrammes et trigrammes sont des probabilités conditionnelles par contexte.
Les quatre caractères initiaux reçoivent 0,01 par type et utilisent le log
naturel de leur probabilité globale.

Le découpage exact conserve la position et les deux mots précédents ; il
n'élimine aucun état par un faisceau de taille limitée. Un mot absent du
dictionnaire doit être décomposé en fragments connus, au besoin en lettres
isolées. **C'est une limite testée, pas une gestion complète des mots inconnus.**

Les deux clés finales sont enregistrées avant toute évaluation. Elles sont
ensuite appliquées sans ajustement au passage réservé. Seules ses limites
de mots sont calculées avec le même modèle. Le meilleur résultat d'une
vérité connue n'est jamais choisi parmi les redémarrages.

### Mesures et règle de passage

Mesures : lettres correctement décodées ; précision, rappel et F1 des espaces
intérieurs ; correspondances de clé sur les signes observés. Les lettres
jamais observées ne sont pas présentées comme des clés identifiées.

Le bras exact doit atteindre, **sur chacun des douze passages de transfert** :

1. précision des lettres ≥ 95 % ;
2. F1 des limites de mots ≥ 0,90.

Un seul échec ferme le passage à une interprétation sur le Voynich avec
cette configuration. Ces seuils sont une règle opérationnelle de calibration,
pas une preuve statistique générale. Même un succès dans cette famille
imposerait encore de comparer les témoins sans message avant une conclusion
sur le manuscrit. Aucun test Voynich n'est lancé par ces scripts.

L'évaluation compare aussi le score de l'initialisation et un diagnostic
à lettres correctes connues, calculé **après** tous les ajustements. Si les
lettres correctes ont un meilleur score, cela signale une limite de recherche ;
si le modèle préfère un résultat erroné, cela signale une limite de son
objectif dans ce cas. Le découpage des lettres correctes mesure également
ce qui reste difficile même avec une clé parfaite. Ces diagnostics ne
changent pas les résultats du solveur.

### Vérification et reproduction

Le calcul C++ est comparé au programme d'origine sur l'exemple anglais,
puis à une énumération exhaustive sur 24 chaînes courtes. Après l'étude,
un second code Python reconstruit les chiffrés, les métriques et les scores,
et recalcule les optimums de segmentation des sorties exactes et des lettres
correctes. Cette vérification interne partage les sources et modèles.

```sh
python3 tools/hydrate.py
python3 voynich_phase20/src/calibration.py prepare
python3 voynich_phase20/src/calibration.py fit
python3 voynich_phase20/src/calibration.py evaluate
python3 voynich_phase20/src/verify_calibration.py
python3 voynich_phase20/src/audit_calibration_provenance.py
```

Python 3, NumPy et un compilateur C++17 sont nécessaires. Aucun nouveau
téléchargement n'est utilisé pour ces contrôles. `prepare` reconstruit les
modèles et chiffrés déterministes ; travailler dans une copie pour refaire
les ajustements, en y déplaçant d'abord `results/calibration/`. Une sortie
existante n'est réutilisée que si son identité de commande, d'entrées,
de protocole et de programme concorde. Les modèles et exécutables restent
dans `tmp/` ; les chiffrés, vérités d'évaluation et résultats sont archivés.

Pour reconstruire le rapport et les figures, ajouter Matplotlib et lancer
`python3 voynich_phase20/src/report_calibration.py` après la vérification.
L'intégrité des fichiers archivés se vérifie séparément avec
`python3 voynich_phase20/src/manifest.py`. Une nouvelle exécution peut modifier
les durées et métadonnées d'environnement ; l'inventaire existant décrit
les résultats publiés, pas toutes les réexécutions futures.

Les scripts et le nouveau moteur restent sous CC BY-SA 4.0 ; les attributions
et limites des corpus sont celles de la [notice de phase 20](README.md)
et de la [notice du dépôt](../NOTICE.md).
