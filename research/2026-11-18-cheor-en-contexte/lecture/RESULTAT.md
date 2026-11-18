# Peut-on lire la phrase qui reprend cheor ?

À la ligne 32, on peut faire coïncider trois groupes avec de véritables suites de mots latins ou allemands. La ligne 39 contient un voisin, `cheekey`, que les deux transcriptions lisent de la même manière. **Aucune table obtenue sur la ligne 32 ne donne pour ce voisin un seul mot du vocabulaire de l’ouvrage correspondant.** L’essai ne permet donc de retenir aucune de ces lectures. [Protocole](PROTOCOLE.md) · [Prédictions enregistrées](PREDICTIONS.json) · [Vérification des occurrences](VERIFICATION.json)

Le modèle suppose que chacun des signes transcrits `ch, sh, e, o, r, d, a…` représente toujours de une à deux lettres consécutives. Il autorise deux signes ayant même valeur et respecte les espaces de chaque version. L’essai élargi va jusqu’à trois lettres. Les 130 441 fenêtres de trois mots sont toutes examinées dans chaque version et avec chaque longueur maximale. Les sources ne traversent jamais une limite de notice ou de fragment éditorial retenue. Dans Celse, elles peuvent en revanche traverser une ponctuation de l’édition. La succession des textes n’établit aucun lien de copie entre le Voynich et ces quatre ouvrages ou corpus. [Provenance et détail des éditions](../../2026-11-18-phrase-et-doublets/lecture/RESULTAT.md)

| Source | Fenêtres de trois mots | Débuts compatibles sur les deux premiers mots, longueur maximale 2 / 3 | Triplets complets en lecture H, maximum 2 / 3 | Triplets complets en lecture ZL, maximum 2 / 3 |
|---|---:|---:|---:|---:|
| *Macer*, latin | 13 813 | 399 / 1 028 | 0 / 1 | 0 / 1 |
| Celse, latin | 100 053 | 3 249 / 7 233 | 0 / 14 | 2 / 9 |
| *Gart*, allemand, douze ouvertures | 201 | 6 / 10 | 0 / 0 | 0 / 0 |
| RIDGES, six extraits germaniques | 16 374 | 719 / 1 065 | 0 / 2 | 1 / 1 |

Un triplet est compté une fois par emplacement et par modèle, quel que soit le nombre de tables qui le donnent. La lecture H se termine par `sheor`, la lecture ZL par `shoar`. À titre d’exemple, les trois mots latins *quia nulla alia* permettent de lire `dar cheor shoar` avec deux tables à une ou deux lettres par signe. L’une exige que `cheekey` commence par *nulul*, l’autre par *null*. Dans le second cas, un autre *l* doit encore se trouver après la valeur de `k`. Aucun mot du lexique de Celse ne remplit toutes les conditions. Le même test donne zéro candidat pour les deux suites du *Macer* au maximum de trois lettres, *multis aliis vitiis* et *bis binis foliis*. Le mot *foliis*, « feuilles » au datif ou à l’ablatif pluriel, arrive en troisième position dans le second essai. Il correspondrait à `shoar` et ne fournit aucune lecture indépendante de `cheor`. [Tables détaillées](PREDICTIONS.json)

Le témoin déplace une copie de `e` en finale. Deux tables de Celse, au maximum de trois lettres par signe, donnent alors au moins un mot du lexique, mais aucun de ces mots ne suit le mot central obtenu sur un autre emplacement de Celse. La recherche d’un même passage comportant trois mentions échoue donc dès l’examen du voisin de la ligne 39. Les ambiguïtés d’espace de la ligne 33 ne peuvent sauver ces tables. Aucune prédiction ne livre une forme unique en contexte. Un programme indépendant recoupe les emplacements des triplets et les résultats des deux mots de la ligne 39 par expressions régulières à références arrière. [Programme de lecture](lecture.py) · [Contrôle indépendant](recouper.py)

## Que devient expressément l’idée de racine ou de plante ?

Un deuxième essai élimine l’obligation d’expliquer la ligne 32. On suppose simplement que `cheor` donne une forme de *radix* (racine), *herba* (herbe ou plante), *folium* (feuille) ou *flos* (fleur), puis on complète toutes les tables possibles pour son voisin `cheekey`. Le *Macer* offre 22 formes de ces quatre noms, présentes 213 fois. Chez Celse, on en trouve 19, présentes 132 fois. Une forme en fin de notice du *Macer* manque de voisin droit. **Aucune de ces hypothèses ne fournit le voisin dans le dictionnaire de l’ouvrage**, même en laissant jusqu’à trois lettres à chaque signe. Le contrôle de disposition admet des mots du lexique pour quatre flexions chez Celse, sans trouver le voisin correspondant dans le texte. Les paradigmes retenus omettent notamment les formes suivies d’une enclitique. [Règle fixée avant ce deuxième dépouillement](PREDICTION-ANCRE.md) · [Toutes les flexions et tous les dénominateurs](BOTANIQUE.json)

Cette difficulté touche tout le lexique. Dans une vérification exploratoire supplémentaire, on oublie le sens de `cheor` et on laisse tous les mots de l’ouvrage concourir. En permettant jusqu’à trois lettres par signe, 6 618 paires successives du *Macer* et 33 952 de Celse ont les longueurs requises. Aucune ne peut donner conjointement `cheor cheekey` avec cette table. Le modèle prévoit le même bloc de lettres trois fois dans le deuxième mot, dont deux fois de suite, avec un début commun au premier mot. Le zéro sur les quatre noms ne permet donc pas de les écarter au profit d’un autre sens. Le modèle et les répertoires font obstacle à toute lecture de ce type. [Comparaison sur tous les mots](TEMOIN-LEXIQUE.json) · [Calcul indépendant des paires](temoin_lexique.py)

## Reproduire

Depuis ce répertoire, télécharger le XML attribué à Perseus et exécuter les commandes suivantes. Le module de lecture contrôle l’empreinte du fichier. Les prédictions ont été enregistrées dans le commit `363828f` avant la vérification des concordances.

```sh
curl -L --fail -o /tmp/voy-f89-celsus.xml https://raw.githubusercontent.com/PerseusDL/canonical-latinLit/669d3657637ee44fb0aed2c37dd0f95c2b062193/data/phi0836/phi002/phi0836.phi002.perseus-lat5.xml
python3 -B lecture.py predire /tmp/voy-f89-celsus.xml
python3 -B lecture.py verifier /tmp/voy-f89-celsus.xml
python3 -B botanique.py /tmp/voy-f89-celsus.xml
python3 -B temoin_lexique.py /tmp/voy-f89-celsus.xml
python3 -B recouper.py /tmp/voy-f89-celsus.xml
```

[Contrôles à lecture connue](NOTE-ETALON.md)
