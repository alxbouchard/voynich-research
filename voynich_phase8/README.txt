VOYNICH - PHASE 8 - 28 OCTOBRE 2026

Résultat : les scores de phase 7 ne permettent pas de corriger automatiquement les espaces incertains. Accord avec IT : 716 / 1 089, soit 65,7 %, contre 64,3 % pour toujours séparer. Sur les scores <= 0,1 ou >= 0,9 : 252 / 319 accords et 67 désaccords.

Le rapport PDF contient une comparaison chiffrée et sept zones d'image. Six cibles ont été sélectionnées avant leur examen ciblé, par extrema du score sur trois pages prédéfinies. Un septième désaccord a été ajouté après le calcul et est identifié comme tel. Examen de l'assistant non aveugle, assisté par les transcriptions ; aucun contrôle indépendant de paléographe.

AUCUNE TRADUCTION OU CORRECTION AUTOMATIQUE.
Les 2 394 virgules restent présentes dans results/transcription_variant_ledger.json. L'accord avec IT n'est pas une vérité linguistique. Les scores ne sont pas des probabilités étalonnées de lecture correcte. Les images sont des découpes exactes, sans restauration générative. Aucune largeur de blanc en pixels n'est revendiquée.

REPRODUCTION
Conserver la structure voynich_phase8/.
Python 3, numpy, Pillow, scikit-learn, matplotlib, reportlab (versions dans ENVIRONMENT.json).
Depuis le répertoire contenant voynich_phase8 :
  python3 voynich_phase8/research.py
  python3 voynich_phase8/build_audit.py
  python3 voynich_phase8/verify.py
  python3 voynich_phase8/make_report.py

Les trois premiers scripts reproduisent les calculs, les découpes à partir des coordonnées d'audit et les vérifications. Ils ne refont pas l'identification visuelle manuelle. make_report.py reconstruit le PDF. Les extraits figés de phase 7 sont inclus dans data/source_*.json ; leurs empreintes d'origine et d'extrait figurent dans data/source_lineage.json. La chaîne complète des phases 1 à 7 n'est pas réexécutée par cette archive.

CONTENU
PROTOCOL.json : choix de cette étape, fixés avant ses calculs, sans prétention de préenregistrement indépendant.
data/paired_uncertain.json : 1 089 comparaisons strictes.
results/transfer_summary.json : résultats, dix tranches de scores, sous-ensembles, bootstrap descriptif par cahier (2 000 tirages).
results/extreme_disagreements.json : les 67 désaccords aux scores extrêmes.
results/image_audit.json : sept localisations, coordonnées natives, variantes ZL/IT, limites.
results/transcription_variant_ledger.json : les 2 394 frontières incertaines préservées, avec canaux d'évidence distingués.
results/verification.json : vérification des données et calculs, pas validation des lectures manuelles.
data/*.jpg : quatre JPEG sources Yale. results/crop_*.png : sept découpes exactes.
Les frontières x des flèches sont approximatives. Les offsets de texte renvoient aux fragments conservés en phase 7, pas à l'intégralité brute d'un locus.

SOURCES
Yale University Library, Beinecke MS 408 : https://collections.library.yale.edu/catalog/2002046
Images 1006076 (f1r), 1006208 (f75r), 1006254 (f103r), 1006271 (f113v).
René Zandbergen : https://voynich.nu/extra/sp_transcr.html
Transcriptions figées ZL3b-n et IT2a-n, cette dernière de Takeshi Takahashi.
Les contenus de tiers restent attribués à leurs auteurs et institutions. Aucune nouvelle licence n'est imposée sur ces sources.
