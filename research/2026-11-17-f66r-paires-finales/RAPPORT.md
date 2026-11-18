# Les signes vont-ils par paires sur f66r ?

**La lecture par paires n’a prédit aucune des cinq finales réservées.** Les premiers exemples suggéraient que le signe pair transcrit `o` annonçait une fin en `y`. Sur le douzième mot, le premier cas réservé auquel cette règle s’appliquait, les deux éditions et une lecture photographique séparée donnent `n`. [Planche des cinq prédictions](../../docs/PIECES_REFERENCES.md#piece-9af775b44ec7f4) · [Résultats par règle et par édition](RESULTATS.json)

## L’idée mise à l’épreuve

La colonne de gauche de f66r contient 15 mots courts. La colonne médiane comporte 34 entrées. Jorge Stolfi a envisagé que ces entrées forment **17 paires** et que deux mots manquent à gauche. Il a aussi noté le décalage au milieu du feuillet. Nous avons ajouté une hypothèse précise et testable : le second signe d’une paire permettrait de prédire la dernière unité graphique du mot correspondant. Les lettres EVA qui suivent désignent des formes d’écriture. [Note 034 de Stolfi, section f66r](https://www.ic.unicamp.br/~stolfi/EXPORT/00-EXPORT/Notes/034/Note-034.html) · [Feuillet entier, Yale](https://collections.library.yale.edu/iiif/2/1006192/full/full/0/default.jpg)

Les 34 marques et les initiales des 15 mots étaient déjà connues du projet. Nous avons réservé les **finales des mots 11 à 15** pour cet essai. Le protocole a été déposé dans le commit local `b31dc37`. Les prédictions, les entrées d’apprentissage et les affectations ont été enregistrées dans `1781142` avant d’afficher les mots réservés ou les réponses du lecteur de la photo. Les entrées des deux éditions avaient déjà été publiées. [Protocole](PROTOCOLE.md) · [Annonces gelées](PREDICTIONS.json)

## Affecter les paires avant de lire les finales

Deux relevés indépendants de la hauteur de l’encre, calculés sur le cliché Yale, donnent les mêmes 15 correspondances. Sur les 136 choix possibles de deux paires à laisser sans mot, les deux mesures minimisent la distance verticale avec les **paires 6 et 14** laissées de côté. Le meilleur choix suivant écarte les paires 6 et 13. Il déplace seulement le mot 12 de la paire 13 à la paire 14. Dans le relevé B, il suffirait de déplacer le centre de ce mot de 1,45 pixel, à centres des paires fixes, pour égaliser les deux coûts. L’organisation physique justifie donc de vérifier les deux lectures à cet endroit. Les paires laissées de côté sont un choix du modèle. La photo seule ne démontre aucune omission du scribe. [Positions, coûts et 136 affectations](geometrie/COUTS.json)

## Cinq mots réservés

Sur les dix premiers mots, deux paires à second signe `o` sont associées à la finale `y` (mots 1 et 8). C’est l’unique relation apprise avec au moins deux exemples concordants dans la lecture commune. Les autres ne donnent aucune annonce de la table. La finale majoritaire de l’apprentissage est également `y`.

| Mot | Paire | Copie du second signe prédite | Finale prédite par la table | Finale ZL, IT et lecture photo |
|---:|---:|:---:|:---:|:---:|
| 11 | 12 | x | — | y |
| 12 | 13 | o | y | n |
| 13 | 15 | t | — | l |
| 14 | 16 | x | — | a |
| 15 | 17 | d | — | l |

La copie obtient **0/5**. La table apprise émet **une prédiction fausse et quatre abstentions**. Prédire `y` partout donne 1/5, au mot 11. Les tests exacts sur la réserve et les corrections de Holm donnent 1 pour les deux règles. Au deuxième meilleur alignement, la copie échoue encore cinq fois et la table s’abstient cinq fois. Ces résultats se reproduisent dans chaque édition séparément. [Mots dévoilés dans les deux éditions](RESERVE.json) · [Tableau complet](RESULTATS.json)

Un lecteur IA distinct a examiné des recadrages de la colonne de gauche dans un ordre mélangé, sans les transcriptions, sans les marques médianes et sans les prédictions. Il a donné une finale pour 13 des 15 mots. Pour la réserve il donne `y, n, l, a, l`, avec une confiance moyenne pour le mot 12 et forte pour les quatre autres. ZL et IT transcrivent le mot 12 respectivement `saiin` et `raiin`, avec la même dernière unité. Cette mesure corrobore la forme des finales et ne leur donne aucune valeur sonore. [Réponses photographiques originales](photo/lectures.csv) · [Planche anonymisée](../../docs/PIECES_REFERENCES.md#piece-f935732e092b66)

## Les deux omissions peuvent-elles sauver la règle ?

Nous avons ensuite essayé les **136 affectations** en conservant l’ordre des mots, y compris celles qui contredisent leur position physique. Dans la lecture commune, l’affectation retenue sur la photographie reproduit 2 finales sur 11 couples entièrement évaluables à ce bord. Le meilleur score en choisissant les omissions après lecture monte à **3 finales confirmées sur 15 positions**, avec 11 à 12 positions évaluables selon le choix. Dix-huit affectations atteignent ce maximum. Aucune des 136 ne donne un seul mot dont **les deux bords** répètent littéralement les deux signes avec accord des éditions. La convention stricte écarte les champs incertains. Si on créditait toutes les incertitudes compatibles, les maxima théoriques de la lecture commune seraient de 7 pour les finales et de 4 pour les deux bords. [Résultats détaillés](OMISSIONS.json)

Nous avons permuté les douze finales lisibles en laissant les trois autres positions indéterminées en place. Pour chacun des **110 880 ordres distincts**, nous avons de nouveau choisi les omissions qui avantagent le plus la règle. **7 770 ordres** font aussi bien, soit **7,01 %**. Les rotations, qui conservent mieux l’ordre local, atteignent ce score dans **3 cas sur 12**. La permutation suppose les finales échangeables entre ces positions. Elle ne mesure pas la probabilité que le manuscrit contienne un message. [Calcul exact](PERMUTATION_EXACTE.json) · [Recomptage intégral indépendant](audit/RECOMPTAGE.json)

Une table de correspondance inconnue, reconstruite **après** lecture de tout le feuillet, est un critère plus permissif. Avec la seule information commune certaine, cinq affectations sur 136 évitent toute contradiction, en omettant la paire 12 ainsi que l’une des paires 1 à 5. Elles ne sont pas les minima géométriques. Dans chacune des éditions, prise séparément avec davantage de données lisibles, aucune affectation n’évite les contradictions. Dans un contrôle supplémentaire, la variante de ZL au début du mot 2 (`[r:s]als`) laisse sa finale `s` intacte. Sa réintégration réduit les cinq affectations compatibles à trois, sans aucun effet sur les cinq prédictions réservées. [Sensibilité aux variantes internes](SENSIBILITE.json)

Ce qui échoue ici est la tentative d’utiliser le second signe de chaque paire pour **lire la fin du mot de gauche**. Une fonction de la paire entière comme unité ou un autre emploi de la colonne restent ouverts. Aucune des valeurs testées ne permet de traduire un mot.

## Recalcul

Dans ce dossier, exécuter `python3 -B geometrie/calcul_original.py`, `python3 -B paires.py calibrer`, `python3 -B paires.py rejouer`, puis `python3 -B exact.py` et `python3 -B sensibilite.py`. Le calcul de la meilleure affectation a été confronté à l’énumération des 136 choix sur 300 cas artificiels. Un cas positif recouvre les 15 finales après deux insertions. Les fichiers d’apprentissage et de réserve sont séparés. [Calcul principal](paires.py) · [Calibration](CALIBRATION.json)
