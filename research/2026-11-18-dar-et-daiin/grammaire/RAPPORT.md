# Que peut-on déduire du mot entre deux groupes identiques ?

**Le fait d’être entouré du même groupe ne suffit pas à lire `dar` ou `daiin` comme un nom, un article ou une préposition.** Dans des recettes connues, cette disposition permet parfois de retrouver le mot central exact. En cachant le centre et en retirant toute la face concernée de l’apprentissage, la même règle fait 41 prédictions sur le Voynich. Les 41 échouent. [Test des mots masqués](MOT-AVANT.md) · [Prédictions, témoins et résultats à chaque emplacement](MOTS.json.gz)

Les deux séquences de départ, `qokol daiin qokol` sur f18v.7 et `qokchol dar qokchol` sur f23r.7, se trouvent sur le même bifeuillet. Pour le test manuscrit, les deux feuillets entiers ont été retirés, ainsi que f14, déjà consulté. Un encadrement *X B X* désigne trois groupes consécutifs avec un centre B différent de X. Aucun calcul ne confère de valeur phonétique aux signes. [Protocole initial](AVANT.md) · [Disposition des deux grandes pages](../../2026-11-18-renvois-entre-plantes/composant/BIFEUILLET.md)

## Ce que montrent les textes lisibles

- **Une préposition.** Chez Martino, trois recettes emploient *grado in grado*, au sens de « par degrés » ou « couche après couche ». En masquant le mot central et en excluant chaque recette tour à tour, les autres occurrences permettent de retrouver *in* trois fois. [Édition du *Libro de arte coquinaria*](https://www.uni-giessen.de/de/fbz/fb05/germanistik/absprache/sprachverwendung/gloning/tx/martino2.htm)
- **Une conjonction.** Dans le *Viandier*, *lardez le et le mengez* relie deux instructions. Les deux *le* reprennent le lièvre ; le groupe central *et* coordonne les verbes. Dans une autre entrée, la même construction sert à décrire comment préparer un esturgeon. Le test récupère *et* dans les deux entrées en laissant de côté celle qu’il prédit. [*Viandier*, version de la Vaticane](https://histolf.ulb.be/index.php/textes-gh/260-1450-viandier-taillevent-ms-vaticane-texte-et-traduction)
- **Un nom et une énumération.** Chez Martino, *de pollastri, de capponi, de capretti* présente trois volailles ou viandes possibles. *Capponi* (« chapons ») est le centre de *de capponi de*. L’énumération est la construction de la phrase ; le nom désigne l’un des éléments. Dans le *Viandier*, le même calcul récupère aussi le nom *boullon* entre deux *de*. [Édition de Martino](https://www.uni-giessen.de/de/fbz/fb05/germanistik/absprache/sprachverwendung/gloning/tx/martino2.htm) · [Lieux dans les deux ouvrages](MOTS.json.gz)

Sur les 1 415 encadrements des sept sources, le lexique restreint classe 160 centres, dont 145 noms, 10 coordonnants et 5 prépositions. Il laisse 60 graphies ambiguës et 1 195 hors lexique. Il couvre surtout les noms de matière et d’anatomie et certains mots grammaticaux. La proportion de 145/160 décrit cet échantillon de formes reconnaissables. Une forme telle que le français *le* peut aussi être un pronom. [Lexique appliqué](lexique.py)

Le classifieur doit annoncer une catégorie avant de voir B. Il apprend sur six ouvrages, avec le même poids pour chaque ouvrage qui fournit des exemples, puis teste le septième. Son seul indice est le rang de X, parmi les dix graphies les plus fréquentes du livre ou en dehors de ces dix. La fréquence est calculée sans l’unité où figure la fenêtre. Pour le témoin, le classifieur ignore ce rang. Voici également, dans la dernière colonne, l’épreuve distincte où l’on doit retrouver le **mot entier**, avec apprentissage dans d’autres chapitres ou recettes du même ouvrage.

| Source réservée | Encadrements | Catégories justes / classables | Catégories justes en ignorant le rang | Mots exacts / annoncés |
|---|---:|---:|---:|---:|
| Celse | 936 | 53/73 | 67/73 | 21/781 |
| *Macer* | 14 | 2/3 | 2/3 | 0/2 |
| Mayence, 1485 | 2 | 0/0 | 0/0 | 0/0 |
| RIDGES | 115 | 6/8 | 6/8 | 7/59 |
| Martino | 203 | 47/57 | 54/57 | 26/78 |
| *Régime* | 11 | 0/0 | 0/0 | 0/0 |
| *Viandier* | 134 | 16/19 | 16/19 | 9/107 |
| **Total** | **1 415** | **124/160** | **145/160** | **63/1 027** |

Le témoin qui ignore le rang de X annonce « nom » dans chacun des sept retraits. Pour les mots entiers, le programme utilise le centre le plus fréquent des autres *X B X* avec le même X, avec abstention en cas d’égalité. Il exclut le chapitre de Celse, la notice botanique du *Macer*, l’entrée ou la recette, la page de Mayence ou du *Régime*, ou le fichier-source de RIDGES. Sur les 907 lieux où l’apprentissage par encadrement et l’apprentissage sur les suites ordinaires *X B Z* proposent tous deux un mot, le premier retrouve 54 centres, le second 6. Pour 1 023 des 1 027 annonces, il existe en plus des fenêtres témoins ordinaires avec le même X et le même tiers de position, hors de l’unité testée. Le mot annoncé est exact 61 fois dans ces encadrements, pour 4,02 attendus d’après la fréquence du même mot dans leurs témoins. Les occurrences de la même formule au sein d’un ouvrage peuvent être liées. [Résultats par catégorie](HISTOIRE.json.gz) · [Résultats par mot](MOTS.json.gz)

## Les articles et les autres classes dans les herbiers allemands

La couche grammaticale publique de RIDGES permet de vérifier la couverture du petit lexique sur les six extraits allemands de 1482 et 1487. Sur 115 encadrements, 114 centres s’alignent sur une seule étiquette. On compte 43 noms communs, 3 noms propres, 24 formes verbales, 18 formes adjectivales, 7 prépositions, 3 étiquettes d’article, une conjonction de coordination et une conjonction de subordination. Les autres étiquettes figurent dans l’archive. Le classement automatique se fonde sur la normalisation de l’allemand historique. Il faut parfois lire la phrase pour distinguer un article d’un pronom. Ainsi, dans *hat die hat*, *die* est étiqueté article alors qu’il est suivi d’un verbe fini. Le chiffre de trois est un décompte d’étiquettes, sans validation manuelle de trois articles. [Règle déposée avant ouverture des étiquettes](RIDGES-AVANT.md) · [Toutes les étiquettes et leur contexte](RIDGES-POS.json.gz) · [Méthode d’annotation de RIDGES](https://ridges.pages.cms.hu-berlin.de/corpus/guidelines/auto-annotationen.html)

En annonçant « nom commun » lorsque les deux groupes extérieurs ont chacun une étiquette d’article ou de préposition, on tombe juste **28 fois sur 40**. Pour 36 de ces cas, on dispose aussi de fenêtres avec des extérieurs différents mais les mêmes étiquettes, le même mot à gauche, la même édition et le même tiers de position. On obtient 25 succès sur ces 36 encadrements, pour 19,20 attendus d’après 63 fenêtres témoins distinctes. Par exemple, dans *mit Wein mit*, le centre est le nom « vin ». Cette règle exige de connaître les catégories des mots extérieurs. Nous n’avons pas cette information pour `qokol` et `qokchol`. [Classes, témoins et calcul](RIDGES-POS.json.gz) · [Sources, auteurs, licence CC BY 3.0 et préparation des six extraits](../../2026-11-18-phrase-et-doublets/lecture/RIDGES-SOURCES.json)

## Application aux autres lignes du Voynich

Le test de fréquence utilise uniquement les formes écrites. Si X appartient aux dix formes les plus fréquentes, il prédit un centre moins fréquent que X ; sinon il prédit un centre plus fréquent. Les fréquences se calculent hors de la face concernée, et les trois groupes doivent se suivre dans les quatre lectures sans traverser une interruption. Dans les textes connus, sur 1 408 encadrements comparables, le test réussit 1 117 fois, pour 1 101,82 attendus selon 28 340 fenêtres témoins distinctes. Le gain varie selon les ouvrages. Le témoin est apparié sur X et le tiers de position, au sein de l’ouvrage ou de la section du Voynich. [Effectifs par ouvrage](HISTOIRE.json.gz) · [Tous les encadrements du manuscrit](VOYNICH.json.gz)

| Centre révélé dans le Voynich | Encadrements | Fréquences prédites correctement | Succès parmi les cas appariés | Succès attendus selon les témoins |
|---|---:|---:|---:|---:|
| Tous | 173 | 99/173 | 91/160 | 95,86 |
| `dar` | 3 | 2/3 | 2/3 | 1,69 |
| `daiin` | 6 | 4/6 | 2/4 | 3,30 |

Pour le test du **mot entier**, il reste 173 emplacements répartis dans 14 201 fenêtres possibles de prose. Il y a une annonce unique pour 41 d’entre eux, **aucune exacte**, contre 0,97 attendue d’après les témoins ordinaires. Sur les 34 positions où les deux modèles proposent un mot, la règle d’encadrement obtient 0 succès et le modèle des suites ordinaires 2. Parmi les neuf centres qui se révèlent être `dar` ou `daiin`, huit donnent lieu à une abstention. Sur f83r.3 la règle propose `ol` et la transcription donne `daiin`. Les échecs et les faibles effectifs laissent ouvertes plusieurs fonctions possibles. Ils ne justifient d’attribuer ni un sens botanique ni une catégorie grammaticale à l’une des deux formes. [Les neuf lieux, les annonces et les abstentions](MOTS.json.gz)

## Reproduction

Depuis ce dossier, avec Python 3, les trois premiers arguments correspondent au XML Perseus de Celse et aux éditions HTML du *Viandier* et de Martino. Le quatrième fichier est l’archive générale de RIDGES 9.0, dont le script extrait lui-même `excel/Excel_9-0.zip`. Les trois empreintes externes figurent dans `HISTOIRE.json.gz`, celles des six classeurs dans `RIDGES-POS.json.gz`. Le nom du script principal est `categories_centres.py`. [Éditions et provenance des corpus](../../2026-11-18-renvois-entre-plantes/phrase/RAPPORT.md) · [Archive RIDGES à télécharger](https://www.laudatio-repository.org/download/format/3/35/9.0)

```sh
python3 -B categories_centres.py CELSE.xml VIANDIER.html MARTINO.html
python3 -B centres_masques.py CELSE.xml VIANDIER.html MARTINO.html
python3 -B ridges_pos.py RIDGES-9.zip
```

Les sources historiques ont des tailles et des époques très différentes. Les limites de paragraphe, de recette et la ponctuation retenue par les éditions modifient les fenêtres accessibles. Des virgules peuvent notamment séparer des termes d’une liste. Les passages du manuscrit et certains exemples historiques avaient déjà été consultés. Le masquage retire le centre ou la face au programme qui formule la prédiction. Il ne constitue pas une première lecture en aveugle par l’équipe.
