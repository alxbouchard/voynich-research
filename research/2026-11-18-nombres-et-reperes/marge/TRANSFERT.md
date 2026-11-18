# Les cinq signes de f49v dans la roue de f57v et dans la marge de f76r

**Aucune des deux listes ne reproduit deux signes consécutifs de la série stricte dans l’ordre prescrit.** Pour le meilleur segment de cinq entrées, une seule position sur cinq correspond. La roue a été essayée dans les deux sens, depuis toutes ses positions, dans chacune des quatre répétitions. La marge de f76r a été lue de haut en bas puis, en sensibilité, de bas en haut. Le test concerne une notation qui conserverait à la fois les signes et leur ordre d’un feuillet à l’autre. [Règle fixée avant le calcul](../PROTOCOLE.md) · [Yale, f57v](https://collections.library.yale.edu/catalog/2002046?child_oid=1006187) · [Yale, f76r](https://collections.library.yale.edu/catalog/2002046?child_oid=1006210)

| Cible, même édition de part et d’autre | Ordre 12345, positions exactes sur 5 | Plus long bloc exact | Meilleur ordre concurrent, positions sur 5 | Ordres strictement meilleurs parmi 120 | Ordres à égalité, ordre prescrit compris |
|---|---:|---:|---:|---:|---:|
| f57v, ZL3b, meilleur des quatre quarts | 1 | 1 | 2 | 72 | 48 |
| f57v, H historique, meilleur des quatre quarts | 1 | 1 | 3 | 108 | 12 |
| f57v, IT2a, meilleur des quatre quarts | 1 | 1 | 3 | 108 | 12 |
| f76r, haut vers bas, chacune des trois éditions | 1 | 1 | 2 | 12 | 108 |
| f76r, meilleur des deux sens, chacune des trois éditions | 1 | 1 | 2 | 24 | 96 |

Sur la roue, ZL donne notamment `o`, `r` et `y`, mais les intercale parmi d’autres entrées. Les quatre quarts de ZL donnent séparément les mêmes résultats du tableau. L’ordre 12435, par exemple, fait mieux que 12345 en ZL. Chez H et IT, les quatre ordres 14253, 15243, 34251 et 35241 atteignent 3/5. Cela tient au dernier quart dont ces éditions transcrivent la fin en deux entrées, `r` puis `n`. Les trois autres quarts ont pour maximum 2/5. On prend le meilleur résultat pour chaque ordre parmi les quatre quarts, qui appartiennent à un seul anneau. [Transcription historique H de f57v](https://www.voynich.nu/q08/f057v_tr.txt) · [Comparaison des graphies sur la roue](../roue/QUATRE-TOURS.jpg)

La marge de f76r donne `s d q s o l k r s` dans les trois éditions. Dans l’ordre descendant, `o` et `r` sont aux rangs 5 et 8 de la liste. Un ordre qui les espace de trois positions, tel 13425, peut donc faire deux rencontres dans le même segment. Leurs emplacements ne reproduisent pas le début `o r` vu sur f49v. [Transcription historique H de f76r](https://www.voynich.nu/q13/f076r_tr.txt)

## Variantes, une hypothèse à la fois

- **Premier chiffre incertain.** Avec la série réduite 2345, la roue reste à 1/4 dans toutes les éditions. Sur f76r, le score descendant est 0/4. Le premier signe attendu, `r`, est bien présent au rang 8, où il ne reste que deux entrées pour une fenêtre de quatre. Le plus long fragment retrouvé reste donc de longueur un. Autoriser la remontée donne 1/4. En retirant plutôt le cinquième ancrage, 1234 donne au mieux 1/4 dans les deux listes.
- **Désaccord sur le signe pour 2.** Admettre `s` aussi bien que `r`, comme le permet la lecture F de f49v, ne change rien sur la roue ni sur f76r en descendant. En remontant f76r apparaissent `o s` aux rangs 5 puis 4, soit un fragment de 2 et un score de 2/5. Dans cette même variante avec les deux sens autorisés, 84 ordres sur 120 atteignent ce maximum.
- **Signes spéciaux.** Admettre également la forme 192 pour le 2, ou séparément la forme 163 pour le 5, laisse les résultats stricts inchangés dans les éditions qui identifient ces signes. IT2a laisse le cinquième signe inconnu. Aucun point ne lui a été attribué.
- **Séparation des entrées de la roue.** Scinder en ZL `@169;v` en deux entrées donne quatre quarts de 18. Réunir le `r,n` final de H ou IT en une seule entrée donne quatre quarts de 17. Dans les deux variantes, la série testée reste à 1/5 et le meilleur fragment est de longueur un. Dans chaque variante, 72 ordres concurrents atteignent 2/5. [Analyse antérieure des séparations](../../../voynich_phase41/RAPPORT.md)

## Reproduction

L’unité de comparaison est l’entrée délimitée par l’édition sur la roue ou le signe isolé dans la marge. Chaque essai cherche une fenêtre complète où aligner les valeurs, sans saut. Le « bloc » est le plus long morceau de la clé retrouvé sans interruption n’importe où dans la liste, même près du bord d’une marge. Un `?` et un `*` isolés n’apportent aucun point, même face à une autre inconnue. Les alternatives explicites du document sont conservées et les quarts de 18 ne sont jamais tronqués. Les 120 ordres sont les permutations exactes de cinq positions distinctes. Ce dénombrement donne une comparaison exhaustive à signes fixés, sans estimer la probabilité qu’un manuscrit soit chiffré.

Le script relit les fichiers ZL3b et IT2a du dépôt, vérifie leurs empreintes, puis charge les extraits historiques H, où chaque rangée de f49v peut être retrouvée dans la collation d’origine. Il conserve dans le JSON les entrées de chaque quart, les distributions de scores, les ordres concurrents maximaux du test principal et chaque sensibilité. Depuis ce dossier, exécuter `python3 transfert.py`. [Code](transfert.py) · [Données H](extraits-historiques-H.tsv) · [Résultats détaillés](transfert-resultats.json) · [Transcription ZL3b](https://www.voynich.nu/data/ZL3b-n.txt) · [Transcription IT2a](https://www.voynich.nu/data/IT2a-n.txt)
