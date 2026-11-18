# L’expression latine *sub* suivie du nom d’un astre

**Quelle part d’un nom peut-on lire sur un passage tenu en réserve ?** Sur les sept vraies notices latines de Bâle, nous avons remplacé chaque lettre par un identifiant opaque selon une permutation commune. Le programme d’apprentissage a reçu les quatre premières fenêtres masquées de seize mots, les quatre ablatifs correspondants et la préposition *sub*. Il a dû localiser lui-même les deux mots voisins. Les normalisations u/v et i/j avaient été fixées dans l’étude précédente. [Témoin photographique et transcription](../temoin/README.md) · [Protocole](../PROTOCOLE.md)

Une seule table partielle satisfait les quatre premières notices. Puis le programme reçoit les trois dernières fenêtres masquées et cette table figée. Il trouve chaque fois *sub* à la quatrième place. Pour Vénus il lit `uenere` (6/6), pour Mercure `mer?urio` (7/8) et pour la Lune `luna` (4/4). La lettre c de Mercure manquait aux quatre expressions d’apprentissage. Le résultat est de **deux noms complets sur trois et 17 lettres sur 18**. Les formes de référence des trois dernières notices interviennent au moment de noter les sorties. Ce test vérifie la récupération en écriture masquée sur un texte dont la formule est réelle. [Données d’étalonnage](etalonnage.json)

Sur f67r2, nous avons retenu les sept paragraphes des secteurs 1, 3, 5, 6, 7, 8 et 11. Les domiciles fournissent deux distributions qui échangent le Soleil et la Lune. Le premier calcul ci-dessous place la Lune en 7 et le Soleil en 8. Les nombres sont identiques dans la distribution inverse. Chaque combinaison peut choisir ses groupes n’importe où dans les paragraphes entiers, y compris sur deux lignes consécutives. Un seul groupe contient toute l’expression dans la version soudée. Deux groupes immédiatement contigus sont requis dans la version séparée. Les tables opérant sur un à trois éléments autorisent des sorties identiques pour des entrées différentes. Dans la version soudée, un groupe de lettres correspondant à un signe peut chevaucher la limite latine après *sub*. [Paragraphes et lieux](../../2026-11-18-secteurs-rouges/photos/secteurs.csv) · [Deux distributions préexistantes](../../2026-11-18-sept-astres/domiciles.json)

| Table commune | Deux groupes | Un groupe soudé |
|---|---:|---:|
| Un signe, une lettre distincte | 0/7 | 0/7 |
| Un signe rend 1 à 3 lettres | 1/7 | 3/7 |
| Une lettre rend 1 à 3 signes | 1/7 | 0/7 |

Ce tableau utilise les unités EVA composées dans les deux éditions, H et ZL. En ASCII, la dernière case atteint 1/7. La séparation des espaces douteux et l’exclusion des groupes ZL comportant une alternative donnent les mêmes maxima de correspondances observées. Dans la variante ZL qui exclut un groupe douteux du secteur 8, on peut accorder à cette lacune un secteur supplémentaire comme borne supérieure absolue. [Résultats par modèle et variante](manuscrit.json)

Avec la lecture H et des groupes distincts, une table à développement variable peut faire lire `am.or` au 21e locus, groupes 2–3, comme *sub Iove*. Six tables partielles permettent cette lecture du secteur 3. Le dernier groupe se lit `ar` dans ZL et l’ajustement disparaît. En ZL, le meilleur lieu pour ce même modèle séparé est le secteur 1. La bijection lettre à lettre ne permet de lire aucune des sept expressions proposées dans chacune des deux éditions. [Ajustements détaillés et clés](manuscrit.json)

En soudant les mots et en faisant rendre une à trois lettres par signe, trois paragraphes de H admettent par exemple `sochy` (.14, mot 1) comme *sub Saturno*, `saral` (.20, mot 2) comme *sub Iove*, et `dakan` (.33, mot 1) comme *sub Luna*. La table partielle donne notamment **s** et **d** comme deux façons d’écrire la lettre s, **o** comme *ubs* et **ch** comme *atu*. Pour la distribution avec la Lune en 7, six triplets distincts atteignent ce maximum dans H, avec respectivement 3, 29, 7, 1, 99 et 48 tables partielles. Le secteur 6, celui de Mercure, ne permet même pas de satisfaire l’expression isolément dans ce calcul EVA. [Détail par triplet](manuscrit.json)

Nous avons ensuite attribué les sept mêmes ablatifs aux sept paragraphes selon les 5 040 permutations. Dans la configuration soudée à développements variables et en EVA, H admet un maximum d’au moins trois pour **4 012/5 040** attributions (79,6 %) et ZL pour **4 756/5 040** (94,4 %). H donne même quatre lieux pour 88 attributions, ZL pour 76. L’attribution suggérée par les domiciles est donc couramment égalée par des affectations concurrentes. Cette comparaison conditionne sur les sept paragraphes et la liste des sept noms. [Distributions exactes](manuscrit.json)

Si l’on retient après coup le meilleur résultat parmi les deux éditions, les deux alphabets, les choix d’espacement et de traitement des alternatives, les trois types de tables et les deux dispositions des mots, 4 993 permutations sur 5 040 atteignent trois lieux ou davantage. Cela couvre 72 combinaisons de réglages, équivalant ici à 18 matrices distinctes de contraintes. Permettre de plus l’échange des noms du Soleil et de la Lune, pour **chaque** permutation soumise au même choix, porte cet effectif à **5 014/5 040 (99,5 %)**. Parmi elles, 284 atteignent quatre lieux. Les deux distributions historiques restent à trois. Les pourcentages expriment cette sélection parmi des affectations calculées sur les mêmes données. [Contrôle de la sélection multiple](manuscrit.json)

## Rejouer

```sh
python3 formule.py etalonnage
python3 formule.py manuscrit
python3 verifier.py
```

Le calcul énumère les segmentations possibles au sein des limites fixées, fusionne les contraintes par sous-ensemble et conserve le maximum compatible avec une seule table. Le parcours des permutations énumère à part les affectations partielles injectives compatibles, puis toutes leurs extensions à sept noms. Le contrôle indépendant relit chaque exemple directement dans les deux fichiers IVTFF d’origine et applique la table enregistrée à chacun des groupes cités. [Calcul](formule.py) · [Vérification](verifier.py)
