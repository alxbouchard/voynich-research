# Précision sur l’accès aux données et la portée des résultats

Le texte gelé du protocole et le champ `reason` de `results/SUMMARY.json` disent que les entrées manuscrites ne sont pas ouvertes après l’échec de calibration. Cette formulation est trop large : la fonction de contrôle d’intégrité lit leurs **octets pour vérifier les empreintes** avant le calcul. Elle ne les interprète pas comme observations et ne les transmet pas au modèle.

Le constat exact est : **aucune extraction, estimation de correspondance, prédiction ou évaluation sur le Voynich n’est exécutée par cette phase**. La branche d’analyse manuscrite est arrêtée par le critère gelé, et aucun résultat de cette branche n’est produit. Les fichiers gelés et leur formulation originale sont conservés ; aucun résultat ni critère de calibration n’est modifié par cette précision.

De même, les fonctions d’inférence reçoivent uniquement des observations chiffrées ; cela constitue une séparation des arguments et des étapes, pas un aveugle humain ni un isolement du système de fichiers. Les sources littéraires, clés de construction et réponses restent accessibles à l’opérateur.
