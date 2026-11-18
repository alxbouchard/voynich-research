# Phase 39 — lire les abréviations avec des références historiques

17 novembre 2026. **NOT_TRANSLATION. Aucun déchiffrement ni traduction du Voynich obtenus. L'objectif utilisateur reste ouvert.**

Cette phase apporte une ressource qui manquait aux essais précédents : des transcriptions médiévales accompagnées de développements de référence. Elle construit et teste un lecteur conservant les lettres visibles. Le test montre que cette contrainte et des correspondances apprises signe par signe ne suffisent pas : **260 expansions concordantes sur 350 évaluables, soit 74,29 %**, avec une couverture de seulement 9,45 % des mots marqués évaluables. Le seuil prévu échoue.

## Ce qui a été acquis

L'étude [PEN, Clérice et collaborateurs, 2026](https://arxiv.org/html/2602.13905v1) décrit un ensemble de test corrigé par un philologue, à côté de transcriptions automatiquement alignées. Son [jeu public](https://huggingface.co/datasets/comma-project/pen-alignment-pairs) a été récupéré à la révision `c55a9f21e1aea6d8e8d84fac4417a6683596a5e1`. Le fichier `test` contient 1 879 lignes ; le papier décrit 588 alignements d'origine. Ces unités ne sont pas assimilées et aucune nouvelle expertise des images n'est revendiquée.

Le fichier de validation a aussi été conservé pour inventaire, mais n'a pas été utilisé. Les 4,66 millions de lignes automatiques d'entraînement n'ont pas été téléchargées. Le lecteur utilise uniquement le fichier de test publié, repartitionné pour notre expérience. Cette décision permet de travailler sur une référence annotée ; elle ne prétend pas reproduire le modèle neuronal PEN.

