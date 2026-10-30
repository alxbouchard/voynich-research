VOYNICH, PHASE 6 - 28 OCTOBRE 2026
Recherche documentaire et expériences contrôlées. Aucune traduction validée.

LIRE D'ABORD
output/pdf/Voynich_phase6_etude_approfondie_2026-10-28.pdf
results/summary.json et results/verification.json
references/bibliography.json : références et niveau d'accès réel.

ÉTENDUE
17 références principales, sans prétention de revue exhaustive.
80 nouvelles exécutions : 8 contrôles initialisés par fréquences, 8 contrôles
avec initialisation apprise, 32 configurations réelles et 32 témoins mélangés.
Deux étapes par cas sélectionné : la recherche de phase 5 puis la recherche
sous contraintes de phase 6. La vraie clé n'est jamais passée au solveur.
8 jeux de voisinage x 2 modèles nuls x 100 permutations = 1 600 tirages.
Les essais réels du solveur utilisent ZL ; le voisinage compare ZL et IT.
Les contrôles à deux clés partagent un même ouvrage. Ils ne sont pas des
contrôles indépendants de genre, de langue ou de bruit.

REPRODUCTION
Python 3.12, NumPy, matplotlib, reportlab et g++ (C++17).
Depuis le dossier racine contenant voynich_phase6/ et les phases antérieures :

  g++ -O3 -std=c++17 voynich_phase6/src/constrained.cpp -o voynich_phase6/src/constrained
  g++ -O3 -std=c++17 voynich_phase6/src/constrained_warm.cpp -o voynich_phase6/src/constrained_warm
  python3 voynich_phase6/run_constrained.py --controls --force
  python3 voynich_phase6/run_constrained.py --controls --warm --force
  python3 voynich_phase6/run_constrained.py --real --force
  python3 voynich_phase6/adjacency_diagnostics.py
  python3 voynich_phase6/verify_phase6.py
  python3 voynich_phase6/make_report.py

Les modèles binaires de phase 5 sont reconstruits automatiquement depuis les
corpus normalisés s'ils sont absents. Les paramètres et les graines sont fixes.
L'option --hot est présente dans le code mais n'a jamais été exécutée.
Sans --force, les résultats déjà présents sont relus au lieu d'être recalculés.
Le vérificateur recalcule les scores à partir des clés sans relancer la recherche.
Les clés apprises de phase 5 sont incluses et correspondent aux amorces fournies.
Pour refaire aussi cette étape : compiler voynich_phase5/src/syllabic.cpp,
puis lancer run_syllabic.py --controls --force et --real --force.
Pour refaire les sources antérieures, voir leurs propres README et métadonnées.
Le plafonnement de l'ajustement à 24 000 unités et la séparation par feuillet
physique sont hérités de la phase 5. Le tri de feuillets est lexicographique.
Les scores sont en bits par séquence de QUATRE UNITÉS, pas par caractère.
Les digrammes CV/VC sont des unités orthographiques, pas de vraies syllabes.

DIAGNOSTIC DE VOISINAGE
adjacency_inputs.json conserve chaque position et les lectures exclues (null).
Les alternatives, groupes à virgule ambiguë et signes rares ne sont pas forcés.
Les paires ne franchissent ni barrière inconnue ni ligne. Le second modèle nul
fixe le premier et dernier mot RETENU de chaque ligne, non nécessairement les
mots graphiques extrêmes lorsque ceux-ci sont incertains.
Les contrôles textuels utilisent une disposition ZL artificielle. Dante conserve
32 824 / 33 409 mots et Naibbe 32 824 / 34 809 ; Pline et Timm sont entiers après
leur nettoyage (8 954 et 10 823 mots). La ligne initiale publiée de Timm, issue du
Voynich, est retirée ; cela n'efface pas le choix des paramètres ni l'amorce du
générateur. Aucun générateur Timm n'a été réexécuté dans cette phase.
Le fichier Naibbe provient d'une exécution des phases précédentes, non d'une
nouvelle génération. Le programme de production complet n'est pas requis pour
reproduire les mesures de phase 6 ; le texte généré utilisé est inclus.
Les jeux ont des longueurs et des genres différents. Les quantiles des mélanges
ne sont pas des intervalles de confiance des observations. Valeurs p brutes
exploratoires seulement, sans correction des comparaisons multiples.

LIMITES DE VALIDATION
Aucune nouvelle analyse matérielle, chimique ou multispectrale.
Aucune nouvelle transcription experte aveugle et aucune langue identifiée.
Aucune réplication intégrale des travaux externes cités, aucun Transformer exécuté.
Les feuillets réservés ont été consultés dans plusieurs phases : une confirmation
finale nécessitera une nouvelle réserve indépendante. Les meilleurs scores par
inventaire sont des choix a posteriori et non des découvertes linguistiques.

CRÉDITS
Les sources des phases 1 à 5, leurs crédits et licences sont conservés.
César / Perseus : CC BY-SA 4.0, voir voynich_phase2/SOURCES_AND_LIMITS.json.
Timm et Schinner : A possible generating algorithm of the Voynich manuscript,
Cryptologia 44(1), 2020, publié en ligne 2019, DOI 10.1080/01611194.2019.1596999.
Échantillon : https://github.com/TorstenTimm/SelfCitationTextgenerator
executable/generate/generated_text.txt, blob Git 31b5f847097d6c31e210d1ebc23ea9878f456607.
Licence MIT dans data/LICENSE_TIMM.txt ; empreinte des octets inclus dans SOURCES.json.
Greshko, Michael A. (2025), The Naibbe cipher: a substitution cipher that encrypts
Latin and Italian as Voynich Manuscript-like ciphertext, Cryptologia,
DOI 10.1080/01611194.2025.2566408. Licence avec citation obligatoire conservée dans
voynich_20261028/controls/LICENSE_GRESHKO.
Les titres et résumés courts du rapport renvoient aux sources ; les articles
intégraux, les scans d'images et les téléchargements de travail ne sont pas inclus.

INTÉGRITÉ
SHA256_MANIFEST.json à la racine de l'archive couvre tous les fichiers inclus,
sauf ce manifeste lui-même. Les binaires compilés et les modèles LM .bin sont
exclus ; le code et les données permettent de les reconstruire.
