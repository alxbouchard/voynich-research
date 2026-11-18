# Le groupe `oteos` revient-il en haut à gauche des autres panneaux zodiacaux ?

**Une des sept prédictions est confirmée.** Sur f72r2, le groupe entier `oteos` se trouve sur le cercle extérieur vers 10 h 07. C’est la seule occurrence extérieure commune aux deux transcriptions sur les sept panneaux examinés. Les trois autres quarts en comptent chacun zéro. Le résultat reproduit l’emplacement déjà observé sur f73r une fois de plus, mais une seule occurrence dans cette série ne permet pas d’établir une préférence de position. [Planche photographique](../../docs/PIECES_REFERENCES.md#piece-bcd48dd94e8c70)

## Sept prédictions fixées avant ouverture

Nous avons retenu les sept panneaux restants sur les douze classés comme zodiacaux dans la transcription de Zandbergen–Landini. Les quatre panneaux qui ont servi à choisir le groupe, ainsi que f73r, ont été écartés du décompte. Pour chacun des sept autres, nous avons prédit au moins un groupe entier `oteos` sur la ligne de texte la plus extérieure, dans le quart de 9 h inclus à midi exclu. Le protocole et les sept prédictions ont été enregistrés dans le commit local `f5f737e` et annoncés dans la conversation avant la consultation des sept inscriptions. [Prédictions originales](PREDICTIONS.json) · [Protocole](PROTOCOLE.md)

| Cercle extérieur | Haut gauche, 9–12 h | Haut droit, 12–3 h | Bas droit, 3–6 h | Bas gauche, 6–9 h |
|---|---:|---:|---:|---:|
| f70v2 | 0 | 0 | 0 | 0 |
| f70v1 | 0 | 0 | 0 | 0 |
| f71r | 0 | 0 | 0 | 0 |
| f71v | 0 | 0 | 0 | 0 |
| f72r1 | 0 | 0 | 0 | 0 |
| **f72r2** | **1** | 0 | 0 | 0 |
| f73v | 0 | 0 | 0 | 0 |
| **Total** | **1** | **0** | **0** | **0** |

Chaque case compte les occurrences certaines sur la portion photographiée du cercle pour lesquelles Zandbergen–Landini (ZL) et Takahashi (IT, édition interlinéaire) donnent au même endroit un groupe entier identique. Les quatre quarts ont été parcourus. Les classements par nombre d’occurrences et par nombre de panneaux donnent ici le même résultat. Le haut gauche arrive seul en tête parce qu’il contient l’unique occurrence. Les six autres panneaux n’apportent aucune information permettant de départager les quarts. [Décompte intégral et transcriptions](RESULTATS.json) · [Éditions de référence](https://www.voynich.nu/transcr.html)

## Retrouver le groupe sur la page

Sur le grand dépliant, f72r2 est le troisième diagramme en partant de la gauche, avec deux personnes au centre. En remontant son bord gauche dans le sens horaire, la suite se lit `otees | oteos | aiin`. Elle traverse le point de départ conventionnel retenu pour transcrire l’anneau. Ainsi, `otees` termine la ligne écrite dans le fichier et `oteos` la commence. On peut cependant voir les trois groupes côte à côte sur la même photographie. Le cercle extérieur est le lieu `f72r2.6,@Cc`, après cinq étiquettes transcrites séparément. [Dépliant original de Yale](https://collections.library.yale.edu/iiif/2/1006203/full/full/0/default.jpg) · [Tracé et voisins](../../docs/PIECES_REFERENCES.md#piece-e7dcfa7a709d2f)

Deux contrôles séparés sur l’image de 8865 × 3018 pixels placent le milieu du groupe vers (4396, 925) et (4398, 927), depuis le coin supérieur gauche. Les centres estimés du diagramme donnent respectivement 10 h 06 et 10 h 08. La petite différence ne modifie pas le quart. [Emplacements et coordonnées](POSITIONS.json) · [Vue native repérée](../../docs/PIECES_REFERENCES.md#piece-da97a1ec547516)

Un autre lecteur IA a reçu le seul extrait photographique, sans cote ni forme attendue. Il a proposé spontanément `otees oteos ain`, avec `aiin` comme autre lecture pour le troisième groupe. Cette lecture libre retrouve le groupe prédit et laisse apparaître l’incertitude sur le nombre de petits traits dans le groupe voisin. [Extrait sans annotation](../../docs/PIECES_REFERENCES.md#piece-7248fee8cac825) · [Lecture originale](lectures/lecture_bande_anonyme.json)

## Cas qui changeraient le décompte si l’on changeait de règle

- **Formes plus longues.** Sur le cercle extérieur de f70v1, ZL et IT donnent `oteoshey` vers 11 h 40. Les deux éditions écrivent ce groupe d’un seul tenant. Sur f71v vers 6 h 47, ZL donne `oteoshar` et IT `oteochor`. Aucune des deux lectures n’isole `oteos`. Accepter toutes les virgules comme des coupures laisse les quatre totaux inchangés. [f70v1, Yale](https://collections.library.yale.edu/iiif/2/1006201/full/full/0/default.jpg)
- **Autres anneaux.** Les deux transcriptions placent un `oteos` entier dans un anneau intérieur de f70v2, f71r et f72r1. Elles en donnent aussi un dans une étiquette de f71r. Les inclure aurait changé la question posée. [f70v2, Yale](https://collections.library.yale.edu/iiif/2/1006200/full/full/0/default.jpg) · [f71r, Yale](https://collections.library.yale.edu/iiif/2/1006202/full/full/0/default.jpg)
- **Limites de lecture.** À droite de f71v, la reliure gêne la lecture du cercle entre environ 2 h 30 et 3 h 30. Sur f71r une tache atteint un groupe, et sur f72r2 un long intervalle apparaît au pli droit. Le bas du cercle de f73v est plus pâle. Un zéro signifie qu’aucune occurrence entière commune n’est attestée dans les lectures disponibles. [f73v, Yale](https://collections.library.yale.edu/iiif/2/1006207/full/full/0/default.jpg) · [Audit des sept cercles](../../docs/PIECES_REFERENCES.md#piece-fe2e0597cbddf3)

## Portée

Le test portait sur sept inscriptions nouvelles pour cette prédiction positionnelle. Les photographies sont publiques et le projet avait déjà constitué un atlas du manuscrit. Trois panneaux, dont le seul positif, figurent sur un dépliant déjà affiché dans l’expérience précédente. Les résultats indiquent qu’une répétition à cet endroit est possible et que la prédiction échoue à se généraliser à six des sept panneaux. Les agents IA ont contrôlé des tracés sur un même fac-similé. Ces contrôles n’établissent ni un sens pour `oteos`, ni une règle d’écriture à l’échelle du manuscrit.

## Reproduire le calcul

Depuis ce dossier, exécuter `python3 -B depouiller.py`. Les deux extraits de sources contiennent les lignes des sept panneaux avec leurs commentaires. Le script reprend le lecteur IVTFF de l’essai précédent, vérifie les positions enregistrées, puis produit `RESULTATS.json`. La livraison autonome inclut le même lecteur sous le nom `lecture_ivtff.py`. [Conventions IVTFF](https://voynich.nu/software/ivtt/IVTFF_format.pdf)
