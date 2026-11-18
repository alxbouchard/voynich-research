# Le texte latin du Macer et deux pages d’un manuscrit de 1478

**Le témoin de calcul contient 77 notices complètes, 2 269 vers et 13 967 mots.** Chaque entrée de `corpus.json` donne les mots d’une notice dans leur ordre. Le premier mot de l’entrée *Aristolochia* est `aristolochiae`. Cette notice compte 42 vers et 256 mots. Le titre figure uniquement dans la clé. Le texte des vers, avec sa ponctuation, sa casse et les positions des mots, figure dans l’autre fichier. [Corpus de calcul](corpus.json) · [Les vers avec leurs repères](vers.tsv)

La source est la révision 272959 de la transcription latine du *De viribus herbarum*, attribué à Odon de Meung et diffusé sous le nom de Macer Floridus. Cette révision indique l’édition Panckoucke et *Corpus Corporum* (Zurich). Le poème date de la fin du XIe siècle. La copie italienne consultée ci-dessous date de 1478. Elle contient les mêmes deux notices, dans une suite différente de celle de l’édition. [Révision de Wikisource latin](https://la.wikisource.org/w/index.php?title=De_viribus_herbarum&oldid=272959) · [Source intégrale archivée dans le dépôt](../../2026-11-18-noms-dans-les-notices/historique/source.wiki.gz) · [Catalogue de Wellcome, MS.458](https://wellcomecollection.org/works/cfqd658f)

## Une aristoloche que l’on peut lire en 1478

Sur le verso du feuillet 7, l’initiale bleue ouvre la notice sous la rubrique **DE ARISTOLOGIA**. Au premier vers on lit *Aristologie*, où l’édition écrit *Aristolochiae*. Les lettres `ch` et la graphie finale `ae` de l’édition modifient donc la suite de lettres qu’une table de déchiffrement devrait produire. La comparaison ne suppose pas que ces deux témoins représentent la seule orthographe médiévale. [Recadrage de la rubrique et des cinq premiers vers](ms458-f7v.jpg) · [Photographie de Wellcome, canevas 18](https://iiif.wellcomecollection.org/image/b19209113_ms_458_0018.JP2/760,1920,2450,900/1500,/0/default.jpg)

Les deux vers suivants permettent de distinguer trois observations concrètes.

| Élément observé | Au feuillet 7v | Vers de l’édition |
|---|---|---|
| La racine | *radix* dans le deuxième vers, *radice* dans le troisième | `radix` au mot 8 et `radice` au mot 18 de la notice |
| La longue | Le deuxième vers commence par *lōga* et reprend *longa* avant *vocatur*. La barre abrège le premier *n*. | `longa` aux mots 6 et 11 |
| La ronde | Le troisième vers porte *rotunda* vers le début et reprend la même forme à la fin, avec des traits de nasalité. | `rotunda` aux mots 14 et 19 |

Un auteur médiéval peut répéter un nom et faire varier son cas, ou répéter le qualificatif de l’organe. Pour cette aristoloche, aucun des trois exemples n’est constitué de mots immédiatement adjacents. Les graphies d’*Aristologie* et de *radix* ont été lues sur le témoin visible. Les expansions de marques abrégées et l’identification des vers ont bénéficié de la comparaison avec l’édition.

## Une variation de l’ordre des mots

La rubrique du feuillet 8v est **DE YSOPO**, suivie d’*Est ysopum*. Cette ouverture correspond à la notice 45 du témoin de calcul, deux pages après l’aristoloche dans la copie. Plus bas, au troisième vers de la notice, le copiste a écrit *Sic simul ut cocta sint*. La transcription éditée à la position correspondante donne *sic ut cocta simul sint* (vers 1505). Une recherche qui impose deux mots immédiatement voisins dépend donc aussi du témoin choisi. Les sondages portent sur deux notices sélectionnées dont une concerne directement l’hypothèse botanique. [Recadrage de la notice de l’hysope](ms458-f8v.jpg) · [Photographie de Wellcome, canevas 20](https://iiif.wellcomecollection.org/image/b19209113_ms_458_0020.JP2/850,2220,2330,850/1500,/0/default.jpg)

## Extraction et contrôles

À partir de ce répertoire, `python3 -B preparer.py` régénère les deux fichiers à partir de la source intégrale déjà archivée. L’extracteur existant vérifie l’empreinte de la source, extrait le contenu des 77 blocs de poésie et enlève les marqueurs de vers. Les mots sont mis en minuscule et les signes diacritiques retirés. Les différences i/j et u/v restent dans la transcription. Il n’y a ni lemmatisation ni correction d’après le Voynich. La séparation par notice évite qu’un dernier mot soit apparié au premier de la suivante. Des mots voisins peuvent être sur deux vers ou deux phrases différents. [Programme](preparer.py) · [Extracteur du projet réutilisé](../../2026-11-18-noms-secteurs/herbier/mesurer.py)

Les 2 269 rangs de vers suivent l’ordre des lignes du poème conservé. Chaque groupe de mots du tableau TSV se raccorde exactement à la tranche indiquée de l’entrée JSON. Les numéros imprimés tous les cinq vers sont conservés tels que transcrits. Sur les 453 marques, cinq s’écartent du rang compté, aux rangs 55 (65), 1125 (1126), 1570 (1510), 1575 (1515) et 1750 (1150). La sixième rubrique, *Plantago*, répète le numéro V de la cinquième. La segmentation utilise les titres et leur ordre. Les vers 1395 et 1505 portent bien les numéros attendus dans la source.

| Fichier | SHA-256 |
|---|---|
| Source Wikisource décompressée | `41ca63622e4fbcc4f52c40d7c9261541c5b6d24ee59ebb2964ece69cee480e26` |
| corpus.json | `c251598bbab3f9f93de40a72d4e039c17f52ce079dd95e86c7322f9a2283893b` |
| vers.tsv | `ccbb4145e1e00f3f5a55259a47e661da39d514ebe53618eacf98f956db4c6b34` |
| ms458-f7v.jpg | `633e194176fa2e1650b43534dd4316c920fa390c4182974a539e5ebe906549db` |
| ms458-f8v.jpg | `42635f796deddfb7fbd4c40d8962a25cc5fe46f89e0077e5953d6542014fee57` |

**Crédits.** Texte médiéval et édition imprimée du domaine public. Pour la transcription numérique, crédit à Wikisource latin et à *Corpus Corporum*, Université de Zurich. Les modifications présentes sont le découpage, la suppression des balises, la normalisation des mots et l’indexation des vers. La page de Wikisource indique CC BY-SA 4.0. Le carnet de provenance du projet rapporte aussi les conditions distinctes affichées par *Corpus Corporum*. Les deux photographies portent la marque du domaine public de la Wellcome Collection. [Attributions et conditions de transcription](../../2026-11-18-noms-dans-les-notices/historique/README.md) · [Notice de la Wellcome Collection et droits des images](https://wellcomecollection.org/works/cfqd658f)
