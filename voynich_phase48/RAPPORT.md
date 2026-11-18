# Phase 48 — Audit du décodeur public CMM

17 novembre 2026 — **NOT_TRANSLATION**

La méthode CMM de Kenneth Young ne fournit pas, dans l'implémentation et les résultats examinés, une traduction vérifiée du Voynich. Son score d'accord lexical est déterminé par la construction des sorties : des chaînes créées sans message obtiennent environ 99 %. Les quatre résultats publiés que nous avons rejoués sont pourtant reproduits exactement pour les fonctions étudiées. Le problème porte donc sur leur interprétation comme déchiffrement.

## Sources et protocole

Nous avons examiné [Voynich_Pipeline](https://github.com/keninayoung/Voynich_Pipeline/tree/c7c3b66fe6c4e5ea8c172df4c607befeae823740), commit `c7c3b66fe6c4e5ea8c172df4c607befeae823740`. Dix fichiers ont été téléchargés et vérifiés contre leurs tailles et SHA Git, notamment le code, les entrées et les sorties publiées. Le README annonce un accord lexical moyen de 91 % avec des corpus Trotula/Hildegard.

Le [protocole](PROTOCOL.json), les sources et le programme d'audit ont été figés au commit local `9ca7cbb092ede3f88e7840b1b08112452ca1ea94`, avant l'exécution des nouveaux scores. L'inspection préalable du code avait déjà permis de prévoir la circularité : ce n'est pas une expérience aveugle. Deux agents IA en contextes séparés ont examiné le mécanisme et la provenance ; ils ne constituent pas une expertise linguistique ou paléographique humaine.

Le fichier Python original contient un unique octet non UTF-8 dans un commentaire. Pour exécuter les fonctions, cet octet a été remplacé en mémoire par une apostrophe ASCII, sans modification des octets archivés ni du code exécutable. BERT, les graphiques et le lancement complet du pipeline sont hors périmètre. [Détails d'exécution](results/EXECUTION.json).

## Ce que mesure réellement l'accord lexical

Les correspondances imposent, par exemple, `a → aqua` et `o → oleum`. Toutes les racines émises par les tables figurent dans la liste interne `MED_LEX`. Chaque clause retenue reçoit ensuite un seul verbe ajouté, `fac` ou `usa`, absent de cette liste. Si la sortie contient N tokens et C clauses :

`lexicon_alignment = round(1 − C/N, 4)`.

Cette identité est vérifiée sur les **199 lignes de résultats publiés** et les **205 exécutions de contrôle**. Le score ne compare pas le texte produit à une traduction connue. Le code disponible ne charge aucun corpus Trotula/Hildegard ; aucune ressource comparative de ce type n'a été trouvée dans l'arbre épinglé. Les références bibliographiques du README ne fournissent pas un alignement vérifiable. [Tables et métrique originales](https://github.com/keninayoung/Voynich_Pipeline/blob/c7c3b66fe6c4e5ea8c172df4c607befeae823740/voynich_pipeline.py#L98), [audit des sorties](results/PUBLISHED_AUDIT.json).

## Entrées sans message

Chaque entrée a été passée dans les mêmes fonctions de nettoyage, de génération et de mesure, sous cinq identifiants activant les cinq contextes du programme. Les 205 entrées traitées sont conservées sans sélection par score. Le nettoyage les laisse toutes inchangées.

| Famille | Entrées distinctes / exécutions | Accord lexical | Z-score de structure |
|---|---:|---:|---:|
| Lettres EVA tirées indépendamment, 40 mots de longueur 3 à 8 | 20 / 100 | 98,89–99,17 %, moyenne 99,042 % | −2,059 à 2,385 |
| Unités tirées indépendamment dans l'inventaire de la table, 40 mots | 20 / 100 | 78,38–80,26 %, moyenne 79,03 % | 3,812 à 9,161 |
| Cycle artificiel `qkeitlfpd` répété 100 fois | 1 / 5 | 99,89 % | 132,327 |

Les contextes d'une même entrée sont dépendants : **41 chaînes distinctes, pas 205 textes indépendants**. Les unités tirées dans la table constituent un contrôle ciblé. Le cycle périodique est un contre-exemple construit après inspection du code, fixé avant mesure ; il n'est ni un texte aléatoire ni un modèle historique du manuscrit.

Le contrôle uniforme dépasse donc l'accord de 91 % annoncé, mais son z-score reste proche de zéro. Nous ne prétendons pas que tous les témoins réussissent toutes les métriques. Le contrôle périodique montre qu'une structure répétitive sans message cible peut aussi dépasser largement les seuils de z-score affichés. Un test détectant une organisation non aléatoire ne suffit pas à établir une langue ou un sens.

Le z-score est calculé après développement des signes en mots latins et traitement des clauses. Son mélange de référence détruit aussi les séquences créées par les tables. Il ne constitue pas une comparaison contrôlée entre texte historique traduit et texte sans message. [Toutes les entrées, sorties et mesures](results/CONTROLS.json), [résumé](results/SUMMARY.json).

## Contrôles complémentaires

Les sorties latines, anglaises et toutes les métriques du cœur étudié ont été reproduites exactement pour les quatre identifiants publiés `1v`, `68r`, `78r` et `99r`. La sensibilité et BERT ne sont pas inclus dans cette égalité. Les 199 accords lexicaux stockés sont également égaux au comptage direct des mots dans `MED_LEX`.

Une permutation des noms des 20 concepts latins, appliquée aux tokens de deux sorties témoins, laisse toutes les métriques de `compute_metrics` identiques. Il s'agit d'une invariance du score, sans réexécution du rendu anglais et sans proposition de traduction rivale.

La sensibilité comporte un problème distinct : sa référence passe par le traitement des clauses, mais la variante est mappée directement. Avec `a` répété 100 fois et `drop_ratio=0`, une seule valeur est sélectionnée puis permutée avec elle-même. La table reste donc identique ; pourtant le programme annonce **100 % de baisse d'entropie**. Il compare `aqua usa` à 100 occurrences de `aqua`. Ce diagnostic ne quantifie pas la part d'artefact dans toutes les sensibilités publiées et n'utilise pas leur paramètre par défaut. [Diagnostic complet](results/DIAGNOSTICS.json).

## Provenance des entrées publiées

Un audit descriptif ajouté après les scores compare les deux fichiers LSI livrés par l'auteur, sans comparaison à une édition officielle extérieure. Le fichier utilisé commence à la ligne 2384 de celui nommé « original ». Il manque 154 balises de folios/loci, dont 153 pour f1r et l'en-tête de f1v. Deux contenus conservés diffèrent par suppression de marqueurs d'incertitude. Les deux fichiers comptent respectivement 38 939 et 33 639 lignes ; cette comparaison porte sur les fichiers du dépôt étudié, sans authentification externe.

Le début du CSV f2v concatène exactement, sur 234 caractères nettoyés, les cinq lectures H, C, D, F et U du même locus f2v.1. Ces lectures parallèles ne sont pas cinq passages successifs. Ce corpus agrégé ne doit donc pas être adopté comme une transcription canonique. Le guide ancien présente aussi du texte descriptif anglais comme « Original EVA » et correspond à une autre génération de résultats. [Audit reproductible de provenance](results/PROVENANCE_AUDIT.json).

## Portée du résultat

Cette phase retire aux scores examinés leur valeur de preuve indépendante de traduction. Elle ne démontre ni que le Voynich est dépourvu de message, ni qu'une hypothèse latine serait impossible, et ne juge pas les intentions de l'auteur. Aucun mot du manuscrit ne reçoit ici un sens validé.

Pour retenir une lecture, il faudra des correspondances justifiées indépendamment, une récupération de textes connus avec clé cachée et un transfert sans retouche à des passages réservés. Les phrases fabriquées par ce pipeline ne remplissent pas ces conditions.

Les six sorties principales ont été rejouées à l'octet. Un vérificateur séparé contrôle les générateurs, les clauses, les identités lexicales et le contre-exemple périodique ; sa portée exacte figure dans [la vérification](results/INDEPENDENT_VERIFICATION.json). Voir aussi [reproduction](REPRODUCTION.md) et [attributions](NOTICE.md).
