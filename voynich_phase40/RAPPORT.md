# Phase 40 — ce que cinq lectures astronomiques permettent de contraindre

**Aucun déchiffrement ni traduction validés.** Les cinq lectures proposées par Caspari et Faccini sont compatibles avec une clé partielle dans **une seule des huit configurations de transcription** examinées. Cette compatibilité impose neuf correspondances si l'on accepte leurs mots de départ ; elle n'établit pas que ces mots sont ceux du manuscrit.

## Les passages effectivement examinés

La figure 1 de [*A Key to the Voynich Manuscript*](https://doi.org/10.31235/osf.io/8b4we_v1), page 4 du [PDF source](../docs/PIECES_REFERENCES.md#piece-def075ceb6ef64), propose les cinq lectures suivantes. Les apostrophes sont retirées pour les équations, sans développer les abréviations.

| Figure | Locus IVTFF | Formes conservées | Lecture proposée par les auteurs |
|---|---|---|---|
| A | f68r2.19 | `cholar`, `chodar` | `POLAR` |
| B | f68v2.17, mot au-delà de l'étoile | `ypchy`, `yypchy` | `EXPE` |
| C | f68r3.11 | `doaro`, `doary` | `TOARE` |
| D | f68r1.15 | `otydy` | `O'CETE` |
| E | f68r1.26 | `otor` | `O'COR` |

ZL et IT donnent respectivement `cholar`, `ypchy`, `doaro`, `otydy`, `otor`. Les interlinéaires historiques ajoutent `chodar` chez Roe, `yypchy` dans la ligne C et `doary` chez Grove. Les références exactes et lignes brutes sont dans [ANCHORS.json](ANCHORS.json). La suppression des `!` d'alignement suit la [description du format par Stolfi](https://www.ic.unicamp.br/en/~stolfi/EXPORT/voynich/98-12-28-interln16e6/). Aucun signe inconnu n'a été remplacé par une lettre attendue.

Les cinq zones ont été retrouvées sur les [images originales Yale](https://collections.library.yale.edu/catalog/2002046) : recto 7 993 × 3 828 pixels, verso 8 135 × 3 843 pixels. Les [recadrages](PLANCHES.md) sont conservés. Le premier aperçu d'atlas consulté mesurait seulement 1 800 × 862 pixels ; le recto original a été retéléchargé et son empreinte correspond à celle de l'archive antérieure. Ces observations servent à localiser les passages. L'opérateur connaissait les lectures proposées : aucune adjudication paléographique indépendante n'est revendiquée.

L'identité des astres ne constitue pas un texte clair de référence. Par exemple, la [description du cahier 9](https://www.voynich.nu/q09/) présente l'identification du groupe de sept étoiles comme une hypothèse et signale une alternative. Notre calcul n'introduit ni « Pléiades », ni « Taureau », ni une traduction française comme réponses certaines.

## Une famille de règles explicite

Le solveur exact de phase 30 est réutilisé sans modification. Chaque lettre du texte proposé reçoit un code de 1 à 3 caractères EVA. Deux lettres ne partagent pas un code et aucun code n'est préfixe d'un autre. Le sens de lecture et une terminaison muette commune de 0 à 2 caractères sont recherchés. Aucun ajout, suppression ou réordonnancement propre à un mot n'est permis.

C'est une famille restreinte, utile pour vérifier les équations. Elle ne représente pas toutes les abréviations, polyphonies ou ligatures qui se recouvrent dans la table complète de la publication. Un échec ne réfute donc pas toutes les versions de cette hypothèse, encore moins toute possibilité de déchiffrement.

Le [protocole](PROTOCOL.json), les sources et les scripts ont été figés au commit `5f9b197b64bb628be91ffa49736976c2bf6476b9`, avant le calcul des scores. Les mots et la difficulté `doaro/TOARE` avaient déjà été examinés : le gel n'est pas un aveuglement rétroactif. Onze contrôles mécaniques passent, notamment pour les codes inconnus, la lecture inversée, la terminaison commune, l'ambiguïté et l'épuisement du budget. Ils ne prouvent aucune capacité sémantique historique.

## Résultat des huit configurations et des permutations

| A | B | C | Ajustement des cinq lectures | Affectations compatibles parmi les 120 permutations |
|---|---|---|---|---|
| cholar | ypchy | doaro | Incompatible | 0 |
| cholar | ypchy | doary | Unique sur les neuf lettres couvertes | 1 |
| cholar | yypchy | doaro | Incompatible | 0 |
| cholar | yypchy | doary | Incompatible | 0 |
| chodar | ypchy | doaro | Incompatible | 0 |
| chodar | ypchy | doary | Incompatible | 0 |
| chodar | yypchy | doaro | Incompatible | 0 |
| chodar | yypchy | doary | Incompatible | 0 |

Les 960 affectations sont toutes évaluées, y compris les huit affectations publiées. La seule compatible est l'affectation publiée avec `cholar/ypchy/doary`. **Ce résultat n'est pas une probabilité de vérité ni une validation linguistique** : les cinq chaînes proposées ont été construites par leurs auteurs à partir de ces mêmes signes. Les contraintes de longueur et de répétition contribuent fortement à éliminer les permutations.

La clé conditionnelle obtenue lit de gauche à droite, sans terminaison muette :

| Unité EVA | a | t | y | l | o | ch | r | d | p |
|---|---|---|---|---|---|---|---|---|---|
| Valeur latine supposée | a | c | e | l | o | p | r | t | x |

Ce sont neuf valeurs **déduites des mots supposés**, pas neuf lettres historiquement déchiffrées. Les valeurs absentes de ces exemples restent inconnues.

La contradiction de C est particulièrement simple. `doaro` et `toare` ont chacun cinq caractères. Avec des codes non vides, chaque lettre devrait occuper un seul caractère ; aucune terminaison muette n'est possible. En lecture directe, le même `o` EVA devrait alors valoir `o` et `e`. En lecture inverse, le motif de répétition reste incompatible. Ce n'est pas un échec d'optimisation : aucune solution n'existe dans la famille déclarée. [Interlinéaire conservant les deux lectures](https://www.voynich.nu/q09/f068r3_tr.txt).

## Que reste-t-il quand on retire un exemple ?

Dans la configuration compatible, le retrait de chaque ancrage donne :

| Exemple retiré | Résultat avec les quatre autres | Prédiction sans compléter la clé |
|---|---|---|
| A, POLAR | Plusieurs clés ; `l` absent de l'apprentissage | Aucune lecture unique |
| B, EXPE | Clé unique sur les lettres restantes ; `x` absent | `e?`, lecture interrompue au code inconnu |
| C, TOARE | Clé unique | `toare` si la transcription est `doary` |
| D, O'CETE | Clé unique | `ocete` |
| E, O'COR | Clé unique | `ocor` |

Sans A, deux segmentations sont notamment possibles pour B : `y-p-ch-y` et `y-pc-h-y`, avec des valeurs différentes pour les unités centrales. B ne détermine pas seul cette séparation. Les trois restitutions exactes C/D/E sont une cohérence interne entre les exemples de la publication. Elles ne sont pas trois confirmations indépendantes, puisque ces exemples ont servi ensemble à construire la proposition.

Les 40 retraits, sur les huit configurations, sont archivés. Dans la configuration ZL/IT `cholar/ypchy/doaro`, retirer C permet d'ajuster les quatre autres, mais prédit `toaro`, et non `toare`. Les quatre autres retraits laissent une contradiction.

## Application littérale aux autres légendes

La règle conditionnelle est appliquée aux transcriptions originales, sans remplacer silencieusement `doaro` par `doary`. La projection figée porte sur les 58 loci dont le marqueur est exactement `@Ls` : 12 sorties entièrement couvertes par transcription, dont 8 hors des quatre loci d'ajustement présents dans ce périmètre. B est sur une ligne radiale et ne figure pas dans ce sous-ensemble.

Un [supplément déclaré après résultat](ADDENDUM.md) inclut les six autres loci `Ls`, précédés de `+`, `=` ou `*`. Sur les **64 légendes**, 14 sont entièrement couvertes dans chaque transcription, dont 10 hors des loci d'ajustement. ZL conserve 46 sorties incomplètes et 4 loci à marques non prises en charge ; IT conserve 50 sorties incomplètes. Les 14 sorties ne concernent pas exactement les mêmes loci dans les deux sources.

Voici toutes les sorties entièrement couvertes dans au moins une transcription. **Ce tableau contient des suites conditionnelles de lettres, aucune signification attribuée.** Le tiret signifie que la projection ne fournit pas de suite complète admissible.

| Locus | Sortie ZL | Sortie IT |
|---|---|---|
| f68r1.15 | ocete | ocete |
| f68r1.18 | ecpote | ecpote |
| f68r1.20 | olor | olor |
| f68r1.23 | ocpte | — (`otcsdo`, code inconnu) |
| f68r1.25 | ocol | ocol |
| f68r1.26 | ocor | ocor |
| f68r2.10 | opore | opore |
| f68r2.12 | tpol | tpol |
| f68r2.17 | oetpe | oetpe |
| f68r2.19 | polar | polar |
| f68r2.28 | potar | potar |
| f68r3.10 | — (`dchol,day`, frontière incertaine) | tpol tal |
| f68r3.11 | toaro | toaro |
| f68r3.14 | ocare | ocore |
| f68r3.20 | tarall | tarall |

Aucun catalogue stellaire, dictionnaire ou modèle de langue ne sélectionne les lignes qui « ressemblent » à des mots. Les sorties complètes et incomplètes restent dans [all_star_labels.json](results/all_star_labels.json). Ce faible périmètre ne mesure pas la couverture de la table complète de Caspari et Faccini, qui comporte d'autres règles ; celle-ci avait fait l'objet d'un audit différent en phase 38.

## Vérification et portée

Un second programme énumère toutes les compositions de longueurs possibles, combine les équations et compte les modèles sans importer le solveur principal. Il confirme les **1 016 cas** : 8 ajustements, 960 permutations, 40 retraits et 8 paires individuelles. Contrairement au solveur principal, qui s'arrête après deux contre-modèles, il énumère les ensembles complets ; le plus grand contient 12 modèles.

Les témoins source, les pixels des cinq recadrages, les 116 lignes de projection principale et tous les comptes sont contrôlés. Le supplément vérifie ses 128 lignes avec les deux décodeurs. Une réexécution en dossier neuf reproduit **huit fichiers à l'octet**. Il s'agit d'une vérification informatique par le même opérateur, pas d'une réplication externe ni d'une expertise paléographique. [Reproduction](REPRODUCTION.md).

La piste fournit ainsi des contraintes vérifiables et un désaccord local précis, mais aucune clé historique validée. Pour progresser vers une traduction, il faut des lectures de signes justifiées indépendamment des mots recherchés, puis une règle qui prédit du texte suivi et reçoit des confirmations externes. Choisir `doary` parce que cela produit `TOARE`, ou développer librement les chaînes restantes, ne satisferait pas cette exigence. L'objectif de déchiffrement reste ouvert.
