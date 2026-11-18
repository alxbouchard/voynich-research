# Phase 28 — décoder avec des signes ajoutés ou des lettres à plusieurs signes

**22 contrôles positifs sur 24 retrouvent exactement le passage de transfert. Le critère fixé exigeait 24/24 : calibration non validée. Aucune application au Voynich. `NOT_TRANSLATION`.**

Le résultat positif est une capacité limitée : retrouver certains textes connus, artificiellement chiffrés, sans fournir leur clé au solveur. Le résultat négatif indique précisément où cette capacité se dégrade. Il ne renseigne pas directement sur la langue ou le sens du manuscrit.

[Résultats des quatre familles](../docs/PIECES_REFERENCES.md#piece-45f4f3c3a0c682)

## Dispositif réellement testé

La phase 27 avait montré que l’ajout réversible d’un signe pouvait sortir un message réel de la famille de substitutions étudiée. Ici, nous testons la récupération du texte lui-même. Le protocole, le code expérimental, les sources et leur normalisation ont été figés au commit `55a4637`, avant génération et mesure ; [empreintes du gel](FREEZE.json). Il s’agit d’un gel local, pas d’un préenregistrement externe.

Deux nouveaux auteurs servent de contrôles : [Apulée, *Métamorphoses*, texte latin Perseus à révision fixée](https://github.com/PerseusDL/canonical-latinLit/blob/8b536bdf3ed1f43494055efe112433b4a58eab67/data/phi1212/phi002/phi1212.phi002.perseus-lat1.xml), et [Manzoni, *I promessi sposi*, édition italienne](https://www.gutenberg.org/ebooks/45334). Les modèles de langue restent ceux de César et de Dante déjà archivés. Le changement d’auteur, d’époque et de genre est une limite de représentativité, pas une démonstration de robustesse générale.

Par auteur, trois passages d’ajustement de 1 000 mots commencent aux indices 0, 4 000 et 8 000 du texte normalisé. Chaque passage de transfert contient 400 mots, après une marge de 100 mots. Les douze intervalles sont disjoints au sein de leur source. Cela donne six paires de passages, soit 6 000 mots d’ajustement et 2 400 mots de transfert uniques, comprenant 12 903 lettres de transfert. Les quatre encodages réutilisent ces mêmes paires : **24 variantes chiffrées ne constituent pas 24 messages indépendants**.

La langue correcte et les espaces normalisés sont fournis. Accents et ponctuation sont normalisés, les apostrophes séparent des tokens ; aucun découpage inconnu n’est résolu ici. Cette phase ne corrige donc pas l’échec de segmentation des phases 20–22.

Les quatre encodages sont : substitution simple ; ajout d’un signe dédié à la fin de chaque mot ; ajout d’un même signe après un sous-ensemble fixe de douze lettres ; combinaison des deux ajouts. Les signes ajoutés sont distincts des signes de base. Cette famille est beaucoup plus étroite qu’un chiffre multigraphique arbitraire.

La détection cherche une finale dédiée et des couples « signe de base + marqueur ». Elle retient l’hypothèse unique comportant le plus de mécanismes d’ajout, avec les supports fixés dans le [protocole](PROTOCOL.json). Ce choix est une hypothèse explicite ; il ne prouve pas qu’une lettre doit être supprimée. Le solveur C++ de phase 18, conservé à l’octet près, cherche ensuite une substitution sur huit départs de 60 000 étapes. Toutes les règles et clés sont fixées avant d’ouvrir les passages de transfert ; aucune retouche n’est faite ensuite.

## Résultats de transfert

| Encodage | Latin | Italien | Total exact |
|---|---:|---:|---:|
| Substitution simple | 3/3 | 3/3 | 6/6 |
| Signe final ajouté | 3/3 | 3/3 | 6/6 |
| Certaines lettres à deux signes | 2/3 | 3/3 | 5/6 |
| Combinaison | 2/3 | 3/3 | 5/6 |
| Total des variantes | 10/12 | 12/12 | **22/24** |

« Exact » exige ici les vraies unités, les bons rôles des marqueurs et toutes les lettres du transfert, avec ses espaces connus. Les six substitutions simples conservent les caractères authentiques. Aucun seuil moins strict n’a remplacé le critère principal après observation des résultats. Les 36 cas, leurs états et mesures figurent dans [RESULTATS.csv](results/RESULTATS.csv) et [SUMMARY.json](results/SUMMARY.json).

Le texte d’ajustement, critère secondaire, est entièrement exact dans 20/24 variantes. Deux contrôles qui réussissent le transfert (`c010`, `c011`) remplacent néanmoins l’unique `z` d’ajustement par `w` ou `j`. Ce `z` n’apparaît pas dans leur transfert. **Un transfert exact ne garantit donc pas que toute la clé soit retrouvée.** Le critère principal, fixé avant les résultats, exigeait les unités exactes sur les deux passages et le texte exact sur le transfert, pas la totalité du texte d’ajustement.

Les deux échecs, `c012` et `c013`, correspondent au même troisième passage latin. Une lettre `z` apparaît une seule fois dans l’ajustement ; elle fait partie des lettres encodées sur deux signes. La règle exige au moins cinq occurrences de chaque prédécesseur admis. Elle exclut donc ce prédécesseur, puis rejette le marqueur parce qu’une de ses occurrences reste inexpliquée. Le système retombe sur une interprétation erronée à un signe par lettre, au lieu de s’abstenir. C’est un diagnostic du code et des comptages existants, **sans essai d’un nouveau seuil**.

Sur ces deux transferts, la fidélité par distance d’édition est respectivement **44,00 % et 31,02 %** : il ne s’agit pas d’une seule lettre de sortie mal récupérée. La distance est calculée à l’intérieur de chaque mot, les espaces étant connus, puis normalisée par le plus grand total de caractères. Le refus du bon modèle d’unités perturbe l’ensemble de la substitution. [Diagnostic détaillé](results/DIAGNOSTIC.json).

## Ce que montrent les douze cas difficiles

**Six chiffres réversibles plus généraux : six abstentions.** Chaque lettre possède un deuxième signe distinct, sans marqueur partagé. Ils sortent de la grammaire et de l’inventaire pris en charge. Ce résultat limite la portée de la méthode ; il ne signifie pas que ces messages sont indéchiffrables.

**Quatre textes générés sans passage littéraire cible : quatre récupérations exactes.** Un modèle de Markov utilise les statistiques des anciennes références, puis le texte produit est chiffré avec les deux types d’ajout. Le décodeur peut retrouver cette suite générée aussi bien qu’un passage d’auteur. C’est une récupération algébrique réelle, mais pas une preuve d’intention sémantique. Ces générateurs héritent de régularités linguistiques et peuvent produire de vrais mots ; « sans passage cible » ne veut pas dire « aucune structure ou aucun mot ayant un sens ».

**Deux adversaires à vraie finale : deux suppressions erronées.** Les tokens sont tirés des références normalisées avec exactement un `a`, placé à la fin. Ils sont chiffrés par substitution simple : aucun signe muet n’est ajouté. Pourtant, le système retire cette vraie lettre dans les deux cas, soit **800 lettres finales effacées sur les 800 mots de transfert**. Le latin `lingua`, par exemple, devient `lingu`. Les distances totales sont 400 éditions en latin et 412 en italien ; les douze éditions italiennes supplémentaires concernent d’autres erreurs de lettre. Les 2 000 mots d’ajustement adversariaux perdent également leur finale.

Une même distribution visible peut donc recevoir une interprétation « vraie lettre finale » ou « signe nul ». La préférence actuelle pour davantage de marqueurs ne suffit pas à trancher. Même un succès de 24/24 sur les contrôles positifs n’aurait pas justifié une suppression automatique de signes du Voynich.

## Vérification et limites de preuve

Les 80 allers-retours mécaniques sur données artificielles passent. La vérification séparée contrôle 72 inversions des 36 chiffres (ajustement et transfert), les douze plages sources, les sorties des règles et les distances. Les 30 objectifs effectivement optimisés sont recalculés directement ; l’écart maximal vaut `3,64 × 10⁻⁹`. Le replay complet régénère **257 fichiers identiques à l’octet**, y compris les deux échecs. [Vérification](results/verification.json) ; [replay](results/replay.json).

Les clés de génération et les réponses sont stockées dans `sealed/`, séparément de `inputs/`. Le solveur C++ reçoit seulement le chiffré d’ajustement et les modèles de référence ; son score ne consulte pas la vérité. **Il s’agit d’une séparation logicielle, pas d’un aveugle humain ni d’un isolement du système de fichiers.** Le vérificateur d’empreintes commun lit aussi les sources claires archivées pour calculer leurs SHA-256. L’opérateur peut consulter tous les fichiers. Cette limite précise la formulation « clés inconnues » : elles ne sont pas données à l’algorithme d’ajustement.

Les anciennes phases et l’atlas sont vérifiés sans modification. Aucune nouvelle clé Voynich, aucun texte Voynich décodé, aucune inspection supplémentaire des dessins et aucune identification de langue ne sont produits. Les contrôles logiciels ne remplacent pas une validation historique ou linguistique indépendante.

La prochaine correction à tester devrait traiter les événements rares sans sélectionner silencieusement une mauvaise famille, et conserver l’ambiguïté lorsqu’une vraie lettre peut être prise pour un signe nul. Elle devra être évaluée sur d’autres intervalles réservés avant de considérer le manuscrit. Cette correction n’est pas exécutée ni validée dans la présente phase.
