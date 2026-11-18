# Phase 18 — substitutions à l’initiale ou à la finale

30 octobre 2026. **Aucune langue, clé ou traduction du Voynich validée.**

Les seize contrôles synthétiques passent les seuils fixés. Les deux modèles
ont ensuite été appliqués aux transcriptions, avec des pages réservées et
des mélanges de lettres respectant leur rôle dans le mot. Le critère exploratoire de poursuite est atteint pour : **finale / modèle latin**. Il autorise à concevoir une nouvelle étude, pas à identifier une langue ou à annoncer un déchiffrement.

[Comparaison des gains](https://github.com/alxbouchard/voynich-research/blob/7542c393ad441383c0d9957a1eee999682ba1f03/voynich_phase18/results/position_comparison.png)

## Question et protocole

La première expérience emploie une table pour la première lettre du mot,
la seconde pour sa dernière lettre ; chacune conserve une autre table pour
toutes les autres positions. Ce sont deux expériences distinctes. Un mot
d’une lettre utilise la table de position. Les espaces restent fixes, les
passages incertains et les fins de ligne interrompent les fenêtres de calcul.
Les caractères EVA sont des unités de transcription, sans phonétique connue.

Le [protocole](PROTOCOL.json), le solveur et l’orchestrateur ont été enregistrés
dans le commit local `876da79` avant la calibration de phase 18. Ce gel local
n’est pas une préinscription externe. Aucun paramètre de recherche n’a été
modifié après lecture des résultats de cette phase. Le contrôle de calcul et
la rédaction ont été ajoutés ensuite. Le [brouillon](PROTOCOL_DRAFT.md) est intact.

Chaque ajustement utilise huit redémarrages de 60 000 propositions, puis au
plus huit passes gloutonnes. Le choix de clé repose uniquement sur l’objectif
d’apprentissage. Le modèle à une table reçoit le même nombre de propositions ;
cette égalité ne garantit pas la même difficulté d’optimisation.

## Calibration : retrouver un texte dont la clé est cachée

Les modèles de langue proviennent de César et de l’Enfer/Purgatoire de Dante,
déjà archivés en phase 10. Les textes chiffrés sont Pline et le Paradis.
Quatre clés sont tirées pour chaque langue et famille : **seize essais sur
deux textes**, pas seize corpus indépendants. Le solveur ne reçoit ni les
textes clairs ni les clés vraies. Ces derniers servent à mesurer l’exactitude.

| Table distincte | Langue témoin | Clés | Exactitude minimale (%) | Position minimale (%) | Couverture minimale (%) | Seuils passés |
| --- | --- | --- | --- | --- | --- | --- |
| Initiale | Latin | 4 | 99,9930 | 99,9589 | 100,0000 | Oui |
| Initiale | Italien | 4 | 99,9954 | 99,9814 | 99,9954 | Oui |
| Finale | Latin | 4 | 99,9930 | 100,0000 | 100,0000 | Oui |
| Finale | Italien | 4 | 99,9926 | 99,9702 | 99,9926 | Oui |

Seuils préfixés : exactitude globale ≥99 %, aux positions concernées ≥98 %,
couverture des signes observés en apprentissage ≥99,5 %, sur les huit contrôles
de chaque famille. Les espaces ne comptent pas comme lettres correctes.
Les erreurs, y compris les signes non vus, restent au dénominateur.
Les réussites portent exclusivement sur ces chiffres synthétiques.

La meilleure clé ajustée peut encore être imparfaite : dans les contrôles,
l’objectif d’apprentissage dépasse celui de la clé vraie d’au plus
1,292101 unités. Même après une calibration proche
de 100 %, la maximisation de cet objectif n’est donc pas un certificat de vérité.

## Voynich : pages exclues de l’ajustement

Les groupes Currier A/B et les transcriptions ZL/IT sont traités séparément.
La liste lexicographique des feuillets physiques est réservée aux indices
0, 5, 10, etc. Recto et verso restent dans le même ensemble. L’apprentissage
est plafonné à 24 000 lettres en lignes complètes. Cette partition reproduit
la phase 10 : elle n’est pas nouvelle pour l’analyste et ne réserve pas des
cahiers entiers. Elle ne garantit pas une représentation équilibrée des mains
et sections. Voir [les feuillets exacts](https://github.com/alxbouchard/voynich-research/blob/7542c393ad441383c0d9957a1eee999682ba1f03/voynich_phase18/data/split.json).

Le gain est la diminution du score négatif de langue, en bits par fenêtre
de quatre caractères, espaces inclus, face à une seule table. Un gain positif
n’est ni un pourcentage de texte traduit ni une identification de langue.
Les valeurs absolues de deux modèles linguistiques ne sont pas comparables
comme probabilités de langue.

| Corpus | Modèle de langue | Table distincte | Gain | Étendue des 19 mélanges | Mélanges ≥ observé | Couverture (%) |
| --- | --- | --- | --- | --- | --- | --- |
| ZL / A | Latin | Initiale | 0,3173 | -0,1939 à 0,3099 | 0/19 | 100,00 |
| ZL / A | Latin | Finale | 1,0038 | 0,1223 à 0,5619 | 0/19 | 100,00 |
| ZL / A | Italien | Initiale | 0,2357 | -0,0368 à 0,3400 | 5/19 | 100,00 |
| ZL / A | Italien | Finale | 0,9965 | 0,6597 à 1,0486 | 2/19 | 100,00 |
| ZL / B | Latin | Initiale | 0,1099 | -0,0270 à 0,3665 | 7/19 | 99,99 |
| ZL / B | Latin | Finale | 1,1996 | 0,1028 à 0,5716 | 0/19 | 99,99 |
| ZL / B | Italien | Initiale | 0,6638 | 0,0069 à 0,4832 | 0/19 | 99,99 |
| ZL / B | Italien | Finale | 1,2437 | 0,7951 à 1,1147 | 0/19 | 99,99 |
| IT / A | Latin | Initiale | 0,6463 | Non calculé | — | 100,00 |
| IT / A | Latin | Finale | 1,1483 | Non calculé | — | 100,00 |
| IT / A | Italien | Initiale | -0,3609 | Non calculé | — | 100,00 |
| IT / A | Italien | Finale | 0,5587 | Non calculé | — | 100,00 |
| IT / B | Latin | Initiale | 0,1214 | Non calculé | — | 100,00 |
| IT / B | Latin | Finale | 1,1839 | Non calculé | — | 100,00 |
| IT / B | Italien | Initiale | 0,0347 | Non calculé | — | 100,00 |
| IT / B | Italien | Finale | 1,1880 | Non calculé | — | 100,00 |

IT est une autre transcription du même manuscrit, pas une réplication sur
un objet indépendant. Aucun témoin mélangé IT n’était prévu. Les décomptes
de dépassement sont descriptifs ; aucune p-valeur ni découverte corrigée pour
comparaisons multiples n’est revendiquée.

## Ce que les mélanges contrôlent

Pour chaque groupe ZL, dix-neuf témoins permutent les caractères dans les
groupes « feuillet physique × rôle dans le mot » : initiale, intérieure,
finale, singleton. Les longueurs de mots, les fins de ligne, les inconnues
et les fréquences de signes par rôle sont préservées avant filtrage des
segments courts. Apprentissage et test sont mélangés séparément. Les mêmes
témoins alimentent les deux modèles de langue et les deux familles.
Les clés sont réapprises intégralement sur chaque témoin.

**Limite vérifiée après exécution :** les segments de moins de quatre caractères
sont ensuite exclus. Un mélange peut échanger une lettre avec un tel segment.
Les fréquences par rôle ne sont donc pas exactement fixes dans le sous-ensemble
finalement noté : l’écart L1 maximal, sommé par feuillet/rôle/signe, vaut
212 occurrences sur les ensembles vérifiés.
Ce diagnostic ne change ni les tirages ni les résultats ; une éventuelle
suite devra laisser les segments exclus fixes avant de construire les témoins.

Ces mélanges détruisent beaucoup de contraintes locales, y compris celles
d’un générateur sans message. Les dépasser établit au plus une organisation
séquentielle. Cela ne suffit pas à démontrer le chiffrement testé.

## Vérification et portée

- 284 ajustements contrôlés : 32 sur témoins connus,
  24 sur transcriptions non mélangées et 228 sur mélanges.
- 6 260 056 prédictions de lettres réservées recalculées,
  en comptant les répétitions entre clés et modèles, pas des lettres uniques du manuscrit.
- Décodage, compte des positions, objectifs d’apprentissage, scores réservés,
  exactitudes et résumés recalculés par un second code Python.
- 76 ensembles mélangés vérifiés pour les longueurs,
  barrières et comptes par rôle avant filtrage.
- Cinq tests ciblés passent, dont le cas d’un alphabet partiellement absent
  et la séparation des passages inconnus.
- Les 1 771 fichiers de l’archive des phases 1 à 17 ont été vérifiés avant
  le travail ; ces expériences historiques n’ont pas été relancées.

Les deux codes de calcul partagent les données et modèles figés. Ce contrôle
interne n’est pas une réplication par une autre équipe ni une expertise
linguistique. Les clés et sorties complètes restent archivées sous le nom
`test_decoded_NOT_TRANSLATION`. Aucune phrase n’est déclarée traduite.

Les conclusions restent limitées au périmètre du test : deux permutations
de caractères, espaces conservés, deux modèles de langue et un budget donné.
Ils ne couvrent pas les homophonies, abréviations, ligatures, segmentation
conjointe, autres langues ou mécanismes sans message.

## Suite utile

Le critère exploratoire de poursuite est atteint pour : **finale / modèle latin**. Il autorise à concevoir une nouvelle étude, pas à identifier une langue ou à annoncer un déchiffrement.

Avant tout nouveau travail lexical, une suite devrait comparer les sorties
à des générateurs sans message plus structurés et à des chiffres connus,
préserver exactement les segments effectivement notés dans les mélanges,
et examiner la stabilité des clés sur des partitions de cahiers. Ces tests
restent à préparer et à exécuter ; aucun résultat de phase 19 n’est revendiqué.

[Instructions de reproduction](README.md) · [Résultats structurés](results/real_summary.json)
· [Vérification](results/verification.json) · [Attributions](../NOTICE.md)
