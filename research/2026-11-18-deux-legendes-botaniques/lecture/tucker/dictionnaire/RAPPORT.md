# Deux mots isolés sur les dix de f100v.16

Avec la table et les variantes fixées dans le [protocole de la ligne](../LIGNE.md), deux positions donnent une graphie normalisée enregistrée dans une source du XVIe siècle. Il s’agit de `chol → maca` au mot 2 et de `ches → man` au mot 7. La plus longue suite attestée a donc un seul mot. En inversant les signes à l’intérieur de chaque mot, aucune des dix positions ne donne de fiche. L’écart sur ce seul témoin ne mesure pas la probabilité d’une rencontre fortuite.

| Position | Transcription EVA | Sorties directes testées | Fiches du XVIe siècle | Sorties en ordre inverse, toutes sans fiche |
|---:|---|---|---:|---|
| 1 | ykeeol | itlaaaca, ytlaaaca | 0 | caaaatli, caaaatly |
| 2 | chol | maca | 33 | caam |
| 3 | chey | mai, may | 0 | iam, yam |
| 4 | eeoseeos | aaanaaan | 0 | naaanaaa |
| 5 | sheeo | tsaaa, tzaaa | 0 | aaats, aaatz |
| 6 | okeol | atlaaca | 0 | caaatla |
| 7 | ches | man | 1 | nam |
| 8 | okeor | atlaae | 0 | eaatla |
| 9 | okeol | atlaaca | 0 | caaatla |
| 10 | dy | chi, chy | 0 | ich, ych |

Le quatrième mot suit la segmentation en dix mots choisie avant consultation. Les positions 6 et 9 répètent le même mot. Toutes les graphies marquées zéro restent également sans fiche dans les sources ultérieures interrogées.

## Ce que donnent les fiches anciennes

- **Mot 2, `maca`.** Molina (1571, 2e partie, f. 50r) distingue sur le même feuillet *Maca, nicte* « donner quelque chose à un autre ou le restituer », *Maca, nicno* « prendre un médicament » et *Maca, no*, décrit comme une marque d’interdiction. La recherche en graphie normalisée efface ces distinctions. Choisir le sens médical à partir de l’illustration exigerait de retrouver indépendamment dans la ligne les indices grammaticaux qui le justifient. Le GDN renvoie 33 fiches datées du XVIe siècle, 27 des XVIIe–XVIIIe et 13 des XXe–XXIe. [Donner ou restituer](https://gdn.iib.unam.mx/diccionario/maca/150580) · [Prendre un médicament](https://gdn.iib.unam.mx/diccionario/maca/150579) · [Interdiction](https://gdn.iib.unam.mx/diccionario/maca/150581)
- **Mot 7, `man`.** L’unique fiche, attribuée à Tezozomoc (1598), donne la paléographie *MAN*, le préfixe *ni* et la glose *estar dedicado*, « être voué, consacré ». Le passage cité (f. 096r) situe le mot dans *mapan man* et parle de personnes vouées au sacrifice. Cette attestation explique la glose du dictionnaire. Le rattachement grammatical de ce mot aux positions 6 et 8 du manuscrit reste inconnu. [Fiche Tezozomoc](https://gdn.iib.unam.mx/diccionario/man/175027)

Les huit lacunes empêchent de relier ces deux entrées en une proposition traduisible. Le résultat concerne les graphies entières et le champ interrogé. Une orthographe historique différente ou une analyse morphologique demanderait un autre test.

## Vérification du dictionnaire

Le 18 novembre 2026, les **26 graphies distinctes** des deux listes et deux témoins ont obtenu une réponse HTTP 200. Le témoin positif `atl` a rendu 23 fiches, dont 13 du XVIe siècle. Olmos (1547) donne *atl* « eau ». La chaîne témoin `zzzxqvzzzz` a rendu le message explicite « No se han encontrado registros ». [Olmos, fiche 20262](https://gdn.iib.unam.mx/diccionario/atl/20262) · [Recherche de la chaîne témoin](https://gdn.iib.unam.mx/termino/search?queryCreiterio=zzzxqvzzzz&queryPartePalabra=completa&queryBuscarEn=nahuatlGrafiaNormalizada&queryLimiteRegistros=500)

Chaque requête porte sur le mot entier (`queryPartePalabra=completa`) en graphie normalisée (`queryBuscarEn=nahuatlGrafiaNormalizada`), tous dictionnaires confondus. Le serveur fournit à la grille paginée toutes les lignes dans le tableau JavaScript `mydata`. Le script extrait chaque ligne, contrôle que les identifiants sont distincts et que chaque graphie correspond exactement à la demande. Le plus grand tableau a 73 fiches pour une limite de 500. Les dates suivent l’attribution de la rubrique *Fuente* du GDN, y compris les marques d’incertitude. Les gloses reproduisent l’index de résultats, dont certaines lignes peuvent abréger le texte de la fiche.

Les [résultats structurés](resultats.json) donnent l’URL, l’horodatage et l’empreinte de chaque réponse, toutes les fiches avec leur identifiant et leur source, et le relevé par position. Le [script Python](interroger.py) relit la [liste figée des graphies](../MOTS-A-VERIFIER.json) et espace les requêtes. Depuis ce répertoire, la commande `python3 interroger.py` relance la consultation.
