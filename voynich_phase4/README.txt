VOYNICH - PHASE 4 - TEST D'UNE SUBSTITUTION HOMOPHONIQUE FIXE
28 octobre 2026

CONCLUSION
Aucune traduction validée. Aucune langue identifiée.
Quatre contrôles positifs : deux clés sur Pline en latin, deux sur le Paradis
de Dante en italien. Ce sont deux textes, pas quatre textes indépendants.
Chaque contrôle chiffre 48 signes avec une clé absente des entrées du solveur.
Exactitude évaluée après les 24 000 lettres d'ajustement :
latin 96,784217877 % (921 erreurs / 28 640 lettres), italien 100 %
(0 erreur / 109 933 lettres), pour les deux clés de chaque langue.
Le dernier caractère isolé de Pline est exclu des segments évaluables.

16 configurations Voynich et 16 témoins mélangés ont été exécutés.
Les unités expérimentales ne constituent pas un alphabet validé du manuscrit.
Le score mesure des fenêtres de quatre lettres, pas le sens d'un texte.
Sur le contrôle latin, la sortie erronée obtient même un meilleur score que
le texte exact. Les bons scores des candidats ne sont donc pas un déchiffrement.

CONTENU
output/pdf/Voynich_phase4_homophonie_2026-10-28.pdf : rapport de 5 pages.
PROTOCOL.json : hypothèse, paramètres et critères avant les nouveaux résultats.
run_homophonic.py : préparation des corpus, contrôles, encodage, essais.
src/homophonic.cpp : solveur C++ avec vérification interne des deltas de score.
verify_and_summarize.py : recalcul indépendant des scores et exactitudes.
make_report.py : génération du rapport à partir des résultats vérifiés.
package_phase4.py : constitution et vérification de l'archive.
data/ : entrées entières du solveur, corpus normalisés, fréquences, vérités
  des contrôles (fichiers séparés, jamais fournis au programme C++).
results/ : toutes les clés, tous les scores, l'audit d'encodage, les textes
  candidats complets explicitement marqués NOT_A_TRANSLATION, la vérification.
results/summary.json : résultats et groupes de symboles fusionnés par clé.
SOURCES.json : provenance et empreintes des sources brutes.
SHA256_MANIFEST.json, à la racine de l'archive : empreintes de tous les fichiers.
Les binaires compilés et les modèles binaires dérivés sont exclus de l'archive.
Ils sont reconstruits avec les commandes ci-dessous.

Des dépendances ciblées des phases précédentes sont incluses sous leurs
répertoires d'origine : parseur, protocole, transcriptions complètes ZL et IT,
format IVTFF, corpus sources et crédits. Les petits résultats du pilote
documentent les correspondances provisoires ; ses photographies complètes
restent dans l'archive séparée de la phase 3 déjà livrée.

REPRODUCTION
Après extraction, conserver les quatre répertoires voynich_* côte à côte.
Prérequis : Python 3, numpy ; g++ compatible C++17.
Pour le rapport : reportlab et matplotlib ; Poppler pour le contrôle visuel.
Depuis le répertoire parent de voynich_phase4 :

g++ -O3 -std=c++17 voynich_phase4/src/homophonic.cpp -o voynich_phase4/src/homophonic
python3 voynich_phase4/run_homophonic.py --controls --force
python3 voynich_phase4/run_homophonic.py --real --force
python3 voynich_phase4/verify_and_summarize.py
python3 voynich_phase4/make_report.py

Sans --force, les cas présents sont réutilisés. --real refuse de continuer si
les quatre contrôles ne passent pas 95 %. Un autre compilateur, une autre
bibliothèque C++ ou des paramètres modifiés peuvent changer l'optimisation.
Graine solveur : 20261028 ; graines du chiffrement : voir chaque résultat.
Aucune calibration supplémentaire n'a été faite dans cette phase.

