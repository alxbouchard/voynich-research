# Les rapprochements botaniques publiés dans les cahiers 15 et 19

Les notices de René Zandbergen signalent **35 liens entre 34 petits fragments et 34 grandes faces de plante**. Deux petits dessins, 94 et 116, sont rapprochés de la grande plante de f96v. Inversement, le fragment 150 est rapproché de deux grandes plantes, f30v et f55v. Le catalogue indique où comparer les dessins ; il ne certifie ni une espèce ni le référent de l’écriture. L’extraction des propositions porte sur les descriptions, avant le calcul des mots de cette étude. Les documents et leurs graphies avaient déjà servi à des recherches antérieures. [Catalogue Q15](https://www.voynich.nu/q15/index.html) · [Catalogue Q19](https://www.voynich.nu/q19/index.html) · [Registre détaillé, rang dans le dessin et liens directs](RENVOIS.json)

| Formulation de la notice | Q15 | Q19 | Total |
|---|---:|---:|---:|
| Le dessin paraît représenter la même plante | 2 | 7 | 9 |
| Ressemblance proposée dans la description du fragment | 8 | 14 | 22 |
| Proposition supplémentaire de Th. Petersen dans les notes | 4 | 0 | 4 |

Les **31 liens principaux** comportent tous une mention explicite du numéro du fragment dans la notice de la grande plante. Les quatre notes distinctes attribuées à Petersen n’y trouvent aucune reprise explicite du numéro. Les formulations réciproques proviennent du même catalogue ; elles vérifient les identifiants, sans procurer de seconde expertise botanique. La note sur le 31 est déjà comptée dans les liens principaux. [Audit des 34 grandes faces et empreintes des notices](VERIFICATION.json)

## Registre par panneau

Chaque entrée indique le numéro du fragment puis sa grande face. L’astérisque désigne une proposition supplémentaire de Petersen. Le signe † désigne les neuf cas où le catalogue suggère expressément qu’il pourrait s’agir de la même plante.

| Panneau à fragments | Grandes faces proposées |
|---|---|
| f88r | 8* → f15v, 11 → f90r2 |
| f88v | 22 → f94v |
| f89r1 | 25 → f57r, 26* → f43v, 28 → f30r, 31 → f33r |
| f89r2 | 35 → f35v, 40* → f87v |
| f89v2 | 50 → f10v, 52* → f40v, 54† → f48v, 56 → f24r, 61† → f48r |
| f89v1 | Aucun renvoi à une grande plante |
| f99r | 80 → f51r, 94 → f96v |
| f99v | 95 → f44r, 110 → f34v |
| f100r | 116 → f96v |
| f100v | 133 → f13v, 136 → f90v2 |
| f101r | 150 → f30v et f55v, 155 → f49r, 168 → f4v |
| f101v | 188 → f37r |
| f102r1 | 203† → f37v, 204† → f1v |
| f102r2 | 205† → f47v, 206† → f32v, 209 → f53r, 212† → f18v, 213† → f23r |
| f102v2 | 225 → f36r |
| f102v1 | 240† → f19r |

## Identifiants et limites

- Le fragment 31 est physiquement sur f89r1. La note sous f89r2 renvoie au même numéro et à la même grande face f33r, avec un lien HTML tronqué. Pour le 52, le chemin HTML est défectueux mais le libellé désigne f40v. Les chemins canoniques ont été vérifiés. Les numéros 39 et 228 ont été sautés dans la numérotation ancienne. Le 59 existe bien, mais l’ancienne seconde ligne de sa légende est donnée comme de l’encre visible par transparence. [f89r2](https://www.voynich.nu/q15/index.html#f89r2) · [f89v2](https://www.voynich.nu/q15/index.html#f89v2) · [f102v2](https://www.voynich.nu/q19/index.html#f102v2)
- Les grandes faces f43v et f87v montrent chacune deux plantes différentes. Les liens vers les fragments 26 et 40 ne précisent pas laquelle. La face f40v présente aussi deux plantes décrites comme semblables, avec une différence marquée de fleur. Sur f48v, deux exemplaires se croisent à la racine. En f23r, deux parties aériennes partagent une racine et une branche. Un test sur la prose d’une face ne peut pas désigner à lui seul le dessin précis dont parle un mot. [Deux plantes de f43v](https://www.voynich.nu/q06/index.html#f43v) · [Deux plantes de f87v](https://www.voynich.nu/q15/index.html#f87v) · [Deux plantes de f40v](https://www.voynich.nu/q05/index.html#f40v)
- f101r et f101v sont deux faces du même dépliant. La prose traverse le pli. On compte dix lignes ordinaires P0 au recto et neuf au verso dans les deux éditions. La dixième ligne du verso est centrée. Les 16 faces à fragments et les 34 grandes faces de l’inventaire comportent toutes de la prose P0. Au recto 101, les dessins n’ont aucune légende de fragment dans le catalogue. Sur f89v1, il y a de la prose et six fragments mais aucun lien vers une grande face. [Dépliant f101r](https://www.voynich.nu/q19/index.html#f101r) · [Face f101v](https://www.voynich.nu/q19/index.html#f101v) · [Cahier 15](https://www.voynich.nu/q15/index.html#f89v1)
- La proposition « chardon » pour le 30 ne donne aucune autre page à comparer. Les bulbes de f90r1 renvoient à ceux de f3v, deux grandes faces. Les 212 et 213 sont voisins dans leur rangée et les deux grandes faces associées occupent le même côté d’un bifeuillet ; la remarque redouble les deux liens déjà comptés. L’inventaire couvre les deux notices de cahier et les numéros des fragments qu’elles désignent. Il ne prétend pas recenser toutes les identifications botaniques de tous les chercheurs. [Proximité des deux fragments](https://www.voynich.nu/q19/index.html#f102r2) · [Bulbes de f90r1](https://www.voynich.nu/q15/index.html#f90r1)

Pour reproduire, télécharger les pages `index.html` des cahiers 15 et 19, puis lancer `python3 -B extraire.py q15.html q19.html`. Pour l’audit des liens de retour, télécharger au même format les cahiers 01 à 08, 15 et 17. Si les fichiers sont nommés `q1.html` à `q19.html` sans zéro initial, lancer `python3 -B verifier_notices.py 'q{q}.html'`. Le programme consulte uniquement les en-têtes des lignes de transcription pour compter les emplacements P0. [Extraction](extraire.py) · [Vérification](verifier_notices.py) · [Travail antérieur sur les légendes du cahier 19](../../../voynich_phase46/RAPPORT.md)

Pour les grandes faces rapprochées d’un fragment dont la notice signale des baies ou des groseilles, l’essai consacré à ce motif donne également les lectures des deux étiquettes de fragment, les dénominateurs de prose par édition et trois agrandissements Yale. [Essai sur les baies](baies/RAPPORT.md)
