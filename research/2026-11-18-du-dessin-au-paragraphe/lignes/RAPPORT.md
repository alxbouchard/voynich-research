# Le scribe reprend-il le mot écrit juste au-dessus ?

Dans les deux lots de réserve, une prédiction faite à partir d’un mot de la ligne supérieure a retrouvé **17 mots entiers sur 1 238 cases lisibles** (1,37 %). Quand les mots d’une même ligne échangent leurs positions tout en gardant le même nombre de signes, on attend **15,02** correspondances. Parmi 4 999 simulations de ce contrôle, 1 128 donnent au moins 17 réussites (22,56 %). Ces résultats ne permettent pas d’attribuer les ressemblances à un scribe qui aurait délibérément copié le mot situé au-dessus. [Dépôt horodaté des annonces avant ouverture](https://github.com/alxbouchard/voynich-research/commit/b47dabb) · [Inventaire des résultats](RESULTATS.json)

| Lot | Faces | Paires de lignes | Annonces | Cible incertaine | Copies exactes / lisibles | Attendues, permutation libre | Attendues, même longueur |
|---|---:|---:|---:|---:|---:|---:|---:|
| Panneaux pharmaceutiques | 15 | 86 | 287 | 130 | 0 / 157 | 0,77 | 0,50 |
| Feuillets 1–16 | 30 | 147 | 342 | 126 | 5 / 216 | 3,16 | 5,40 |
| Feuillets 103–116 | 23 | 410 | 1 638 | 616 | 12 / 1 022 | 8,82 | 9,62 |

**Deux annonces consultables sur le manuscrit.** Sur f3v, la ligne 7 a fourni `chor` au troisième rang. Le programme a prédit `chor` au troisième rang de la ligne 8, où les quatre lectures s’accordent sur cette graphie. Sur f2r, le quatrième mot de la première ligne a fait annoncer `otchal` au deuxième rang de la deuxième ligne. Les transcriptions y donnent `chkar`. À f2r.2, le second mot annoncé, `ypchaiin` au rang 4, échoue également devant `shor`. [Photographie Yale du f3v](https://collections.library.yale.edu/iiif/2/1006081/full/1600,/0/default.jpg) · [Photographie Yale du f2r](https://collections.library.yale.edu/iiif/2/1006078/full/1600,/0/default.jpg) · [Toutes les annonces vérifiées](OUVERTURES.json.gz) · [Deux réussites et un échec voisin sur la photographie de f3v](f3v/NOTE.md)

**Une case à droite.** La case immédiatement à droite donnait parfois une lecture incertaine. Sur les 1 083 cibles des deux réserves dont les deux cases étaient lisibles, le mot annoncé convenait 16 fois dans l’axe et 5 fois à droite. Le détail est de 4 contre 1 sur les 192 cases des premiers feuillets, puis 12 contre 4 sur les 891 cases des derniers feuillets. Dans les panneaux pharmaceutiques, le témoin de droite réussit 2 fois et la position annoncée 0 fois sur 135 cases communes. Ce déplacement modifie également la largeur du mot rencontré.

**Fréquence et longueur.** Une permutation libre des mots entiers à l’intérieur de la ligne inférieure donne 11,98 réussites attendues dans les deux réserves, et 362 tirages sur 4 999 atteignent 17 (7,24 %). La permutation à nombre d’unités EVA égal porte l’attente à 15,02. La proportion des permutations de même longueur qui égalent ou dépassent le score observé vaut 78,30 % pour les premiers feuillets et 12,08 % pour les derniers. Parmi les 1 238 cases lisibles des réserves, 455 sont les seules de leur longueur sur leur ligne parmi les cases intérieures lisibles (98 et 357 respectivement). Sept des 17 correspondances y sont inévitables une fois la longueur et la ligne fixées. Dans les panneaux, 60 cases ont cette propriété, aucune ne réussit. Les tirages échangent ensemble les mots de chaque ligne et gardent les positions illisibles fixes.

**Ce qui a pu être vérifié.** Les paires sont formées dans des paragraphes P0 dont la délimitation est identique dans les deux éditions. Les rangs impairs fournissent les mots visibles et les rangs pairs les mots à ouvrir. Les 36 paragraphes entièrement cartographiés des panneaux, les 51 des premiers feuillets et les 259 des derniers ont été admis. Le fichier du prédicteur ne contient pour les lignes inférieures que les coordonnées et les identifiants de ligne. Le calage préalable des coordonnées utilise les graphies du visualiseur pour les mettre en correspondance avec la transcription H. La géométrie et la disponibilité des boîtes dépendent donc du manuscrit et du visualiseur. Parmi les 1 980 annonces sur les réserves, 742 restent incertaines. Le test porte sur les graphies entières de rang intérieur, avec un mot source d’au moins trois unités, et sur une seule correspondance géométrique entre deux lignes de prose. Une ressemblance de sens entre des mots de graphies différentes échappe à ce critère. [Protocole](PROTOCOLE.md) · [Sources et couverture par face](SOURCES.json)

## Reproduction

`masquer.py` réutilise le calage et le découpage des paragraphes du dossier voisin `passages`. Il lit les cartes du visualiseur, disponibles aux adresses de `SOURCES.json`, après sauvegarde sous `<face>.json`. Chaque panneau conserve la médiane des pentes des lignes. Le prédicteur projette leurs centres sur l’axe `x + pente × y`, élimine les égalités et ne reçoit que les mots de la ligne supérieure. Le vérificateur emploie NumPy (`2.4.6` ici), une graine de 991820 et 4 999 réplications par contrôle. Le registre des annonces a pour SHA-256 `dbb90dd73ee95aad7aa53a66893f8e49373f52968033b7193bf48f7a2eea1c28`. [Carte masquée](CARTE-MASQUEE.json.gz) · [Annonces](PREDICTIONS.json.gz) · [Vérification](verifier.py)

```sh
python3 -B masquer.py /tmp/voy-panneaux-paragraphes
python3 -B annoncer.py
python3 -B verifier.py
```
