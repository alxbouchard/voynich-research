# Phase 31 — Les mois lisibles fournissent-ils un alignement avec le texte Voynich ?

**31 octobre 2026 — NOT_TRANSLATION.** L’audit ne trouve pas de dispositif central régulier qui permettrait d’aligner chaque mois lisible avec un mot Voynich. Sur les douze diagrammes, dix n’ont aucune courte légende Voynich autonome visible dans la région définie ; f70v2 en présente une près d’une étoile, et f70v1 plusieurs. La recherche de mots communs aux diagrammes portant le même mois dépend en outre des frontières retenues par les transcriptions. Aucune paire claire–chiffrée n’est authentifiée.

Ce résultat écarte une hypothèse spatiale précise. Il ne prouve ni l’absence de noms de mois ailleurs dans les diagrammes, ni une absence de message, ni la fonction des annotations. Les contrôles de phase 30 ne sont pas transposés : ils disposaient de 26 mots alignés exacts et de 9 mots témoins couvrant l’alphabet, information toujours absente ici.

## La question choisie et ce qui était connu

Le dossier de phase 30 proposait f1r, f116v et f70v2 comme candidats documentaires. Les sources primaires et images accessibles ont été réexaminées avant de choisir un test.

- À f1r, la photographie native est très pâle. La figure multispectrale publiée montre une table à trois colonnes avec plusieurs lectures incertaines. Sa fonction de clé du texte principal n’est pas établie. Les possibilités « tentative de substitution », « exercice personnel » et « mauvais rattachement d’une ligne » restent ouvertes.
- À f116v, les photographies naturelle et traitée montrent une écriture mixte dans des lignes. La proximité d’un groupe Voynich et d’une autre écriture ne démontre pas qu’ils se traduisent. L’alternative `oror/aror` reste conservée ; les images n’autorisent pas ici une nouvelle lecture certaine.

