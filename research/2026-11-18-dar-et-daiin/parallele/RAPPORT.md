# Le retour de daiin met à l’épreuve les cinq lectures de Celse

Nous avons comparé les groupes entiers de f18v.7 et f23r.7 à deux passages d’un même ouvrage de la forme X Y X et U V U. Les quatre mots clairs devaient être distincts. Pour représenter le `ch` supplémentaire de `qokchol`, le mot U devait pouvoir s’obtenir en ajoutant une ou deux lettres contiguës à l’intérieur de X. Ce modèle cherche des correspondances entre mots entiers. Les quatre affectations de chaque dictionnaire restent fixes. [Règle avant calcul](AVANT.md) · [Programme](dictionnaire.py)

## Du quatrième mot au dixième

Dans les sept corpus, **10 671 paires** satisfont le critère d’insertion intérieure. Seules six permettent de nommer en EVA le mot suivant du premier passage, et les six donnent `dar`, déjà connu de l’équipe. En admettant aussi l’insertion au bord du mot, on obtient 12 496 paires, 70 annonces et les mêmes six succès. Dans les extraits de Cambridge, quatre paires à insertion intérieure relient les formes anglaises *of* et *off*. Leurs voisins historiques sont extérieurs au dictionnaire appris. Elles s’abstiennent au mot de contrôle. [Annonces des sept corpus](ANNONCES-sept.json.gz) · [Vérification](OUVERTURE-sept.json.gz) · [Annonces de Cambridge](ANNONCES-cambridge.json.gz) · [Vérification à Cambridge](OUVERTURE-cambridge.json.gz)

Les six rapprochements retenus sont chez Celse. Ils imposent tous *et* pour `qokol` et *est* pour `qokchol`. Le tableau montre la lecture annoncée pour `daiin` et le mot de Celse à l’endroit où le scribe répète ce même groupe, au rang 10 de f23r.7. L’alignement avance d’un mot latin pour chaque groupe de signes. [Test fixé avant lecture à cette distance](LIGNES-AVANT.md) · [Deux directions d’alignement et tous les mots](LIGNES.json.gz)

| Valeur annoncée pour `daiin` | Valeur attribuée à `dar` | Paires de passages | Au rang 10, dans la phrase stricte | Au rang 10, dans le même paragraphe |
|---|---|---:|---|---|
| *crudele* | *supervacuum* | 1 | fin du segment avant le rang 10 | *a* |
| *plenus*, *modo* ou *tardius* | *non* | 3 | *gargarizare* dans les trois cas | *gargarizare* |
| *linum* | *id* | 2 | fin du segment avant le rang 10 | *et* pour l’un, *haec* pour l’autre |

Le passage de la phrase au paragraphe lève la barrière de ponctuation lorsqu’on peut retrouver le segment d’origine à une place unique. Il conserve les autres coupures du corpus. Dans cette fenêtre élargie, les six rapprochements imposent deux valeurs différentes à la même graphie. Permettre à plusieurs graphies de rendre un même mot latin ne résout pas cette contradiction. [Comparaison avec l’incunable de Florence](celse/RAPPORT.md) · [Script d’alignement](lignes.py)

## Le troisième passage et les autres feuillets

Sur f14r.5, les deux éditions donnent `qokchol dar dala qotolo` et `qokchol dar dalo qotolo`. Avec la lecture *est id*, *quod* est le voisin le plus fréquent dans les autres passages du corpus. On peut dès lors essayer d’attribuer *quod* à `dala` ou à `dalo`. Après *est id quod*, *habet* vient en tête avec **3 occurrences sur 12**. Cette majorité relative suggère pour `qotolo` une lecture conditionnelle, que la première table n’avait pas les moyens de prédire en EVA. Sur les feuillets réservés, `qotolo` n’a aucune occurrence concordante à tester. Aucun des six rapprochements ne fournit, dans le texte de Celse, le doublet visible après `qokol daiin` sur f102r2.18. [Critères de prolongement](SUITE-AVANT.md) · [Lectures et effectifs](SUITE.json.gz)

Avec la table *et / linum / est / id*, aucun des **14 couples de mots lisibles** sur les autres feuillets ne donne un couple attesté chez Celse. Les deux extensions par *quod* et *habet* donnent le même résultat. La table *et / modo / est / non* en retrouve quatre, tous dus à la même paire `daiin dar` lue *modo non*. Seize des 24 permutations des quatre valeurs font aussi bien ou mieux. Aucun triplet n’est lisible avec ces dictionnaires sur le lot réservé. À titre de comparaison, `daiin` y apparaît 617 fois sur 24 221 positions concordantes, et *linum* sept fois sur 101 718 mots dans Celse. [Calcul sur les autres feuillets](suite.py)

## Reproduction et portée du contrôle

Les trois entrées externes sont le [XML de Celse](https://raw.githubusercontent.com/PerseusDL/canonical-latinLit/669d3657637ee44fb0aed2c37dd0f95c2b062193/data/phi0836/phi002/phi0836.phi002.perseus-lat5.xml), [l’édition du *Viandier*](https://histolf.ulb.be/index.php/textes-gh/260-1450-viandier-taillevent-ms-vaticane-texte-et-traduction) et [l’édition de Martino](https://www.uni-giessen.de/de/fbz/fb05/germanistik/absprache/sprachverwendung/gloning/tx/martino2.htm). Les annonces contiennent les empreintes des versions utilisées. Les quatre autres corpus et les transcriptions du Voynich sont lus depuis le dépôt. [Provenance des corpus](../../2026-11-18-renvois-entre-plantes/phrase/RAPPORT.md)

Depuis ce dossier, placer les trois fichiers sources sous les noms employés ci-dessous, puis exécuter les commandes dans l’ordre.

```sh
python3 -B dictionnaire.py sept annoncer voy-f89-celsus.xml voy-d-formule-viandier.html voy-d-formule-martino.html
python3 -B dictionnaire.py sept ouvrir
python3 -B dictionnaire.py cambridge annoncer ../cambridge/CORPUS.json.gz
python3 -B dictionnaire.py cambridge ouvrir
python3 -B suite.py voy-f89-celsus.xml voy-d-formule-viandier.html voy-d-formule-martino.html
python3 -B lignes.py voy-f89-celsus.xml
```

Le contrôle positif archivé pour ce modèle emploie trois passages construits et des leurres. Il retrouve les deux voisins attendus. Le protocole envisageait aussi une calibration de ce modèle par mots entiers sur un passage historique chiffré à réponse connue. Elle restait à faire à la clôture de la séance. La séance précédente avait réalisé une telle calibration pour un autre modèle, qui attribuait des lettres aux signes. [Contrôle construit de cette séance](CONTROLE.json) · [Contrôle historique du modèle précédent](../../2026-11-18-renvois-entre-plantes/composant/paralleles/RAPPORT.md)
