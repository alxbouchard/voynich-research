# Phase 43 — une clé publiée passe-t-elle un contrôle de déchiffrement ?

**Aucune clé ni traduction validées.** Nous avons exécuté deux modules publics de la proposition Stalnecker et testé leurs dépendances. Ils reproduisent les résultats annoncés, mais ces résultats ne constituent pas une vérification des valeurs phonétiques. Le décodeur supplémentaire nommé pour un exemple décisif n'est pas présent dans la version inspectée.

## Ce qui a été exécuté

La version examinée est le commit `60536d3d425b1e1d9d25a0d9bff2cd145be7205b` de [VoynichPapers](https://github.com/Frederick-Stalnecker/VoynichPapers/tree/60536d3d425b1e1d9d25a0d9bff2cd145be7205b). Dix fichiers originaux sont conservés avec leurs empreintes Git et SHA-256. L'arbre complet comporte 61 entrées et n'est pas tronqué. Les transcriptions ZL et IT proviennent des phases précédentes. Le code était déjà lu avant le gel de notre [protocole](PROTOCOL.json) : il s'agit d'un audit, pas d'une confirmation aveugle.

Les deux modules sont chargés tels quels. Leurs seules sorties sont redirigées vers des dossiers temporaires ; les modifications de contrôle restent en mémoire. Aucun corpus n'est fourni à leurs fonctions de test, qui ne le demandent pas.

| Expérience exécutée | Résultat |
|---|---|
| Module de rotation, données originales | R = 14, neuf accords, `PASS` |
| Mêmes positions, phonèmes et justifications remplacés par des valeurs arbitraires | Scores et `PASS` inchangés |
| Dix-sept jeux artificiels imposant chacun une rotation différente | La fonction de score retrouve chaque rotation imposée |
| Module du syllabaire, fiches originales | `PASS` |
| Termes et sens remplacés ; alternatives déclarées connues ; indicateurs de réussite conservés | `PASS` maintenu |
| Un indicateur de réussite passé à faux | `PASS` devient faux |

Ces contrôles montrent exactement les dépendances des programmes. Ils ne prétendent pas que les valeurs arbitraires sont des traductions possibles.

Dans le [module de rotation](https://github.com/Frederick-Stalnecker/VoynichPapers/blob/60536d3d425b1e1d9d25a0d9bff2cd145be7205b/scripts/1_cipher.py), les neuf différences entre position cible et position de départ valent déjà14. Le code compare les positions, sans comparer les phonèmes. Retrouver14 vérifie cette cohérence. Les dix-sept contrôles portent sur la fonction de score ; le verdict global du module reste explicitement programmé pour exiger14.

Dans le [module du syllabaire](https://github.com/Frederick-Stalnecker/VoynichPapers/blob/60536d3d425b1e1d9d25a0d9bff2cd145be7205b/scripts/2_syllabary.py), le verdict combine les quatre indicateurs fournis et le nombre d'entrées déclarées confirmées. Il ne consulte pas de lexique pour décider si une alternative est possible. Les arguments linguistiques devraient donc être validés par d'autres éléments que ce résultat logiciel.

## L'exemple « kooiin » reste non reproduit

Le mot `kooiin` figure effectivement au début de f2v et de f29v dans ZL et IT ; `tsheos` figure au début de f3r. Les [lignes sources](results/AUDIT.json) sont conservées. Leur présence ne confirme pas les sens proposés.

Le [compte rendu publié](https://github.com/Frederick-Stalnecker/VoynichPapers/blob/60536d3d425b1e1d9d25a0d9bff2cd145be7205b/pre_registrations/pre_reg_f2v_kooiin_pomegranate_2026-07-25.md) vise une sortie `aanar`, associée à la grenade. La fonction simplifiée fournie produit `kaa-in`, ce que notre exécution retrouve et que l'auteur reconnaît déjà. Un autre programme, `decode_paper_v1.py`, est cité pour confirmer la lecture complète ; il est absent de l'arbre figé. **Nous n'avons donc pas reproduit ce décodeur et nous ne prétendons pas l'avoir réfuté.**

Le [fichier botanique public](https://github.com/Frederick-Stalnecker/VoynichPapers/blob/60536d3d425b1e1d9d25a0d9bff2cd145be7205b/data/botanical_dataset.json) contient109 fiches de folios avec des identifications déjà attribuées, sans lexique de noms phonétiques candidats. Sa fiche f2v porte le lotus, tandis que le papier revendique la grenade. Cela peut refléter des étapes différentes du projet, mais ne permet pas une confirmation indépendante. Le TSV de f108r contient494 lignes de sorties stockées ; il ne remplace pas le programme nécessaire à leur reconstruction.

Le [test réservé publié](https://github.com/Frederick-Stalnecker/VoynichPapers/blob/60536d3d425b1e1d9d25a0d9bff2cd145be7205b/experiments/pre_reg_held_out_decode_2026-06-05.md) reconnaît lui-même l'échec de son critère P3 : avantage de0,029 sur le témoin permuté, contre0,10 requis. Nous avons vérifié le document, sans réexécuter ce test dont le code nommé est absent de la version inspectée.

## Statistique et portée

Sous un modèle hypothétique où neuf rotations sont indépendantes et uniformes, la probabilité de neuf accords sur une rotation spécifiée est17⁻⁹ ; celle d'un accord sur une rotation quelconque parmi17 est17⁻⁸. Le code calcule la première. L'indépendance et l'absence de sélection historique des hypothèses ne sont pas établies par ce calcul. Ces nombres ne sont pas une probabilité que le manuscrit soit traduit correctement.

Le [contrôle séparé](results/verification.json) vérifie les sources, les calculs et les dépendances. La [reproduction](REPRODUCTION.md) recalcule les résultats en dossier neuf. Les avertissements d'espaces finaux des fichiers tiers sont conservés avec leurs octets originaux ; ils ne sont pas corrigés silencieusement.

**Décision : ne pas adopter cette table comme clé validée.** L'audit concerne les modules et exemples inspectés, pas toutes les statistiques du projet ni la possibilité générale d'une langue mongole ou tibétaine. Une poursuite de cette proposition nécessiterait le décodeur complet, des règles déterministes et des prédictions de passages sans significations fournies d'avance. L'objectif reste le déchiffrement du manuscrit, non atteint.
