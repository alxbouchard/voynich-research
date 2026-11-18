# Deux feuilles près d’un pot et deux mots dans le cahier final

Près du premier pot de f102v2, deux fragments végétaux de rangées différentes portent les légendes `otol` et `opchy` selon Takahashi. Au verso du folio 112, **les deux groupes se retrouvent à quatre mots d’intervalle**. Les deux transcriptions et la photographie permettent de situer cette rencontre. La lecture `otol` auprès du dessin 218 est débattue. Le rapprochement devient visible en tenant compte de cette lecture et d’un paragraphe dont les éditions placent la fin à des endroits différents. [Photographie des deux feuilles](rangees/f102v2-218-224.jpg) · [Photographie des deux lignes et de leur marge](rencontre112/NOTE.md)

## Ce que nous avions prédit

Un agent a relevé les groupes de dessins associés par la mise en page à un même récipient. Les inscriptions de deux objets distincts fournissaient une paire de noms possibles, à rechercher dans le texte situé sous les dessins, puis dans le cahier 20. Pour l’essai principal, les deux légendes devaient comporter un seul groupe d’au moins trois signes EVA, lu de la même façon dans les deux éditions. Dans la prose, les mots pouvaient se présenter dans l’un ou l’autre ordre, avec sept mots intercalés au maximum. Les mots incertains occupent toujours leur place. Nous avons enregistré les listes de prédictions et les résultats locaux dans des commits successifs avant d’ouvrir les passages de vérification. L’équipe connaissait déjà plusieurs de ces pages par d’autres recherches. [Protocole](PROTOCOLE.md) · [Table des 17 rangées](rangees/README.md) · [Prédictions principales](predictions.json) · [Prédictions par pot](predictions_pots_elargis.json)

| Terrain d’illustration | Paires distinctes annoncées | Testables dans leur paragraphe local commun | Retrouvées localement | Avec les deux mots présents quelque part dans le cahier, parmi les 261 notices communes | Retrouvées ensemble dans une des 261 notices |
|---|---:|---:|---:|---:|---:|
| 17 rangées, 72 fragments | 62 | 37 sur 7 rangées | 0 | 8/62 | 0 |
| 18 groupes de dessins quand on réunit les deux étages de f99r et f102v2, 89 fragments | 119 | 109 sur 9 groupes | 0 | 14/119 | 0 |

Les deux tableaux géométriques se recouvrent. Les unités comptées dans la prose locale exigent à la fois une paire lisible et un paragraphe dont les lignes sont les mêmes dans H et ZL. Deux rangées de f102 sont écartées de ce dernier dénominateur parce que les partitions diffèrent. Dans le premier terrain, 13 des 42 mots entrant dans au moins une paire sont attestés dans les 261 notices communes du cahier final. Sur le terrain élargi, on en retrouve 17 sur 53. Même en examinant le paragraphe entier, aucune des 62 ou des 119 paires n’y est reprise exactement. Les 261 notices couvrent 972 lignes sur 23 faces. Les huit paires dont les deux mots existent au premier essai restent réparties entre des notices différentes. Les transcriptions portent sur le même manuscrit. [Sortie locale](local.json) · [Sortie sur le cahier 20](notices.json) · [Sortie à géométrie élargie](notices_pots_elargis.json) · [Délimitations comparées](notices/NOTE.md)

La paire `otoldy`–`okol`, suggérée auparavant par une légende probable de pot et une inscription de fragment voisin, avait une épreuve à part. Les deux groupes n’apparaissent ensemble ni dans le paragraphe de cette rangée de f89r2 ni dans les notices contrôlées du cahier 20. Cette proposition mettait en jeu deux types d’objets différents. [Prédiction n° 7](PROTOCOLE.md) · [Photo du pot et incertitude de sa dernière lettre](../2026-11-18-noms-secteurs/plantes-recipients/pot89/NOTE.md)

## Ce qui se lit sur f102v2 et f112v

Sur f102v2, le fragment 218 est compact, vert, muni de pointes et d’une courte attache brun-rouge. Le 224 forme une touffe de lames étroites qui divergent au bout d’une tige fine. L’un se trouve au premier étage de dessins, l’autre au deuxième. Ces deux étages sont placés devant le même récipient. Aucun trait visible ne relie les deux fragments. Les éditions donnent toutes deux `opchy` près de 224. Pour 218, H lit `otol` et ZL `okol`. Avant cette expérience, deux lecteurs IA à qui l’on avait présenté des signes anonymisés avaient indépendamment choisi le signe transcrit `t`. La photographie favorise donc `otol`. Elle laisse ouverte l’espèce, l’usage et la fonction de la légende. [Vue d’ensemble et quatre détails](rangees/f102v2-218-224.md) · [Lecture antérieure de 218](../2026-11-18-noms-secteurs/plantes-recipients/graphie218/NOTE.md)

