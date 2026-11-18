# Peut-on reconnaître une abréviation à partir des mots qui l'entourent ?

**Sur 23 développements annoncés, un seul restitue le mot de l'édition. Aux 22 autres endroits, le mot était déjà complet selon l'édition.** Le test porte sur un témoin lisible de *Piers Plowman*, le manuscrit HM 128 de la Huntington Library. Le programme ne connaissait ni les lettres ni la liste des abréviations. Dans cette expérience, une forme courte et une forme longue entre les mêmes voisins constituent un indice trop faible pour restituer un mot. La règle échoue au seuil fixé pour passer au Voynich. [Protocole](PROTOCOLE.md) · [Édition du manuscrit](https://piers.chass.ncsu.edu/texts/Hm/intro)

## Ce que le programme pouvait voir

Le programme cherchait un fait simple dans les premiers chants du poème. Si, entre les deux mêmes voisins, le copiste emploie deux mots dont l'un contient une à trois lettres de plus, peut-on développer le plus court au prochain emploi dans ce cadre ? L'annonce devait donner le mot entier. Les deux voisins et la forme courte devaient avoir déjà été observés ensemble. Une seule forme longue était admise par contexte. Le programme disposait des limites des vers et des mots. Les lettres étaient remplacées par des signes opaques et les marques d'abréviation elles-mêmes étaient masquées.

L'apprentissage porte sur 2 762 vers du prologue aux passus 1–9. Les passus 10–12 ont été laissés de côté. Le score porte sur 3 255 vers des passus 13–20. Le protocole a été enregistré au commit `b940d3e`, les trois programmes au commit `ff4dc07` et les [23 annonces](ANNONCES.json) au commit `ae8b1a7`, avant la lecture du corrigé. La valeur exacte à retrouver vient des lettres insérées par les éditeurs dans le XML. La réserve avait déjà servi au projet pour une autre question sur le trait nasal. Les décisions de cette expérience ont été fixées avant son score. [Précédente étude du manuscrit](../2026-11-18-abreviations-scribes/RAPPORT.md)

## Résultats

| Mesure | Résultat |
|---|---:|
| Positions intérieures admissibles, mot visible d'au moins deux signes | 23 359 |
| Mots abrégés selon l'édition à ces positions | 910 |
| Parmi eux, formes développables en insérant un bloc de 1 à 3 signes | 844 |
| Prédictions, formes courtes distinctes, passus représentés | 23, 14, 8 |
| Mots correctement développés | 1 sur 23 annonces (4,35 %) |
| Mots déjà complets allongés à tort | 22 |
| Abréviations pour lesquelles la règle s'abstient | 909 sur 910 |
| Réponse témoin « garder le mot visible » aux mêmes 23 positions | 22 réponses exactes |
| Réponse témoin « forme longue la plus fréquente » aux mêmes positions | 0 réponse exacte |
| Texte sans message produit par copie avec variations | 707 fausses expansions sur 6 000 positions (11,78 %) |

Le programme s'abstient à 23 336 positions. Compter ces abstentions comme des mots déchiffrés gonflerait artificiellement le score. La précision minimale fixée était de 80 % sur les annonces. Le taux de fausses expansions permis sur le texte sans message était de 1 % au plus. Cette simulation utilise une seule graine et un seul mode de copie. Elle montre concrètement comment le test peut trouver des abréviations dans un texte dont tous les mots sont complets par construction. [Résultats par passus et critères](RESULTATS.json) · [Témoin simulé](TEMOIN.json)

## Le cas réussi et deux erreurs

Au f. 178v, vers Hm.15.446, l'édition donne `alle man[er]e of`. Les crochets délimitent deux lettres restituées par les éditeurs. En partant des signes de `mane`, le programme a retrouvé `manere`. L'apprentissage contenait déjà les deux formes entre les mêmes voisins, la graphie abrégée en Hm.P.18 et la forme entière en Hm.2.57. La réussite porte sur un autre vers où revient cette expression. [Fac-similé du f. 178v](https://piers.chass.ncsu.edu/media/images/manuscripts/B/Hm/folios/Hm178v.jpg) · [Forme entière au f. 119r](https://piers.chass.ncsu.edu/media/images/manuscripts/B/Hm/folios/Hm119r.jpg)

En Hm.13.2, le programme développe `as` en `was` entre `and` et `a`. Les deux phrases sont possibles et le scribe avait bien écrit `and was a` en Hm.2.131. Le vers réservé porte `and as a`, avec `as` déjà complet. En Hm.18.243, il développe de même `he` en `sche` entre `that` et `was`. Cette fois, la substitution changerait le pronom. La vérification de ces trois exemples porte sur le XML. [Édition XML de HM 128](https://piers.chass.ncsu.edu/texts/xml/HmWhole.xml)

## Portée du contrôle

Le test porte sur les expansions explicitement encodées dans cette édition. Le dépouillement exclut 26 vers de l'apprentissage et 81 de la réserve, notamment en cas de lacune, de saut physique de ligne dans un vers ou d'expansion de remplacement difficile à aligner. La ponctuation sépare les unités, les ajouts éditoriaux de normalisation sont ignorés, et le signe & constitue une unité. Les formes aux extrémités des vers et les centres d'un seul signe sortent du test. Les données sont des transcriptions éditoriales. Le programme n'a pas examiné les traits de plume. Une seconde exécution en dossier neuf a reproduit à l'octet les sept fichiers intermédiaires et finaux. Un autre agent du projet a refait le décompte sur les entrées anonymisées avec son propre code. Il a retrouvé les 23 annonces, les deux scores témoins et les 707 fausses expansions de la simulation. [Détail de l'extraction](EXTRACTION.json)

## Refaire le calcul

Depuis le dossier de ce rapport, avec Python 3 et un répertoire temporaire. La copie complète de l'édition et son corrigé restent dans ce répertoire. L'extracteur contrôle l'empreinte de la source. Le scoreur vérifie l'empreinte des annonces avant d'ouvrir le corrigé.

```sh
atelier=$(mktemp -d)
curl -fsSL https://piers.chass.ncsu.edu/texts/xml/HmWhole.xml -o "$atelier/HmWhole.xml"
python3 -B edition.py "$atelier/HmWhole.xml" "$atelier"
python3 -B predire.py "$atelier/train.json" "$atelier/reserve.json" "$atelier/annonces.json"
python3 -B predire.py --temoin "$atelier/temoin.json"
python3 -B noter.py "$atelier/reserve.json" "$atelier/corrige.json" "$atelier/annonces.json" "$atelier/temoin.json" 35ba837c5db06a712f48cd252989971d6e68c5ae1e9e1ce9ebe7f51d57b6518e "$atelier/resultats.json"
cmp "$atelier/annonces.json" ANNONCES.json
cmp "$atelier/resultats.json" RESULTATS.json
```
