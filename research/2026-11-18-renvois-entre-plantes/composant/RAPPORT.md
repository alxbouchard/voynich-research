# Une prédiction de mot à partir de deux racines dessinées

**Le groupe annoncé, `dar`, revient trois fois dans la prose de la deuxième grande plante.** Sur f102r2, le fragment 212 porte la légende `koldarod`, et son voisin 213 la légende `odalydary`. Le catalogue rapproche le premier de la grande plante f18v et le second de f23r. Sur f18v.7, le groupe intérieur commun aux deux légendes s’écrit seul, deux places après `daiin`. La prédiction déposée était de retrouver `dar` sur f23r et, plus précisément, dans les trois mots suivant un `daiin`. Cette page avait déjà servi à d’autres études. [Prédiction déposée](AVANT.md) · [Le bifeuillet et les deux formes de racines](BIFEUILLET.md)

| Lieu prédit sur f23r | Ce que porte la page |
|---|---|
| Mot entier dans la prose | Trois emplois distincts, aux lignes 6, 7 et 10, dans 79 positions concordantes. |
| Un des trois mots après `daiin` | Aucune touche. Sur six départs, quatre ont au moins un voisin lisible dans l’alignement conjoint, aucun n’en a trois. Chaque édition prise séparément présente deux fenêtres complètes et aucune occurrence de `dar` dans les fenêtres complètes ou partielles. |

À la ligne 6, `dar` se lit entre `yky` et `okol`. À la ligne 7, il est entre deux `qokchol`. La ligne 10 contourne deux fleurs bleues. À droite de la seconde, on lit `dar ykain`. Parmi 28 autres grandes faces qui ont un lien direct dans le catalogue, neuf présentent le mot, dont six sur les quinze de longueur comparable. Une de ces quinze grandes faces, f1v, le présente également trois fois. La fréquence n’avait pas été prédite. La projection sur f23r réussit à l’échelle de la page ; la page seule ne détermine pas le sens de `dar`. [Les trois agrandissements de Yale](photos/dar-f23r.jpg) · [Résultats par page et par édition](RESULTATS.json)

Hors des feuillets 102, 18 et 23, on compte 22 autres renvois directs à vérifier. Huit seulement présentent une légende entière d’un mot aux quatre lectures concordantes, compte tenu des attachements du registre. Aucune n’a `dar` à l’intérieur avec une unité au moins de part et d’autre. Ce contrôle manque donc d’une troisième étiquette qui permettrait de décider si le composant prédit une autre grande plante. [Script](verifier.py) · [Registre des attaches](../../2026-11-18-noms-dans-les-notices/registre/registre.csv)

## Deux textes disposés de la même façon

La vérification de f23r a révélé un parallèle plus précis. Dans les deux grandes plantes, la séquence commence au **quatrième mot de la septième ligne de prose**.

| Grande plante | Mot 4 | Mot 5 | Mot 6 | Mot 7 |
|---|---|---|---|---|
| f18v.7, fragment associé 212 | qokol | daiin | qokol | dar |
| f23r.7, fragment associé 213 | qokchol | dar | qokchol | dairo |

[Les deux lignes et les quatre dessins sur une seule planche](photos/deux-phrases.jpg)

On passe d’un mot extérieur à l’autre en insérant l’unité EVA `ch`. Les deux pages appartiennent au même côté d’une feuille pliée. Les dessins connus permettent de les apparier sans connaître la prose. En revanche, le rang 4, la ligne 7 et l’encadrement du mot du milieu ont été **remarqués après** l’ouverture de f23r. Ils peuvent suggérer une formule ou un modèle de copie. Le moment où le scribe a écrit chaque ligne reste inconnu. [Ligne de f18v](../photos/qokol-oky.jpg) · [Ligne de f23r](photos/dar-f23r.jpg)

**Épreuve sur d’autres faces.** Au sein des huit premiers cahiers, hors du bifeuillet de départ, 82 grandes faces ont une septième ligne comportant au moins un triplet vérifiable. Sur 241 triplets, deux présentent des mots extérieurs identiques autour d’un mot différent, `chy s chy` (f15v.7) et `aiin or aiin` (f33r.7). Parmi les 29 côtés de bifeuillet dont les deux septièmes lignes se prêtent à la comparaison, aucun ne répète la construction sur les deux faces. En étendant l’exploration à toutes les lignes et en exigeant le même rang de départ dans les quatre lectures, un seul des 52 côtés examinés offre une répétition de part et d’autre. Les mots extérieurs y diffèrent de plus qu’une insertion ou ne satisfont pas à la condition sur les milieux. Les témoins de même cahier et d’orientation correspondante, sur d’autres bifeuillets, donnent zéro correspondance complète sur 138 comparaisons, dont huit avec répétitions sur les deux faces. Cette rareté limite la force du contrôle. [Critères](ENCADREMENTS-AVANT.md) · [Septièmes lignes](ENCADREMENTS.json) · [Toutes les lignes, exploratoire](AUTRES-LIGNES.json)

Sur tout le manuscrit, hors de f18 et f23, une autre ligne commence par `qokchol dar`. Sur f14r.5, le mot suivant se lit `dala` ou `dalo` selon l’édition. Malgré l’incertitude sur son dernier signe, les deux excluent le mot répété attendu. La photo montre le début à deux boucles. [Vérification sur f14r.5](photos/F14R.md) Après un mot d’au moins quatre signes commençant par q et finissant par ol puis `dar`, aucune des deux suites entièrement concordantes ne redonne le mot de départ. Pour tous les mots extérieurs d’au moins quatre unités, 86 des 126 suites sont vérifiables. Une seule répète le mot, `checthy dar checthy` sur f84r.20, contre 0,2 attendue en redistribuant les voisins à l’intérieur de la même face et de la même catégorie de position. Seules cinq positions peuvent faire varier ce total. [Calcul des encadrements](encadrements.py) · [Comparaison des autres lignes](autres_lignes.py)

## Lecture historique

Dans le chapitre consacré à l’ache du *Gart der Gesundheit* (Ulm, 1487), le texte emploie `wurtz` pour la racine, puis le mot se retrouve à l’intérieur des composés qui désignent la racine d’ache et la racine de persil. La méthode récupère ces deux composés lorsque nous les chiffrons sous une clé cachée. Dans les écritures du Voynich, aucune des 26 paires de mots historiques proposées pour « racine » ne peut lire les deux légendes selon la table annoncée. Plus largement, 1 415 passages à mots extérieurs répétés dans sept corpus fournissent des ressemblances pour chacune des deux phrases prise séparément. Aucune table commune des familles testées ne lit les deux avec la même valeur pour chaque signe. [Les composés dans l’imprimé de 1487](lectures/ulm-1487-racines.jpg) [Épreuve des noms botaniques](lectures/RAPPORT.md) · [Épreuve des phrases parallèles](paralleles/RAPPORT.md)

Reproduction depuis ce dossier avec `python3 -B verifier.py`, puis `python3 -B encadrements.py` et `python3 -B autres_lignes.py`. Les identifiants désignent les groupes de signes dans les transcriptions IT2a-n et ZL3b-n. Le comptage des unités suit la segmentation EVA du projet.
