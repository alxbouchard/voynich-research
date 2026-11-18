# Le début ytoa près des luminaires de f68r1 et f68r2

**Aucune des six inscriptions retenues ne contient de récurrence lisible de `ytoa`, de `ytoaiin` ou de `ytoar`.** L’édition Zandbergen–Landini laisse une réserve dans le cercle solaire de f68r2.31. Elle code le dernier groupe par quatre signes spéciaux, `@231;@232;@233;@234;`. Nous le conservons comme indéterminé pour une lecture en alphabet EVA de base. L’autre édition donne `koiin` à cet endroit. [Dépliant Yale](https://collections.library.yale.edu/iiif/2/1006196/full/full/0/default.jpg) · [Délimitation des figures](../sources/LUMINAIRES.md)

## Occasions de retrouver la séquence

Chaque cellule donne le **nombre de groupes où le test de préfixe peut trancher, puis le nombre total de groupes**. Les trois lignes dans le disque solaire de f68r1 et les trois bandes circulaires constituent six loci. Une lecture intérieurement incertaine peut exclure `ytoa` grâce à sa première lettre lisible. Les chiffres du tableau incluent ces exclusions. Les trois recherches donnent chacune zéro occurrence sur les deux panneaux. [Résultats détaillés](resultats.json)

| Partie du dessin | ZL3b, espaces douteux joints | ZL3b, séparés | IT2a, les deux traitements |
|---|---:|---:|---:|
| Soleil de f68r1, .5–.7, trois lignes | 3 / 3 | 3 / 3 | 3 / 3 |
| Lune de f68r1, .37, bande | 5 / 5 | 5 / 5 | 5 / 5 |
| Lune de f68r2, .6, bande | 8 / 8 | 8 / 8 | 8 / 8 |
| Soleil de f68r2, .31, bande | 10 / 11 | 11 / 12 | 11 / 11 |
| **Quatre figures** | **26 / 27** | **27 / 28** | **27 / 27** |
| Reste de f68r1, 33 loci | 56 / 57 | 56 / 57 | 57 / 57 |
| Reste de f68r2, 29 loci | 61 / 61 | 62 / 62 | 62 / 62 |

Sur les quatre figures, 23 groupes ZL joints et 24 séparés ont une lecture intégrale unique en caractères EVA ordinaires. IT2a en a 25. Parmi les inscriptions restantes, l’autre début non résolu en EVA de base se trouve dans une légende d’étoile, f68r1.30, qui commence par `@167;` en ZL. Les autres textes de f68r1 comprennent 29 légendes d’étoiles et quatre lignes de paragraphe. Ceux de f68r2 comprennent 24 légendes d’étoiles et cinq lignes de paragraphe. La photographie situe les inscriptions testées dans le disque ou la bande. Leur fonction reste inconnue. [Images et inventaire des loci](../sources/LUMINAIRES.md)

## Toutes les occurrences positives du manuscrit

| Locus | Type de la transcription | ZL3b | IT2a |
|---|---|---|---|
| f2r.14 | Lp, étiquette sur une feuille | `ytoail` | Locus absent. Le dernier locus de cette page est .13. |
| f67r2.37 | L0, étiquette du panneau astronomique | `ytoaiin` | `ytoaiin` |
| f72r3.30 | Lz, étiquette du zodiaque | `ytoar` suivi de `shar` | `ytoar` suivi de `shor` |

Les trois attestations ZL et les deux IT2a survivent aux deux traitements de l’espacement. La photographie confirme que la première se situe sur le bord d’une foliole. L’auteur de l’hypothèse l’avait déjà signalée. Les trois lectures ZL de ce tableau occupent toutes le premier groupe de leur locus. [Folio botanique, détail Yale](https://collections.library.yale.edu/iiif/2/1006078/2100,1220,490,380/full/0/default.jpg) · [Fichier Zandbergen–Landini](https://www.voynich.nu/data/ZL3b-n.txt) · [Relevé antérieur, oshfdk](https://github.com/oshfdk/f67r2planets/blob/9cdd099422878e1524b9a5be6ba7674359999ba6/meaning.md#prefix-probabilities-in-a-text)

| Corpus | ZL3b joints, positifs / tranchables / total | ZL3b séparés | IT2a |
|---|---:|---:|---:|
| Légendes L | 3 / 1 135 / 1 149 | 3 / 1 184 / 1 199 | 2 / 1 034 / 1 046 |
| Paragraphes P | 0 / 32 526 / 32 612 | 0 / 34 981 / 35 075 | 0 / 34 454 / 34 491 |
| Textes circulaires C | 0 / 2 146 / 2 184 | 0 / 2 359 / 2 398 | 0 / 2 002 / 2 029 |
| Textes radiaux R | 0 / 333 / 333 | 0 / 354 / 354 | 0 / 352 / 353 |
| **Ensemble** | **3 / 36 140 / 36 278** | **3 / 38 878 / 39 026** | **2 / 37 842 / 37 919** |

Le calcul distingue les espaces francs des virgules IVTFF et conserve les coupures dues à un dessin. Les variantes entre crochets sont lues séparément. Un résultat est tranchable si toutes les lectures concordent. Le programme s’arrête au premier signe inconnu rencontré avant toute différence certaine. Ce choix conservateur laisse certains groupes sans décision, y compris lorsque des lettres postérieures pourraient aider à les exclure. Une lettre différente au début suffit à exclure le préfixe malgré une fin abîmée. Les résultats donnent également le décompte des initiales, des quatre premiers caractères ordinaires et des formes entièrement lisibles. [Programme](verifier.py) · [Dénombrements et empreintes des éditions](resultats.json)

Le relevé montre une concentration des occurrences observées dans les légendes et l’absence de transfert lisible sur les quatre figures retenues. Les six inscriptions testées appartiennent à des paragraphes courts ou à des bandes circulaires. Elles ne portent pas de nom individuel vérifié. Le résultat laisse donc ouverte l’interprétation des deux formes des panneaux d’origine.
