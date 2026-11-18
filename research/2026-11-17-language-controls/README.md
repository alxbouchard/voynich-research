# NorthEuraLex — lexiques non indo-européens disponibles

17 novembre 2026. **Source trouvée et recouvrement mesuré; aucun entraînement ni calibration exécutés.** Le finnois et le hongrois sont classés dans la famille ouralienne, et le basque séparément, dans les métadonnées archivées. Le finnois est le candidat le plus simple parmi ces trois pour préparer ultérieurement un lexique de comparaison : tous les concepts communs sont couverts et aucune frontière interne `+` ne figure dans les formes sélectionnées. Ce choix pratique ne constitue pas une validation scientifique du lexique ou du moteur.

## Source, version et licence

- Dépôt éditorial primaire : [lexibank/northeuralex](https://github.com/lexibank/northeuralex/tree/e9a8119f25cf6078299132d8c4e7db338d46ff23), commit `e9a8119f25cf6078299132d8c4e7db338d46ff23`.
- [Release CLDF v4.1](https://github.com/lexibank/northeuralex/releases/tag/v4.1), DOI annoncé par la release : [10.5281/zenodo.13269523](https://doi.org/10.5281/zenodo.13269523). Le tag et la tête du dépôt consultée pointent sur le même commit. Cela reste un dérivé CLDF du **NorthEuraLex 0.9** original; ce sont deux numéros de version distincts.
- Licence [CC-BY-4.0](../../docs/PIECES_REFERENCES.md#piece-da5918e14d10ca), conservée avec les crédits dans le [README source](../../docs/PIECES_REFERENCES.md#piece-4e85b44262d073).
- Article primaire : Dellert, Daneyko, Münch et al., [*NorthEuraLex: a wide-coverage lexical database of Northern Eurasia*](https://link.springer.com/article/10.1007/s10579-019-09480-6), publié en ligne le 30 novembre 2019, *Language Resources and Evaluation* 54, 273–301 (2020). Le site éditeur a été consulté; les sites northeuralex.org et la résolution Zenodo n'ont pas été accessibles par l'outil web.

Seize fichiers, 24 381 215 octets, sont archivés sans modification et vérifiés contre les blobs du commit : [RECEIPTS.json](../../docs/PIECES_REFERENCES.md#piece-59e9612924d17f). Le téléchargement des deux grandes tables a utilisé les URL GitHub brutes au commit fixé, après découverte des métadonnées par le connecteur GitHub. Aucune source miroir n'est substituée. Les trois fichiers IE-CoR nécessaires au rapprochement sont également copiés et authentifiés : [IECOR_SOURCE.json](../../docs/PIECES_REFERENCES.md#piece-b3f8dfd4522a18), commit IE-CoR `dd1ebc997bc38c824fb18a1ef234bbf2c229420b`, release v1.2.1.

## Concepts réellement communs

Le rapprochement emploie exclusivement l'égalité exacte des identifiants `Concepticon_ID` non vides. Il n'assimile pas deux libellés ressemblants. IE-CoR contient 170 concepts à identifiants distincts. NorthEuraLex contient 1 016 paramètres, 954 identifiants Concepticon distincts et 60 paramètres sans identifiant. **156 des 170 concepts IE-CoR sont communs**, avec un seul paramètre NorthEuraLex pour chacun de ces 156 identifiants. Les trois langues possèdent effectivement des formes pour tous ces concepts.

| Langue | Famille source | Formes du lexique entier | Formes sur les 156 concepts | Chaînes `Segments` concaténées distinctes | Groupes homophones avant moteur |
|---|---|---:|---:|---:|---:|
| Finnois `fin` | Uralic / Finnic | 1 188 | 171 | 169 | 2 |
| Hongrois `hun` | Uralic / Hungarian | 1 234 | 174 | 169 | 5 |
| Basque `eus` | Basque | 1 290 | 190 | 188 | 2 |

Les synonymes et homophones sont conservés. Les 14 concepts non joints sont : burn, fight, fruit, hair, hit, live, rotten, straight, swell, turn, vomit, thigh, shadow et grind. Leur absence du rapprochement exact ne signifie pas qu'aucun mot ne peut exprimer ces notions dans NorthEuraLex : une notion voisine peut porter un autre identifiant. Aucune fusion manuelle n'a été effectuée.

[CONCEPT_CROSSWALK.csv](../../docs/PIECES_REFERENCES.md#piece-16cc5159bce7eb) conserve les 156 liens, identifiants et gloses des deux sources. [MATCHED_FORMS.csv](../../docs/PIECES_REFERENCES.md#piece-d87356c9b75624) contient les 535 formes sélectionnées, tous leurs champs CLDF et les enregistrements d'origine correspondants. [SUMMARY.json](../../docs/PIECES_REFERENCES.md#piece-3b63a5ff9d5596) détaille les comptes, les synonymes, les collisions, les différences de transcription et les concepts exclus. L'égalité de concept ne démontre aucune cognation.

## Ce que représentent les transcriptions

L'article, §3.3, décrit des conversions automatiques de l'orthographe vers IPA fondées sur des descriptions phonologiques, avec exceptions possibles. Les auteurs reconnaissent que certaines transcriptions combinent niveaux phonétique et phonémique. **Ce n'est donc pas un inventaire uniformément phonémique ni un ensemble d'enregistrements oraux.** Les décisions lexicales ont leurs propres statuts de révision. [Article primaire, §3.1–3.3](https://link.springer.com/article/10.1007/s10579-019-09480-6).

Le trajet vérifié dans [le code de conversion](../../docs/PIECES_REFERENCES.md#piece-73991b11902a14) est :

| Champ | Provenance et usage |
|---|---|
| `raw/nelex.tsv:Word_Form` | Graphie lexicale originale; devient `Value` en CLDF. |
| `raw/nelex.tsv:rawIPA` | Transcription publiée; alimente `Form` après retrait d'espaces externes et remplacement des espaces internes par `_`. |
| `cldf/forms.csv:Form` | IPA issue du trajet de préparation; ne pas la confondre avec l'orthographe. |
| `cldf/forms.csv:Segments` | Segmentation et normalisation CLDF/BIPA, documentées par `etc/orthography.tsv` et `TRANSCRIPTION.md`. |
| `Orthography` | Champ présent mais vide pour les formes inspectées; utiliser `Value` pour la graphie. |
| `Source` | `Dellert2020` pour toutes les formes sélectionnées; pas une citation de dictionnaire distincte pour chaque entrée. |
| `Next_Step` de la table brute | `validate` pour les 171 formes finnoises et 174 hongroises; 188 `validate` et 2 `review` en basque. `validate` n'est pas `validated`. |

Toutes les 535 formes ont été reliées à leurs enregistrements bruts sans remplacement. La source ne possède pas ici un champ `Phonemic_Segments` équivalent à celui utilisé dans IE-CoR. Le README Lexibank avertit de modifications importantes de l'IPA lors de la conversion CLDF. La provenance de cette version cite Concepticon v3.2.0 et CLTS v2.3.0, alors que la version IE-CoR utilisée cite Concepticon v3.4.0. Les identifiants joints sont exacts, mais ce décalage de versions et les définitions détaillées doivent rester visibles dans un futur protocole.

## Limites avant toute utilisation dans le moteur

- `Form` et la concaténation des `Segments` diffèrent pour 45 formes finnoises, 26 hongroises et 72 basques. Exemples : `kiɛ̯li` devient les segments `k iɛ l i`; une affriquée `t͡ʃ` peut devenir le token `tʃ`; `ɡ` peut devenir `g`. La concaténation perd les frontières entre tokens BIPA; sa resegmentation par un autre parseur doit être vérifiée, pas présumée équivalente.
- Une marque de durée `ː` apparaît dans 48 formes finnoises et 94 hongroises sélectionnées. Le parseur par défaut employé en phase 51 retire cette marque. Il faudra documenter les pertes et collisions propres à ces langues avant de choisir cette convention. Aucun nombre de candidats « après IpaSequence » n'est annoncé ici : ce parseur n'a pas été exécuté.
- Les 19 formes basques contenant `+` représentent des expressions comprenant des frontières internes. Le profil CLDF transforme `_` en `+`. Par exemple, `zutik egon` donne `s u t i k + e g o n`. Effacer le marqueur, le convertir en son ou exclure ces formes serait une décision nouvelle à déclarer. Les deux formes basques marquées `review` expriment « bite ».
- Les maxima observés sont 9, 8 et 14 tokens de segments pour finnois, hongrois et basque; les maxima en points de code après concaténation sont 11, 9 et 14. Le compte basque inclut les marqueurs `+`. Ces nombres ne sont pas des longueurs garanties dans `IpaSequence` et ne justifient pas de reprendre silencieusement les bornes de phase 51.
- Les champs `Loan` et `Cognacy` sont vides dans les 535 lignes. Une famille non indo-européenne n'implique pas l'absence d'emprunts, de ressemblances fortuites ou de contacts. Cette source ne certifie donc pas un lexique sans aucun mot historiquement apparenté aux langues indo-européennes.
- Le partage des 156 concepts ne règle pas l'équilibrage des tailles, synonymes, longueurs et fréquences. Un futur contrôle devra fixer sa sélection et sa normalisation avant les scores. Les graphies et concepts ne doivent pas devenir des indices implicites fournis au moteur.

## Rejouer uniquement l'inventaire

Avec les sources archivées, `python3 inspect_overlap.py` authentifie les fichiers puis régénère les trois sorties d'inventaire. Il n'importe ni PyTorch ni le moteur, et ne réalise aucun entraînement. `acquire.py` permet de récupérer les mêmes fichiers publics au commit fixé si nécessaire; il vérifie leur taille et leur SHA de blob avant archivage. Aucun fichier gelé de phase 51 n'est écrit par ces scripts.
