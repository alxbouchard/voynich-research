# Phase 18 : substitutions selon la position dans le mot

**Statut : projet préparé, non exécuté.** Aucun résultat, aucune clé et aucune traduction ne sont associés à ce document.

## Question

Une substitution qui change au début ou à la fin des mots permet-elle de récupérer un texte cohérent mieux qu'une substitution unique, sur des pages exclues de l'ajustement ?

## Deux familles proposées

1. Table initiale : une permutation pour le premier caractère de chaque mot, une autre pour les caractères restants.
2. Table finale : une permutation pour le dernier caractère de chaque mot, une autre pour les caractères restants.

Les mots d'un caractère appartiennent à la table de position dans chaque expérience. Ces deux variantes sont distinctes ; aucune troisième table initiale/finale combinée n'est prévue dans ce premier test. Les espaces restent ancrés. Les incertitudes créent des ruptures. Les unités seraient les caractères EVA littéraux, sans prétendre qu'ils correspondent chacun à un glyphe ou un son.

## Développement avant application réelle

Construire des contrôles latins et italiens avec clés cachées au solveur. Évaluer l'exactitude sur les caractères réservés et séparément sur les positions qui changent de table. Comparer avec la substitution unique. Une famille qui ne récupère pas les contrôles ne doit pas être appliquée au Voynich comme instrument validé.

## Validation à figer avant tout calcul

- Enregistrer les fichiers, les SHA-256, les graines, le budget, les seuils de calibration et la règle de séparation des feuillets physiques.
- Séparer ZL/IT et Currier A/B. Les deux faces d'un feuillet doivent rester dans le même ensemble.
- Choisir les clés sur l'apprentissage seulement ; conserver toutes les sorties et les échecs.
- Définir un témoin adapté : permuter l'ordre des mots ne détruit pas les positions internes des lettres et ne suffit donc pas, à lui seul, à tester ce mécanisme.
- Ne pas qualifier les pages de totalement inédites : elles ont été examinées dans le projet antérieur.

Ce fichier est un projet de protocole, pas une version définitive ni une préinscription. Il reste à fixer les paramètres, développer les contrôles et implémenter le calcul. La création du dépôt a précédé cette exécution.
