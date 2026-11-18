# Les deux figures portent-elles le même verbe sous deux formes ?

**Aucune des flexions distinctes attestées dans les deux textes médicaux ne se laisse lire à la fois à f80r.2 et f83v.34 avec la même clé.** En revanche, donner exactement le même mot aux deux inscriptions est facile. On peut leur faire dire *laver*, *prendent* ou *prenge*, mais aussi 247 autres mots français de ce manuel. Les emplacements sont `olchdy` (f80r.2) et `okchdy` (f83v.34), tous deux classés auprès d’une figure. [Photographies et cotations des gestes](../gestes-verifies.jpg) · [Prédictions déposées avant les contrôles](PREDICTIONS.json)

Les cinq unités se lisent `o l ch d y` et `o k ch d y`. Les quatre unités communes imposent un début et une fin identiques. Les deux mots historiques devraient donc différer seulement vers leur deuxième morceau. Dans les formes françaises attestées, *prendent* est employé au pluriel pour les eaux qui « prennent » une autre nature, *prenge* introduit la recommandation de prendre garde, et *laver* est un infinitif dans « sen cors laver ». *Prendent* et *prenge* diffèrent aussi en fin de mot. [Attestations avec références](PREDICTIONS.json) · [Texte du manuel et sa transcription](../../francais/TRANSCRIPTION.md)

| Texte de comparaison | Formes des verbes retenus pouvant être répétées aux deux places | Autres mots tout aussi possibles | Couples orientés de mots différents possibles dans tout le vocabulaire, indépendamment du sens |
|---|---:|---:|---:|
| Aldebrandin, français | 3 | 247 | 38 |
| Pierre d’Éboli, latin | 13 | 1 134 | 156 |

Ces comptes permettent une à deux lettres par unité et des signes homophones. Dès que `l` et `k` ont la même valeur, un même mot de cinq à dix lettres peut occuper les deux places. Chez Pierre, les formes admises sont *tenet*, *tacte*, *sumere*, *sumpta*, *sumant*, *sumit*, *capit*, *accipiunt*, *fundit*, *lauare*, *lavari*, *lavat* et *lavantur*. Elles couvrent plusieurs situations. La faim « tient » le malade dans *quos tenet egra fames* ; *tacte* qualifie la neige touchée par le soleil ; dans *Petra*, la boisson *lavat*, « lave ». *Lavari* signifie « être lavé » et *lavantur* « sont lavés ». Remplacer l'écriture *lauare* par *lavare* conserve l'absence de couple de flexions distinctes. [Lieux et contexte des 13 formes](PREDICTIONS.json) · [Contrôle de graphie](RESULTATS.json)

## La troisième figure et le dispositif

Si on ajoute l’hypothèse `t = l = k`, la troisième inscription, `otchdy`, devrait donner exactement le même mot. Cette hypothèse ajoute une valeur au modèle car les deux premières inscriptions sont dépourvues de t. En laissant t ouvert, certaines clés latines permettent aussi *sanant* (« ils guérissent ») à la place de *sumant* (« qu’ils prennent »), ou *letantur* (« ils se réjouissent ») à la place de *lavantur*. La troisième forme ne tranche donc pas entre les lectures. [Tables et mots concurrents](PREDICTIONS.json)

La figure de **f77r.49** porte uniquement `otchdy` dans les quatre lectures. À **f78r.2**, près des éléments du dispositif, les quatre lectures donnent `okchdy`, comme à la figure de f83v.34. Ces lieux n’ont aucun second mot permettant de mettre la lecture verbale à l’épreuve sur place. [Vérification photographique de f78r.2](../paire/f78r-verifie.jpg) · [Transcriptions des quatre emplacements](RESULTATS.json)

## Les voisins de prose

Une fois enlevés les huit feuillets appartenant aux quatre bifeuillets de l’expérience, il reste quatre occurrences concordantes de `olchdy`, treize de `okchdy` et vingt-deux de `otchdy`. Elles livrent **59 voisins immédiats** lisibles dans les deux transcriptions et avec les deux traitements des blancs incertains. Seuls cinq voisins se déchiffrent entièrement avec au moins une des clés. **Aucune de leurs lectures ne se retrouve auprès du verbe proposé** du côté attendu chez Aldebrandin ou chez Pierre. L’échange des côtés donne également zéro. Par exemple, à f114r.9, la table qui lit *laver* produit *vler* pour le mot suivant, `chody`. Les deux textes historiques ont un vocabulaire restreint ; le test évalue ces verbes et cette famille de clés. [Emplacements et résultats détaillés](RESULTATS.json)

Pour reproduire, exécuter `python3 -B proposer.py CACHE` puis `python3 -B verifier.py CACHE`. Le répertoire CACHE contient la transcription vérifiée de Pierre d’Éboli sous le nom `vers.json`. [Protocole](PROTOCOLE.md) · [Calcul des tables](proposer.py) · [Contrôle hors échantillon](verifier.py)
