VOYNICH, PHASE 2 | 28 OCTOBRE 2026

Résultat : aucune traduction validée. Les clés et extraits sont des candidats
statistiques, explicitement NON_TRANSLATION. Une optimisation réussie du score
ne démontre ni une langue ni un sens.

CONTENU
Le dossier voynich_20261028 voisin contient les deux transcriptions IVTFF,
leur parseur vérifié, les sources et contrôles de la phase 1. Conserver cette
arborescence après extraction. voynich_phase2 contient les nouveaux corpus,
le solveur C++, les 30 configurations, les contrôles à clé cachée et l'index
de 729 légendes. Le rapport PDF résume les observations et leurs limites.

REPRODUCTION
Python 3.12, numpy, pandas, lxml ; g++ pour le solveur C++17.
Rapport : reportlab, matplotlib. Versions complètes de la phase 1 dans
voynich_20261028/requirements.txt. Dans le dossier voynich_phase2 :

  python prepare_sources.py
  g++ -O3 -std=c++17 src/solve.cpp -o src/solve
  python search_keys.py
  python extended_search.py
  python labels.py
  python verify_phase2.py
  python make_report.py

Les sources sont incluses, aucun téléchargement n'est requis. Les résultats
peuvent varier légèrement entre compilateurs : générateur pseudo-aléatoire
fixé, mais bibliothèque C++ et arrondis flottants peuvent modifier le chemin
d'optimisation. Les résultats fournis correspondent à cette exécution.

DÉFINITIONS ET LIMITES
Les champs historiques *_cross_entropy_bits désignent ici une moyenne de
-log2 p(quatre lettres), en bits par fenêtre de quatre lettres. Il ne s'agit
pas d'entropies par caractère. Comparer directement les modèles de deux
langues ne permet pas d'identifier la langue du manuscrit.
Le solveur teste des substitutions bijectives entre 26 symboles et lettres.
Les regroupements EVA sont une convention expérimentale, pas un alphabet
voynich établi. Les variantes COMPOSED utilisent les 26 unités fréquentes
dans les feuillets d'apprentissage uniquement. Les unités rares et les
caractères incertains interrompent les segments dans les essais étendus.
Les quatre premiers essais EVA de search_keys.py retirent les mots incertains
via r['clean'], puis concatènent les mots ; cette convention peut créer des
voisinages artificiels. Les essais étendus conservent les ruptures et servent
à contrôler cette limite. Les espaces sont retirés ; le sens inverse porte
sur chaque segment entier, pas sur la seule séquence des mots.
Les feuillets tenus à l'écart ne servent pas à optimiser les clés. Choisir le
meilleur de plusieurs scores sur ces feuillets reste exploratoire ; aucun
troisième ensemble de confirmation n'a été employé.
Naibbe : les tables morphologiques publiées sont données au décodeur ; seule
une permutation globale des lettres de sortie est cherchée. Le contrôle
ainsi obtenu est équivalent au contrôle latin, pas une troisième expérience
indépendante ni la résolution générale d'un Naibbe à tables inconnues.

Les deux contrôles linguistiques ont des clés de substitution cachées au
solveur. Latin : modèle César ; message Pline ; 24 000 lettres pour chercher
la clé, puis 28 641 lettres séparées pour évaluer (2 erreurs). Italien :
modèle Inferno + Purgatorio ; message Paradiso ; 24 000 lettres pour chercher
la clé, puis 109 933 séparées pour évaluer (aucune erreur). L'auteur est donc
commun au modèle et au contrôle italiens, contrairement au latin.
Le fichier Dante contient deux copies intégrales. La seconde est exclue.
Une première fonction de score conditionnel avait échoué sur le contrôle :
résultat conservé dans control_failed_conditional.json. Le score conjoint a
été choisi après cette calibration. PROTOCOL.json est un document de travail
antérieur aux résultats, pas un préenregistrement externe ; les variantes
italiennes et composées prolongent ce protocole de façon exploratoire.

Dans illustration_anchors.csv, chaque ligne est un locus de légende IVTFF.
paragraph_occurrences compte les lignes de texte courant contenant le mot,
pas ses occurrences multiples dans une même ligne. 258 est le nombre de
loci de légendes concordantes avec au moins une ligne correspondante,
pas le nombre de mots distincts. Accord ZL/IT ne signifie pas lecture certaine
ou indépendance des transcriptions. Le sens de chaque entrée reste UNKNOWN.
Les noms de mois en alphabet latin sont des ajouts plus tardifs, sans
alignement bilingue démontré avec les légendes en écriture voynich.

SOURCES ET DROITS
SOURCES_AND_LIMITS.json contient les URL fixées et les empreintes SHA-256.
César, De Bello Gallico : Perseus Digital Library, canonical-latinLit.
Le XML original porte la licence CC BY-SA 4.0. La version dérivée
data/latin_train.txt, sans notes/titres, normalisée en lettres a-z avec
j→i, k→c, w→uu, reste sous CC BY-SA 4.0 :
https://creativecommons.org/licenses/by-sa/4.0/
Dante et code/tableaux Naibbe : sources du dépôt Michael A. Greshko.
Conserver voynich_20261028/controls/LICENSE_GRESHKO. Référence demandée :
Greshko (2025), Cryptologia, DOI 10.1080/01611194.2025.2566408.
Les droits des transcriptions restent ceux de leurs auteurs, indiqués dans
les fichiers sources ; l'archive ne leur applique aucune nouvelle licence.
f71r_reference.jpg : vignette 337 × 480, Beinecke MS 408, via René Zandbergen,
https://www.voynich.nu/q11/f071r_crd.jpg. Inspection de la mise en page seulement,
résolution insuffisante pour une vérification paléographique des glyphes.

Le manifeste global SHA256_MANIFEST.json de l'archive liste les fichiers
livrés avec leur empreinte. Aucun compte ou identifiant privé n'est inclus.
