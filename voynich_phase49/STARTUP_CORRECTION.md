# Correction avant lancement du transfert

Le premier lancement du programme de transfert s'est arrêté avant toute optimisation avec `KeyError: 'passed'`. Le vérificateur indépendant publie son résultat global sous `status: PASS`, alors que le lanceur cherchait un booléen `passed`.

Seule cette lecture de statut est corrigée. Aucun critère, passage, clé, score ni paramètre de recherche n'est modifié. Le gel initial de transfert est conservé dans `MANUSCRIPT_FREEZE_v1.json` ; le gel courant met à jour l'empreinte du lanceur et ajoute cette note. Aucun processus d'optimisation du manuscrit n'avait été créé par l'appel arrêté.
