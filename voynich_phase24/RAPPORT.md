# Phase 24 — Les associations entre mots résistent-elles à des contrôles sans message cible ?

**Résultat : le critère distingue les textes à code bijectif des mécanismes de copie testés, mais ne distingue pas un message de tous les générateurs. Le Voynich ne franchit le critère dans aucune variante prévue. Aucun déchiffrement. `NOT_TRANSLATION`.**

Cette phase du 30 octobre 2026 répond à la relance vers un déchiffrement démontrable. Les phases 19 et 23 ont montré que des signaux de finales ou d'étiquettes peuvent apparaître sans message cible. La correction de segmentation de phase 22 n'a produit aucun gain sur les nouveaux transferts. Ici, nous testons une hypothèse différente et falsifiable : les associations entre paires de mots, retrouvées sur des folios distincts, pourraient séparer un code stable de mots d'une copie locale.

Le protocole, les sources, les générateurs et les calculs sont figés au commit `7fc5e24c9097bd2caf49a9b5d9375ad83280c61d`, avant les nouvelles générations et mesures. Les 55 empreintes figurent dans [FREEZE.json](FREEZE.json). C'est un gel local, pas un préenregistrement externe. Toutes les anciennes réserves du manuscrit ont déjà été exposées.

## Ce qui a été exécuté

Le score mesure la corrélation de rang des associations de mots entre deux groupes de folios. Il tient compte des fréquences de chaque page, des longueurs de segments et de leurs extrémités. L'attente du mélange est calculée exactement ; 199 permutations donnent une référence conditionnelle. Le critère fixé exige **à la fois ρ ≥ 0,10 et p ≤ 0,01**. Une petite valeur de p seule ne suffit pas.

Le cadre principal contient **22 373 mots utilisables, 3 063 segments, 172 pages, 85 folios physiques**. Tous les contrôles utilisent exactement ce cadre, ses emplacements incertains et ses partitions. Chaque contrôle principal conserve les 300 types les plus fréquents ; aucun ajustement de paramètres n'est effectué après les résultats.

Deux passages disjoints de chacun de trois auteurs — César, Dante et, nouvellement acquis, Austen — fournissent six messages de contrôle. Les substitutions aléatoires de mots et les variantes à quatre codes par mot sont réversibles ; leurs tables ne sont pas transmises au calcul du score. **Ce test mesure la conservation de structure, pas la récupération d'une clé.**

