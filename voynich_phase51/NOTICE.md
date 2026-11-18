# Phase 51 — sources, attributions et limites

Cette expérience est une **nouvelle calibration lexicale** du moteur de Luo et al. sur IE-CoR. Elle cherche des correspondances entre des graphies gothiques dont les valeurs phonétiques ne sont pas fournies au moteur et un lexique phonémique vieux-islandais. Elle n'utilise aucune entrée du Voynich et n'établit aucune traduction. Cette notice décrit les matériaux et transformations, sans annoncer de résultat d'entraînement.

## Données IE-CoR

La source est le dépôt des éditeurs [lexibank/iecor](https://github.com/lexibank/iecor/tree/dd1ebc997bc38c824fb18a1ef234bbf2c229420b), release CLDF [v1.2.1](https://github.com/lexibank/iecor/releases/tag/v1.2.1), commit `dd1ebc997bc38c824fb18a1ef234bbf2c229420b`. Les quinze fichiers de `sources/iecor/` proviennent de cette source primaire éditoriale, et non d'un miroir. Leurs tailles, SHA de blobs Git et SHA-256 sont consignés dans [sources/RECEIPTS.json](../docs/PIECES_REFERENCES.md#piece-dd8bf540ece59b).

Crédits de la base : Paul Heggarty, Cormac Anderson et Matthew Scarborough, *Indo-European Cognate Relationships database*, Leipzig, Max Planck Institute for Evolutionary Anthropology, 2024. Le README archivé indique la version source 1.1, tandis que la page de release indique 1.2 : le commit et la release CLDF ci-dessus identifient donc précisément les octets utilisés, sans confondre ces numéros. L'article de référence est Anderson et al. (2025), [*The Indo-European Cognate Relationships dataset*](https://doi.org/10.1038/s41597-025-05445-3). Les notices [Gothic](https://iecor.clld.org/languages/gothic) et [Old Icelandic](https://iecor.clld.org/languages/oldicelandic), ainsi que les métadonnées archivées, attribuent ces deux contributions à Matthew Boutilier, `Author_ID=73`.

Les données sont sous [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). Le texte de licence est conservé dans [sources/iecor/LICENSE](../docs/PIECES_REFERENCES.md#piece-d8418adae23548). Les données préparées ici sont une transformation de ces données : sélection de langues, concaténation et normalisation phonémique décrites ci-dessous. Les fichiers source archivés restent inchangés. Cette attribution n'implique aucun soutien des auteurs à l'expérience.

Les entrées choisies sont les 123 formes gothiques de `Language_ID=303` et les 170 formes vieux-islandaises de `Language_ID=302`. Les champs `native_script`, `Phonemic`, `Phonemic_Segments` et les jugements `Cognateset_ID` viennent des tables CLDF. `Form`, `phon_form` et `Segments` ne sont pas substitués à ces champs. La politique de transcription des éditeurs est archivée dans [sources/iecor/etc/Transcription-and-Transliteration-Policy.md](../docs/PIECES_REFERENCES.md#piece-cc1135fdcc8e6a).

Les colonnes de références des formes sont vides dans cet export. Les 82 classes cognates communes possèdent des références dans `cognatesets.csv`; les annotations sélectionnées sont marquées expertes et non douteuses, et aucune classe sélectionnée n'est répertoriée dans `loans.csv`. La vérité d'évaluation retient **l'égalité exacte de `Cognateset_ID`**, sans fusionner les superclasses et sans utiliser la seule égalité de concept. Ces jugements restent des annotations savantes; une cible absente ne prouve pas l'absence de toute relation historique.

## Moteur et bibliothèques

Référence : Jiaming Luo, Frederik Hartmann, Enrico Santus, Regina Barzilay et Yuan Cao (2021), [*Deciphering Undersegmented Ancient Scripts Using Phonetic Prior*](https://aclanthology.org/2021.tacl-1.5/), *Transactions of the Association for Computational Linguistics* 9, 69–81, DOI `10.1162/tacl_a_00354`.

Les sources de Jiaming Luo sont fixées à :

- [j-luo93/xib, commit 50dd1d4133ad154d89f37c476ad7a4adff06e970](https://github.com/j-luo93/xib/tree/50dd1d4133ad154d89f37c476ad7a4adff06e970), branche TACL lors de l'acquisition;
- [j-luo93/dev_misc, commit 8cb3c73bebe444dd22da25e44a3fe05d13aff8c5](https://github.com/j-luo93/dev_misc/tree/8cb3c73bebe444dd22da25e44a3fe05d13aff8c5).

[source_manifest.json](../docs/PIECES_REFERENCES.md#piece-d84bca478aba52) identifie les 103 blobs archivés dans `upstream/`. Aucun fichier de licence explicite n'a été trouvé dans ces arbres archivés; cette notice ne leur attribue donc pas de nouvelle licence. La licence CC-BY des données IE-CoR ne s'étend pas automatiquement au code ou aux dépendances. Les bibliothèques restent soumises à leurs licences respectives.

Le moteur utilisé est `ExtractModelV2` avec la configuration `FinalNon`. [COMPATIBILITY.json](COMPATIBILITY.json) décrit quatre modifications de compatibilité : retrait d'un import CLTK inutilisé, conservation des lots sur CPU, syntaxe de sélection de colonnes pandas, et désactivation de la lecture du commit du répertoire temporaire. Les sources non modifiées et les différences exactes sont conservées. La préparation et l'export d'inférence sont propres à cette calibration; l'objectif et l'optimiseur natifs sont conservés.

## Transformations et ambiguïtés

Le moteur reçoit uniquement les 24 signes des graphies gothiques natives et le lexique connu. Les phonèmes gothiques, les concepts, les identifiants lexicaux et les classes cognates ne sont pas des entrées d'optimisation. Chaque séquence contient deux formes concaténées, ou la dernière forme seule; une seule ligne `Word` est sérialisée pour la séquence complète. Les champs obligatoires d'annotation contiennent une IPA inconnue factice et le même candidat connu `a`. Les scores de l'évaluateur natif sur ces annotations factices sont écartés.

Les formes connues sont obtenues en concaténant les tokens `Phonemic_Segments` de la source, puis en conservant exactement la sortie de `IpaSequence('non', chaîne)` du moteur. Les segments sources omettent déjà les accents présents dans certains champs `Phonemic`. Avec l'environnement enregistré, le parseur original supprime 85 marques de durée `ː` dans 77 formes; `ipapy 0.0.9.0` canonise aussi quatre occurrences de `u̯` en `w`. Il ne s'agit pas d'une nouvelle transcription inventée pour l'expérience. [data/GOLD.json](../docs/PIECES_REFERENCES.md#piece-2d67bfa89bd59d) conserve, forme par forme, les champs source, la chaîne fournie, la sortie canonique et chaque transformation; [data/INPUTS.json](../docs/PIECES_REFERENCES.md#piece-32e35dfeaf96bf) en donne les comptes.

Les 170 entrées correspondent à 167 chaînes avant cette normalisation, puis à **166 candidats canoniques**. Quatre classes contiennent deux entrées chacune : `bɛi̯n`, `fotr`, `ormr` et `watn`. La première collision est introduite par la suppression de durée entre `bɛi̯n` et `bɛi̯nː`; les trois autres préexistent dans la représentation source. Une correspondance correcte désigne donc une **classe IPA**, pas nécessairement un lexème ou un sens unique. Aucune entrée n'est éliminée silencieusement pour contourner le parseur ou les limites de longueur.

## Portée de la calibration

IE-CoR fournit des listes lexicales. Les 62 séquences de cette expérience sont des concaténations construites, pas des passages historiques continus. Leurs limites externes restent connues du modèle. Les 92 formes d'apprentissage et les 31 formes réservées sont séparées avant l'optimisation, avec 63 et 19 formes respectivement possédant au moins une cible cognate annotée. Les cinq graines partagent la même réserve : ce ne sont pas cinq jeux linguistiques indépendants.

Cette calibration n'est pas une réplication exacte des corpus, radicaux et scores A@10 de TACL 2021. Son critère est une frontière complète exacte plus une cible IPA acceptable, évaluées sur des formes réservées. La référence par permutation mesure l'association conditionnelle aux annotations de cette réserve; elle n'est pas un taux général de faux positifs pour identifier une langue. Même un franchissement des seuils du [protocole](PROTOCOL.json) établirait seulement un transfert lexical partiel dans ces conditions, sans valider une clé phonétique complète, une traduction du gothique suivi ou un déchiffrement du Voynich.
