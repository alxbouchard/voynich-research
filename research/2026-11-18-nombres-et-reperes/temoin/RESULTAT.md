# Un calendrier anglais permet de prédire les chiffres de février

La copie du *Kalendarium* de John Somer conservée à Columbia présente janvier au f. 2r et février au f. 2v. La bibliothèque situe la copie du calendrier vers 1417, d’après une date au f. 1v. Les tables d’éclipses vont jusqu’en 1433. Les colonnes sont identifiées par l’exposition de Columbia. [Notice du manuscrit](https://archive.org/details/PlimptonMS254_20) · [Description des colonnes](https://liturgical.columbia.edu/exhibits/complete/) · [Janvier](https://liturgical.columbia.edu/liturgical/plimpton254_jan/) · [Février](https://liturgical.columbia.edu/liturgical/plimpton254_feb/)

**Pour refaire le test**, ouvrir la [planche masquée](exercice.png). En janvier, la colonne rouge immédiatement à gauche des lettres a–g donne les nombres d’or. Du haut vers le bas, les six premières inscriptions se lisent 3, 11, 19, 8, 16, 5. Ajouter 8 en ramenant le résultat entre 1 et 19 reproduit cette suite. En remontant, le pas vaut 11. Le 31 janvier porte de nouveau 3 et la lettre c. La colonne rouge à droite des lettres compte aussi les jours jusqu’aux calendes, aux nones et aux ides. À partir du 14 février, compter jusqu’au 1er mars en incluant les deux dates.

Les quatre prévisions de la [fiche figée](prediction.json) ont été consignées avant téléchargement de février. SHA-256 `6d0745c11865a04f2e4c33add3edf25758da93acaa97cfe0cf80d5361fbee995`. Un seul lecteur logiciel a relevé les valeurs. Les cases des quatre lignes se recoupent et appartiennent à un seul calendrier.

| Cible sur février | Prédiction | Lecture de l’image | Accord |
|---|---|---|---:|
| Six premières cases remplies des nombres d’or | 11, 19, 8, 16, 5, 13 | 11, 19, 8, 16, 5, 13, aux jours 2, 3, 4, 6, 7, 9 | 6/6 |
| Nombres d’or aux jours 1–12, en reportant les jours 2–13 de janvier | ∅, 11, ∅, 19, 8, ∅, 16, 5, ∅, 13, 2, ∅ | ∅, 11, 19, 8, ∅, 16, 5, ∅, 13, 2, ∅, 10 | **2/12** |
| Lettres des jours 1–12 | d e f g a b c d e f g a | d e f g a b c d e f g a | 12/12 |
| Compte inclusif vers les calendes de mars, jours 14–21 | 16, 15, 14, 13, 12, 11, 10, 9 | 16, 15, 14, 13, 12, 11, 10, 9 | 8/8 |

La place du **19** distingue les hypothèses. Il suit bien le 11, mais tombe le 3 février. Le report mécanique entre mois le plaçait le 4. Son dernier trait descend sous la boucle, à la différence du zéro de « 10 » le 12. La forme du 4 se vérifie aussi au sein de « 14 », dans l’autre registre. [Planche dévoilée](verification.png)

**Images.** Columbia University, Rare Book and Manuscript Library, Plimpton MS 254, ff. 2r–2v. Recadrages des JPEG de 2 048 × 3 072 pixels de Digital Scriptorium, légèrement agrandis. Les rectangles opaques sont ajoutés sur la version d’exercice. Archive `columbia-html.zip`, dossier `columbia/PlimptonMS254_20/`, fichiers `bk0009m8c78.jpg` et `bk0009m8d1g.jpg`. [Archive et licence CC BY 4.0](https://doi.org/10.5281/zenodo.6856582)
