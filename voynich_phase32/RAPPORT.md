# Phase 32 — Coupures d’avril : trois lectures IA séparées

**31 octobre 2026 — NOT_TRANSLATION. Phase exécutée ; les deux coupures ciblées restent non résolues.**

Trois agents IA, travaillant dans des contextes séparés sans l’historique du projet, ont examiné les extraits anonymisés. Tous repèrent une séparation possible dans chacun des deux passages principaux, mais la jugent incertaine. Aucun ne fournit la séparation graphique nette exigée par le protocole ; aucun n’établit non plus qu’il s’agit d’un seul groupe. Les deux segmentations doivent donc rester ouvertes.

Ces lectures sont séparées au sens de la procédure, pas trois expertises humaines indépendantes. Les agents héritent de la même configuration de modèle ; leur apprentissage peut être commun. Tous déclarent que les images leur évoquent le Voynich. Les identifiants, le mois, les transcriptions concurrentes et les résultats des autres lecteurs ne leur ont pas été fournis, mais cela ne crée pas un aveugle absolu.

## Résultat principal

| Passage | Agent 1 | Agent 2 | Agent 3 | Conclusion fixée par le protocole |
|---|---|---|---|---|
| f71r.13 | Séparation possible, incertaine | Séparation possible, incertaine | Séparation possible, incertaine | Non résolu |
| f71r.17 | Séparation possible, incertaine | Séparation possible, incertaine | Séparation possible, incertaine | Non résolu |

À f71r.13, les trois lecteurs placent le principal intervalle candidat presque au même endroit, autour de `(349, 203)` dans l’extrait. Ils expliquent que sa largeur ne se distingue pas assez nettement de certains espacements internes. Les nombres de groupes proposés restent respectivement **1–3, 1–2 et 1–2**.

À f71r.17, ils placent également un intervalle candidat près du même endroit, autour de `(184, 209)`, sans le considérer comme une coupure assurée. Les nombres de groupes restent **1–2, 1–2 et 1–3**. Cette convergence sur l’emplacement d’un doute n’est pas une validation de deux mots.

Les deux présentations répétées de chaque cible reçoivent les mêmes classifications chez chaque lecteur. Les trois agents ont toutefois reconnu les répétitions. Cette cohérence n’est donc ni une répétition aveugle ni une augmentation du nombre d’observateurs : il y a **trois lecteurs, quatre images distinctes et dix-huit présentations consultées**.

