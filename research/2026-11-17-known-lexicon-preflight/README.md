# Vérification de cinq lexiques connus — 17 novembre 2026

Ce dossier mesure la compatibilité de formes lexicales publiées avec le parseur IPA original de Luo et al. Il contient **799 entrées sur 156 concepts communs**, sans apprentissage, inférence, score de déchiffrement ou traduction. Les synonymes CLDF, erreurs, unités natives, matrices de traits et collisions sont conservés. Il ne fournit pas un lexique final validé.

Deux résultats sont volontairement séparés : [PREFLIGHT.json](../../docs/PIECES_REFERENCES.md#piece-8e9b263e06583a), sans normalisation Unicode ajoutée, et [NFD_DIAGNOSTIC.json](../../docs/PIECES_REFERENCES.md#piece-f95f51d9920db2), diagnostic technique NFD demandé après constat des erreurs. Le second ne remplace pas le premier. Aucun fichier gelé de phase 51 n'est modifié par ces scripts.

## Sources authentifiées et périmètre

Les données proviennent des dépôts éditoriaux primaires, sous CC-BY-4.0. Les licences sont conservées dans [sources/iecor/LICENSE](../../docs/PIECES_REFERENCES.md#piece-f019eb85d447b8) et [sources/northeuralex/LICENSE](../../docs/PIECES_REFERENCES.md#piece-53c7a732dbe8b7). Les sélections et résultats présents sont des transformations de ces données, sans soutien implicite des auteurs.

| Source | Version exacte | Champs lus pour les formes connues |
|---|---|---|
| [IE-CoR](https://github.com/lexibank/iecor/tree/dd1ebc997bc38c824fb18a1ef234bbf2c229420b), Heggarty, Anderson et Scarborough | CLDF v1.2.1, commit `dd1ebc997bc38c824fb18a1ef234bbf2c229420b` | `Phonemic_Segments`, avec tous les autres champs des lignes connues conservés pour provenance |
| [NorthEuraLex](https://github.com/lexibank/northeuralex/tree/e9a8119f25cf6078299132d8c4e7db338d46ff23), Dellert, Daneyko, Münch et al. | CLDF v4.1, commit `e9a8119f25cf6078299132d8c4e7db338d46ff23`, dérivé de NorthEuraLex 0.9 | `Segments`; l'orthographe n'est pas fournie au parseur |

Références primaires : Anderson et al., [*The Indo-European Cognate Relationships dataset*](https://doi.org/10.1038/s41597-025-05445-3), 2025 ; Dellert et al., [*NorthEuraLex: a wide-coverage lexical database of Northern Eurasia*](https://link.springer.com/article/10.1007/s10579-019-09480-6), 2020. Les deux versions CLDF ne sont pas des textes historiques suivis ni des enregistrements oraux.

[bootstrap.py](../../docs/PIECES_REFERENCES.md#piece-334f428c0ba580) vérifie les tailles, SHA-256 et SHA de blobs Git des tables amont archivées, puis extrait les langues connues. Il contrôle `Language_ID` avant l'accès aux champs phonétiques. Les octets des tables complètes sont authentifiés, mais aucune phonétique d'une autre langue n'est extraite ou utilisée. Les seules formes locales sont vieux-islandais `302`, anglais `22`, latin `112`, grec ancien `110` et finnois `fin`. Aucune lecture des fichiers GOLD, test, poèmes, graphes de modèle ou phonèmes gothiques n'est nécessaire.

[PROVENANCE.json](../../docs/PIECES_REFERENCES.md#piece-3f42be5e0d3fc2) donne les URL au commit, empreintes des sources, numéros des lignes d'origine et empreintes des six tables locales. Les tables locales contiennent 684 formes IE-CoR connues et 1 188 formes finnoises avant restriction de concepts. La restriction repose exclusivement sur l'égalité exacte des `Concepticon_ID` non vides : **156 concepts**, tous couverts dans chacune des cinq langues. Aucune ressemblance de glose n'est utilisée. Les versions de Concepticon annoncées par les sources diffèrent : 3.4.0 pour IE-CoR et 3.2.0 pour NorthEuraLex ; CLTS 2.3.0 est indiqué pour les deux.

Les 14 concepts IE-CoR hors intersection sont : burn, fight, fruit, hair, hit, live, rotten, straight, swell, turn, vomit, thigh, shadow et grind. Les entrées hors intersection sont inventoriées dans `outside_shared_concepts`, pas supprimées pour contourner une erreur de parseur. La langue finnoise est classée ouralienne dans les métadonnées : cela ne garantit ni l'absence d'emprunts ni l'absence de ressemblances fortuites. L'égalité de concept ne démontre pas une cognation.

## Transformations déjà présentes dans les sources

Pour IE-CoR, `Phonemic_Segments` dérive du champ `Phonemic`. [Le code source, lignes 614–635](https://github.com/lexibank/iecor/blob/dd1ebc997bc38c824fb18a1ef234bbf2c229420b/lexibank_iecor.py#L614-L635) applique des réécritures, développe les parenthèses et retient la première variante intra-ligne avant la tokenisation. **Tous les synonymes** signifie ici toutes les lignes CLDF sélectionnées, pas toutes les variantes qui existaient avant cette conversion. Dans les lignes retenues, `Phonemic` diffère de la concaténation de `Phonemic_Segments` pour 61 entrées vieux-islandaises, 17 anglaises, 141 latines et 145 grecques. Ces différences ne proviennent pas de notre parseur.

Un cas optionnel est conservé explicitement : latin `112-133-1`, `Phonemic=(h)aˈreːna`, segments `h a r eː n a`. Le `h` facultatif est devenu présent et le stress a été omis en amont. Aucune autre entrée retenue ne contient les marqueurs de variantes recherchés `, ; / ~ ≠` dans `Phonemic`. Les champs sources complets restent dans chaque `source_record`.

Pour NorthEuraLex, le [README éditorial](https://github.com/lexibank/northeuralex/blob/e9a8119f25cf6078299132d8c4e7db338d46ff23/README.md#L24) avertit de modifications importantes de l'IPA lors du passage en CLDF. `Segments` est une représentation CLTS/BIPA issue de `rawIPA`, pas `Word_Form` et pas une copie garantie de l'IPA originale. [Le code de conversion](https://github.com/lexibank/northeuralex/blob/e9a8119f25cf6078299132d8c4e7db338d46ff23/lexibank_northeuralex.py) et [le profil de transcription](https://github.com/lexibank/northeuralex/blob/e9a8119f25cf6078299132d8c4e7db338d46ff23/etc/orthography.tsv) sont les références de cette transformation. Dans les 171 entrées finnoises, `Form` diffère des segments concaténés 45 fois. La publication décrit une transcription mêlant parfois niveaux phonétique et phonémique ; sa compatibilité informatique ne prouve pas sa validité linguistique.

## Parseur original et limites de son paramètre de langue

Le code est fixé à [j-luo93/xib `50dd1d4133ad154d89f37c476ad7a4adff06e970`](https://github.com/j-luo93/xib/tree/50dd1d4133ad154d89f37c476ad7a4adff06e970) et [j-luo93/dev_misc `8cb3c73bebe444dd22da25e44a3fe05d13aff8c5`](https://github.com/j-luo93/dev_misc/tree/8cb3c73bebe444dd22da25e44a3fe05d13aff8c5). Six fichiers xib et 49 fichiers dev_misc sont copiés sans modification et authentifiés par blob Git et SHA-256. Aucun des ajustements de compatibilité de phase 50 ne touche ces fichiers. Aucun fichier de licence explicite n'a été trouvé dans ces arbres archivés : la licence des données n'est donc pas attribuée au code. Les dépendances conservent leurs licences propres.

Référence de la méthode : Luo et al., [*Deciphering Undersegmented Ancient Scripts Using Phonetic Prior*](https://aclanthology.org/2021.tacl-1.5/), TACL 2021. Le présent travail contrôle seulement son parseur et ses traits, sans répliquer un résultat de l'article.

La chaîne fournie est exactement `''.join(source[field].split())`. Les espaces séparant les tokens disparaissent, mais tout marqueur explicite `+` reste présent. Chaque entrée est ensuite passée à `IpaSequence(label, chaîne)` avec le label propre : `non`, `eng`, `lat`, `grc` ou `fin`. Le label sélectionne les règles de `DigraphProcessor` ; il ne transcrit pas une orthographe vers des sons. Tous les labels partagent les séparations `n͡m`, `d͡b`, `k͡p`, `t͡p` en deux unités. Seul `non` ajoute ici la séparation `t͡s` en `t` et `s`.

Le défaut natif `use_length=False` enlève la marque `ː`. `ipapy 0.0.9.0` applique aussi ses alias. Exemples observés : `u̯` devient `w` dans quatre entrées vieux-islandaises ; anglais `wʊdz` devient `wʊd͡z` et `tʃɛst` devient `t͡ʃɛst` ; finnois `ʋɑtsɑ` devient `ʋɑt͡sɑ`. Ce sont des comportements du parseur d'origine, pas des corrections phonétiques validées. Les unités natives peuvent différer des tokens CLTS, notamment pour les diphtongues finnoises. Les différences de chaînes archivées sont mécaniques et ne sont pas qualifiées de règles phonologiques.

Chaque entrée est vérifiée avant tout éventuel chargeur de vocabulaire : non-vacuité, matrice native finie, dimensions, indices de catégories et absence de gradients. `Vocabulary` n'est pas utilisé, car ses suppressions silencieuses de `ValueError` et filtres de longueur cacheraient des entrées. Les 14 colonnes natives sont conservées. Le diagnostic PCV utilise exactement les sept catégories de `FinalNon` : PTYPE, C_VOICING, C_PLACE, C_MANNER, V_HEIGHT, V_BACKNESS, V_ROUNDNESS. Stress, durée, diacritiques et autres catégories ne font pas partie de cette sélection.

## Résultat brut, conservé sans réécriture

| Langue et label | Lignes sélectionnées | Parseur et traits réussis | Erreurs | Chaînes canoniques distinctes parmi les succès | Longueur native min–max parmi les succès |
|---|---:|---:|---:|---:|---:|
| Vieux-islandais `non` | 156 | 156 | 0 | 153 | 1–9 |
| Anglais `eng` | 156 | 155 | 1 | 153 | 2–9 |
| Latin `lat` | 158 | 158 | 0 | 156 | 2–11 |
| Grec ancien `grc` | 158 | 13 | 145 | 13 | 2–10 |
| Finnois `fin` | 171 | 171 | 0 | 169 | 2–10 |
| **Total** | **799** | **653** | **146** | — | — |

L'expression anglaise `22-45-1`, `b i + s k ɛː d`, est fournie comme `bi+skɛːd` et reste en erreur `ValueError` de `IpaSequence`. Le marqueur de frontière n'est ni effacé ni converti en son. L'autre expression anglaise `22-184-1`, `b i + s ɪ k`, est hors intersection de concepts ; elle reste dans la table source connue mais n'entre pas dans les 799 appels. Les 145 erreurs grecques se produisent au même stade, avant toute matrice de traits. Elles ne sont pas filtrées ou remplacées.

Les collisions canoniques brutes sont : vieux-islandais `fotr`, `ormr`, `watn` ; anglais `flaɪ`, `si` ; latin `os`, `unɡwis` ; finnois `jɑlkɑ`, `kʏnsi`. Seule la paire latine `os`/`oːs` devient ici une nouvelle collision par suppression de durée. Les autres paires préexistent dans les chaînes fournies. Les identifiants et chaînes de chaque groupe sont conservés. Aucune paire de chaînes canoniques **distinctes** ne partage toute sa séquence PCV parmi les 653 succès bruts. Cela ne couvre pas les entrées en erreur et ne prouve pas une distinction complète du modèle.

Il ne serait pas possible de reprendre une borne de neuf unités sans exclusions : latin `interfikere` en a 11, `abskondere` 10 ; grec `apo̞tʰnɛ́jskɔ` 10 ; finnois `murɑhɑinɛn` 10. Les maxima portent sur les unités du parseur, pas les lettres ou les tokens CLTS. Aucune borne de longueur n'est appliquée ici.

Empreinte du résultat brut : `982a0cf7089b7d9638e392869adee4aeb2974d30b3ca1982237904d566989eea`. [AUDIT_INDEPENDENT_BASELINE.json](../../docs/PIECES_REFERENCES.md#piece-4e4e88f0e25803) reproduit indépendamment les 799 appels et matrices, et vérifie les six tables et 55 fichiers de code. Cet audit IA distinct contrôle la reproductibilité informatique ; ce n'est pas une expertise phonologique indépendante.

## Supplément NFD uniquement

[nfd_diagnostic.py](../../docs/PIECES_REFERENCES.md#piece-a23d90fce61449) authentifie le résultat brut, son script, les tables et le code du parseur avant de produire un fichier séparé. Pour chacune des 799 chaînes, il applique uniquement `unicodedata.normalize('NFD', chaîne)` avant le même parseur et vérifie explicitement `NFC(original) == NFC(NFD(original))`. Les preuves chaîne par chaîne et points de code sont archivés. Aucun NFKD, retrait de marqueur, effacement de diacritique ou changement manuel n'est utilisé.

La NFD change exactement les **145 chaînes grecques précédemment en erreur** : elles passent toutes le parseur et le contrôle de traits. Les 653 succès bruts conservent exactement leur chaîne canonique, leurs unités et leur matrice de traits. L'erreur anglaise avec `+` persiste. Le supplément contient donc **798 succès et une erreur**, avec 799 équivalences canoniques Unicode vérifiées. Le grec a alors 157 chaînes canoniques distinctes sur 158 lignes, de 2 à 11 unités. La paire `110-24-1`/`110-218-1` partage déjà la chaîne fournie ; sa canonique est `é̞rkʰo̞mai̯`. Une deuxième forme grecque dépasse neuf unités : `o̞spʰrái̯no̞mai̯`, 11 unités.

Trois groupes de chaînes distinctes partagent une séquence identique des sept traits PCV :

| Périmètre | Chaînes canoniques distinctes | Entrées |
|---|---|---|
| Grec uniquement | `ó̞nyks` / `ó̞nykʰs` | `110-49-1` / `110-226-1` |
| Latin / grec | `tres` / `três` | `112-176-1` / `110-176-1` |
| Vieux-islandais / grec | `hals` / `háls` | `302-109-1` / `110-132-1` |

Exemple tiré des concepts sources : le vieux-islandais `hals` (`302-109-1`, Concepticon 1333) désigne le cou, tandis que le grec `háls` (`110-132-1`, Concepticon 1274) correspond au sel. Leur projection sur ces sept traits est identique malgré les concepts différents ; aucun sens du Voynich n’en est déduit.

Ce sont des **séquences de traits partagées**, sans affirmation d'indistinction totale du modèle. Aucun ensemble de réponses acceptées de phase 51 n'est élargi. Le supplément conserve séparément `raw_result`, `normalization`, `nfd_result` et `canonical_effects`, y compris toutes les erreurs et matrices. NFD établit ici une compatibilité d'encodage canonique, pas la validité linguistique d'un lexique. Le choix éventuel d'une convention pour une future expérience doit rester explicite et indépendant des scores.

Empreinte du supplément : `c7ebe1153f969aa2a5ec9997be6ac6314498bd71b6ff01f7798c19d42734fb2b`.

[AUDIT_INDEPENDENT_NFD.json](../../docs/PIECES_REFERENCES.md#piece-ce55d796f92588) reproduit les 799 appels NFD et confirme les équivalences Unicode, les 145 seuls changements grecs, les 653 résultats initiaux inchangés et les trois groupes PCV. Il s'agit encore d'un contrôle informatique par un agent IA séparé. **Le panel de cinq langues n'est pas prêt pour une expérience** : le traitement de la frontière anglaise doit être décidé explicitement, sans faire disparaître la ligne concernée. Les bornes de longueur et conventions de traits devront également être fixées avant toute nouvelle calibration.

## Reproduire sans modèle

L'exécution a utilisé l'environnement existant `chemin-local/python`, Python 3.9.6, macOS arm64, torch 2.8.0, numpy 1.26.4, pandas 1.5.3, ipapy 0.0.9.0, typeguard 2.13.3 et inflection 0.5.1. Les versions et empreintes de tous les fichiers IPA importés figurent dans chaque rapport. Aucune installation dans un environnement vierge n'a été validée.

Rejouer dans une copie du dossier permet de conserver les rapports d'origine :

```sh
cp -R chemin-local/voynich-known-lexicon-preflight chemin-local/voynich-known-lexicon-reproduction
cd chemin-local/voynich-known-lexicon-reproduction
PYTHONDONTWRITEBYTECODE=1 chemin-local/python preflight.py
PYTHONDONTWRITEBYTECODE=1 chemin-local/python nfd_diagnostic.py
```

`nfd_diagnostic.py` exige l'empreinte brute ci-dessus et s'arrête si elle diffère. Un autre environnement peut produire un rapport différent et doit être audité, pas contourné par la suppression de cette garde. Les scripts n'appellent aucun téléchargement. Pour reconstruire les six tables et les 55 fichiers de parseur dans cette copie à partir des archives authentifiées existantes :

```sh
python3 bootstrap.py \
  --phase51-root chemin-local/voynich-phase51-iecor \
  --discovery-root chemin-local/voynich-unrelated-lexicon-discovery
```

Les entrées nécessaires sont les reçus de sources, tables connues extraites à partir des CSV archivés, licences et manifeste de code ; aucun jeu d'évaluation n'est nécessaire. Les URL et empreintes dans `PROVENANCE.json` permettent de contrôler une réacquisition des fichiers publics aux commits fixés.

PyTorch sert uniquement à représenter les matrices natives et à vérifier `isfinite`. L'import de dev_misc charge transitivement des définitions `trainlib` et émet des avertissements de dépréciation ; aucun Trainer ou modèle n'est instancié. Une garde interdit les imports `xib.model` et `xib.training`. Aucun forward, backward, optimiseur, sélection fondée sur des scores ou modification des données de phase 51 n'est effectué.
