# La contraction de deux groupes sur trois roues du Voynich

Sur f67r2, **une des sept légendes se reconstitue**, celle du secteur 8. Les deux éditions donnent `ytor.daiin` → `yto` + `aiin` → `ytoaiin`. La même coupe reconstitue la même légende au secteur 6, à partir de deux mots différents. Aucun des cinq secteurs réservés, ni aucun des deux feuillets de transfert, ne reproduit le mécanisme dans le sens annoncé. [Hypothèse et règles figées](HYPOTHESE.md)

## Les deux cas à l’origine de la règle

| Cible | Lieu de départ | Lecture et concurrence |
|---|---|---|
| Secteur 8, f67r2.37, `ytoaiin` | Secteur 8, .36, mots 1–2, dernière ligne | `ytor.daiin` donne la seule coupe `yto + aiin`. Dans le secteur 6, .29, mots 1–2, `ytody.saiin` donne exactement la même coupe. Ce second emplacement est en première ligne. |
| Secteur 5, f67r2.28, `okain.am` en H | Secteur 5, .27, mots 1–3 | Dans `okeor.aiin.am`, réduire `aiin` en `ain` conserve ensuite **tout** le second groupe. La règle exige d’enlever au moins une unité à chacune des deux sources. Copier `am` ne résout pas cette difficulté. En ZL, `okeo,r` et `a[m:g]` ajoutent une incertitude de lecture. |
| Même cible du secteur 5 | Secteur 2, .16, mots 2–3, en ZL | `okoes.oekain` donne `ok + ain`. Seul le premier groupe de la légende est rendu. |

Les coupes et les lieux ci-dessus incluent toutes les réussites directes dans les douze paragraphes. Réduire les suites de `i` conserve ces lieux. Dans le secteur 8, la coupe normalisée est `yto + ain`. Aucun triplet de sources ne restitue deux groupes cibles consécutifs.

## Les cinq autres légendes

| Secteur | Légende H | Légende ZL | Secteurs donnant au moins une contraction directe |
|---|---|---|---|
| 1, .15 | dylchsody | dolchsody | 0 sur 12 |
| 3, .22 | okal | okal | 0 sur 12 |
| 6, .31 | opcholdy | opcholdy | 0 sur 12 |
| 7, .34 | dfar.oeoldan | ofar.oeoldan | 0 sur 12 |
| 11, .47 | yfain | yfain | 0 sur 12 |

Le résultat vaut pour les douze lectures, même en cherchant sur toutes les lignes et en acceptant n’importe quel groupe de la légende. L’inversion des deux sources ne donne aucun accord local parmi les sept légendes. Ailleurs, elle crée notamment `ofar` dans le secteur 4 en ZL. Les résultats donnent également les autres accords inversés, l’ordre physique de leurs sources et toutes leurs coupes.

## Position et témoins

On compte un succès par légende dans son propre secteur. Les rotations déplacent ensemble les cibles autour des douze notices, décalage nul compris. Les permutations injectives attribuent des notices distinctes aux cibles, en gardant leur texte intégral, leur longueur et le nombre de groupes de chaque étiquette. Pour les sept cibles, il existe 3 991 680 affectations possibles. Les probabilités indiquent la fraction donnant au moins le score observé. Les exemples ayant inspiré la règle entrent dans ce calcul descriptif.

| Lecture et portée | Réussites locales | Fenêtres concurrentes avec accord | Rang de la rotation réelle, ex æquo inclus | Probabilité exacte, permutations |
|---|---:|---:|---:|---:|
| Légende entière, toute ligne, H et ZL | 1/7 | 1 | 1–2 sur 12 | 665 280 / 3 991 680 = 1/6 |
| Légende entière, dernière ligne, H et ZL | 1/7 | 0 | 1 sur 12 | 332 640 / 3 991 680 = 1/12 |
| Un groupe suffit, toute ligne, H | 1/7 | 1 | 1–2 sur 12 | 1/6 |
| Un groupe suffit, toute ligne, ZL | 1/7 | 2 | 1–3 sur 12 | 31/132 |
| Cinq cibles réservées, un groupe suffit, toute ligne | 0/5 | 0 | 1–12 sur 12 | 95 040 / 95 040 = 1 |

