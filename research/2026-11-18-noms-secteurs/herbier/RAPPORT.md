# Quelle notice peut-on retrouver à partir d’un nom ?

Sur 37 notices de Macer évaluées parmi les 77 de l’ouvrage, la forme latine avec quelques flexions retrouve seule la bonne notice **30 fois dans les 8 premiers mots et 32 fois dans les 16 premiers**. Si seules la longueur et les répétitions de lettres sont lisibles, le résultat tombe à **8 sur 37** à chaque fenêtre. La longueur seule ne donne aucune bonne première place unique. La lecture en contexte situe pourtant le nom de rubrique, ou une forme apparentée, dans les 8 premiers mots de 35 notices.

## Une série nouvelle, évaluée contre tout le livre

Les chapitres 41 à 77 sont tous retenus. L’étude précédente du même poème latin en hexamètres s’arrêtait à 40. Les 37 textes de validation sont donc nouveaux pour ce calcul, mais relèvent du même ouvrage et de la même édition. Chaque nom doit retrouver sa notice parmi les 77, avec une chance de 1 sur 77 (1,30 %) par choix aléatoire. Le logiciel vérifie que chacune des 77 rubriques précède un bloc de vers délimité, puis l’exclut avec les numéros de vers. *Gingiber* ne possède que 13 mots. Le texte évalué est la transcription de l’édition de 1845, révision 272959. [Texte latin](https://la.wikisource.org/wiki/De_viribus_herbarum) · [Source figée et provenance](../../2026-11-18-noms-dans-les-notices/historique/README.md)

| Information disponible | 8 mots, bonnes / réponses uniques émises | 16 mots, bonnes / réponses uniques émises | Rang moyen à 8 puis 16 mots |
| --- | ---: | ---: | ---: |
| Longueur seule | 0 / 1 | 0 / 0 | 27,84 puis 32,80 |
| Longueur et positions répétées | 8 / 11 | 8 / 10 | 21,19 puis 21,37 |
| Mot identique, alphabet connu | 17 / 18 | 19 / 20 | 21,55 puis 19,50 |
| Mot identique ou flexion prévue, alphabet connu | 30 / 31 | 32 / 33 | 5,16 puis 3,11 |

Toutes les lignes portent sur les mêmes 37 tentatives, ex æquo compris. Le rang moyen attribue le milieu de la plage en cas d’égalité, contre 39 par hasard. Si l’on impose une réponse en tirant au sort au sein du meilleur groupe, le taux moyen de première place avec le patron des lettres est de 30,03 % à 8 mots et de 29,88 % à 16 mots, contre 1,30 % au hasard. Les seules réponses uniques à 16 mots représentent 8 succès sur 10 propositions, contre 10/77 soit 0,13 succès attendus si leurs associations aux notices étaient aléatoires. Ces références arithmétiques ne supposent aucune indépendance entre les rubriques. Les deux intitulés qui commencent par *Elleborus* posent la même question au modèle. Ils restent ex æquo aux rangs 1–2.

La lecture de chaque ouverture retrouve 18 premières formes identiques au nom de rubrique, 18 flexions et une forme grecque apparentée (*Chamaedryos*, à côté du latin *gamandrea*). Le rang médian de cette première occurrence est 2. Les effectifs cumulés atteignent 35 sur 37 à 8 mots et 36 sur 37 à 16 mots. Les noms de rubrique mesurent 4 à 12 lettres. Seules 23 des 37 premières formes conservent la longueur du nom. Dix gagnent une lettre, trois en perdent une et une en gagne deux. Les longueurs portent sur des caractères alphabétiques normalisés. [Positions, graphies, exemples et longueurs](positions_macer.tsv)

## Trois erreurs dont on connaît le sens

- **Un autre nom peut précéder le nom cherché.** La plante *Colubrina* est déjà nommée *dragonteam* au mot 2. Son appellation *colubrina* est au mot 11. Le poème explique qui emploie chacun des noms.
- **Une graphie exacte peut avoir un autre sens sur la bonne page.** Dans *Iris*, le nom de la plante se lit *Iri* au premier mot. L’exact *iris*, treizième mot, désigne l’arc-en-ciel auquel les couleurs sont comparées. Il compte parmi les 19 succès de classement exact à 16 mots. Dix-huit de ces 19 correspondent donc à une reprise exacte de la désignation botanique.
- **Un rapprochement exact peut choisir la mauvaise page.** Chercher *Piper* à 8 ou 16 mots désigne uniquement *Gingiber*, qui cite le poivre au mot 3. La propre notice du poivre introduit *piperis* au mot 22, après une transition vers les produits vendus. Le catalogue de la British Library donne un parallèle matériel indépendant. Dans la copie Harley MS 2651 de 1448, au f. 40r, la rubrique *De pipere* vient après les cinq premières lignes de la section. Ce détail provient de la notice du conservateur, les images étant signalées indisponibles. [Texte de Macer](https://la.wikisource.org/wiki/De_viribus_herbarum) · [Notice Harley MS 2651](https://searcharchives.bl.uk/catalog/040-002048482)

Le patron des lettres produit lui aussi des faux rapprochements. À 16 mots, les huit succès uniques s’appuient sur sept graphies identiques et sur une flexion, *Gariofilus → gariofilum*, de même longueur et de même patron. Les deux erreurs uniques concernent *Chelidonia* et *Verbena*. Ce résultat suppose une substitution bijective lettre pour signe et des limites de mots exactes. Il sert à chiffrer ce qu’une courte forme isolée peut apporter sous ces hypothèses. Il ne livre aucune valeur de signe.

## Le premier nom dépend de la mise en page et de la langue

Les douze premières notices du *Gart der Gesundheit* de Mayence (1485) avaient déjà servi à une expérience à 24 mots, par lots de six. Ici chacune des deux désignations complètes de la rubrique, latine ou allemande, concourt seule contre les douze paragraphes, à 8 et 16 mots. La planche montre la rubrique sur une ligne distincte du corps, sous l’image dans dix cas. Dans les douze paragraphes, l’emplacement de la première grande initiale est vide. Le détail du chapitre V permet de lire la ligne de titre puis le début du corps en caractères plus petits, *grimonia ferraria minor latine*. [Planche des douze pages](../../2026-11-18-mots-et-dessins/herbier_1485/pages.jpg) · [Détail agrandi du chapitre V](../../2026-11-18-mots-et-dessins/herbier_1485/agrimonia-titre-texte.jpg) · [Édition et exemplaires](https://kdih.badw.de/datenbank/druck/70/3/a)

| Nom demandé parmi douze | 8 mots, présence / bonne première place unique | 16 mots, présence / bonne première place unique |
| --- | ---: | ---: |
| Latin complet, mots incertains masqués | 0 / 0 | 0 / 0 |
| Latin complet, première initiale restituée | 10 / 9 | 10 / 9 |
| Allemand complet, mots incertains masqués | 0 / 0 | 3 / 3 |

Les dix noms latins complets retrouvés après restitution commencent tous au premier mot. *Apium* seul renvoie à quatre notices. La graphie du qualificatif de *Apium emoroidarum* est incertaine et *Aristologia rotunda* ne reparaît pas au complet. Parmi les noms allemands, *knobelauch* apparaît au mot 12, *wermut* et *Eppich* au mot 14. Dans la notice d’*Agrimonia*, les mots 2–3 sont *ferraria minor* qualifié de latin au mot 4. *Argemonia* est qualifié de grec aux mots 5–6. Le terme allemand de la rubrique, *odermynge*, vient plus loin sur le scan. Une désignation vernaculaire peut aussi changer à l’intérieur d’une notice. Sous *Aristologia longa / osterlutzye*, les mots 15–16 donnent *lange hoilwurtz*. Ces appellations lues en contexte n’entrent pas dans le score d’identité. La restitution du A initial, commun ici à tous les noms latins, est un essai de sensibilité informé par les rubriques. La série est alphabétique. [Pages du chapitre V](https://www.digitale-sammlungen.de/view/bsb00032739?page=22) · [Chapitre XI](https://www.digitale-sammlungen.de/view/bsb00032739?page=33)

Pour les secteurs de f67r2, ces témoins donnent deux moyens de départager des hypothèses. Lorsque le candidat vient d’une source dans une autre langue, un nom absent des huit premiers mots peut correspondre à un synonyme, à une flexion ou à une désignation vernaculaire plus tardive. Lorsque le seul indice est la longueur du mot, chaque notice concurrente doit rester dans le classement. Même sous une substitution lettre pour signe favorable à la méthode, doubler l’extrait de 8 à 16 mots n’a ajouté aucun succès unique au patron des lettres. Le texte des secteurs du Voynich n’a pas été consulté pour ce contrôle.

## Reproduction

Depuis ce dossier, exécuter `python3 -B mesurer.py`. Le script vérifie les empreintes des deux sources partagées avec les études antérieures et la structure de tous les blocs latins. Les annotations sémantiques ont été ajoutées après extraction. Elles ne sont pas utilisées pour choisir ou classer une notice. Le détail conserve les rangs minimal et maximal de chaque bonne notice et les positions des correspondances. [Protocole enregistré avant ouverture des 37 notices](PROTOCOLE.md) · [Calcul](mesurer.py) · [Résultats](resultats.json) · [Rangs de Macer](rangs_macer.tsv) · [Rangs du Gart](rangs_gart.tsv) · [Attribution et conditions de la transcription de Macer](../../2026-11-18-noms-dans-les-notices/historique/README.md)
