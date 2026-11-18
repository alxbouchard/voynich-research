# Refaire les comptages

Le dossier de données du dépôt voynich-research est `voynich_20261028/data`. Les fichiers principaux sont IT2a-n.txt (Takahashi) et ZL3b-n.txt (Zandbergen–Landini). Les catégories d'objets et les limites de mots proviennent des éditeurs de ces transcriptions. Les deux éditions traitent le même manuscrit. [Éditions et conventions](https://www.voynich.nu/transcr.html)

Depuis le dossier de cette étude, définir DEPOT comme chemin absolu de la copie de voynich-research. Les commandes utilisent Python 3. Le script des recadrages utilise aussi Pillow. Le premier sous-programme fixe les candidats, le second vérifie que ces candidats correspondent au fichier conservé avant de les compter sur les autres feuillets.

```sh
python3 -B etiquettes.py apprendre --donnees "$DEPOT/voynich_20261028/data"
python3 -B etiquettes.py verifier --donnees "$DEPOT/voynich_20261028/data"
python3 -B occurrences.py --donnees "$DEPOT/voynich_20261028/data"
python3 -B prose/prose.py predire "$DEPOT/voynich_20261028/data"
python3 -B prose/prose.py evaluer "$DEPOT/voynich_20261028/data"
python3 -B prose/bifeuillet.py "$DEPOT/voynich_20261028/data"
python3 -B racines/rangees.py "$DEPOT"
python3 -B racines/prose.py "$DEPOT"
python3 -B herbier_1485/compter.py herbier_1485/corpus.json
```

Le script photographique prend en premier argument la racine du dépôt, puis un répertoire de sortie existant. Les images en entrée sont les fichiers Yale conservés dans voynich_phase25. Les empreintes et les coordonnées des trois détails sont consignées dans [le registre photographique](photos_okol/SOURCES.json).

Le protocole principal figure dans la révision locale `096eb83`. Les prédictions ont été enregistrées sous `fe29a82`, avant le comptage sur réserve. Les contrôles ajustés après examen sont signalés dans le rapport de chaque lot.
