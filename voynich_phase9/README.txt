VOYNICH - PHASE 9 - 28 OCTOBRE 2026
Dépendances locales entre les bords de groupes.

AUCUNE CLÉ, LANGUE OU TRADUCTION VALIDÉE.

RÉSULTAT
Le modèle avec correction de voisinage partagée améliore la prédiction du premier caractère du groupe suivant sur des cahiers exclus de l'apprentissage : +0,082 bit/cible ZL/A ; +0,186 ZL/B ; +0,090 IT/A ; +0,202 IT/B. Dans ZL/B, l'exactitude du caractère initial passe de 24,1 % à 32,6 %. Le gain ne concerne pas des mots traduits.
Le résultat du deuxième modèle est exploratoire. PROTOCOL.json fixe le premier protocole ; ADDENDUM.json documente le second modèle, défini après le diagnostic du premier et avant ses propres calculs. Ne pas présenter ce second résultat comme préenregistré ou comme découverte nouvelle de la dépendance entre bords de groupes.

ORIGINAL ET CORRECTION
research.py : référence hiérarchique globale -> section/main -> position ; modèle voisin par table conjointe section/main/position/finale. Aucun effet voisin possible si le contexte n'a pas été appris. Dans ZL/B, 79,9 % des cibles ont une section/main absente du pli d'apprentissage.
pooled.py : même référence positionnelle, corrigée par P(initiale | finale précédente) / P(initiale), apprise globalement dans le seul ensemble d'apprentissage, puis normalisée. Hypothèse : cette correction est partageable entre catégories. Ce modèle a été ajouté après les premiers résultats. Les deux versions restent disponibles.

REPRODUIRE LES CALCULS À PARTIR DES ENTRÉES FIGÉES
Python 3, numpy. Pour le rapport : matplotlib, reportlab.
Depuis le dossier contenant voynich_phase9/ :
  python3 voynich_phase9/research.py
  python3 voynich_phase9/pooled.py
  python3 voynich_phase9/verify.py
  python3 voynich_phase9/make_report.py

Les données et les versions de dépendances sont dans data/inputs.json et ENVIRONMENT.json.
prepare.py est le script de provenance utilisé dans le dossier complet des phases antérieures. Il dépend de phase6/data/adjacency_inputs.json et du parseur/corpus de phase 1. Il n'est pas requis pour les quatre commandes ci-dessus ; cette archive ne prétend pas reconstruire toute la chaîne antérieure. data/lineage.json contient les empreintes des entrées originales.

VÉRIFICATION
verify.py utilise des Counter Python, séparés des tableaux numpy du calcul principal, pour reconstruire les cohortes et toutes les probabilités principales enregistrées. Il vérifie 190 328 évaluations position/modèle, quatre premiers mélanges et l'absence de chevauchement de feuillets entre apprentissage/test.
Les modèles de sensibilité réutilisent l'implémentation principale vérifiée ; leurs calculs n'ont pas tous une seconde implémentation.

LIMITES
- Positions approximatives par rang dans la transcription, pas coordonnées d'encre. Les dessins et espacements réels ne sont pas mesurés.
- Les groupes à virgule incertaine ou signes ambigus restent exclus, sans correction. Une absence de signe dans la cohorte n'est pas une absence dans le manuscrit.
- ZL/IT portent sur le même objet. Les plis partagent une grande partie de l'apprentissage. Les intervalles par rééchantillonnage ne sont pas une réplication indépendante.
- Les permutations portent sur les finales disponibles, dans chaque page et catégorie de position ; elles ne produisent pas des textes complets valides. Les valeurs de queue sont exploratoires, non corrigées pour comparaisons multiples.
- Pline, Dante, Naibbe et Timm diffèrent par taille, genre et procédé. Leur disposition en lignes est artificielle. Aucun classement universel du sens ou des langues n'en découle.
- Le témoin synthétique dépendant n'a aucun message ; son gain est pourtant très fort. Le témoin indépendant a un gain minuscule positif (~0,0023 bit), mais se situe dans sa distribution de mélanges (queue 0,545). Cela illustre aussi les limites d'une interprétation isolée des intervalles.
- Les gains aux distances 2 et 3 se comparent sur une même cohorte, plus petite que le test principal. Leur absence ne prouve pas l'absence de toutes dépendances longues.
- La décomposition q / autres est algébrique sur les mêmes probabilités ; ce n'est pas un réapprentissage après suppression de q.

FICHIERS
results/summary.json : premier modèle.
results/pooled_summary.json : second modèle, mêmes témoins et variantes.
results/toy_summary.json : contrôles synthétiques.
results/*predictions.json : probabilités et prédictions hors cahier/bloc.
results/*null_draws.json : tous les mélanges.
results/descriptive_edge_examples.json : exemples bruts, non ajustés, sans interprétation phonétique.
results/verification.json : vérification indépendante.
PROTOCOL.json, ADDENDUM.json, SOURCES.json : décisions, chronologie et attributions.
SHA256SUMS.json à la racine de l'archive : empreintes des fichiers livrés.

ATTRIBUTION DES TÉMOINS
Naibbe : Michael A. Greshko (2025), The Naibbe cipher: a substitution cipher that encrypts Latin and Italian as Voynich Manuscript-like ciphertext, DOI 10.1080/01611194.2025.2566408. Sortie créée en phase 1 avec le code de l'auteur ; licence jointe.
Timm et Schinner (2019/2020), A possible generating algorithm of the Voynich manuscript, DOI 10.1080/01611194.2019.1596999. Échantillon public du générateur, ligne d'amorce retirée en phase 6 ; licence MIT jointe. Aucun nouveau lancement de ce générateur en phase 9.
Les sources historiques et les autres références sont documentées dans SOURCES.json et les fichiers source_* du dossier data.
