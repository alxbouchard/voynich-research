# Les deux finales de f52v seraient-elles des marques de cas ?

Sur f52v.4, `ctheor ctheol cheeor cheol` présente deux alternances entre r et l. Dans Celse VIII.1.27, *digiti digitis, ungues unguibus respondent* signifie que les orteils correspondent aux doigts et les ongles des orteils à ceux des doigts. Chaque nom est au nominatif pluriel, puis au datif pluriel. Nous avons donné ces cinq mots latins aux cinq groupes successifs, avec `chckheey` pour le verbe. Aucune correspondance entre lettres n’est requise dans cette hypothèse de mots entiers. Les deux noms prennent le même cas en l, malgré la disparition d’un e entre `cheeor` et `cheol`. Le détail botanique de f52v ne suffit pas à identifier des orteils ou des ongles. [Celse sur le cliché de Florence de 1478](../../photos/fievres/orteils-1478.jpg) · [Deux pages de plantes, dont f52v](../../photos/deux-grandes-plantes.jpg) · [Hypothèse et annonces](AVANT.md)

## Le mot juste à gauche

Le premier mot physique de la ligne, `tchor`, précède immédiatement `ctheor`. Dans l’édition latine, le passage complet donne *planta palmae, digiti digitis, ungues unguibus respondent*. Le premier couple compare la **plante du pied** (nominatif singulier) **à la paume** (datif singulier). Si l’alignement s’étend d’un seul mot vers la gauche, `tchor` doit donc rendre le datif *palmae*. Un r marquant obligatoirement le nominatif pluriel contredirait la syntaxe dès cet endroit. Isolée, la forme *palmae* peut aussi s’analyser comme un nominatif pluriel. Dans l’imprimé de 1478, on lit *Plãtæ / palmæ* avec deux finales en æ. Le raisonnement qui oppose le nominatif singulier *planta* et le datif *palmae* se fonde sur la rédaction de l’édition ; le second mot garde la graphie *palmae* dans les deux témoins. [Édition de Spencer, livre VIII.1](https://penelope.uchicago.edu/Thayer/L/Roman/Texts/Celsus/8%2A.html) · [Feuillet florentin entier](https://www.digitale-sammlungen.de/en/view/bsb00050602?page=366)

## Sur les autres feuillets

Après exclusion de f52, les quatre premiers mots de la petite table fournissent 139 points de départ concordants dans les deux transcriptions et les deux lectures des blancs. Le cinquième ne réapparaît jamais parmi les mots entiers de la prose retenue. Les départs non évaluables sont conservés dans le registre. [Prédictions par lieu](ANNONCES.json) · [Ouverture et décomptes](RESULTATS.json)

| Départ | Mot suivant annoncé par la formule | Réussites / voisins lisibles | Voisin non évaluable |
|---|---|---:|---:|
| `ctheor` | `ctheol` | 0/3 | 0 |
| `ctheol` | `cheeor` | 0/7 | 1 |
| `cheeor` | `cheol` | 0/9 | 1 |
| `cheol` | `chckheey` | 0/104 | 14 |

Sur le panneau pharmaceutique f102v2, à deux lignes d’écart, `cheeor` est suivi de `ol` et `ctheor` de `okey`. Ailleurs, en f101r.5, la table lit deux mots de suite, *digitis unguibus* ; en f96r.6, *unguibus digiti* ; en f107r.39, *unguibus unguibus*. Aucune de ces paires n’apparaît dans les autres chapitres de Celse. Le même contrôle sur l’ordre inverse des deux cas donne 0/7 après `ctheol` et 0/104 après `cheol`. L’épreuve de la seule suite `cheeor cheol` recoupe le [test précédent](../AVANT.md). Les trois autres voisins et la contrainte sur *palmae* sont propres à ce calcul.

Il existe une limite à cette comparaison. Hors de VIII.1, Celse emploie ces cinq graphies à 60 endroits et **aucune n’est immédiatement suivie d’une autre du même dictionnaire**. Un vrai manuel latin peut donc employer ces termes sans jamais répéter cette formule. Les nouvelles lignes du Voynich ne confirment pas la table. L’enchaînement répété n’est pas une obligation de la langue, et ces comptes ne décident pas si d’autres signes pourraient marquer un cas.

Pour reproduire le calcul, lancer `python3 -B cas.py annoncer celsus.xml`, puis remplacer `annoncer` par `ouvrir`. Le fichier XML et son empreinte sont ceux du [dépouillement de Celse](../../../2026-11-18-phrase-et-doublets/lecture/corpus_sources.py). [Programme](cas.py)