Sur f112v, `opchy` est l’avant-dernier mot de la ligne 43 et `otol` le quatrième de la ligne 44. Entre les deux figurent le dernier mot de la ligne 43 (`famom` chez H, `famam` chez ZL) puis `qokchal qokey qaiin`. Les deux éditions s’accordent sur l’absence de coupure de paragraphe entre les deux lignes. H réunit les lignes 42 à 47, tandis que ZL s’arrête à 44. La direction du passage est donc `opchy` puis `otol`, inverse de la succession des deux dessins si on lit les rangées du haut vers le bas. Dans le cahier 20 entier, cette paire n’apparaît qu’une seule fois à huit positions ou moins dans un même paragraphe, quelle que soit l’édition ou la convention d’espacement. Les quatre graphies intercalées n’ont pas de traduction établie. [Lignes 43 et 44 photographiées et transcrites](rencontre112/NOTE.md)

Nous avons isolé les conséquences de deux décisions prises pour interpréter ce cas découvert dans les variantes. Le premier changement admet toutes les suites de lignes consécutives tenues **dans un même paragraphe par les deux éditions**, même si elles divergent sur l’étendue du reste du paragraphe. Cela fournit 297 tronçons, dont les 261 notices identiques. Le second réintègre une seule étiquette à la table de départ, celle de 218, et essaie séparément ses deux lectures. Le terrain est celui des pots à un ou deux étages.

| Lecture de 218 | Légendes formant une paire | Paires dans 261 notices identiques | Paires dans 297 tronçons partagés |
|---|---:|---:|---:|
| Signe douteux écarté | 119 paires | 0 | 0 |
| `okol` | 128 paires | 0 | 0 |
| `otol` | 128 paires | 0 | 1, `opchy`–`otol` |

Pour situer ce résultat, imaginons les 19 étiquettes de fragments du panneau f102v2 redistribuées entre ses pots, en gardant 14 places devant le premier et cinq devant le second. Deux étiquettes données atterrissent devant le même pot dans **101 des 171 paires de places**, soit 59,1 %. Dans le décompte exhaustif des rapprochements textuels à cette distance pouvant relier deux fragments distincts d’un même panneau, seule la paire 218–224 entre en jeu sous cette lecture. La probabilité calculée porte sur le regroupement des dessins, une fois connues les occurrences textuelles. [Six combinaisons de lectures et de limites](deux_feuilles.json)

Un second contrôle redistribue les **mots de la prose** sur chaque face. Il préserve leur fréquence et leur place en début, en milieu ou en fin de ligne. Sous ce modèle, une paire désignée d’avance comme `opchy`–`otol` se rencontrerait quelque part dans le cahier dans 9,18 % des redistributions en H et 9,78 % en ZL, par calcul exact. Or nous avions examiné 128 paires dans cette variante. Sur 49 999 tirages par édition, **au moins une des 128** se retrouve à huit positions ou moins dans 63,16 % des tirages en H et 36,88 % en ZL. Chaque chiffre concerne une seule édition. Les calculs n’estiment pas la probabilité qu’une préparation soit réellement décrite. [Modèle, variantes et vérification exacte](rencontre112/hasard/NOTE.md)

## La paire a-t-elle permis une nouvelle prédiction ?

Après l’observation de f112v, nous avons prédit une autre rencontre de `opchy` et `otol` dans les paragraphes de f58r/v, avec une seconde comparaison sur les deux feuillets à fragments f100 et f101. Ces six faces fournissent 1 304 positions de prose en H, 1 242 en ZL aux espaces incertains joints et 1 347 en les coupant. **La prédiction échoue sur les trois feuillets.** `otol` seul figure dans f58v.37 et f101r.3 dans les deux transcriptions, et `opchy` manque entièrement à la prose de ces six faces. Aucun des deux mots ne se trouve dans le paragraphe f102v2.17–23 sous leurs propres dessins. [Prédiction enregistrée](EPREUVE_F58.md) · [Résultats et positions](deux_feuilles.json)

