# Vérifier la phase 37

Python standard uniquement. Les fichiers sources et les règles de calcul sont épinglés dans FREEZE.json. Le manifeste de livraison couvre aussi les résultats et le rapport ajoutés après les mesures.

Depuis ce dossier :

```sh
python3 -B src/manifest.py
python3 -B src/verify.py
python3 -B src/replay.py
```

Le vérificateur reconstruit les réponses et les décisions par une implémentation distincte. Il réécrit à l'identique le CSV et les preuves de vérification ; la réexécution crée ses cas dans un autre dossier temporaire et laisse intacts les cas livrés. Le manifeste peut être vérifié de nouveau ensuite.

La commande de développement `development/check_old_cases.py` nécessite le dossier frère `voynich_phase36`. Elle n'est pas requise pour vérifier ou reproduire les nouveaux résultats de cette livraison autonome.

Le script d'étude refuse de remplacer un résultat existant. Pour une modification de méthode, créer une nouvelle phase ou une copie de développement et conserver le résultat négatif actuel. Une modification de fichier figé fait échouer le contrôle d'intégrité.

La méthode de phase 36 et son résultat négatif sont conservés. Le nouveau comparateur ne modifie aucun fichier ancien. La restauration des archives 23–25 a nécessité l'extraction de leurs sous-dossiers de phase ; leurs enveloppes de livraison restent conservées dans `artifacts/restored_deliveries` du dépôt. Cette correction de chemins ne touche aucun octet figé de phase 37.
