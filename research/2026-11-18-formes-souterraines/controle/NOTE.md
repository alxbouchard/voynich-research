# Contrôle indépendant du test sur les cahiers D–G

Sur les 40 faces réservées, les deux lecteurs ont reconnu un renflement sur 8 et son absence sur 15. Le mot EVA `or` manque les huit positifs. Ses deux seules annonces, f38v et f54r, portent sur des images restées indécises. Il est donc impossible d’estimer la précision de ce mot sur les images cotées par les deux lecteurs.

## Reconstruction

L’analyse repart des deux transcriptions IVTFF, IT2a et ZL3b, des deux clés et des quatre relevés de votes. Le programme retrouve les 85 faces éligibles à partir des métadonnées ZL, de la présence de prose P0 dans les deux témoins et de l’index de photographies de Yale. Les empreintes des témoins concordent avec le dépôt. Pour chaque face et chaque convention d’espace, le nombre total de positions concorde. Le mot porteur et l’adresse de chaque occurrence annoncée concordent également. Le fichier de prédictions examiné est identique à celui du commit `c46eabf`.

| Lot | Faces | O/O | N/N | ?/? | N/? | O/? |
|---|---:|---:|---:|---:|---:|---:|
| Apprentissage A–C | 45 | 11 | 21 | 10 | 2 | 1 |
| Réserve D–G | 40 | 8 | 15 | 11 | 5 | 1 |

L’ordre des deux votes dans ce tableau est I, puis II. Sur la réserve, le second lecteur s’est abstenu sur les 17 faces indécises. Le premier s’est prononcé sur six d’entre elles. Toutes les décisions O ou N émises par les deux lecteurs concordent.

## Apprentissage et épreuve réservée

Avec les espaces douteux joints, 33 mots entiers et 46 terminaisons satisfont aux seuils d’apprentissage. Les gagnants sont uniques avant même le départage alphabétique. Le mot `or` est présent sur 5/11 positifs et 3/21 négatifs, pour un indice de Youden de 24/77. La terminaison `-od` atteint 6/11 positifs et 4/21 négatifs, pour un indice de 82/231.

| Règle et convention | Vrais positifs | Faux positifs | Faux négatifs | Vrais négatifs | Annonces indécises | Précision sur les jugés | p exacte | p Monte Carlo déposée |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Mot `or`, espaces joints | 0 | 0 | 8 | 15 | 2 | Indéfinie | 0,58333 | 0,58180 |
| Finale `-od`, espaces joints | 3 | 5 | 5 | 10 | 8 | 3/8 | 0,19248 | 0,19135 |
| Mot `or`, espaces séparés | 0 | 2 | 8 | 13 | 2 | 0/2 | 0,86111 | 0,86330 |
| Finale `-dal`, espaces séparés | 1 | 4 | 7 | 11 | 5 | 1/5 | 0,81111 | 0,80840 |
| Exploratoire `otoldy`, prose entière | 1 | 2 | 7 | 13 | 0 | 1/3 | 0,44444 | 0,44380 |

Parmi les faces jugées, 8/23 (34,8 %) présentent un renflement. Pour `-od`, la précision atteint 3/8 (37,5 %), soit 2,7 points au-dessus de cette fréquence. La sensibilité est de 3/8 et la spécificité de 10/15. L’indice de Youden est de 1/24.

| Cahier | O/O | N/N | Indécis | Vrais positifs de `-od` | Faux positifs de `-od` | Annonces indécises de `-od` |
|---|---:|---:|---:|---:|---:|---:|
| D | 2 | 3 | 7 | 2 | 0 | 4 |
| E | 2 | 2 | 4 | 0 | 0 | 1 |
| F | 1 | 7 | 0 | 1 | 3 | 0 |
| G | 3 | 3 | 6 | 0 | 2 | 3 |

Les trois bonnes annonces de `-od` sont f28r, f30v et f47r. Les cinq fausses annonces sont f44v, f45v, f47v, f51v et f53v. La terminaison manque f37r, f37v, f49r, f54v et f56v. Huit annonces portent sur des faces indécises, f25r, f27r, f27v, f29v, f38v, f49v, f52r et f53r.

## Permutation exacte et sensibilités

Chaque permutation transporte ensemble les prédictions du recto et du verso d’un feuillet et conserve leur orientation à l’intérieur du cahier. Les votes demeurent à leurs places, y compris les indécis. Pour les 8 positifs et 15 négatifs, la statistique entière est `15 × VP − 8 × FP`, proportionnelle à l’indice de Youden. Pour chaque cahier, une programmation dynamique compte les affectations par sous-ensemble de feuillets déjà employés et par score atteint. Une énumération directe vérifie chaque distribution. Leur convolution donne **6! × 4! × 4! × 6! = 298 598 400** permutations équiprobables. La probabilité unilatérale inclut les égalités. L’exactitude du calcul est conditionnelle à l’hypothèse d’échangeabilité des feuillets dans chaque cahier.

Pour `or`, 174 182 400 arrangements atteignent ou dépassent le score observé, soit 7/12. Pour `-od`, leur nombre est de 57 475 008, soit 11 087/57 600. Les écarts avec les probabilités de l’analyse principale reflètent son échantillonnage de 19 999 permutations.

- **Espaces incertains.** Les espaces séparés maintiennent `or` au premier rang, mais ajoutent les fausses annonces f32v et f45v. Pour les finales, le réapprentissage fait passer `-dal` devant `-od`, avec 5/11 positifs et 1/21 négatif à l’apprentissage, puis un seul vrai positif en réserve, f47r. À titre complémentaire, garder `-od` fixé et changer seulement les espaces ajoute f37r aux trois vrais positifs. Ses cinq fausses annonces subsistent et la probabilité exacte est de 9 277/86 400 (0,10737).
- **Images déjà examinées.** Parmi les dix faces botaniques de l’essai antérieur, huit appartiennent au corpus actuel et six à sa réserve. Une de ces six, f27r, était indécise. Après exclusion des six faces, 6 positifs et 12 négatifs sont évaluables. Le mot `or` manque les six positifs. La finale `-od` fournit 2 vrais et 3 faux positifs, avec une probabilité exacte de 7 937/34 560 (0,22966). Les trois annonces de `otoldy` provenaient exclusivement des anciennes faces, soit f28r, f44v et f53v.
- **Exclusion complète des feuillets anciens.** Dans le calcul prévu, les faces retirées ont un poids nul, mais leurs prédictions peuvent être redistribuées. Un contrôle complémentaire retire aussi les partenaires recto/verso des six faces et leurs prédictions avant toute permutation. Sur les 28 faces restantes, 6 sont positives et 10 négatives. Pour `-od`, il reste 2 vrais et 3 faux positifs, avec p = 19/96. Pour `otoldy`, ce contrôle ne comporte plus aucune prédiction positive et p = 1.
- **Lecteurs pris séparément.** Avec le lecteur I seul, la finale `-od` annonce 3 positifs sur 9 et 6 négatifs sur 20, avec p = 7 439/25 920. Le lecteur II seul fournit les mêmes effectifs que l’accord des deux lecteurs, puisque toutes ses décisions O ou N sont partagées.

Les listes de faces pour chaque règle, chaque cahier et chaque sensibilité figurent dans [les résultats du contrôle](resultat.json). Le [programme de vérification](verifier.py) s’exécute avec `python3 verifier.py` et produit ces résultats sur la sortie standard. Il vérifie également les effectifs et les scores par rapport au fichier de résultats de l’analyse principale.
