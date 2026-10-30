VOYNICH - PHASE 16 - 29 OCTOBRE 2026
Audit de deux points d'appui historiques : alphabets marginaux f1r et ligne mixte f116v.
Aucune traduction validée. Cette étude exploratoire vérifie des pistes déjà publiées.

REPRODUCTION
Python 3 + Pillow pour les images. ReportLab pour régénérer le PDF.
python3 src/analyse.py
python3 src/audit_images.py
python3 src/verify.py
python3 src/make_report.py

results/analysis.json contient les concordances avec loci et lignes originales, les quatre clés partielles fixes, les sorties mécaniques et les lignes entièrement substituables.
PROTOCOL.json a été écrit avant les calculs de cette phase, mais après consultation de sources et de résultats négatifs publiés. Ce n'est pas une préinscription indépendante.
ADDENDUM.txt documente la requête jointe ajoutée après le résultat et la correction d'orientation EXIF.

Ne pas interpréter le pourcentage de groupes substituables comme un pourcentage de texte déchiffré.
Les clés f1r ne couvrent qu'un sous-ensemble de la table préliminaire publiée. Les lignes marquées comme incertaines dans cette table ont été écartées; j/k est traité par choix global fixé. Les signes inconnus restent visibles entre crochets. Aucun algorithme n'ajuste la clé à une langue ou à un dictionnaire.
La table est recodée manuellement en EVA à partir d'une lecture moderne, sans adjudication paléographique indépendante. Le calcul reste conditionnel à ce recodage et à la segmentation des unités.

f116v est absent de IT. ZL porte oror.sheey. La variante aror n'est pas imposée comme correction : elle est examinée parce qu'elle est publiée et parce que le premier signe reste discuté. La suite de f104r n'est pas une découverte de cette phase : Anton l'indiquait déjà le 21 avril 2016.

CRÉDITS IMAGES
Beinecke Rare Book & Manuscript Library MS 408, f1r, f104r et f116v.
Images multispectrales et référence couleur du jeu de 2014 : The Lazarus Project and The Chester F. Carlson Center for Imaging Science at Rochester Institute of Technology. Traitements de Roger Easton; mise à disposition par Lisa Fagin Davis en 2024.
Images publiques Yale : https://collections.library.yale.edu/manifests/2002046
Captures screenshot-696.png et screenshot-691.png : figures du billet de Lisa Fagin Davis du 8 septembre 2024, conservées comme références de l'audit. Aucun traitement génératif.

Les sorties tmp et les paramètres temporaires d'accès ne font pas partie du dossier livré. Les crops PNG conservent exactement les pixels des sources après orientation EXIF, avec leurs coordonnées dans results/image_audit.json.
