# Recherche bornée d'un ancrage sémantique indépendant

Consultation achevée le **17 novembre 2026 à 19:14:46 UTC**. **Aucun nouvel ancrage exploitable repéré dans ce périmètre.** Cela ne tranche ni la présence d'un message ni la possibilité d'un déchiffrement. Aucun calcul de modèle, aucune lecture IA d'image et aucune modification des données gelées de phase 51 n'ont été effectués.

Un ancrage admissible devrait relier une portion identifiée du texte principal à un contenu connu autrement que par la méthode à tester : texte parallèle, équivalence marginale attestée, ou ordre externe des étiquettes établi indépendamment. Une nouvelle ressemblance ou un contrôle de parseur ne suffit pas.

## Exclusion des travaux déjà faits

Les rapports 42–50 du dépôt ont été consultés avant la recherche : compteurs de f49v (42), modules Stalnecker (43), marge de f17r (44), liens entre fragments de plantes et grandes plantes (45–46), répertoire Naibbe (47), pipeline CMM (48), CTTS (49), moteur Luo (50). Les inventaires `docs/SOURCES.md` et `research/2026-10-30-methods/README.md` ont également été recherchés. L'imagerie multispectrale de 2024 et l'article sur les singulions y figuraient déjà; ils ne sont pas présentés ici comme de nouvelles découvertes.

**Les phases 45 et 46 ne réutilisent pas la piste Averyanov/Yoshida.** Elles partent des rapprochements iconographiques publiés par Zandbergen dans les cahiers 3 et 19, puis cherchent la récurrence exacte ou approximative des étiquettes dans la prose des grandes plantes associées. La phase 45 teste trois rapprochements forts; la phase 46 neuf étiquettes de rapprochements plus faibles. Elles ne supposent ni noms de degrés zodiacaux, ni table d'al-Biruni, ni décalage 23, ni sigles de deux lettres. Leur référence est [le catalogue du cahier 19](https://www.voynich.nu/q19/index.html), et non les deux projets ci-dessous. Cette distinction a été contrôlée dans leurs rapports actuels, pas déduite d'un souvenir.

## 1. Averyanov : correction explicite d'un alignement zodiacal

Source primaire : [*Thirty Names per Sign*, §2](https://voynich.site/paper-2-labels?lang=en), extraction consultée lignes 36–40. La correction datée du 25 octobre 2026 indique :

> “Degree alignment, withdrawn as evidence”

L’auteur rapporte que la valeur p passe de 0,0088 à 0,63 lorsque les permutations préservent les demi-anneaux. Le décalage 23 devient une convention, sans preuve d’ordre sémantique. Ces nombres ne sont pas recalculés ici. L’hypothèse de sigles reste dépendante de son modèle.

Le contrôle Yoshida compare des parseurs sur le même interlinéaire, sans fournir de sens. La page HTML reste modifiable ; aucune édition immuable de cette correction ni aucun paquet de réplication n’a été authentifié. L’agent principal a relu directement ces passages le 17 novembre 2026.

## 2. Yoshida : témoin de traitement, pas témoin sémantique

Source primaire : [seeton/Voynich-public](https://github.com/seeton/Voynich-public/tree/8920f2e506fce4c2c5a1245fb21a312f25655f1b), commit **`8920f2e506fce4c2c5a1245fb21a312f25655f1b`**, daté du 13 août 2026. Trois fichiers ont été acquis au commit et vérifiés par SHA de blob Git; leurs SHA-256 figurent dans [SOURCE_CHECKS.json](../../../docs/PIECES_REFERENCES.md#piece-39bb5144a9c936).

- [summary.json, ligne 5](https://github.com/seeton/Voynich-public/blob/8920f2e506fce4c2c5a1245fb21a312f25655f1b/analysis/results/label_locality/summary.json#L5) précise pour son ordre de pages : “it is not production chronology or metric physical distance.” Les comptes 883/1 021/747 figurent aux lignes 10–12; la limite sémantique est explicitée ligne 7.
- [manifest.json, lignes 39–59](https://github.com/seeton/Voynich-public/blob/8920f2e506fce4c2c5a1245fb21a312f25655f1b/analysis/results/label_locality/manifest.json#L39) documente le retrait public des champs textuels `known_tokens` et `raw_text`. Il donne les empreintes de l'interlinéaire et de l'EVT aux lignes 10–12.
- [label_records.csv](https://github.com/seeton/Voynich-public/blob/8920f2e506fce4c2c5a1245fb21a312f25655f1b/analysis/results/label_locality/label_records.csv) contient des repères de page, ligne, type, section, bifolio et comptes, sans correspondance vers une langue connue. Le [code associé](https://github.com/seeton/Voynich-public/blob/8920f2e506fce4c2c5a1245fb21a312f25655f1b/analysis/semantics/label_locality.py) est localisé, mais n'a pas été exécuté ici.

Ces ressources peuvent servir à contrôler un inventaire et sa provenance. Elles ne donnent pas d'ordre historique externe ni de paire texte–sens à intégrer comme vérité de déchiffrement. Notre vérification porte sur les fichiers et leurs déclarations; elle ne reproduit pas l'ensemble de leurs statistiques.

## 3. Pelling, janvier 2026 : proposition nouvelle sur une marge déjà étudiée

[Nick Pelling, 22 janvier 2026](https://ciphermysteries.com/2026/01/22/finally-i-can-read-the-voynich-manuscript), propose une lecture occitane de f17r contenant `balsamina`. La page cite un rapprochement lexical avec [Wellcome MS 626](https://wellcomecollection.org/works/eu3ym7su/items?canvas=61). C'est une proposition de l'auteur, pas une transcription marginale consensuelle ni une paire bilingue authentifiée. Aucun alignement vérifié avec le corps principal n'est fourni par cette page.

Le support est précisément la marge multispectrale examinée en phase 44; seule cette proposition bibliographique n'était pas mentionnée dans les inventaires recherchés. Elle ne justifie pas de refaire les lectures IA ni de remplacer leurs abstentions par un sens attendu. Une expertise paléographique indépendante pourrait l'examiner, sans la traiter d'avance comme clé.

## Contrôle institutionnel et limites d'accès

La [notice courante de Yale Beinecke](https://beinecke.library.yale.edu/beinecke/collections/beinecke-cipher-voynich-manuscript) décrit toujours un texte non déchiffré; elle fournit les images et précise que la bibliothèque ne compile ni n'évalue systématiquement les propositions de recherche. L'[article Yale News du 21 février 2025](https://news.yale.edu/2025/02/21/deciphering-mysterious-manuscript) ne donne pas de nouveau texte parallèle ou de correspondance sémantique. Ces deux pages ne constituent pas un inventaire exhaustif de toute recherche récente.

[Layfield et Davis, *Singulion Structure and the Voynich Manuscript*](https://doi.org/10.4000/16k0a), déjà inscrit dans le dépôt, reste une proposition sur l'organisation matérielle et la similarité textuelle. L'accès direct éditeur rencontre Anubis; des passages primaires indexés sont consultables, mais aucun téléchargement intégral authentifié n'a été obtenu ici. Cette piste n'est pas transformée en ordre établi des mots ou des étiquettes.

Le [PDF récent de Stolfi sur la dernière section](https://www.ic.unicamp.br/~stolfi/EXPORT/projects/papers/voynich/2026-02-10-sps-is-sbj.pdf) a renvoyé un délai d'accès; il n'est ni évalué ni compté comme résultat. Aucune recherche sur les archives privées ou consultation humaine n'a été menée. La conclusion est donc limitée aux documents consultés : aucune nouvelle vérité sémantique n'est disponible pour alimenter les tests.
