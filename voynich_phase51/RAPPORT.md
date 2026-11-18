**Mise à jour.** Deux essais longs ont ensuite été terminés. [Lire leur bilan](../voynich_phase51_longbudget/fin_deux_essais/RAPPORT.md).

# Phase 51 — campagne initiale incomplète

17 novembre 2026. **NOT_TRANSLATION — limite de calcul atteinte, critère non évaluable.**

Mise à jour à 20:06 UTC : les deux essais commencés ont expiré après 3 600 secondes. Les journaux attestent au moins 1 700 pas chacun ; aucun checkpoint final ni aucune inférence ne sont disponibles. Les trois autres essais initiaux restent non commencés. Voir `ORIGINAL_OUTCOME.json` et `TERMINAL_ARTIFACT_MANIFEST.json`. Le détail ci-dessous conserve aussi l’historique de préparation.

Le [banc séparé](../research/2026-11-17-zero-context-equivalence/RAPPORT.md) échoue à l’équivalence stricte dès la première graine ; la seconde n’a pas été commencée. Une [campagne native distincte à budget accru](../voynich_phase51_longbudget/README.md) conserve les cinq graines, les données, le modèle et les critères, avec un plafond de 10 800 secondes. Aucun poids partiel ni candidat optimisé n’y est repris.

Le modèle phonétique original de Luo, retrouvé et exécuté en phase 50, est maintenant testé sur de véritables formes lexicales. La préparation, l'évaluateur et les paramètres ont été figés dans le commit local `b38fa082fcc9e732114a54a636a68a8e64026888`, avant tout apprentissage. Le Voynich n'entre pas dans cet essai et aucune traduction n'est proposée.

## Données et réponses cachées au modèle

