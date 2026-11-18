# Ce que Molina atteste pour les lectures de Tucker et Janick

Molina atteste en 1571 le nom `atl` « eau » et le verbe `mayaui` « jeter, renverser ». Les témoins consultés ne fournissent ni le mot entier `ātlmaāe`, ni un nom nahuatl du XVIe siècle désignant spécifiquement la fougère *Ceratopteris pteridoides*. La notice de Tucker et Janick présente l’espèce avec un point d’interrogation, donne un nom anglais et propose elle-même le rapprochement avec le verbe. Son renvoi ethnopharmacologique concerne un usage du nord de la Colombie et une expérience publiée en 2013 sur des rats. [Tucker et Janick, 2019, p. 46, fig. 4.7](https://doi.org/10.1007/978-3-030-19377-5_4) · [Alviz, Salas et Franco, 2013](https://pubmed.ncbi.nlm.nih.gov/23715314/)

## Lecture de l’imprimé de 1571

| Forme | Lecture et portée | Témoin |
|---|---|---|
| `Atl` | Molina donne notamment « eau ». L’édition analytique de Karttunen distingue `ā-tl` avec une voyelle longue. Molina écrit ici `a` sans marque de longueur. | [Molina II, f. 8r, colonne gauche](https://hdl.huntington.org/iiif/2/p16003coll19:43822/full/1300,/0/default.jpg) · [Notice UNAM](https://gdn.iib.unam.mx/diccionario/atl/35404) · [Karttunen, s.v. Ā-TL](https://nahuatl.wired-humanities.org/content/atl) |
| `Mayaui. nic.` | Jeter quelque chose, prétérit `onicmayauh`. La dernière entrée du recto se poursuit sous deux autres préfixes au verso, `nite` pour renverser quelqu’un, `nitla` pour jeter quelque chose, avec `onitemayauh` et `onitlamayauh`. Cette localisation corrige le renvoi collectif de la transcription de l’Oregon à 51r. | [Molina II, f. 51r, en bas à droite](https://hdl.huntington.org/iiif/2/p16003coll19:43908/full/1300,/0/default.jpg) · [f. 51v, en haut à gauche](https://hdl.huntington.org/iiif/2/p16003coll19:43909/full/1300,/0/default.jpg) · [Notice UNAM](https://gdn.iib.unam.mx/diccionario/mayahui/151348) · [Transcription Oregon](https://nahuatl.wired-humanities.org/content/mayahui) |
| `Atlacui` | Puiser l’eau d’un puits ou réservoir (`onatlacuic`) et aller chercher de l’eau à la rivière (`ononatlacuito`). C’est le verbe invoqué pour `otoly → ātlācai` auprès d’un dessin distinct, f. 101v(1) nº 4, attribué à *Zea* avec réserve. Chez Molina, la forme est `atlacui` et chez Karttunen `ātlacui`. La finale proposée `cai` a un `a` là où l’entrée attestée `cui` a un `u`. | [Molina II, f. 8r, bas de la colonne gauche et haut de la droite](https://hdl.huntington.org/iiif/2/p16003coll19:43822/full/1300,/0/default.jpg) · [UNAM](https://gdn.iib.unam.mx/diccionario/atlacui/35458) · [Oregon](https://nahuatl.wired-humanities.org/content/atlacui) · [Tucker et Janick, 2019, p. 165, fig. 4.124](https://doi.org/10.1007/978-3-030-19377-5_4) |
| `Atlaca` | Molina donne « marins » ou « gens malfaisants ». Ce voisin graphique finit par `a`. L’ajout d’un `i` demanderait son propre témoin. | [Notice UNAM](https://gdn.iib.unam.mx/diccionario/atlaca/35432) · [Imprimé, f. 8r](https://hdl.huntington.org/iiif/2/p16003coll19:43822/full/1300,/0/default.jpg) |

Dans `ātlmaāe`, ôter `ātl` laisse `maāe`. Le GDN normalise `Mayaui, nic` en `mayahui`. Son index du Codex de Florence rattache aussi `maiavi` à ce lemme. Ces alternances historiques de `u`, `hu` ou `v` pour /w/ et les prétérits effectivement imprimés ne fournissent aucune dérivation de `maāe`. L’interprétation « diurétique » exige donc une étape supplémentaire, même lorsque l’on accepte la segmentation initiale. [Exemple du Codex de Florence indexé par le GDN](https://gdn.iib.unam.mx/diccionario/mayahui/203237) · [Analyse de l’orthographe de Molina, INALI](https://site.inali.gob.mx/publicaciones/libro_lectura_nahuatl/pdf/lectura_del_nahuatl.pdf)

## Recherches de formes entières, 18 novembre 2026

Le formulaire du GDN a été interrogé par `GET /termino/search`, sans filtre de dictionnaire. `queryCreiterio` est le nom exact du paramètre. Pour chaque forme UTF-8, `queryPartePalabra=completa`, `queryLimiteRegistros=500` et successivement `queryBuscarEn=nahuatl` (paléographie) et `queryBuscarEn=nahuatlGrafiaNormalizada`. Les décomptes portent sur les fiches, toutes sources et dates confondues. [Formulaire UNAM](https://gdn.iib.unam.mx/) · [Journal des URL, réponses et empreintes HTML](gdn-requetes.tsv)

| Lieu ou rôle | Avec marques, échec technique dans les deux champs | Graphies interrogeables, zéro fiche dans les deux champs |
|---|---|---|
| Fougère proposée, f. 100v | `ātlmaāe` | `atlmaae` |
| Autre attribution publiée, f. 101v | `ātlācai` | `atlacai` |
| Transfert, f. 89r2, `opcheor` | `āhumaāe`, `āgumaāe` | `ahumaae`, `agumaae` |
| Transfert, f. 100v.16, `okeor` | `ātlaāe` | `atlaae` |
| Transfert, `okeol` | `ātlaācâ`, `ātlaāca` | `atlaacâ`, `atlaaca` |
| Transfert, `opcheol` | `āhumaācâ`, `āgumaācâ`, `āhumaāca`, `āgumaāca` | `ahumaacâ`, `agumaacâ`, `ahumaaca`, `agumaaca` |

Les requêtes avec `ā` ont toutes renvoyé HTTP 500 et l’erreur de collation 1267, y compris les témoins positifs `ātl` et `ātlacui`. Les zéros du tableau correspondent exclusivement aux réponses HTTP 200 affichant « No se han encontrado registros ». Les variantes intermédiaires en `â` gardent le circonflexe final du tableau publié et enlèvent seulement les macrons. [Exemple en échec](https://gdn.iib.unam.mx/termino/search?queryCreiterio=%C4%81tlma%C4%81e&queryPartePalabra=completa&queryBuscarEn=nahuatl&queryLimiteRegistros=500) · [Exemple négatif, paléographie](https://gdn.iib.unam.mx/termino/search?queryCreiterio=atlmaae&queryPartePalabra=completa&queryBuscarEn=nahuatl&queryLimiteRegistros=500) · [Exemple négatif, graphie normalisée](https://gdn.iib.unam.mx/termino/search?queryCreiterio=atlacai&queryPartePalabra=completa&queryBuscarEn=nahuatlGrafiaNormalizada&queryLimiteRegistros=500)

| Contrôle | Fiches, paléographie | Fiches, graphie normalisée |
|---|---:|---:|
| `atl` | 19 | 23 |
| `atlacui` | 2 | 11 |
| `atlaca` | 4 | 5 |
| `mayaui` | 0 | 0 |
| `Mayaui, nic` | 2 | 0 |
| `mayahui` | 1 | 29 |
| `maiavi` | 1 | 0 |

Le contrôle `mayaui` illustre la limite de la recherche par mot entier. La forme historiquement lue est incluse dans une entrée munie d’un préfixe et reçoit une autre graphie normalisée. Un zéro borne ce que l’on a trouvé dans ces deux champs du GDN. Il laisse ouvertes une forme fléchie, une graphie absente de l’index ou une attestation dans un autre témoin. La date 1571 est celle de l’imprimé consulté. Elle ne date ni le premier emploi de ces mots ni le manuscrit de Voynich. [Méthode de normalisation du GDN](https://gdn.iib.unam.mx/presentacion)
