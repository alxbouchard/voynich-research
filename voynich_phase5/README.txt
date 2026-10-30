VOYNICH - PHASE 5 - LETTRES ET GROUPES DE DEUX LETTRES
28 octobre 2026

CONCLUSION
Aucune traduction validée. Aucune langue identifiée.
L'hypothèse testée est une clé fixe qui transforme chaque unité chiffrée
en une unité claire de une ou deux lettres. Plusieurs unités chiffrées
peuvent partager la même unité claire (homophonie).
Quatre inventaires seulement : latin/italien, CV/VC. Ce n'est pas une recherche
exhaustive des systèmes syllabiques, ni une réplication d'un article publié.

Huit contrôles : deux clés cachées par langue et inventaire.
Exactitude sur les UNITÉS réservées, pas sur les lettres :
Latin CV : 98,848079394 % (260 erreurs / 22 571 unités), deux clés.
Latin VC : 99,858789232 % (31 erreurs / 21 953 unités), deux clés.
Italien CV : 100 % (0 / 95 503 unités), deux clés.
Italien VC : 100 % (0 / 92 993 unités), deux clés.
Les contrôles italiens reconstituent exactement le texte normalisé réservé,
sans récupération des espaces ou de la ponctuation d'origine.

32 configurations Voynich et 32 témoins mélangés ont été exécutés.
Les 32 clés optimisées présentent au moins une incohérence de redécoupage
sur les segments réservés. Ce diagnostic concerne les clés retenues,
pas toutes les clés possibles et pas la famille syllabique entière.
Les groupes de deux lettres représentent de 0 à 6,861 % des unités décodées.
Les quatre meilleurs candidats par inventaire ont été appliqués sans
réajustement aux loci IT correspondants : le résultat demeure incohérent.
Cette sensibilité à la transcription est une analyse supplémentaire après
comparaison des variantes, décrite dans SUPPLEMENT.json.

FICHIERS PRINCIPAUX
output/pdf/Voynich_phase5_syllabes_2026-10-28.pdf : rapport de six pages.
PROTOCOL.json : protocole avant les résultats de la phase 5.
SUPPLEMENT.json : portée du diagnostic après comparaison ZL/IT.
src/syllabic.cpp : solveur homophonique sur alphabet clair de 32 unités.
run_syllabic.py : modèles, contrôles, encodage, recherche et scores.
verify_and_summarize.py : vérifications et diagnostics de découpage.
transcription_sensitivity.py : réutilisation des clés ZL sur IT, sans ajustement.
make_report.py : génération du rapport depuis les résultats vérifiés.
package_phase5.py : empaquetage et vérification des empreintes.
data/ : quatre dictionnaires, fréquences, entrées d'ajustement et d'évaluation,
  vérités et clés de contrôle séparées (jamais transmises au solveur C++).
results/ : 72 résultats, clés, paramètres, graines, sorties intégrales marquées
  NOT_A_TRANSLATION, vérification, comparaison ZL/IT et synthèse JSON.
SOURCES.json : provenance des sources et références bibliographiques.
ENVIRONMENT.json : versions de l'environnement ayant exécuté l'expérience.
SHA256_MANIFEST.json : empreintes des fichiers inclus dans l'archive.

Les modèles binaires dérivés et le programme compilé sont exclus de l'archive.
Ils sont reconstruits par les commandes suivantes. Les dépendances ciblées
des phases précédentes sont incluses en conservant leur chemin d'origine.
Les fac-similés photographiques restent dans le dossier séparé de la phase 3.
Aucune nouvelle transcription sur image n'est revendiquée dans cette phase.

REPRODUIRE
Après extraction, conserver tous les répertoires voynich_* côte à côte.
Prérequis : Python 3 et numpy ; compilateur g++ compatible C++17.
Pour le rapport : reportlab et matplotlib ; Poppler pour rendre les pages.
Depuis le répertoire parent de voynich_phase5 :

g++ -O3 -std=c++17 voynich_phase5/src/syllabic.cpp -o voynich_phase5/src/syllabic
python3 voynich_phase5/run_syllabic.py --controls --force
python3 voynich_phase5/run_syllabic.py --real --force
python3 voynich_phase5/verify_and_summarize.py
python3 voynich_phase5/transcription_sensitivity.py
python3 voynich_phase5/make_report.py

Sans --force, les résultats individuels déjà présents sont réutilisés.
Le calcul des modèles est toujours renouvelé à partir des corpus normalisés.
Seuls les modèles dont les deux contrôles atteignent 95 % sont appliqués au
Voynich. Dans cette exécution, les quatre passent. La vérification intégrale
ci-dessus attend donc 8 contrôles et 64 essais réels/témoins.
Une autre bibliothèque C++ peut modifier le parcours pseudo-aléatoire.

PARAMÈTRES ET CONVENTIONS
Alphabet normalisé : abcdefghilmnopqrstuvxyz, 23 lettres ; j devient i,
k devient c, w devient uu. Les diacritiques, espaces et ponctuations sont
retirés. Voyelles : a,e,i,o,u ; y est une consonne dans cette convention.
Chaque inventaire ajoute les neuf paires CV ou VC les plus fréquentes dans
le seul corpus d'entraînement. Découpage glouton de gauche à droite, priorité
aux paires, puis aux lettres isolées. Les frontières de mots ne sont pas
présentes dans les corpus normalisés : une paire peut les traverser.
Il s'agit d'unités orthographiques, pas d'une syllabification phonologique.

