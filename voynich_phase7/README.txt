VOYNICH PHASE 7 - 28 OCTOBRE 2026
Prédire les frontières et préserver les ambiguïtés. Aucune traduction validée.

RÉSULTAT
Le modèle local à quatre caractères retrouve environ 90 % des espaces nets ZL,
avec environ 90 % de précision, sur les cahiers exclus de l'apprentissage.
Un second modèle BPE ne voit aucun espace, même à l'apprentissage. Ses groupes
traversent 19,88 % des espaces incertains et 2,52 % des espaces nets à 64 fusions.
Ces résultats ne prouvent ni le sens du texte ni la nature linguistique des unités.
Le contrôle Naibbe prédit ses espaces encore mieux. Les fichiers sources font foi.

FICHIERS À LIRE
output/pdf/Voynich_phase7_espaces_2026-10-28.pdf
PROTOCOL.json : choix fixés avant l'exécution des modèles.
results/summary.json : six jeux et toutes les sensibilités.
results/annotated_uncertain_boundaries.json : 2 394 positions originales
incertaines, probabilités hors cahier et BPE. AUCUNE correction automatique.
results/verification.json, prediction_intervals.json, paired_transcriptions.json.
results/published_ink_gap_reanalysis.json : recalcul de mesures des auteurs,
pas une nouvelle campagne d'images, ni une étude indépendante.

REPRODUIRE
Python 3.12, NumPy, scikit-learn, matplotlib, reportlab ; g++ C++17.
Depuis le dossier contenant voynich_phase7/ et voynich_20261028/ :
  g++ -O3 -std=c++17 voynich_phase7/src/bpe.cpp -o voynich_phase7/src/bpe
  python3 voynich_phase7/research.py --force
  python3 voynich_phase7/followup_checks.py
  python3 voynich_phase7/verify.py
  python3 voynich_phase7/make_report.py
Sans --force, research.py relit les résumés déjà présents.
Les données brutes et leurs contrôles SHA-256 sont inclus. Les quatre témoins
préparés viennent de phase 6. Leur source exacte est documentée dans son dossier.
Les modèles compilés ne sont pas inclus ; les sources C++ le sont.

MÉTHODE
Utiliser le raw IVTFF, non la normalisation qui choisit une alternative.
Toute alternative de signe, caractère rare/inconnu ou interruption de dessin
crée une coupure. On retire les fragments de moins de 4 caractères. Pas de
passage entre lignes. Paragraphes Currier A/B uniquement, soit 14 cahiers.
Chaque cahier est absent du fit qui prédit ses propres positions.
Les contrôles ont 8 blocs contigus, avec des longueurs et genres différents.
L'apprentissage supervisé ignore les virgules incertaines dans la perte.
Les contextes sont calculés sur le flux sans espaces ; leur étiquette provient
uniquement des cahiers d'apprentissage. Lissage paire=16, contexte4=32,
seuil=.5, constants avant l'exécution. Un modèle de paire est aussi conservé.
La BPE fréquente apprend séparément sur les chaînes sans séparateurs. 64 fusions
est le choix principal, 0/32/128 les sensibilités fixées avant calcul.
Les unités composées initiales sont ckh,cth,cph,cfh,ch,sh,iiiin,iiin,iin,in,
reconnues en plus long d'abord sur le flux sans espaces. Ce choix n'impose pas
les frontières observées ; le taux de franchissement à zéro fusion est mesuré.
Chaque règle BPE est appliquée dans son ordre appris, de gauche à droite.
Les occurrences chevauchantes sont comptées dans la sélection des paires.
Les égalités sont tranchées par identifiant numérique, de façon déterministe.
Les labels 0/1/2 désignent intérieur/espace net/espace incertain.
Les 100 mélanges par jeu permutent les longueurs originales des morceaux dans
chaque fragment, tout en gardant le nombre et l'ordre des catégories de séparateurs.
Les 2000 bootstraps rééchantillonnent les cahiers des observations hors cahier.
Les entraînements se chevauchent entre plis : l'incertitude n'est pas celle
d'une étude indépendante, et aucun sens n'est inféré de ces intervalles.

LIMITES
Les jugements des transcripteurs ne sont pas une vérité linguistique. Ils peuvent
eux-mêmes être influencés par les formes voisines. ZL et IT partagent l'objet.
La comparaison exacte de loci peut retenir des fragments lorsque les mêmes
bords sont exclus ; elle ne garantit pas que toutes les lignes sont complètes.
Les contrôles réutilisent la disposition artificielle et les troncatures de phase 6.
Ce n'est pas une comparaison à tailles et genres appariés. Aucun chiffre nouveau
Naibbe ou texte Timm n'est généré dans cette phase.
Les exemples sont les premiers fragments de 30-80 caractères sans espace
incertain sur f1r/f2r/f75r/f103r, sans sélection par performance. f2r n'a pas de
fragment admissible et n'apparaît pas. Les 3 exemples montrent les erreurs.

CRÉDITS
Hypothèse et tests apparentés : Liudmila Rozanova et Alexander Temerev (2026),
A Glyph Is Not a Letter, a Token Is Not a Word, a Space Is Not a Space:
What the Units of Voynichese Are Not, arXiv:2608.17096v1.
https://github.com/lrozanova/voynich-units
Mesures d'encre : data/direct_pixel/results_unblinded.csv, blob Git
fb0788d339fd3486d6954357598c4c776713cbd5. Licence MIT conservée.
Les mesures des auteurs sont réanalysées ; leurs images ne sont pas redistribuées.
Leur code n'est pas exécuté : nos expériences sont une implémentation propre
de tests apparentés avec un protocole différent, pas une réplication intégrale.
Transcriptions ZL/IT : https://www.voynich.nu/transcr.html, crédits originaux inclus.
Greshko, Michael A. (2025), The Naibbe cipher: a substitution cipher that encrypts
Latin and Italian as Voynich Manuscript-like ciphertext. Cryptologia.
DOI 10.1080/01611194.2025.2566408. Licence avec citation obligatoire conservée.
Timm et Schinner (2019/2020), A possible generating algorithm of the Voynich
manuscript. DOI 10.1080/01611194.2019.1596999. Licence MIT du générateur conservée.
Les sources antiques/italiennes et crédits sont référencés par les métadonnées
des phases antérieures incluses. Les articles entiers ne sont pas redistribués.
