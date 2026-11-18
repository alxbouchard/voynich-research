# Où revient le groupe `oteos` dans les douze panneaux zodiacaux ?

**On compte 5 occurrences entières à l’intérieur et 6 à l’extérieur.** Les deux transcriptions les placent aux mêmes endroits sur les photographies. Les 24 anneaux intérieurs contiennent ensemble autant de segments délimités par des points que les 12 cercles extérieurs dans l’édition de Zandbergen–Landini. On obtient 5 occurrences pour 430 segments à l’intérieur (1,16 pour 100) et 6 pour 430 à l’extérieur (1,40 pour 100). La différence porte sur une seule occurrence. [Planche comparative](../../docs/PIECES_REFERENCES.md#piece-d28eb5895239c5) · [Relevé chiffré](RESULTATS.json)

## Les quatre quarts

Le quart est déterminé par le milieu du groupe sur le cliché de Yale, dans le sens horaire. Les heures servent de repères sur la page. La case frontière accueille les groupes dont le milieu se trouve à moins de 5° d’un axe, soit dix minutes sur le cadran. Ce seuil rend compte de l’imprécision du choix du centre et du milieu des tracés. [Règles et dénominateurs](METHODE.md)

| Position | Haut gauche, 9–12 h | Haut droit, 12–3 h | Bas droit, 3–6 h | Bas gauche, 6–9 h | À la limite des deux quarts du bas | Total |
|---|---:|---:|---:|---:|---:|---:|
| 12 cercles extérieurs | 5 | 1 | 0 | 0 | 0 | **6** |
| 24 anneaux intérieurs | 2 | 0 | 0 | 2 | 1 | **5** |

Les six occurrences extérieures se trouvent dans la moitié supérieure. À l’intérieur, deux sont dans la moitié supérieure et trois dans la moitié inférieure. Sur f72r1, la forme écrite chevauche l’axe de 6 h. Selon le centre retenu, le milieu du groupe se déplace de part et d’autre de cet axe. Il compte une seule fois dans la moitié inférieure. Ces décomptes par quart indiquent l’emplacement des groupes. La quantité de texte inscrite dans chaque quart n’a pas été mesurée. [Groupe sur l’axe de f72r1](../../docs/PIECES_REFERENCES.md#piece-103410f51a22ca) · [Photographie du dépliant comprenant f72r1](https://collections.library.yale.edu/iiif/2/1006203/full/full/0/default.jpg)

## Ce qui est compté

Le relevé contient les 36 inscriptions continues classées `@Cc` dans les douze panneaux zodiacaux. C1 longe la circonférence extérieure, C2 vient ensuite et le numéro augmente en allant vers le dessin central. Les étiquettes isolées auprès des personnages sont exclues. Un groupe entre dans le résultat commun lorsque Zandbergen–Landini (ZL) et Takahashi dans l’édition interlinéaire (IT) lisent exactement `oteos`, avec des limites certaines au même emplacement. Les voisinages ont été contrôlés sur les clichés. [Lignes et transcriptions utilisées](ANNEAUX.json) · [Conventions des éditions](https://www.voynich.nu/transcr.html)

| Rang du cercle en allant vers le centre | Cercles | Segments ZL | Occurrences communes |
|---|---:|---:|---:|
| C1, extérieur | 12 | 430 | 6 |
| C2 | 12 | 293 | 2 |
| C3 | 11 | 130 | 2 |
| C4 | 1 | 7 | 1 |

Un seul panneau possède un quatrième cercle. À l’intérieur, cinq anneaux répartis sur quatre panneaux portent le groupe. À l’extérieur, cinq cercles répartis sur cinq panneaux le portent. Aucun des douze panneaux ne présente une occurrence **commune aux deux éditions** dans les deux zones à la fois.

| Panneau | Cercle extérieur | Anneaux intérieurs |
|---|---|---|
| f70v2 | — | C3, vers 7 h 32 |
| f70v1 | — | — |
| f71r | — | C2, vers 10 h 31 |
| f71v | — | — |
| f72r1 | — | C3, sur l’axe de 6 h |
| f72r2 | Vers 10 h 07 | — |
| f72r3 | — | C2 vers 11 h 45 et C4 vers 6 h 17 |
| f72v3 | Vers 10 h 16 | — |
| f72v2 | Vers 10 h 11 | — |
| f72v1 | Vers 9 h 47 et 1 h 01 | — |
| f73r | Vers 9 h 54 | — |
| f73v | — | — |

Un tiret signifie qu’aucune occurrence entière commune n’est attestée dans les lectures disponibles. Des plis et quelques tracés pâles limitent la portée d’une conclusion d’absence. Les heures sont arrondies, et un groupe peut déborder sur un autre quart même si son milieu reste attribuable. C’est le cas de la forme de f72r3 à 6 h 17. [Coordonnées sur les photographies et pièces de vérification](POSITIONS.json)

## Que change le choix de la transcription ?

| Groupe entier selon chaque édition | Intérieur | Extérieur |
|---|---:|---:|
| ZL, tous les segments délimités par des points | 5 / 430 (1,16 pour 100) | 6 / 430 (1,40 pour 100) |
| IT, tous les segments délimités par des points | 7 / 489 (1,43 pour 100) | 7 / 466 (1,50 pour 100) |
| ZL, seulement les segments constitués de lettres simples | 5 / 360 (1,39 pour 100) | 6 / 365 (1,64 pour 100) |
| IT, seulement les segments constitués de lettres simples | 7 / 477 (1,47 pour 100) | 7 / 446 (1,57 pour 100) |

Les 430 segments sont des champs **éditoriaux** incluant les lectures difficiles et les coupures internes marquées comme incertaines. Le dénominateur de Takahashi change parce que les deux éditions ne placent pas toujours leurs séparations au même endroit. Une autre vérification accepte les virgules et les interruptions `<->` comme séparations supplémentaires. Elle donne 5/492 à l’intérieur et 7/474 à l’extérieur dans ZL, puis 7/494 et 7/469 dans IT. Aucun de ces choix ne donne une fréquence intérieure supérieure. [Spécification du format IVTFF](https://www.voynich.nu/software/ivtt/IVTFF_format.pdf)

Trois cas expliquent les différences. À l’intérieur de f72v3, près de midi, IT donne `oteos` là où ZL lit `oteor`. À l’intérieur de f72v1, vers 1 h 45, IT sépare `oteos.aiin` et ZL donne `oteo,r,aiin`. À l’extérieur de f73r, vers 12 h 43, les signes concordent et la coupure reste discutée. IT sépare `oteos.air.ar` et ZL écrit `oteos,air,ar`. [Relevé du dépliant f72](lectures/milieu/lectures.json) · [Relevé de f72v1 et de f73](lectures/fin/lectures.json)

## Portée de la comparaison

Les quatre panneaux utilisés pour choisir le groupe apportent quatre occurrences extérieures et deux intérieures. Le contrôle antérieur sur f73r ajoute une occurrence extérieure commune. Sur les sept panneaux restants, on observe **trois occurrences intérieures et une extérieure**. L’ensemble des douze est donc un bilan descriptif. Le léger écart global et la concentration en haut à gauche sur le cercle extérieur ne démontrent pas une règle applicable à un autre texte. Aucun sens ni aucune prononciation n’a été attribué au groupe.

## Reproduire

Exécuter `python3 -B compter.py` depuis ce dossier. Le script relit les extraits des deux éditions, recalcule les effectifs et attribue les quarts à partir des coordonnées natives. Les huit photographies de Yale couvrent les douze panneaux, plusieurs étant sur le même dépliant. Les lecteurs visuels et le contrôle numérique ont travaillé séparément sur les mêmes sources. [Empreintes des transcriptions](CORPUS.json) · [Photographies de Yale](PHOTOGRAPHIES.json) · [Décompte indépendant](lectures/audit_numerique.json)
