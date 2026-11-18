# Peut-on prévoir le mot avant une finale en m ?

**Le modèle qui rapproche un *m* final d'un *r* a prédit le mot entier `chedy` sur f103v.6.** Dans le cahier d'essai, la ligne finit effectivement par `chedy qokam`. Sur f34v.5, une ligne de l'apprentissage contient `chedy qokar`, puis encore deux mots. Les photos montrent les deux groupes au même endroit relatif, avec des signes terminaux différents. Cette réussite compte pour une seule cible. Sur les 84 cibles où les quatre modèles ont donné une réponse, le modèle *r* a réussi deux fois, les trois autres une fois chacun. [Photographies rapprochées](paire.jpg) · [F. 34v, source Yale](https://collections.library.yale.edu/iiif/2/1006141/1712,682,368,115/full/0/default.jpg) · [F. 103v, source Yale](https://collections.library.yale.edu/iiif/2/1006255/2209,460,341,106/full/0/default.jpg)

## L'épreuve

Les données d'apprentissage comprennent 12 488 paires de mots adjacents lisibles et alignés dans quatre conventions de transcription des lignes P0, hors du dernier cahier. Dans 1 643 paires, le mot de droite termine la ligne physique. Le modèle de fond choisit `daiin`, l'avant-dernier mot le plus fréquent dans ce sous-ensemble (86 occurrences). Les autres modèles votent à partir du mot de droite ; le mot de gauche est prédit entier. Dans tous les cas, les deux mots doivent appartenir au même tronçon, sans saut de dessin ni de ligne. Une forme rare qui n'a fourni aucun exemple produit une abstention. [Règle fixée avant l'ouverture](AVANT.md) · [Programme](voisins.py)

Sur le cahier T, **193 annonces** ont été figées avant de lire les voisins. Leur empreinte SHA-256, communiquée avant l'ouverture, est `07b224b6e2e6752b66777d057302aa835fe91813af34ac90033274b152e1a0e0`. Le voisin exact concorde entre les quatre lectures dans **161 cas**. Les 32 autres sont exclus du score. L'exemple f103v.6 et les cinq mots annoncés pour cette cible ont aussi été communiqués avant sa vérification. [Fichier des annonces](ANNONCES.json.gz) · [Réponses et erreurs par locus](VERIFICATION.json.gz)

| Modèle | Réponses données / 161 | Exactes | Erronées | Abstentions | Exactes sur les 84 cibles communes |
|---|---:|---:|---:|---:|---:|
| Garder m | 86 | 1 | 85 | 75 | 1 |
| Remplacer m par r | 113 | 3 | 110 | 48 | 2 |
| Remplacer m par l | 102 | 1 | 101 | 59 | 1 |
| Remplacer m par iin | 106 | 1 | 105 | 55 | 1 |
| Fond, `daiin` | 161 | 2 | 159 | 0 | 1 |

Sur les 84 cibles communes, changer *m* en *r* modifie la réponse à 37 endroits. Un seul changement améliore la réponse, sur f103v.6 ; dans les 36 autres, les deux réponses restent fausses. Sur toutes les cibles évaluables, *r* gagne également f105r.34, où il prédit `ar` devant `alkam` tandis que l'identité s'abstient. L'apprentissage ne comportait que deux voisins pour cette dernière classe, et un seul était `ar`. Le modèle *l* ne gagne ni ne perd aucune réponse exacte par rapport à l'identité. Le modèle *iin* gagne f114v.16 et perd f105r.24.

**Les 26 formes finissant précisément en `dam` donnent une réponse exacte par modèle, y compris pour le fond.** L'identité donne 12 réponses et en manque 11. Les modèles *r*, *l* et *iin* donnent respectivement 14, 15 et 14 réponses et se trompent respectivement 13, 14 et 13 fois. Pour les six occurrences du mot `dam` lui-même, toutes les règles répondent et chacune réussit exactement une fois. À f114v.16, *iin* trouve `chol` ; à f105r.24, le voisin est `daiin` et cette même règle annonçait `chol`.

## La paire sur les photographies

Le choix du cas à illustrer suit la règle écrite avant ouverture. Dans l'ordre des folios, f103v.6 est le premier gain d'une substitution face à l'identité avec une paire d'apprentissage effectivement écrite sous la forme substituée. L'alignement de f34v.5 donne `kair chedy qokar chekaly cholky`. Le passage de f103v.6 donne `shedy qokaiin chedy qokam`. Dans la photographie du premier, le dernier signe transcrit *r* possède un crochet et un retour court. Dans la seconde, le signe transcrit *m* présente une petite boucle haute et un jambage descendant. Les lecteurs H et ZL concordent localement sur les deux bigrammes. Les graphies et leur position se vérifient directement ; leurs valeurs sonores ou grammaticales ne peuvent pas se déduire de cette paire. [Ligne entière de f34v.5](https://collections.library.yale.edu/iiif/2/1006141/716,676,1844,119/full/0/default.jpg) · [Ligne entière de f103v.6](https://collections.library.yale.edu/iiif/2/1006255/646,452,1924,123/full/0/default.jpg)

Pour f103v.6, la classe *r* a donné dix votes à `chedy` sur 89 paires d'apprentissage. L'identité annonçait `chdam` (2/10), *l* annonçait `qokeedy` (7/108), *iin* annonçait `shedy` (11/106). L'apprentissage et la réserve portent sur le même manuscrit ; des mots ou des motifs de page peuvent se répéter. Le corpus vérifie la proximité sur une ligne matérielle, sans fournir de frontières de phrases linguistiquement établies. Deux succès sur 84 places communes ne suffisent pas à établir une équivalence entre *r* et *m*.

Pour reproduire, exécuter `python3 -B voisins.py annoncer`, puis `python3 -B voisins.py verifier`. La photographie est un montage de deux JPEG natifs de Yale. Les télécharger comme `1006141.jpg` et `1006255.jpg`, puis lancer `python3 planche.py DOSSIER`. Le script vérifie les empreintes avant de découper. [Source Beinecke MS 408, f. 34v](https://collections.library.yale.edu/iiif/2/1006141/full/full/0/default.jpg) · [F. 103v](https://collections.library.yale.edu/iiif/2/1006255/full/full/0/default.jpg) · [Coordonnées et programme photographique](planche.py)
