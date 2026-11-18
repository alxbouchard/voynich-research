# Contrôle du rapprochement publié pour f88v.4

La lecture de départ tient dans les deux transcriptions. L’étiquette de fragment végétal f88v.4 (`@Lf`) porte bien `otar arody`. **La paire entière a zéro occurrence dans le cahier 20**, y compris lorsqu’on autorise deux lignes successives d’un même paragraphe. Les six exemples donnés par Dennis Martin Herbers emploient des formes différentes de l’étiquette. La plupart de ces lectures se reproduisent aux emplacements annoncés. [Analyse 202 de l’auteur](https://www.dmh.dev/data/attack202_pharmaceutical_albarelli_registers_and_recipe_bridge.json) · [Takahashi](https://www.voynich.nu/data/IT2a-n.txt) · [Zandbergen–Landini](https://www.voynich.nu/data/ZL3b-n.txt)

| Locus des notices | Variante publiée | Lecture ZL | Lecture H | Position de la forme dans la notice |
| --- | --- | --- | --- | --- |
| f105r.6 | `par arody` | Oui | `por arody` | Premiers segments du paragraphe |
| f105v.29 | `karody` | Oui si la virgule suivante sépare les mots | Oui | Sixième segment de la première ligne quand on coupe à la virgule |
| f112v.39 | `teodarody` | Oui | Oui | Premier segment du paragraphe |
| f114v.37 | `tar arody` | Oui | Oui | En fin de la deuxième ligne d’un paragraphe de six lignes |
| f115v.13 | `pchdarody` | Oui | Oui | Premier segment du paragraphe |
| f116r.19 | `qotar ar arody` | Oui | Oui | À partir du cinquième segment de la deuxième ligne d’un paragraphe de treize lignes |

Les exemples de l’auteur sont présents pour **6/6 dans ZL** en coupant aux virgules et **5/6** en les joignant. H en donne **5/6** sous les deux conventions. Trois des formes publiées occupent le tout début d’un paragraphe dans ZL, deux dans H. Le guide réunit les parallèles sous la notion de formule d’ouverture, tandis que son JSON distingue plusieurs rôles dans la recette. Sa description de f114v.37 correspond à une fin de ligne. Le paragraphe se poursuit quatre lignes plus loin. [Guide de l’auteur, § 49](https://www.dmh.dev/voynich/library?doc=plain-english-visual-readers-guide&subtab=docs) · [Relevé détaillé par l’auteur](https://www.dmh.dev/data/attack202_pharmaceutical_albarelli_registers_and_recipe_bridge.json)

## Mots entiers des étiquettes de f88v

Les 13 loci Lc/Lf de f88v donnent 14 segments dans chaque édition. **Cinq sur quatorze (35,71 %) figurent sous leur forme entière dans le cahier 20**. Le nombre publié est reproduit dans les deux éditions et avec les deux conventions relatives aux virgules.

| Forme | Étiquette | Occurrences H | Occurrences ZL, virgules coupées | Occurrences ZL, virgules jointes |
| --- | --- | ---: | ---: | ---: |
| `cheocthy` | f88v.2 | 2 | 2 | 2 |
| `cpheor` | f88v.3 | 1 | 1 | 1 |
| `otar` | f88v.4 | 53 | 59 | 50 |
| `arody` | f88v.4 | 8 | 7 | 7 |
| `okaiin` | f88v.14 | 94 | 97 | 97 |

Le taux distinct de 64,29 % publié par Herbers compte des radicaux après regroupement de formes. Il n’a pas été recalculé ici. Son test de permutation publié dans le même JSON porte sur f99v. Il ne fournit donc pas de comparaison aléatoire pour le résultat de f88v. [Tableaux de l’analyse 202](https://www.dmh.dev/data/attack202_pharmaceutical_albarelli_registers_and_recipe_bridge.json)

## Portée du contrôle

La reprise de cinq formes entières est une observation reproductible. Pour passer de cette observation à une lecture de préparation d’une même racine, l’auteur doit traiter les six variantes comme grammaticalement apparentées et interpréter l’image pharmaceutique ainsi que la prose des notices. Les deux affirmations vérifiées ici n’apportent ni nom botanique unique ni quantité mesurable, et ne produisent aucune lecture indépendante d’un passage nouveau. Les lieux des variantes étaient déjà connus de l’auteur au moment de leur publication.

Le [gel préalable](CLAIMS.md) a pour SHA-256 `484032b470751429304b26faadde80f2158edc9fec30f4f561236f67df7054ad`. Exécuter `python3 research/2026-11-18-paires-ingredients/sources-dmh/verifier.py` pour régénérer la [vérification par édition et par segmentation](verification.json).
