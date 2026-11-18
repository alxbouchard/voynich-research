# Le même mot apparaît-il près des figures et près des cuves ?

`otedy` apparaît deux fois près de figures et deux fois près d'autres éléments des bains. `otoly` apparaît deux fois près de figures. À ces deux derniers endroits, le dessin voisin est fréquemment une figure, quel que soit le mot inscrit. Les graphies `otedy` et `otoly` suivent la convention de transcription EVA. Leur sens et leur prononciation restent ouverts.

Nous avons repris les deux formes entières les plus répandues parmi les 41 inscriptions de figures concordantes de l’étude précédente. Ce choix a été fait à la vue de leurs fréquences. La comparaison porte cette fois sur les feuillets 75 à 84, en gardant les faces qui offrent les deux sortes d’inscriptions. La catégorie éditoriale Ln désigne une inscription près d’une figure humaine dite « nymphe ». Lt désigne une inscription de conduit, de cuve ou d’un autre élément de ces scènes. Cette classification décrit le rattachement proposé par les éditeurs. Elle ne code ni le sexe de chaque figure ni le sens du mot. Une unité est une ligne d’inscription IVTFF qui peut contenir plusieurs mots. [Étude qui a sélectionné les candidats](../../../2026-11-18-mots-et-dessins/RAPPORT.md) · [Convention IVTFF, tableau 9, p. 22](https://www.voynich.nu/software/ivtt/IVTFF_format.pdf#page=22) · [Catalogue du cahier 13](https://www.voynich.nu/q13/index.html)

| Face | Lignes près des figures | Lignes près des autres éléments | Occurrences des deux mots |
| --- | ---: | ---: | --- |
| f75v | 18 | 7 | `otoly` près d'une figure (.37), `otedy` près d'un autre élément (.54) |
| f77r | 3 | 7 | `otedy` près d'un autre élément (.3) |
| f82r | 5 | 1 | aucune |
| f82v | 6 | 5 | `otedy` près d'une figure (.2) |
| f83v | 1 | 3 | aucune |
| f84r | 8 | 1 | `otedy` et `otoly` près de figures (.8 et .11) |
| **Total** | **41** | **24** | **6 occurrences** |

Le tableau retient les inscriptions entièrement lisibles pour lesquelles les deux transcriptions donnent les mêmes groupes de signes une fois joints les espaces douteux. Lorsque ces espaces sont séparés, 42 inscriptions de figures et 23 d'autres éléments concordent sur les mêmes six faces. Chez Takahashi seul, sept faces permettent la comparaison (53 et 36 lignes). Chez Zandbergen–Landini seuls, les mêmes sept faces comptent 50 et 33 lignes. Les six occurrences restent aux mêmes endroits avec chaque lecture. Les lignes écartées et les pages portant une seule catégorie lisible figurent dans le relevé complet. [Loci, dénominateurs et calculs](RESULTATS.json)

À f75v, des figures jouxtent 18 des 25 emplacements retenus et, à f84r, 8 sur 9. Si on choisit un emplacement au hasard sur chacune de ces deux faces, en gardant fixes les nombres de lignes de chaque type, la probabilité de tomber deux fois près de figures est de 18/25 × 8/9 = 64 %. Pour les quatre occurrences de `otedy`, le même calcul sur leurs quatre faces donne 326/375, soit 86,9 %, d’en placer au moins deux près de figures. Ces probabilités décrivent les possibilités de placement de deux mots déjà sélectionnés. La présence d'une figure ou la proximité d'une cuve pourrait aussi intervenir dans le sens d'une expression plus longue.

Pour reproduire le tableau, exécuter `python3 -B compter.py` depuis ce dossier. Le programme reprend le lecteur IVTFF de l’étude initiale, compte chaque mot au plus une fois par ligne et énumère les répartitions par face à nombres de lignes et d’occurrences constants. Les empreintes des deux fichiers sources sont incluses dans le résultat. [Programme](compter.py) · [Transcriptions et éditions](https://www.voynich.nu/transcr.html)
