# Registre des fragments rapprochés d’une grande plante

Ce registre rassemble les propositions iconographiques documentées par les deux enquêtes du 17 novembre 2026 et leur pilote de la phase 45. Il conserve aussi la référence à l’épreuve ultérieure du fragment 25. Une entrée représente un fragment numéroté. Plusieurs sources qui montrent le même couple enrichissent sa provenance. Le numéro de cahier est celui du petit dessin pharmaceutique.

| Cahier source | Fragments numérotés | Attache sûre | Faible | Loci multiples | Sans locus | Pilotes non cotés | Un locus et une cible attribuée | Attache sûre et cible retrouvée par les deux lecteurs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 15 | 14 | 5 | 9 | 0 | 0 | 0 | 13 | 0 |
| 19 | 26 | 5 | 8 | 1 | 10 | 2 | 15 | 1 |

Les 40 fragments ont 43 propositions de dessin attribuées et 41 pages cibles distinctes. Pour les 30 fragments ayant au moins une légende, la conservation de toutes les combinaisons donne 34 triplets fragment–locus–dessin. Deux montages dont la découpe englobe plusieurs plantes restent à part. Les 28 fragments avec une seule étiquette et une seule destination attribuée comprennent les attaches faibles et les deux pilotes.

**Attache et reconnaissance.** Une attache sûre signifie que le contrôle spatial antérieur attribue le groupe écrit à la petite plante sans voisin concurrent raisonnable. La double reconnaissance signifie que chacun des deux lecteurs de sa carte a choisi la page **attendue** avec confiance moyenne ou forte. Les deux avis sont ceux de lecteurs IA sur les mêmes images. `null` signifie qu’aucune carte cotée n’a été retrouvée pour ce fragment. Le JSON donne aussi les choix individuels, leur confiance et les abstentions. La carte V09 représentait le mauvais dessin. Les réponses sont archivées et désactivées. V09b montre le fragment 225.

Les cinq attaches sûres du cahier 15 concernent les fragments 11, 22, 26, 35 et 52. Celles du cahier 19 concernent les fragments 94, 113, 116, 217 et 225. Les deux lecteurs ont choisi la cible dans les conditions requises pour les fragments 80, 94, 133, 136, 188 et 207, tous du cahier 19. Parmi les six, seul **94, f99r.46 → f96v**, possède aussi une attache sûre. Pour 207, l’absence de légende empêche tout test textuel.

**Choix concurrents.** Le fragment 40 possède un locus et deux cibles, f87r et f87v. Le fragment 110 possède deux loci, f99v.27 et f99v.28, et deux cibles, f34v et f90v1. Le registre conserve les quatre combinaisons. Le fragment 150 possède deux cibles mais aucune étiquette. La projection de l’ancien protocole vers la première ligne du dos est donnée séparément sous `prior_destinations`. Pour f90r2 ou f90v1 elle porte sur plusieurs panneaux de l’autre face. Pour f57r, elle est vide. La page du dessin f57r a bien fait l’objet d’un test exact ultérieur.

MK04 rapproche f55r d’une découpe qui couvre les fragments 53 ou 54 de f89v2. MK05 rapproche f41r d’une découpe qui couvre les fragments 27 ou 28 de f89r1. Chaque montage est une seule observation ambiguë. Le CSV représente ses deux possibilités avec le même identifiant. Les fragments 54 et 28 ont chacun une proposition documentaire attribuée séparément, dont le registre conserve la provenance. MK01 reprend 50 → f10v et MK03 reprend 168 → f4v. Ce pilote public couvre huit montages de Knowles. Le chiffre annoncé d’environ 108 comparaisons ne donne pas les coordonnées des autres propositions.

**Attaches discutées et pilotes.** Pour 86, la préparation note une attache nette et la contre-lecture signale une ambiguïté. Le classement final est faible et les deux avis figurent dans les preuves. Pour 25, le contrôle ancien signale une plante voisine. Le travail de localisation du 18 novembre appuie l’attribution de f89r1.4 au troisième dessin. Ce contrôle ultérieur est référencé séparément. Les anciens pilotes 212 et 213 possèdent chacun une inscription au-dessus du fragment. Le coordinateur les a examinés sur les vues de Yale, puis la phase 45 les a déjà testés sur f18v et f23r. Leur dossier ne comporte pas la cotation d’attache du lot suivant ni un vote de deux lecteurs. Ils ont leur propre classe. La phase 45 avait aussi testé 240 → f19r, repris ensuite dans les neuf cartes de la première campagne.

**Dépendances.** Les fragments 94 et 116 visent tous deux f96v. Les fragments 209 et 217 visent f53r, avec une légende seulement pour 217. La cible de 113, f55r, apparaît aussi sur le montage ambigu MK04. Le champ `target_folio_shared_with` repère les feuillets cibles identiques même lorsque les panneaux ou les côtés diffèrent. Les étiquettes de 212 et 213 viennent d’une même rangée de f102r2. Les résultats sur un même feuillet physique demandent un regroupement explicite.

**Antériorité des tests.** `prior_tests` distingue les épreuves exactes sur le corps, les premières lignes au dos, les lectures variantes et les cas inscrits au protocole mais inévaluables. `VARIANTES.json` porte sur huit triplets et sept loci. Les anciens mots, scores, positions des concordances et lignes cibles n’interviennent dans aucune décision de ce registre. Les provenances couvrent les campagnes citées. L’absence d’une épreuve dans cette colonne ne garantit aucune antériorité ailleurs.

## Reproduction

Les fichiers `sources.json`, `extraire_sources.py` et `construire.py` permettent de répéter l’assemblage hors ligne avec Python 3 depuis ce répertoire.

```sh
python3 -B construire.py --out sortie
cmp registre.json sortie/registre.json
cmp registre.csv sortie/registre.csv
cmp audit.json sortie/audit.json
```

Le premier étage conserve les champs documentaires et les empreintes des 30 fichiers sources complets. Les scripts utilisent des chemins relatifs à la racine du dépôt. Pour refaire également l’extraction à partir de l’arbre de recherche complet et du dépôt de publication, passer ces deux racines. Les archives photographiques et quelques tables de préparation ne sont pas distribuées intégralement dans l’arbre public. La copie réduite `sources.json` suffit à refaire les tables publiées.

```sh
python3 -B extraire_sources.py CHEMIN_DEPOT_RECHERCHE --publication CHEMIN_DEPOT_PUBLICATION --out sources_reconstruites.json
cmp sources.json sources_reconstruites.json
```

## Sources graphiques

La provenance est détaillée proposition par proposition dans `evidence`, par chemin de fichier et URL quand disponible. Les deux notices alimentent l’inventaire initial. Les notes marginales et Stolfi fournissent les renvois complémentaires. Le recadrage du n°240 explique l’écart avec l’indication de colonne de Stolfi. [Cahier 15](https://voynich.nu/q15/index.html) · [Cahier 19](https://voynich.nu/q19/index.html) · [Table des notes de Petersen](https://www.voynich.nu/extra/herb_oldid.html) · [Planches de Stolfi](https://www.ic.unicamp.br/en/~stolfi/EXPORT/voynich/00-06-07-word-grammar/Notes/064/work/projects/voynich/projects/programs/c/big/big/projects/voynich/Notes/102/work/Notes/091/report/report_091.html) · [Montages de Knowles](https://www.voynich.ninja/thread-4067.html)
