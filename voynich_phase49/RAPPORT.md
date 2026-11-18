# Phase 49 — Recherche de clés avec le moteur CTTS

17 novembre 2026 — **Aucune traduction du Voynich validée.**

Le moteur CTTS retrouve exactement les huit clés observées de nos contrôles latins et italiens : 16 000 lettres d'ajustement et 8 000 lettres réservées sont récupérées sans erreur. Son application exploratoire au Voynich ne fournit cependant aucun candidat franchissant le critère de compatibilité fixé avant ce second calcul. Les huit clés proposées, leurs sorties et les comparateurs sont conservés intégralement, sans traduction ajoutée.

## Ce qui a été exécuté

Nous utilisons le cœur Java de [CTTS, George Lasry et l'équipe CrypTool](https://github.com/CrypToolProject/CTTS/tree/d8b7d77b4e12e7a22d3980f8b5fb4e44c773287b), version `d8b7d77b4e12e7a22d3980f8b5fb4e44c773287b`. Cette version cherche des substitutions homophoniques de lettres : plusieurs signes peuvent représenter une même lettre. Elle ne met pas en œuvre ici le solveur syllabique de Lasry (2024), dont le texte intégral officiel n'a pas pu être téléchargé dans cette session. Les phases4–6 utilisaient d'autres programmes ; cet essai ne reprend pas leurs sorties comme résultats CTTS.

Les fonctions de score, d'acceptation et de déplacement de clé viennent du code publié. Une [instrumentation explicitement diffée](../docs/PIECES_REFERENCES.md#piece-f474c9cf5d70e0) fixe les graines, borne les redémarrages, conserve la meilleure clé même lorsqu'elle apparaît à l'initialisation et compte les évaluations. Un lanceur sans interface appelle le moteur dans une JVM distincte par cas. Il reproduit la préparation des indices et des capacités du pilote d'origine. Ce n'est ni une reproduction de l'interface complète, ni une nouvelle résolution des documents historiques étudiés par les auteurs.

Paramètres : groupes de cinq lettres, six redémarrages, 250 tours par redémarrage, température maximale100000, aucune correspondance initiale imposée. Deux processus au maximum tournent en parallèle. Les fichiers de vérité sont réservés à l'évaluation ; le programme Java reçoit le chiffré et la référence linguistique. Le lanceur Python lit leurs empreintes pour l'intégrité : cette séparation fonctionnelle n'est pas un cloisonnement des droits d'accès.

## Étape 1 — Clés inconnues et transfert réel

Les références livrées par CTTS sont normalisées par ses propres fonctions. Le fichier latin commence par les *Confessiones* d'Augustin ; le fichier italien contient un corpus de correspondance. Les contrôles utilisent Pline et le *Paradiso* de Dante, hérités des sources du projet. Aucune suite de 80 caractères des passages de contrôle ne figure dans les références normalisées ; les ressemblances plus courtes ne sont pas exclues.

Les huit essais combinent deux langues, des ajustements de 1 000 ou 3 000 lettres et deux familles de capacités homophoniques. Chaque clé est appliquée sans retouche à 1 000 autres lettres, après un intervalle de 250 lettres. Les passages d'une même œuvre sont disjoints. Le projet avait déjà consulté ces œuvres ; elles ne sont pas inconnues de l'analyste.

| Famille | Cas | Lettres d'ajustement exactes | Lettres réservées exactes |
|---|---:|---:|---:|
| Substitution simple, latin | 2 | 4000/4000 | 2000/2000 |
| Homophonie, latin | 2 | 4000/4000 | 2000/2000 |
| Substitution simple, italien | 2 | 4000/4000 | 2000/2000 |
| Homophonie, italien | 2 | 4000/4000 | 2000/2000 |

Les **268 correspondances observées** sont exactes. Deux signes secrets absents restent non évalués dans chacun des cas italiens. Les lettres sont évaluées après normalisation : substitutions graphiques et suppression des doubles dans les mots. Les espaces et l'orthographe originale ne sont pas récupérés par cet essai.

Le générateur respecte les capacités non uniformes que CTTS attribue aux lettres d'après la référence. La langue et cette famille de capacités sont donc fournies ; il ne s'agit pas d'un test de langue inconnue ou de tout système de chiffrement. Le seuil fixé était 95 % des lettres dans chaque ajustement et chaque transfert. Les huit cas le franchissent. [Protocole initial](PROTOCOL.json), [évaluation complète](results/EVALUATION.json), [vérification indépendante](results/INDEPENDENT_VERIFICATION.json).

## Étape 2 — Essai sur le Voynich

Après cette réussite, un second protocole a été figé avant toute recherche sur le manuscrit. Nous avons choisi deux groupes selon les attributions présentes dans ZL : Currier A/main 1 et Currier B/main 2. Pour chacun, nous conservons deux hypothèses graphiques : caractères EVA séparés, ou regroupements `cth`, `ckh`, `cph`, `cfh`, `ch`, `sh` à l'intérieur des mots transcrits. Ces conventions ne sont pas déclarées phonétiques.

Les lignes de prose incertaines ou interrompues sont entièrement exclues. Les deux faces et les panneaux d'un même feuillet physique appartiennent à la même partition, déterminée par son numéro haché. Nous retenons les premières lignes complètes fournissant au moins 3 000 unités pour l'ajustement et 1 000 pour le transfert. Les quatre sélections ne sont pas indépendantes et ces pages ont été vues dans des phases antérieures. L'alphabet utilisé pour nommer les identifiants comprend l'union ajustement/réserves : la réserve n'est donc pas cachée quant à cet alphabet. Ses fréquences et ses scores ne servent pas à choisir la clé.

Une clé est cherchée pour chaque groupe, chaque représentation et chaque référence linguistique : **huit candidats**. Les mêmes paramètres sont appliqués à **huit comparateurs**, issus de quatre paires de chaînes générées sans texte clair cible. Leur générateur de transitions d'ordre 2 apprend uniquement sur les unités d'ajustement du manuscrit, avec redémarrage en cas d'impasse. Il ne prétend pas expliquer la fabrication historique du Voynich.

Chaque clé réelle reste ensuite fixe sur la réserve ZL et les loci disponibles dans IT. Quatre lignes de la réserveA manquent ou sont incertaines dans IT ; elles sont signalées, pas remplacées. Les variantes des phases antérieures restent conservées ; aucun signe ambigu n'est choisi pour améliorer une lecture.

Le filtre exploratoire exige une couverture d'au moins 95 %, un score sur la réserve au moins égal au minimum des contrôles correctement décodés dans la langue concernée, et un score supérieur au comparateur généré. **Ce filtre mesure une compatibilité avec les références, sans test de signification ni valeur de probabilité.**

| Groupe / unités | Référence | Score Voynich réservé, millions | Comparateur généré, millions | Plancher de calibration, millions |
|---|---|---:|---:|---:|
| A1 / EVA | Latin | 6,637 | 9,572 | 12,110 |
| A1 / EVA | Italien | 7,260 | 7,662 | 13,207 |
| A1 / regroupements | Latin | 7,061 | 8,024 | 12,110 |
| A1 / regroupements | Italien | 6,605 | 7,490 | 13,207 |
| B2 / EVA | Latin | 7,693 | 7,329 | 12,110 |
| B2 / EVA | Italien | 7,404 | 7,281 | 13,207 |
| B2 / regroupements | Latin | 7,051 | 7,486 | 12,110 |
| B2 / regroupements | Italien | 7,903 | 7,353 | 13,207 |

La couverture des unités réservées est 100 % dans ces essais, mais **0/8 candidat passe le filtre**. Trois dépassent leur comparateur généré ; aucun n'atteint le plancher de calibration. Une seule génération par sélection ne permet pas une estimation statistique des faux positifs. Les scores latins et italiens ne doivent pas être comparés comme une identification de langue.

Avec les mêmes clés, les scores sur les passages IT restent entre 6,836 et 7,779 millions. L'autre transcription ne fournit donc pas ici une confirmation de lecture. Toutes les sorties restent des suites de lettres candidates, sans insertion de mots ou paraphrase. [Protocole de transfert](MANUSCRIPT_PROTOCOL.json), [sélection](../docs/PIECES_REFERENCES.md#piece-4746e034b4a0ca), [clés et sorties](results/MANUSCRIPT_OUTPUTS.json), [résumé](results/MANUSCRIPT_SUMMARY.json).

## Vérification, portée et suite

Les sources, données et programmes ont été figés avant chaque étape. Une correction de lecture du statut du vérificateur, effectuée avant la création de tout processus d'optimisation du manuscrit, est conservée dans [la note de démarrage](STARTUP_CORRECTION.md). Elle n'a modifié ni les critères ni les données.

Un second programme a reconstruit les normalisations, les huit clés secrètes et les chiffres, puis recalculé les exactitudes et les scores. Des vérifications distinctes contrôlent [la sélection et les générations](results/SELECTION_VERIFICATION.json) et [les calculs du transfert](results/MANUSCRIPT_VERIFICATION.json). La reproduction conserve les mêmes clés et sorties pour les 24 recherches. Voir [reproduction](REPRODUCTION.md) et [attributions](NOTICE.md).

Cette phase établit une capacité de récupération de clés dans le cadre calibré, puis son absence de candidat satisfaisant dans l'essai Voynich défini. Elle ne prouve pas l'impossibilité d'une autre clé, d'un autre découpage des signes, d'une autre langue ou d'un autre mécanisme. Elle n'établit pas non plus que le manuscrit serait dépourvu de message. La recherche de sens reste ouverte ; les sorties présentes ne constituent pas une traduction.
