# Peut-on retrouver la page d’une plante du Voynich à partir de son étiquette ?

**L’étiquette a permis de retrouver trois notices sur six dans un herbier lisible de 1485. Dans le Voynich, une seule des neuf paires de dessins satisfaisait tous les critères matériels et visuels. Son étiquette, `tolsasy`, ne figure dans la prose d’aucune des 126 pages botaniques comparées, dans l’une ou l’autre transcription.** Parmi les huit étiquettes lisibles du lot élargi, aucune ne reparaît comme mot entier sur la page indiquée par le catalogue. La règle ne fournit donc aucune lecture botanique ou phonétique.

## Un cas qu’on peut vérifier sur les images

Sur la dernière rangée de f99r, on voit un fragment végétal près d’un vase. L’inscription f99r.46 est au-dessus de la jonction entre la partie orangée et sa tige. Le vase porte une autre inscription. Un troisième lecteur a revérifié cette disposition sur la page entière, sans lire les mots. Les deux premières lectures, faites séparément sur une carte où les inscriptions étaient masquées, ont sélectionné **C, f96v**, avec une confiance forte. Les deux décrivent la même combinaison de caractères, un segment brun coudé et de petites feuilles triangulaires espacées. Cette ressemblance reste compatible avec plusieurs interprétations botaniques. [Carte donnée aux lecteurs](../../docs/PIECES_REFERENCES.md#piece-32c8b317db21ad) · [Position sur le feuillet](../../docs/PIECES_REFERENCES.md#piece-e58f3895a43d13) · [Photographie de Yale](https://collections.library.yale.edu/iiif/2/1006246/full/1200,/0/default.jpg)

Les deux transcriptions donnent `tolsasy` pour le fragment. Dans le choix textuel, f96v était comparée à f2v, f27v et f53r, toutes de classe Currier A et de quantité de texte voisine. Sur les deux transcriptions, aucun des quatre débuts de page ne contient l’étiquette. L’extension à la page entière et la variante à une seule unité terminale ajoutée ou retranchée ne donnent pas davantage de correspondance. [Comptages par page et par édition](AUDIT.json)

## Que fait un herbier du XVe siècle ?

Les douze premiers chapitres numérotés du *Gart der Gesundheit*, édition de Mayence du 28 mars 1485, ont été pris sans sélection de leurs résultats. Les noms latins et vernaculaires imprimés dans chaque titre ont été cherchés parmi les 24 premiers mots du corps. L’emplacement de la grande initiale est vide dans cet exemplaire aux douze débuts. Les mots incomplets et ceux de lecture incertaine ont été masqués dans l'épreuve principale. La transcription des photographies, assistée par OCR et revue par un lecteur IA, est fournie avec ses incertitudes. [Témoin de la Bayerische Staatsbibliothek](https://www.digitale-sammlungen.de/view/bsb00032739) · [Transcription des douze chapitres](historique/corpus.json)

| Épreuve | Notices | Réponses émises | Bonnes notices | Abstentions |
|---|---:|---:|---:|---:|
| Choix de la règle sur les chapitres I–VI | 6 | 4 | 4 | 2 |
| Règle fixée, chapitres VII–XII | 6 | 4 | 3 | 2 |

La règle retenue est la répétition d’un mot entier du titre. Les trois bonnes réponses sur réserve étaient *Apium rusticum*, *Aristologia rotunda* et *Altea*. Dans leurs notices, des indices lisibles apparaissent respectivement aux positions 2 et 23 (*rusticum*, *apium*), 22 (*aristologia*) et 24 (*altea*). Une notice a été mal attribuée et deux titres restaient sans gagnante unique. Parmi les 720 redistributions des six titres, 12 égalent ou dépassent les trois bonnes réponses (p = 0,0167). Sous substitution bijective des signes, le moteur reproduit les mêmes décisions sans connaître leurs valeurs.

En ne retenant que la première dénomination lexicale de chaque titre, l’épreuve complémentaire donne encore trois bonnes réponses sur six, avec trois erreurs et aucune abstention (p = 0,05). Ce contrôle est plus proche des étiquettes Voynich formées d’un mot. Il ne supprime pas la différence entre une rubrique imprimée et l’inscription voisine d’un dessin. Rétablir les initiales laissées en blanc ou retirer complètement le premier mot conserve les trois réussites en réserve avec la règle principale. La calibration porte sur les douze premiers chapitres de cet exemplaire et plusieurs traitent de plantes nommées de manière proche. [Calcul sur la réserve](historique/RESERVE.json) · [Contrôle à un seul mot](historique/UN_MOT.json)

## Le test sur le Voynich

La liste de départ comprend 30 rapprochements ou entrées relevés dans le catalogue illustré des cahiers 15 et 19. Dix-sept n’avaient pas de légende indexée explicitement par le numéro du fragment dans les données utilisées, une avait plusieurs légendes, une plusieurs plantes candidates et deux étaient les exemples déjà étudiés. Restent **neuf cas**, dont deux décrits comme des plantes apparemment identiques dans le catalogue et sept comme des ressemblances. Ce sont des propositions publiées, et le recrutement des cas est limité à ces entrées. [Inventaire complet](visuel/INVENTAIRE.json) · [Cahier 15](https://voynich.nu/q15/index.html) · [Cahier 19](https://voynich.nu/q19/index.html)

Avant ouverture de la clé, le programme avait enregistré les prédictions des deux éditions sur **toutes les 129 étiquettes entières concordantes** et sur **126 pages botaniques** comptant au moins 24 emplacements dans chaque édition. Un choix de quatre pages était constitué pour chaque page possible, en contrôlant la quantité de texte et, quand elle était disponible, la classe Currier. Le moteur devait désigner la même page en Zandbergen–Landini et en Takahashi, seule en tête et avec au moins un mot correspondant. La liste de quatre pages proposée au lecteur de dessins était indépendante du choix textuel. Les vues complètes sont évaluées en fréquence par emplacement. [Protocole](PROTOCOLE.md) · [Prévisions enregistrées](PREDICTIONS.json)

| Sous-ensemble | Paires | Choix textuels sur les 24 premiers emplacements | Bonnes pages | Choix sur la page entière | Bonnes pages |
|---|---:|---:|---:|---:|---:|
| Attache sûre et même dessin retenu par les deux lecteurs avec confiance moyenne ou forte | 1 | 0 | 0 | 0 | 0 |
| Même critère visuel, en acceptant aussi l’attache éditoriale | 4 | 0 | 0 | 0 | 0 |
| Tous les rapprochements catalogués avec étiquette de lecture concordante | 8 | 0 | 0 | 1 | 0 |

Quatre cartes sur neuf ont donné le bon dessin chez les deux lecteurs au degré requis. Trois cartes sur neuf présentaient une inscription sans motif voisin concurrent sur la photographie. Les deux conditions coïncident sur la carte V05. Une des neuf étiquettes diffère entre les transcriptions, ce qui laisse les huit cas du dernier rang du tableau. L’unique choix émis sur page entière y était f53v pour `otoldy`, alors que le catalogue propose f44r. Cinq des huit étiquettes sont absentes comme mot entier de toutes les 126 pages dans les deux éditions. Dans les 40 320 permutations du lot élargi, aucune association n’obtient de bonne réponse en mode principal sur les débuts de page. La faible couverture rend ce test peu discriminant, et l'unique paire stricte ne permettait pas à elle seule d'atteindre le seuil de trois. [Décisions individuelles](visuel/DECISIONS.json) · [Résultats et permutations](RESULTATS.json) · [Couverture dans le reste de l’herbier](PORTEE.json)

**Correction des images.** La carte V09 a d’abord montré le quatrième fragment de la rangée, alors que le catalogue désignait le cinquième. La carte a été refaite sous l’identifiant V09b ; deux nouveaux lecteurs sans accès à la première image l’ont évaluée. Un seul a choisi la référence avec confiance moyenne. Les réponses à la carte d’origine sont exclues. V07 comprend une petite feuille possiblement rattachée au dessin voisin et sa légende reste difficile à attribuer. Les dessins ont été comparés par des agents IA distincts utilisant la même famille de modèles. Une expertise humaine indépendante reste possible à partir des images sources. [Journal de correction](visuel/CORRECTION.md) · [Lectures de la carte corrigée](visuel/lectures/CORRIGEE.json)

## Observation après ouverture : deux mots sur l’autre face

En examinant la répartition des huit étiquettes après le test, nous avons remarqué que deux figurent sur l’autre face du feuillet physique proposé, toutes deux dans la première ligne de prose. Les deux transcriptions concordent sur les mots.

| Étiquette | Dessin en pleine page proposé | Autre face où se lit le mot | Position dans la ligne |
|---|---|---|---|
| `opchor`, f100v.3 | f13v | f13r, ligne 1 | 7e mot en ZL et IT |
| `otoldy`, f99v.2 | f44r | f44v, ligne 1 | 10e en ZL, 9e en IT, du fait d’une coupure antérieure |

Les autres faces sont disponibles pour les huit cas. En redistribuant les huit étiquettes entre les huit références, 720 redistributions sur 40 320 produisent deux correspondances sur la face opposée. Ce calcul porte sur le texte entier de cette face. La face opposée a été choisie après observation, et la première ligne a été remarquée ensuite. La fraction n’est donc pas une probabilité confirmatoire. Les deux attaches de légende sont jugées ambiguës sur les photographies ; pour `otoldy`, les deux lecteurs se sont aussi abstenus sur le dessin. Aucun de ces deux cas n'appartient au lot strict. Les lignes sont vérifiables. Leur éventuelle fonction et leur sens restent inconnus. [Relevés IVTFF et décompte de toutes les permutations](verso/audit.json)

La prédiction à vérifier sur de nouveaux couples est maintenant écrite : une étiquette entière, de lecture identique dans les deux éditions, devrait réapparaître dans la première ligne de prose P0 de la face opposée au dessin en pleine page. Exclure de cette nouvelle épreuve les neuf cas examinés et les deux anciens pilotes. Fixer d'abord les rapprochements sur image et l'attache des inscriptions, puis comparer les premières lignes des deux faces et celles des feuillets témoins. Cette prédiction reste à éprouver sur d'autres données.

## Vérification

Les deux pages pilotes f18v et f23r sont exclues. Le protocole a été enregistré au commit local `5e88389`, les prédictions textuelles au commit `cd9e5f2` et le choix de la règle historique au commit `ee0d4e6`. Le fichier scellé des prévisions a pour empreinte SHA-256 `03e15cfeafe3895d7e4f0cc2e2c7b260e1c28821ddb29012588876a690eacaaf`. Une seconde implémentation a recompté 256 combinaisons de locus, d’édition, de choix et de page. Depuis le dossier extrait de l’archive, exécuter `python3 -B reproduire.py` pour reconstruire le corpus historique, les prévisions, les classements, les permutations et les résultats à partir des entrées archivées. Le code vérifie leur identité avec les fichiers de cette étude.
