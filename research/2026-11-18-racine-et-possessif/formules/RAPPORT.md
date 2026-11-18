# Peut-on découvrir « sa racine » à partir des seuls voisinages ?

**Sur un herbier dont on connaît la langue, le classement aveugle place le possessif latin *eius* au seizième rang.** Lorsqu’on lui fournit le mot correct et les deux débuts de mots cherchés, ces éléments se retrouvent ensemble huit fois sur sept autres plantes. Ce décalage mesure une difficulté du déchiffrement. Une formule que l’on sait reconnaître sur de nouvelles pages peut rester difficile à découvrir dans une écriture inconnue. [Règle enregistrée](PROTOCOLE.md) · [Tous les scores et les lignes](resultats.json)

## Le classement sur les 39 notices d’apprentissage

Nous avons écarté *Chelidonia*, la notice n° 52 où la copie de 1478 nous avait donné les deux expressions. Les 39 notices impaires fournissent 1 158 vers d’apprentissage et les 37 autres notices paires, 1 092 vers réservés. Chaque mot de droite peut être suivi dans tout le poème. Un mot de gauche appartient à une famille si ses trois premières lettres sont communes à plusieurs graphies du vocabulaire d’apprentissage. L’algorithme n’utilise ni lexique latin ni glossaire. En remplaçant chaque lettre du texte d’apprentissage par un symbole privé aléatoire de manière bijective, nous avons vérifié que les rangs de tous les mots de droite et de toutes leurs familles restent identiques. Les lettres i et j de l’édition avaient été réunies avant cette opération. [Programme complet](classer.py) · [Source, crédits et graphie de l’édition](../../2026-11-18-opcheor-paralleles/latin/SOURCE.md)

Parmi 2 294 mots distincts en position de droite, 54 suivent au moins deux familles qui satisfont aux critères. *Si* obtient le premier rang, *modo* le deuxième et *vel* le troisième. Pour le mot recherché *eius*, les mots commençant par *fol* arrivent premiers parmi ses familles. Il s’agit chaque fois de *foliis*, à trois emplacements sur deux plantes. Les mots commençant par *rad* arrivent neuvièmes, avec *radicibus* et *radices*, chacun sur une plante. D’autres voisinages réguliers concurrencent ceux des deux organes. La famille *vis* précède ainsi *eius* dans trois notices. Voici les rangs et les contextes de chaque couple pour le possessif. [Classement détaillé, champ audit_cle](resultats.json)

## Les occurrences dans la réserve

| Mot fléchi avant *eius* | Notice et numéro du vers | Occurrences |
|---|---|---:|
| *foliis* | *Urtica* 125, *Papaver* 1062, *Asarum* 1558 | 3 |
| *radices* | *Plantago* 236, *Violae* 1366 | 2 |
| *radicis* | *Colubrina* 1741 et 1750 | 2 |
| *radicibus* | *Verbena* 1873 | 1 |

Les huit mots appartiennent bien aux deux noms d’organes selon la concordance de l’édition. Pour la racine, les mots correspondent selon le vers à « ses racines », « de sa racine » ou à une forme plurielle à l’ablatif. Pour les feuilles, le vers 1558 demande de prélever trente unités fraîches. Les huit passages donnent les positions et les vers dans le relevé. [Concordance des organes dans le texte entier](../../2026-11-18-legendes-repetitions/temoin/occurrences.tsv) · [Réserve détaillée](resultats.json)

En redistribuant les mots à l’intérieur de chaque vers réservé, six des 999 mélanges donnent au moins huit rencontres. La probabilité de permutation estimée avec la correction qui inclut le texte observé est 0,007. Un calcul exact de la même distribution donne **0,00894** et une espérance de **3,24** rencontres sur les 19 vers pouvant former une paire. Les vers conservent leur vocabulaire et leur longueur. Ce témoin porte sur l’ordre local des mots. Certaines notices reprennent des vers formulaires entiers, ce qui limite l’indépendance des huit occurrences et la généralisation à d’autres auteurs. [Comptage et distribution exacte](resultats.json)

L’épreuve de découverte exigeait que le mot correct arrive dans les trois premiers et que les deux familles arrivent dans ses cinq premières. Le classement manque les deux critères. Respectant la règle déposée, nous n’avons appliqué aucun nom de possession ou de partie végétale aux groupes du Voynich par ce modèle. L’accord des huit occurrences réservées concerne les **réponses latines connues à l’avance**. [Feuillet de 1478 à l’origine de ces réponses](../../2026-11-18-legendes-repetitions/temoin/celidonia-65.jpg)

Pour reproduire les calculs, utiliser `python3 -B classer.py` depuis ce dossier. Le script vérifie l’empreinte du protocole et inscrit dans les résultats celles des trois données d’entrée. Le calcul exact fusionne des couples orientés de mots distincts dans les permutations d’un vers. Sa distribution élémentaire est aussi vérifiée en énumérant toutes les permutations d’un exemple de cinq mots.
