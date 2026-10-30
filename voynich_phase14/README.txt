VOYNICH - PHASE 14 - 29 OCTOBRE 2026

Résultat: aucune traduction validée. Cette phase vérifie les images et les étiquettes répétées; elle ne lance pas de nouveau décodeur phonétique.

LIRE D'ABORD
output/Voynich_phase14_images_et_etiquettes.pdf

DONNÉES ET PORTÉE
19 images originales Yale correspondant à 20 références de pages; choix raisonné, non aléatoire. Vue d'ensemble, puis 16 recadrages examinés sur 5 pages.
Translittérations: ZL3b-n, version du 13 mai 2025, et IT2a-n, copies conservées des données utilisées dans la phase 8. Leur provenance est documentée par https://voynich.nu/transcr.html . IVTFF_format.txt définit les codes.
Manifeste source: https://collections.library.yale.edu/manifests/2002046
Les URL exactes, dimensions, références de pages et SHA-256 sont dans data/image_sources.json.

Les étiquettes sont des loci documentaires, pas nécessairement des mots, des noms propres ou les noms des dessins les plus proches. Les lettres EVA ne présupposent aucune prononciation. Les catégories Lf, Ln, Lt et Lz sont des métadonnées de contexte, pas des traductions.

REPRODUIRE LE CALCUL
Depuis ce répertoire, avec Python 3 et numpy:
  python3 src/analyse_labels.py
Résultats: results/labels.json, results/parsed_loci.json et sortie standard JSON.
Le script conserve les variantes, rejette les loci inexistants et ne transforme pas les espaces incertains en espaces certains.
Le test principal contient 15 pages, 198 étiquettes ZL et 202 IT. Dans chaque fichier, 11 occurrences réapparaissent exactement dans la prose de leur page. 10 000 permutations de blocs, graine 20261029, p unilatéraux 0,279272 et 0,192981.
ZL et IT ne sont pas deux réplications indépendantes. L'échangeabilité des pages reste une approximation; les feuillets partagés ne sont pas modélisés comme des blocs physiques.
Les contrôles construits vérifient le logiciel, pas la validité d'un déchiffrement.

REPRODUIRE LES IMAGES ET LE RAPPORT
Avec Pillow:
  python3 src/build_audit.py
Avec ReportLab et les polices DejaVu dans /usr/share/fonts/truetype/dejavu:
  python3 src/make_report.py
Optionnel, reconstruire les planches d'ensemble et récupérer les JPEG manquants à partir des URL Yale:
  python3 src/prepare_images.py
Les 19 JPEG sont déjà inclus. Aucune connexion n'est requise pour refaire le calcul principal et les recadrages.

AUDIT VISUEL
results/image_audit.json: 16 lignes, coordonnées xyxy natives, variantes ZL/IT, notes d'inspection guidée et empreintes. audit/: PNG exacts, sans restauration générative, rotation ni accentuation. Les images du PDF sont réduites pour la mise en page.
L'examen n'était pas aveugle et ne vaut pas arbitrage indépendant de paléographe. Le locus f73v.1 reste très pâle. Les lectures divergentes et frontières linguistiques incertaines ne sont pas résolues.

PROVENANCE ET RECHERCHE
PROTOCOL.json: protocole local établi avant le calcul, pas une préinscription publique.
Sources documentaires supplémentaires consultées:
https://voynich.nu/extra/sta-aaa.html
https://www.ic.unicamp.br/~stolfi/EXPORT/voynich/98-02-01-lotsa-labels/labels-t.html
Aucun sens botanique, astronomique ou grammatical proposé sur ces pages n'a été utilisé comme vérité de référence.
Aucun transfert du modèle lexical de la phase 13 ni installation complète de TranscriptTool n'a été effectué ici.

INTÉGRITÉ
SHA256SUMS.json recense les fichiers de cette archive avant empaquetage, à l'exclusion de ce manifeste d'empreintes lui-même. Les résultats quantitatifs ont été recalculés à partir d'une extraction fraîche des données et scripts de l'archive.
