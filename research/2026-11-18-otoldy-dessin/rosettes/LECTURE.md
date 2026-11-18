# Les deux inscriptions, sur les photographies de Yale

Le premier extrait est pris dans la neuvième ligne de f48v, immédiatement à droite d'une tige qui interrompt la prose. L’autre s'inscrit entre les deux bords ondulés d’un passage dessiné sous la rosette supérieure droite, près de petites constructions. Il faut tourner ce détail du dépliant d’environ 180° pour le lire dans le même sens que la prose. Aucun trait ne désigne sans ambiguïté un élément précis du dessin. Les cinq cartes anonymisées sont tirées des deux JPEG du même manuscrit. [Les deux inscriptions en couleur](deux-inscriptions.png) · [Le passage sur le dépliant](passage-du-depliant.jpg) · [Trois lignes de f48v](trois-lignes-herbier.jpg)

La transcription Zandbergen–Landini situe la légende à fRos.45, repère 7:9 de Petersen. Pour la localiser, nous avons consulté la transcription spatiale d’Alessandro Placa. Ses deux entrées `31:1` et `31:2` portent `otchdy`, `otoldy`. Leurs coordonnées dans son propre cadre sont respectivement (2014, 840) et (1964, 838) avec des orientations de −177,6° et −174,3°. L’auteur attribue la couche textuelle à ZL. Ces coordonnées permettent de localiser les signes mais leur transcription ne constitue pas un vote indépendant. Le recadrage final a été vérifié sur le JPEG de Yale de 7 925 × 7 268 pixels. Les formes ont été examinées sans employer de traduction proposée. [Données spatiales de Placa, version utilisée](https://github.com/alessandroplaca-uro/voynich-spatial-data/blob/7580dafa624cf23a63665f4819022003f8d128ef/rosettes/tokens_f85v_86r.csv#L505) · [Inventaire du dépliant](https://www.voynich.nu/q14/index.html#fRos) · [Cotes, régions, orientations et empreintes Yale](COORDONNEES.json)

## Lecture sans indication du mot recherché

Les deux lecteurs IA ont reçu cinq cartes en gris, mélangées, sans folio, sans texte candidat et sans accès à l'autre lecteur. Ils avaient fini l’évaluation botanique auparavant. Les désignations en caractères latins suivent la convention de transcription EVA. Les deux reconnaissent les mêmes deux cartes comme la seule paire de suites entières possiblement identiques. Ils hésitent sur certaines lettres et n’ont pas restitué sans aide tous les segments de la transcription dans les deux images.

| Carte | Lecteur 1 | Lecteur 2 | Source |
|---|---|---|---|
| S12 | `o[t?][ch/ee]dy o[t?][a/o][l/r]dy` | `otchdy ot(o)(l/r)dy` | f48v.9, troisième segment de la ligne, deux premiers groupes |
| S23 | `[s?]a[s?]ee[cTh?]dy` | `[l?]a[s?]e[e?][gibet sur banc]dy` | Inscription située à droite du passage sur la photographie de Yale avant rotation |
| S37 | `o[t?]eedy o[t?][o/a][l/r]dy` | `oteedy ot(o)(l/r)dy` | fRos.45, entre les bordures |
| S48 | `y[t?]ai[m?] o[t?]edy` | `ytain otedy` | f48v.9, deux derniers groupes |
| S59 | `o[potence?][sh?]edaiin` | `o[p/f?]shedaiin` | Inscription située à gauche du passage avant rotation |

Le premier lecteur juge une répétition intégrale probable. Le second ne l’affirme pas. Ils indiquent tous deux que la liaison horizontale entre les deux petits arcs du premier groupe est beaucoup plus apparente sur l'herbier que sur le dépliant. Dans la translittération c'est ce qui fait hésiter entre `ch` et `ee`. Le deuxième groupe leur paraît très semblable aux deux endroits. L’accord entre éditions, l’identification de la bonne paire d’images et une lecture signe par signe sont trois résultats de portée différente. Les lecteurs IA peuvent partager des habitudes de reconnaissance. [Cinq cartes remises aux lecteurs](cartes/)

Le script régénère les cartes, le détail de chaque page et la planche en couleur. Donner en arguments les deux JPEG natifs dont les URL et SHA-256 sont dans le registre, puis un dossier de sortie. Les images grises d’une même carte partagent les pixels source avec son extrait en couleur. [Programme de reproduction](photos.py) · [Herbier à Yale](https://collections.library.yale.edu/catalog/2002046?child_oid=1006169) · [Dépliant à Yale](https://collections.library.yale.edu/catalog/2002046?child_oid=1006231)

Le contrôle ultérieur sur la photographie de 2004 retrouve la différence de visibilité dans le premier groupe. Les témoins d’autres mots du dépliant montrent une barre très visible dans certains groupes transcrits `ch` et incertaine dans d’autres. Ces comparaisons informées conservent les deux lectures possibles. [Deux campagnes photographiques](ancien/NOTE.md) · [Comparaison aux signes voisins](barre/LECTURE.md)
