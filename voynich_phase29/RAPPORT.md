# Phase 29 — signes rares, abstention et ambiguïté des unités

**Calibration non validée : 5/24 contrôles positifs donnent une lecture de transfert exacte et autorisée. Les 18 variantes avec signes ajoutés restent toutes ambiguës ; un autre contrôle s’abstient devant des signes inconnus. Aucune application au Voynich. `NOT_TRANSLATION`.**

La correction évite les suppressions destructives dans les cas testés, mais elle ne résout pas l’ambiguïté des unités. Maintenir la bonne lecture parmi plusieurs possibilités n’est pas la retrouver. Les résultats de phase 28 sont conservés, sans correction rétrospective ni effacement des échecs.

[Résultats et abstentions](../docs/PIECES_REFERENCES.md#piece-b49706ef37fb12)

## Ce qui change et ce qui reste inconnu

En phase 28, un prédécesseur vu une seule fois faisait rejeter un marqueur pourtant soutenu par de nombreuses occurrences. La nouvelle règle conserve tous les prédécesseurs compatibles, y compris rares, et exige seulement qu’au moins quatre soient fréquents. Elle exige toujours une explication de toutes les occurrences du marqueur ; elle n’invente pas la règle d’un signe jamais observé.

La préférence systématique pour supprimer davantage de signes est retirée. Toutes les grammaires admissibles sont conservées. Une lecture n’est autorisée que si une seule grammaire reste possible, sans alerte structurelle, et que son transfert ne rencontre ni signe inconnu ni violation de règle. Si plusieurs grammaires sont possibles, les sorties restent alternatives, quel que soit leur score linguistique. Le transfert ne sert pas à promouvoir une alternative.

Un signe fréquent présent uniquement en fin de certains mots déclenche une abstention : l’ajout facultatif ne fait pas partie de la grammaire prise en charge, et ce signe peut aussi être une vraie lettre. Cette alerte ne l’efface pas.

Les quatre cas problématiques connus de phase 28 (`c012`, `c013`, `c017`, `c035`) servent d’abord de régressions de développement. Dans chacun, les bonnes unités sont conservées, mais la réponse reste ambiguë. Après gel, le calcul complet retrouve également un transfert exact parmi leurs alternatives. **Aucun de ces quatre cas n’entre dans les dénominateurs de validation nouvelle, et aucun n’est déclaré déchiffré par la nouvelle politique.** [Régressions](development/REGRESSIONS.json).

## Gel, données et indépendance

Protocole, sources, code, graines, critères et règles d’arrêt ont été figés au commit `af23400`, avant toute génération ou mesure des nouveaux cas. Les fichiers de gel et leurs empreintes sont dans [FREEZE.json](FREEZE.json). Ce gel est local ; aucune évaluation humaine en aveugle ni préinscription externe n’est revendiquée.

Les sources sont les mêmes instantanés qu’en phase 28 : [Apulée, *Métamorphoses*, transcription Perseus fixée à une révision précise](https://github.com/PerseusDL/canonical-latinLit/blob/8b536bdf3ed1f43494055efe112433b4a58eab67/data/phi1212/phi002/phi1212.phi002.perseus-lat1.xml), et [Manzoni, *I promessi sposi*, texte italien](https://www.gutenberg.org/ebooks/45334). Les modèles linguistiques restent ceux de César et de Dante. Aucun nouvel auteur n’est ajouté. Les fichiers sources entiers étaient déjà disponibles ; seuls les intervalles évalués ici sont nouveaux et disjoints des anciens.

Dans chaque source, les ajustements contiennent 1 000 mots à partir des indices 12 000, 16 000 et 20 000 ; les transferts contiennent les 400 mots suivant une marge de 100 mots. Les douze intervalles ne se recoupent ni entre eux ni avec ceux de phase 28. Cela représente six paires littéraires, 6 000 mots d’ajustement et 2 400 mots de transfert uniques, soit 13 152 lettres de transfert. Les espaces normalisés et la langue correcte sont fournis. Le problème de segmentation des phases 20–22 reste ouvert.

Chaque paire reçoit quatre encodages positifs et deux encodages hors modèle, avec des clés couplées pour ces variantes. Ce sont donc six messages de base, pas 36 messages indépendants. Les témoins générés réutilisent des distributions ou vocabulaires de référence ; ils ne sont pas de nouveaux textes littéraires indépendants.

Au total : **48 cas nouveaux et quatre régressions exposées**, 92 recherches de clé sur des grammaires candidates, dont 82 pour les cas nouveaux et dix pour les régressions. Une même recherche ne bénéficie d’aucune nouvelle tentative après résultat : huit départs, 60 000 étapes, solveur C++ de phase 18 inchangé. Les candidats partagent passages et modèles ; ils ne constituent pas des réplications indépendantes.

## Résultats complets par groupe

| Groupe nouveau | Cas | Transfert exact autorisé | Ambiguïté conservée | Autre abstention |
|---|---:|---:|---:|---:|
| Substitution simple | 6 | 5 | 0 | 1 |
| Signe final ajouté | 6 | 0 | 6 | 0 |
| Certaines lettres à deux signes | 6 | 0 | 6 | 0 |
| Combinaison des deux ajouts | 6 | 0 | 6 | 0 |
| Deux signes distincts pour chaque lettre | 6 | 0 | 0 | 6 |
| Signe final ajouté à un mot sur deux | 6 | 0 | 0 | 6 |
| Vraie finale `a` ou `e`, sans ajout | 4 | 0 | 4 | 0 |
| Vraie lettre interne en couples réguliers, sans ajout | 2 | 0 | 2 | 0 |
| Vraie finale sur la moitié des mots, sans ajout | 2 | 0 | 0 | 2 |
| Markov, encodage combiné | 4 | 0 | 4 | 0 |
| **Total nouveau** | **48** | **5** | **28** | **15** |
| Régressions exposées, séparées | 4 | 0 | 4 | 0 |

Les 24 positifs exigeaient une sortie unique, un transfert exact et les bonnes unités sur les deux passages. Le résultat est **5/24**, contre 24/24 requis. Les cinq réussites sont toutes des substitutions simples. Aucun des 18 nouveaux encodages à signes ajoutés n’a été résolu de façon unique.

Les bonnes unités existent parmi les branches calculées sur les deux passages dans **22/24** positifs ; un transfert exact existe sous ces bonnes unités dans **20/24**. Ces chiffres sont des diagnostics après comparaison aux réponses, jamais des récupérations annoncées. Aucun « meilleur candidat selon la réponse » n’est transmis comme lecture du système. Les tableaux [RESULTATS.csv](results/RESULTATS.csv), [SUMMARY.json](results/SUMMARY.json) et [BRANCH_AUDIT.json](results/BRANCH_AUDIT.json) conservent les distinctions.

## Lettres rares, lettres absentes et clés incomplètes

Le contrôle italien `c028` possède une grammaire unique et un texte d’ajustement exact. Mais `j` et `y`, chacun présent une fois dans le transfert, sont absents de l’ajustement. Leurs signes restent inconnus : le système s’abstient. Les variantes à deux signes du même passage (`c030`, `c031`) rencontrent aussi ces prédécesseurs jamais observés, avec deux erreurs de règle dans les branches à marqueur. La correction des signes rares déjà vus ne résout pas les signes absents de l’ajustement.

Parmi les cinq lectures de transfert autorisées, seuls **trois textes d’ajustement sont exacts**. `c004` remplace un `z` par `k` dans l’ajustement ; `c016` remplace deux `z` par `j`. Ces erreurs n’apparaissent pas dans leurs transferts. Sur les six grammaires uniques de substitution simple, quatre ajustements sont exacts, en comptant `c028` dont le transfert est refusé.

**Aucune des cinq lectures autorisées ne possède une clé complète de 26 lettres identifiée.** Elles couvrent respectivement 23, 22, 23, 21 et 21 lettres observées, dont 22, 22, 22, 21 et 21 correctement associées. Les lettres non observées restent non identifiées ; le statut « incomplet » n’efface pas les deux erreurs d’association observées. Un transfert exact ne prouve ni un ajustement exact ni une clé complète.

## Suppressions erronées, faux positifs et coût de l’abstention

Les contrôles sans signe nul comprennent les six substitutions littéraires simples et huit adversaires, soit **14 cas**, 14 000 mots et 85 031 lettres d’ajustement, puis 5 600 mots et 34 113 lettres de transfert. Dans leurs sorties autorisées, aucune vraie lettre n’est supprimée. Toutefois, seuls cinq cas donnent une sortie ; **neuf sur quatorze s’abstiennent ou restent ambigus**. Les cinq sorties autorisées n’effectuent aucune suppression, même correcte. Ce résultat ne valide donc pas encore une procédure capable de supprimer avec succès de vrais marqueurs sur de nouveaux textes.

Six adversaires nouveaux comportent des branches alternatives qui effaceraient de vraies lettres : quatre à finale constante, deux à couples internes. Elles restent archivées et non choisies. Les deux adversaires à finale partielle s’abstiennent avant recherche de clé. Une absence de suppression dans la sortie ne signifie pas qu’aucune branche dangereuse n’a été envisagée.

Les **12 encodages hors modèle s’abstiennent tous** : six sont hors inventaire, six déclenchent l’alerte de finale partielle. Il y a zéro acceptation erronée sur ces douze cas. Ce sont deux mécanismes construits, pas une mesure générale du rejet de tout chiffre inconnu.

Les quatre témoins de Markov restent ambigus ; chacun possède une branche retrouvant exactement la suite générée. Cela ne fournit pas une preuve de message intentionnel. Les deux adversaires à couples internes possèdent les bonnes unités parmi les alternatives, mais aucune branche ne retrouve leur transfert exact : préserver les unités ne garantit pas la clé.

| Critère figé | Résultat | Décision |
|---|---|---|
| 24/24 positifs : unités exactes et transfert unique exact | 5/24 | **Échec** |
| Zéro suppression de vraie lettre dans les 14 cas sans signe nul | Zéro, avec neuf cas sans lecture autorisée | Passe, portée limitée |
| Abstention sur les 12 encodages hors modèle | 12/12 | Passe |
| Tous les critères ensemble | Le critère de récupération échoue | **Aucun transfert au Voynich** |

Les 22/24 de phase 28 et les 5/24 présents ne sont pas une comparaison avant/après sur les mêmes passages : les textes de validation et la politique de sélection diffèrent. On ne présente pas la baisse de sorties comme un gain de déchiffrement.

## Vérifications et arrêt

La vérification indépendante contrôle 104 inversions et leurs alignements, les 92 objectifs de recherche (écart maximal `4,42 × 10⁻⁹`), les distances d’édition, 158 240 positions supprimées dans les branches, les dénominateurs et les intervalles sources. Les 413 910 lettres ainsi vérifiées incluent les variantes dépendantes et les régressions : elles ne sont pas autant de lettres littéraires uniques. Les fichiers gelés et les inventaires des phases 20–28 et de l’atlas sont vérifiés. [Vérification](results/verification.json), [préservation](results/preservation.json).

Le replay complet reconstruit **422 fichiers identiques à l’octet** dans une copie isolée. Son contrôle d’accès Python interdit au processus d’ajustement de lire les nouveaux auteurs, les réponses, les clés ou les régressions. Le solveur C++ reçoit les seuls modèles linguistiques et chiffrés ; ses lectures sont contrôlées par inspection du code et de ses arguments, pas par cette instrumentation Python. Ce dispositif vérifie la séparation logicielle ; ce n’est ni une isolation OS ni un aveugle humain. [Replay](results/replay.json), [audit des lectures](../docs/PIECES_REFERENCES.md#piece-1cee838e19d0e6).

Les diagnostics, rapports et vérificateurs ajoutés après les résultats ne changent aucune règle gelée. Aucun seuil assoupli, nouvelle tentative de clé, correction manuelle ou sélection favorable n’a été exécuté. Aucune validation historique ou linguistique extérieure n’a eu lieu. Les réserves manuscrites déjà vues restent exposées.

Les deux textes normalisés sont également reproduits à l’octet près depuis les sources brutes incluses, en rejouant la préparation de phase28 et son ancien auxiliaire de normalisation. Cela confirme la préparation reproductible, pas la justesse éditoriale de chaque caractère. [Contrôle des sources](../docs/PIECES_REFERENCES.md#piece-24cc4ccd743204).

La suite utile serait de tester une information supplémentaire indépendante qui permette de départager les unités sans connaître la réponse. Accumuler davantage de lectures possibles ou choisir la plus agréable ne résoudrait pas le problème démontré ici. Cette nouvelle piste n’est pas exécutée dans la phase 29.
