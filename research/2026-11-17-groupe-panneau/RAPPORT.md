# Le groupe `oteos` sur le panneau f73r du Voynich

Nous avons prédit qu’un groupe entier, noté `oteos` en EVA, réapparaîtrait dans le quart supérieur gauche de l’inscription circulaire extérieure de f73r. La photographie le montre vers **9 h 54**, à la place annoncée. La prédiction supplémentaire de **deux occurrences entières sur ce cercle** reste incertaine. La seconde suite de signes est visible, mais deux éditions divergent sur le blanc qui la suit. [Planche annotée](../../docs/PIECES_REFERENCES.md#piece-9c995b59989a7d) · [Photographie originale de Yale](https://collections.library.yale.edu/iiif/2/1006206/full/full/0/default.jpg)

## Ce qui avait été annoncé avant ouverture

f73r est la photographie isolée qui suit immédiatement le panneau de la Balance précédemment étudié. Nous avons choisi le groupe sur les quatre panneaux déjà ouverts. Les trois plus proches fournissaient un précédent pour l’emplacement, dans le début de la ligne extérieure qui se lit dans le sens horaire. Le panneau le plus ancien, f72r3, fournit un contre-exemple. Un seul de ces quatre panneaux justifiait d’essayer la prédiction plus exigeante du doublon. [Protocole](PROTOCOLE.md) · [Prédiction originale](PREDICTION.json) · [Photographie des deux panneaux f72v3 et f72v2](https://collections.library.yale.edu/iiif/2/1006204/full/full/0/default.jpg)

| Panneau de départ | Groupes entiers `oteos` dans le cercle extérieur | Rang depuis le début choisi dans l’édition, ZL / IT |
|---|---:|---|
| f72r3 | 0 | La forme se trouve dans deux anneaux intérieurs. |
| f72v3 | 1 | 5 / 6 |
| f72v2 | 1 | 3 / 3 |
| f72v1 | 2 | 1 et 12 / 1 et 12 |

La cible et le secteur ont été fixés dans le commit local `f76f329` et la prédiction a été écrite dans la conversation avant l’ouverture. Nous avons utilisé l’orientation de la photographie de Yale et défini le quart de 9 h inclus à 12 h exclu par rapport au centre du diagramme. Le numéro de groupe dans une ligne ne suffit pas à fixer sa position sur la page. Dans la cible, la ligne extérieure est cataloguée `f73r.5,@Cc` et son début conventionnel est vers 11 h. Quatre inscriptions de figures la précèdent dans l’ordre du fichier.

## Les deux emplacements sur l’original

| Emplacement approximatif | Zandbergen–Landini (ZL) | Takahashi (IT, édition interlinéaire) | Vérification |
|---|---|---|---|
| **9 h 54**, quart supérieur gauche | `ykeydam.oteos.alar` | `ykeydom.oteos.alar` | Les deux éditions isolent le même groupe sur la photographie. Prédiction principale confirmée. |
| **12 h 43**, quart supérieur droit | `daraly.oteos,air,ar` | `daraly.oteos.air.ar` | La suite des signes est commune. IT compte un second groupe entier. ZL laisse incertaine la coupure après le dernier signe. |

Le point représente un espace retenu par le transcripteur, la virgule un espace incertain. Un peu plus loin, les deux éditions donnent également `oteosdal` en un seul groupe. La règle fixée avant ouverture excluait ce type de correspondance partielle. Dans les deux éditions, le dépouillement trouve **zéro** occurrence entière dans les deux anneaux intérieurs et dans les 30 étiquettes de figures. Les deux lectures ne donnent donc qu’une occurrence entière commune sur la page. [Conventions et éditions de la translittération](https://www.voynich.nu/transcr.html) · [Détail des lignes examinées](cible.json)

Les heures sont des repères de lecture approximatifs. Les milieux des deux formes se situent vers les pixels (380, 1300) et (1620, 825), depuis le coin supérieur gauche du cliché de 2834 × 3761 pixels. Les formes se trouvent nettement de part et d’autre de midi. [Coordonnées, lectures et décomptes](RESULTATS.json)

## Lecture de la photographie sans le groupe attendu

Deux lecteurs IA ont reçu séparément le même cliché anonymisé et les limites du secteur. Ils n’avaient reçu ni la forme recherchée, ni la cote, ni les transcriptions. Tous deux ont écrit spontanément `oteos` en lisant le troisième groupe visible de l’arc, de gauche à droite sur le déroulé. Leurs estimations placent le milieu du groupe vers 9 h 52, à environ deux minutes du repère de la planche. L’un propose `otees` comme variante de moindre confiance. Pour le groupe suivant, tous deux proposent `ylar`, tandis que les éditions ont `alar`. Cet écart illustre la limite de leur accord. Les deux lecteurs ont examiné le secteur annoncé ; la deuxième occurrence possible, au-delà de midi, a été vérifiée sur la photographie avec les deux éditions. [Lecture J](lecteurs/J.json) · [Lecture K](../../docs/PIECES_REFERENCES.md#piece-1f3fe158a9e950) · [Secteur déroulé, lecture J](../../docs/PIECES_REFERENCES.md#piece-debfb95eead037)

## Portée de l’essai

Sur un nouveau panneau, les panneaux voisins ont permis de prévoir une forme écrite et son emplacement. Le manuscrit est public et avait déjà été archivé par le projet. L’antériorité vaut pour cette prédiction, dans cette séance. Nous avons choisi la forme qui se répétait sur les pages de départ, puis testé un seul panneau. Cette observation ne mesure pas la fréquence des réussites fortuites et ne suffit pas à établir une règle pour tout le manuscrit. EVA sert ici à désigner les tracés. Leur sens, leur prononciation et la fonction de cette répétition restent inconnus.

## Refaire le décompte

Les fichiers dans `sources/` sont des extraits littéraux des lignes des cinq panneaux, issus de ZL 3b et d’IT 2a. Les empreintes des éditions intégrales sont consignées dans la prédiction. Les deux commandes ci-dessous reproduisent les relevés de départ et de cible. [Conventions IVTFF](https://voynich.nu/software/ivtt/IVTFF_format.pdf)

```sh
python3 essai.py depart --sources sources
python3 essai.py cible --sources sources
```