Les [planches avec les comptes et observations](PLANCHES_LECTURES.md), les [réponses originales](../docs/PIECES_REFERENCES.md#piece-c0c1e3671d82dd) et le [calcul gelé](results/AGREEMENT.json) permettent de vérifier cette conclusion.

## Ce que montrent les extraits de comparaison

À f70v1.11, tous les lecteurs conservent une forte incertitude liée à la pâleur de l’encre ; chacun propose de un à trois groupes graphiques. Aucune valeur de signe, notamment la variante `a/o`, n’a été demandée ni tranchée.

À f70v1.16, les trois agents signalent un intervalle nettement ouvert avec une confiance déclarée élevée, près de `(379, 200)`. Ils ne s’accordent pourtant pas sur toute la segmentation : leurs comptes sont **3, 2–4 et 2–3**. Ce constat secondaire est descriptif. L’emplacement commun a été relevé après les réponses ; il ne constitue pas un contrôle positif à vérité linguistique connue, ni une preuve que les décisions sur les deux cibles sont exactes.

## Ce qui a réellement été comparé

Les quatre loci avaient été sélectionnés et localisés en phase 31. Les lignes ZL et IT sont reprises de ses fichiers inchangés. Les quatre lignes GC ont été lues dans le [fichier publié GC2a-n](https://voynich.nu/data/GC2a-n.txt), dans son alphabet v101. Aucun dictionnaire, nom de mois attendu, conversion automatique en EVA ou essai de clé n’intervient.

Dans ce tableau, le point marque la séparation explicite du relevé, la virgule une séparation incertaine. Le nombre de groupes découle de ces signes de transcription ; il ne compte pas des mots dont le sens serait connu.

| Passage | ZL, EVA | IT, EVA | GC, v101 | Groupes ZL / IT / GC |
|---|---|---|---|---|
| f70v1.11 | `otal.ypsharal` | `otol.ypsharal` | `okAe.9g2ayae` | 2 / 2 / 2 |
| f70v1.16 | `oteoeey.otal.okealar` | `oteoeey.otal.okeal.ar` | `okcocc9.okae.ohcae,ay` | 3 / 4 / 3–4 |
| f71r.13 | `otolchdy` | `otol.chdy` | `okoe189` | 1 / 2 / 1 |
| f71r.17 | `otaldar` | `otal.dar` | `okae.8ay` | 1 / 2 / 2 |

Les formes v101 restent littérales : les ressemblances visuelles entre caractères latins de deux alphabets ne sont pas utilisées comme équivalences. À f70v1.11, le nombre de groupes commun ne résout pas la variante de signe `a/o`. À f70v1.16, GC conserve explicitement le doute sur une séparation supplémentaire. Les [douze formes et comptes](results/ARCHIVAL_COMPARISON.json) et les [extraits sources GC](../docs/PIECES_REFERENCES.md#piece-303db6f12c7d21) restent consultables.

## Quelle indépendance ?

Ces relevés proviennent de traditions d’auteurs distinctes : Zandbergen/Landini, Takahashi dans l’interlinéaire de 1999, et Claston. Leur mise au format IVTFF a toutefois harmonisé les lieux de texte par comparaison des fichiers et des images. Le relevé RF combine ZL et GC : il ne serait pas un quatrième lecteur indépendant. L’historique est décrit par [René Zandbergen](https://voynich.nu/transcr.html).

Il s’agit donc de lectures humaines **déjà publiées**, avec un historique commun de sources et de normalisation. Ce ne sont ni trois nouvelles expertises commandées, ni trois observations aléatoires indépendantes, ni une expérience aveugle. Le coordinateur connaissait déjà ZL/IT et a vu les lignes GC avant le gel de la préparation des nouvelles lectures. La comparaison documentaire est explicitement exploratoire.

## Déroulement et indépendance réelle

Le protocole, les images et l’évaluateur étaient figés au commit `1be0e5a6d7d815fc052afb7ea73daa02eb3d36de`, avant toute nouvelle réponse. Après le choix explicite de plusieurs agents IA par l’utilisateur, les trois missions ont été lancées sans reprise de l’historique de cette conversation (`fork_turns=none`), avec des ordres d’examen différents déjà fixés. Aucun changement de modèle n’a été demandé.

Chaque agent a reçu uniquement un dossier contenant les consignes, six présentations d’images, les rectangles désignant les inscriptions entières et un formulaire. La table des identités et les transcriptions sont restées hors de ce dossier. L’accès n’était cependant pas isolé par le système d’exploitation : les restrictions de consultation reposaient sur les consignes. Les déclarations des agents listent uniquement les fichiers permis, six ouvertures d’images chacun et aucune consultation du web, de mémoire ou de réponse concurrente. Ce sont des déclarations d’accès conservées, pas un audit indépendant du système.

Les trois agents ont terminé avant toute confrontation. Leurs fichiers ont été copiés à l’identique, vérifiés contre les empreintes retournées, puis engagés au commit `9838e0bf2893d675b18e7bff03fa05275d477315`, avant que le coordinateur n’ouvre leur contenu ou ne lance la comparaison. Aucune réponse n’a été réécrite et aucune négociation de consensus n’a eu lieu. Le [registre de lancement](../docs/PIECES_REFERENCES.md#piece-551051f7bb703e) et le [scellement des réponses](RESPONSE_FREEZE.json) conservent la chronologie.

Le critère prévu exigeait trois classifications concordantes et non incertaines, avec répétitions cohérentes. Il n’a pas été assoupli. Le résultat « non résolu » était une issue admissible et ne prouve pas qu’un spécialiste serait incapable de trancher sur ces images ou sur d’autres sources.

## Limites de localisation et de mesure

Les points et boîtes sont des estimations visuelles, pas des mesures de largeur d’encre. À f71r.17, deux points candidats sont placés à `y=209`, soit un pixel hors de la fenêtre prédéfinie commençant à `y=210` ; le troisième est sur la limite. Ce détail est conservé, sans déplacer la fenêtre après observation. Il ne cause pas le rejet : toutes les présentations principales sont déjà marquées incertaines par les lecteurs, et aucune ne contient une séparation déclarée nette avec une confiance élevée. Le classement resterait donc incertain même si ces points étaient inclus.

Dans la sortie du logiciel, le champ `first` désigne l’identifiant canonique de l’image, pas nécessairement sa première présentation temporelle. Le protocole imposant la concordance des deux présentations, cette dénomination ne modifie pas un verdict accepté. Les ordres réels restent conservés.

Les rectangles peuvent inclure des tracés voisins ; les lecteurs en ont tenu compte dans leurs limites. Aucune image n’a été tournée, retouchée, améliorée ou générée. Les six PNG sont toujours des copies exactes des quatre découpes natives utilisées auparavant.

## Vérifications et conservation

Le contrôle logiciel distinct vérifie les trois réponses scellées, les dix-huit observations, leurs coordonnées et les douze classifications des deux cibles avec leurs répétitions. Il retrouve les deux verdicts de l’évaluateur figé. Une reproduction dans un dossier neuf retrouve son résultat à l’octet. Ces contrôles prouvent le traitement déclaré ; ils ne vérifient ni la vérité paléographique ni une indépendance d’apprentissage des modèles.

La confrontation documentaire antérieure et ses douze formes restent inchangées. Les lignes GC proviennent du rendu web du fichier standardisé : les téléchargements directs avaient reçu HTTP 406, et l’original GC n’a pas été authentifié octet par octet. Les limites sont conservées dans le journal d’acquisition et le registre de provenance. Aucun nouveau téléchargement n’était nécessaire pour les lectures IA.

La livraison préparatoire complète reste conservée séparément et son inventaire a été revérifié. Dans les entrées gelées, les mentions « en attente » et les champs de zéro nouvelle lecture décrivent cet état préparatoire ; l’état final est dans [STATUS.json](STATUS.json). Les phases antérieures n’ont pas été modifiées. Aucun push, publication, déploiement ou contact externe.

## Conséquence pour la recherche

Les nouvelles lectures ne permettent de privilégier ni les groupes joints de ZL ni les coupures d’IT aux deux cibles. Les variantes doivent continuer à être calculées séparément. Une prochaine adjudication demanderait un lecteur humain compétent, sans lui fournir le mot souhaité, et une justification explicite des frontières retenues. Même une frontière graphique mieux établie ne suffirait pas à attribuer le nom du mois ni à identifier une clé.

**Zéro frontière linguistique ou équivalence sémantique authentifiée ; aucune traduction validée.**
