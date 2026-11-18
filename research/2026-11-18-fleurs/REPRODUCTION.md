# Reproduire les essais

Les scripts utilisent Python 3 et les deux fichiers IVTFF du dépôt dans `voynich_20261028/data`. Les cartes sources sont les photographies de Yale. Les fichiers CARTES_A.json et correspondance.json donnent les liens originaux, dimensions, codes et empreintes. Les deux lectures de chaque image et chaque convention de translittération sont publiées dans le dossier de l'essai concerné. Les numéros manuscrits éventuels restent visibles sur les cartes, mais les lecteurs n’ont pas reçu la correspondance des codes, les mots retenus ou les prédictions. [Publications des transcriptions](https://www.voynich.nu/transcr.html)

Depuis ce répertoire, avec DATA défini comme chemin absolu vers le dossier des transcriptions et OUT vers une destination de travail existante :

```sh
python3 -B protocole_initial/fleurs.py predire --donnees "$DATA" --sortie "$OUT/initial" --b protocole_initial/B.json
python3 -B protocole_initial/fleurs.py verifier --donnees "$DATA" --sortie "$OUT/initial" --b protocole_initial/B.json --c protocole_initial/C.json
mkdir -p "$OUT/corolles"
python3 -B corolles/tester.py --donnees "$DATA" --sortie "$OUT/corolles" --apprendre corolles/BC.json
python3 -B corolles/tester.py --donnees "$DATA" --sortie "$OUT/corolles" --apprendre corolles/BC.json --evaluer corolles/A.json
python3 -B position_qotor/compter.py "$DATA"
```

Le premier mot candidat et les quinze prédictions sur les corolles sont consignés dans [PREDICTIONS.json](corolles/PREDICTIONS.json). Les décisions et le corrigé forment des fichiers distincts. Dans la branche de travail locale, 4269774 enregistre l'abstention initiale, 2d0539e fixe le nouveau dessin, 368cefe conserve les prédictions avant les images du cahier A et f21176d fixe le calcul hors des trois cahiers. La publication GitHub a été réalisée après les vérifications. On peut comparer les fichiers du rejeu aux JSON conservés dans les deux répertoires d'essai.
