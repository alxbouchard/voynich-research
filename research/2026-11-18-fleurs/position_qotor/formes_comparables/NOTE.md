# Les mots voisins de qotor ont-ils aussi tendance à ouvrir les lignes ?

Deux lectures exactes de la même transcription par des programmes différents donnent les mêmes emplacements et rangs pour les quatre combinaisons (H ou ZL, toutes les pages ou main 1/Currier A). Dans les pages botaniques à partir du feuillet 25, Takahashi compte 4 débuts sur 10 occurrences et Zandbergen–Landini 5 sur 9, parmi 1 014 lignes P0. Les quatre débuts en commun sont f37v.8, f37v.16, f42r.11 et f49r.2. Le premier groupe de f36v.2 se lit `qotar` pour Takahashi et `qotor` pour Zandbergen–Landini. Les deux relèvent aussi `qotor` en cinquième position sur cette ligne. Les deux éditions s'accordent exactement sur huit positions au total, toutes positions confondues. [Résultats, rangs de chaque occurrence et empreintes des sources](RESULTATS.json)

Le contrôle compare les formes de cinq caractères EVA commençant par `qo`, avec une fréquence entre la moitié et le double de celle de `qotor`. Sur toutes les pages, on compte 8 formes admissibles chez H, dont 2 atteignent le taux initial de `qotor` (lui compris). Chez ZL, 1 sur 10 l'atteint. Dans le sous-ensemble de la même main 1 et de variété A, **`qotol` et `qotor` sont exactement à égalité dans chacune des deux transcriptions**. Les cinq débuts `qotol` concordent aux mêmes lieux dans les deux éditions : f36r.7, f37v.22, f45v.5, f47v.4 et f51v.7. Ils s'ajoutent aux débuts de `qotor` à d'autres emplacements. Les petits dénominateurs rendent les rangs sensibles à une seule lecture. Ce signal porte sur la position dans la ligne. Aucune valeur de prononciation, de traduction ou de classe grammaticale n'est établie. [Critères enregistrés avant le comptage des comparateurs](PROTOCOLE.md)

## Ensemble complet des formes admissibles

| Forme | H, toutes les pages | ZL, toutes les pages | H, main 1/Currier A | ZL, main 1/Currier A |
|---|---:|---:|---:|---:|
| `qodal` | 0/5 | 0/5 | 0/5 | 0/5 |
| `qokal` | 0/10 | 0/10 | — | — |
| `qokam` | — | 0/5 | — | — |
| `qokey` | 1/7 | 1/6 | 1/4 | — |
| `qokol` | — | 1/16 | 2/10 | 1/8 |
| `qokor` | 3/8 | 3/7 | 3/7 | 3/7 |
| `qotal` | 0/6 | 0/6 | — | — |
| `qotar` | 2/9 | 1/8 | — | — |
| `qotol` | 5/12 | 5/10 | 5/10 | 5/8 |
| `qotor` | 4/10 | 5/9 | 4/8 | 5/8 |

Chaque cellule indique le nombre de premières positions avec la forme sur son nombre total d’occurrences. Le tiret signifie que la forme est hors des bornes de fréquence du lot. Les bornes sont respectivement 5–20, 5–18, 4–16 et 4–16 occurrences. Les taux au moins égaux à celui de `qotor`, en l’incluant, se rencontrent chez 2/8, 1/10, 2/6 et 2/5 des formes. Ces fractions décrivent ce petit groupe de comparaison. Un classement de ce type ne constitue pas un test significatif du sens des mots.

Reproduction avec Python 3 : `python3 verifier.py /chemin/vers/voynich_20261028/data RESULTATS.json`. [Takahashi](https://www.voynich.nu/data/IT2a-n.txt) · [Zandbergen–Landini](https://www.voynich.nu/data/ZL3b-n.txt)
