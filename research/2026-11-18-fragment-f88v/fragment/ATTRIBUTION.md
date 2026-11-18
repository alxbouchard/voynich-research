# Quel petit dessin porte la légende f88v.3 ?

**Choix fixé sur la page source.** A est le deuxième fragment végétal de la rangée supérieure, après le récipient. B est le troisième. La légende tombe sous la feuille de A, entre l’axe de A et le col de B. L’ordre des inscriptions et les notices éditoriales favorisent A. Le parchemin laisse néanmoins B possible. [Plan de localisation](LOCALISATION.jpg) · [Photographie de la rangée, Yale](https://collections.library.yale.edu/iiif/2/1006233/80,70,2850,860/1200,/0/default.jpg)

## Décompte et vérification sur la rangée

| Objet de gauche à droite | Repère publié | Indice dans la photographie |
| --- | --- | --- |
| Récipient | f88v.1 | À gauche de tous les végétaux. Sa légende compte dans la numérotation des inscriptions. |
| Fragment 1 · V08 | f88v.2 dans l’ordre éditorial | Sa feuille large et crénelée domine la légende précédente. Sa tige est au-delà de l’axe de A lorsqu’on part de f88v.3 vers la gauche. |
| **Fragment 2 · V15 · A** | **f88v.3 dans l’ordre éditorial** | Sa feuille dentée s’étend à droite, au-dessus de f88v.3. |
| **Fragment 3 · V22 · B** | f88v.4 dans l’ordre éditorial | Le col strié de B est immédiatement à droite de f88v.3. Sa couronne verte rayonnante est au-dessus de f88v.4. |
| Fragment 4 · V03 | f88v.5 dans l’ordre éditorial | Sa base rouge dédoublée se trouve encore plus à droite, au-delà de B. |

Le centre approximatif de f88v.3 est **(1566, 419)** dans la photo de 9078 × 3777 pixels. Il n’y a pas de trait reliant la légende à une plante. Une association « sous la feuille » favorise A. Une association « inscription précédant le col » laisse B dans l’intervalle plausible. Le récipient et les deux fragments extérieurs sont plus éloignés. La table d’attaches conserve V15 et V22 pour ce locus, avec V15 pour la correspondance éditoriale LSI. [Table des attaches](../../2026-11-17-herbier-etiquettes-f88/documentation/ATTACHES.json) · [Positions des fragments](../../2026-11-17-herbier-etiquettes-f88/documentation/POSITIONS_V.json)

Chez Stolfi, la transcription ancienne de cette seule face conserve la succession f88v.t.2, f88v.t.3 et f88v.t.4. Son entrée f88v.t.3 porte `cpheor`. Dans son inventaire de légendes, ce locus reçoit une description de racines et de feuilles sombres, peu discriminante à elle seule. La notice de l’interlinéaire LSI place « plant [1,2] » avant f88v.3 et « plant [1,3] » avant f88v.4. L’indice [1,2] désigne la rangée 1, plante 2. Ces éditions apparentées documentent une même tradition d’attribution. La photographie vérifiée pour cette étude est celle de Yale. Les pages de Stolfi citées donnent des repères éditoriaux. [Stolfi, transcription de f88v](https://ic.unicamp.br/~stolfi/voynich/Notes/015/pages-html-old/f88v.html) · [Stolfi, inventaire des légendes](https://www.ic.unicamp.br/~stolfi/EXPORT/00-EXPORT/98-02-01-lotsa-labels/labels-a.html)

## Critères visuels fixés avant la comparaison

| Carte | Partie supérieure | Partie inférieure | Ce qui distingue le dessin |
| --- | --- | --- | --- |
| **A**, primaire | Une feuille visible, verte, allongée, à apex aigu et bord en dents. Elle part vers le haut à droite d’une tige pâle et fourchue. | Corps brun ocre en fuseau strié longitudinalement. Il se rétrécit, s’incurve vers le bas à gauche, puis se termine par plusieurs pointes minces, dont certaines repartent vers la droite. | Réunion sur un même axe de la feuille latérale dentée et du corps souterrain un peu renflé, courbé, à extrémité divisée. |
| **B**, alternative | Une forme verte à pointes rayonnantes prolonge vers la droite plusieurs traits pâles. Un petit col en éventail présente des stries serrées. | Petit renflement arrondi et partagé de part et d’autre, teinté de rouge. De longs filets rougeâtres se recourbent en replis presque horizontaux sous le renflement. | Réunion de la silhouette verte étoilée, du col strié et des filets recourbés en dessous. La proximité du quatrième dessin rend délicate la séparation de certaines extrémités basses. |

La couleur seule et la présence d’une tige ou d’une racine individualisent peu ces objets. La carte A ne montre qu’une feuille. Elle ne renseigne pas la disposition des feuilles sur une plante entière. Le mot « couronne » décrit seulement la silhouette de B. La page source laisse la nature botanique précise de cet organe ouverte.

## Cartes masquées et contrôle

Les cartes A et B ont été redimensionnées et présentées sous les codes T3 et T1 parmi les sept images anonymisées de l’épreuve. Le plan annoté se trouve à côté des cartes, dans ce dossier de documentation. Les polygones de détourage de l’inventaire du 17 novembre ont servi aux deux cartes. Les pixels extérieurs au dessin sont remplacés par un fond uni et les marges qui portaient les anciens codes V ont été enlevées. Chaque PNG conserve l’échelle et l’orientation natives du dessin. Les cartes ne contiennent aucune métadonnée textuelle.

| Carte | Dimensions | Boîte sur le cliché Yale (gauche, haut, droite exclue, bas exclu) |
| --- | --- | --- |
| A | 542 × 653 | (1143, 160, 1685, 813) |
| B | 656 × 653 | (1490, 179, 2146, 832) |

Le contrôle visuel sur la rangée et sur chacune des cartes confirme l’absence de signes visibles. Le rectangle contenant f88v.3, (1480, 363, 1655, 456), est entièrement hors des deux masques. Le contrôle par pixel a reproduit les deux PNG depuis le JPEG Yale téléchargé le 18 novembre 2026, identique au JPEG d’archive (SHA-256 `3b553c70d0c068cb39a276d391127165c5d9d868ec08e7f5eb2e73b32bb95d1e`). Les polygones manuels peuvent retrancher une frange de parchemin ou de pigment pâle au contour. [Photographie Yale en pleine définition](https://collections.library.yale.edu/iiif/2/1006233/full/full/0/default.jpg) · [Masques et empreintes des cartes](MASQUES.json) · [Script de vérification](verifier.py)

Pour reproduire le contrôle avec Pillow, lancer `python3 verifier.py image-yale-1006233.jpg` en indiquant le JPEG entier fourni par Yale.
