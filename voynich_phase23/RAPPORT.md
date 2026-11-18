# Phase 23 — Ce qui distingue les étiquettes du texte courant

**Résultat : les débuts des étiquettes ont une structure distincte qui se retrouve dans plusieurs cahiers. Les fins présentent également un effet après appariement du début, mais cet effet est plus sensible aux choix de comptage et reste insuffisamment contrôlé pour la mise en page. Aucun de ces résultats ne fournit une traduction.**

`NOT_TRANSLATION` — Travail local, protocole et code figés avant les nouveaux calculs au commit `7b6cfdd`. Aucune publication, aucun push. Toutes les anciennes réserves ont été vues pendant l’atlas : les exclusions de cahiers ci-dessous concernent les calculs, pas une réserve historiquement aveugle.

## Ce qui a été testé

Deux questions ont été fixées : les différences de **première unité** entre étiquettes et prose se retrouvent-elles sur un autre cahier ? Et existe-t-il une différence de **dernière unité** quand on apparie aussi la première unité ?

Les comparaisons portent sur la même page et la même longueur. Elles conservent les métadonnées de section, main et cahier. Le texte courant principal exclut les mots aux extrémités des segments de ligne. Chaque cahier est évalué avec des poids calculés uniquement dans les autres cahiers. Les formes ambiguës sont exclues selon des règles fixes ; aucun caractère ni espace n’est corrigé à la main.

Ce n’est pas un échantillon de toutes les étiquettes : les étiquettes zodiacales sans paragraphe comparable sur la même page ne participent pas à ce test. Les catégories graphiques de l’atlas ne donnent aucun sens supposé aux mots.

## Résultats principaux

| Comparaison | Transcription | Étiquettes / mots de prose appariés | Folios / cahiers | T | p conditionnel |
|---|---|---:|---:|---:|---:|
| Débuts | ZL | 326 / 2271 | 14 / 4 | 0.2079 | 0.0002 |
| Débuts | IT | 328 / 2548 | 13 / 4 | 0.2331 | 0.0002 |
| Fins, à début égal | ZL | 190 / 528 | 11 / 3 | 0.0340 | 0.0010 |
| Fins, à début égal | IT | 202 / 572 | 11 / 3 | 0.0361 | 0.0008 |

Les deux tests principaux ZL passent le seuil fixé de 0,025, qui tient compte de deux tests. Les contributions sont positives dans chaque cahier retenu et l’effet garde le même sens dans IT. **IT est une autre transcription du même manuscrit, pas une réplication indépendante.** T mesure l’accord des différences entre cahiers ; ce n’est ni un taux de lecture correcte ni une probabilité de traduction.

Les p-values proviennent de 4 999 réallocations des rôles dans les groupes appariés. Elles testent seulement ce modèle de réallocation des mots. Les dépendances entre mots et les conventions de disposition peuvent violer ses hypothèses ; elles ne sont pas éliminées par un petit p.

Dans le détail descriptif, les débuts `o` sont plus fréquents et les débuts `q` moins fréquents parmi les étiquettes. Ce constat était déjà présent dans les sources : la nouveauté ici est son contrôle par page et longueur, avec transfert entre cahiers. Pour les fins, le déficit de `n` est la principale contribution commune ; cette inspection par symbole est postérieure au résultat et ne vaut pas nouveau test indépendant.

