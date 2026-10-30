VOYNICH - PHASE 10 - 28 OCTOBRE 2026
Deux tables de lecture, déclenchement après EVA y.
AUCUNE CLE, LANGUE OU TRADUCTION VALIDEE.

RESULTAT
Le modèle final, limité à deux permutations alphabétiques avec espaces conservés,
retrouve 99,98596 à 100 % des lettres de huit témoins chiffrés. Dans les seules
initiales déclenchées après y, sa réussite va de 99,7326 à 100 %.
Ce sont quatre clés par langue sur deux mêmes textes, pas huit corpus indépendants.
Sur Voynich, les gains ZL/A restent dans l'étendue des 19 mélanges; les scores
ZL/B et IT/B se dégradent en latin et en italien. Aucun déchiffrement validé.

CHRONOLOGIE ET CHANGEMENT DE PORTEE
PROTOCOL.json : modèle arbitraire plusieurs signes vers une lettre, espaces omis.
Echec des quatre contrôles dans le sous-ensemble déclenché, malgré 97,5 à 99,0 %
d'exactitude globale. Des clés fausses dépassent le score de la vraie clé.
ADDENDUM.json : après ce diagnostic, conservation des espaces fixes dans le
modèle de langue. Le latin reste sous le seuil, donc pas d'application Voynich.
ADDENDUM_PERMUTATION.json : nouvelle hypothèse plus étroite, une permutation
par table. Les huit contrôles passent; seule cette famille est appliquée au réel.
Ce développement après contrôles est exploratoire, pas une confirmation
préenregistrée. L'échec d'une famille ne valide pas la suivante par lui-même.

REPRODUIRE DEPUIS LES DONNEES FIGEES
Python 3, numpy, lxml; g++ C++17. Rapport : reportlab, matplotlib.
Depuis le dossier contenant voynich_phase10/ :
  mkdir -p voynich_phase10/tmp
  g++ -O3 -std=c++17 voynich_phase10/src/homophonic.cpp -o voynich_phase10/tmp/homophonic
  g++ -O3 -std=c++17 voynich_phase10/src/context_boundary.cpp -o voynich_phase10/tmp/context_boundary
  g++ -O3 -std=c++17 voynich_phase10/src/context_permutation.cpp -o voynich_phase10/tmp/context_permutation
  python3 voynich_phase10/prepare_boundary_lm.py
  python3 voynich_phase10/run.py --controls
  python3 voynich_phase10/run.py --boundary-controls
  python3 voynich_phase10/run.py --permutation-controls
  python3 voynich_phase10/run.py --permutation-real
  python3 voynich_phase10/diagnose.py
  python3 voynich_phase10/verify.py
  python3 voynich_phase10/summarize.py
  python3 voynich_phase10/make_report.py

run.py réutilise les fichiers résultats *_blind.json et *_context.json existants.
Pour recalculer les optimisations, les retirer uniquement dans une copie de
l'archive, puis lancer ces commandes. run_initial.py conserve le script avant
les deux ajouts; le script actuel reproduit aussi les réglages initiaux.
Les temps de calcul changent; comparer clés, textes décodés et scores, pas seconds.
Les entrées source_inputs.json sont figées depuis phase9. L'archive ne reconstruit
pas les images ni toute la chaîne antérieure. Les programmes n'accèdent pas au web.

METHODE
Premier caractère d'un mot après un mot connu finissant par y : table1.
Tous les autres caractères : table0. Etat réinitialisé après une ligne ou un
groupe incertain. Les espaces sont ancrés et ne peuvent être déchiffrés en lettres.
Ils ne sont jamais comptés comme lettres correctes dans les exactitudes témoins.
Les états sont déterminés par le texte chiffré, avant toute recherche de clé.
Le solveur C++ reçoit seulement les identifiants chiffrés et les modèles de langue.
Les clés vraies et le texte témoin servent uniquement à l'évaluation Python.
Les clés finales comprennent aussi les lettres absentes de l'apprentissage;
leur correspondance reste arbitraire si elle n'est pas imposée par élimination.
La couverture compte séparément ces positions absentes de l'apprentissage.
Les espaces/transcriptions sont supposés correspondre à de vrais mots du clair.

