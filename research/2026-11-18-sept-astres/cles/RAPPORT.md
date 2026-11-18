# Sept noms latins, une même table d’écriture

Sur chacun des deux folios, aucune des **5 040** attributions possibles ne rend les sept inscriptions compatibles avec une table commune, dans les trois familles d’écriture testées. En laissant choisir les noms, les lieux et les variantes graphiques, on peut faire tenir au plus **trois noms entiers sur sept**, ou **cinq noms abrégés sur sept**. La table et les lieux sont alors choisis après lecture. Ces accords partiels ne désignent aucun astre individuel. [Protocole et appariements](PROTOCOLE.md) · [Calcul complet](manuscrit.json) · [Vérification des maxima](verification.json)

## Une contradiction visible sur la feuille du Cancer

Sur f72r3, les deux éditions lisent `opalal` en .27 et `yfary` en .28. L’attribution publiée y place Mercure et Mars. Leurs deux noms latins commencent par **m**, au nominatif comme au génitif et après abréviation. Si chaque lettre latine s’écrit par une suite fixe de glyphes, cette suite devrait commencer à la fois par **o** et par **y**.

La difficulté existe aussi dans l’autre sens. La même inscription .27, attribuée à Mercure, et `oletal` en .33, attribuée à Vénus, commencent par **o**. Si chaque glyphe se développe en une suite fixe de lettres, celle-ci devrait commencer à la fois par **m** et par **u** (Venus est normalisé en *uenus*). Chacune de ces trois inscriptions tient en un seul groupe dans les deux éditions. Intervertir le Soleil et la Lune laisse ces deux contradictions intactes. [Transcriptions et graphies normalisées](manuscrit.json)

## Jusqu’où vont les correspondances partielles ?

Le tableau donne le maximum de lieux acceptés simultanément par **une seule** table. Pour chaque case, le calcul retient le plus favorable des deux cas grammaticaux et des deux découpages en glyphes. Il autorise également le choix entre les deux transcriptions à chaque lieu. Les meilleurs sous-ensembles et les tables peuvent différer d’une case à l’autre. [Calcul de l’attribution publiée](manuscrit.json) · [Calcul indépendant en attribution libre](verification.json)

| Forme des noms | Attribution publiée, f67r2 | Attribution publiée, f72r3 | Attribution libre, f67r2 | Attribution libre, f72r3 |
|---|---:|---:|---:|---:|
| Noms entiers | 2/7 | 2/7 | 3/7 | 3/7 |
| Trois premières lettres | 4/7 | 4/7 | 5/7 | 5/7 |

Avec les trois premières lettres des nominatifs et une à trois unités EVA par lettre, **chacun des sept rapprochements publiés** peut être obtenu isolément, sur chaque feuille. Garder la même table pour ces rapprochements fait tomber le maximum à quatre. Après échange du Soleil et de la Lune, le meilleur résultat abrégé est quatre sur f67r2 et trois sur f72r3. Aucune affectation complète n’existant déjà sur l’une ou l’autre série, aucune clé ne peut se transférer à la série partenaire, même lorsque l’on autorise le changement de cas ou de longueur des noms entre les deux folios.

## Formes manuscrites et contrôles

Les génitifs viennent des anneaux de l’imprimé de Nuremberg de 1493. Leurs initiales et leurs longueurs peuvent différer des nominatifs, notamment *Iupiter* et *iouis*. Le nominatif de Vénus utilise l’expansion usuelle du signe abréviatif final. Pour la sensibilité à l’abréviation, la règle des trois premières lettres est appliquée à chacun des sept noms. [Fac-similés, transcription et conventions de lecture](../temoin/LECTURE.md)

Les annotations horaires de ZL sont supprimées. Son alternative `okain.a[m:g]` sur f67r2.28 autorise les deux lectures du deuxième groupe et les groupes contigus. La variante qui omet ce lieu laisse six contraintes sur f67r2 ; même les six restantes ne peuvent recevoir six noms distincts avec une seule table. Sur f72r3, les sept lieux sont évaluables dans les deux éditions. Aucun lieu manquant n’est compté comme un nom lu.

Le contrôle synthétique présente l’une des séries en unités chiffrées et l’autre avec des groupes coupés et du remplissage. Le solveur retrouve la permutation cachée et la clé unique, puis lit avec cette clé les sept noms de la seconde série. Inverser la seule inscription chiffrant *sol* en préserve la longueur et le motif interne, mais aucune des 5 040 affectations ne rétablit une substitution bijective. Deux autres exemples construits pour les tables de largeur variable demandent effectivement des règles de deux et trois unités. Dans chaque cas la vraie affectation et la seule table compatible sont retrouvées. [Contrôles synthétiques détaillés](etalonnage.json)

Le premier programme essaie les 5 040 affectations puis réunit les tables partielles permises par chaque lieu. Le second découpe toutes les chaînes aux positions possibles et choisit ensemble le lieu, le nom et ses correspondances. Il recalcule le maximum sur tous les sous-ensembles de lieux. Les deux programmes relisent les fichiers IVTFF ; le second reprend les quatre listes normalisées du premier. Depuis la racine du dépôt, les trois commandes reproduisent les résultats.

```sh
python3 research/2026-11-18-sept-astres/cles/lecture.py etalonnage
python3 research/2026-11-18-sept-astres/cles/lecture.py manuscrit
python3 research/2026-11-18-sept-astres/cles/verifier.py
```

L’épreuve porte sur sept noms latins sous des règles d’écriture explicites. L’hypothèse iconographique de figures ou de secteurs associés aux astres demeure ouverte. Identifier des mots exigerait par exemple une table apprise ailleurs et des lectures exactes sur de nouveaux lieux, ou un témoin intelligible plaçant des mots reconnaissables aux mêmes endroits.
