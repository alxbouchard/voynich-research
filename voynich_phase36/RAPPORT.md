# Phase 36 — Retrouver une équivalence de signes en début de ligne

**31 octobre 2026 — NOT_TRANSLATION. Expérience terminée, calibration non validée.** Une nouvelle méthode sans dictionnaire retrouve correctement une règle partielle dans **3 des 12 contrôles positifs**, contre au moins 10 requis. Elle refuse les clés changées et les préfixes trompeurs, mais s’abstient trop souvent même lorsque le mécanisme recherché est réellement présent. Elle n’est donc pas appliquée au Voynich.

## La question choisie après les phases 1–35

La [revue des conclusions et limites](REPRISE_1_35.md) écarte les reprises du glossaire central, des marginalia comme texte parallèle et des variantes zodiacales déjà testées. Aucun mot clair historique fiable n’est disponible pour contraindre une clé de traduction. L’expertise graphique humaine indépendante reste également manquante.

Nous avons donc testé une contrainte plus limitée : **le premier signe d’un mot en début de ligne pourrait être une variante régulière de son signe ordinaire**, le reste du mot restant identique. La sortie attendue serait une correspondance entre deux signes chiffrés selon leur position, sans leur attribuer de son ni de sens. Une permutation globale de l’alphabet clair resterait inconnue.

