# Phase 25 — Étiquettes répétées et traits des dessins

**Résultat : aucune association image–étiquette établie par ce test. L’échantillon exploitable est insuffisant pour une conclusion confirmatoire. `NOT_TRANSLATION`.**

Le contraste principal vaut **−0,0190**, soit −1,90 point de similarité, avec **p = 0,625** dans les 64 affectations conditionnelles possibles. Les occurrences d’une même étiquette ne sont donc pas plus semblables dans cette mesure. Cela ne démontre pas l’absence de relation entre texte et image : cinq folios seulement contribuent, contre six requis, et le minimum de 100 affectations n’est pas atteint.

Étude exécutée le 30 octobre 2026 à Montréal ; clôture documentaire le 31 octobre UTC. Aucune langue, clé ou lecture du manuscrit n’en résulte.

[Contraste observé, distribution conditionnelle et calibration](../docs/PIECES_REFERENCES.md#piece-86614b89a3b777)

## Question et continuité avec les travaux antérieurs

Nous avons demandé si **les répétitions littérales d’une étiquette accompagnent des motifs partageant davantage de traits graphiques observables** que des étiquettes différentes mais comparables. Aucun nom d’objet attendu n’a été fourni au calcul.

Les phases 14–15 avaient testé les correspondances entre légendes et prose, sans fournir de sens lexical. Les phases 23–24 ont montré les limites de la spécificité des contrastes de formes et des associations entre mots. L’atlas fournit les sources iconographiques et leurs limites. Les pièces consultées sont épinglées dans [PRIOR_EVIDENCE.json](../docs/PIECES_REFERENCES.md#piece-d81d4bf822a671). L’atlas ne constitue pas un alignement exhaustif entre chaque signe et chaque objet.

Toutes les anciennes réserves de pages ont déjà été vues. Cette expérience ajoute un protocole et de nouvelles annotations, **pas un manuscrit ni une réserve historiquement inconnus**.

## Décisions figées avant le calcul réel

Le [protocole](PROTOCOL.json), les [définitions des traits](FEATURES.json), le code et les sources ont été figés au commit `2dc6ef4`. Le [premier inventaire d’empreintes](FREEZE.json) couvre 33 fichiers. Les rattachements, annotations et cartes finales ont ensuite été figés par [ANNOTATION_FREEZE.json](ANNOTATION_FREEZE.json), 53 fichiers, puis au commit `da076de`, avant le premier calcul sur le manuscrit.

L’inventaire textuel retient exclusivement des étiquettes uniques d’au moins trois caractères EVA alphabétiques, identiques entre ZL et IT au même locus et de même catégorie documentaire, répétées sur au moins deux folios physiques dans une même section/main attribuée/catégorie. Il contient **15 types, 35 occurrences et 11 folios** : 9 occurrences pharmaceutiques, 20 zodiacales et 6 biologiques. L’accord entre transcriptions n’est pas une confirmation indépendante.

L’inventaire exclut 123 occurrences incertaines ou non unitaires dans ZL, 130 absentes ou différentes dans IT et 361 sans répétition entre folios. Ces filtres ne sont pas une segmentation linguistique et ne représentent pas toutes les étiquettes du manuscrit.

## Rattachements et observation

Les 35 occurrences ont été recherchées sur **16 JPEG natifs Yale**, dont les empreintes sont conservées. Chaque fiche indique la source, le rectangle de l’inscription, celui du motif, les masques, la position et la justification géométrique. Les groupes de loci et les positions horaires documentaires aident au repérage, sans garantir le référent.

- **32 rattachements de confiance haute**, au sens géométrique restreint.
- **2 incertains** : f88r.15, partie ou ensemble d’un motif végétal ; f84r.8, deux figures voisines plausibles.
- **1 non résolu** : f75v.54, attribution à un segment précis du conduit ou de l’enceinte impossible.

Ces trois derniers ne participent pas au calcul principal. Une figure, son étoile tenue et son éventuelle enceinte forment une unité connectée lorsqu’elles sont visibles ; cela n’affirme pas que l’inscription nomme la figure, l’étoile ou leur ensemble. Les hypothèses alternatives figurent dans [attachments.json](../docs/PIECES_REFERENCES.md#piece-89a5641a223409).

Chaque carte a été examinée avec douze traits binaires prédéfinis. Un trait effacé, masqué ou ambigu reste inconnu. Trois autres cartes à rattachement retenu ont moins de huit traits connus : f82v.2, f72v3.27 et f72v3.31. Il reste **29 motifs admissibles** au filtre visuel ; tous ne disposent pas d’un comparateur apparié.

Les recadrages sont exacts, sans restauration générée. Les étiquettes visées sont occultées en tout ou partie, mais des fragments voisins peuvent subsister. Le même opérateur avait déjà vu les transcriptions et les images pendant le rattachement : **l’annotation n’est pas strictement aveugle**. Le découpage des unités, les masques et les critères de coiffe, de cheveux ou d’enveloppe restent sujets à appréciation. Les [limites d’annotation](data/ANNOTATION_LIMITS.md) ont été écrites avant le score réel.

## Comparaisons et absence de pseudoréplication

Une paire exige deux folios physiques différents, la même section, la même main attribuée, la même catégorie d’étiquette, la même fréquence d’inventaire et la même classe de longueur graphique. Les faces et panneaux d’un même folio ne sont pas comptés comme des folios indépendants.

La similarité est la proportion de traits égaux parmi au moins huit traits conjointement connus. Les absences communes comptent ; leur niveau de base est comparé à celui des étiquettes différentes. Pour chaque type et paire de folios, on soustrait la similarité des étiquettes différentes de celle des répétitions. On moyenne ensuite par paire de folios, type, puis strate, avec poids égal entre strates admissibles. Les 38 paires admissibles ne sont pas 38 réplications indépendantes.

Les permutations restent dans la même page, section, main attribuée, catégorie, fréquence et classe de longueur. Elles conservent les effectifs des types par page et donc leur distribution par folio et cahier. Cette condition conserve plusieurs facteurs de confusion, mais l’échangeabilité historique des étiquettes demeure une hypothèse du test.

## Résultats exécutés

| Analyse | Contraste T | p unilatéral exact | Types estimables | Folios contributeurs | Affectations possibles |
|---|---:|---:|---:|---:|---:|
| Principale figée | −0,01903 | 0,625 | 8 | 5 | 64 |
| Même rangée/anneau/bande verticale | −0,02559 | 0,750 | 5 | 5 | 16 |
| Anneau et quadrant, diagnostic additionnel | +0,01742 | 0,500 | 2 | 2 | 8 |

Dans l’analyse principale, deux types pharmaceutiques et six zodiacaux sont estimables. Les folios contributeurs sont **f70, f72, f73, f88 et f99**. Les autres types restent conservés mais sans contraste apparié estimable ; aucune strate biologique ne contribue au score global.

Le [diagnostic d’orientation](ADDENDUM_01.md) a été ajouté après inspection de la disposition radiale, avant annotation et score réel. Il ne remplace pas le protocole initial. Il utilise des quadrants tirés des positions horaires documentaires, approximatives. **Les deux types restant dans ce diagnostic sont seulement pharmaceutiques : aucune comparaison zodiacale ne subsiste.** Son contraste positif n’est donc pas un signal zodiacal qui résisterait au contrôle d’orientation.

Le retrait successif des onze folios donne deux contrastes positifs sur onze ; six retraits ne changent pas le score car leurs folios ne contribuaient déjà pas. En se limitant aux cinq folios contributeurs, seuls **2/5** retraits donnent un contraste positif, sous les 80 % requis. Ce sont des sensibilités internes, pas des réplications.

Les seuils conjoints figés échouent : couverture, amplitude minimale de +0,10, p ≤ 0,05, stabilité et contrôle de position. Le résultat doit rester **exploratoire et non concluant**, même si son sens descriptif ne soutient pas l’avantage recherché. Aucun seuil, trait ou rattachement n’a été réajusté après observation des scores.

## Calibration et vérification

Le même calcul détecte **20/20 contrôles positifs construits**, contre **0/20 contrôles à traits indépendants** et **0/20 contrôles dépendant seulement de la fréquence et de la page**. Cela satisfait les seuils de calibration prévus. Ces 60 jeux sont des matrices de traits synthétiques ; ils ne valident ni la vision, ni le rattachement, ni tous les mécanismes possibles du manuscrit. Zéro détection sur vingt ne signifie pas un taux de faux positifs nul en général.

Une implémentation arithmétique distincte, écrite par le même assistant, retrouve les **88 affectations réelles** — 64 + 16 + 8 — ainsi que les 60 contrastes synthétiques observés. Les trois calculs réels complets ont été répétés à l’identique. Une reproduction complète dans un répertoire neuf a aussi régénéré les 60 calibrations et toutes les mesures réelles : les 63 fichiers JSON correspondants sont identiques octet pour octet ([preuve](results/full_reproduction.json)). Les exemples exacts vérifient également le renommage des types, la déduplication d’objets et l’exclusion des traits inconnus. Les pixels des 35 cartes sont identiques aux sources hors masques, et blancs dans les masques. Ces vérifications ne certifient pas les jugements visuels.

Les inventaires antérieurs des phases 1–17, 22, 23, 24 et de l’atlas ont été revérifiés sans rejouer leurs expériences. [Résultats de vérification](results/verification.json) ; [préservation](results/preservation.json).

## Validation humaine préparée, pas effectuée

Le dossier [human_review_blind](human_review_blind/LIRE_AVANT.md) contient les 35 cartes, des définitions et des formulaires vierges, sans scores ni correspondances d’étiquettes. Un nouveau lecteur doit remettre et faire sceller son codage avant d’accéder aux loci ou aux résultats. Le [second dossier](human_review_linkage/LIRE_APRES_SCELLEMENT.md) permet ensuite une vérification indépendante des rattachements sur les images originales.

Il faudra rapporter les désaccords par trait, les inconnus et les reconnaissances de pages, puis fixer les règles d’arbitrage avant un nouveau calcul. Aucun arbitrage ne doit choisir le meilleur score. Une relecture du même échantillon évaluerait les annotations ; elle ne créerait pas une nouvelle réserve de manuscrit. **Aucun humain extérieur n’a encore validé ce travail.**

Le progrès concret est un test exécuté, traçable et reproductible, avec ses insuffisances. Il ne fournit aucune traduction ni signification de mot.