Nous avons aussi réellement compilé et exécuté le [générateur Java publié par Torsten Timm](https://github.com/TorstenTimm/SelfCitationTextgenerator/tree/a6ede2202dd7ad6285ce2c007bf22c2a0e7709b7), avec six graines fixées. Cela dépasse la phase 19, qui réanalysait seulement un échantillon publié. Le code tiers et sa licence sont conservés exactement ; les six sorties natives, leurs configurations et leurs journaux sont archivés. Elles sont ensuite replacées dans le cadre commun : leur disposition native n'est donc pas testée ici.

## Calibration : résultat contrasté

| Famille, six cas chacune | Intervalle de ρ, 300 types | Critère franchi |
|---|---:|---:|
| Texte à code bijectif | 0,1197 à 0,1629 | 6/6 |
| Texte, quatre codes par mot | 0,0964 à 0,1339 | 3/6 |
| Préférence aléatoire par page | 0,0366 à 0,0618 | 0/6 |
| Copie locale des mots récents | −0,0953 à 0,0304 | 0/6 |
| Générateur publié Timm | 0,0512 à 0,0636 | 0/6 |
| Préférence aléatoire par segment | 0,2087 à 0,2247 | 6/6 |
| Transitions de Markov entre mots | 0,1418 à 0,1685 | 6/6 |

La calibration de sensibilité réussit, y compris dans chacun des trois auteurs. La discrimination des **deux réglages de copie testés** réussit également. En revanche, le critère de spécificité à un message échoue : les préférences persistantes par segment et les transitions de Markov passent toutes. Ces derniers générateurs ne transmettent aucun passage cible ; le modèle de Markov hérite de statistiques linguistiques et peut produire des fragments accidentellement intelligibles. Nous ne prétendons pas démontrer qu'il est dépourvu de toute signification possible.

Ce contre-exemple est central : une association stable entre mots ne constitue pas, à elle seule, une preuve sémantique. Les six cas d'une famille ne sont pas six auteurs indépendants, et les taux ci-dessus ne sont pas des estimations universelles de sensibilité ou de spécificité.

La sensibilité prévue à 150 types conserve 6/6 réussites pour les codes bijectifs et 0/6 pour Timm. Elle ne corrige pas l'échec de spécificité observé à 300 types.

[Contrôles et manuscrit, avec le critère fixé](../docs/PIECES_REFERENCES.md#piece-47c7d53a38754a)

## Manuscrit : aucun franchissement du critère

La calibration de sensibilité autorisait l'exécution sur le manuscrit. Toutes les variantes prévues sont conservées, sans sélectionner la meilleure.

| Transcription / variante | Types | Mots utilisables | ρ | p conditionnel | Critère |
|---|---:|---:|---:|---:|---|
| ZL stricte, principale | 300 | 22 373 | 0,09416 | 0,020 | Non |
| ZL stricte | 150 | 22 373 | 0,05197 | 0,005 | Non |
| ZL, virgules traitées comme jointures | 300 | 24 955 | 0,08978 | 0,010 | Non |
| IT stricte | 300 | 27 844 | 0,08519 | 0,005 | Non |
| IT stricte | 150 | 27 844 | 0,05812 | 0,005 | Non |
| IT, virgules traitées comme jointures | 300 | 27 844 | 0,08519 | 0,005 | Non |

Les variantes utilisent les mêmes 85 folios, mais les conventions de transcription et d'admission des segments changent les effectifs. Seuls les contrôles et ZL principale ont exactement le même cadre. La variante de jointure IT est identique à IT stricte sur ces données ; ce n'est pas une confirmation supplémentaire.

Certaines variantes dépassent les mélanges, sans atteindre l'amplitude requise. **Le seuil n'est pas abaissé après observation.** Le manuscrit n'est ni identifié comme copie ni identifié comme texte chiffré par cette expérience. Les échecs de trois contrôles à homophonie montrent notamment qu'un résultat négatif ne peut exclure la présence d'un message sous un codage différent.

## Vérification et portée de la preuve

Les [vérifications](results/verification.json) passent :

- 55 fichiers figés et 39 fichiers tiers vérifiés, dont 38 fichiers du générateur et le texte d'Austen, avec leurs empreintes Git exactes ; 42 cadres identiques et 12 allers-retours des chiffres vérifiés.
- Comptages complets et résidus des **60 configurations** recalculés par une autre arithmétique ; attentes vérifiées par coefficients binomiaux sur 7 680 cellules déterministes, en complément de l'énumération exhaustive de 1 440 permutations sur de petits exemples.
- Écart maximal des attentes : 2,42 × 10⁻¹³ ; des résidus : 5,56 × 10⁻¹⁵. Calcul indépendant des rangs concordant. Le diagnostic postérieur d'arrondi à 12 décimales change ρ d'au plus 1,58 × 10⁻⁶ ; il ne remplace pas la mesure figée.
- Répétition exacte des 199 permutations sur un contrôle bijectif, une sortie Timm et ZL principale ; nouvelle compilation et nouvelle exécution de la graine Java 81 reproduisant la sortie à l'octet près.
- Inventaires antérieurs revérifiés : phase 22, 150 fichiers ; phase 23, 50 fichiers ; atlas, 684 fichiers. Les anciens résultats restent inchangés.

Il s'agit d'une vérification technique par le même opérateur. Les groupes de folios sont une validation interne ; ZL et IT décrivent le même manuscrit. Un code publié externe ne fournit pas une confirmation externe du sens du manuscrit. Aucune relecture paléographique indépendante ni prédiction linguistique confirmée n'est ajoutée.

La méthode est une adaptation, **pas une reproduction**, de la mesure de paires présentée par [Zhang et Sheng, version 1](https://arxiv.org/html/2610.34499v1). Notre attente combinatoire, le choix des partitions, le traitement des incertitudes et l'absence de masque orthographique diffèrent. Les valeurs publiées ne sont donc pas directement comparables aux nôtres. Le périmètre de lecture et les sources figurent dans [l'audit](../docs/PIECES_REFERENCES.md#piece-a991c27a91dc2d).

## Conséquence pour le déchiffrement

Cette hypothèse n'apporte pas de clé, de langue ou de lecture continue. Elle empêche de traiter une nouvelle corrélation comme une traduction : même une réussite aurait été insuffisante au vu des générateurs à préférences persistantes. Réajuster le seuil ou isoler après coup les meilleures paires ne donnerait pas une validation.

Pour reprendre une piste de déchiffrement, il faudra une règle de lecture stable produisant des prédictions de mots et de passages, puis une validation réservée avant ces prédictions et une confirmation extérieure. Les observations actuelles peuvent contraindre des modèles concurrents ; elles ne fournissent pas encore cette règle. Les sorties négatives restent intégralement disponibles dans [le tableau](results/table.csv), [les résultats](../docs/PIECES_REFERENCES.md#piece-f42d286c49d603) et [la procédure de reproduction](README.md).
