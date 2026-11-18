# Quels mots accompagnent les Pléiades dessinées ?

Dans un manuscrit italien du XVe siècle, les sept têtes des Pléiades portent sept noms différents. Dans un manuscrit rhénan de la même époque, les sept femmes portent chacune une étoile rouge et l'explication est commune au groupe.

| Manuscrit et périmètre | Figures | Figures avec légende individuelle | Légendes individuelles contenant un nom commun pour « étoile » |
|---|---:|---:|---:|
| Göttweig, cod. 146 rouge / 190 noir, f. 18v, ensemble des Pléiades | 7 | 7 | 0 sur 7 |
| Morgan, M.384, f. 21r, cercle supérieur des Pléiades | 7 | 0 | Aucune légende individuelle à tester |

**Göttweig.** Sur le cliché, on lit *Merope* au sommet, *Alcione* en haut à gauche, *Celaeno* en haut à droite, *Electra* au centre, *Taygete* en bas à gauche, *Sterope* en bas à droite et *Maea* à la base. La casse est régularisée. Sous les visages, une inscription collective s'étend sur deux parties. La notice descriptive de Kristen Lippincott répète *Merope* dans son énumération. Sa planche photographique permet de lire *Sterope* en bas à droite. Le catalogue autrichien date la copie du XVe siècle. Lippincott la situe en Italie du Nord dans la seconde moitié du siècle. [Photographie, planche 10, en bas à gauche](https://www.thesaxlproject.com/assets/Uploads/00-PLeiades-16a-Nov-2025.pdf#page=10) · [Notice de Lippincott, pp. 1 et 5](https://www.thesaxlproject.com/assets/Uploads/Mss-descriptions-Cicero-Gottweig-7-29-Oct-2025.pdf#page=5) · [Catalogue autrichien](https://manuscripta.at/?ID=36858)

**Morgan.** Sur cette page de *Von dem Gang des Himels und Sternen*, quatre femmes occupent le rang supérieur et trois le rang inférieur. Chacune a une étoile rouge au-dessus de la tête. Le texte manuscrit se trouve à gauche et au-dessous du groupe. Le cercle inférieur, qui représente la Lyre, constitue une autre illustration. La bibliothèque attribue le manuscrit à la Rhénanie dans la seconde moitié du XVe siècle. [Photographie du folio](https://ica.themorgan.org/icaimages/3/m384.021r.jpg) · [Notice et identification des deux groupes](https://ica.themorgan.org/manuscript/page/23/77318)

**Un cas où « étoile » apparaît dans la légende.** Sur le troisième fuseau de la première feuille du globe de Johann Schöner, daté de [1517] par la Library of Congress, la pointe nord porte *Alrucaba stella polaris*. Plus bas, sur le même fuseau, on lit *Rigel* au pied d'Orion. Les deux désignations coexistent sur un même objet. Cet exemple a été recherché pour vérifier l'existence d'une légende avec *stella*. Il ne participe pas au décompte des manuscrits du XVe siècle. [Détail de l'étoile polaire](schoner-polaire.jpg) · [Détail d'Orion](schoner-orion.jpg) · [Original et droits, Library of Congress, Jay I. Kislak Collection](https://www.loc.gov/item/2016586439/)

## Refaire le relevé

Les deux témoins ont été cherchés pour leur illustration d'un même groupe céleste. Dans chacun, le dénominateur est fixé par la figure dessinée. Prendre tous les visages du groupe avant de lire les mots. Compter une légende individuelle quand une inscription autonome est placée auprès d'un seul visage. La prose qui entoure le cercle et l'inscription collective sous les sept têtes relèvent d'une autre unité de lecture. Les quatorze positions, y compris les cellules vides, sont consignées dans le [relevé](positions.tsv).

Pour recompter depuis ce répertoire avec un outil standard Unix, la première colonne de nombres donne les figures, la deuxième les légendes individuelles et la dernière celles qui contiennent le mot latin *stella*.

```sh
awk -F '\t' 'NR>1 {n[$1]++; if ($4!="") l[$1]++; if (tolower($4) ~ /(^| )stella( |$)/) s[$1]++} END {for (t in n) print t, n[t], l[t]+0, s[t]+0}' positions.tsv
```

La lecture directe des sept noms vérifie également le cas des synonymes et des formes fléchies. Les deux manuscrits constituent des exemples choisis pour leurs images. Pour examiner un autre manuscrit, il reste à déterminer ce que chaque inscription individualise, par exemple l'astre, la figure humaine ou le groupe entier.

Les deux détails du globe proviennent de l'image IIIF `ct007571` de 15 216 × 6 055 pixels. Le premier est la région `2550,500,680,1350`. Le second est la région `2300,2850,1000,1540`, ramenée à 840 pixels de large. Crédit des images reproduites ici : Library of Congress, Jay I. Kislak Collection. [Service IIIF de l'original](https://tile.loc.gov/image-services/iiif/service:gmd:gmd3:g3191:g3191b:ct007571/info.json)
