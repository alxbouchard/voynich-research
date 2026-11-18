# Une légende entière permet-elle de retrouver le type de dessin ?

Parmi 445 étiquettes lisibles d'un seul groupe sur 19 feuillets, **quatre graphies** permettent de retrouver leur catégorie sur un autre feuillet avec la règle annoncée. Elles donnent neuf réponses justes. La même règle donne 61 réponses fausses et s'abstient 375 fois. La simple répétition du groupe entier ne permet donc pas, à cette échelle, de reconnaître de façon fiable un fragment végétal, une étoile ou une figure. [Méthode déposée avant le calcul](PROTOCOLE.md) · [Prédictions à chaque lieu](resultats.json)

| Dessin auprès de l'étiquette | Étiquettes retenues | Mot absent des autres feuillets | Égalité | Prédiction juste | Prédiction fausse |
|---|---:|---:|---:|---:|---:|
| Récipient de la section pharmaceutique | 18 | 17 | 0 | 0 | 1 |
| Fragment végétal | 130 | 103 | 2 | 5 | 20 |
| Figure des bains | 47 | 31 | 0 | 2 | 14 |
| Étoile | 48 | 44 | 0 | 0 | 4 |
| Cuve, conduit ou autre détail des bains | 31 | 22 | 0 | 0 | 9 |
| Figure du zodiaque | 171 | 137 | 19 | 2 | 13 |
| **Total** | **445** | **354** | **21** | **9** | **61** |

Les 714 emplacements de départ comprennent des mots multiples ainsi que des lectures incertaines. Les 445 inscriptions admissibles représentent 383 graphies distinctes. Seules 34 graphies se retrouvent sur plus d'un feuillet. Pour tester une inscription, le calcul retire toutes les inscriptions portant son numéro de feuillet, y compris les autres panneaux du recto et le verso. Les inscriptions sont déjà classées d'après leur place près des dessins. Pour une graphie donnée, chaque autre feuillet donne une voix à chacune des catégories où il l'atteste. [Données d'entrée et conventions](../../2026-11-18-deux-legendes-botaniques/lecture/tucker/prefixe/NOTE.md) · [Source des translittérations](https://www.voynich.nu/transcr.html)

Les neuf réponses justes viennent de quatre répétitions. **`otoky`** accompagne un fragment à f88r.5 et un autre à f99v.9. **`otoldy`** accompagne trois fragments, f89r1.4, f99r.14 et f99v.2. **`otoly`** revient auprès de figures à f75v.37 et f84r.11. **`okaram`** revient près de figures du zodiaque à f70v2.27 et f72r2.3. La réciproque emploie les mêmes observations. Les neuf réponses ne représentent donc pas neuf confirmations indépendantes. Dans la convention qui réunit les inscriptions deux à deux sur f75v, le premier `otoly` cesse d'être une légende entière d'un seul mot et les deux succès disparaissent. [Lieux et voix de chaque feuillet](resultats.json)

Deux erreurs désignent précisément les dessins à comparer. `ykchdy` accompagne un fragment à f100v.7 et une étoile à f68r1.29. Il en va de même pour `okos` à f99r.33 et f68r3.13. Le premier emplacement de chaque paire ferait prédire un autre fragment au second. Le manuscrit laisse ouverte la possibilité d’une propriété commune à ces objets. [Relevé des emplacements](resultats.json)

Sur les 70 lieux où la méthode donne une prédiction, annoncer la catégorie la plus nombreuse des autres feuillets réussit 7 fois, contre 9 pour le mot. La catégorie d'objet dépend fortement du feuillet. Les 48 inscriptions d'étoiles proviennent de deux feuillets, les 171 du zodiaque de quatre autres. Même une répartition aléatoire des catégories entre inscriptions du même feuillet donne **en moyenne 14,22 bonnes réponses** sur les 445 inscriptions, contre 9 observées. Dans 959 des 999 répartitions, le résultat atteint ou dépasse 9. Cette comparaison préserve le nombre de dessins de chaque catégorie et le vocabulaire de chacun des 19 feuillets. Seuls huit feuillets comportent plusieurs catégories admissibles et permettent un échange. Le test ne tranche pas entre le nom d'une espèce et celui d'une partie du dessin. [Calcul et contrôles](predire.py)

**Quelle place reste-t-il pour un mot générique ?** Dans ces légendes admissibles, la graphie végétale la plus courante est `otoldy` à 3/130, soit 2,3 %. Les 48 inscriptions d'étoiles ont toutes des graphies différentes. Les 18 inscriptions de récipients également. Le scénario où le scribe aurait écrit partout le même mot entier pour « étoile » ou « plante » échoue sur ces inscriptions. Le nom générique pourrait cependant figurer dans des inscriptions de plusieurs mots, sous des formes variables ou uniquement dans les paragraphes. De plus, une figure zodiacale peut tenir une étoile. [Inventaire par graphie et par contexte](resultats.json)

La variante qui réunit les paires de figures de f75v garde 427 emplacements admissibles et donne 7 réponses justes contre 53 fausses. Celle qui sépare chaque ligne des étiquettes de récipients garde 448 emplacements et donne 9 réponses justes contre 63 fausses. Les identifications zoologiques ou botaniques particulières demanderaient d'autres critères que ces catégories de mise en page.

Deux contrôles artificiels vérifient le fonctionnement du calcul sur les mêmes emplacements. Avec un mot constant par type d’objet, il retrouve le type aux 445 emplacements. Avec un mot propre à chaque feuillet, il s’abstient aux 445 emplacements.

Pour reproduire les trois calculs et les 999 permutations, exécuter `python3 -B predire.py` depuis ce dossier avec Python 3.10 ou supérieur. [Script](predire.py) · [Résultats complets et empreinte du fichier d'entrée](resultats.json)
