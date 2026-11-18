# Développement avant la mesure réservée

Le premier apprentissage autorisait des sorties arbitraires de0 à8 lettres pour les signes marqués. L'inspection des seules données d'apprentissage a montré des sorties incompatibles avec les lettres visibles. La version retenue impose leur conservation, y compris les lettres suscrites représentées par des marques Unicode. Les alternatives faibles restent archivées, mais une valeur n'entre dans le lecteur qu'avec le soutien d'au moins deux groupes documentaires.

Une première empreinte FREEZE a été créée avant tout calcul réservé. Le commit n'a pas abouti parce que `git diff --check` signalait les fins de ligne CRLF de la carte tierce inchangée. Le lancement suivant s'est arrêté à l'analyse syntaxique de `study.py` (crochet manquant), avant toute lecture de données ou production de résultat. L'empreinte avortée est conservée dans PREFREEZE_ABORTED.json. Le crochet a été corrigé, les sources tierces gardées intactes et les fichiers Python compilés syntaxiquement avant le gel effectif. Aucun résultat réservé n'était disponible pendant ces corrections.

Les seuils, la partition, les règles et le modèle appris n'ont pas été ajustés à des cibles réservées.
