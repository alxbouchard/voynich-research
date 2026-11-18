# Une inscription végétale se retrouve-t-elle à côté de cheor ?

Le [protocole fixé avant le comptage](CADRE.md) part de la possibilité que `cheor` corresponde à une partie de plante. Il prédit que l’un de ses deux voisins immédiats pourrait aussi figurer dans une légende végétale du panneau. La confirmation demandait une réussite sur deux feuillets physiques distincts et un score supérieur au 95ᵉ centile des permutations.

| Ensemble | Mentions de cheor | Voisins immédiats concordants gauche / droite | Dont graphies admissibles gauche / droite | Correspondances locales |
|---|---:|---:|---:|---:|
| Panneau de départ f102v2 | 3 | 2 / 1 | 2 / 1 | 0 |
| 14 autres panneaux pharmaceutiques | 14 | 10 / 9 | 10 / 6 | 1, à gauche |
| 11 panneaux hors du feuillet 102 entier | 11 | 9 / 7 | 9 / 4 | 1, à gauche |

À f102v2, les trois côtés complets sont `dar cheor` en .32, puis `yotaiin cheor` et `cheor cheekey` en .39. Le mot `cheor` de .33 est concordant, mais aucun de ses voisins immédiats ne forme avec lui une séquence concordante dans les quatre lectures. Aucun des trois voisins retenus ne figure dans les légendes végétales locales.

Dans le transfert, 13 des 14 mentions ont au moins un voisin immédiat concordant, et 12 en ont au moins un admissible par sa longueur et sa forme. Le seul rapprochement local est `chody cheor` en f89v2.9. Les deux transcriptions lisent la légende f89v2.12 en deux mots, `otair.chody`. La prose reprend donc son second mot. Un rapprochement hors panneau est également possible dans le même cahier, entre le voisin `chor` en f102v1.14 et une légende de f99v.

En redistribuant les paquets entiers de légendes entre les panneaux de leur cahier, 7 862 400 des 29 030 400 affectations donnent au moins une correspondance, soit 27,08 %. En retirant tout le feuillet 102, le même rapprochement subsiste et 14 400 des 86 400 affectations l’égalent ou le dépassent (16,67 %). À deux positions, avec un groupe interposé et toute la séquence concordante sur une seule ligne, on obtient zéro correspondance locale pour 1 voisin au départ et 14 voisins sur les autres panneaux.

Le rapprochement de f89v2 permet de localiser et relire un passage concret. Les deux conditions de confirmation échouent. L’expérience laisse le sens de `chody` et de `cheor` ouvert. Elle couvre la répétition exacte d’une graphie dans une inscription conservée et lisible.

Exécuter `python3 -B research/2026-11-18-cheor-en-contexte/distribution/cadre.py` depuis la racine. Le [fichier de résultats](CADRE-RESULTATS.json) donne chaque séquence retenue et les histogrammes exacts. Les six histogrammes ont aussi été vérifiés par énumération directe des bijections dans chaque cahier.