Le score est une somme de log-probabilités de fenêtres de quatre caractères,
avec pénalité de divergence des fréquences de lettres (coefficient4).
8 redémarrages de 60000 propositions; meilleur objectif d'apprentissage retenu.
Les scores publiés sont des bits moyens par fenêtre de quatre caractères,
espaces inclus dans les modèles boundary/permutation. Ce n'est ni une entropie
par lettre, ni un pourcentage de traduction. On ne compare pas directement les
valeurs absolues entre modèles avec et sans espaces.
ZL/IT, A/B séparés. Un feuillet physique sur cinq dans la liste lexicographique
est réservé. Apprentissage plafonné à24000 lettres, en lignes complètes.
Les feuillets test ne servent ni au choix de la clé ni à son optimisation.
Contrairement à phase9, ce test réserve des feuillets, pas des cahiers entiers.

TEMOINS MELANGES
19 permutations par couple ZL(A/B) et langue. Les deux langues utilisent les
mêmes tirages de mots. Tous les mots intérieurs connus d'une ligne sont mélangés,
sans changer les premiers/derniers mots ni les positions None. Les lettres et
l'intérieur des mots restent intacts; les voisinages et positions changent.
Chaque tirage est réappris pour les deux modèles, puis évalué sur son test mélangé.
Il s'agit d'un témoin faible de structure, pas d'un générateur complet du manuscrit.
Les décomptes de dépassement sont descriptifs; aucune p-valeur n'est revendiquée.

VERIFICATION ET LIMITES
verify.py ne dépend pas de run.py. Il reconstruit les 200 encodages/décodages,
les objectifs d'apprentissage, les100 comparaisons et4 899 916 prédictions de
lettres, ainsi que736 376 caractères de contrôles chiffrés/déchiffrés.
Il partage les données et tables de langue figées : ce n'est pas une réplication
par un autre chercheur. Un contrôle de reproduction depuis archive est conservé.
Les corpus César/Dante ne couvrent pas toutes les langues ou formes médiévales.
Le modèle final exclut l'homophonie, les abréviations, les ligatures et changements
de segmentation. Le budget heuristique n'offre pas de garantie d'optimum global.
Un échec sur Voynich ne réfute donc pas tous les chiffres contextuels.
Les transcriptions sont deux lectures du même objet, non des données indépendantes.
Les virgules incertaines restent exclues avec leur groupe entier; aucune correction
ou lecture manuscrite nouvelle n'a été imposée.

FICHIERS
results/report_summary.json : résultats primaires, sensibilités et témoins.
results/*summary.json : toutes les comparaisons des trois étapes.
results/*_context.json et *_blind.json : clés candidates et sorties NON VALIDEES.
results/calibration_diagnostic.json : clés fausses mieux notées que la vraie.
data/*truth.json : clés connues des contrôles, jamais transmises au solveur.
data/split.json, data/lineage.json, data/final_source_hashes.json : provenance.
SOURCES.json, data/source_phase2.json, data/source_phase9.json : attributions.
ENVIRONMENT.json : versions. SHA256SUMS.json dans l'archive : empreintes.

ATTRIBUTION
César : Perseus Digital Library, CC BY-SA4.0, XML et licence conservés.
Dante/Pline : sources historiques fournies dans le dépôt Michael A. Greshko;
code/source selon licence jointe. Greshko2025, The Naibbe cipher,
DOI10.1080/01611194.2025.2566408. Les chiffres de phase10 sont nos témoins construits,
pas une réexécution du chiffre Naibbe.
Les lignes Naibbe/Timm du snapshot ne sont pas utilisées dans cette phase.
Timm et Schinner, DOI10.1080/01611194.2019.1596999; licence MIT jointe.
