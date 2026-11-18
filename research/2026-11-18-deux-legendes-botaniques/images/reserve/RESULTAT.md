# Une paire de plantes peut-elle être réservée sur d’autres feuillets ?

**Aucune nouvelle paire de dessins n’a pu être constituée avec la substitution annoncée.** En dehors de f89 et f100, les deux éditions donnent des inscriptions de fragments végétaux sur neuf panneaux de quatre feuillets physiques, 88, 99, 101 et 102. Sur les 120 emplacements de légende relevés, 83 possèdent un seul mot entièrement lisible et identique au même endroit dans les deux éditions et les deux traitements du blanc. Ces emplacements donnent 78 mots distincts. [Règle déposée avant le décompte](PROTOCOLE.md) · [Toutes les lectures admissibles et leurs lieux](resultats.json)

Dans cette réserve, 25 mots différents d’au moins trois unités comportent un `k` autonome, à 28 emplacements. Quatre mots comportent un `p` autonome et chacun n’apparaît qu’une fois. Les quatre proviennent du feuillet 102. Le tableau donne la forme attendue d’après la seule substitution fixée, avec conservation de toutes les autres unités.

| Mot en p | Lieu | Forme en k recherchée | Rencontres en réserve |
|---|---|---|---:|
| `opchytcy` | f102v1.6 | `okchytcy` | 0 |
| `ypcholdy` | f102v1.16 | `ykcholdy` | 0 |
| `opchdard` | f102v1.18 | `okchdard` | 0 |
| `opchy` | f102v2.13 | `okchy` | 0 |

Les 83 emplacements fournissent 2 385 comparaisons de deux lieux sur des feuillets différents. Parmi elles, 479 réunissent deux mots de la même longueur avec au moins trois unités chacun. Aucune ne diffère seulement par un `p` et un `k`. En permettant deux emplacements d’un seul feuillet de la réserve, la liste de paires reste vide. Les deux calculs, substitution dans le dictionnaire des formes et distance entre toutes les paires de mots de même longueur, sont vérifiés l’un contre l’autre. Un `p` ou un `k` à l’intérieur d’un banc indivisible comme `cph` ou `ckh` n’est pas une unité autonome. [Programme de contrôle](enumerer.py)

Ce résultat indique la limite de la répétition visuelle tentée sur de nouveaux feuillets. Les 37 emplacements écartés et les nombreux mots de prose demeurent hors de ce dépouillement. Les deux planches de départ documentent donc une seule paire de légendes. Pour reproduire le relevé depuis ce dossier, exécuter `python3 -B enumerer.py` avec les transcriptions distribuées dans le dépôt.
