# Reconnaître un type de dessin à partir de la prose

Le vocabulaire d'un court extrait de prose contient un indice sur la section illustrée. Nous avons pris 18 feuillets attribués dans les métadonnées à la même main et à la même variété textuelle de Currier. Le partage alterné par numéro de feuillet donne neuf feuillets d'apprentissage et neuf autres à classer. La base de hasard « toujours herbier » réussirait 5/9. Le modèle ignore les légendes et les mots absents de son vocabulaire d'apprentissage. [Protocole](PROTOCOLE.md) · [Format des transcriptions, tableau 6](https://www.voynich.nu/software/ivtt/IVTFF_format.pdf)

| Lecture | Feuillets correctement classés | Herbier | Bains | Permutations atteignant ce score sur 15 876 |
|---|---:|---:|---:|---:|
| Takahashi, espaces incertains joints ou séparés | 9/9 | 5/5 | 4/4 | 35 |
| Zandbergen–Landini, espaces incertains joints | 8/9 | 5/5 | 3/4 | 292 |
| Zandbergen–Landini, espaces incertains séparés | 9/9 | 5/5 | 4/4 | 27 |

Les feuillets botaniques réservés sont f31, f34, f40, f46 et f55. Les bains sont f76, f78, f82 et f84. La seule erreur du premier essai est f78 dans ZL avec les espaces incertains joints. L'échantillon des bains de f76 commence sur f76v, seule face de ce feuillet répondant au critère de section. Les 40 emplacements sont disponibles pour chacun des 18 feuillets. En réserve, sur 360 emplacements, 359 ont une graphie simple en Takahashi, 346 en ZL joint et 349 en ZL séparé. Respectivement 181, 177 et 185 emplacements correspondent à un mot rencontré dans l'apprentissage et contribuent au score. La même série de photographies sous-tend les deux transcriptions. [Décisions sur identifiants opaques](PREDICTIONS.json) · [Classes de référence](CLE.json) · [Comptages complets, scores et distributions de hasard](RESULTATS.json)

## Que se passe-t-il sur une autre feuille de parchemin ?

Le partage par numéro de feuillet crée une proximité matérielle inattendue. Huit des neuf feuillets de réserve ont leur feuillet conjugué dans le lot d'apprentissage, les deux moitiés provenant de la même feuille de parchemin pliée. Seul f78 n'a aucun conjugué dans le lot d'apprentissage. Après l'épreuve principale, nous avons donc retiré du lot d'apprentissage, pour chaque cible, le feuillet conjugué déterminé par la paire d'attributs du cahier et du bifeuillet. Nous avons recalculé vocabulaire, probabilités et permutations. La taille d'apprentissage devient huit feuillets pour huit cibles et reste neuf pour f78. [Définition des variables Q et B](https://www.voynich.nu/software/ivtt/IVTFF_format.pdf) · [Contrôle complémentaire enregistré](CONTROLE_BIFEUILLET.md)

| Lecture | Réponses correctes | Herbier | Bains | Feuillets mal classés | Permutations atteignant ce score |
|---|---:|---:|---:|---|---:|
| Takahashi, deux traitements des espaces | 7/9 | 3/5 | 4/4 | f31, f46 | 1 596/15 876 (10,1 %) |
| Zandbergen–Landini, espaces incertains joints | 7/9 | 4/5 | 3/4 | f46, f78 | 1 514/15 876 (9,5 %) |
| Zandbergen–Landini, espaces incertains séparés | 8/9 | 4/5 | 4/4 | f31 | 337/15 876 (2,1 %) |

Les permutations changent les classes au niveau du feuillet en conservant les effectifs dans les deux lots. Les quatre bains réservés proviennent du même cahier M que les quatre bains utilisés pour l'apprentissage. Les dix feuillets botaniques proviennent de quatre autres cahiers (D à G). Le contraste reste donc compatible avec des différences de cahier, de mise en texte et de sujet. Les taux de permutation supposent l'échangeabilité des feuillets entre groupes, approximation particulièrement fragile ici ; ils ne sont pas des probabilités que l’écriture décrive le dessin. L'étude porte sur de la prose en début de page. Le résultat ne donne de sens individuel à aucun signe ni à aucun mot, et ne permet pas de trancher ce que décrit une phrase particulière. [Prédictions individuelles et contrôle par permutation](BIFEUILLET.json)

Pour reproduire, exécuter, dans le répertoire de cette note, les trois commandes ci-dessous avec Python 3 et le dossier de données du projet. Les transcriptions originales sont également publiées par leur éditeur. [Takahashi](https://www.voynich.nu/data/IT2a-n.txt) · [Zandbergen–Landini](https://www.voynich.nu/data/ZL3b-n.txt)

```sh
python3 -B prose.py predire /chemin/vers/voynich_20261028/data
python3 -B prose.py evaluer /chemin/vers/voynich_20261028/data
python3 -B bifeuillet.py /chemin/vers/voynich_20261028/data
```

L'empreinte SHA-256 du protocole au moment de son enregistrement est 49c3e4672f88b9d1e2c39b8c34c13a152030056229a24ba5f31c996f619b5855. Celle des prédictions écrites avant le dépouillement des réponses est 4aaad2e904e4add851f64a5f5186921b2e24af217a37cb8afa7d99fa65e2582d. L'aveugle concerne les entrées du classifieur. L'expérimentateur connaissait la provenance des folios.
