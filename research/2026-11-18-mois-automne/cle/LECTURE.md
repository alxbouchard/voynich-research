# Peut-on lire le nom d’octobre avec ce qu’on apprend des trois autres mois ?

Le programme apprend des correspondances entre signes et lettres sur septembre, novembre et décembre. La question est de savoir comment il écrirait octobre, puis de chercher cette graphie parmi les légendes de la Balance et sur huit autres panneaux. Le principe suppose qu’au moins une des inscriptions choisies par panneau répète son nom de mois. L’inscription en lettres latines indique ce nom. Elle ne désigne aucune légende particulière dans l’écriture inconnue. [Protocole](../PROTOCOLE.md) · [Annotations sur le parchemin](../photographies/LECTURES.md)

## Une prédiction déposée avant comparaison

Pour le test principal, chaque signe prend une valeur fixe d’une ou deux lettres. Un banc transcrit `ch` compte comme un signe. L’entrée comprend uniquement les légendes entières d’un seul mot lisibles au même emplacement dans les deux éditions et les deux traitements des blancs. Nous testons séparément les deux sens. Chaque lecture individuelle autorise des tables. Après septembre et novembre, il en reste vingt dans chaque sens. Avec décembre, il en reste **zéro**. Un autre calcul, qui énumère les découpages possibles des noms lettre par lettre, reproduit ce résultat. [Contre-calcul](CONTRE-CALCUL.json) · [Inventaire des graphies et emplacements](INVENTAIRE.md)

Une version plus permissive accepte Takahashi seul et des valeurs de longueur libre. En lecture inverse, 5 251 tables conviennent aux trois noms. Une seule permet d’écrire octobre en entier. Elle propose `oairoled`, à partir de `airolm`, `chdy` et `okeos` pour les trois mois d’apprentissage. Le mot prédit manque parmi les légendes d’octobre et dans les huit panneaux de comparaison. Sur un chiffre artificiel de contrôle, le programme trouve la seule graphie correcte, `jbpfgalf`, et écarte les huit leurres formés des mêmes signes. [Prédictions enregistrées avant vérification](PREDICTIONS.json.gz) · [Résultats par panneau](RESERVE.json) · [Contrôle à clé connue](APPRENTISSAGE.json)

Le calcul complet sépare légendes et anneaux, conventions de lecture, sens, largeurs et graphies cibles. Les 60 configurations initiales émettent 772 graphies en comptant leurs recoupements. Les 24 configurations supplémentaires pour des formes attestées à Paris et à Chantilly en émettent trois. Sur les **753 graphies distinctes** au total, aucune ne se rencontre comme prévu en octobre, ni sur les huit autres panneaux, dans le type d’inscription et l’édition pour lesquels elle était prédite. Octobre était réservé au calcul. Certaines de ses graphies et sa disposition avaient déjà été vues par l’équipe. Cet échec concerne les règles et les mots retenus. Il laisse ouverte la possibilité que l’annotateur ait utilisé une autre langue que les scribes ou ait ajouté des noms absents du texte principal. [Graphies des témoins](AUTRES-TEMOINS.md) · [Vérification complémentaire](RESERVE-TEMOINS.json)

## Une table qui semble donner les quatre mois

Une deuxième expérience a été conçue après le relevé de la finale commune `eody`. On autorise cette finale à servir d’abréviation et un signe à rester muet. On ajuste les quatre noms simultanément. Sur les neuf inscriptions entières d’automne qui concordent entre éditions, les 16 choix possibles ne donnent aucune table, même en laissant les quatre réponses visibles. Avec Takahashi seul, la lecture supplémentaire `cheody` de f73v.4 permet de faire apparaître les quatre formes du calendrier parisien. Voici l’une des 18 tables obtenues en lecture directe avec `o` muet.

| Groupe transcrit | Application de la même table | Lecture obtenue |
|---|---|---|
| `yteody` | s + eptem + bre | septembre |
| `oeeody` | ∅ + octo + bre | octobre |
| `okeody` | ∅ + novem + bre | novembre |
| `cheody` | decem + bre | decembre |

Si l’on cache le nom d’octobre, les trois autres mots n’apprennent aucune valeur pour le signe `e` isolé devant la finale. Les 18 tables ne rendent alors que la fin du mot. Si l’on redistribue les quatre noms sur les panneaux, **chacun des 24 ordres** admet au moins une table de même nature. Six ordres en admettent au moins autant que le véritable ordre. La table ci-dessus écrit aussi *novembre* auprès d’un fragment végétal de f102v1.3 et sur des panneaux de septembre et de décembre. Une date pourrait figurer dans un texte botanique, mais aucune inscription lisible ne l’atteste à cet endroit. [Tables et contrôles de permutation](CONTROLES.json) · [Photographie et deux lectures séparées du signe de décembre](../photographies/finale/LECTEURS.md)

Avec les noms développés au plus près des annotations du Voynich, 35 tables dans la version Takahashi lisent les quatre noms en sens inverse en effaçant la finale entière `eody`. Douze des 24 ordres deviennent alors possibles. La fonction de cette finale reste ouverte. [Essais avec et sans abréviation](ABREVIATION.json)

## Reproduire les essais

Depuis ce dossier, utiliser Python 3 avec les deux transcriptions distribuées dans le dépôt. Ces commandes reconstruisent les fichiers des prédictions puis ceux des observations.

```sh
python3 -B dechiffrer.py apprendre
python3 -B dechiffrer.py verifier
python3 -B temoins.py apprendre
python3 -B temoins.py verifier
python3 -B contre_calcul.py
python3 -B abreviation.py
python3 -B contre_epreuve.py
python3 -B inventaire.py
```
