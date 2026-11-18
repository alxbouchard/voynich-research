# Où se trouvent `oteos` et `oteey` sur les cercles hors du zodiaque ?

**Aucun des six diagrammes comparables ne réalise l’une ou l’autre des deux prédictions dans les deux transcriptions.** Leurs anneaux extérieurs contiennent deux `oteey` sur lesquels les éditions s’accordent. L’un se trouve en bas à droite, l’autre en bas à gauche. Aucun de ces anneaux ne porte de groupe entier lu `oteos` par l’une des deux éditions. [Planche photographique](../../docs/PIECES_REFERENCES.md#piece-21fe35c1fb547c)

## Ce qui était prédit avant l’ouverture

Sur les douze panneaux zodiacaux étudiés auparavant, la transcription Zandbergen–Landini (ZL) plaçait cinq des six `oteos` en haut à gauche et trois des six `oteey` en haut à droite. Pour tester si cette disposition s’étend à d’autres pages, nous avons retenu les huit premiers panneaux hors du zodiaque dont l’inventaire ZL signale de l’écriture circulaire. Les cotes et les types de lignes ont suffi pour les sélectionner.

Avant de consulter les images ou le texte de ces panneaux dans cette séance, nous avons inscrit pour chacun les deux mêmes prédictions sur le cercle écrit le plus extérieur du diagramme principal. Nous attendions au moins un `oteos` en haut à gauche et au moins un `oteey` en haut à droite. Le protocole demandait que chaque forme réussisse sur au moins deux panneaux et que son taux dans le quart annoncé dépasse celui de chacun des autres quarts. Les huit panneaux ont été conservés. Le registre et le protocole figurent dans le commit local `569d17e` du 17 novembre 2026 à 20 h 06, heure de Toronto. Le projet possédait déjà un atlas du manuscrit. [Registre des huit prédictions](PREDICTIONS.json) · [Protocole original](PROTOCOLE.md)

## Quantité de texte et occurrences

Un segment est une suite de signes délimitée par les points de la transcription ou par les bornes de la ligne. Le dénominateur principal inclut tous les segments ZL de l’anneau, même ceux qui portent une marque d’incertitude. Le numérateur exige que ZL et Takahashi (IT) lisent le groupe entier au même emplacement. Les numéros de segment peuvent différer entre éditions. Les milieux des groupes sont repérés sur les photographies de Yale, selon les rayons à midi, 3 h, 6 h et 9 h.

| Quart du cercle | Segments ZL | Segments IT | `oteos` communs | `oteey` communs | `oteey` pour 100 segments ZL |
|---|---:|---:|---:|---:|---:|
| Haut gauche | 62 | 65 | 0 | 0 | 0 |
| Haut droit | 64 | 61 | 0 | 0 | 0 |
| Bas droit | 58 | 60 | 0 | 1 | 1,72 |
| Bas gauche | 58 | 58 | 0 | 1 | 1,72 |
| **Total** | **242** | **244** | **0** | **2** | **0,83** |

Pour `oteey`, le quart annoncé présente **0 sur 64** en haut à droite, contre **2 sur 178** dans les trois autres quarts réunis, soit 1,12 pour 100. Pour `oteos`, on trouve **0 sur 62** en haut à gauche et **0 sur 180** ailleurs. Son absence sur les six anneaux empêche d’y estimer une préférence de position. [Résultats par panneau, quart et édition](RESULTATS.json)

## Lecture des huit panneaux

| Panneau | Inscription examinée | Segments ZL / IT | Observation sur le cercle principal |
|---|---|---:|---|
| f57v | f57v.2 | 47 / 51 | Aucun des deux groupes |
| f67r1 | f67r1.5 | 37 / 36 | Aucun des deux groupes |
| f68r1 | Médaillon excentré | — | Aucune circonférence écrite continue autour du diagramme principal |
| f68r2 | Deux médaillons excentrés | — | Aucune circonférence écrite continue autour du diagramme principal |
| f68r3 | f68r3.1 | 36 / 38 | Un `oteey` en haut à droite dans IT seul |
| f68v3 | f68v3.5 | 52 / 49 | Aucun des deux groupes |
| f68v2 | f68v2.6 | 32 / 32 | `oteey` en bas à droite dans les deux éditions |
| f68v1 | f68v1.1 | 38 / 38 | `oteey` en bas à gauche dans les deux éditions |

Sur **f68v2**, les éditions placent le même `oteey` au 16ᵉ segment, après `otychdy`, à environ 137° de midi dans le sens horaire. Sur **f68v1**, elles le placent au 32ᵉ segment, entre `shety` et `dair`, à environ 252°. Les deux groupes sont éloignés des limites entre quarts. [Agrandissement de f68v2](../../docs/PIECES_REFERENCES.md#piece-515274d9794485) · [Agrandissement de f68v1](../../docs/PIECES_REFERENCES.md#piece-540a96e5de81b6) · [Verso entier, Yale](https://collections.library.yale.edu/iiif/2/1006197/full/full/0/default.jpg)

Sur **f68r3**, la seule lecture qui va dans le sens prédit se trouve à environ 31° de midi. IT lit `oteey` au rang 13. ZL lit `choteey` au rang 12, entre les mêmes groupes voisins. La trace avant le `o` est trop pâle pour trancher. En retenant IT seul, le taux en haut à droite passe à **1/61** (1,64 pour 100), contre **2/183** dans le reste du cercle (1,09 pour 100). Il reste inférieur à celui du bas droit (1/60) et du bas gauche (1/58). Cela donne un seul panneau positif sur les deux demandés. [Photographie annotée du recto](../../docs/PIECES_REFERENCES.md#piece-510e9ad4cff9cd) · [Recto entier, Yale](https://collections.library.yale.edu/iiif/2/1006196/full/full/0/default.jpg)

Les trois inscriptions circulaires locales de f68r1 et f68r2 totalisent **24 segments dans chaque édition**. Nous les avons également examinées autour des centres de leurs propres médaillons. Elles ne contiennent ni `oteos` ni `oteey`. Ces deux panneaux restent non évaluables pour la prédiction sur le pourtour du diagramme principal. Le troisième cercle de f67r1 comporte par ailleurs une coupure discutée, IT donnant `oteos` et ZL `oteo.s`. Ce cercle intérieur était exclu par le protocole. [Médaillons et mesures du recto](lectures/f68-recto/axes.json) · [Détail de f67r1](../../docs/PIECES_REFERENCES.md#piece-e49a2697950e9a)

## Robustesse et portée

Trois segments des anneaux principaux ont un milieu assez proche d’un rayon pour justifier un second classement. Les huit combinaisons donnent, dans ZL, de 61 à 62 segments en haut à gauche, de 64 à 65 en haut à droite, de 56 à 58 en bas à droite et de 58 à 60 en bas à gauche. Aucun des deux `oteey` ne change de quart. Si l’on compte seulement les groupes transcrits entièrement en lettres simples, il reste 215 segments ZL et 241 segments IT. Les deux groupes communs sont toujours en bas. Un second calcul à partir des lignes des éditions et des relevés des axes reproduit ces chiffres. [Recomptage](lectures/recomptage.json) · [Affectation des segments aux quarts](AXES.json)

Sur ces six anneaux, la position remarquée dans le zodiaque ne se reproduit pour aucune des deux formes selon les critères annoncés. Avec deux occurrences communes au total et quatre des six anneaux sur le même dépliant, l'essai ne suffit pas non plus à établir une préférence de `oteey` pour le bas à l’échelle du manuscrit. Les relevés photographiques ont été réalisés avec l’aide d’agents IA et comparés aux deux éditions publiées. Les lettres EVA servent ici à désigner des formes graphiques.

## Refaire le comptage

Exécuter `python3 compter.py` dans ce dossier, avec Python 3 et sa bibliothèque standard. Le script vérifie l’empreinte du protocole enregistré, extrait les inscriptions, retrouve les groupes et leurs voisins, calcule les taux, puis réécrit les deux fichiers de sortie. Les identifiants et empreintes des quatre photographies permettent de retrouver les images intégrales. [Script](compter.py) · [Inscriptions retenues](CERCLES.json) · [Emplacements appariés](OCCURRENCES.json) · [Photographies de Yale](PHOTOGRAPHIES.json) · [Éditions des transcriptions](https://www.voynich.nu/transcr.html)
