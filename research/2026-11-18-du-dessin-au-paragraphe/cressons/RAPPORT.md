# Les deux cressons de Passau donnent-ils une lecture du Voynich ?

Une paire voisine du Voynich, `arol otoky` à la fin du premier rang de f99v, peut être ajustée aux deux qualificatifs latins *ortulanum* et *aquaticum*. **Aucune des quatre tables compatibles ne permet de lire un nouveau mot parmi les cibles historiques annoncées.** Dans la prose du panneau, même les deux formes ajustées ne réapparaissent pas. Lorsqu’on mélange les étiquettes à l’intérieur de leur panneau, 44,5 % des tirages produisent au moins une paire compatible avec ces qualificatifs. [Tables et attentes publiées avant ouverture de la prose](https://github.com/alxbouchard/voynich-research/blob/07ff7f2/research/2026-11-18-du-dessin-au-paragraphe/cressons/PREDICTIONS.json.gz) · [Transfert dans la prose](TRANSFERT.json.gz) · [Contrôle des mélanges](CONTROLE.json)

## Ce que les pages de Passau autorisent à chercher

Dans l’herbier de 1485, les deux rubriques latines commencent par le même mot, *Nasturcium*. Le mot suivant change, *ortulanum* (« des jardins ») ou *aquaticum* (« aquatique »). L’allemand donne deux composés, *gartenkresz* et *brunkresz*, avec la partie commune *kresz* à la fin. Les premiers mots du texte latin sont *Nasturcium domesticum et agreste* pour la première notice et *Nasturcium aquaticum* pour la seconde. Nous avons essayé les deux titres latins en entier, les qualificatifs latins seuls et les deux noms allemands entiers. La table de substitution doit rester la même pour les deux étiquettes. Chaque signe EVA peut donner une, deux ou trois lettres consécutives. [Transcription des formes historiques](../temoin/CRESSONS.tsv) · [Détails du témoin de Passau](../temoin/RAPPORT.md) · [Règles de sélection](PROTOCOLE.md)

Le registre photographique couvre 9 panneaux, 17 rangées et 72 inscriptions de fragments. Dans 49 cas, les deux transcriptions H et ZL et leurs deux traitements des blancs incertains donnent les mêmes mots entiers et les mêmes frontières. Il reste 45 légendes à un mot, 3 à deux mots et 1 à trois mots. Sur les 55 paires de places voisines, les deux légendes sont recevables dans 28 cas. Dans 22 de ces paires chacune contient un seul mot. Les six autres associent un mot d’un côté et deux de l’autre. Aucun voisinage ne comporte deux étiquettes de deux mots chacune. Les objets écartés restent à leur place dans le registre, sans rapprocher artificiellement leurs voisins. [Registre avec les quatre lectures](REGISTRE.json.gz) · [Attribution des légendes et limites de la géométrie](../../2026-11-18-paires-ingredients/rangees/README.md)

| Modèle | Paires voisines ayant la structure demandée | Paires compatibles jardins puis aquatique | Paires compatibles dans l’ordre inverse |
|---|---:|---:|---:|
| Deux titres latins de deux mots, premier groupe identique | 0 | 0 | 0 |
| Deux qualificatifs latins seuls | 22 | 1, avec 4 tables | 0 |
| Deux noms allemands | 22 | 0 | 0 |

Aucune paire ne subsiste si l’on plafonne le développement à **deux lettres par signe**. Les quatre tables du seul voisinage admissible sont toutes injectives sur les sept signes rencontrés. Un même signe redonne toujours la même suite et, dans ces quatre tables, deux signes différents ont également des suites différentes. Cela autorise quatre partitions des mêmes mots historiques. [Calcul exhaustif](ajuster.py) · [Tables et origines](PREDICTIONS.json.gz)

## Le voisinage de f99v et ses quatre lectures ajustées

Les deux inscriptions sont les septième et huitième étiquettes de fragments du rang supérieur, à droite du premier récipient rayé. Elles suivent l’étiquette `olsy`. Le fac-similé montre à cet endroit plusieurs formes peintes. L’une est brune et s’ouvre en deux longues branches, la dernière à droite est pâle, striée de rouge. Le paragraphe situé sous ce rang occupe les loci f99v.10–13. Le registre attribue l’ordre des inscriptions. Aucun nom d’espèce indépendant n’a été donné à ces dessins. [Détail photographique de Yale, Beinecke MS 408](f99v-legendes.jpg) · [Page entière](https://collections.library.yale.edu/iiif/2/1006247/full/1050,/0/default.jpg)

Les quatre tables se lisent facilement dans cet exemple. Pour décomposer *ortulanum*, `a·r·o·l` donne soit *or·tul·a·num*, soit *ort·ul·a·num*. Pour *aquaticum*, `o·t·o·k·y` donne soit *a·qu·a·ti·cum*, soit *a·qu·a·tic·um*. Les deux décisions peuvent se combiner indépendamment. Dans les quatre cas, `l` reçoit *num*, ce qui impose trois lettres à un seul signe. [Les quatre partitions complètes](PREDICTIONS.json.gz)

Dans le sens inverse, des lettres latines vers les signes EVA, chaque table ne produit qu’**une** graphie pour *ortulanum* (`arol`) et pour *aquaticum* (`otoky`). Elle n’en produit **aucune** pour *nasturcium*, *domesticum*, *et* ou *agreste*. La suite *nasturcium aquaticum* ne peut donc même pas être prédite au moyen de cette table. Pour *kresz*, aucune table allemande issue d’une paire voisine n’atteint l’étape de prédiction. L’absence de forme générable est une abstention du modèle avant d’ouvrir la prose. [Attentes publiées avant lecture](https://github.com/alxbouchard/voynich-research/blob/07ff7f2/research/2026-11-18-du-dessin-au-paragraphe/cressons/PREDICTIONS.json.gz)

| Prose ordinaire P0 | Lignes communes H/ZL | Positions lisibles au même rang sous quatre traitements | Reprises de `arol` | Reprises de `otoky` |
|---|---:|---:|---:|---:|
| Panneau source f99v | 19 | 80 | 0 | 0 |
| Autre face du même feuillet, f99r | 18 | 101 | 0 | 0 |
| Hors du feuillet 99 | 3 847 | 20 134 | 3 | 0 |

Les trois reprises certaines de `arol` sont f40v.18 au rang 6, f106r.16 au rang 5 et f113v.45 au rang 2. Même graphie signifie ici seulement que le groupe déjà ajusté existe ailleurs. Les lectures individuelles, sur les loci communs, retrouvent dix `arol` hors du feuillet en H, six en ZL avec les blancs joints et sept avec les blancs séparés. Aucune ne retrouve `otoky` dans les lignes de prose examinées. Le complément aux autres catégories de paragraphes, P1, Pb, Pc, Pr et Pt, ajoute 669 positions concordantes sans reprise. Ces dénominateurs mesurent ce que les transcriptions permettent de contrôler et peuvent omettre des mots à rang incertain. [Toutes les positions et leurs éditions](TRANSFERT.json.gz) · [Vérification après publication](transferer.py)

## Compatibilités accidentelles et contrôle sur le texte connu

Lorsque le modèle allemand ne trouvait aucun voisinage, la sensibilité prévue a autorisé deux légendes non voisines. Parmi 968 paires admissibles à un mot de chaque côté, 20 sont compatibles dans l’ordre du registre et 22 dans l’autre sens. Seize paires figurent dans les deux listes, soit 26 paires distinctes. Deux seulement des 26 appartiennent au même panneau. L’orientation des paires prises sur des panneaux différents est celle du registre utilisé. Ces associations exploratoires n’ont pas servi à prédire la prose. Dans le modèle latin à deux mots, même les trois légendes de deux mots non voisines ont trois premiers groupes différents. [Paires exploratoires et exemples de tables](PREDICTIONS.json.gz)

Un second contrôle a été ajouté **après** le transfert. Il garde à leur place toutes les cases qui portent une étiquette simple et lisible et échange les étiquettes entre ces cases à l’intérieur de chaque panneau. Le nombre attendu de paires latines compatibles est **178/315, soit 0,565**, contre une paire observée. Sur 25 000 tirages à graine fixée, 11 131 en donnent au moins une. C’est une mesure de la facilité d’obtenir cet ajustement dans ce petit ensemble en ignorant l’ordre réel. Elle ne donne pas la probabilité que f99v représente du cresson. [Contrôle reproductible](controle.py) · [Comptes exacts et tirages](CONTROLE.json)

Le contrôle positif a chiffré les véritables rubriques de Passau par une substitution aléatoire d’une lettre par signe opaque. Le lecteur de test reçoit les rubriques chiffrées et les mots supposés en clair. La clé du générateur lui est cachée. Il en retrouve une seule pour les signes présents. Avec les deux titres latins complets, il retrouve la suite *nasturcium aquaticum* déjà fournie par l’ajustement et sait, en plus, former *in*, mot réellement employé dans la première phrase du cresson aquatique. Il lui manque *d* et *e* pour *domesticum*, *e* pour *et*, *e* et *g* pour *agreste*. Avec les seuls qualificatifs, le *s* de *nasturcium* manque aussi. Les deux composés allemands fournissent toutes les lettres nécessaires pour prédire *kresz* dans l’exercice chiffré. L’herbier donne cette base à l’intérieur de composés. Pour chaque cible formable du contrôle, remplacer le dernier signe après prédiction par **un autre signe déjà connu** donne un mot différent. [Épreuves et lettres manquantes](CALIBRATION.json) · [Programme sans accès à la clé lors de l’ajustement](calibrer.py)

Depuis ce répertoire, les quatre programmes Python utilisent la bibliothèque standard et les lecteurs EVA déjà présents dans le dépôt. L’ajustement ne consulte que les légendes. Le transfert vérifie l’empreinte SHA-256 du fichier publié avant de chercher les mots en prose.

```sh
python3 -B ajuster.py
python3 -B calibrer.py
python3 -B transferer.py
python3 -B controle.py
```
