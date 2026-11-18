# f101v.10 et le paragraphe sous les dessins

La photographie permet de situer la légende `okol` sur la moitié gauche du dépliant et de classer les trois paragraphes par distance. **Le plus proche, f101v.19–.21, ne donne aucune reprise entière de `okol`**, sur 32 positions où les deux éditions et les deux traitements du blanc incertain concordent. Il contient un voisin précis au treizième rang de .20. ZL transcrit `qokol` et H `qokol???` juste avant la lacune du pli. La forme visible dans chacune porte un signe supplémentaire devant `okol`. [Règle de sélection](REGLE.md) · [Prédiction consignée avant dépouillement](PREDICTION.md) · [Les deux parties du dépliant](deux-vues.jpg)

## Ce que les deux photographies restituent

La carte du visualiseur donne à .10 la boîte (0, 234, 0, 27), de largeur nulle. Le traitement automatique n'admet aucune des neuf lignes de prose P0 de f101v. Huit manquent à l'exigence d'ordre croissant des abscisses, une a des boîtes incomplètes. Les deux clichés natifs de Yale, 1006250 et 1006251, permettent de reprendre exactement le cadre déjà publié de la légende, de situer sur chaque moitié les neuf lignes et la dixième ligne centrée, et de délimiter trois blocs. La moitié droite de f101v occupe la partie gauche du second cliché ; les deux panneaux de f102r, visibles au-delà, sont exclus. Le texte se poursuit au-delà du pli, dont les bords sont endommagés. Les deux images de la planche sont présentées séparément pour conserver cette lacune. Le dépôt contient déjà l'examen de la lecture de .10 et de son dessin. La mesure des paragraphes et la prédiction de reprise sont l'apport de cette vérification. [Géométrie automatique du panneau](../CARTE-MASQUEE.json.gz) · [Cadre photographique initial de la légende](../../../2026-11-18-mots-et-dessins/photos_okol/NOTE.md) · [Description du dépliant de f101v](https://www.voynich.nu/q19/#f101v)

Sur le cliché natif de gauche, le centre du cadre de .10 est (917,5 ; 887,5). Sa projection verticale tombe dans les trois rectangles de prose. Du centre au bord du premier rectangle, nous mesurons environ 1 263 px. Le deuxième et le troisième sont à environ 1 524 et 1 738 px. Les rectangles sont relevés à vue : des lettres hautes montent dans l'interligne, mais une imprécision de 50 px sur chaque bord conserve le premier rang. Les deux éditions commencent des paragraphes à .19, .22 et .25. H isole .28 en une ligne courte de type Pc, tandis que ZL l'attache au troisième groupe. Les photographies récupèrent la géométrie des blocs et d'une légende ; la coordonnée de chaque mot au pli reste indéterminée. [Coordonnées et empreintes des deux JPEG](GÉOMÉTRIE.json) · [Yale, partie gauche](https://collections.library.yale.edu/iiif/2/1006250/full/full/0/default.jpg) · [Yale, partie droite avec f102r](https://collections.library.yale.edu/iiif/2/1006251/full/full/0/default.jpg)

## Couverture textuelle

| Emplacement | Positions strictement concordantes | Mots lisibles dans H | Mots lisibles dans ZL, blancs joints / séparés | `okol` entier |
|---|---:|---:|---:|---:|
| Lignes .19–.21, paragraphe prédit | 32 | 52 | 48 / 54 | 0 |
| Lignes .22–.24 | 3 | 58 | 48 / 54 | 0 |
| Lignes .25–.27 | 36 | 57 | 56 / 60 | 0 |
| Ligne décalée .28 | 2 | 7 | 7 / 9 | 0 |

Le test strict compare les graphies au même rang dans une ligne, d'où le faible nombre de positions retenues dans .22–.24 en présence de différences de segmentation en début de ligne. La recherche séparée dans chaque édition parcourt aussi tous les mots lisibles qui changent de rang. Elle donne également zéro, y compris en joignant .28 au dernier paragraphe. Le pli laisse des fragments illisibles dans plusieurs lignes ; le résultat porte sur les graphies que les sources permettent de contrôler. L'absence d'un mot entier observable ne résout pas la relation du dessin avec le texte. [Comptes par lecture, ligne et bloc](RESULTATS.json)

Exécuter `python3 depouiller.py` pour les effectifs. Pour la planche et les bornes des paragraphes, télécharger les deux JPEG natifs ci-dessus dans un même dossier, sous les noms `1006250.jpg` et `1006251.jpg`, puis exécuter `python3 cadrer.py DOSSIER` avec Pillow. [Calcul du texte](depouiller.py) · [Relevé des photographies](cadrer.py)
