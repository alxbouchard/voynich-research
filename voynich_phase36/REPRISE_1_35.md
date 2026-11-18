# Reprise des conclusions et limites des phases 1 à 35

Le [bilan intégral figé](../docs/PIECES_REFERENCES.md#piece-0c0b297fe78073) conserve une entrée pour chaque phase. Les conclusions/limites des rapports sources 1–17 et 18–35 ont été relues. Aucun de ces résultats n’est annoncé comme nouvellement répliqué ici.

| Phases | Résultat qui contraint cette reprise | Conséquence |
|---|---|---|
| 1–6 | Contrôles parfois excellents, scores trompeurs, unités et familles de clés limitées ; aucune lecture historique. | Mesurer l’exactitude d’une règle sur des réponses connues, pas son score linguistique. |
| 7–10 | Prédiction de frontières et dépendances entre mots ; les scores de segmentation ne donnent pas une certitude graphique. Clé conditionnée par la finale précédente déjà testée. | Ne pas répéter cette condition ; isoler ici le début de ligne et chercher une équivalence relative de signes. |
| 11–13 | Couvertures insensibles aux sens permutés ; sens de départ non confirmés ; clés lexicales instables. | Aucun glossaire ni dictionnaire n’entre dans le nouveau test. |
| 14–17 | Liens étiquettes/prose non confirmés, transformations limitées négatives, marginalia incertains. | Aucun mot supposé clair ni texte parallèle. |
| 18–19 | Avantage des clés finales également produit par des générateurs sans message. | Inclure une génération sans passage cible et ne pas confondre régularité et sens. |
| 20–22 | Récupération imparfaite des espaces, correction de fusions non transférée. | Espaces fournis et explicitement limitants ; aucune correction automatique de mots. |
| 23–24 | Effets de position et associations non spécifiques ; transferts structurels ne donnent pas de lecture. | Contrôler la formation des lignes, exiger des équivalences exactes et un transfert sans retouche. |
| 25–26 | Associations image/texte insuffisamment couvertes et non confirmées extérieurement. | Ne pas recycler l’annotation IA comme vérité indépendante. |
| 27–29 | Invariants limités ; expansions/nulls difficiles à identifier ; ambiguïtés persistantes. | Tester explicitement un préfixe inséré hors modèle et s’abstenir devant les conflits. |
| 30 | Solveur exact réussi avec des mots clairs synthétiques riches ; prérequis historique absent. | L’objectif est une clé **relative entre deux positions**, sans prétendre retrouver les valeurs linguistiques des signes. |
| 31 | Aucun glossaire central régulier ni équivalence historique authentifiée. | Piste centrale abandonnée, pas d’utilisation des mois comme mots connus. |
| 32 | Lectures IA séparées, deux frontières non résolues, aucune expertise humaine. | Aucun nouveau lecteur IA pour remplacer l’expertise manquante. |
| 33–35 | Correspondances d’avril sensibles à plusieurs lectures ; troisième coupure stable pour certaines intersections seulement. | Conserver ces travaux et changer de question : aucun nouveau calcul sur ces variantes. |

## Nouvelle expérience et preuve extérieure manquante

Hypothèse locale : une permutation stable remplace seulement le premier signe des mots en début de ligne. Sa prédiction porte sur la normalisation de groupes dans des passages distincts. Elle peut être testée sans connaître leur traduction, car le reste du groupe reste identique dans ce modèle.

Mais des mots différents peuvent partager la même fin ; une correspondance ainsi construite peut être fausse. Les nouveaux contrôles doivent donc retrouver exactement les équivalences cachées, conserver l’identité quand aucun remplacement n’a eu lieu, et refuser une clé changée ou un signe ajouté. Un générateur de groupes inventés teste aussi la limite sémantique du dispositif.

Une expertise graphique indépendante reste nécessaire pour identifier de vrais allographes du manuscrit. Une éventuelle régularité calculée ne la remplace pas. Le test ne permettra pas non plus de nommer une langue : une permutation globale de tout l’alphabet clair resterait indéterminée.

Cette expérience est nouvelle dans le dossier ; elle n’est pas présentée comme une découverte historique ou une méthode inédite dans toute la littérature. Le protocole, le code et les sources sont gelés avant les nouveaux cas.
