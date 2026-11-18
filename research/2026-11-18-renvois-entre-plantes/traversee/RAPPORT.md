# Après le dessin, peut-on prédire « sol » ?

**La paire exacte `qokol daiin` arrive au bord d’un dessin dans les deux exemples qui ont motivé la prédiction. Aucune troisième occasion ne permet de la vérifier.** Sur f3r.16, la ligne reprend par *soleeg* après la tige verte. Sur f23v.7, elle reprend par *sol* après la partie basse de la fleur à pétales bleus. Les deux reprises ont en commun les trois signes transcrits *s, o, l*. Une seule donne le mot entier *sol*. Les photographies confirment les interruptions physiques et les deux lectures éditoriales s’accordent. Ces passages ont été vus avant l’annonce. [Photographies](../photos/interruptions.jpg) · [Prédiction préalable](AVANT.md)

## Après une autre occurrence de daiin

Les feuillets 3 et 23 ont été retirés en entier. Le contrôle strict exige que les éditions IT et ZL indiquent les mêmes marqueurs de coupure sur toute la ligne, que le mot à gauche soit aligné, et que le mot à droite soit lu de la même façon dans les quatre versions pour pouvoir noter une réussite. La prévision assouplie admet tout mot commençant par les trois signes *s, o, l*. Les conditions portant sur le texte de gauche sont emboîtées.

| Texte juste avant la coupure | Prédictions strictes | Reprises lisibles | Mot entier *sol* | Commence par *sol* |
|---|---:|---:|---:|---:|
| qokol daiin | 0 | 0 | — | — |
| Un mot finissant par *ol*, puis daiin | 5 | 5 | 0 | 0 |
| Tout daiin | 20 | 19 | 0 | 0 |

Les cinq mots repris après la condition en *ol* sont *ydaiin* (f22r.12), *otchol* (f28r.1), *shol* (f28r.8), *yd* (f37r.4) et *okoly* (f99v.37). Dans l’alphabet de transcription employé, *sh* est une unité distincte de *s*. L’unique reprise stricte indéterminée est f38v.7, lue *dais* par IT et *dain* par ZL. Les quatre versions proviennent de deux éditions et de deux traitements des blancs. [Relevé des 26 annonces et lectures](VERIFICATION.json)

**Sensibilité.** Six annonces supplémentaires ont été faites lorsque les deux éditions divergent sur une autre coupure de la ligne (1), ou que seule IT marque la coupure étudiée (5). Aucune annonce supplémentaire ne relève de ZL seule. Cinq reprises sont lisibles et aucune ne commence par *sol*. La seule reprise supplémentaire après un mot finissant par *ol* est *chor* à f89v2.9. Celle de f89r2.24 reste indéterminée. Au total, 24 reprises après *daiin* sont lisibles pour 26 annonces. Les deux régimes de sélection sont disjoints. [Prédictions enregistrées](PREDICTIONS.json)

## Contrôles

Au niveau strict, **78 autres coupures lisibles** figurent sur les 14 mêmes faces que les 19 cibles évaluables. Six de ces coupures appartiennent à la même ligne qu’une cible. Aucune des 78 ne reprend par *sol* ou par un mot en *sol-*. Les 19 cibles ont toutes un témoin sur la même face et trois en ont sur la même ligne. Dans le sous-ensemble des cinq cibles après un mot en *ol*, on compte 14 autres coupures lisibles sur quatre faces, aucune sur leur ligne. En sensibilité, les cinq cibles lisibles ont au total six autres coupures sur les mêmes faces, dont une sur la même ligne, et aucune reprise en *sol-*. Ces témoins sont comptés une seule fois par site. L’espérance calculée par le script, qui donne à chaque cible le taux de sa face, vaut également zéro dans ces groupes.

À l’échelle de tout le corpus strict retenu, en dehors des deux feuillets de découverte, **437** des 524 coupures alignées à gauche ont un mot de droite lisible. Quatre reprennent par le mot entier *sol*, après *chl* (f15r.4), *chety* (f54r.7), *chedy* (f75r.15) et *keed* (f75v.12). Deux autres reprennent par *sold* (f36r.7) et *solkaiin* (f82r.3). Les six cas surviennent donc après d’autres mots que *daiin*. L’absence de réussite après *daiin* ne démontre pas que le scribe l’évitait, vu la rareté de ces reprises et le nombre d’occasions. Le corpus supplémentaire comprend 33 coupures communes localement, 38 propres à IT et 23 propres à ZL. [Script et sélection](reprise.py)

**En prose continue**, les quatre lectures donnent *qokol* sur f18v.7 et *oky* sur f102r2.18 après la même paire de départ. Deux autres reprises lisibles sont *dam* sur f22v.8 et *chekal* sur f89v1.10. Sur f104v.11, *daiin* termine la ligne. f53v.4 est un cas propre à IT. ZL y lit un blanc incertain et *daiiin* avec un *i* de plus. Ces occurrences ne constituent pas des répétitions supplémentaires du contexte avec dessin. [Contrôle de la prose](../phrase/REPETITIONS-OUVERTES.json.gz)

Les deux photos justifient de consigner la ressemblance *sol / soleeg*. Les conditions plus larges ne permettent pas de prédire ces trois signes sur d’autres pages ; l’hypothèse la plus précise reste sans nouvel exemple. La graphie latine conventionnelle *sol* ne donne ni un son ni le mot « soleil » du manuscrit. Le code stabilise l’alignement avec les lignes transcrites complètes avant de masquer le voisin droit. Il s’agit d’un contrôle informatique rétrospectif et aucun lecteur indépendant n’a déchiffré une page inconnue.

Les résultats ont été recalculés depuis les transcriptions et correspondent à `VERIFICATION.json`. Pour les reproduire depuis ce dossier, exécuter `python3 reprise.py ouvrir` avec le fichier d’annonces fourni. SHA-256 du fichier d’annonces : `77cbfc0dc1415cb41d8730d9ace4ae0626b479f790ab03652ba72b910c32da6c`. [Annonces](PREDICTIONS.json) · [Résultats](VERIFICATION.json)
