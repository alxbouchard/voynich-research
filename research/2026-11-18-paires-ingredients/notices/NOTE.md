# Délimitation des paragraphes du cahier 20

Les deux éditions donnent **261 paragraphes dont tous les identifiants de ligne se correspondent dans le même ordre**, sur 23 faces. Ce sont les unités appariables pour une comparaison portant sur la présence de formes dans le même paragraphe. Le critère sélectionne les lignes à partir de leur position et de leur annotation, avant toute lecture lexicale. Une unité désigne ici un paragraphe transcrit sur une page à étoiles marginales. L’association d’une étoile à un passage précis demande une observation distincte de l’image.

## Définition et couverture

Le filtre conjoint utilise le cahier `$Q=T`, l’illustration `$I=S` et le type de locus `P`. Les pages sont f103r/v à f108r/v, f111r/v à f115r/v et f116r. L’édition ZL fournit aussi f116v avec `$I=T` et un unique locus `Lx`. Cette face est absente du fichier H. Le lecteur ouvre une unité à `<%>` et la ferme à `<$>` sur la même face. Il vérifie que chaque début et chaque fin est à la place prescrite et que toute ligne appartient à une seule unité. Les comparaisons emploient l’identifiant IVTFF entier, avec numéro, localisateur et sous-type. [Spécification IVTFF, §§ 6.3, 6.4, 6.7 et 6.9](https://www.voynich.nu/software/ivtt/IVTFF_format.pdf)

| Corpus | Paragraphes | Lignes | Segments, espaces incertains joints | Segments, espaces incertains coupés |
| --- | ---: | ---: | ---: | ---: |
| H, toutes les unités | 289 | 1 083 | 10 682 | 10 682 |
| ZL, toutes les unités | 285 | 1 084 | 10 093 | 10 893 |
| H, unités communes | 261 | 972 | 9 558 | 9 558 |
| ZL, unités communes | 261 | 972 | 9 028 | 9 751 |

Les longueurs comptent les segments délimités par les points, les coupures de dessin et, dans la dernière colonne, les virgules. L’indicateur compte une position même si sa lecture présente un signe incertain. Il ne conserve ni la forme ni le sens du segment. Les lectures alternatives entre crochets sur ces faces n’introduisent aucune coupure concurrente. Le relevé par face et par édition est dans [comptes.tsv](comptes.tsv).

Les 278 débuts communs et les 278 fins communes produisent 262 couples de bornes identiques. Un seul de ces couples contient des listes de lignes différentes. Entre f106r.27 et f106r.31, ZL contient f106r.29 et H passe directement de f106r.28 à f106r.30. Après son exclusion, les 261 listes concordent jusque dans le sous-type de locus. Chaque édition comprend trois lignes Pr et une ligne Pc. H compte en outre 1 079 lignes P0, ZL 1 080. Pt est absent de cette sélection. Toutes les lignes des unités communes sont P0.

Les cinq paragraphes d’une ligne de H portent chacun les deux marques explicites. Ils correspondent à f105r.10 (Pr), f105r.37 (Pc), f108v.53 (Pr), f112r.15 (P0) et f114r.34 (Pr). ZL les regroupe avec les lignes attenantes. Le lecteur n’a trouvé aucune ligne orpheline dans H ni ZL et aucune unité d’une seule ligne dans leur intersection.

## Folios 108 et 116

| Face | Lignes H et ZL | Paragraphes H | Paragraphes ZL | Paragraphes communs | Lignes communes retenues |
| --- | ---: | ---: | ---: | ---: | ---: |
| f108r | 50 | 16 | 14 | 12 | 38 |
| f108v | 53 | 10 | 7 | 5 | 19 |
| f116r | 50 | 8 | 8 | 8 | 50 |

Sur f108r, H divise les lignes 8–13 et 39–44 en deux unités chacune. Le catalogue décrit 16 étoiles et avance un total probable de 16 paragraphes, avec des coupures incertaines. Sur f108v, les cinq premières unités (1–4, 5–6, 7–11, 12–14, 15–19) sont les seules communes. Le catalogue les décrit alignées avec les premières étoiles et estime qu’il pourrait y avoir huit paragraphes pour 16 étoiles sur cette face. Ce troisième comptage illustre l’incertitude des limites. [Catalogue du cahier 20](https://www.voynich.nu/q20/index.html)

Sur f116r, les huit intervalles communs sont 1–3, 4–6, 7–9, 10–14, 15–17, 18–30, 31–45 et 46–50. Le catalogue signale dix étoiles dans la partie supérieure. Les deux dernières unités, soit les lignes 31–50, n’ont pas d’étoile en marge. Pour exclure ces deux unités à elles seules, il reste 259 paragraphes communs. En retirant intégralement les faces f108r, f108v et f116r, il en reste 236 couvrant 865 lignes sur 20 faces. [Catalogue du cahier 20](https://www.voynich.nu/q20/index.html)

## Reproduction

Depuis la racine du dépôt, exécuter `python3 research/2026-11-18-paires-ingredients/notices/lire.py`. [paragraphes.json](paragraphes.json) donne, sous les clés `H`, `ZL` et `accord`, les listes ordonnées des paragraphes de chaque corpus. Chaque paragraphe est une liste d’identifiants IVTFF complets, sans chevrons. [lire.py](lire.py) vérifie l’alternance des marques et régénère les deux fichiers de sortie avec la bibliothèque standard Python.

Le 18 novembre 2026, les fichiers publics et les copies locales de `voynich_phase14/data/` avaient les mêmes SHA-256.

| Édition | SHA-256 | Source |
| --- | --- | --- |
| H, Takahashi (IT2a-n) | `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5` | [Fichier de l’éditeur](https://www.voynich.nu/data/IT2a-n.txt) |
| ZL, Zandbergen–Landini (ZL3b-n) | `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc` | [Fichier de l’éditeur](https://www.voynich.nu/data/ZL3b-n.txt) |
