# Le mot `otor` désigne-t-il couramment une étoile du zodiaque ?

**Aucune des 299 légendes zodiacales ne contient le groupe entier `otor`, dans l’une ou l’autre transcription. Aucune lecture incertaine de ces légendes n’est compatible avec lui.** Deux textes circulaires des mêmes panneaux contiennent le groupe dans les deux éditions. La prédiction demandait une rencontre dans chacune de ces deux classes. Une légende de fragment végétal porte également le groupe dans les deux éditions et sous les deux conventions d’espacement. Le résultat laisse ouverte la possibilité d’un nom propre particulier à f68r1. [Protocole fixé](TRANSFERT-OTOR.md) · [Résultats, rencontres et lectures incertaines](otor-resultats.json)

## Fréquences observées

Chaque case donne les loci contenant le mot sur tous les loci de sa classe, puis les occurrences sur tous les groupes de cette classe. Les dénominateurs incluent les groupes incertains. La comparaison entre les deux conventions concerne les espaces douteux indiqués par une virgule dans la transcription.

| Emplacement | ZL, espaces séparés | ZL, espaces joints | IT2a, espaces séparés ou joints |
|---|---|---|---|
| Légendes zodiacales des douze panneaux (Lz) | 0/299 · 0/350 | 0/299 · 0/336 | 0/299 · 0/367 |
| Cercles de ces panneaux (C) | 2/36 · 2/966 | 2/36 · 2/860 | 3/36 · 3/963 |
| Légendes de fragments végétaux (Lf) | 2/194 · 2/210 | 1/194 · 1/203 | 3/194 · 3/215 |
| Légendes de récipients (Lc) | 0/40 · 0/40 | 0/40 · 0/40 | 0/37 · 0/40 |
| Légendes de personnages des bains (Ln) | 0/63 · 0/65 | 0/63 · 0/64 | 0/63 · 0/68 |
| Légendes de tubes ou bassins (Lt) | 0/47 · 0/56 | 0/47 · 0/53 | 0/47 · 0/55 |

Un emplacement correspond ici à un locus IVTFF. Deux lignes d’une légende peuvent avoir deux identifiants. Par exemple f99r.6 et f99r.7 concernent le même fragment. Une entrée que IT2a déclare fictive (`f89v2.26,!Lf`) est écartée. Les dénominateurs de mots lisibles seulement et chaque exclusion se trouvent aussi dans le JSON. Les catégories de contrôle couvrent tous les loci Lf, Lc, Ln et Lt des deux fichiers. [Catalogue et transcriptions de Zandbergen](https://www.voynich.nu/transcr.html) · [Format IVTFF conservé dans le dépôt](../../../../voynich_phase8/data/IVTFF_format.txt)

## Où se trouve `otor` ?

- Dans les cercles, les deux éditions le donnent à **f70v1.1** (Bélier) et **f71v.12** (Taureau). Une troisième lecture à **f72r1.12** (Taureau) dépend de l’édition. IT2a donne `otor` et ZL `otar` devant `chokaiin`. Dans les douze panneaux, les marques incertaines compatibles se limitent à des groupes entiers illisibles `???` dans les cercles de f72r3.1 et f72v3.1 (ZL), et de f71v.1 (IT2a). Ils ne fournissent aucun trait positif en faveur d’`otor`. [ZL3b](https://www.voynich.nu/data/ZL3b-n.txt) · [IT2a](https://www.voynich.nu/data/IT2a-n.txt)
- **Sur f99v.3**, les deux éditions donnent `otor<->chy`, auprès d’une racine dans la rangée supérieure. Dans le recadrage de Yale, la forme lue `otor` est sous le coude de la tige et le groupe suivant est à sa droite. Une petite zone sombre au contact de la tige rend l’extrémité du premier groupe moins nette. La convention IVTFF traite l’interruption du texte par un élément de dessin (`<->`) comme une séparation de mots. Le premier groupe compte donc sous les deux traitements des virgules. Il s’agit d’un contre-exemple à un emploi exclusif de ce groupe auprès d’étoiles. [Recadrage natif des groupes et de la racine](otor-f99v-haut.png) · [Fac-similé Yale, f99v](https://collections.library.yale.edu/catalog/2002046?child_oid=1006247)
- À **f88r.24**, ZL donne `otor,am` et IT2a `otor.am`. À **f89v1.22**, IT2a donne `otor.chos` et ZL `otorshos`. Le libellé de bain **f77r.4** donne `otork` dans les deux éditions. La comparaison porte sur un mot complet et conserve son `k` final. Aucune lecture incertaine compatible avec `otor` n’a été relevée dans les quatre classes de contrôle. [ZL3b](https://www.voynich.nu/data/ZL3b-n.txt) · [IT2a](https://www.voynich.nu/data/IT2a-n.txt)

## Rejeu

Exécuter `python3 otor-compter.py` depuis ce dossier. Le script vérifie les empreintes de ZL3b et IT2a, exclut les commentaires et teste chaque groupe. Il examine explicitement les choix entre crochets, les caractères illisibles isolés et les suites illisibles de longueur inconnue. Seuls les groupes certains entrent au numérateur. Le fichier JSON conserve la transcription originale de chaque rencontre et de chaque groupe incertain ainsi que son rang pour chacune des conventions. [Code du test](otor-compter.py) · [Résultats détaillés](otor-resultats.json)

Le recadrage a été extrait sans redimensionnement ni retouche du JPEG de Yale OID 1006247 (2 802 × 3 697 pixels), rectangle `x=515, y=116, largeur=1065, hauteur=322`. Empreinte SHA-256 du JPEG `111f6dfc34b8ecb9230cb5a0d144afef4cbd788048ddda2f440108941c91d5e5`. [Image source IIIF](https://collections.library.yale.edu/iiif/2/1006247/full/full/0/default.jpg)

Sur le détail photographique de f99v.3, la fin du premier groupe touche le contour d’une tige. Un autre transcripteur lit `otos`. [Tracé de la tige et variantes historiques](photo-f99v/LOCALISATION.md)
