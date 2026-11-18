# Sept noms d’astres en marge d’un manuscrit de 1429

Bâle, Universitätsbibliothek, O.IV.4, ff. 11v–12r, conserve un court traité latin du pseudo-Ptolémée. Arnold Grub a copié en 1429 la partie du volume qui contient ces feuillets. Le texte est attesté dès le XIIIe siècle. Au XVe, le copiste de Bâle place le nom de chaque astre en marge. Dans la notice correspondante, la préposition latine *sub* introduit le même nom à l’ablatif. [Notice du manuscrit](https://ptolemaeus.badw.de/ms/601) · [Histoire du traité](https://ptolemaeus.badw.de/work/59)

| Section PAL | Folio | Nom marginal développé | Forme après *sub* | Position de *sub* | Position du nom |
|---|---|---|---|---:|---:|
| I.1 | 11v | Saturnus | Saturno | 7 | 8 |
| I.2 | 11v | Iupiter | Iove | 4 | 5 |
| I.3 | 11v | Mars | Marte | 4 | 5 |
| I.4 | 11v | Sol | Sole | 4 | 5 |
| I.5 | 11v | Venus | Venere | 4 | 5 |
| I.6 | 11v | Mercurius | Mercurio | 4 | 5 |
| I.7 | 12r | Luna | Luna | 4 | 5 |

Chaque fenêtre commence au premier mot du texte courant sous le sous-titre de l’édition. Elle inclut l’attribution à Ptolémée et s'étend sur seize mots. L’indexation commence à 1. L’appareil moderne, deux mots biffés dans la première notice et les restitutions éditoriales sont exclus. Les abréviations sont développées et les majuscules suivent l’édition. Dans ces conventions, une seule paire présente deux formes identiques. Les sept paires sont grammaticalement identifiables. La flexion de *Iupiter* offre le cas le plus éloigné graphiquement, avec *Iove*. [Transcription et variantes, David Juste, mise à jour du 18 août 2023](https://ptolemaeus.badw.de/ms/601/878/text/1)

La vérification sur les photographies a porté sur les sept emplacements marginaux, les premières lignes, la rature après le troisième mot de I.1 et la coupure de feuillet après le début de I.6. Sur le 11v, la rature reste lisible. La rubrique de Mars apparaît à gauche, en face du début de sa notice au milieu d’une ligne. Au 12r, la fin de la notice de Mercure précède la rubrique de la Lune en marge droite. Le départ de la notice lunaire se trouve à la fin d’une ligne et le couple recherché commence à la ligne suivante. [Fac-similé du 11v](https://ptolemaeus.badw.de/ms/601/878/11v) · [Fac-similé du 12r](https://ptolemaeus.badw.de/ms/601/878/12r)

À Lyon, Bibliothèque municipale, 172, ff. 52r–52v, l’appareil de David Juste signale l’omission des **sept** noms marginaux. Aucune variante du couple *sub* et nom n’y est signalée. Les variantes d’autres mots de chaque fenêtre sont décrites dans le JSON avec le numéro de la note éditoriale. Dans la notice solaire, le fac-similé du 11v place *eius* à la fin de la ligne et *domus* au début de la suivante. Le lemme de la note 28 confirme cet ordre. Le texte principal de l’édition en ligne intervertit ces deux mots, aux positions 10 et 11. Le jeu figé conserve l’ordre de l’édition pour sa reproductibilité. Une lecture conforme à la photographie s’obtient en échangeant ces positions dans I.4. Cette correction laisse *sub* au mot 4 et *Sole* au mot 5. La vérification photographique directe porte sur Bâle. Les données de Lyon viennent de la collation publiée. Les deux manuscrits transmettent le même texte. [Collation](https://ptolemaeus.badw.de/ms/601/878/text/1) · [Notice du témoin lyonnais](https://ptolemaeus.badw.de/ms/602)

## Reproduction

Le JSON conserve les seize mots normalisés de chaque notice sous forme d’indices dans un vocabulaire fourni, leur empreinte SHA-256, les positions recherchées et les liens précis. Les 112 mots peuvent être restitués hors ligne avec Python 3. Chaque empreinte porte sur les seize mots joints par un espace simple, en UTF-8 avec la casse fournie et sans ponctuation.

```sh
python3 extrait_bale.py --windows
curl -fsSL 'https://ptolemaeus.badw.de/ms/601/878/text/1' -o pal-source.html
python3 extrait_bale.py --html pal-source.html | diff - bale1429.json
```

Les données de texte sont dérivées de la transcription de David Juste, *Ptolemaeus Arabus et Latinus*, 18 août 2023, par retrait de l’appareil critique, découpage des fenêtres et indexation. Le jeu a été constitué avant la comparaison au Voynich. Empreinte du fichier des données figé le 18 novembre 2026 : `7a374e298fd49f8fd88439c1a0acacfb0ed84498bb47d3962608d6e52f22b338`. [Transcription source](https://ptolemaeus.badw.de/text/M878) · [Licence CC BY 4.0 du corpus](https://gitlab.lrz.de/badw-data/pal-texts/-/blob/master/LICENSE.md)
