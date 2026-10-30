# Pistes ouvertes et critères de progrès

## Résultat nouveau : clé selon la position

La phase 18 est [exécutée et vérifiée](../voynich_phase18/RAPPORT.md). Les deux familles retrouvent les contrôles connus. La clé distincte en finale, évaluée par le modèle de langue latin, est la seule combinaison qui remplit le critère exploratoire de poursuite : gain positif au-delà des 19 mélanges sur ZL/A et ZL/B, avec gains positifs sur IT/A et IT/B. Cela n'identifie pas le latin comme langue du manuscrit et n'établit aucune traduction.

La prochaine étape utile est de vérifier si ce signal résiste à des **générateurs sans message plus structurés**, à des chiffres porteurs de sens et à de nouvelles partitions par cahier. Les mélanges devraient laisser les segments courts exclus fixes, afin de préserver exactement les distributions sur les caractères effectivement notés. Il faudra également mesurer la stabilité des clés. Aucun calcul de phase 19 n'est exécuté à ce stade.

Le [brouillon initial](../voynich_phase18/PROTOCOL_DRAFT.md), le [protocole figé](../voynich_phase18/PROTOCOL.json), les sorties et les limites restent archivés. Les pistes sur l'initiale et le modèle italien n'atteignent pas ensemble ce critère sur les deux groupes ; ne pas les relancer uniquement jusqu'à obtenir un résultat favorable.

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
