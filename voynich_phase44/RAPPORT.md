# Phase 44 — Lectures séparées de la marge de f17r

**Aucune lecture complète ni traduction validée.** Trois agents IA, sans la transcription attendue dans leur contexte, décrivent sept groupes graphiques possibles. Tous s'abstiennent de fournir une lecture continue ; aucun ne propose une translittération EVA complète de la partie droite. La lecture publiée `oteeeon.oiil` n'est donc ni confirmée ni réfutée par cet essai.

## Question et préparation

La marge supérieure de f17r juxtapose des tracés évoquant la cursive latine et des signes de type Voynich. Nous vérifions sa lisibilité avant de l'utiliser comme indice de déchiffrement. Une juxtaposition graphique ne démontre pas que deux portions se traduisent l'une l'autre. La [description du feuillet](https://www.voynich.nu/q03/index.html) signale cette marge et sa difficulté de lecture.

Deux images multispectrales traitées, rendues publiques en 2024, et une photographie Yale sont archivées avec leurs dimensions et empreintes. Les deux fichiers multispectraux correspondent exactement aux empreintes déjà conservées dans l'inventaire du projet. Il s'agit de traitements existants, pas d'une nouvelle acquisition ou d'une nouvelle méthode d'amélioration de l'image. La [notice de diffusion](https://manuscriptroadtrip.wordpress.com/2024/09/08/multispectral-imaging-and-the-voynich-manuscript/) en explique la provenance et les limites.

Le [protocole](PROTOCOL.json), les sources et les sept cadrages natifs ont été figés au commit `35c03294574c7f83bdc57fb68a9d249307d80243`, avant les réponses. Chaque agent a reçu les mêmes sept cartes, dans un contexte neuf, sans nom de folio, transcription attendue, langue ou sens proposés. Les instructions excluaient les autres fichiers, le web et les réponses des pairs. Le coordinateur connaissait déjà la lecture ZL ; son interprétation ne compte pas comme lecture indépendante.

## Résultats conservés

Les positions ci-dessous sont approximatives et rapportées à la largeur des bandes A/B ; elles ne valent pas comme frontières linguistiques.

| Observation | Lecteur 1 | Lecteur 2 | Lecteur 3 |
|---|---|---|---|
| Groupes potentiellement textuels | 7 | 7 | 7 |
| Marques supplémentaires sans lecture | Décrites dans les limites | Une entrée distincte | Une entrée distincte |
| Groupe vers 53–61 % | `o? [hampe] ???` | `o? …` | `o [t?/glyphe à potence?] ? ? ?` |
| Groupe vers 61–65,5 % | `?u?` | `a? u? ?` | `a? u? [y?/d?]` |
| Lecture complète soutenue | Non | Non | Non |
| EVA complet de la partie droite | Aucun | Aucun | Aucun |

Les réponses intégrales [1](readers/reader1.md), [2](readers/reader2.md) et [3](readers/reader3.md), ainsi que leurs JSON originaux, sont conservées. Les ressemblances `o`, `u`, `t`, etc. sont des descriptions hésitantes de formes ; elles ne constituent pas une conversion entre alphabets. Les indices de confiance fournis par les agents sont subjectifs et non calibrés. Aucune moyenne de confiance, correction majoritaire ou lecture fusionnée n'est calculée.

Après archivage des trois réponses, la comparaison avec les transcriptions donne :

```text
ZL, version 3b : <f17r.13,@Lx> oteeeon.oiil
IT, version 2a modifiée : locus f17r.13 absent
```

L'absence dans IT est une omission, pas une transcription contradictoire. Le locus est déjà présent dans ZL : nous n'avons pas découvert une inscription jusque-là non transcrite. Les lectures IA ne permettent pas de remplacer ZL ni d'en établir les caractères et la coupure avec assurance. Le début rond relevé par les lecteurs est trop partiel pour confirmer la séquence entière. Leur abstention ne démontre pas que la lecture publiée est fausse.

## Portée et décision

Le travail établit la traçabilité des images et des réponses, mais n'apporte pas de mot clair authentifié. Cette marge ne fournit donc pas, dans notre dossier, une paire bilingue utilisable comme clé certaine. Aucun sens n'est attribué aux groupes et aucune traduction n'est proposée.

Les agents ont des contextes séparés, mais ne constituent pas trois experts humains ni trois méthodes statistiquement indépendantes. Une familiarité acquise lors de l'entraînement ne peut être exclue. Les traitements A/B partagent les mêmes acquisitions et les détails gauche/droite répètent leurs pixels ; C représente le même support. Le protocole ne comporte pas de contrôle à vérité connue permettant de mesurer la précision de ces lecteurs. Un échec de lecture IA renseigne sur les limites de cet essai, pas sur la lisibilité par un paléographe.

La suite utile consiste à rechercher une contrainte vérifiable sans lecture sémantique supposée, par exemple le lien entre des illustrations répétées et leurs étiquettes. La marge reste disponible pour une expertise paléographique ultérieure, sans choisir arbitrairement une de ses lectures.

## Vérification

Le vérificateur contrôle les 18 fichiers figés, les trois images sources et les sept cadrages par comparaison de leurs octets de pixels avec les lignes des images originales : 4 299 400 pixels présentés, avec recouvrement entre cartes. Il recopie fidèlement les trois réponses JSON, vérifie les sept noms d'images déclarés par chaque lecteur et extrait le locus dans ZL/IT. Cela ne prouve pas que chaque lecture graphique est exacte.

La [reproduction](REPRODUCTION.md) vérifie en dossier neuf les mêmes réponses archivées et les mêmes pixels. Elle ne réexécute pas les jugements des agents. Le [résultat](results/verification.json) et la [collation](results/COLLATION.json) séparent explicitement intégrité des fichiers, lecture et déchiffrement.

Crédit des images multispectrales : **The Lazarus Project and The Chester F. Carlson Center for Imaging Science at Rochester Institute of Technology; Beinecke Rare Book & Manuscript Library MS 408, f17r.** Voir les [sources et crédits](NOTICE.md) et les [images](PLANCHES.md).
