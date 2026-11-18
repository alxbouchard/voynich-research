# Reproduire l’expérience

Le protocole a été enregistré dans le commit local `b2bd110`. Les règles, le code de recherche de quatre formes et les valeurs à éprouver ont été enregistrés dans `d374dea` avant le calcul sur les paragraphes de réserve. Les originaux intégraux des éditions modernes de textes médiévaux restent disponibles auprès de leurs éditeurs.

## Décomptes et témoins

Depuis ce dossier, exécuter `python3 -B verifier.py` pour vérifier les photographies anonymisées par leurs empreintes et recompter les résultats publiés. Pour refaire les calculs des paragraphes à partir des sources, le répertoire `voynich_20261028/data` du dépôt contient les deux transcriptions. Les versions utilisées sont aussi disponibles en ligne. [Takahashi IT2a](https://www.voynich.nu/data/IT2a-n.txt) · [Zandbergen–Landini ZL3b](https://www.voynich.nu/data/ZL3b-n.txt)

Le premier argument de la commande suivante est le chemin du fichier HTML local. L’option de téléchargement le récupère si nécessaire. Le répertoire de destination contiendra les notices, les identifiants anonymes et la clé séparée.

```sh
python3 etalons/tacuinum/extraire.py tacuinum.html corpus-latin --download
python3 -B verifier.py --transcriptions ../../voynich_20261028/data --latin corpus-latin/notices.json
python3 etalons/tacuinum/calibrer.py train corpus-latin
python3 etalons/tacuinum/calibrer.py test corpus-latin
```

Pour le *Viandier*, travailler dans une copie de `etalons/viandier`. Placer les deux éditions HTML de Giessen dans ce dossier sous les noms `sion.html` et `vatican.html`. L’extraction utilise le module Python `lxml`. Pour la relancer, exécuter successivement `python3 extraire.py`, `python3 apparier.py prepare`, `python3 apparier.py predict`, puis `python3 apparier.py evaluate`. Le fichier `GEL.sha256` donne les empreintes des sources et des listes figées. La note du témoin explique la correction du découpage et distingue les scores avant et après cette correction. [Édition de Sion](https://www.uni-giessen.de/de/fbz/fb05/germanistik/absprache/sprachverwendung/gloning/tx/viandier-sion.htm) · [Édition du Vatican](https://www.uni-giessen.de/de/fbz/fb05/germanistik/absprache/sprachverwendung/gloning/tx/vi-vat.htm)

## Photographies

Les vues de f103r et f116r proviennent du Beinecke MS 408. Le dossier `photos/f116r` donne la planche masquée, ses cartes individuelles, les deux lectures indépendantes et les coordonnées dans les JPEG de Yale. Chaque rectangle est défini par ses bords gauche, haut, droit exclu et bas exclu. Les modèles proviennent de f15v, les six cartes du f116r. Les deux lecteurs ont reçu la seule planche masquée. Ils peuvent partager des biais de reconnaissance visuelle. [f103r](https://collections.library.yale.edu/iiif/2/1006254/full/full/0/default.jpg) · [f116r](https://collections.library.yale.edu/iiif/2/1006276/full/full/0/default.jpg) · [f15v](https://collections.library.yale.edu/iiif/2/1006103/full/full/0/default.jpg)