Les fichiers originaux et leurs empreintes sont dans [SOURCES.json](../docs/PIECES_REFERENCES.md#piece-bd46e6bd81ebba). La conversion Parquet vers JSON a été vérifiée sur les 1 879 lignes. Les données dérivées conservent source, cible, chemin documentaire, langue et identifiant.

## Partition et garanties

Après regroupement des variantes d'identifiants documentaires, 1 245 extraits de 224 groupes servent à apprendre ; 631 extraits de 65 autres groupes sont réservés. Trois lignes à langue indéterminée sont conservées mais exclues des calculs. Il s'agit de groupes dérivés des chemins, pas d'un nouveau catalogue paléographique.

Tous les extraits des collections à chemin de type `alto/` ou `paramhtrs-alignement/` sont réservés, ainsi qu'un cinquième des autres groupes choisi par empreinte. L'étiquette interne `GT` désigne ces collections, rapprochées des sources de référence décrites dans l'étude ; elle ne signifie pas que nous avons réexpertisé les images. Les quatre fichiers `alto/` restent dans un seul groupe. Aucune source normalisée complète du test ne duplique une source d'apprentissage ; des œuvres et des phrases communes peuvent néanmoins traverser les groupes.

La partition, le programme, le modèle appris et les critères ont été figés avant les prédictions réservées : **22 fichiers**, le 17 novembre 2026 à **16:31:43 UTC**, commit `31ff2163505d4f3a874b655ae2f479fcd7ad99c8`. Les cibles réservées ne sont pas transmises à l'apprentissage. Ce garde-fou est logiciel ; il ne constitue pas un aveuglement physique de l'opérateur. Les incidents de préparation sont consignés dans [development/NOTES.md](development/NOTES.md).

## Comment fonctionne le lecteur

Les majuscules sont rabattues, les distinctions u/v et i/j réunies, les ligatures ae/oe développées et les marques Unicode décomposées. Les accents de la référence sont retirés. Les scores portent donc sur des chaînes normalisées, pas sur la restitution exacte de l'édition ou de son orthographe complète.

L'alignement des mots conserve les passages identiques et certaines substitutions courtes encadrées par des mots identiques. C'est un alignement automatique, non une annotation humaine mot à mot. Les prédictions hors de ces paires restent non évaluées.

Pour apprendre une règle, les lettres ordinaires doivent rester identiques et dans le même ordre. Un signe marqué peut développer au plus huit lettres, en conservant ses lettres visibles, y compris ses lettres suscrites identifiables dans Unicode. Seuls les cas à décomposition unique alimentent les règles par signe. L'apprentissage conserve **4 238 paires d'évidence, 114 unités marquées et 2 165 formes de mots**.

Une valeur doit apparaître dans au moins deux groupes d'apprentissage pour entrer dans le lecteur. Les valeurs plus rares restent archivées. Ce filtre peut écarter une expansion correcte : il s'agit d'une hypothèse testée, pas d'une garantie. Le lecteur conserve toutes les combinaisons admises, ajoute les développements de mots entiers suffisamment attestés, et ne répond que si une seule chaîne reste. Il s'abstient lorsqu'un signe manque ou que plusieurs chaînes subsistent. Aucun dictionnaire ne choisit entre les chaînes produites.

Les critères prévus exigeaient, pour chaque langue, au moins 30 réponses évaluables, une précision d'au moins 95 % et une couverture d'au moins 20 % des mots marqués évaluables. Même leur réussite n'aurait validé qu'un composant à alphabet connu.

## Résultats réservés

Les 631 extraits contiennent 22 084 mots source, dont 8 263 portent une unité marquée selon notre convention. Seulement **3 702** de ces derniers disposent d'une paire mot à mot évaluable. Les autres ne sont pas comptés comme correctement lus.

| Sous-ensemble | Mots marqués évaluables | Réponses du lecteur | Concordances | Écarts | Précision parmi les réponses | Couverture |
|---|---:|---:|---:|---:|---:|---:|
| Latin | 3 481 | 327 | 242 | 85 | 74,01 % | 9,39 % |
| Ancien français | 221 | 23 | 18 | 5 | 78,26 % | 10,41 % |
| Ensemble | 3 702 | 350 | 260 | 90 | 74,29 % | 9,45 % |

Le lecteur émet aussi **482 expansions hors des paires évaluables**. Elles ne sont ni validées ni déclarées fausses. Au total il émet 832 expansions, s'abstient devant 6 677 mots ambigus et trouve 754 mots contenant un signe sans valeur suffisamment soutenue. Il ne rencontre aucun dépassement du plafond de 4 096 candidats.

Sur les formes de mots absentes de la table de mots apprise, les 233 réponses évaluables comprennent 155 concordances et 78 écarts. Les réussites existent, mais la généralisation est insuffisante pour une lecture fiable.

Exemples historiques réservés, sans rapport sémantique établi avec le Voynich :

| Source annotée | Sortie | Référence | Observation |
|---|---|---|---|
| `ꝓut` | `prout` | `prout` | Développement concordant sur une forme nouvelle. |
| `debitoꝵ` | `debitorum` | `debitorum` | Développement concordant sur une forme nouvelle. |
| `mag̃r` | `magr` | `magister` | La valeur retenue ne développe pas l'abréviation requise. |
| `tamꝙ̃` | `tamquem` | `tamquam` | Une réponse unique peut être erronée dans ce contexte. |

Tous les cas, y compris les écarts et les alternatives, sont conservés dans [EVALUATED.json](../docs/PIECES_REFERENCES.md#piece-5e45efd07aab69) et [PREDICTIONS.json](../docs/PIECES_REFERENCES.md#piece-7d3a7ea480c690).

## Comparateurs et diagnostic

Deux comparateurs avaient été définis avant le test. Sur les mêmes 3 702 paires :

| Méthode | Réponses uniques évaluables | Concordances | Écarts | Précision | Couverture |
|---|---:|---:|---:|---:|---:|
| Lecteur par signes | 350 | 260 | 90 | 74,29 % | 9,45 % |
| Mots entiers déjà attestés | 997 | 974 | 23 | 97,69 % | 26,93 % |
| Deux lettres ajoutées à un squelette, lexique d'apprentissage | 513 | 281 | 232 | 54,78 % | 13,86 % |

Le comparateur de mots entiers est plus fiable sur ce sous-ensemble, mais dépend de formes déjà rencontrées et conserve 23 écarts. Il ne remplace pas après coup le lecteur préenregistré. Le comparateur à deux insertions n'inclut pas les préfixes de phase 38 ; ses taux ne constituent pas une réplication de cette phase.

Un diagnostic **ajouté après les résultats**, sans changer les règles, répartit les 90 écarts du lecteur : 39 nécessitent une règle absente de l'apprentissage ; 12 nécessitent une valeur observée mais éliminée par le seuil de deux groupes ; 39 ne sont pas compatibles avec la conservation des lettres visibles dans ce modèle. Cette dernière catégorie peut mêler correction de transcription, choix éditorial et erreur d'alignement. Elle ne prouve pas que la référence ou le manuscrit serait fautif. Voir [diagnosis.json](results/diagnosis.json).

## Conséquence pour le déchiffrement

Le corpus, les correspondances documentées et le lecteur sont désormais disponibles pour tester des hypothèses d'abréviation. Le résultat privilégie l'étude du mot et de son contexte plutôt qu'une valeur isolée par signe. Il montre aussi qu'une unique forme lexicale ne certifie pas une expansion.

**Aucune valeur de signe Voynich n'a été établie ici.** Les transcriptions étudiées ont un alphabet identifié ; le modèle ne récupère pas une clé inconnue. Il ne valide pas non plus une hypothèse italienne, puisque ses références sont latines et françaises. Le lecteur échoue au critère fixé et n'est pas appliqué au manuscrit. L'objectif de décodage reste ouvert : une correspondance indépendante entre les glyphes du Voynich et des unités lisibles manque toujours.

## Vérifications

Une implémentation distincte reconstruit l'apprentissage par programmation dynamique vers l'avant, les candidats par parcours de suffixes et le comparateur lexical par recherche directe de sous-séquences. Elle vérifie **4 238 paires d'apprentissage, 114 unités, 9 700 formes d'entrée réservées, 631 extraits et 3 702 paires évaluées**. L'alignement automatique est contrôlé selon sa définition, sans prétendre le faire valider par un philologue.

La réexécution réapprend le modèle dans un dossier vierge, confirme les 22 empreintes figées et reproduit **six sorties à l'octet**. Voir [verification.json](results/verification.json), [replay.json](results/replay.json) et [REPRODUCTION.md](REPRODUCTION.md). Même opérateur ; aucune expertise historique indépendante nouvelle. Livraison locale uniquement.
