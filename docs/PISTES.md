# Pistes ouvertes et critères de progrès

## Résultat nouveau : signal des finales non spécifique

La phase 18 avait retenu la clé distincte en finale, évaluée par le modèle de langue latin, comme piste exploratoire : gain positif au-delà des 19 mélanges sur ZL/A et ZL/B, avec gains positifs sur IT/A et IT/B. La [phase 19](../voynich_phase19/RAPPORT.md) montre que des textes produits sans message intentionnel peuvent aussi franchir ce critère. Ce résultat réduit la portée de la piste : le gain des finales ne suffit pas à distinguer un message d'un générateur dans ce dispositif.

La comparaison avec des générateurs structurés et la correction des segments courts sont désormais exécutées. Les six nouveaux textes sont tirés de modèles de transitions appris uniquement sur l'apprentissage ; l'échantillon Timm–Schinner publié est réanalysé, sans réexécution de son générateur. Les succès et échecs sont tous conservés. Cela n'identifie ni le latin ni l'absence de sens du manuscrit.

La prochaine étape utile est de **calibrer un critère discriminant** sur plusieurs mécanismes connus porteurs de messages et plusieurs générateurs sans message, puis de tester la stabilité des clés et les prédictions sur des partitions par cahier réservées avant leur sélection. Le critère des finales seul ne peut plus servir de confirmation linguistique.

La [phase 20](../voynich_phase20/RAPPORT.md) a ensuite testé une recherche de
clé avec segmentation sur douze contrôles. Le découpage exact progresse face
au découpage glouton, mais un seul contrôle atteint les deux seuils fixés.
La configuration n'est pas appliquée au Voynich. Les douze contrôles ont
ensuite servi au développement du traitement des mots inconnus en phase 21.

La [phase 21](../voynich_phase21/RAPPORT.md) évalue cette correction sur
douze nouveaux chiffrés et passages disjoints des anciens. Le découpage
progresse dans tous les cas, mais cinq seulement passent les deux seuils.
Les coupures inutiles diminuent fortement, tandis que les mots voisins
sont plus souvent fusionnés. La prochaine piste est un modèle plus précis
des frontières de mots, notamment en latin, et une représentation explicite
des signes jamais observés. Les nouveaux contrôles devront à leur tour
devenir des données de développement si leurs erreurs guident une correction.

Le [brouillon initial](../voynich_phase18/PROTOCOL_DRAFT.md), les protocoles figés de [phase 18](../voynich_phase18/PROTOCOL.json) et de [phase 19](../voynich_phase19/PROTOCOL.json), les sorties et les limites restent archivés. Les pistes sur l'initiale et le modèle italien n'atteignaient pas ensemble le critère de phase 18 sur les deux groupes ; elles ne sont pas réajustées dans la phase 19.

## Autres pistes non épuisées

- Segmentation conjointe des signes, espaces, abréviations et unités phonétiques. Les BPE et variantes des phases précédentes ne résolvent pas ce problème complet.
- Lexiques historiques plus larges, autres langues, modèles adaptés aux abréviations et budgets de recherche plus importants, après calibration appropriée.
- Paléographie indépendante des loci discriminants, sans fournir à l'évaluateur le mot souhaité.
- Réplication complète d'études récentes lorsque leur texte et leur code sont disponibles, avec distinction entre résumé lu et résultats reproduits.
- Tests comparatifs de plusieurs générateurs sans message et de plusieurs chiffres porteurs de sens sous un même budget.
- Analyse de l'organisation par cahier, main et section, sans traiter les regroupements statistiques comme des langues établies.

## Ce qui constituerait un progrès décisif

Une règle courte et stable devrait produire des lectures sur des pages qui n'ont pas servi à la choisir, expliquer les variantes et les erreurs de copie, conserver une grammaire cohérente sur des passages entiers et obtenir des confirmations externes. Un exemple isolé ou un taux de mots reconnus ne suffit pas.

Le projet n'affirme pas avoir testé tout ce qui est possible. Les échecs ne s'étendent qu'aux familles, corpus, budgets et conventions réellement exécutés.