Dans les douze paragraphes de H, la recherche parcourt 55 fenêtres lisibles de deux groupes et 25 de trois. En dernière ligne, elle en parcourt 19 et 9. En ZL prudent, avec les espaces douteux joints, ces nombres sont 52 et 24 sur la page, 19 et 9 en dernière ligne. Espaces coupés, ils passent à 54 et 26, puis 20 et 10. Au secteur 8, la destination locale est à égalité au premier rang avec le secteur 6 sur l’ensemble des lignes examinées. Elle arrive seule en tête parmi les dernières lignes.

## Deux roues de transfert

Les rayons et les frontières proviennent du relevé géométrique préalable. Pour f69r, le relevé strict conserve 13 rayons devant 12 des 16 cases. Les quatre cases sans rayon strict restent à leur position dans les rotations. Le relevé élargi examine les 16 cases et 22 rayons distincts. Pour f67v1, les 12 cartouches ont chacun leur rayon intérieur. L’ajout du rayon .28 à la case .12 porte le total à 13. Chaque fenêtre reste à l’intérieur d’un rayon. [Relevé et planches](../geometrie/README.md)

| Feuillet et rayons | Fenêtres physiques lisibles H, deux / trois groupes | Réussites directes locales | Réussites directes ailleurs |
|---|---:|---:|---:|
| f69r, attribution stricte | 27 / 14 | 0 sur 12 cases pourvues | 0 |
| f69r, bordures admises | 46 / 24 | 0 sur 16 | 0 |
| f67v1, axe intérieur | 25 / 13 | 0 sur 12 | 0 |
| f67v1, bord admis | 27 / 14 | 0 sur 12 | 0 |

Le décompte des fenêtres physiques compte une seule fois chaque position d’un rayon placé entre deux cases. Les quatre comparaisons donnent le même résultat direct dans les deux éditions et toutes les variantes, y compris sous rotation ou permutation. Dans le seul contrôle inversé de f69r qui donne des accords, le rayon .24, mots 3–4, fournit `dair` par `da + ir` à distance. La bordure le rattache à .6 et .7. Il apparaît donc deux fois dans la matrice pour chaque cible compatible. Aucune légende complète n’y correspond.

## Reproduction

Depuis ce dossier, exécuter `python3 comparer.py` puis `python3 verifier.py`. Le vérificateur relit les IVTFF, énumère tous les préfixes et suffixes propres des sources, puis reconstruit les fenêtres, les rotations et les distributions d’injections. Il contrôle 1 440 scores. Les éditions sont H (IT2a-n) et ZL (ZL3b-n). Chacune est traitée avec espace douteux joint ou coupé et avec lecture prudente, première ou dernière alternative. Une position illisible conserve sa place. Le troisième mot éventuel doit être recopié littéralement, y compris dans la variante à `i` réduit.

Les JSON compressés consignent les textes avec leurs positions, le volume par secteur, toutes les coupes locales et concurrentes, les matrices de fenêtres distinctes, les rangs ex æquo, les rotations et les distributions exactes. Le champ `deux` accepte n’importe quel groupe cible, `trois` demande en plus la copie du groupe suivant et `complet` exige que toute la légende soit rendue. Une légende de plus de deux groupes dépasse par construction la portée de la prédiction complète. [f67r2](f67r2.json.gz) · [f69r strict](f69r-strict.json.gz) · [f69r élargi](f69r-possible.json.gz) · [f67v1 strict](f67v1-axis_inside_visible_frame.json.gz) · [f67v1 élargi](f67v1-possible_including_edge.json.gz)
