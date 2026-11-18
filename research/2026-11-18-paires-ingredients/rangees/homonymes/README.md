# Retrouve-t-on la forme du même dessin hors du feuillet 102 ?

**`opchy` ne fournit aucun deuxième fragment. Pour `otol`, le seul candidat végétal dépend du choix de transcription, et le contour de la plante contredit la prédiction de compacité.** La [prédiction](prediction.md) a été rédigée avant le dépouillement des autres feuillets. Elle exigeait trois caractères visuels pour chacun des deux mots. Elle partait du [dessin de f102v2](../f102v2-218-224.jpg).

| Mot | Légendes de fragments en H, hors f102 | En ZL, hors f102 | Conséquence visuelle |
|---|---:|---:|---|
| `opchy` | 0 | 0 | La touffe à feuilles étroites, divergentes et dentées de f102v2.13 reste sans réplique testable. |
| `otol` | 0 | 1, f101v.3 | La forme du dessin candidat est ramifiée et ouverte. Les pointes vertes seules concordent. |

Chaque édition fournit 164 loci réels `Lf` hors de l’intégralité du feuillet 102. Cela représente 163 inscriptions après réunion des deux lignes f99r.6+7 sur l’objet 72. La ligne signalée fictive `!Lf` en H sur f89v2 est écartée. Les comptes par classe ainsi que les deux lectures de chaque emplacement figurent dans les [dénominateurs](comptes.tsv) et les [occurrences](occurrences.tsv).

## L’unique candidat botanique

Sur la moitié gauche de f101v, le troisième dessin du premier rang porte le nº 175 dans l’inventaire Petersen. Il présente une tige et des ramifications largement espacées, terminées par sept cônes verts à pointe isolée. La racine inférieure forme une arche avec deux extrémités orangées. Le dessin du nº 218 est un seul limbe compact dont le bord se prolonge en plusieurs pointes. Appliqué à l’objet entier, le critère de compacité échoue en f101v. Le vert et les pointes se retrouvent. L’inscription f101v.3 est en haut à droite du nº 175, entre ce motif et le quatrième, sans trait d’attache. Cette géométrie rend l’attribution éditoriale au troisième moins certaine qu’une inscription interne. [Recadrage de f101v.3 et du nº 175](f101v-3.jpg) · [Pixels natifs Yale](https://collections.library.yale.edu/iiif/2/1006250/1200,55,770,790/full/0/default.jpg) · [Inventaire du cahier 19](https://www.voynich.nu/q19/index.html#f101v).

En f102v2.7, H lit `otol` et ZL `okol`. En f101v.3, H lit `otal` et ZL `otol`. **Aucune des deux éditions modernes ne donne `otol` aux deux emplacements.** L’ancienne interlinéaire de Stolfi reproduit toutefois à l’emplacement de f101v.3 une ligne attribuée à H qui porte `otol`, aux côtés des lectures `otal` de Grove et de Stolfi. La version de transcription est donc déterminante. Le recadrage provient du JPEG entier Yale 1006250, SHA-256 `1122f1b13afdf1509402334816f95e5e9baa2b6c94aa9e347b04aa2e4e54f36b`, région x=1200, y=55, largeur=770, hauteur=790. [Ancienne unité f101v2.R1, légende 3](https://www.ic.unicamp.br/~stolfi/EXPORT/voynich/00-06-07-word-grammar/Notes/015/L16%2BH-eva/UNITS/f101v2.R1).

## Les autres classes de légendes

H comporte 678 autres loci `L` hors f102 et ZL en comporte 822. Le dépouillement couvre `L0`, `La`, `Lc`, `Ln`, `Lp`, `Ls`, `Lt`, `Lx` et `Lz`. `opchy` ne remplit aucun de ces loci dans les deux éditions. Pour `otol`, deux légendes indépendantes sont entières dans les deux éditions et un locus supplémentaire en ZL relève d’une unité plus incertaine.

| Locus | Lecture H / ZL | Emplacement et portée |
|---|---|---|
| f68r1.25, `Ls` | `otol` / `otol` | Étoile près du bord droit du cercle, vers 3 heures, unité historique f68r1.S.21. [Photo Yale](https://collections.library.yale.edu/catalog/2002046?child_oid=1006196) · [Relevé de Stolfi](https://www.ic.unicamp.br/~stolfi/EXPORT/voynich/00-06-07-word-grammar/Notes/015/L16%2BH-eva/UNITS/f68r1.S). |
| f77r.5, `Lt` | `otol` / `otol` | Entre les troisième et quatrième branches du tube en haut de la page. [Photo Yale](https://collections.library.yale.edu/catalog/2002046?child_oid=1006212) · [Relevé de Stolfi](https://www.ic.unicamp.br/~stolfi/EXPORT/voynich/00-06-07-word-grammar/Notes/015/L16%2BH-eva/UNITS/f77r.X). |
| fRos.149, `L0` | absent / `otol` | Premier locus marqué `II` du groupe fRos.149–151 sur le dépliant des rosettes. Seul le premier locus égale le mot. Le référent et l’autonomie physique de cette ligne comme inscription distincte restent indéterminés. [Photo Yale](https://collections.library.yale.edu/catalog/2002046?child_oid=1006231). |

Le [script de décompte](compter.py) vérifie les empreintes des sources locales. Il ignore les commentaires d’édition et les accolades de ligature. Les autres signes, espaces de mots, lectures alternatives et marques d’incertitude restent discriminants. La recherche porte uniquement sur les loci `L` réels. Les occurrences dans le corps des paragraphes n’interviennent pas. Relancer `python3 compter.py` depuis ce répertoire régénère les deux TSV. [Source H, IT2a-n](https://www.voynich.nu/data/IT2a-n.txt) · [Source ZL3b-n](https://www.voynich.nu/data/ZL3b-n.txt).
