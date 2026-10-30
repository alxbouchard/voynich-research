VOYNICH - PHASE 15 - 29 OCTOBRE 2026

Cette expérience teste des transformations courtes et partagées entre étiquettes pharmaceutiques et prose. Elle ne décode pas les signes et ne propose aucune traduction.

RÉSULTAT
Dans les quatre configurations, les transformations apprises diminuent le contraste entre le bon feuillet et les cinq autres, par rapport à l'identité seule. Aucun des tests exacts ne fournit un signal convaincant. Les contrôles artificiels récupèrent 120 liens préfixés connus et zéro lien dans le cas déconnecté.

LIRE
output/Voynich_phase15_variantes_et_prediction.pdf
PROTOCOL.json et ADDENDUM.txt

REPRODUIRE
Depuis le répertoire voynich_phase15, avec Python 3, numpy et threadpoolctl:
  python3 src/controls.py
  python3 src/experiment.py
  python3 src/verify.py
La commande experiment.py lance quatre processus indépendants. Elle réapprend six modèles pour chacune des 720 affectations possibles de textes à des blocs d'étiquettes, dans chacune des quatre conditions. Un seul cas peut aussi être exécuté:
  python3 src/experiment.py --case ZL strict
  python3 src/experiment.py --case IT lattice
La construction des candidats sans les données de test est vérifiée à la fin de chaque cas. Les sorties standard indiquent le progrès. Aucun accès réseau n'est requis.

RAPPORT
Avec ReportLab et les polices DejaVu dans /usr/share/fonts/truetype/dejavu:
  python3 src/make_report.py
Les commandes de contrôle graphique utilisent pdftoppm, si installé.

DONNÉES
data/ZL3b-n.txt: translittération ZL, version 3b, 13 mai 2025.
data/IT2a-n.txt: translittération IT, version 2a.
data/IVTFF_format.txt: règles documentaires, y compris crochets, virgules, ligatures et interruptions par dessin.
Copies des données de la phase 14; page source: https://voynich.nu/transcr.html
Les empreintes SHA-256 sont conservées dans SOURCE_MANIFEST.json et SHA256SUMS.json.

UNITÉS ET VALIDATION
Six feuillets physiques: f88, f89, f99, f100, f101, f102. Toutes leurs faces et tous leurs panneaux restent ensemble. Les 16 pages/panneaux de prose pharmaceutique sont utilisés, y compris f101r, qui ne porte pas d'étiquette admissible mais appartient à f101.
Le critère est la moyenne des fractions par feuillet, pas un ratio calculé sur toutes les étiquettes regroupées. Le test compare le texte de son propre feuillet à ceux des autres.
La branche strict est conservatrice. La branche lattice conserve des alternatives explicitement présentes et permet des fusions bornées. Ce n'est ni une segmentation phonétique conjointe ni un modèle de langue historique.
La famille de règles, le soutien minimum et le seuil d'amélioration figurent dans le protocole établi localement avant le calcul. Aucune préinscription externe.

FICHIERS DE RÉSULTATS
ZL_strict.json, IT_strict.json, ZL_lattice.json, IT_lattice.json: résultats complets, règles par feuillet exclu, matches détaillés et 720 permutations par cas.
summary.json: synthèse des quatre cas.
controls.json: contrôle positif avec préfixe q et contrôle négatif.
q_prefix_descriptive.json: diagnostic exploratoire ajouté après les résultats, sans test confirmatoire.
verification.json: réajustements observés, p recomptés et contrôles directs des correspondances strictes.
portable_verification.json: reproduction complète depuis une extraction fraîche, si présente dans cette version livrée.

INTERPRÉTATION
Ce résultat ne démontre pas l'absence de sens. Il limite seulement l'intérêt des transformations d'extrémités testées pour retrouver un lien local entre étiquettes et texte. Les deux translittérations ne sont pas deux manuscrits indépendants. Les six feuillets offrent une puissance limitée et peuvent partager du contenu. Les données de test étaient déjà présentes dans les travaux antérieurs; elles sont exclues de l'ajustement de cette phase, pas inconnues de l'analyste.
Les contrôles synthétiques appartiennent à la famille du modèle. Aucune sensibilité générale aux morphologies historiques n'est revendiquée.

SOURCES DOCUMENTAIRES CONSULTÉES
https://voynich.nu/extra/labels.html
https://voynich.nu/hist/stolfi/grammar.html
https://arxiv.org/abs/2610.34499 (prépublication déposée le 25 octobre 2026, non reproduite ici)

Aucun fichier d'authentification ni outil de transfert ne fait partie de cette archive.
