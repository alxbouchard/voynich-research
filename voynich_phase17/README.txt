VOYNICH, PHASE 17 : IMAGERIE BRUTE ET CONTRAINTES DE DECHIFFREMENT

ETAT : aucune traduction validée du texte principal.

Cette expérience porte sur les annotations de f116v et sur une hypothèse
limitée de copie chiffrée d'une formule marginale. Elle ne prétend pas avoir
épuisé les modèles de chiffrement, les écritures, les langues ou les lectures.
Les 3 TIFF bruts de f1r téléchargés précédemment ne sont pas analysés ici.

REPRODUCTION
Python 3 avec NumPy, SciPy, Pillow, ReportLab. Les versions exactes sont dans
ENVIRONMENT.json. Depuis le dossier extrait :

OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 src/spectral.py
python3 src/make_figures.py
python3 src/crib_scan.py
python3 src/shuffle_diagnostic.py
python3 src/extend_crib.py
python3 src/make_report.py

spectral.py utilise par défaut les recadrages natifs du NPZ livré. Chaque
plan contient les pixels 16 bits originaux, après une rotation exacte de
90 degrés et un recadrage explicite. Aucune génération d'image ni invention
de traits n'est utilisée. Si ce NPZ n'existe pas, le script peut le reconstruire
à partir du dossier voisin voynich_resources, téléchargé lors de l'étape
précédente. Les TIFF complets ne sont pas dupliqués dans cette archive.

TRAITEMENT DES IMAGES
Région avant bord de sécurité : (2400,550)-(6050,1570), coordonnées après
rotation antihoraire de 90 degrés. La normalisation est un contraste relatif
au fond local, pas un étalonnage de réflectance ni une identification d'encre.
Les translations entières appliquées et les résidus de trois zones sont
conservés dans results/spectral.json. Les 22 bandes et neuf composantes sont
livrées, y compris les vues où le texte devient moins lisible.

RECHERCHE DE LA FORMULE
Lecture proposée, non établie comme texte clair : six marix morix vix.
Deux corpus du même manuscrit : ZL3b-n et IT2a-n, copiés sans modification.
Deux segmentations des caractères, deux traitements des espaces incertains,
deux sens et deux modèles de substitution. La recherche conserve d'abord
les quatre mots, puis supprime leurs frontières à l'intérieur des segments
autorisés. Les inconnues et lacunes interrompent la recherche.

Le protocole initial est PROTOCOL.json. Les diagnostics ajoutés après le
premier balayage sont déclarés dans ADDENDUM.txt : brouillages et extension
vers maria. Ils ne sont pas une validation indépendante ni un test statistique
confirmatoire. Les hypothèses « maria » et le groupe intermédiaire étaient
déjà connus des lectures publiées. Chaque candidat ne teste qu'un motif de
répétition sous une clé ajustée à la formule ; il n'en établit pas le sens.

Les fenêtres compatibles sont toutes dans results/crib_scan.json. Les valeurs
Latin de ces clés sont imposées par la formule recherchée, pas découvertes.
Ne jamais présenter ces fenêtres ou leurs substitutions comme une traduction.

CONTROLES
- 22 recadrages comparés exactement à une rotation/recoupe indépendante Pillow.
- Vérifications de signes répétés, homophonie, bijection et barrières.
- 6 817 comparaisons exhaustives sur petits alphabets.
- Vérification indépendante de chaque clé retenue et contrôle vectorisé du
  nombre de fenêtres ZL avant brouillage.
- Recalcul numérique depuis les seuls fichiers du dossier.
- Décodage strict des PNG et contrôle CRC de l'archive.

Les quelques PNG tronqués lors de la première écriture ont été recalculés
avec les mêmes paramètres. Aucun chargement tolérant les troncatures n'est
employé. La sauvegarde scientifique des PNG est maintenant atomique.

SOURCES
SOURCE_MANIFEST.json conserve les liens publics et les folios concernés.
Le parallèle erex/arex/rymex est documenté dans Jones et Olsan (2015), pages
412 et 414, figure 1, British Library Sloane 3160 f129v. Le PDF de l'article
et sa photographie ont été consultés ; ils ne sont pas redistribués ici.
Cette analogie de genre n'est pas une équivalence textuelle avec le Voynich.

CREDITS DES IMAGES DU VOYNICH
Beinecke Rare Book & Manuscript Library MS 408, f116v.
The Lazarus Project and The Chester F. Carlson Center for Imaging Science
at Rochester Institute of Technology. Captures de 2014 rendues publiques
en 2024. Les traitements de cette phase sont nouveaux et distincts des
traitements publiés par Roger Easton.
