# Vérification indépendante des lectures à une ou deux lettres par signe

Chaque fenêtre contient quatre mots effectivement successifs dans une même notice ou un même fragment. L’ordre direct de la chaîne de signes et celui du texte historique définissent l’épreuve principale. Sur **13 736** fenêtres du *Macer* latin et **102** des fragments français, aucune table de valeurs non vides d’une ou deux lettres ne permet de lire la première paire `opcheor opcheol`. [Données de toutes les comparaisons](resultat.json)

## Quand une seule valeur peut être vide

Dans le sens direct, trois paires latines admettent une table avec un signe muet. Elles se trouvent dans les notices de la camomille (*herba herbae*), de la sarriette (*somnum somno*) et de la morelle (*succo succus*). Seules les deux premières permettent aussi de lire le troisième mot. En parcourant le latin en sens inverse, trois fenêtres atteignent le troisième mot. Le tableau conserve la position de départ, comptée depuis 1 dans l’ordre physique du témoin. Chaque ligne présente les formes sans ponctuation effectivement comparées.

| Sens du texte | Notice et position | Trois mots d’apprentissage | Quatrième mot prédit pour `sholdy` | Quatrième mot du témoin |
|---|---|---|---|---|
| Direct | Chamomilla, 19 | herba herbae tam | taeam (3 tables) | similis |
| Direct | Satureia, 75 | somnum somno gravat | groavat (3) | hic |
| Inverse | Chamomilla, 20 | herbae herba brevis | braevis (3) | et |
| Inverse | Satureia, 76 | somno somnum haec | humaec (6), haumec (3) | vetat |
| Inverse | Maurella, 53 | succus succo illita | ilolita (3) | depellitur |

L’inversion des unités de chaque groupe, avec ou sans inversion de la suite des mots du témoin, ne conserve aucun triplet. Aucune fenêtre française n’atteint deux mots dans les quatre combinaisons de sens. Le test conserve `ch` et `sh` comme unités et la graphie majoritaire de chaque mot du manuscrit.

## Ce que le seul passage du troisième au quatrième mot autorise

Les unités de `sholdy` s’obtiennent en insérant `l` dans `shody`. Une table à valeurs fixes impose donc que l’on puisse produire le quatrième mot clair en insérant une suite de lettres contiguës dans le troisième. Si `l` est muet, les deux mots doivent être identiques. Cette propriété est conservée quand on inverse les unités de chacun des mots. Nous avons relâché le test en autorisant l’ajout à **n’importe quelle position** du mot clair. Le tableau compare toutes les fenêtres, même celles dont les deux premiers mots n’admettent aucune table.

| Corpus et parcours | Fenêtres | Insertion de longueur positive quelconque | Insertion d’une ou deux lettres | Répétition exacte |
|---|---:|---:|---:|---:|
| Latin direct | 13 736 | 38 | 30 | 0 |
| Latin inverse | 13 736 | 35 | 17 | 0 |
| Français direct | 102 | 3 | 1 | 0 |
| Français inverse | 102 | 0 | 0 | 0 |

Les trois cas français sont *les → feulles*, *les → feules* et *a → la*. Parmi les fenêtres qui franchissent le test des deux premiers mots avec au plus un signe muet, **aucune** ne satisfait même au critère d’insertion de longueur libre à la fin. La difficulté demeure donc si l’on autorise une insertion plus longue au quatrième mot tout en gardant les mêmes tables admissibles sur la paire initiale.

## Calcul et contrôle

Le programme a été écrit avant lecture des résultats du calcul principal. Il n’utilise aucun de ses modules. Il énumère les vecteurs de longueurs des six unités distinctes de la paire de départ. Un vecteur détermine les positions de découpe. À chaque emplacement, des unités identiques doivent extraire rigoureusement la même suite. Pour le troisième mot, on ajoute les longueurs des trois nouvelles unités `sh`, `d`, `y`. La somme des valeurs vides de la table reste limitée à un seul signe. Le quatrième mot est soumis à la comparaison après l’apprentissage. Un contrôle artificiel vérifie la récupération d’une table avec émission de deux lettres, puis l’émission vide pour `l` ou `d`, dans les deux sens de lecture des unités. [Programme autonome](contre_calcul.py) · [Corpus latin](../latin/SOURCE.md) · [Corpus français sur photographie](../francais/RAPPORT.md)

Exécuter `python3 -B contre_calcul.py` depuis ce dossier pour régénérer les résultats. Les empreintes des deux corpus accompagnent les positions et les tables dans le JSON.