La source est [IE-CoR v1.2.1](https://github.com/lexibank/iecor/tree/dd1ebc997bc38c824fb18a1ef234bbf2c229420b), au commit `dd1ebc997bc38c824fb18a1ef234bbf2c229420b`. Quinze fichiers primaires sont archivés avec leur SHA-256, taille et empreinte de blob Git. Les tables donnent les écritures natives, transcriptions phonétiques et classes de cognats établies par les auteurs. Un cognat est ici une forme historiquement apparentée, pas nécessairement un synonyme utilisable comme traduction en contexte.

L'entrée inconnue contient 123 formes gothiques distinctes, écrites avec 24 signes. Le lexique connu contient 166 candidats en IPA issus de 170 entrées de vieil islandais. Les valeurs phonétiques gothiques, concepts et correspondances de référence ne sont pas transmis à l'optimiseur. Les caractères natifs ne servent que d'identifiants de signes.

La séparation utilise un hachage des identifiants de formes, sans consulter les réponses : 92 formes pour l'apprentissage, 31 pour la réserve. Respectivement 63 et 19 ont au moins un cognat attesté dans le lexique connu. Aucun mot source n'est partagé entre les deux partitions. Tous les signes de la réserve figurent dans l'apprentissage.

Chaque partition est mélangée séparément, puis les mots sont concaténés deux par deux sans espace ni frontière interne dans les objets d'entrée. Il reste un singleton dans la réserve. Cela produit 46 séquences d'apprentissage et 16 de test. Ces séquences sont construites à partir de formes lexicales : elles ne constituent pas un texte historique continu.

Le parseur IPA original retire les marques de longueur et normalise certains signes. Quatre groupes de formes deviennent des candidats homophones, dont un groupe créé par la suppression de longueur. L'évaluation porte donc sur une classe IPA documentée, pas sur une identité lexicale ou un sens unique. La liste complète des transformations figure dans `data/INPUTS.json` et `data/GOLD.json`.

## Expérience figée

Cinq départs, graines 51001 à 51005, comportent chacun 3 000 étapes du modèle `ExtractModelV2`, configuration `FinalNon`. Les valeurs phonétiques connues du gothique, les oracles et les coupures de référence sont désactivés. Le lexique cible complet est fourni : les cibles possibles de la réserve peuvent donc être présentes dans ce lexique. Seules les formes du côté inconnu sont réservées.

Le moteur et sa fonction d'apprentissage restent ceux des sources authentifiées en phase 50, avec les quatre mêmes modifications de compatibilité. La borne minimale des candidats est explicitement fixée à un signe pour conserver tout le lexique. Deux processus de calcul au maximum fonctionnent simultanément, avec deux fils CPU chacun. Aucun meilleur départ n'est sélectionné.

Les poids initiaux et finaux seront évalués avec exactement les mêmes paramètres de score et le même alphabet. La mesure principale exige simultanément la frontière complète du mot source et une cible IPA appartenant à sa classe de cognats. Son dénominateur est de 19 formes annotées dans la réserve, et non de 31 traductions à produire.

Le critère fixé exige un gain moyen positif, un gain dans au moins quatre départs sur cinq, et deux valeurs p au plus égales à 0,01 contre 9 999 permutations communes des étiquettes dans des blocs de longueur. Ce contrôle teste une association conditionnelle entre prédictions et annotations ; il ne mesure pas le taux général de fausses découvertes d'une langue dans le Voynich.

Les réponses de référence sont conservées séparément et ne sont pas ouvertes par le processus d'apprentissage. Elles restent physiquement accessibles sur le disque : il s'agit d'une séparation du parcours logiciel vérifiée, pas d'un cloisonnement de sécurité.

## État de cette édition

Les entrées ont été reconstruites séparément par un agent d'audit. Le protocole et l'évaluateur ont été relus par un autre agent ; ses dix contrôles arithmétiques passent. Ces vérifications IA sont séparées au niveau des agents mais ne remplacent pas une validation linguistique externe.

Les essais 51001 et 51002 ont démarré le 17 novembre à 19:06 UTC et ont chacun dépassé 100 étapes sans erreur constatée. Les trois suivants sont en file d'attente. La file prévoyait leur lancement à libération d'une place ; le complément ci-dessous décrit la réservation ultérieure d'un créneau pour vérifier une accélération. Les états vivants sont dans `ORCHESTRATION.json` et `runs/*/RUN.json` dans le dossier de travail.

**Aucun score final ni succès du critère n'est encore établi dans cette édition.** Un dépassement de la limite de calcul sera conservé comme essai incomplet, pas comme échec scientifique. Le protocole ne sera pas ajusté en fonction des réponses obtenues.

Cette phase est une nouvelle calibration sur IE-CoR, pas une reproduction exacte des données ou du chiffre A@10 de l'article TACL. Même un résultat positif ne validerait qu'une récupération partielle de cognats dans cette expérience. Il ne donnerait ni langue du Voynich, ni clé complète, ni traduction du manuscrit. L'objectif de déchiffrement reste ouvert.

## Compléments vérifiés pendant le calcul

La reconstruction dans un nouveau dossier, depuis le commit figé, reproduit exactement les 242 fichiers du gel, y compris les données et les copies runtime. Aucun nouvel apprentissage n’est lancé par ce contrôle : voir `INPUT_REPLAY.json`.

L’[audit statique de performance](STATIC_PERFORMANCE_AUDIT.md) identifie une contribution de contexte nulle dans la configuration réelle, mais des calculs de convolution toujours exécutés. Une accélération reste à tester en conservant RNG, gradients et paramètres ; aucune n’a été appliquée aux cinq essais.

Une [recherche primaire bornée](research_notes/anchor_search/SEARCH_NOTE.md) ne fournit pas de nouvel ancrage sémantique indépendant. L’[avis sur la suite](POST_GATE_REVIEW.md) distingue les contraintes graphiques existantes d’une traduction : même après une calibration positive, le choix du lexique et la spécificité face aux témoins resteraient à vérifier.

## Réservation d’un créneau pour le banc d’équivalence

À 19:34 UTC, les deux apprentissages natifs ont dépassé 900 étapes et continuent. Le débit constaté pourrait dépasser le plafond de 3 600 secondes avant les 3 000 étapes requises. Ce plafond est conservé pour ces essais ; un arrêt à cette limite sera un calcul incomplet, sans conclusion linguistique.

Les trois graines non démarrées sont temporairement retenues par `HOLD_NEW_TRIALS.json`. Aucun des deux apprentissages n’a été interrompu ni modifié. L’ordonnanceur v3 conserve un créneau pendant tout le parcours d’une graine, y compris les transitions entre apprentissage et inférences ; ses versions précédentes restent archivées.

Un banc séparé est préparé et figé après revue indépendante. Il compare deux préfixes de 1 et 10 étapes pour deux graines, avec le programme natif de 3 000 étapes et son annealing inchangés. Le seul candidat détache deux branches de contexte après leur calcul avant complet ; une règle explicite rétablit les gradients nuls des convolutions après un certificat natif préalable. Les états initiaux ne sont jamais corrigés et les trajectoires ne sont pas resynchronisées.

Les critères exigent les mêmes octets des tenseurs, états aléatoires, pertes et mises à jour, avec seulement les différences de graphe déclarées. Trente contrôles statiques et de données factices passent ; six scénarios séparés contrôlent l’attente du créneau. **Aucun résultat réel d’équivalence ni gain de vitesse n’est encore établi dans cette édition.** L’attente doit réserver au maximum deux processus de modèle au total et ne libérera pas automatiquement les graines restantes après le banc.
