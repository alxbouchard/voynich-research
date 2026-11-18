# Corrections et diagnostics postérieurs, sans remplacement des anciens résultats

## Images de la livraison30

Le code de l’atlas `voynich_visual_atlas/src/campaign.py` fabrique des vues limitées à 1800×1600 et réenregistre en JPEG qualité 94. Deux de ces vues ont été recopiées en phase 30, avec des empreintes exactes, mais décrites à tort comme natives. Les champs d’empreinte du fichier livré et de l’original étaient distincts ; c’est leur qualification textuelle qui était erronée.

| Fichier de phase 30 | Taille réelle | SHA-256 livré | Original natif récupéré en phase 31 |
|---|---|---|---|
| `critical_edition/images/f1r.jpg` |1263×1600 | `adc09a39272c7457b65ebcf9aeee79699cd9c47b28a53b379b737bee127326a2` |2972×3766, OID1006076 |
| `critical_edition/images/f116v.jpg` |1162×1600 | `93489000392c38b0ce4c9613fb5e6e080c384ff51fcf23567537af6de140bef2` |2686×3697, OID1006277 |

Les nouvelles empreintes natives correspondent au catalogue d’origine et sont dans `SOURCE_INVENTORY.json`. Aucun fichier de phase 30 n’est modifié. Ses essais chiffrés et leurs résultats n’utilisaient pas ces images et restent inchangés.

## Préparation31 avant les observations

Le premier contrôle d’empreinte a rejeté une vue réduite utilisée à tort comme image native. Le shell initial n’étant pas configuré pour s’arrêter à la première erreur, une fausse fiche de gel a été produite, pointant vers le commit précédent. Elle est conservée sous `preparation/INVALID_FREEZE_ATTEMPT.json` et n’est jamais utilisée pour les vérifications. Aucune nouvelle annotation ou intersection n’avait encore été exécutée. Après correction et acquisition des vrais natifs, le gel valide est `FREEZE.json`, commit `da26615448ecc12b9bf5cee8e58eddaf61023f1a`. Les étapes dépendantes suivantes s’arrêtent sur erreur.

## Clarification de l’unité de compte à f70v1

La fiche d’observation scellée donne 5–7. Sa borne basse correspond aux cinq groupes de légende spatiaux visibles dans l’anneau intérieur ; la borne haute mélangeait une éventuelle séparation de groupes avec des segments de mots et n’est pas un maximum établi. Elle ne doit pas être citée comme nombre possible maximal de mots.

La clarification postérieure retient **cinq groupes spatiaux**, chacun pouvant contenir plusieurs mots. Les cinq loci ZL sont f70v1.13–17 ; ils comportent respectivement1,1,3,3 et2 tokens sous leurs frontières, sans établir que ces frontières sont linguistiques. L’original est conservé et la correction est explicitement postérieure aux comptages. Le verdict « plusieurs, donc pas exactement un » ne change pas ; les dix autres panneaux sans groupe visible suffisaient déjà à contredire l’hypothèse universelle.

## Diagnostic des divergences de transcription

Les intersections pour avril ont motivé une inspection ciblée, non prévue comme adjudication indépendante. Les variantes `otal/otol`, `otolchdy/otol.chdy` et `otaldar/otal.dar` sont conservées. Les premiers crops f70v1.16, f71r.13 et f71r.17 visaient le mauvais anneau ou une zone voisine ; ils restent archivés comme tentatives non concluantes. Les fichiers suffixés `_inner` montrent les régions corrigées après distinction des anneaux. f70v1.11 était correctement localisé au premier essai.

Aucune image ni sortie de transcription n’est retouchée pour faire apparaître une correspondance. La présence d’un intervalle graphique ne prouve pas une frontière de mot. Les 528 comparaisons gelées restent inchangées ; le diagnostic ne sert pas à choisir `otol` ou `otal` comme traduction d’avril.
