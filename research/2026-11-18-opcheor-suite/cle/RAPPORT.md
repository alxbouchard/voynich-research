# Deux mentions d’une plante peuvent-elles se lire avec la même clé ?

À f89r2, la prose donne `opcheor opcheol shody`. À f100v, elle donne `okeor okeol dy`. Chaque lieu se trouve sur un panneau de fragments végétaux. Nous avons recherché deux passages distincts d’un même livre, en laissant les plantes, les mots et les sens libres de différer. La contrainte porte sur les signes que les deux passages ont en commun. Ils doivent conserver leurs valeurs. [Photographies des deux lignes](../photos/deux-lignes-de-depart.jpg) · [Règle fixée avant le calcul](AVANT.md)

Autoriser jusqu’à deux fusions différentes de deux signes EVA contigus, répétées partout, puis lire une ou deux lettres par unité, sans signe muet. Les 67 choix de fusion et les deux longueurs donnent 134 règles par ouvrage. Les fenêtres restent dans leur notice ou segment. Aucun des 111 144 triplets des quatre corpus n’aboutit à un couple de lieux qui satisfasse aux deux lignes avec la même table. Ce résultat dépend à la fois des sources et du type précis de substitution. Un témoin artificiel, avec fusion nécessaire et deux textes distincts, permet de retrouver la table exacte et de distinguer la vraie suite d’un leurre. [Prédictions, contrôles et clés](ANNONCES.json.gz)

| Source | Fenêtres de trois mots | Lieux qui s’ajustent aux trois premiers mots de f89r2 | Suites distinctes et vérifiables, comptées par lieu | Quatrièmes mots corrects |
|---|---:|---:|---:|---:|
| Celse | 80 756 | 12 | 21 | 0 |
| *Macer* | 13 813 | 1 | 3 | 0 |
| *Gart* de 1485, extraits | 201 | 0 | 0 | 0 |
| RIDGES, extraits de 1482 et 1487 | 16 374 | 2 | 2 | 0 |

Deux cas sont particulièrement parlants. Dans le passage sur les accès de fièvre, le latin de Celse *singulae singulis diebus* signifie ici « un [accès] chaque jour ». Les quatre lectures déterminées pour le mot suivant sont des variantes de *diebus* augmentées d’un ou deux caractères. Le véritable mot est *fiunt*, « se produisent ». Ailleurs, *digiti digitis ungues* est suivi de *unguibus*. Le passage compare les doigts et les orteils, puis leurs ongles. La même figure de répétition se prête donc à deux rapports grammaticaux différents dans un texte lisible. Les deux suites ont été retrouvées sur les pages de Florence de 1478. [Clichés et lecture du sens](../photos/fievres/RAPPORT.md) · [Tous les voisins effectivement lus](OUVERTURE.json.gz)

Une lecture italienne, obtenue avec un autre modèle, est assez naturelle pour tromper à l’oreille. *Pian piano col* figure dans une recette où l’on remue une soupe avec une cuillère. La clé ajustée sur les trois mots écrit *cnool*, tandis que le cuisinier écrit *cocchiaro*. La même clé échoue sur f19r après une paire compatible. [Manuscrit italien et vérification sur f19r](../vernaculaire/RAPPORT.md)

Pour reproduire, utiliser l’extrait XML de Celse figé à l’empreinte contrôlée par le lecteur du projet. Lancer `python3 -B chercher.py annoncer /chemin/celse.xml` puis `python3 -B chercher.py ouvrir /chemin/celse.xml`. La sortie des annonces conserve un représentant par lieu et quatrième mot proposé pour les ajustements de f89r2 seul. Les rapprochements entre deux lieux conservent les clés compatibles. Les sorties indéterminées sont explicites. [Code, critères de découpage et téléchargements](../../2026-11-18-phrase-et-doublets/lecture/RESULTAT.md) · [Programme](chercher.py)