[Contrastes descriptifs des bords de mots](../docs/PIECES_REFERENCES.md#piece-3e9de02f66c5a4)

La figure montre des différences de fréquences pondérées, en points de pourcentage. Elle n’identifie ni articles, ni terminaisons grammaticales, ni noms de plantes.

## Variantes fixées avant les résultats

| Variante | Débuts ZL : p | Débuts IT : p | Fins ZL : p | Fins IT : p |
|---|---:|---:|---:|---:|
| Prose en début de segment | 0.0002 | 0.0002 | effectif insuffisant | effectif insuffisant |
| Prose en fin de segment | 0.0002 | 0.0002 | effectif insuffisant | effectif insuffisant |
| Formes répétées retirées par page et rôle | 0.0002 | 0.0002 | 0.0488 | 0.0156 |
| Longueur en caractères EVA individuels | 0.0002 | 0.0002 | 0.0240 | 0.0060 |

Ces variantes sont toutes conservées, sans sélection de la meilleure. Leurs p-values sont descriptives. Le signal initial persiste. **Le signal final s’atténue après déduplication : ZL atteint p = 0,0488**, au-dessus du seuil principal de 0,025. Les comparaisons finales avec les bords de ligne n’ont pas assez de données : les seuils n’ont pas été abaissés pour obtenir une réponse. On ne peut donc pas affirmer que l’effet final est indépendant de la disposition.

## Calibration : pourquoi ce n’est pas une preuve de message

| Mécanisme construit | Débuts détectés / 20 | Fins détectées / 20 |
|---|---:|---:|
| Texte connu chiffré avec marqueurs de rôle | 20 | 20 |
| Sans message, sans marqueur de rôle | 0 | 1 |
| Sans message, bords dépendant du rôle | 20 | 20 |
| Sans message, convention de disposition ; prose intérieure | 20 | 20 |
| Même convention ; comparaison avec débuts de ligne | 0 | 0 |

Le seuil de détection et les règles de réussite ont été fixés avant les calculs. La calibration passe. Cependant, les gabarits **sans message** obtiennent le même type de résultat positif. Une convention de disposition suffit à produire un effet ; le témoin comparant les mêmes positions le fait disparaître. Ces contrôles sont des mécanismes simples construits pour éprouver la mesure, pas une reconstitution historique de la fabrication du Voynich. Le programme de mesure ne reçoit ni clé ni texte clair, et il ne déchiffre pas les contrôles.

## Ce que cela change pour la recherche

Les étiquettes ne doivent pas être traitées comme un tirage quelconque des mots du texte courant. Une proposition de lecture devra expliquer les différences de bords et leur variation avec la disposition. Ce résultat permet de contraindre un futur modèle ; il ne choisit pas une langue et ne donne pas de dictionnaire.

Les phases 14–15 n’avaient pas validé de correspondance locale entre étiquettes et prose par identité ou courtes transformations. Les phases 18–19 avaient montré qu’un avantage en fin de mot peut également apparaître sans message. Les phases 20–22 ont ensuite testé le décodage et les espaces sur des mécanismes connus. En phase 22, **aucune fusion n’a été corrigée sur les 12 nouveaux passages de transfert**, sans ajout de fausse coupure sur ces passages ; les limites de segmentation restent donc ouvertes. Cette phase 23 n’applique pas ce correcteur au Voynich.

La piste concrète qui reste à départager est celle d’une convention de forme liée au rôle ou à la disposition, face à une différence linguistique. Le déficit final de `n` est une observation candidate, pas un sens attribué. Toute exploitation sémantique devra fixer des prédictions et disposer d’annotations image–texte indépendantes, avec témoins, avant leur ouverture. Les vues déjà examinées ne peuvent pas jouer ce rôle de réserve neuve.

## Vérifications et fichiers

- 20 configurations recalculées avec une seconde implémentation arithmétique ; invariance au renommage bijectif des symboles vérifiée.
- Les deux tests principaux, y compris leurs 4 999 réallocations chacun, ont été reproduits à l’identique.
- Vérification du parseur, des positions, des allers-retours de chiffrement et d’un petit modèle nul énumérable exactement.
- Les 150 fichiers de phase 22 et les 684 fichiers inventoriés de l’atlas sont inchangés ; leurs manifestes passent.
- Il s’agit de vérifications techniques par le même opérateur, pas d’une confirmation externe du manuscrit.

Les [méthodes détaillées](METHODS_EN.md), le [protocole figé](PROTOCOL.json), les [sources et limites de lecture](../docs/PIECES_REFERENCES.md#piece-059708bc673468), les [résultats complets](results/summary.json), la [calibration](results/calibration.json) et les [vérifications](results/verification.json) sont conservés. Le [README](README.md) fournit les commandes de reproduction.

Les observations antérieures sur les débuts proviennent notamment de [Landini (2001)](https://www.voynich.net/Arch/2001/03/msg00014.html) et de [Zandbergen](https://www.voynich.nu/extra/labels.html). Le contrôle des regroupements documentaires est motivé aussi par [Sterneck, Polish et Bowern](https://arxiv.org/html/2107.02858v1), dont les modèles de thèmes n’ont pas été reproduits ici.
