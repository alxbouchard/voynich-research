# Que peut-on lire après le d d’un début de ligne ?

Sur f84r, trois inscriptions distinctes surmontent trois personnes au bord d’un bain. La dernière, `dshedy`, se rencontre en début de ligne dans la prose. Sous le dessin figure la forme courte `shedy`. En rapprochant ces deux graphies sur les autres pages des bains, on retrouve un mot masqué sous l’image. Dans le dernier cahier, la même règle échoue sur les trois débuts en `dshedy`. La signification de l’inscription au-dessus du personnage reste inconnue. [Scène et texte sur le feuillet](legendes/scene-et-prose.jpg) · [Transcriptions, hypothèses et résultats](legendes/RAPPORT.md)

Le même feuillet permet aussi de tester l’idée que les mots des dessins signifient « plante », « racine », « étoile » ou « femme ». Sur les 445 légendes de six types, aucune paire de signes ne se maintient dans la moitié des inscriptions sur chacun des feuillets retenus pour les étoiles, les fragments de plante ou les figures des bains. Une racine à deux bras avait pu être prédite sur f99v. Le nouveau contrôle des finales sur quatre feuillets donne 17 paires de même forme pour 18,84 attendues. [Images, légendes et contrôle dans un herbier du XVe siècle](objets/RAPPORT.md)

## Le mot suivant sur d’autres feuillets

L’apprentissage utilise la prose des bains et les pages botaniques de la première main entre les feuillets 1 et 25. La règle rapproche une forme initiale en d de sa forme courte. Nous avons masqué les suites dans les autres feuillets, puis retenu les voisins dont deux transcriptions, chacune lue selon deux conventions d’espacement, confirment l’identité et la continuité. Les feuillets avaient déjà servi à d’autres recherches. Les annonces A et B précèdent la révélation du deuxième mot pour C. [Protocole](PROTOCOLE.md) · [Annonces A et B](ANNONCES-AB.json.gz) · [Annonces C](ANNONCES-C.json.gz)

| Débuts testés | A · Deuxième mot exact | B · Deux mots suivants exacts | C · Troisième mot exact, deuxième montré |
|---|---:|---:|---:|
| Dernier cahier, d devant ch ou sh | 0/47 | 0/44 | 0/44 |
| Herbier de main 2, classe B, d devant ch ou sh | 1/10 | 0/9 | 0/9 |
| Autres pages, d devant ch ou sh | 1/67 | 0/56 | 2/56 |
| Dernier cahier, toutes les formes en d à base courte attestée | 3/119 | 0/112 | 1/112 |

À f31r.2, le voisin de `dcheey` est bien `daiin`, visible après `cheey` à f20r.6. À f49v.22, le regroupement perd une réponse juste. Après `dchol cthol`, il propose `chkor` là où le modèle gardant le d retrouve `daiin`. Dans le dernier cahier, les trois réussites de l’épreuve élargie sont deux `dain chey` et un `dol shedy`. Un contrôle supplémentaire, qui conserve le d et apprend uniquement aux débuts de ligne, obtient lui aussi 3/119. Devant ch ou sh, le regroupement dégrade la probabilité du mot observé de 1,19 bit par emplacement en moyenne. Aucun des douze feuillets n’y gagne. [Deux passages botaniques](deux-lignes/photos/deux-plantes.jpg) · [Comparaison des modèles](COMPARAISONS.json) · [Contrôle de position](CONTROLE-POSITION.json)

## Ce que l’image permet de prédire

À f84r.15, la transcription donne `dar shedy qokedy qokeedy`. Dans les autres bains, après regroupement, `qokedy` arrive seul en tête avec 13 occurrences sur 138 et restitue le mot masqué. Après la seule graphie courte, il était à égalité avec `qokaiin` (10 sur 124 chacun). Le modèle principal, qui tient compte de `dar`, propose `chedy` et échoue. Aucune paire d’inscriptions voisines prise dans l’ordre de quatre rangées de figures ne se retrouve dans les 19 165 paires de prose comparables. À la ligne suivante, deux lectures indépendantes par des IA laissent incertaine la coupure dans `shedytedy`. [Résultats sous le bain](legendes/RAPPORT.md) · [Espace examiné sur photographie](legendes/jointure/RAPPORT.md)

Deux paires de lignes sur des feuillets différents commencent par les mêmes deux mots et alternent ensuite entre `qokeedy` et `qokeey`. Le prolongement annoncé de sept signes échoue sur f116r.17. Une prédiction de mise en page réussit cependant. Après la ligne f103v.36, une étoile est visible dans la marge, en face de f103v.37. Sur les deux lignes proposées comme fins de paragraphe, seule celle de f103v termine le sien. [Quatre débuts, annonces et photographies](deux-lignes/RAPPORT.md)

## Les lectures historiques à l’épreuve du quatrième mot

Une table fixe rend `dain chey qokeedy` par *orae esse compressae*, trois mots de Celse sur les bords d’une fissure du crâne, visibles dans un imprimé florentin de 1478. Celse poursuit par *vel*. Sur f116r.17 la table donne *mpresse* au même endroit. Ailleurs, sur 1 826 paires entières lisibles avec cette clé, aucune sortie ne se retrouve dans le reste de Celse ou dans le *Macer* selon les règles annoncées. Les essais en français et en italien sur f43 échouent aussi à prédire le troisième mot, sur les deux faces. [Latin, clé et transfert](lecture-trois-mots/RAPPORT.md) · [Deux témoins florentins](lecture-trois-mots/temoins/LECTURE.md) · [Essais vernaculaires](vernaculaire/RAPPORT.md)

Un témoin allemand donne la mesure d’une prédiction sur un texte connu. Dans deux éditions du *Buch der Natur*, le même mot *Nigella* conserve son identité malgré un changement de marque. Sur trois nouvelles rubriques de l’édition de 1482, le pied-de-mouche et le mot *Von* sont retrouvés trois fois, l’article *der* deux fois. Dans le Voynich, les réussites portent jusqu’ici sur des graphies et des emplacements, et aucune de ces clés ne fournit de lecture continue. [Rubriques, témoins et éditions de 1475 et 1482](temoin/RAPPORT.md)

Pour reproduire les épreuves principales, lancer `suites.py` avec Python 3 dans l’ordre `masquer_AB`, `annoncer_AB`, `masquer_C`, `annoncer_C`, `verifier`, puis `verifier_position.py`. [Réponses par ligne](OUVERTURES.json.gz) · [Programme](suites.py)
