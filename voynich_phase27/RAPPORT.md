# Phase 27 — Une propriété que les clés positionnelles ne peuvent pas corriger

**Les substitutions bijectives selon la position ne peuvent pas ramener les échantillons Voynich dans les bandes de nos textes témoins : la mesure choisie reste exactement inchangée sous ces substitutions.** Les huit échantillons ZL, dans les groupes A et B et leurs deux ensembles de folios, se situent sous les deux bandes fixées. La sensibilité IT donne la même conclusion opérationnelle.

Cela met en difficulté **le modèle testé avec ces références et ces unités de transcription**. Ce n'est pas une exclusion de tout latin ou italien, de tout chiffre positionnel, ni une preuve d'absence de message. Huit contrôles à message connu, parfaitement réversibles mais ajoutant un suffixe nul, sortent eux aussi des bandes. **Aucune clé, langue ou traduction n'est identifiée.** `NOT_TRANSLATION`.

[Résultats et contre-exemples](../docs/PIECES_REFERENCES.md#piece-c816132c48b531)

## Pourquoi cette piste après les phases précédentes

La phase 18 obtenait un gain avec des tables de substitution distinctes en fin de mot. La phase 19 montrait que des générateurs sans passage cible produisaient aussi ce gain. La phase 22 n'améliorait pas le découpage des nouveaux passages ; la phase 26 excluait de relancer le dispositif image–étiquette inchangé. Il fallait donc un critère que l'optimisation d'une clé ne puisse pas artificiellement améliorer.

Les travaux sur l'entropie du Voynich, notamment [Lindemann et Bowern](https://arxiv.org/abs/2010.14697v2), motivent l'étude de la prévisibilité des caractères. Ici, la comparaison est conditionnée par la longueur exacte et la position dans le mot ; ce n'est pas une reproduction intégrale de leur étude. Le caractère historiquement connu de la faible entropie n'est pas présenté comme une découverte nouvelle. [Sources et périmètre de consultation](../docs/PIECES_REFERENCES.md#piece-7b97d8179ef8a8).

## Hypothèse testée et propriété démontrable

L'hypothèse associe un caractère littéral EVA à une lettre du texte clair, conserve espaces et longueurs, et utilise une permutation fixe de l'alphabet à chaque couple **longueur du mot × position**. Cette famille contient les deux modèles de phase 18 et autorise même une table différente pour chaque position de chaque longueur.

Pour deux positions voisines, changer leurs alphabets bijectivement permute les lignes et colonnes du tableau de fréquences. Cela conserve exactement les entropies et donc `H(signe suivant | signe précédent, longueur, position)`. La moyenne de ces quantités, appelée **T**, est notre mesure principale. Une valeur plus basse signifie davantage de prévisibilité dans cet échantillon.

Chaque paquet comporte **600 occurrences de mots : 150 de chacune des longueurs 4, 5, 6 et 7**, soit 3 300 caractères. Les positions sont moyennées à l'intérieur de chaque longueur, puis les quatre longueurs reçoivent le même poids. Aucun espace ni transition entre mots n'entre dans T. L'entropie marginale par position est un contrôle secondaire, sans critère de découverte.

Cette invariance est une propriété exacte des tableaux observés. En revanche, supposer que les textes témoins représentent la distribution d'un éventuel texte clair inconnu est une hypothèse empirique, beaucoup plus limitée.

## Protocole figé avant les mesures

Le commit local **`84805ce`**, puis [FREEZE.json](FREEZE.json), fixent sources, sélection, code, seuils et règles d'arrêt avant la génération et les nouvelles mesures. Les seuls décomptes préalables concernaient la disponibilité des mots par longueur et les métadonnées. Ce gel local n'est pas un préenregistrement extérieur.

Douze paquets disjoints de César et douze d'Inferno/Purgatorio servent de référence. Pour chaque langue, la bande opérationnelle va du minimum au maximum de T observés sur ces douze paquets, avec une marge préfixée de **0,20 bit de chaque côté**. Ce ne sont pas des intervalles de confiance et aucune p-value n'est calculée.

Six paquets disjoints de Pline et six du Paradiso servent à la validation. Le protocole exige au moins **5/6 dans la bande de leur langue, séparément pour les deux langues**, ainsi que la conservation mécanique des mesures sous chiffrement. Un échec aurait arrêté l'expérience avant toute mesure Voynich. Aucun seuil n'a changé après résultat.

Chaque paquet de validation est chiffré par trois nouvelles clés : initiale distincte, finale distincte et tables libres par longueur/position. Le calcul ne reçoit pas les clés ; elles sont conservées à part pour la vérification. **Les 36 chiffres dérivent de douze paquets de deux œuvres : ce ne sont pas 36 textes indépendants et aucun déchiffrement n'est effectué.** Dante fournit plusieurs livres, sans constituer plusieurs auteurs indépendants.

## Calibration et mécanismes concurrents

Les bandes obtenues sont **[1,490181 ; 1,939661] bits pour la référence latine** et **[1,642797 ; 2,092231] pour l'italienne**. Les contrôles passent : 6/6 Pline, 6/6 Paradiso, et les 36 versions chiffrées donnent exactement les mêmes mesures que leurs textes de départ.

| Famille de contrôle | Nombre | Résultat par rapport à la bande de référence correspondante |
|---|---:|---|
| Textes de validation non chiffrés | 12 | 12 dans la bande |
| Trois familles de substitution bijective | 36 | 36 dans la bande, invariance exacte |
| Ordre des mots mélangé | 12 | 12 dans la bande, mesure inchangée |
| Colonnes de caractères mélangées à longueur fixe | 12 | 12 au-dessus de la bande |
| Générateur local de caractères Markov d'ordre 1 | 12 | 12 dans la bande |
| Voyelles a/e/i/o/u fusionnées en a | 12 | 6 latins dans la bande ; 6 italiens au-dessous |
| Suffixe nul réversible ajouté à chaque mot | 8 | 8 au-dessous |
| Générateur Timm, sorties archivées | 6 | 6 au-dessous des deux bandes |

Les **110 contrôles** ne représentent pas autant de mécanismes ou de corpus indépendants. Les contrôles dérivés partagent leurs mots sources. Les six sorties Timm avaient été exécutées en phase 24 ; elles sont rééchantillonnées pour cette nouvelle mesure, sans prétendre à une nouvelle exécution native.

Les témoins mélangés par colonne conservent exactement chaque fréquence de signe à chaque position et longueur. Leur rejet montre que la mesure distingue ici les dépendances internes des simples marges positionnelles. Les modèles Markov, ajustés uniquement sur les sources de référence, produisent au contraire des mots selon des transitions locales sans encoder un passage choisi, et passent tous. Une valeur dans la bande n'est donc pas une preuve de message.

Le contre-exemple réversible est particulièrement instructif : on ajoute exactement un `x` à chaque mot, puis on chiffre par une seule permutation. L'inverse de la clé suivi du retrait d'exactement ce caractère ajouté récupère chaque mot original. Pourtant, les huit paquets sont rejetés par le filtre. **Une sortie sous la bande n'est donc pas une preuve d'absence de texte clair.** Ce contrôle est hors de l'hypothèse initiale, car il change les longueurs. Il ne reproduit pas tout le Voynich, notamment les valeurs plus basses du groupe B.

## Manuscrit : partitions et résultats

La calibration ayant passé, les deux transcriptions sont extraites directement de leurs fichiers IVTFF épinglés : loci réels P0/P1, mots littéraux `[a-z]+`, métadonnées connues. Les mots à alternatives, espaces incertains ou signes illisibles sont exclus sans choisir une lecture. Les interruptions ne sont pas franchies. Les lignes repliées et changements de métadonnées sont traités. f85/f86 sont exclus ensemble ; fRos n'est pas converti en folio indépendant.

A et B sont séparés. La partition suit `floor(numéro_de_folio / 5) modulo 2` : les faces et panneaux d'un folio restent ensemble. Deux paquets sans occurrence commune sont tirés dans chaque moitié, soit quatre par groupe et transcription. Chaque paquet conserve locus, ligne source, folio, section, main attribuée et identifiant d'occurrence.

| Transcription / groupe | Paquets | Occurrences distinctes | Folios physiques représentés | Étendue de T | Critère figé |
|---|---:|---:|---:|---:|---|
| ZL A, principal | 4 | 2 400 | 54 | 1,141394–1,224223 | 4/4 sous les deux bandes |
| ZL B, principal | 4 | 2 400 | 38 | 0,953609–1,008787 | 4/4 sous les deux bandes |
| IT A, sensibilité | 4 | 2 400 | 54 | 1,224387–1,235921 | 4/4 sous les deux bandes |
| IT B, sensibilité | 4 | 2 400 | 38 | 0,988495–1,053208 | 4/4 sous les deux bandes |

Les 4 800 occurrences ZL et les 4 800 IT ne sont pas additionnées comme inscriptions indépendantes. IT est une autre transcription du même manuscrit. Les listes complètes des folios et distributions section/main sont dans [verification.json](results/verification.json) et chaque fichier de paquet ; les exclusions d'extraction sont dans [MANUSCRIPT_COVERAGE.json](../docs/PIECES_REFERENCES.md#piece-7179695f585393).

Tous les quatre paquets d'un groupe doivent sortir de la bande du même côté pour déclarer l'incompatibilité opérationnelle. Cette condition passe pour les deux groupes et les deux références, avec la même sensibilité IT. Aucune combinaison de p-values n'est utilisée. Les partitions restent internes à des données déjà exposées, avec mélanges de sections et de mains explicités, non supprimés statistiquement.

## Ce qui est prouvé, observé et encore inconnu

**Preuve mathématique et logicielle :** toute clé de la famille définie conserve T. Pour les paquets mesurés, chercher une meilleure clé dans cette famille ne peut donc corriger l'écart avec les bandes de référence.

**Observation calibrée :** les textes témoins et leurs chiffres bijectifs passent ; ZL et IT restent sous les bandes sur toutes les partitions prévues. Ce résultat est conditionnel aux textes, normalisations, unités EVA, longueurs et échantillonnages choisis.

**Limites :** ces références couvrent peu d'œuvres et deux langues. L'échantillon de Pline le plus élevé est à environ 0,006 bit de la borne supérieure : une marge choisie autrement aurait pu changer la calibration. La marge de 0,20 était fixée avant mesure ; elle n'est pas une garantie universelle. L'estimateur empirique est biaisé en petit échantillon, et égaliser les effectifs ne neutralise pas tous les effets de support alphabétique. Aucune sensibilité supplémentaire de marge ou d'unité n'est ajustée après résultat.

Les espaces peuvent être inexacts, un signe EVA peut ne pas être une unité de chiffre, plusieurs signes peuvent encoder une lettre, des signes peuvent être insérés ou supprimés, ou les tables peuvent changer par mot ou par main. Ces possibilités sont hors de l'hypothèse testée. Les contrôles montrent eux-mêmes que compatibilité et incompatibilité ne sont ni reconnaissance de langue ni preuve de sens ou de non-sens.

**Rien ici n'identifie un mécanisme historique.** Le générateur Timm et le témoin à suffixe peuvent approcher certaines valeurs sans expliquer tous les groupes, les images, la syntaxe ou un message continu. Aucun exemple de « traduction » n'est produit.

## Vérification et suite justifiée

Une seconde implémentation utilise directement les probabilités conditionnelles, sans la soustraction de deux entropies du moteur principal. Elle vérifie **150 paquets et 2 700 cellules conditionnelles**, avec un écart maximal de **1,33 × 10⁻¹⁵**. Les 44 paquets chiffrés réversibles, soit 145 200 caractères en comptant les versions répétées, sont inversés exactement. Les 264 marges des mélanges positionnels et les 9 600 occurrences Voynich sont relues dans les sources brutes. Les non-chevauchements promis et les partitions physiques passent.

Une réexécution isolée depuis les sources reproduit **257 fichiers à l'octet près**. C'est une vérification du logiciel et de la reproductibilité, pas une validation linguistique extérieure. La figure a été inspectée. Les manifestes des phases 22 à 26 et de l'atlas passent ; aucune ancienne réserve n'est rétablie artificiellement et aucun des 970 loci non examinés de phase 26 n'est déclaré inspecté.

La piste concrète suivante serait de calibrer la récupération d'un **encodage réversible qui ajoute des signes ou change les unités**, avec récupération exacte de clés/messages sur des passages neufs avant tout transfert au Voynich. Le suffixe nul fournit un contre-exemple simple pour cette calibration, pas une solution du manuscrit. Cette phase s'arrête conformément à son protocole, sans lancer un réglage supplémentaire après résultats.

[Protocole](PROTOCOL.json) · [Méthodes techniques](METHODS_EN.md) · [Reproduction](README.md) · [Tous les contrôles](results/controls.json) · [Résultats Voynich](results/manuscript.json) · [Vérification](results/verification.json)
