VOYNICH | ÉDITION PILOTE DE 12 PAGES | 28 OCTOBRE 2026

Ce dossier constitue un travail de transcription et de localisation sur
images. Il ne contient aucune traduction ni nouvelle clé de déchiffrement.

LIRE LE DOSSIER
output/pdf/Voynich_pilote_12_pages_2026-10-28.pdf : édition de 44 pages avec
bilan, conventions, quatre paires d'extraits, deux divergences laissées
ouvertes, douze fac-similés et les deux lectures de chacun des 384 loci.
Les liens internes relient fac-similés et lectures comparées.
results/aligned_loci.csv et .json : toutes les lectures, originales et
débarrassées de leurs seuls commentaires, les états d'accord, les réserves,
les identifiants d'image et les coordonnées des huit régions cibles.
results/image_annotations.json : coordonnées en pixels de la source et
commentaires de la relecture. Les cadres sont des rectangles approximatifs,
pas une segmentation exacte du contour de chaque glyphe.
data/page_image_map.json : association des douze pages aux images Yale.
data/image_sources.json et yale_manifest.json : provenance officielle.
images/ : quatorze JPEG de résolution native, sans retouche. Deux vues
supplémentaires ont servi à distinguer les panneaux des dépliants ; elles
ne sont pas ajoutées aux douze pages du pilote.

RÉSULTATS ET LIMITES
384 loci dans l'union des deux sources : 164 accords après suppression des
commentaires ; 29 accords seulement après normalisation ; 188 divergences ;
1 locus absent de ZL ; 2 absents de IT. Un accord de transcription n'est pas
une certitude paléographique. Un locus peut être une ligne, une légende, un
texte circulaire ou un autre petit élément écrit.
127 loci ont un marqueur d'incertitude (virgule, alternative ou illisible).
130 loci sont signalés si l'on inclut aussi les codes de signes rares.
Un signe rare correctement codé n'est pas nécessairement incertain.

Les quatre paires proviennent de la phase 2. Trois résistent à la fusion
ou séparation des espaces incertains et à toutes les variantes explicites
des lignes concernées. La quatrième, okols, dépend de l'espace douteux dans
ZL f89v2.21 : okols,sheey peut aussi être lu comme une unité okolssheey.
C'est une correction de la portée de notre sélection précédente, pas une
preuve que l'une de ces deux segmentations est la bonne.

Les huit emplacements ont été examinés par l'assistant à l'aide des lectures
ZL et IT. Ce contrôle n'est ni aveugle ni une expertise humaine indépendante.
Le statut de lecture reste provisoire. Les 376 autres loci sont importés
et comparés informatiquement, sans certification visuelle de chaque signe.
La vérification d'un mot cible ne certifie pas le reste de sa ligne.
Chaque meaning demeure UNKNOWN.

NORMALISATION
Les chaînes diplomatic_* conservent la ponctuation, les alternatives,
les ligatures et les codes de signes rares ; elles retirent les commentaires
et les balises de début/fin de paragraphe. Elles gardent <-> et <~>.
Les codes N/accord_apres_normalisation reprennent la convention de la phase 1,
qui choisit la première alternative et sépare les espaces incertains. Les
tests des quatre paires développent au contraire toutes les alternatives
explicites de leurs lignes. Aucun texte clair n'est inféré.

REPRODUIRE
Conserver voynich_20261028 et voynich_phase3 comme dossiers voisins.
Python 3.12 ; pillow, reportlab, matplotlib et pypdf pour le document.
Depuis voynich_phase3 :
  python audit_transcription.py
  python make_edition.py
  python verify_pilot.py
Le téléchargement peut être refait par download_images.py à partir du
manifeste enregistré. Les JPEG complets sont déjà inclus : aucun réseau
n'est requis pour reconstruire l'édition.
Les PNG et JPEG dans tmp/ sont des dérivés de travail et ne sont pas livrés.
Le PDF emploie des fac-similés réduits et compressés ; utiliser les originaux
dans images/ pour examiner les détails. Aucun trait n'a été reconstruit.

SOURCES ET CRÉDITS
Photographies : Cipher manuscript (Voynich manuscript), General Collection,
Beinecke Rare Book and Manuscript Library, Yale University.
https://collections.library.yale.edu/catalog/2002046
https://collections.library.yale.edu/manifests/2002046
Les déclarations de droits et métadonnées du fournisseur sont conservées
intégralement dans le manifeste. L'étude ne leur attribue pas de nouvelle
licence et ne revendique aucune propriété des photographies.

Transcriptions : ZL3b-n (Zandbergen-Landini) et IT2a-n (Takahashi, version
interlinéaire), disponibles via René Zandbergen. En-têtes et crédits conservés.
https://www.voynich.nu/transcr.html
Format IVTFF : document 2.0.2 du 8 juillet 2025, version du format 2.0.1.
https://www.voynich.nu/software/ivtt/IVTFF_format.pdf
Descriptions de contrôle des panneaux :
https://www.voynich.nu/q15/index.html
https://www.voynich.nu/q19/index.html
https://www.voynich.nu/q17/index.html
https://www.voynich.nu/q20/index.html

Le manifeste SHA256_MANIFEST.json de l'archive permet de vérifier chaque
fichier. Les images sources et les lectures historiques sont conservées,
y compris les éléments qui divergent ou dont la segmentation reste ouverte.
