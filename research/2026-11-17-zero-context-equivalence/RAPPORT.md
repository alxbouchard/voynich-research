# Banc d’équivalence : critère strict non satisfait

Le 17 novembre 2026, la paire de la graine **51001** a exécuté deux trajectoires
de dix pas : modèle natif, puis candidat détachant les deux contextes. Les quatre
processus prévus pour cette paire sont terminés. Le comparateur a rendu
`EQUIVALENCE_NOT_ESTABLISHED` ; le lanceur de paire est sorti avec le code 2.
Conformément à la règle d’arrêt, **la graine 51002 n’a pas été commencée**.
Aucun réessai ni élargissement de tolérance n’a été effectué.

Les 103 événements enregistrés ont été comparés. Aucun tenseur capturé n’est
non fini. Les quarante gradients natifs des quatre paramètres de convolution
(quatre paramètres × dix pas) sont présents, finis et nuls. L’état initial et
les premières représentations avant rétropropagation coïncident. Cela ne suffit
pourtant pas : le premier écart non autorisé apparaît dans les gradients des
embeddings, à `step01_clip_raw`. Au total, 77 événements comportent un écart
non autorisé selon le comparateur gelé.

Une vérification séparée a authentifié et chargé les quatre checkpoints locaux
produits par ce banc, sans instancier de modèle. Elle confirme :

| Préfixe | Tenseurs de paramètres différents | Écart absolu maximal entre paramètres |
| --- | ---: | ---: |
| 1 pas | 5 sur 13 | 3,725290298461914 × 10⁻⁹ |
| 10 pas | 8 sur 13 | 1,214444637298584 × 10⁻⁶ |

Les autres champs de ces checkpoints — RNG, réglages, compteurs, valeurs globales
et état de l’optimiseur — coïncident. Les écarts du tableau portent sur les
**paramètres**, pas sur les vecteurs complets de gradients intermédiaires, qui
ne sont archivés que sous forme de descripteurs et d’empreintes. Le mécanisme
précis produisant ces différences n’a pas été établi par ce diagnostic.

La conclusion est limitée : ce candidat ne satisfait pas la promesse d’une
trajectoire identique bit à bit sur le contrôle exécuté. Ce n’est ni une
réfutation de toute optimisation du modèle, ni un résultat linguistique. Les
durées incluent l’instrumentation et ne démontrent pas un gain de vitesse.

Le modèle natif sera conservé pour la campagne de calibration à budget accru.
Aucune optimisation issue de ce banc n’y sera appliquée. Aucun texte du Voynich,
aucune annotation de cognat et aucun passage réservé n’ont été employés ici.

Les pièces principales sont `runs/51001/COMPARISON.json`, les deux `SUMMARY.json`,
`ZERO_GRADIENT_CERTIFICATE.json`, `AUDIT_CHECKPOINTS_ROOT.json` et les traces,
états RNG et checkpoints authentifiés. `PROTOCOL.json` conserve le statut de
préparation historique ; les fichiers `RUN.json` et le présent rapport décrivent
l’exécution effectivement terminée.

Une comparaison indépendante, implémentée séparément en bibliothèque standard,
reproduit les 77 événements divergents et le premier écart. Elle vérifie l’ordre,
les empreintes, les états RNG et les liens vers les checkpoints : voir
`AUDIT_ACTUAL_TRACES_INDEPENDENT.json`. La finitude des intermédiaires demeure
une propriété enregistrée par le worker figé ; leurs tableaux complets ne sont
pas archivés. Cette vérification n’est pas un nouvel entraînement.
