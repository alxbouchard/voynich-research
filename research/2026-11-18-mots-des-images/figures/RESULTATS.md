# Le mot « femme » près des figures étoilées du Taureau

Aucun groupe entier n’apparaît dans plus de deux des quinze étiquettes de chacun des panneaux. Le meilleur candidat commun, `ar`, figure dans deux étiquettes du premier et une seule du second si l’on coupe les espaces douteux. Avec l’autre découpage chez Zandbergen et Landini, il disparaît du deuxième panneau. Ce résultat ne permet pas de lire « femme ».

La photographie de Yale montre deux Taureaux, le premier clair et le second rouge foncé, entourés de deux anneaux de figures humaines. De courtes inscriptions sont placées près des figures et des étoiles. Les anneaux portent aussi des lignes de texte circulaire, exclues du test. La notice compte quinze figures et quinze étiquettes sur chaque panneau. La proximité ne permet pas de décider si les inscriptions désignent les personnes, les étoiles ou d’autres éléments. [Photographie de Yale, recadrage des deux panneaux](https://collections.library.yale.edu/iiif/2/1006203/0,0,4350,3018/1600,/0/default.jpg) · [Description des panneaux](https://www.voynich.nu/q11/index.html)

| Lecture | Forme(s) en tête sur f71v | Validation sur f72r1 | Contrôles f99r et f99v | Réaffectations au moins aussi fortes |
|---|---|---|---|---|
| ZL, virgules coupées | `ar` 2/15 et `otar` 2/15 | `ar` 1/15 et `otar` 0/15 | 0/51 pour chacune | 11 514/20 000, p = 0,576 |
| ZL, virgules jointes | `otar` 2/15 | 0/15 | 0/51 | 20 000/20 000, p = 1 |
| Takahashi, virgules coupées | `ar` 2/15 | 1/15 | 0/51 | 12 257/20 000, p = 0,613 |
| Takahashi, virgules jointes | `ar` 2/15 | 1/15 | 0/51 | 12 257/20 000, p = 0,613 |

La première et la dernière lecture des caractères entre crochets donnent les mêmes comptes dans chaque ligne. Les 51 contrôles sont les 30 loci de fragments de plantes de f99r et les 21 de f99v. Ils ne représentent pas 51 espèces. La cote de main de ces pages diffère de celle du Taureau. Un compte nul dans ces deux pages ne prouve pas une spécificité générale. [Notice des contrôles](https://www.voynich.nu/q19/index.html)

## Lieux et découpages

- `ar` apparaît en lecture découpée aux loci f71v.9 (5 h 30), f71v.11 (9 h) et f72r1.4 (12 h). ZL indique respectivement `otar.ar,aly`, `opalor.ar` et `oaiin,ar,ary`. En joignant les virgules, seul f71v.11 conserve le groupe entier. Takahashi met des séparations fermes à ces trois endroits et lit `okar` à la place du premier `otar` de f71v.9.
- ZL relève `otar` à f71v.9 (5 h 30) et f71v.16 (5 h 30, cercle intérieur) et jamais comme groupe entier sur f72r1, quel que soit le découpage. Le `otaraldy` de f72r1.8 est une autre forme entière.
- Hors sélection, `char` figure en f71v.2 et f72r1.7, et `otaiin` en f71v.7 et f72r1.9. Chacune apparaît dans une étiquette de chaque panneau dans toutes les lectures. Ce sont les seules formes communes lorsque les virgules sont jointes chez ZL.
- En vérification seule, `ary` culmine à 2/15 aux loci f72r1.4 et f72r1.16 en lecture découpée ZL et chez Takahashi. Elle n’apparaît dans aucune étiquette du premier panneau. Quand les virgules sont jointes chez ZL, chacun des dix-neuf groupes distincts de validation ne figure que dans une seule étiquette.
- Autres difficultés zodiacales explicitement signalées dans ZL : lecture alternative en f71v.16 et f72r1.2, espaces douteux en f72r1.10 et f72r1.11. En f71v.13, ZL marque une ligature. Tous les loci et les conventions figurent dans `resultats.json`.

Pour étalonner le meilleur résultat après sélection, le programme redistribue les étiquettes au hasard en deux panneaux de quinze, puis resélectionne tous les gagnants sur le premier. Pour chacun, il prend la plus petite des deux fréquences, puis la plus grande de ces valeurs entre ex aequo. Le score observé est 1 avec les espaces découpés, contre 0 en jointure chez ZL. La probabilité rapportée inclut la correction de Monte-Carlo +1 sur 20 000 tirages. Les deux panneaux représentent le même signe et le même manuscrit. Les calculs ne testent ni la présence éventuelle de noms propres, ni une désignation seulement implicite, ni une autre expression grammaticale de « femme ».

## Reproduction

Exécuter `python3 compter.py` ou donner le chemin du dossier de transcriptions en argument. Le JSON renseigne les contrôles de hachage, les notations originales, les loci des formes et les résultats des huit combinaisons. Le protocole a été enregistré localement le 18 novembre 2026 à 03 h 25 min 17 s (UTC−5) avant ouverture des lignes visées, avec l’empreinte SHA-256 `e6fccec30c07c8dc96211fe0dc973106b37056ad21277b982326369361bd5ead`. [Édition Zandbergen–Landini](https://www.voynich.nu/data/ZL3b-n.txt) · [Édition Takahashi](https://www.voynich.nu/data/IT2a-n.txt)
