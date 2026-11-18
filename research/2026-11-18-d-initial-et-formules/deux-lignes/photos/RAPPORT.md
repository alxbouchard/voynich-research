# Six lignes du manuscrit sur les clichés de Yale

## La prédiction sur f116r.17

Les deux lignes commencent par `dain chey`, puis le troisième groupe donne `qokeedy` sur f108r.20 et `qokeey` sur f116r.17. Après ces ouvertures, la suite annoncée pour la seconde ligne était `ch, o, l, ch, e, e, y`, avec une coupure facultative après le `l`. Sur la photo de f116r.17, le quatrième groupe commence par une boucle `o`. Takahashi (H) et Zandbergen–Landini (ZL) transcrivent tous deux la suite `okeey lain okeey qol chedy`. **Le premier des sept signes prédits échoue.** Les deux lignes, inclinées sur la page, figurent chacune en entier dans le cadrage. [Annonce préalable](../TRAITS-AVANT.md) · [Deux lignes entières et leurs transcriptions](deux-lignes.jpg) · [Original de f108r.20](https://collections.library.yale.edu/iiif/2/1006264/267,1282,1409,160/full/0/default.jpg) · [Original de f116r.17](https://collections.library.yale.edu/iiif/2/1006276/159,1071,1410,155/full/0/default.jpg)

Sur la ligne source f108r.20, H divise `chol.cheey`, ZL réunit `cholcheey`. Pour comparer le blanc avec ses voisins, nous avons relevé dans des bandes choisies sur cette ligne le plus long intervalle horizontal de colonnes sans pixel plus sombre que le seuil indiqué. Une unité correspond à un pixel de l’image Yale pleine résolution. [Détail du trait](blanc-f108r.jpg) · [Bornes des bandes, seuils et mesures](BLANCS.json)

| Intervalle mesuré | Seuil 110 | Seuil 125 | Seuil 140 |
|---|---:|---:|---:|
| `qokeedy` et `chol` | 62 | 60 | 53 |
| `chol` et `cheey` | 16 | 15 | 14 |
| `cheey` et `dalkar` | 64 | 63 | 60 |
| Intervalle intérieur de `cheey` | 15 | 13 | 6 |

Au seuil intermédiaire, les trois autres séparations relevées sur cette même ligne donnent 30, 40 et 33 pixels. La jonction disputée ressemble davantage au petit intervalle intérieur qu’aux deux espaces qui l’encadrent. Les fenêtres ont été placées à la main pour tenir compte de la pente de l’écriture. Ce constat géométrique porte uniquement sur ce lieu. La valeur linguistique d’un tel intervalle reste ouverte.

## Le mot qui suit sur deux feuillets de plantes

Sur f20r.6, `cheey daiin` se trouve aux rangs 4–5 entre `qotol` et `chy`. Sur f31r.2, `dcheey daiin` ouvre la ligne, puis vient `okeedy`. Les deux éditions s’accordent sur les quatre groupes concernés. Le petit signe supplémentaire se trouve avant la forme `cheey` en tête de ligne. La reprise de `daiin` est exacte et les suites de texte divergent dès le groupe suivant. [Deux lignes entières](deux-plantes.jpg) · [Original de f20r.6](https://collections.library.yale.edu/iiif/2/1006112/410,961,1722,134/full/0/default.jpg) · [Original de f31r.2](https://collections.library.yale.edu/iiif/2/1006134/223,500,1534,145/full/0/default.jpg)

## Une étoile au début de f103v.37

Les deux autres lignes commencent par `saiin shey`, suivis de `qokeedy` sur f82v.36 et de `qokeey` sur f103v.36. La première continue par `qokar`, la seconde par `oshey`. Les deux transcriptions placent une fin de paragraphe à f103v.36 et un nouveau départ en .37. Sur f82v.36, toutes deux passent à .37 sans l’une ni l’autre marque et la longue ligne suivante commence par `sol chey`. La prédiction des deux fins de paragraphe réussit sur **une des deux lignes**. [Annonce préalable](../../fin-de-notice/AVANT.md) · [Deux lignes entières](deux-saiin.jpg) · [Original de f82v.36](https://collections.library.yale.edu/iiif/2/1006223/713,2408,1848,156/full/0/default.jpg) · [Original de f103v.36](https://collections.library.yale.edu/iiif/2/1006255/596,2301,1179,159/full/0/default.jpg)

Une étoile au cœur clair dans la marge gauche de f103v est centrée vers `(622, 2423)`. Le centre vertical du premier groupe de .37 se situe vers `2428`, entre ceux de .36 (`2358`) et de .38 (`2486`). Les branches débordent. L’attribution à .37 répond à la prédiction. Le début se lit `ol.shey` chez H, `olshey` chez ZL. La ligne .38 est sans étoile à sa hauteur. Une autre étoile au cœur rouge, vers `(630, 2598)`, correspond à .39. La photo présente les lignes .34 à .40 et la marge jusqu’au bord gauche du cliché. [Photographie avec numéros de lignes hors du tracé](etoiles-f103v.jpg) · [Cadrage Yale sans annotation](https://collections.library.yale.edu/iiif/2/1006255/0,2200,1520,509/full/0/default.jpg) · [Coordonnées des débuts de lignes et des centres des étoiles](ETOILES.json)

## Sources et reproduction

Les planches utilisent les images couleur du Beinecke MS 408 à Yale. Les images de repérage et les coordonnées des groupes de Voynichese.com servent à localiser le rang des mots dans l’image originale. Les boîtes peuvent se chevaucher et englobent du parchemin clair. Les mesures de blanc utilisent directement l’encre et le fond. Le manifeste conserve les deux transcriptions locales, les trois URL et les empreintes SHA-256 de chaque feuillet, les paramètres de recalage et les boîtes. [Manifeste](COORDONNEES.json) · [Programme](planche.py)

Pour reproduire les planches depuis le dépôt, télécharger les trois URL données pour chacun des six feuillets dans un même répertoire. Pour `f108r`, nommer ces fichiers `f108r-n.jpg` (Yale), `f108r-r.jpg` (image de repérage) et `f108r-l.json` (coordonnées, le fichier `.js` contient un tableau JSON). Appliquer la même convention aux cinq autres feuillets, puis exécuter `python3 -B planche.py /chemin/vers/les-sources` depuis ce dossier, avec Pillow, NumPy et OpenCV disponibles.
