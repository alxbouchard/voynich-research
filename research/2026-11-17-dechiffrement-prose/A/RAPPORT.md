# Recherche d’extraits historiques par substitution lettre à signe

Quinze correspondances de douze lettres dans les lignes communes aux deux transcriptions permettaient de prédire au moins huit signes du Voynich. Toutes ont échoué sur la suite. Le meilleur résultat sur ces lignes a donné trois signes justes. Vingt-six des 99 copies mélangées du corpus ont atteint ou dépassé ce maximum.

## Épreuve

Les trois passages sources proviennent de *De viribus herbarum* (armoise), de *De medicina* I.1 (Celse) et du *Régime du corps* (air). Les extraits commencent aux mots 1, 9, 17 et ainsi de suite jusqu’au mot 241, à condition qu’il reste assez de lettres. Les 81 extraits de 24 lettres représentent respectivement 23, 27 et 31 départs. Après normalisation des accents, de i/j et de u/v, ces extraits ont tous des motifs de répétition distincts sur les douze premières lettres. Dix extraits du premier passage, quinze du deuxième et dix-huit du troisième permettent de prédire au moins huit positions de la suite avec trois signes distincts ou plus.

Le test parcourt tous les départs de 24 unités disponibles dans chaque segment lisible d'une ligne P0. Une lecture indéterminée interrompt le segment. Les unités EVA composées sont reconnues dans les mots, puis les séparateurs entre mots sont effacés. Deux unités successives de mots différents gardent leur identité. Un début est compatible quand une clé injective associe les douze lettres aux douze unités EVA dans le même ordre. À chaque début compatible, la clé annonce l’unité attendue pour les lettres déjà rencontrées et s’abstient pour les autres. Le fichier de prédictions a été scellé avant tout calcul de scores. Les fenêtres glissantes peuvent se recouvrir.

## Résultats

| Transcription | Fenêtres de 24 unités | Débuts compatibles | Extraits distincts ayant un début compatible | Suites admissibles | Suites confirmées | Maximum de signes exacts par suite admissible |
|---|---:|---:|---:|---:|---:|---:|
| Lignes communes | 12 618 | 16 | 6 | 15 | 0 | 3 |
| ZL | 34 507 | 47 | 17 | 40 | 0 | 3 |
| IT | 58 087 | 71 | 22 | 60 | 0 | 3 |

Sur les lignes communes, six suites admissibles ont donné zéro signe exact, six en ont donné un, une en a donné deux et deux en ont donné trois. Huit des quinze venaient de Celse et sept de l’armoise. Les vues individuelles et leur intersection recouvrent physiquement les mêmes pages. Aucune clé n’a atteint le seuil qui permettait de passer à un autre folio.

Le premier candidat admissible avait été choisi comme exemple avant le calcul des scores. Au folio 77r, ligne 26, son début occupe les douze unités à partir de l’unité 12 du premier segment. Il est compatible avec un extrait commençant au mot 129 de Celse. La clé prévoit huit des douze unités de la suite.

| Position | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Prévision | ch | · | · | · | · | a | e | d | y | q | d | y |
| Observation | y | l | ch | e | d | y | q | o | k | a | l | y |

Le point marque une abstention. Seule la position 12 correspond, soit un signe juste sur huit annoncés.

## Contrôles et portée

Le moteur a retrouvé les 43 extraits admissibles implantés dans du bruit, chacun à une position aléatoire sous une clé tirée au hasard et cachée au moteur. Sur les 43 témoins dont la suite a été permutée au hasard, il a accepté zéro suite. Ces contrôles évaluent le cas favorable d’une copie exacte sous substitution simple. Une vérification par distances aux occurrences précédentes reproduit toutes les positions candidates, leurs prédictions et les comptes de succès des trois éditions.

Les 99 tirages nuls (graine 761101) permutent les unités au sein de chaque segment lisible de chaque ligne commune et répètent toute la recherche. Ils conservent la fréquence exacte des signes dans chaque segment et détruisent leur ordre. Ils produisent de 5 à 26 débuts compatibles (médiane 17) et de 4 à 20 suites admissibles (médiane 11). Aucun tirage n’a confirmé une suite. La comparaison secondaire du maximum de trois signes donne une probabilité de permutation unilatérale de 0,27 avec correction de Monte-Carlo, (26 + 1) / (99 + 1). Le résultat principal porte sur ces extraits, ces transcriptions et cette hypothèse de copie lettre à signe.

Empreinte SHA-256 des prédictions scellées avant score, `d13e3b6f0c9b57ac3458c0969aa72a50dd64294f9df5ea7401bbd697e53b202e`. Les scripts fonctionnent sous Python 3 avec sa bibliothèque standard.

### Reproduction

Depuis le dossier contenant les scripts, renseigner les chemins des deux corpus JSON et un nouveau répertoire de résultats.

```sh
python3 -B essai.py calibrer --sources "$sources_historiques" --out "$resultats"
python3 -B essai.py predire --sources "$sources_historiques" --corpus "$lignes_voynich" --out "$resultats"
shasum -a 256 "$resultats/PREDICTIONS.json"
python3 -B essai.py ouvrir --sources "$sources_historiques" --corpus "$lignes_voynich" --out "$resultats"
python3 -B essai.py melanger --sources "$sources_historiques" --corpus "$lignes_voynich" --out "$resultats"
python3 -B auditer.py --corpus "$lignes_voynich" --out "$resultats"
```