La position dans la ligne appelle des contrôles de disposition. L’analyse de [Vogt (2012)](https://voynichthoughts.wordpress.com/wp-content/uploads/2012/11/the_voynich_line.pdf) montre notamment que certains effets de longueur peuvent découler de la formation des lignes. Nous l’utilisons comme avertissement méthodologique, sans reproduire son étude ni en déduire une clé.

La méthode cherche des groupes ayant exactement la même suite après leur premier signe. Si plusieurs de ces suites relient toujours le même signe initial au même signe intérieur, elle propose une équivalence. Un passage distinct doit la soutenir avant toute prédiction sur un troisième passage. **Le risque central est que deux mots différents partagent cette même suite.** Ce risque fait partie des hypothèses concurrentes inscrites avant mesure.

## Nouveaux contrôles et critères fixés

Les textes de calibration sont nouvellement acquis pour cette phase : [Doyle, *The Adventures of Sherlock Holmes*](https://www.gutenberg.org/ebooks/1661), [Cervantes, *Don Quijote*](https://www.gutenberg.org/ebooks/2000) et [Verne, *Le tour du monde en quatre-vingts jours*](https://www.gutenberg.org/ebooks/800). Leurs langues ne sont pas proposées comme celles du Voynich. Austen a été écartée dès la revue, car utilisée en phase 24.

Pour chaque œuvre, deux ensembles de passages disjoints fournissent chacun 6 000 mots d’ajustement, 2 000 mots témoins et 4 000 mots de transfert, avec des intervalles séparateurs. Les textes sont normalisés en lettres a–z ; la ponctuation et les distinctions diacritiques sont simplifiées. Deux dispositions sont testées : huit mots par ligne et retour à la ligne à une largeur de 42 caractères, sans couper un mot.

Ces six ensembles de passages sont réutilisés entre dispositions et mécanismes. Les **60 cas ne sont donc pas 60 textes indépendants**. Les clés sont nouvelles et ne sont pas fournies aux fonctions d’inférence. Parmi les 60 cas, douze utilisent des groupes de lettres inventés et échantillonnés sans passage cible.

Le protocole, les sources et le code ont été gelés au commit `d82114ddafed97dfb725ac66c8a9d08acbcdac62`, avant de générer ces cas. Pour réussir un contrôle, il fallait au moins trois équivalences autorisées, au moins 100 mots initiaux prédits, au moins 25 % de couverture en transfert et **aucune erreur** de correspondance ou de mot normalisé. L’autorisation d’un essai Voynich exigeait notamment 10/12 réussites positives, au moins 3/4 chez chaque auteur, 10/12 réussites du contrôle d’identité et l’abstention sur tous les mécanismes trompeurs.

## Résultats

| Mécanisme construit | Cas | Règle partielle autorisée et transfert exact avec couverture suffisante | Abstentions | Erreurs dans les mots effectivement produits |
|---|---:|---:|---:|---:|
| Remplacement stable du premier signe de ligne | 12 | **3** | 9 | 0 |
| Aucun remplacement spécial : identité attendue | 12 | **3** | 9 | 0 |
| Clé initiale changée dans le témoin et le transfert | 12 | 0 | **12** | 0 |
| Signe préfixé au lieu d’un remplacement | 12 | 0 | **12** | 0 |
| Groupes inventés, sans passage cible, puis même remplacement stable | 12 | **11** | 1 | 0 |

Les réussites positives sont réparties ainsi : Doyle **0/4**, Cervantes **2/4**, Verne **1/4**. Les critères de récupération et de répartition échouent. L’absence d’erreurs dans les sorties autorisées doit être lue avec les nombreuses abstentions ; elle n’est pas une garantie générale de sûreté.

Dans les trois contrôles positifs réussis, les règles partielles contiennent respectivement cinq, sept et huit équivalences. Elles normalisent exactement **206/500**, **302/532** et **365/568** mots en début de ligne du passage de transfert, soit **873 mots** au total. Pour 768 de ces prédictions, la suite du mot ne figurait pas parmi les ancres retenues lors de l’ajustement ; cela ne signifie pas que le mot était nécessairement absent de tout le texte d’ajustement.

Cette normalisation retrouve l’écriture dans l’**alphabet chiffré ordinaire**. Elle ne retrouve pas la langue à partir du chiffré et ne constitue pas une traduction. Les réponses claires connues servent seulement à vérifier les contrôles après production des prédictions.

Les 11 réussites sur les groupes inventés démontrent également qu’une règle relative exacte peut exister sans passage linguistique cible. Réussir ce test ne prouverait donc pas, à lui seul, la présence d’un message.

## Ce qui provoque les échecs

Le diagnostic est effectué **après les résultats**, à l’aide des réponses connues des contrôles. Il ne change aucune règle.

Dans les 12 contrôles positifs, les **76 équivalences candidates obtenues à l’ajustement sont correctes** dans les alphabets de leurs cas respectifs. Mais huit témoins rejettent ensuite des règles correctes : ils construisent douze équations trompeuses à partir de mots différents ayant la même fin. Exemples vérifiés dans les passages de contrôle :

| Mot en début de ligne | Mot intérieur | Suite commune après la première lettre |
|---|---|---|
| `fellow` | `yellow` | `ellow` |
| `life` | `wife` | `ife` |
| `peine` | `veine` | `eine` |
| `pommes` | `hommes` | `ommes` |

Ces paires existent dans les contrôles littéraires ; ce ne sont pas des lectures proposées du Voynich. Le témoin prend leur fin commune pour une identité de mot et réclame alors une mauvaise équivalence initiale. Sa règle de refus conserve la prudence, mais produit un faux rejet. Le neuvième contrôle positif échoue par manque de soutien : une seule équivalence candidate est disponible.

Le [diagnostic complet](results/DIAGNOSTIC_POSTHOC.json) conserve les mots, suites chiffrées, effectifs et règles concernées. Il explique une faiblesse de **cette procédure de construction des contraintes**. Il ne réfute pas l’existence éventuelle d’allographes ou d’un mécanisme lié à la ligne dans le manuscrit.

## Vérifications et portée

Une implémentation distincte, par le même opérateur, vérifie les **720 000 occurrences de mots chiffrés** par construction et inversion, les intervalles des sources, les deux dispositions de lignes, les ancres, les décisions du témoin, les **8 145 mots initiaux effectivement produits** et les 296 équivalences autorisées sur l’ensemble des cas. Ces totaux comprennent les identités et les groupes inventés ; ils ne mesurent pas un pourcentage de Voynich décodé.

Les 60 lignes du tableau et les douze diagnostics positifs sont vérifiés séparément. Une reproduction dans un dossier neuf retrouve **663 fichiers de données et de résultats à l’octet**. Les **4 799 entrées** des inventaires des phases 20–35 et de l’atlas restent intactes.

Les fonctions d’inférence ne reçoivent ni clés ni texte clair. L’opérateur a toutefois accès aux réponses : aucune cécité humaine ni expertise extérieure n’est revendiquée. La vérification d’intégrité lit les octets des anciens fichiers manuscrits pour leurs empreintes ; la branche qui les analyserait n’est pas exécutée. Une formulation trop large sur cet accès est précisée dans l’[erratum](ERRATUM.md), sans toucher aux fichiers gelés.

Les contrôles supposent des espaces et des unités connus, une transformation d’un seul signe et des lignes artificielles. Ils ne couvrent pas les abréviations, ligatures réelles, substitutions de groupes, variations de main ou toutes les erreurs de transcription. Les données Voynich précédemment examinées ne deviennent pas une réserve aveugle.

## Décision et prédictions vérifiables

**La méthode n’est pas retenue pour inférer des équivalences Voynich.** L’expérience apporte une contrainte méthodologique précise : une fin commune ne suffit pas à certifier l’identité des mots ni à imposer une équation de clé.

Les fichiers `results/cases/*/predictions.json` contiennent les prédictions fixées avant comparaison aux réponses de transfert ; chaque remplacement peut être contrôlé contre la construction du cas. Les mots sans équivalence autorisée restent explicitement sans prédiction.

Une éventuelle méthode ultérieure devra traiter ces faux rapprochements sans assouplir les critères sur ces mêmes cas. Les exemples actuels deviendraient alors du développement, et sa capacité de récupération devrait être mesurée sur d’autres passages et clés. Cette correction n’a pas été exécutée ici.

Les confirmations historiques et graphiques indépendantes restent absentes. Aucune clé, langue, traduction, ni identité réelle de signes Voynich n’est annoncée. Travail conservé localement, sans publication, push, déploiement ou message externe.
