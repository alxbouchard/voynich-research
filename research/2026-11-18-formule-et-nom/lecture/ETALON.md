# Peut-on effectivement prévoir le troisième mot ?

Sur le premier passage du *Macer* qui satisfait la règle fixée, **la clé déduite de deux mots consécutifs prédit exactement le troisième, `aut`**. Le passage se trouve aux rangs 59 à 61 de la notice *Artemisia*. `Terendo bibatur` termine le vers 10 et `aut` ouvre le vers 11. La recherche respecte les frontières de notice et autorise ce passage d’un vers au suivant. [Vers et rangs dans l’édition de calcul](../../2026-11-18-opcheor-paralleles/latin/vers.tsv) · [Origine de la transcription](../../2026-11-18-opcheor-paralleles/latin/SOURCE.md)

La notice a été chiffrée au moyen d’un alphabet substitué qui préserve l’ordre des caractères, les espaces et la longueur des mots. On a choisi le premier triplet dont le troisième mot, long d’au moins trois lettres et différent des deux premiers, ne contient que des lettres de l’amorce, avec une contribution de chacun des deux mots. La condition construit délibérément un exemple où les lettres nécessaires sont disponibles. Le programme de recherche reçoit le triplet chiffré et les 77 notices de référence. La clé de chiffrement et l’emplacement choisi ne lui sont pas fournis. [Règle fixée avant lecture](PROTOCOLE.md)

| Étape | Résultat |
|---|---|
| Triplet chiffré | `KQBQHOJ IPIWKLB WLK` |
| Recherche des deux premières formes dans le livre | 1 emplacement sur 13 813 positions avec un troisième mot disponible |
| Seule amorce possible | `terendo bibatur`, dix lettres de la permutation déterminées |
| Prédiction gelée pour `WLK` | `aut` |
| Après révélation du troisième mot de chaque emplacement candidat | 1 sur 1 confirmé ; seule la position correcte subsiste |
| Inversion du troisième groupe chiffré en `KLW` | La même amorce prédit `tua`. Zéro position confirmée |
| Quatrième mot | La lecture de `AP` à clé gelée est `?i`. Le texte donne `si` |

L’unicité de l’emplacement était déjà acquise avant la révélation du troisième mot grâce à la longueur des deux premiers et à leurs répétitions de lettres. `aut` apporte donc une vérification exacte sans réduire le nombre de candidats. Seize lettres de l’alphabet restent inconnues. La comparaison par signatures de répétition a reproduit indépendamment les ensembles de positions obtenus aux deux étapes. L’essai mesure la capacité à retrouver une source qui figure à l’identique dans la bibliothèque de recherche. Pour le Voynich, ni le mécanisme d’écriture ni la présence d’un texte source exact dans la bibliothèque n’ont été établis. [Programme](etalon.py) · [Résultats complets](ETALON.json)

## Six mots construits avec les mêmes contraintes que f89v2.9

Le passage artificiel contient `ire bail beat bel maroon bail`. Deux de ses mots, `bail beat`, fixent la valeur de tous les signes du troisième groupe à prédire, `bel`. Le deuxième mot doit en outre réapparaître à la fin. Sous l’hypothèse d’une marque initiale muette, le texte artificiel devient `ire ail eat el maroon ail`. Ces suites ont été fabriquées pour vérifier l’algorithme. Elles n’ont aucun statut de phrase historique.

Les deux modes ont été testés avec un maximum de deux puis de trois lettres par signe dans les fonctions de l’étude `predict` et `confirm`. On a conservé les prédictions du passage intact pour tester les trois altérations. Les seize combinaisons distinguent les résultats suivants.

| Variante | Mot prédit | Répétition au dernier rang | Lecture des six groupes |
|---|---|---|---|
| Passage intact | Correct | Oui | La table de construction est retrouvée avec `i+i`. La lecture en un seul signe `II` accepte aussi la paire `oo`. |
| Dernier mot remplacé par `faux` | Correct | Non | Aucune des deux lectures de la finale ne passe. |
| `maroon` devient `maroxn` | Correct | Oui | Avec deux signes `i` identiques, aucune table ne passe. Avec `II` valant `ox`, une table passe. |
| Échange des deux derniers mots | Correct | Non | La règle déplacée retrouve la répétition au cinquième rang et la forme en `i+i` au sixième. |

Le témoin qui inverse les signes `e` et `y` dans la prédiction du troisième mot échoue dans les seize essais. Le passage intact est reproductible avec les mêmes fonctions que l’analyse du manuscrit. Exécuter `python3 -B etalon.py` depuis ce répertoire.
