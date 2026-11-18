# Quel mot suit les trois formes de la camomille dans la copie de 1478 ?

**Le copiste écrit `similis` en toutes lettres. Les formes qui précèdent sont `herba | Erba terra`, avec un retour à la ligne après `herba`.** La prédiction enregistrée, `taeam`, manque le mot suivant. La copie médiévale modifie aussi deux des trois mots sur lesquels la table avait été ajustée dans l’édition. [Prédiction antérieure à la localisation de la page](PREDICTION.md) · [Photographie du passage](ms458-f14v.jpg)

## Les deux vers

Le feuillet 14v du MS.458 de la Wellcome Collection porte la rubrique *DE Camomilla*. Il s’agit du canevas 32. Au quatrième vers après la rubrique, le premier signe dessine une capitale E. On distingue `rba` immédiatement après, sans initiale h visible. Le deuxième mot présente un t, un e, deux r et une finale a. Le troisième groupe donne `similis`, avec une hampe de l et une finale s distinctes. Ces trois mots ne montrent aucune marque supérieure évidente appelant un développement. La dernière lettre du mot `herba` à la ligne précédente est bien dans le cadre. [Canevas entier de Wellcome](https://iiif.wellcomecollection.org/image/b19209113_ms_458_0032.JP2/full/1400,/0/default.jpg)

| Témoin | Vers 551 ou son correspondant | Vers 552 ou son correspondant |
|---|---|---|
| Édition de calcul | *dicimus; haec multum redolens est et brevis herba,* | *herbae tam similis, quam justo nomine vulgus* |
| Copie de 1478, lecture des traits | *Dicim[us]. hec multū redolens ē ⁊ breuis herba* | *Erba terra similis qu[…] iusto no[…]e uulgus* |

Les crochets de la seconde ligne du tableau signalent un développement de finale ou un groupe abrégé. Le tilde horizontal est rendu ici par un macron. Au vers 551, le copiste abrège *multum* et *est* et emploie un signe pour *et*. Au vers suivant, les lectures de détail des mots après *similis* sont moins sûres. Le segment *Erba terra similis* se détache sur une zone d’encre suffisamment lisible. La transcription conserve *terra* même si la leçon est inhabituelle. La capitalisation, les formes de s et les graphies u/v ne reçoivent aucune valeur phonétique dans ce contrôle. [Extrait institutionnel précis](https://iiif.wellcomecollection.org/image/b19209113_ms_458_0032.JP2/890,840,2510,1170/1650,/0/default.jpg) · [Texte des vers édités](../vers.tsv)

Les identifiants de contrôle sont donc `herba`, `erba`, `terra`, `similis` dans la copie, et `herba`, `herbae`, `tam`, `similis` dans l’édition. L’orthographe médiévale ne rétablit pas le mot prédit par la table d’origine. Un recalcul sur les nouvelles formes serait une expérience différente dont les résultats doivent rester attribués au témoin choisi.

## Provenance

La notice du catalogue place le chapitre 14 du *Macer* après celui du poireau. Les canevas 30 à 34 ont été ouverts pour repérer la séquence. On voit le poireau en 30 et 31, la rubrique de la camomille en 32, puis la fin de cette notice et le début de la suivante en 33. La prédiction avait été communiquée à la personne qui a lu l’image. Ce sondage procède donc d’une lecture dirigée, avec une orthographe cible déjà connue. [Ordre des chapitres et datation du MS.458](https://wellcomecollection.org/works/cfqd658f)

Crédit photographique Wellcome Collection, Public Domain Mark. Le fichier JPEG a été renvoyé directement par le service IIIF, pour la région native `890,840,2510,1170`, mise à 1 650 pixels de large. SHA-256 `7b590f5414d949c8101642b56b7bc0699432305e4a4bca0687c3d1815ef26656`.

Un second lecteur IA a examiné uniquement le cliché, sans connaître le résultat ni consulter l’édition. Il a lu la fin du troisième vers `redolens ē ⁊ breuis herba` et le début du quatrième `Erba terra similis quē`. Les deux lectures s’accordent sur les quatre formes utilisées dans le nouveau calcul. Le développement des abréviations plus loin dans le vers n’intervient pas dans l’essai.

Nous avons ensuite remplacé les trois entrées de l’édition par les mots réellement tracés dans cette copie et recalculé les prédictions. Une impossibilité indépendante du découpage des deux premiers mots est déjà visible. Pour transformer le groupe `shody` en `sholdy`, on ajoute un seul signe à l’intérieur. Dans une table de valeurs fixes, cela insère des lettres en conservant celles de la première lecture, ou conserve le mot si le signe est muet. L’opération ne transforme pas *terra* en *similis*. Elle ne transforme pas non plus *tam* en *similis*. [Résultats pour les 48 règles en ordre historique direct](NOUVEAU-CALCUL.json) · [Calcul](../../manuscrit_1478.py)