On peut aussi suivre les deux légendes vers **d’autres dessins étiquetés**. La prédiction enregistrée attendait une touffe de lames étroites, divergentes et dentées sous une autre inscription `opchy`, et un fragment vert compact à pointes près d’un autre `otol`. Hors du feuillet 102, aucune autre légende botanique entière ne donne `opchy`. Pour `otol`, ZL propose f101v.3, où H lit `otal`. À l’origine, c’était H qui proposait `otol`, là où ZL lit `okol`. Le rapprochement nécessiterait donc un changement d’édition entre les deux lieux. De plus, le dessin attribué par l’inventaire est ramifié, ouvert et porte sept extrémités vertes pointues. La couleur et les pointes correspondent. La silhouette compacte attendue échoue. Les deux éditions lisent aussi le mot entier `otol` dans une légende d’étoile (f68r1.25) et dans une inscription entre deux branches du conduit de f77r (f77r.5). Ces autres emplois laissent ouverte la possibilité d’un nom propre, d’une propriété ou d’un autre rôle. [Inventaire sur les autres feuillets](rangees/homonymes/README.md) · [Prédiction visuelle préalable](rangees/homonymes/prediction.md) · [Dessin concurrent sur f101v](rangees/homonymes/f101v-3.jpg)

## Autres rapprochements et témoin d’époque

Avec une finale variable après une base d’au moins quatre signes, les deux légendes `oldy` et `otaly` du premier rang de f99v satisfont la règle à f107v.26, où l’on lit `otal` puis `oldy`. Une redistribution des objets du premier corpus entre rangs de la même face atteint au moins autant de rangées positives dans environ 73 % des tirages. Autoriser les deux étages d’un pot donne aussi `cheor` et `otor` à f104v.24 pour les légendes `cheor` et `otory` de f102v2. Les lectures relâchées, le changement de coupe et la recherche de mots à l’intérieur des légendes plus longues multiplient les rapprochements possibles. Les premiers exemples, tous les scores et les matrices de contrôle restent disponibles. [Variantes dans le premier terrain](notices.json) · [Variantes par pot](notices_pots_elargis.json)

Une affirmation publiée indépendamment sur f88v établit un parallèle entre l’étiquette `otar arody` et des formes dans le cahier 20. Nous retrouvons le comptage annoncé de cinq groupes réemployés sur les quatorze des inscriptions de cette face. La paire entière ne reparaît jamais de façon consécutive dans ces notices. Sur six variantes proposées à des emplacements précis, six se lisent chez ZL avec les espaces douteux séparés et cinq chez H. L’hypothèse d’une même famille de préparations demande encore un témoignage sur le sens de ces formes. [Contrôle de la proposition de Dennis Martin Herbers](sources-dmh/RESULTATS.md)

Pour comparaison, deux copies du *Liber de coquina* conservent des recettes homologues. Les deux premiers noms de produits végétaux relevés selon une règle définie sur onze recettes de la première copie ont servi à rechercher leurs homologues parmi 168 préparations dans une copie datée de 1461–1465. En autorisant les flexions et les graphies prévues, huit recettes attendues sont retrouvées parmi vingt-trois réponses. Trois paires désignent uniquement la bonne recette. L’épinard et l’aneth distinguent le pâté de hareng ou de sardine au f. 188r, tandis que la marjolaine et le romarin conviennent à quatre préparations. Un copiste écrit `spinnarchia`, l’autre `spinarchia`. Cette calibration porte sur deux témoins d’une œuvre connue et n’assigne aucune de ces plantes aux dessins du Voynich. [Comparaison historique et onze résultats](temoin/README.md) · [Feuillet du Vatican](https://digi.vatlib.it/iiifimage/MSS_Pal.lat.1768/Pal.lat.1768_0393_fa_0188r.jp2/full/1200,/0/default.jpg)

## Reproduction

Exécuter les commandes suivantes depuis le dossier de l’étude. Les fichiers de prédiction consignent les empreintes des deux transcriptions et des tables géométriques. Les tests locaux et ceux du cahier final conservent le lien avec le fichier de prédictions utilisé.

```sh
python3 -B notices/lire.py
python3 -B predire.py
python3 -B predire.py --pots-elargis
python3 -B tester.py local
python3 -B tester.py local --pots-elargis
python3 -B tester.py notices
python3 -B tester.py notices --pots-elargis
python3 -B deux_feuilles.py
python3 -B controle.py
python3 -B rencontre112/verifier.py
```

Le contrôle indépendant énumère directement 16 481 recherches « paire, paragraphe » dans le terrain principal, et le lecteur ciblé de f112v vérifie la rencontre positive à partir des deux IVTFF. Les deux éditions, les deux lectures photographiques et les extractions informatiques partagent le même support matériel.
