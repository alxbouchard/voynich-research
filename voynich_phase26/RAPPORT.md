# Phase 26 — Inventaire des étiquettes, rattachements et faisabilité

**Décision figée : ne pas relancer le test avec le dispositif de phase 25 inchangé.** Même en acceptant hypothétiquement les 35 occurrences textuellement admissibles et en supposant leurs 12 traits tous observables, le contrôle de disposition n'offre que **64 affectations possibles**, sous les **100 exigées**. Cette borne concerne la population, les métadonnées et les bandes de disposition actuelles. Elle ne démontre pas l'impossibilité de toute étude texte–image.

**Aucun nouveau test d'association, score de similarité, trait binaire ou p-value n'a été calculé.** Les seuils et les résultats antérieurs restent intacts. `NOT_TRANSLATION`.

## Ce qui est livré

- [Inventaire lisible, 1 030 lignes CSV](../docs/PIECES_REFERENCES.md#piece-bb2dd5d3d5ff56) : locus, folio physique, section, main attribuée, lectures ZL/IT, statut et exclusions.
- [Inventaire technique complet CSV](../docs/PIECES_REFERENCES.md#piece-3fc1bea8da3e30) et [JSON](../docs/PIECES_REFERENCES.md#piece-0c5558e6fe7580) : lignes originales, empreintes, variantes, récurrences, sources candidates et toutes les alternatives de rattachement.
- [Les 31 fiches de réexamen natif](../docs/PIECES_REFERENCES.md#piece-df870902428f76), [25 cadrages exacts](../docs/PIECES_REFERENCES.md#piece-e6af8079c0a63d), leurs scans sources et les vues de contexte.
- [Catalogue des 342 grandes régions de l'atlas](../docs/PIECES_REFERENCES.md#piece-d0f992cefc94b1). Ce sont des régions descriptives, pas 342 objets individuellement associés à une étiquette.
- [Décision de faisabilité](FEASIBILITY_DECISION.json), [cadre prospectif figé](NEXT_PROTOCOL.json), [décomptes](results/feasibility_reviewed.json) et [vérification indépendante](results/verification.json).

## Un recensement documentaire complet dans un périmètre explicite

L'union des entrées de type générique `L` dans les versions épinglées ZL3b et IT2a donne **1 030 loci documentaires**. ZL en contient 1 029 ; IT en contient 883, dont une entrée `!Lf` marquée inexistante : **f89v2.26**. L'union hors cette entrée fantôme contient donc **1 029 loci**, sans affirmer que chaque ligne correspond à une inscription physique distincte correctement lue.

Le recensement couvre **57 identifiants de page** et **31 numéros de folio physique explicitement attribués**. Les **137 loci fRos** restent sans attribution individuelle entre f85 et f86 : le dépliant est conservé comme un seul groupe de dépendance. Un recto, un verso, un panneau, un scan supplémentaire ou un cadrage ne devient jamais un feuillet indépendant.

Toutes les entrées ont au moins un scan candidat ; **18 ont plusieurs vues candidates**, ce qui n'établit pas leur localisation. Les codes documentaires indiquent le contexte attendu, pas la nature ou le sens démontré du dessin.

| Section documentaire | Loci, entrée fantôme comprise |
|---|---:|
| H | 32 |
| C | 172 |
| T | 60 |
| A | 116 |
| Z | 299 |
| B | 116 |
| P | 235 |

Les mains sont des **attributions des métadonnées**, pas une nouvelle expertise paléographique. Les sources restent séparées. Les récurrences sont calculées littéralement, par source, dans l'ensemble des contextes puis dans la même section/main/type, avec les folios et groupes de dépendance explicités. Aucun choix de variante, fusion d'espace ou rapprochement phonétique n'est ajouté.

Au moins une source signale des lectures alternatives dans 69 loci, des glyphes illisibles dans 49, des espaces incertains dans 47 et plusieurs mots apparents dans 145. Ces catégories se recoupent. Les 20 notations de ligature sont conservées comme conventions d'encodage, sans les déclarer automatiquement erronées.

**La complétude porte sur les entrées `L` de ces deux fichiers.** Elle ne garantit pas d'avoir découvert chaque inscription réelle ni chaque dessin individuel du manuscrit. Les textes circulaires, radiaux ou en paragraphes ne sont pas reclassés arbitrairement en étiquettes. Le catalogue régional couvre les dessins potentiels à une échelle descriptive ; leur délimitation individuelle reste largement à faire.

## Ce qui a réellement été inspecté

L'atlas antérieur a parcouru **213 vues Yale** et décrit 342 grandes régions. Ce parcours de pages n'est ni une lecture de tous les glyphes ni une validation de chaque lien texte–dessin.

La liste de réexamen a été figée avant inspection individuelle : les six exclusions de phase 25, les premières occurrences admissibles selon la règle documentaire dans les folios P/Z/B encore sans examen de motif, les types documentaires non représentés et un cas fRos. Les **31 tentatives prévues sont terminées**, même lorsqu'elles n'aboutissent pas à une localisation ou un rattachement. Le fichier initial `WORKLIST.json` reste inchangé ; son suivi est dans `WORKLIST_COMPLETION.json`.

| Niveau de couverture | Nombre | Portée réelle |
|---|---:|---|
| Loci documentaires recensés | 1 030 | Inclut l'entrée fantôme |
| Loci examinés en phase 25 ou 26 | 60 | 35 anciens + 25 nouveaux ; 6 anciens réexaminés |
| Motifs candidats effectivement inspectés | 58 | Deux recherches n'ont pas localisé de motif attribuable |
| Rattachements géométriques jugés nets | 46 | Même opérateur exposé ; aucune confirmation extérieure |
| Rattachements incertains / non résolus | 9 / 5 | Alternatives conservées |
| Loci sans examen individuel de phase 25 ou 26 | 970 | Le recensement documentaire seul ne les qualifie pas |
| Nouvelles annotations de traits / nouveaux cas admissibles au test | 0 / 0 | Les 29 cas de phase 25 restent les mêmes |
| Relectures humaines indépendantes remises | 0 | Paquets vierges de phase 25 toujours à compléter |

Les 31 nouveaux réexamens donnent 17 rattachements nets, 9 incertains et 5 non résolus. Parmi les 17, trois conservent simplement un rattachement déjà net mais trop peu de traits observables. Les **14 nouveaux rattachements nets** concernent f67, f71, f80, f88, f100 et f102. Cinq de ces folios étaient absents des 35 occurrences de phase 25 ; f88 était déjà présent. Ils enrichissent la cartographie, **sans satisfaire les conditions textuelles du test inchangé**. Les pages avaient déjà été vues dans l'atlas : ce ne sont pas de nouvelles réserves aveugles.

Les 15 loci de l'ancien audit de glyphes de phase 14 sont indiqués séparément ; son ancre supplémentaire f116v.margin n'est pas transformée en entrée `L`. Une ancienne inspection de zone de texte n'est pas comptée automatiquement comme rattachement de motif.

## Ce que les images natives ont clarifié

Les empreintes et dimensions des **213 JPEG locaux**, totalisant **560 960 374 octets**, correspondent à l'inventaire des sources. Seize scans sont copiés dans ce dossier pour les réexamens ; les 25 cadrages sont contrôlés pixel par pixel contre leurs originaux. Aucun masque nouveau, dessin restauré ou détail généré n'est utilisé.

Les requêtes de métadonnées IIIF tentées sur deux vues n'ont pas abouti. Aucun TIFF n'a été téléchargé et aucune résolution supérieure n'est revendiquée. Il s'agit des JPEG natifs disponibles localement ; les agrandir n'ajoute pas de traits disparus.

| Cas | Observation | Conséquence |
|---|---|---|
| f88r.15 | La lame verte rejoint la racine brune par une tige arquée ; une autre étiquette est proche. | Partie ou spécimen connecté complet : incertitude maintenue. |
| f84r.8 | Deux étiquettes surplombent deux figures voisines dans le même bassin. | L'ordre spatial seul ne tranche pas ; incertitude maintenue. |
| f75v.54 | L'ordre des inscriptions aide à situer `otedy` près du coude entrant dans le bassin inférieur. | Texte mieux localisé, mais conduit, bassin et figure restent des candidats ; non résolu. |
| f72v3.27 et .31 | Les figures et petits détails restent très pâles dans les pixels natifs. | Rattachements conservés ; aucun ajout automatique de traits connus. |
| f82v.2 | Le cadrage élargi montre mieux un bras et les structures voisines. | Gain de contexte, sans nouvelle annotation ni qualification automatique à huit traits. |
| f78r et f83r | Plusieurs mots bordent un réseau continûment connecté. | Les sous-parties et l'ensemble restent des alternatives, sans découpage choisi pour améliorer l'effectif. |
| fRos.1 | Une zone d'inscription candidate apparaît entre les premiers cercles. | Lecture incertaine conservée ; référent et attribution physique non résolus. |

Les boîtes nouvelles servent à retrouver approximativement les zones dans les scans ; ce ne sont pas des masques de segmentation exacts. Les anciennes boîtes et alternatives restent enregistrées, même lorsqu'un cadrage plus large est ajouté. La lecture EVA n'a pas été indépendamment revalidée.

## Faisabilité : compter les possibilités, sans mesurer l'association

Le calcul ne compare aucune valeur de trait. Il reconstruit les paires comparables entre **folios physiques distincts**, exige un contraste de même type et de types différents sur la même paire de folios, puis compte types estimables, strates contributrices et affectations conditionnelles possibles. Les seuls masques anciennement connu/inconnu servent au scénario historique.

| Scénario | Motifs | Types / folios / strates du principal | Affectations principales | Affectations avec disposition |
|---|---:|---|---:|---:|
| Annotations historiques réelles | 29 | 8 / 5 / 2 | 64 | 16 |
| Rattachements nets, 12 traits supposés visibles | 32 | 9 / 5 / 2 | 128 | 32 |
| Tous les cas textuels, rattachements et 12 traits supposés parfaits | 35 | 12 / 9 / 3 | 768 | **64** |

Les deux dernières lignes sont **des hypothèses optimistes**, pas des effectifs nouvellement observés. Le principal exige au moins 6 types, 6 folios, 2 strates et 100 affectations. Même lorsque ces conditions principales passent dans la dernière ligne, le contrôle obligatoire de disposition échoue à ses 100 affectations. Ses cinq folios contributeurs et six types sont conservés dans les résultats détaillés.

À population et blocs fixés, retirer un élément ne peut pas agrandir l'espace d'affectation d'un multiensemble : le rapport entre le nombre d'arrangements avant et après retrait est `n / c`, où `c` est la multiplicité du type retiré, donc au moins 1. **Aucun sous-ensemble des 35 ne peut dépasser la borne de 64 pour ces blocs.** Une modification de population, de métadonnées ou de bandes est une nouvelle conception expérimentale à annoncer, pas une récupération obtenue par meilleur cadrage.

Une seconde implémentation reconstruit les neuf combinaisons de scénario et contrôle ; elle énumère les arrangements distincts au lieu de reprendre la formule factorielle du premier calcul. Les décomptes concordent. Cette vérification porte sur le logiciel, pas sur l'exactitude historique des rattachements.

## Décision et travail restant

La décision est **`NO_GO_UNCHANGED_PHASE25_DESIGN`**. Le recensement et la décision de faisabilité sont terminés ; aucun nouvel essai d'association n'est lancé.

Pour envisager un dispositif ultérieur, il reste à localiser individuellement les étiquettes non examinées, inventorier les motifs à cette échelle, résoudre les ambiguïtés de panneau et de référent, vérifier les lectures et coder les traits réellement visibles selon un protocole annoncé à l'avance. Les 137 loci du dépliant ne doivent pas fournir artificiellement 137 unités indépendantes. Les 970 loci sans tentative individuelle comprennent l'entrée fantôme : celle-ci doit rester exclue, sans chercher un objet inexistant.

Toute extension de population ou tout nouveau profil de traits devra porter une version explicite avant mesure, préserver les anciens seuils et résultats, et repasser la faisabilité sur les données réellement qualifiées. Le cadre prospectif livré ne constitue pas une autorisation de lancer cet essai. Les paquets de relecture humaine de phase 25 restent disponibles, sans envoi automatique ; aucune annotation extérieure n'a été reçue.

Toutes les anciennes réserves sont exposées. Le même opérateur a conduit ces réexamens après avoir vu les résultats de phase 25. **Ni un lien géométrique net ni un contrôle logiciel ne démontre le sens d'une étiquette, une langue ou une traduction.**
