# Bilan des expériences

**Aucune traduction validée.** Ce tableau résume les rapports archivés. Il ne constitue pas une nouvelle réplication des expériences.

| Phase | Question et travail exécuté | Résultat principal | Limite ou correction |
|---|---|---|---|
| 1 | Vérifier les transcriptions et une démonstration antérieure ; structure du texte ; contrôle Naibbe. | Le mot `qokeedy` est absent de f1r dans ZL et IT, contrairement à l'extrait de démonstration. Un contrôle Naibbe restitue 52 641 lettres à clé connue. | La démonstration initiale ne porte pas sur le texte annoncé. Une récupération à clé connue ne résout pas une clé inconnue. |
| 2 | Substitutions simples, deux langues, 30 configurations ; inventaire des légendes. | Contrôle latin : 28 639/28 641 lettres ; italien : 109 933/109 933. 729 loci de légendes inventoriés. | Aucune lecture du manuscrit ; sélection de variantes exploratoire. |
| 3 | Pilote de transcription et comparaison sur 12 pages. | 384 loci comparés, huit zones d'image examinées avec les transcriptions. | Relecture non aveugle par l'assistant ; `okols` dépend d'une séparation incertaine. |
| 4 | Substitution homophonique fixe, 16 configurations et 16 mélanges. | Contrôles : 96,784 % en latin, 100 % en italien. | Une sortie latine erronée obtient un meilleur score que le texte exact. Le score ne certifie pas la lecture. |
| 5 | Unités d'une ou deux lettres, quatre inventaires CV/VC. | Huit contrôles et 64 essais réels/témoins ; les 32 clés Voynich retenues violent au moins une contrainte de redécoupage réservé. | Inventaires orthographiques restreints, pas syllabification historique complète. |
| 6 | Corriger la contrainte de découpage ; analyser les voisinages. | 80 exécutions nouvelles. Contrôles latins >99,85 %, italiens 100 %. 14/32 sorties Voynich respectent aussi le découpage réservé. | La conformité au modèle ne donne pas de sens. Dépendances locales compatibles avec plusieurs mécanismes. |
| 7 | Prédire les espaces nets hors cahier ; regroupements sans espaces. | F1 : 0,900 ZL et 0,893 IT. BPE64 traverse 19,88 % des espaces incertains ZL contre 2,52 % des nets. | Bonne prédiction graphique également possible sur un chiffre et un générateur sans message. |
| 8 | Transférer le modèle aux espaces incertains ; vérifier des images. | 716/1 089 accords avec IT, contre 700 pour « toujours séparer ». | Les scores extrêmes ne sont pas des probabilités fiables de lecture correcte. Aucune correction automatique. |
| 9 | Prédire l'initiale suivante à partir de la finale précédente. | Gain du modèle partagé : 0,082 à 0,202 bit par cible selon transcription et groupe. | Deuxième modèle ajouté après diagnostic ; gain prédictif, sans phonétique ou sens. |
| 10 | Deux alphabets, changement à l'initiale après EVA `y`. | Modèle restreint final : 99,986 à 100 % des lettres des huit contrôles. Aucun déchiffrement Voynich. | Les premiers modèles échouent à la calibration ; ils restent archivés. Le modèle final exclut homophonie et changements de segmentation. |
| 11 | Exécuter et auditer deux décodeurs publics, Scott Schechter et ZFD. | Couvertures et plusieurs scores restent identiques après permutations des sens. | Ces métriques ne valident pas les significations. Le test ne réfute pas tous les arguments historiques des auteurs. |
| 12 | Propager les règles de suppression de Scott depuis 18 mots ; contrôler des formes latines. | 15,97 % à 18,85 % de couverture selon variante. 95 lectures changent lorsque la suppression précède le glossaire. | Les 18 sens de départ ne sont pas confirmés. Le test n'implémente pas tout le système. |
| 13 | Adapter CSA_OptMatcher et tester l'appariement lexical. | 64/64 mots réservés pour substitution simple et signe muet ; clés Voynich instables dans 7/8 cas. | Lexiques et budgets restreints ; aucune segmentation phonétique conjointe. |
| 14 | Vérifier les légendes pharmaceutiques et leur rapport à la prose. | Test de correspondance locale exacte : p=0,279 ZL et 0,193 IT. | Correspondances graphiques sans sens établi ; identifications d'objets prudentes. |
| 15 | Apprendre de courtes transformations entre légendes et prose, avec feuillet exclu. | Les quatre configurations dégradent le contraste par rapport à l'identité ; 17 280 ajustements avec 720 permutations. | Six feuillets seulement. Ce résultat ne réfute pas toutes les morphologies ou tous les liens texte/image. |
| 16 | Examiner f116v, f104r et la table partielle en marge de f1r. | Une correspondance `aror/sheey` avec espace incertain apparaît hors marge. La table f1r couvre environ 40 % des occurrences retenues. | Rapprochement déjà publié ; couverture de signes, pas traduction. |
| 17 | Traiter 22 bandes de f116v ; tester le motif hypothétique `six marix morix vix`. | Ambiguïté initiale persistante. Aucun alignement bijectif ; quelques alignements homophoniques sans espaces. | Le texte supposé clair n'est pas assuré. f104r échoue à l'extension testée ; f79r ne reproduit pas tout l'agencement marginal. |

Les pourcentages de contrôles ne décrivent jamais le pourcentage de Voynich décodé.

## Ce qui reste inconnu

La langue, la fonction des unités graphiques, le statut linguistique des espaces, la présence d'un message récupérable, le mécanisme éventuel de codage et le sens des mots étudiés restent indéterminés dans ce dossier.

## Résultats de phase 17 à ne pas surinterpréter

Le test homophonique sans espaces sur ZL en EVA littéral trouve 37 fenêtres compatibles avec le motif. Des mélanges internes aux paragraphes en donnent de 2 à 10 sur 32 essais, moyenne 6,71875. Cette différence peut refléter la structure répétitive du manuscrit. Le diagnostic est ajouté après observation et n'identifie aucune valeur phonétique.

Le rapprochement historique avec `erex + arex + rymex`, étudié par Jones et Olsan, est une analogie de genre avec des charmes, pas une clé ni une attestation de la formule exacte supposée sur f116v.
