ÉTUDE VOYNICH, REPRISE DU 28 OCTOBRE 2026

Résultat : aucun déchiffrement validé. Ce dossier conserve une analyse
effectivement exécutée, ses données, ses résultats négatifs et ses limites.

1. CONTENU

output/pdf/Etude_Voynich_2026-10-28.pdf : rapport en français.
data/ZL3b-n.txt et data/IT2a-n.txt : transcriptions savantes complètes
  récupérées depuis https://www.voynich.nu/data/ et identifiées par SHA-256.
  Elles transcrivent le même manuscrit, pas deux témoins indépendants.
data/submitted_sample.txt : copie de l'extrait proposé dans la conversation.
data/IVTFF_format.pdf et IVTT_manual.pdf : documentation de René Zandbergen.
PROTOCOL.json : plan écrit après inspection du format et avant les calculs.
EXPLORATORY_ADDENDUM.json : test supplémentaire de clé publiée, spécifié
  avant de l'appliquer au manuscrit.
SOURCES.json : sources primaires, provenance et empreintes de blobs GitHub.
results/ : intégrité, comptes, analyses, partitions des modèles, résultats.
controls/ : code, tables et exemple latin publiés par Michael A. Greshko,
  puis fichiers générés clairement séparés sous controls/generated/.
controls/LICENSE_GRESHKO : licence MIT modifiée du matériel de Greshko.
MANIFEST_SHA256.json : empreintes des fichiers conservés dans cette édition.

2. REPRODUCTION

Environnement utilisé : Python 3.12.14; dépendances fixées dans requirements.txt.
Ouvrir un terminal dans ce dossier, puis exécuter dans cet ordre :

python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python analyse.py
python models.py
python naibbe_control.py
python key_probe.py
python make_report.py
python verify_study.py

Les fichiers de données étant joints, aucun téléchargement n'est nécessaire
pour reproduire les calculs. L'installation des dépendances demande Internet.
Le rapport utilise les polices DejaVu fournies avec matplotlib.
La graine est 20261028; elle est fixée pour les permutations et le chiffrement.

3. GARDE-FOUS D'INTERPRÉTATION

- data_real=true désigne une transcription publiée, vérifiée par empreinte
  et format. Ce n'est pas une vérification photographique de chaque glyphe.
- Les caractères latins EVA ne sont ni des sons attestés, ni nécessairement
  des unités sémantiques ou des glyphes indépendants.
- Les pourcentages de couverture d'une table ne sont pas des taux de traduction.
- La comparaison de e entre sections est exploratoire : les feuilles de bains
  proviennent d'un seul cahier. Les p nominaux supposent une échangeabilité
  des feuilles discutable dans ce contexte et ne démontrent pas « e = eau ».
- Les modèles par caractères mesurent une structure prédictible, pas le sens.
- Le contrôle Naibbe est une récupération à clé connue d'un texte normalisé.
  Il ne démontre ni une récupération de clé inconnue, ni le déchiffrement du
  Voynich. Sa clé inchangée ne donne pas de lecture complète du manuscrit.
- Les anciens essais cités dans l'historique ne sont pas repris comme preuves
  vérifiées sans leurs fichiers originaux.

4. CRÉDITS

Manuscrit original : Beinecke MS 408, Yale University Library.
Transcriptions : René Zandbergen / Gabriel Landini et Takeshi Takahashi,
  extraction de l'interlinéaire Landini-Stolfi, versions décrites dans SOURCES.json.
Documentation IVTFF : René Zandbergen.
Code, tables et texte de contrôle Naibbe : Michael A. Greshko.
Citer son article pour tout usage du code ou des jeux de données :
Greshko, Michael A. (2025). The Naibbe cipher: a substitution cipher that
encrypts Latin and Italian as Voynich Manuscript-like ciphertext. Cryptologia.
https://doi.org/10.1080/01611194.2025.2566408

Le présent dossier n'attribue pas à son auteur les transcriptions et travaux
antérieurs. Il ne doit pas être cité comme une solution du manuscrit.