Modèle latin : César (317 080 lettres). Contrôle : Pline (52 641 lettres).
Modèle italien : Enfer et Purgatoire (268 869 lettres). Contrôle : Paradis
(133 933 lettres). Une copie unique de Dante est utilisée, contrairement au
fichier brut qui contient deux copies identiques. Le contrôle italien reste
du même auteur que son modèle. Deux clés ne créent pas deux textes indépendants.

Chaque contrôle utilise 48 signes chiffrés, au moins un pour chaque unité
présente, puis des homophones supplémentaires répartis d'après les fréquences
du modèle. Le solveur reçoit uniquement le modèle, les fréquences et le
texte chiffré. Les 24 000 premières unités chiffrées servent à l'ajustement.
Le reste, découpé par segments de 80 unités, sert à l'évaluation exacte.

Score de recherche : somme des log-probabilités conjointes de quatre unités,
moins 4*N*KL(fréquences des unités de sortie || fréquences du modèle).
Lissage : 0,01 par case du modèle de 32^4 fenêtres ; 0,5 par unité de fréquence.
Huit départs de 60 000 propositions ; échanges et réaffectations ; température
initiale 0,002*N, décroissante, puis amélioration locale. Graine : 20261030.
Les scores du rapport excluent la pénalité de fréquence et sont en bits par
quatre UNITÉS. Ils ne se comparent pas directement aux scores par quatre
lettres de la phase 4, ni entre inventaires distincts. Aucun réglage de
calibration supplémentaire n'a été effectué dans la phase 5.

VOYNICH
Transcription ZL3b ; paragraphes Currier A/B séparés ; EVA ou unités composées ;
sens direct ou inverse. Inverse signifie renverser chaque segment retenu,
pas renverser le manuscrit ou l'ordre des pages.
Unités composées : ckh, cth, cph, cfh, ch, sh, iiiin, iiin, iin, in, puis
caractères restants, extraits à l'intérieur des mots transcrits.
Unités observées au moins 10 fois dans le pool d'ajustement ; plafond 64.
Les lectures alternatives [a:b], les signes inconnus/rares et les interruptions
graphiques créent des coupures, sans sélectionner silencieusement une variante.
La virgule incertaine est une frontière avant l'extraction composée.
Segments de moins de quatre unités exclus. Ajustement plafonné à 24 000 unités.
Même séparation par feuille physique que la phase 4 : une feuille sur cinq
dans l'ordre trié des identifiants est réservée. Les deux faces d'une feuille
restent dans le même ensemble. Ce corpus a déjà été vu dans des phases antérieures.

DIAGNOSTIC DE COHÉRENCE
Le texte obtenu en développant les unités doit redonner les mêmes unités
quand on le découpe de nouveau avec le même dictionnaire. Si ta est choisi,
une clé qui produit t puis a viole le découpage glouton imposé.
Ce contrôle n'est pas une contrainte dure de l'optimisation actuelle.
Il est calculé après la recherche et révèle des candidats inadmissibles.
Les deux vérifications indépendantes, redécoupage et jonctions illégales,
concordent sur les 72 essais. La conformité seule ne prouverait aucun sens.

L'analyse IT utilise les clés au meilleur score réservé non pénalisé dans
chacun des quatre inventaires. C'est une sélection après comparaison.
Les clés restent figées. Les loci communs sont alignés par page et numéro ;
ZL détermine le groupe et l'ensemble réservé. ZL et IT ne sont pas deux lectures
entièrement indépendantes. Des séquences encodées égales peuvent inclure des
coupures inconnues. Les scores peuvent porter sur des longueurs différentes.

CRÉDITS ET LICENCES
Transcriptions : crédits intégraux dans les en-têtes ZL3b et IT2a.
César : Perseus Digital Library, De Bello Gallico, CC BY-SA 4.0 :
https://creativecommons.org/licenses/by-sa/4.0/
Le corpus latin normalisé et ses copies conservent cette licence. Modifications :
retrait du balisage, notes, titres, espaces et diacritiques ; j/i, k/c, w/uu.
Les métadonnées originales sont conservées dans caesar.xml.
Pline et Dante : fichiers fournis par Michael A. Greshko. Licence conservée
dans voynich_20261028/controls/LICENSE_GRESHKO.
Citation requise : Michael A. Greshko (2025), The Naibbe cipher: a substitution
cipher that encrypts Latin and Italian as Voynich Manuscript-like ciphertext,
Cryptologia, DOI 10.1080/01611194.2025.2566408.
Les tables et le chiffrement Naibbe ne sont pas utilisés dans cette phase.
Contexte scientifique : George Lasry (2024), Deciphering Historical Syllabic
Ciphers, HistoCrypt 2024, DOI 10.58009/aere-perennius0106.
Notre méthode limitée n'est pas une reproduction de sa méthode générale.

Les vérifications réussies certifient les calculs et les diagnostics, pas le
déchiffrement. La recherche ne couvre pas les longues syllabes, tous les
inventaires, les signes nuls, les clés variables et toutes les langues.
