# Phase 30 — Quels indices permettent de retrouver une règle de lecture ?

**31 octobre 2026 — NOT_TRANSLATION.** Le solveur retrouve les 20 règles complètes et les 20 passages réservés des contrôles admissibles lorsqu’on lui fournit 26 mots clairs correctement alignés, puis neuf mots de vérification séparés. Aucun indice et les seuls regroupements de signes ne permettent aucune lecture unique. Tous les indices trompeurs testés sont refusés avant autorisation d’une lecture. Cette réussite est conditionnelle à des informations dont nous ne disposons pas encore pour le Voynich.

[Résultats des conditions](../docs/PIECES_REFERENCES.md#piece-bcb8beb7aa1b70)

## Ce que l’essai change

La phase 29 conservait plusieurs interprétations incompatibles des signes ajoutés et des groupes représentant une lettre. Ici, aucune langue ni vraisemblance lexicale ne départage les solutions. Un solveur d’équations cherche exactement les correspondances compatibles avec les indices fournis. Il faut une règle unique, un témoin indépendant réussi, puis un transfert exact sans retouche. La présence de la bonne réponse parmi plusieurs branches ne compte jamais comme récupération.

Le modèle testé associe à chaque lettre a–z un groupe fixe de un à trois signes. Ces groupes sont injectifs et aucun n’est le préfixe d’un autre. Un ajout constant de zéro à deux signes peut terminer chaque mot ; l’ordre de tout le mot peut être inversé. Le solveur ignore les groupes, l’ajout, le sens et la clé. **Les espaces sont fournis** : ce banc ne résout pas la segmentation des mots sans espaces ni l’ensemble des encodages possibles du manuscrit.

Le [protocole](PROTOCOL.json), les sources, les graines, le code et les critères ont été gelés dans le commit `eecd4333397cdacf21259ce01a1b981f036df267`, avant génération des nouveaux contrôles. Quatre jouets de développement et quatre anciennes régressions sont déclarés séparément. Aucun réglage n’a été changé après mesure. Il s’agit d’un gel local, pas d’une préinscription externe ou d’un aveugle humain.

## Nouveaux textes, variantes et information fournie

Les sources sont *Pinocchio* de Collodi, en italien, et *Candide* de Voltaire, en français, dans les fichiers archivés de Project Gutenberg ([Collodi](https://www.gutenberg.org/ebooks/52484), [Voltaire](https://www.gutenberg.org/ebooks/4650)). Les originaux et leurs notices sont conservés. La préparation normalise en a–z et sépare la ponctuation ; elle ne prétend pas représenter une langue médiévale.

Deux paires de passages par auteur fournissent chacune 500 mots d’ajustement et 200 mots de transfert, séparés par 100 mots. Les huit intervalles littéraires et les références des générateurs sont disjoints dans chaque source. Les variantes réutilisent ces **quatre paires**, donc leurs résultats ne sont pas des observations indépendantes.

| Ensemble nouveau | Cas | Construction |
|---|---:|---|
| Positifs ordinaires | 16 | Quatre paires × digrammes arbitraires, groupes variables, ajout final, ajout et inversion |
| Positifs à vraie finale | 4 | Un véritable `a` ajouté au texte clair de chaque mot, sans signe nul |
| Hors modèle | 8 | Alternance homophonique ou groupes de quatre signes |
| Générés sans passage cible | 2 | Mots construits par transitions de lettres et longueurs échantillonnées, puis chiffrés |
| Anciennes régressions, hors dénominateurs nouveaux | 4 | Cas exposés de phase 28, chiffrés et textes conservés à l’identique |

Chaque cas reçoit onze conditions, soit **330 mesures nouvelles et 44 de régression**. Les indices de groupes donnent les véritables limites des codes pour tous les mots d’ajustement, sans identifier les lettres ni désigner l’ajout final. C’est une information synthétique bien plus forte qu’une ligature visible sur une image.

Les mots alignés proviennent d’une liste moderne fixe, l’alphabet phonétique de l’[OTAN](https://www.nato.int/en/about-us/nato-history/history-by-theme/symbols-of-nato/nato-phonetic-alphabet), choisie indépendamment des messages et des clés. Cette liste n’est jamais proposée comme vocabulaire du Voynich.

| Dose d’ajustement | Caractères clairs | Lettres distinctes |
|---|---:|---:|
| 1 mot | 4 | 3 |
| 4 mots | 21 | 13 |
| 12 mots | 61 | 20 |
| 26 mots | 138 | 26 |

Les quatre adversaires à vraie finale ajoutent aussi `a` à chacun des mots indices et témoins. Les comptes de caractères y augmentent donc du nombre de mots. Le témoin séparé est un pangramme de neuf mots, 35 lettres couvrant les 26 lettres, ou 44 lettres dans ces adversaires. Il n’entre jamais dans l’ajustement ou le choix d’une branche. **Le niveau riche utilise 35 mots connus au total : 26 pour ajuster et neuf pour vérifier.** Les doses testées ne prouvent ni un minimum universel ni que 26 mots quelconques suffiraient.

## Résultats complets sur les 30 cas nouveaux

| Condition | Lecture autorisée exacte | Ambiguïté | Incompatibilité | Rejet par le témoin |
|---|---:|---:|---:|---:|
| Aucun indice | 0 | 30 | 0 | 0 |
| Groupes corrects sans lettres | 0 | 22 | 8 | 0 |
| Un groupement altéré | 0 | 0 | 30 | 0 |
| Groupements bruités, échantillon de 10 % | 0 | 0 | 30 | 0 |
| 1 mot aligné | 0 | 18 | 6 | 6 |
| 4 mots alignés | 0 | 19 | 8 | 3 |
| 12 mots alignés | 0 | 8 | 8 | 14 |
| 26 mots alignés corrects | 22 | 0 | 8 | 0 |
| Deux partenaires chiffrés échangés | 0 | 0 | 30 | 0 |
| Un signe altéré dans le dernier mot indice | 0 | 0 | 18 | 12 |
| `a/e` échangés dans tous les mots clairs indices | 0 | 0 | 8 | 22 |

Les 22 lectures sont les **20 positifs** et les **deux textes générés**. Pour les positifs, les 10 000 mots d’ajustement / 45 930 lettres et les 4 000 mots de transfert / 18 840 lettres sont exacts, avec leurs unités et toute la clé de 26 lettres, l’ajout et le sens. Ces comptes comprennent les variantes dépendantes. Aucun caractère du passage réservé n’a servi à choisir une règle.

Les 12 positifs sans signe nul réussissent tous, y compris les quatre adversaires à véritable finale. Aucun signe nécessaire au texte clair n’est effacé. Les 800 `a` ajoutés aux transferts et les 2 000 ajoutés aux ajustements sont conservés. Les huit cas hors modèle ne produisent aucune lecture dans les onze conditions.

Le bruit de groupement vise 50 mots par nouveau cas : 28 cas changent effectivement 50 mots, un en change 49 et un 48, les groupes indivisibles ne pouvant être altérés. Les indices de ces mots sont archivés dans chaque vérité constructeur.

Les indices faux sont essentiels : les 22 substitutions cohérentes de `a/e`, et 12 des 30 altérations d’un signe, produisent une règle unique mais fausse. Les 34 sont rejetées par le témoin. La seule cohérence interne ne suffit donc pas. Sur les faibles doses, 21 des 23 règles uniques partielles ont les correspondances couvertes correctes et deux sont erronées ; aucune n’a la couverture nécessaire pour réussir le témoin. Le champ `unique_rule_correct_before_witness` du CSV teste la **clé complète** : `false` peut aussi signifier « incomplète ». Le détail des correspondances couvertes figure dans [verification.json](results/verification.json).

Les générateurs n’ont pas de passage littéraire cible, mais leurs chaînes chiffrées sont récupérables avec une clé déterminée par des indices externes. Leur succès ne démontre aucune intention sémantique. Les quatre régressions exposées réussissent à la dose 26 avec leur témoin, séparément ; les indices y sont simulés à partir de clés déjà connues du constructeur. Elles n’ajoutent aucune validation nouvelle.

## Vérification et limites

Les cinq critères informatiques gelés passent : récupération 20/20, zéro fausse lecture parmi 330 mesures nouvelles, abstention dans les 150 conditions à indices corrompus, abstention hors modèle, zéro suppression erronée. Aucun dépassement du plafond de deux millions de nœuds n’intervient. Un plafond atteint aurait imposé l’abstention.

Avant génération, 32 comparaisons sur petits alphabets avec énumération indépendante et quatre inversions à alphabet complet vérifient le moteur. Après mesure, une autre implémentation vérifie 68 constructions, 319 modèles retenus, 374 dossiers et 52 inversions de passages autorisés, régressions comprises. Les deux préparations de sources et 56 intervalles littéraires sont relus. Le [replay](results/replay.json) reproduit 1 365 fichiers à l’octet. Une garde Python bloque les réponses, sources, témoins et passages de transfert pendant l’ajustement : zéro tentative interdite sur 794 chemins ouverts, lectures et écritures comprises. Ce n’est pas un isolement OS, une seconde équipe ni une validation historique.

La famille est volontairement étroite : espaces connus, alphabet clair a–z, correspondances préfixes libres, indices exacts fabriqués avec le constructeur, témoin couvrant tout l’alphabet. Les corruptions et encodages hors modèle ne couvrent pas toutes les erreurs possibles. Nous n’avons pas montré qu’une règle résiste à un témoin lui-même faux et cohérent avec de faux indices. La vérité des indices historiques doit être justifiée autrement que par la réussite de notre programme.

## Conséquence pour le manuscrit

L’information utile démontrée est une **correspondance claire–chiffrée authentifiée**, avec assez de contraintes pour une règle unique et un témoin séparé. La relecture des groupes seule laisse les lettres permutables. Le registre établi avant l’essai compte zéro correspondance historique admissible et aucun témoin indépendant. Le critère d’application au Voynich reste donc non satisfait, malgré la réussite informatique.

La [mini-édition critique proposée](critical_edition/EDITION_CRITIQUE.md) conserve les lectures concurrentes de f1r et f116v, et la distinction entre l’annotation ordinaire de f70v2 et un éventuel mot chiffré. Elle fournit les images, les prédictions conditionnelles et une fiche vierge de relecture. Aucun mot du manuscrit n’y est supposé traduit ; aucune confirmation humaine indépendante n’a eu lieu. Aucune recherche de clé Voynich n’a été lancée, aucun passage n’est présenté comme nouvellement aveugle.

Pour franchir ce blocage, il faut une preuve documentaire du lien entre un segment précis du manuscrit et un texte connu, puis un second lien qui ne sert pas à construire la règle. Les anciens mois ou alphabets marginaux ne deviennent pas de telles preuves par leur seule proximité graphique. Le prochain essai réel devra fixer les lectures concurrentes et des passages distincts avant mesure, puis publier aussi les contradictions et abstentions.