CONVENTIONS
Alphabet de sortie : a-z ; la normalisation des corpus réduit j en i, k en c,
w en uu et retire les diacritiques et espaces. Le contrôle italien utilise
une seule copie de la Divine Comédie : le fichier source contient deux copies
identiques. Le modèle utilise Enfer/Purgatoire, le contrôle le Paradis.
Le modèle latin utilise César ; le contrôle utilise Pline, auteur distinct.
Score : log-probabilités conjointes de quatre lettres, lissage 0,01 par case.
Objectif maximisé : somme des scores - 4*N*KL(fréquences de sortie || modèle).
Huit départs de 60 000 propositions ; swaps et réaffectations de lettres ;
température initiale 0,002*N, décroissante ; amélioration locale finale.

Voynich : paragraphes ZL3b, groupes Currier A/B, EVA/composés, direct/inverse.
Le sens inverse renverse chaque segment, pas le manuscrit entier.
Unités composées : ckh, cth, cph, cfh, ch, sh, iiiin, iiin, iin, in,
puis caractères restants ; extraction à l'intérieur de chaque mot transcrit.
Sélection : unités présentes au moins dix fois dans le pool d'ajustement,
plafond 64 ; effectifs réels 19/20 en EVA et 28/29 en unités composées.
Les variantes [a:b], signes inconnus/rares et interruptions coupent le flux.
Aucune lecture alternative n'est choisie par défaut dans cette phase.
La virgule incertaine reste une frontière de mot pour l'extraction composée.
Segments de moins de quatre unités exclus ; cap d'ajustement 24 000 unités.
Les feuilles physiques sont séparées, avec une sur cinq réservée selon
l'ordre trié de leurs identifiants. Les meilleures variantes sont choisies
après comparaison ; aucune confirmation indépendante finale n'est prétendue.
Un seul mélange par cas, avec les mêmes effectifs dans chaque segment :
comparaison descriptive, sans p-valeur ni preuve de langue naturelle.

LIMITES ET ANCRAGES
okcheor, otcheody et otald ont une forme provisoirement robuste dans les
variantes du pilote. Leur sens reste inconnu. Ce ne sont pas des mots clairs
connus. Sous une clé fixe, l'identité de deux sorties est automatique.
okols est conditionnel à un espace incertain devant sheey : okolssheey reste
une lecture possible. Ce cas ne doit pas servir d'ancrage lexical robuste.
Cette phase n'écarte pas syllabaires, nomenclateurs, signes nuls, clés
variables, autres langues, autres segmentations ou chiffrement en général.

CRÉDITS ET LICENCES
Transcriptions : crédits et historique dans les en-têtes complets des sources.
César : Perseus Digital Library, De Bello Gallico, licence CC BY-SA 4.0 :
https://creativecommons.org/licenses/by-sa/4.0/
Le fichier latin_train.txt normalisé et ses copies restent sous CC BY-SA 4.0.
Modifications : retrait du balisage, des notes, titres, espaces et diacritiques,
normalisation j/i, k/c, w/uu. Métadonnées originales conservées dans caesar.xml.
Pline et Dante : fichiers fournis par Michael A. Greshko, crédits et licence
du dépôt conservés dans voynich_20261028/controls/LICENSE_GRESHKO.
Citation requise : Michael A. Greshko (2025), The Naibbe cipher: a substitution
cipher that encrypts Latin and Italian as Voynich Manuscript-like ciphertext,
Cryptologia, DOI 10.1080/01611194.2025.2566408.
Le modèle Naibbe et ses tables ne sont pas exécutés dans cette phase.
Référence de méthode : Nils Kopal (2019), Cryptanalysis of Homophonic
Substitution Ciphers Using Simulated Annealing with Fixed Temperature,
HistoCrypt 2019, p. 107-116. Notre solveur ne reproduit pas exactement cet article.
Kambhatla, Born et Sarkar (2023) figurent dans les références comme piste
de comparaison ; leur déchiffreur neuronal n'a pas été implémenté ici.

Les vérifications réussies concernent les calculs et le protocole exécuté.
Elles ne certifient pas le sens d'un candidat ni la lecture de chaque glyphe.
