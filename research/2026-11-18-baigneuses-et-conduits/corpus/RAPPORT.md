# Les mots des figures se distinguent-ils de ceux des cuves et conduits ?

Sur les six faces où les deux catégories sont lisibles, les mots entiers permettent de trancher sept fois sur 55. Deux décisions correspondent au classement du dessin. En utilisant les deux derniers signes du mot, on tranche 50 fois et on donne 28 réponses correctes. Des permutations sur ces mêmes faces produisent régulièrement un score au moins aussi élevé. [Prédictions pour chaque emplacement](RESULTATS.json)

Un exemple montre la difficulté. Au sommet de **f77r**, `otedy` est classé parmi les inscriptions des conduits et autres éléments du dispositif. À **f82v**, le même mot est classé parmi les inscriptions des figures. Ces deux faces appartiennent au même bifeuillet. Quand on le met en réserve, le mot entier prédit deux fois « dispositif », le début `ot` également, et la finale `dy` prédit deux fois « figure ». Chaque règle réussit à l'une des deux positions. Dans les deux fichiers, ces deux lieux ont également le même signe de localisation `=`, qui indique une inscription sur la même ligne que la précédente. [Description et photographie de f77r](https://www.voynich.nu/q13/index.html#f77r) · [f82v](https://www.voynich.nu/q13/index.html#f82v) · [Lieux et transcriptions](INVENTAIRE.json)

## Couverture du cahier

Les deux transcriptions donnent 917 lieux sur les vingt faces des feuillets 75–84. Dans leurs identifiants IVTFF, **Ln** traduit l'association éditoriale d'une inscription avec une figure. **Lt** regroupe les inscriptions associées aux cuves, aux conduits et aux autres éléments de ces scènes. Les deux transcriptions utilisent le même système de classement. Quelqu'un qui écrit à côté d'une figure et d'un tuyau pourrait parler de l'un, de l'autre, du liquide ou d'une action. [Convention IVTFF, tableau 9](https://www.voynich.nu/software/ivtt/IVTFF_format.pdf#page=22) · [Catalogue du cahier 13](https://www.voynich.nu/q13/index.html)

| Unité | Figures (Ln) | Dispositifs et autres éléments (Lt) |
|---|---:|---:|
| Lignes IVTFF des 11 faces portant au moins une étiquette Ln ou Lt | 63 | 47 |
| Emplacements après regroupement des 20 lignes de f75v en dix paires | 53 | 47 |
| Emplacements ayant un mot partagé de deux unités EVA ou davantage | 39 | 36 |
| Emplacements vérifiés sur les six faces où les deux classes sont lisibles | 32 | 23 |

Les autres lieux comprennent 721 lignes de prose ordinaire, 43 lignes décalées vers la droite, 27 lignes de blocs de texte isolés, une ligne alignée à droite et 15 brèves inscriptions sans objet identifiable selon le code L0. Sur les 100 emplacements recherchés, 25 manquent d'un mot concordant, même en comparant les deux traitements de l’espacement douteux. Treize des 75 emplacements conservés livrent deux mots distincts concordants, 62 en livrent un. Tous ont servi à l’apprentissage lorsque leur bifeuillet n’était pas en réserve. [Inventaire par face et raisons des exclusions](INVENTAIRE.json)

## Réussite hors du bifeuillet d'apprentissage

| Trait fourni au prédicteur | Correct | Erreur | Abstention | Score équilibré | p sur la face | p corrigé (Holm) | p sur la face, à nombre de mots comparable |
|---|---:|---:|---:|---:|---:|---:|---:|
| Mot entier | 2 | 5 | 48 | 38,4 % | 0,979 | 0,979 | 0,966 |
| Deux premières unités EVA | 23 | 23 | 9 | 57,9 % | 0,178 | 0,535 | 0,168 |
| Deux dernières unités EVA | 28 | 22 | 5 | 58,5 % | 0,266 | 0,535 | 0,236 |
| Classe la plus fréquente sur les autres bifeuillets | 23 | 32 | 0 | 50,0 % | | | |

Le score donne le même poids aux deux classes d'une face, aux faces d'un bifeuillet et aux trois bifeuillets vérifiables. Une abstention vaut un demi-point. La règle fréquence seule et un choix équiprobable ont tous deux un score équilibré de 50 %. Les finales atteignent respectivement 43,9 %, 66,7 % et 65,0 % sur les trois bifeuillets. Le deuxième résultat repose sur quatre emplacements de f83v, dont un seul près d'une figure. Le témoin artificiel qui attribue un groupe distinctif à chaque classe remonte à 100 % avec chacun des trois modèles. [Protocole préalable et règle de décision](PROTOCOLE.md) · [Résultats par face et par bifeuillet](RESULTATS.json)

Aucune des trois règles n’atteint le seuil fixé pour prédire la catégorie de dessin sur un autre bifeuillet. Les six faces mixtes se réduisent à trois feuilles de parchemin. Le vocabulaire testé peut donc très bien comporter des termes liés à ce que l’on voit sans qu'une de ces trois règles permette de les reconnaître.

Pour reproduire les données depuis ce dossier avec Python et NumPy, exécuter `python3 -B comparer.py`. Le programme vérifie les empreintes des deux transcriptions et effectue 9 999 permutations dans chacun des deux contrôles. [Programme](comparer.py) · [Épreuve antérieure sur les groupes entiers et leur dernière unité](../../2026-11-18-finale-au-dessin/RAPPORT.md)