Ces deux réexamens utilisent les figures de la [publication primaire de Lisa Fagin Davis](https://manuscriptroadtrip.wordpress.com/2024/09/08/multispectral-imaging-and-the-voynich-manuscript/), ainsi que les nouvelles copies natives Yale. Ils ne constituent pas une expertise paléographique indépendante. L’attribution et la datation proposées dans cette publication restent celles de l’autrice.

Le zodiaque permet une observation comparative plus concrète : douze panneaux comportent des annotations ordinaires de mois, dont deux paires répétées. Les lectures `aberil` et `may` sont attribuées au [relevé de René Zandbergen](https://voynich.nu/writing.html), sans devenir des traductions de mots Voynich.

Le [protocole](PROTOCOL.json) et les entrées ont été gelés au commit `da26615448ecc12b9bf5cee8e58eddaf61023f1a`, avant les nouvelles annotations et les comparaisons. Les annotations ont ensuite été engagées au commit `f5c882fbd360f6555a17642eb2d1ebc5ead02da1`, avant leur agrégation. Le choix de la question est **exploratoire**, fait après les travaux antérieurs et la lecture des sources. Toutes ces pages avaient déjà été vues ; aucune réserve aveugle n’est revendiquée.

## Forme, groupement, alignement et sens

La région primaire est l’intérieur de la bande de texte circulaire la plus proche de l’emblème central. Les étiquettes séparées y sont relevées, même près d’une étoile. L’écriture du mois, le texte qui suit le cercle, les contours du dessin et les dommages ne sont pas des étiquettes Voynich autonomes. Un doute doit rester explicite.

Cette règle distingue quatre problèmes : reconnaître un tracé, décider quels signes forment un groupe, rattacher le groupe à un élément de la page, puis établir ce qu’il signifie. Même une étiquette bien localisée ne devient pas le nom du mois par proximité.

L’hypothèse testée exigeait **une seule étiquette centrale visible dans chaque panneau**. Un panneau clairement sans étiquette, ou en contenant plusieurs, suffisait à contredire cette condition universelle. Un succès sur douze panneaux n’aurait encore prouvé qu’une condition spatiale nécessaire, pas l’équivalence sémantique.

| Panneau | Étiquettes séparées visibles dans la région primaire | Observation discriminante |
|---|---:|---|
| f70v2 | 1 | Suite de signes près de l’étoile supérieure ; annotation ordinaire entre les poissons |
| f70v1 | Plusieurs : 5 groupes spatiaux | La bande de texte intérieure englobe aussi cinq figures avec leurs légendes |
| f71r | 0 | Inscription ordinaire sous l’animal ; texte Voynich au pourtour |
| f71v | 0 | Même distinction, autour du bovin clair |
| f72r1 | 0 | Même distinction, autour du bovin rouge |
| f72r2 | 0 | Inscription ordinaire entre les personnages centraux |
| f72r3 | 0 | Inscription ordinaire sous les deux formes à pinces |
| f72v3 | 0 | Inscription ordinaire sous l’animal |
| f72v2 | 0 | Inscription ordinaire près du personnage, sans étiquette autonome près de son étoile |
| f72v1 | 0 | Inscription ordinaire sous la balance |
| f73r | 0 | Étoile centrale sans étiquette autonome visible, contrairement à f70v2 |
| f73v | 0 | Inscription ordinaire près des pieds de l’archer ; chevauchement conservé comme limite de lecture |

Les [planches de preuve](PLANCHES.md) donnent les douze extraits natifs, coordonnées et sources. À f70v1, le petit cercle autour de l’animal n’est pas la bande de texte définie avant observation : nous n’avons pas déplacé la limite pour obtenir un zéro. La fiche initiale consignait 5–7 en mélangeant groupes spatiaux et segments possibles ; la [clarification](ERRATA_ET_ADDENDUM.md) conserve l’original et précise cinq groupes, sans prétendre compter leurs mots. La réfutation est inchangée, y compris sans ce panneau grâce aux dix zéros.

Ces comptes concernent les marques visibles et classables dans les images consultées. Ils n’excluent pas une écriture cachée par la peinture, effacée, ou située ailleurs. Le même assistant a effectué toutes les observations ; aucune seconde lecture humaine n’a eu lieu.

## Les mêmes mois donnent-ils les mêmes mots candidats ?

La seconde question est conditionnelle : si les deux annotations d’avril, ou de mai, correspondent au même mot clair sous un encodage fixe et déterministe, les ensembles de mots candidats doivent avoir une forme chiffrée commune. Cette prémisse ne vaut pas pour toutes les langues, variantes orthographiques, flexions, codes contextuels ou homophoniques.

Le calcul compare tous les mots d’étiquettes zodiacales, séparément des mots de toute la page. ZL et IT sont conservés séparés. Le mode strict exclut les tokens incertains ; la sensibilité développe uniquement les alternatives littérales entre crochets et traite les virgules comme coupures. Toutes les exclusions restent listées. Aucune recherche par ressemblance, dictionnaire ou mot espéré n’est utilisée.

| Paire de panneaux | ZL, étiquettes strictes | IT, étiquettes strictes | Sensibilité fixée |
|---|---|---|---|
| f70v1 / f71r, avril attribué | Aucun token commun | `otal`, `otol` | ZL reste vide ; IT reste identique |
| f71v / f72r1, mai attribué | `char`, `otaiin` | `ar`, `char`, `otaiin` | ZL ajoute `ar` ; IT reste identique |

Le résultat d’avril n’est donc **pas une réfutation robuste de toutes les variantes**. L’examen documentaire des loci explique la divergence :

| Locus | ZL | IT | Différence |
|---|---|---|---|
| f70v1.11 | `otal.ypsharal` | `otol.ypsharal` | Lecture du signe `a/o` |
| f71r.13 | `otolchdy` | `otol.chdy` | Frontière ajoutée dans IT |
| f71r.17 | `otaldar` | `otal.dar` | Frontière ajoutée dans IT |

Les deux correspondances d’IT à f71r apparaissent après ces coupures. Les images localisent les suites et leurs intervalles ; elles ne certifient pas à elles seules une frontière de mot. Cette inspection ciblée a été choisie **après** le calcul : elle est diagnostique et n’a modifié aucun résultat gelé. Les premiers essais de localisation par l’angle seul, qui visaient le mauvais anneau, restent documentés avec les extraits corrigés.

Pour mai, les formes communes ne sont pas des étiquettes entières identiques : `char.arom`/`char.alif` dans ZL, et `otaiin`/`otaiin.otain`. Les formes `char` et `otaiin` sont communes aux deux transcriptions, mais rien ne les identifie au mois. Leur absence des étiquettes des dix autres panneaux dans cette extraction ne suffit pas à leur donner un sens. Dans le cadre « tous les loci », plusieurs réapparaissent aussi ailleurs.

Les 66 paires de panneaux sont calculées dans chaque combinaison corpus/mode/périmètre, soit **528 comparaisons descriptives**. En mode strict, une intersection non vide apparaît dans32/66 paires d’étiquettes ZL et43/66 IT ; toutes les 66 paires partagent au moins un token lorsqu’on inclut les autres textes de page. Une intersection seule n’identifie donc aucun alignement particulier. Aucune valeur p n’est calculée : ces comparaisons sont dépendantes, sur quatre folios physiques.

## Ce qui change réellement

L’hypothèse d’un petit glossaire bilingue répété au centre de chaque diagramme n’est pas soutenue par la disposition visible définie et testée. L’idée plus large de mots de mois quelque part dans les diagrammes reste ouverte, mais sans localisation ni équivalence authentifiée. Les deux paires répétées ne fournissent pas un indice clair utilisable : avril dépend de la transcription, mai laisse plusieurs candidats sans rattachement sémantique.

Les variantes de f1r et f116v restent des questions documentaires, sans nouvelle clé ni nouveau mot traduit. Le prochain travail discriminant porterait sur une transcription indépendante des frontières précisément localisées et, séparément, sur une preuve historique du lien avec un texte clair. Résoudre une coupure améliorerait le texte de travail ; cela ne transformerait pas un candidat en traduction.

## Sources accessibles, corrections et vérification

Dix JPEG natifs Yale ont été récupérés, dont huit couvrent les douze diagrammes. Leurs dimensions et SHA-256 correspondent aux originaux répertoriés. L’article de Davis et trois figures publiées sont archivés. Les quatre pages Zandbergen ont été lues avec l’outil web ; le téléchargement de leur HTML a reçu HTTP 406, enregistré sans prétendre à un archivage de ces octets. Les fichiers multispectraux originaux ne sont pas présents aux chemins du checkout et n’ont pas été retéléchargés pour cet audit ; les figures publiées utilisées sont bien identifiées comme des dérivés.

Le contrôle a aussi découvert une erreur de description dans la livraison30 : ses images f1r/f116v étaient des vues réduites recopiées à l’identique, pas les JPEG natifs annoncés. Le [correctif traçable](ERRATA_ET_ADDENDUM.md) donne les deux dimensions et empreintes. Les anciens fichiers restent intacts ; la calibration synthétique de phase 30 n’est pas affectée.

La vérification indépendante du logiciel relit 1 340 enregistrements locus/corpus/mode,48 ensembles de page et528 intersections, puis vérifie 21 extraits contre les pixels natifs. Le replay retrouve à l’octet les deux sorties du calcul gelé. Ces contrôles prouvent le traitement annoncé, pas une expertise humaine des signes. Les inventaires antérieurs sont préservés.

**Aucune recherche de clé, langue ou traduction n’est lancée.** Il manque toujours une équivalence claire–Voynich justifiée extérieurement et un témoin distinct, qui n’aurait pas servi à la choisir.
