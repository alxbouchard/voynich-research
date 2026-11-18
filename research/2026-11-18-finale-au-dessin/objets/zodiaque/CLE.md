# Clé et localisation des cartes du zodiaque

La planche de lecture est `cartes.png`, SHA-256 `3c787d155589ab6cefe7cd763f9727fa602a9246daee8d5bdea07818f4dc7164`. Les lecteurs reçoivent uniquement cette planche avec pour consigne de juger le troisième signe de chaque groupe comme **o**, **a** ou **indécidable**, en précisant le trait visible. Les deux modèles étiquetés en haut viennent de sites distincts des cinq épreuves. La clé distingue trois lectures en désaccord et deux contrôles dont la graphie est identique dans les deux éditions. La transcription EVA donne un nom conventionnel aux tracés. [IT](../../../../voynich_20261028/data/IT2a-n.txt) · [ZL](../../../../voynich_20261028/data/ZL3b-n.txt)

| Carte | Fonction | Lieu | Position et vérification du lieu | IT | ZL |
|---|---|---|---|---|---|
| A | Épreuve | f73r.1 | Scorpion, 11 h 15. Première des quatre figures hors du grand cercle, au-dessus de celui-ci. La deuxième porte `chockhy`. | otoly | otaly |
| B | Contrôle o | f75v.37 | Bains, groupe inférieur de la paire à droite de la dernière figure du bassin du milieu. | otoly | otoly |
| C | Épreuve | f72v3.32 | Lion, 9 h 30, bande intérieure des figures. Après le groupe de 8 h 30, cette inscription porte un deuxième élément `yty` sur la photographie. La carte s’arrête à la fin du premier élément pour isoler le troisième signe visé. | otoly.yty | otaly,yty |
| D | Contrôle a | f73r.6 | Scorpion, 11 h dans la première couronne complète des figures, sous la ligne circulaire qui la sépare des quatre figures supérieures. | otaly | otaly |
| E | Épreuve | f72v3.10 | Lion, 2 h 45, bande extérieure des figures. Sur le cliché, compter après le groupe de 1 h 30 terminé par `faiin` et le groupe de 2 h contenant le grand signe `k`. L’inscription suivante à 3 h 30 est `ofalals`. | otoly | ot[o:a]ly |
| Exemple o | Apprentissage | f84r.11 | Groupe médian du petit ensemble au-dessus des trois dernières figures, en haut de la page. | otoly | otoly |
| Exemple a | Apprentissage | f84r.47 | Groupe au bord droit du conduit ondulé, entre les bassins du milieu et du bas, à gauche de la prose. | otaly | otaly |

Les heures viennent des repères de ZL. Elles décrivent approximativement la place dans la suite. La mise en correspondance utilise également l’ordre des figures, les anneaux et les inscriptions voisines. Pour identifier l’épreuve E, le groupe précédent porte lui-même une voyelle litigieuse dans les éditions (`okoly/okaly`). La lecture de cette voyelle n’intervient pas dans sa localisation. Le contraste sur la photographie du Lion est faible, principalement au début du groupe de la carte C. Les positions sont repérables même quand le choix du signe reste difficile. Le groupe de f72v3.32 présente en outre une coupure douteuse dans ZL. Une réponse sur son troisième signe ne décide pas de ce blanc.

## Sources et recadrages

Toutes les vues proviennent de Beinecke MS 408. Les rectangles ci-dessous sont exprimés en pixels dans le cliché entier, selon l’ordre gauche, haut, droite exclue, bas exclu. L’angle en degrés est la rotation antihoraire appliquée au rectangle avant le cadrage final. Les deux régions des bains conservées dans le dossier voisin sont déjà à l’échelle native. Le petit détail d’apprentissage près du conduit a été relu sur le JPEG IIIF natif. Les coordonnées des coupes finales et des flèches, les URL IIIF divisées par identifiant/région et les empreintes SHA-256 des cinq JPEG sources sont consignées dans le programme. Les quatre vues ont des identifiants différents, deux régions provenant de la même vue de f84r. Les flèches se trouvent dans la marge sous l’image. Chaque pixel du cadrage final est agrandi par deux, sans retouche de contraste. Les rotations obliques emploient l’interpolation bicubique. [Programme de recadrage](produire.py) · [Manifeste Yale](https://collections.library.yale.edu/manifests/2002046)

| Carte | Rectangle préparatoire dans le cliché entier | Rotation | JPEG de départ |
|---|---|---:|---|
| A | 873, 550, 1021, 654 | 0° | [Scorpion, Yale 1006206](https://collections.library.yale.edu/iiif/2/1006206/full/full/0/default.jpg) |
| B | 2145, 1590, 2294, 1675 | 0° | [Bains, Yale 1006209](https://collections.library.yale.edu/iiif/2/1006209/1840,1250,520,800/full/0/default.jpg) |
| C | 1630, 1320, 1855, 1580 | −63° | [Lion, Yale 1006204](https://collections.library.yale.edu/iiif/2/1006204/full/full/0/default.jpg) |
| D | 822, 1012, 1004, 1152 | −25° | [Scorpion, Yale 1006206](https://collections.library.yale.edu/iiif/2/1006206/full/full/0/default.jpg) |
| E | 3250, 1720, 3410, 1860 | +90° | [Lion, Yale 1006204](https://collections.library.yale.edu/iiif/2/1006204/full/full/0/default.jpg) |
| Exemple o | 1898, 404, 2043, 494 | 0° | [Bains, Yale 1006226](https://collections.library.yale.edu/iiif/2/1006226/1550,190,900,700/full/0/default.jpg) |
| Exemple a | 120, 2180, 260, 2291 | 0° | [Conduit, Yale 1006226](https://collections.library.yale.edu/iiif/2/1006226/55,1970,360,645/full/0/default.jpg) |
