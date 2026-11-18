# Audit indépendant des quatre groupes

Le seuil maximal en réserve H est **4 notices sur 87**. La seule suite à cette fréquence est `ar → chey → shedy → shey`, dans f113r.45, f115r.26, f116r.18 et f116r.31. Ce maximum est recherché après examen de la réserve. La suite fixée sur les 198 notices de découverte, `aiin → chedy → qokeedy → al`, y obtenait 7 succès et était seule au maximum. Elle donne **0/87** en réserve H et **1/89** en réserve ZL, avec le même succès dans les deux traitements de l’espace douteux.

## Vérifier f116r.31 sur le feuillet

Le paragraphe court des lignes 31 à 45 inclusivement. Les positions ci-dessous commencent à 1 et incluent les groupes incertains. Le premier écart décisif se trouve à la ligne 32, après `qor`. H transcrit `oiin`, ZL transcrit `aiin`. Les deux groupes suivants de la suite coïncident à la ligne 38, dans `chedy.qokeedy`. Le dernier `al` qui la complète se lit à la ligne 39.

| Témoin | Groupes dans le paragraphe | Positions de la première réalisation complète |
|---|---:|---|
| H | 157 | aucune occurrence de `aiin` |
| ZL, espaces incertains joints | 155 | 14, 83, 84, 96 |
| ZL, espaces incertains séparés | 167 | 16, 89, 90, 105 |

Cette vérification porte sur les deux transcriptions. Elle laisse ouverte la lecture paléographique de la ligne 32 sur l’image.

## Comparaison avec les notices latines

| Ordre | Découverte, 117 notices | Réserve à partir de 061r, 87 notices | Inverse en réserve |
|---|---:|---:|---:|
| `complexio → electio → iuuamentum → nocumentum`, unique meilleur ordre en découverte | 109 | 65 | 0 |
| `electio → iuuamentum → nocumentum → remotio`, rubriques historiques prédéfinies | 105 | 85 | 0 |

En réserve latine, le maximum est 85/87. Deux suites l’atteignent. La seconde est `electio → iuuamentum → remotio → nocumenti`. Les deux exceptions aux rubriques historiques sont 071r.1 et 089v.1. Sous le critère d’occurrence en sous-suite, les répétitions sont admises. Le contrôle distinct exigeant l’unicité de chaque mot mesure une autre propriété.

## Énumération et reproduction

Le programme lit directement les transcriptions et le JSON de l’édition. Il forme les ensembles non ordonnés en intersectant les masques de présence par notice. Un ordre apparaissant dans quatre notices requiert que ses quatre termes distincts soient tous présents dans ces mêmes notices. Il suffit donc de vérifier les 24 permutations de chacun des 123 ensembles présents dans au moins quatre notices H. Pour les 2 952 permutations ainsi retenues, la recherche par dichotomie des occurrences suivantes trouve précisément une suite à quatre et aucune au-dessus. L’algorithme d’origine n’est pas importé. Le JSON conserve tous les maxima, les positions des suites figées et les empreintes des quatre entrées.

Les tranches du résultat principal ne couvrent pas chaque longueur exacte commune demandée par le protocole. Le champ `longueurs_exactes_communes_reserve` de cet audit fournit les 18 longueurs partagées. Sur ces seules longueurs figurent 32 notices H, avec zéro succès pour la suite figée, et 50 latines, avec 37 succès pour la suite figée et 49 pour les rubriques historiques. Les sous-effectifs par longueur sont consultables dans le JSON.

Depuis le dossier de l’audit, avec Python 3.10 ou supérieur, exécuter la commande suivante en adaptant les chemins si les données ont été déplacées.

```sh
python3 auditer.py voynich_phase26/sources chemin-local/notices.json research/2026-11-18-notices-etoilees/PREDICTION_QUATRE.json > audit.json
```

Ces résultats concernent les identités de groupes et l’ordre dans les paragraphes sélectionnés. Ils n’attribuent aucune valeur sémantique aux groupes Voynich.
