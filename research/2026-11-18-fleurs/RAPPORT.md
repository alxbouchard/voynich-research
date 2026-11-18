# Un mot permet-il de prédire où le scribe a dessiné une fleur ?

**Le groupe `qotor` a annoncé des corolles au bon endroit sur f5v et à tort sur f8r. Il a également manqué celles de f6v.** Dans les deux premières pages, le groupe ouvre exactement la quatrième ligne, selon les deux transcriptions. Parmi les 12 pages où les lecteurs s'accordent sur le dessin, la règle obtient dix bonnes réponses. Prédire partout l'absence de corolle en donne également dix. [Page f5v](exemples/f5v.jpg) · [Page f8r](exemples/f8r.jpg) · [Page f6v](exemples/f6v.jpg)

## Reconnaître le même détail visuel

Quarante-cinq faces botaniques de trois cahiers ont servi à deux essais. Elles sont toutes attribuées dans les métadonnées à la main 1 et à la variété A de Currier. Les lecteurs ont reçu des reproductions Yale en ordre mélangé. Le modèle de texte n'a reçu que les quarante premières positions de prose ordinaire de chaque face. Les cahiers d'apprentissage et d'épreuve tiennent sur des feuillets physiques différents. Les deux lecteurs sont des agents IA distincts de la même famille. Une incertitude, un désaccord ou l'absence de mot candidat est conservé.

Le premier essai cherchait n'importe quelle fleur ou inflorescence visible. Sur 30 faces des cahiers B et C, aucun des lecteurs n'a donné un « non » sûr. Les épis, fruits ou boutons possibles rendaient le contraste inexploitable. Ils se sont accordés sur 9 présences en B et 10 en C. La méthode préenregistrée s'est abstenue sur les 16 pages de C, car elle n'avait aucun exemple négatif assuré à l'apprentissage. [Première règle](protocole_initial/PROTOCOLE.md) · [Premiers résultats](protocole_initial/RESULTATS.json)

Pour le deuxième essai, le détail recherché a été restreint à une corolle en forme de rosette vue de face, avec au moins quatre pétales, lobes ou rayons disposés autour d'un centre. Il s'agit d'une propriété du dessin qu'un lecteur peut relever sans identifier l'espèce. La règle a été changée après le premier essai. Les cahiers B et C ont servi à apprendre cette fois. Sur 30 faces, les lecteurs s'accordaient sur 9 présences et 18 absences. Les trois autres sont restées indéterminées. Un mot devait apparaître dans au moins deux feuillets illustrant le motif pour être retenu. Les prédictions sur les 15 autres faces (cahier A) ont été enregistrées avant la lecture de leurs photographies pour cet essai. [Deuxième règle](corolles/PROTOCOLE.md) · [Prédictions par face et par édition](corolles/PREDICTIONS.json) · [Photos et empreintes des originaux Yale](corolles/CARTES_A.json)

## Résultats dans le cahier tenu à l'écart

Sur les 15 faces, les lecteurs s'accordent sur 2 présences et 10 absences. Trois cartes ont été écartées pour désaccord ou incertitude, sur f3v, f4v et f7r. La comparaison ci-dessous évalue chaque méthode sur les mêmes douze faces.

| Mots lus dans la prose | Mot fixé sur les deux premiers cahiers | Présences annoncées à juste titre | Fausses annonces | Absences correctement annoncées | Total correct |
|---|---|---:|---:|---:|---:|
| Takahashi, deux conventions d'espacement | `qotor` | 1/2 | 1 | 9/10 | 10/12 |
| Zandbergen–Landini, espaces incertains joints | `ykaiin` | 0/2 | 0 | 10/10 | 10/12 |
| Zandbergen–Landini, espaces incertains séparés | `shor` | 1/2 | 3 | 7/10 | 8/12 |
| Classe majoritaire de l'apprentissage | Toujours « non » | 0/2 | 0 | 10/10 | 10/12 |

Dans les quatre traitements, le modèle qui utilise tous les mots du passage trouve une des deux rosettes, fait une fausse annonce et obtient 10/12. Pour la règle principale `qotor`, un seul des deux feuillets avec des faces de classes opposées permet de changer le score en échangeant recto et verso. Deux des quatre échanges possibles atteignent la réussite observée. [Matrices complètes](corolles/RESULTATS.json) · [Réponses du premier lecteur](corolles/A_LECTEUR_A.json) · [Réponses du second](corolles/A_LECTEUR_B.json)

Sur f5v, plusieurs petites fleurs rouges ont cinq lobes autour d'un point clair. Sur f8r, une tige porte des feuilles mais la rosette annoncée est absente. Sur f6v, des disques verts et bleus portent des rayons pointus, bien que le mot annoncé soit absent de la fenêtre de prose. Cette troisième image rappelle que le test porte sur des formes dessinées. L'ensemble ne donne pas de raison d'écrire « fleur » comme traduction de `qotor`. [f5v à Yale](https://collections.library.yale.edu/iiif/2/1006085/full/full/0/default.jpg) · [f8r à Yale](https://collections.library.yale.edu/iiif/2/1006090/full/full/0/default.jpg) · [f6v à Yale](https://collections.library.yale.edu/iiif/2/1006087/full/full/0/default.jpg)

## Une régularité de position vérifiée séparément

Le fait que les deux prédictions positives se trouvent exactement en tête de la quatrième ligne est apparu **après** la vérification des dessins. Nous avons donc testé séparément, sur les autres pages botaniques à partir du feuillet 25, si `qotor` occupe souvent la première position d'une ligne de prose. Les feuillets de l'essai de fleurs sont tous exclus. Chaque témoin de hasard conserve le nombre d'occurrences de chaque ligne et le nombre de places effectivement lisibles. [Prédiction enregistrée](position_qotor/PROTOCOLE.md)

| Hors des trois cahiers, tous scribes botaniques | Occurrences du mot entier | En première position | Nombre attendu si les places lisibles de chaque ligne étaient équiprobables |
|---|---:|---:|---:|
| Takahashi, espaces incertains joints | 10 | 4 | 1,46 |
| Zandbergen–Landini, espaces incertains joints | 9 | 5 | 1,46 |

La probabilité conditionnelle d'obtenir au moins autant d'initiales est de 0,042 et 0,0058 avec ce modèle précis. Le motif de **quatrième ligne** n'est jamais retrouvé à l'initiale dans ce nouvel ensemble. Les deux éditions lisent le même objet physique et ne constituent pas deux réplications indépendantes. La tendance à commencer une ligne peut refléter la manière d'écrire, la syntaxe ou la mise en page. Elle ne fixe pas une prononciation ou une traduction. [Tous les emplacements et calculs](position_qotor/RESULTATS.json)

[Instructions pour reproduire les résultats](REPRODUCTION.md)

Une vérification indépendante retrouve les quatre débuts communs aux deux éditions, f37v.8, f37v.16, f42r.11 et f49r.2. À f36v.2, la première case est `qotar` chez Takahashi et `qotor` chez Zandbergen–Landini. Un groupe presque identique, `qotol`, a lui aussi une préférence de position. Dans les pages de la main 1 et de variété A, la proportion d'initiales est exactement la même pour les deux mots dans chaque édition, 50 % chez Takahashi et 62,5 % chez Zandbergen–Landini. Le groupe final distingue deux graphies qui se placent souvent en tête de ligne dans cet échantillon. [Comparaison avec toutes les formes de fréquence, de longueur et de préfixe comparables](position_qotor/formes_comparables/NOTE.md)
