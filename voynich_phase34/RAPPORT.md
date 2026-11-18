# Phase 34 — Une variante a/o croisée avec les quatre découpages

**31 octobre 2026 — NOT_TRANSLATION. Phase exécutée.** À signe et découpage identiques, ZL et IT donnent les mêmes formes communes aux étiquettes d’avril. La correspondance `otol` exige à la fois la lecture `o` à f70v1.11 et la coupure de f71r.13. La correspondance `otal` exige la coupure de f71r.17, mais subsiste avec l’une ou l’autre lecture a/o grâce à un autre emplacement. Aucune forme commune aux étiquettes ne résiste aux huit combinaisons. Le test explique une dépendance des résultats aux choix de transcription ; il ne décide pas quelle lecture est correcte.

## Résultat principal

Une seule position varie entre `a` et `o` : le troisième caractère du premier groupe de f70v1.11, soit `otal.ypsharal` ou `otol.ypsharal`. Ces lettres désignent des signes de translittération, sans valeur phonétique établie. Ce changement local est croisé avec les quatre découpages conservés de phase 33 :

| f71r.13 | f71r.17 | Formes communes avec `a` à f70v1.11 | Formes communes avec `o` à f70v1.11 |
|---|---|---|---|
| Joint : `otolchdy` | Joint : `otaldar` | Aucune | Aucune |
| Joint : `otolchdy` | Séparé : `otal.dar` | `otal` | `otal` |
| Séparé : `otol.chdy` | Joint : `otaldar` | Aucune | `otol` |
| Séparé : `otol.chdy` | Séparé : `otal.dar` | `otal` | `otal`, `otol` |

**La même table s’applique à ZL et IT, dans les deux traitements d’incertitude, strict et avec développement des alternatives littérales.** Aucune étiquette d’avril n’est exclue de ces comparaisons. Les valeurs d’origine sont `a` avec les deux groupes joints pour ZL, et `o` avec les deux groupes séparés pour IT.

L’effet a/o sur `otol` est conditionnel : changer le signe n’ajoute aucune forme commune aux étiquettes si f71r.13 reste joint ; il ajoute `otol` si ce groupe est séparé. Cette interaction était une attente déjà exposée par les résultats de phase 33. Sa vérification n’est pas une prédiction aveugle sur un nouveau passage.

L’existence et le nombre des formes communes changent. En revanche, l’absence de candidat d’étiquette commun aux quatre découpages reste vraie pour chaque signe, et donc aux huit combinaisons. Cela ne prouve ni l’absence de sens du manuscrit, ni la justesse d’un découpage, ni une absence de relation historique entre les panneaux.

## Les emplacements qui expliquent ces effets

Dans les étiquettes d’avril, `otol` met en relation f70v1.11 lu `otol.ypsharal` et f71r.13 découpé `otol.chdy`. Avec `a`, le premier emplacement ne fournit plus `otol`. Avec le groupe joint, le second ne fournit plus ce token séparé.

`otal` met en relation f71r.17 découpé `otal.dar` et f70v1.16, qui conserve `otal` dans les deux corpus et pour les deux signes. La lecture `a` à f70v1.11 fournit un deuxième emplacement de soutien sur f70v1 ; la lecture `o` le retire. La présence de `otal` dans l’intersection peut donc rester identique alors que le nombre de lieux qui le soutiennent change. Le test principal porte sur les formes distinctes, pas sur une fréquence d’occurrences.

Le [registre de soutien](results/PAIR_SUPPORTS.json) conserve les lieux, les numéros de ligne et les chaînes sources pour les deux paires cibles. Le [registre des interventions](results/EDIT_LEDGER.json) fournit les lignes avant/après et les empreintes des variantes.

L’accord ZL/IT de cette table n’est pas une égalité des transcriptions complètes. La séparation supplémentaire de f70v1.16, `okealar` dans ZL et `okeal.ar` dans IT, reste propre à chaque corpus, comme toutes les autres différences non ciblées. Les ensembles portant sur la page entière restent différents.

## Les autres comparaisons conservées

Les 66 paires possibles des douze panneaux sont toutes recalculées, avec le périmètre des étiquettes et celui de tous les lieux de texte, dans les deux modes d’incertitude. Aucun résultat n’est retenu ou écarté selon sa capacité à produire une ressemblance.

| Contrôle ou résultat secondaire | Résultat sur les huit combinaisons | Portée |
|---|---|---|
| Étiquette complète identique entre les panneaux d’avril, séparateurs retirés | Aucune ; aucune exclusion | Comparaison littérale des groupes entiers, sans supposer qu’un groupe est un mot |
| Formes communes aux étiquettes de mai | ZL strict : `char`, `otaiin` ; ZL avec alternatives et IT : `ar`, `char`, `otaiin` ; ensembles inchangés | Contrôle du traitement sur des pages non modifiées |
| Formes communes d’avril sur toute la page | ZL strict : 3–5 ; ZL avec alternatives : 8–9 ; IT : 8–10 | D’autres lieux du texte apportent des formes communes ; aucun alignement sémantique établi |
| Paires non vides sur toute la page | 66 sur 66 dans chaque configuration | Une intersection de formes ne localise pas un nom de mois |
| Paires d’étiquettes non vides sur 66 | ZL strict : 32–35 ; ZL avec alternatives : 36–39 ; IT : 39–43 | Totaux descriptifs, dépendants des mêmes pages et tokens |

Les intersections de page entière conservent notamment `daiin`, `oteody`, `s` dans ZL strict et huit formes dans IT à travers les huit cas. L’absence de candidat invariant annoncée dans le résultat principal concerne donc précisément les **étiquettes d’avril**. Sur toute la page, d’autres occurrences de `otol` existent à f71r : sa présence ne dépend plus nécessairement de la première coupure.

Les étiquettes complètes de mai n’ont pas non plus d’égalité littérale, mais trois étiquettes de f71v et quatre de f72r1 sont exclues de ce contrôle dans ZL parce qu’elles comportent des notations non littérales ; aucune dans IT. Cette comparaison secondaire ne remplace pas celle des tokens avec gestion des alternatives.

Les listes de pages tierces où une forme apparaît peuvent changer lorsque f70v1 ou f71r gagne ou perd cette forme. Elles sont recalculées et distinguées de l’intersection propre à une paire.

## Méthode, gel et mêmes contrôles

Le protocole, les sources et le calcul ont été gelés au commit `34f7445e0696b67905497cd7fbf4c1a0a94eabe1` avant de générer les variantes. Treize fichiers sont couverts par le gel initial. Les données et les effets attendus étaient déjà exposés : il s’agit d’une analyse exploratoire de sensibilité, sans nouvelle réserve aveugle ni préenregistrement externe.

Deux signes × quatre découpages donnent huit variantes par corpus, soit seize fichiers. Avec chaque version d’origine, les deux modes et les deux périmètres, le calcul produit **4 752 enregistrements de paires dépendants**. Ce nombre ne représente pas des textes ou essais indépendants. Aucune valeur p n’est calculée.

Le parseur de phase 31 et les fonctions de phase 33 sont repris à l’octet. Les seuils, les exclusions et les conventions de comparaison ne changent pas. La modification du signe est testée sur un exemple synthétique réversible, avec conservation des fins de ligne et des autres occurrences a/o.

Les contrôles antérieurs sont maintenus en distinguant les facteurs :

- À signe fixe, les **55 paires sans f71r** conservent leurs formes communes entre les quatre découpages : 2 640 comparaisons de contrôle.
- À découpage fixe, les **55 paires sans f70v1** conservent leurs formes communes entre `a` et `o` : 1 760 comparaisons de contrôle.
- Lorsque les deux facteurs varient, les **45 paires sans aucune des deux pages modifiées** restent identiques pour leurs formes communes : 2 880 comparaisons avec les origines. Ce passage de 55 à 45 résulte de la seconde page modifiée ; il ne remplace pas les deux contrôles conditionnels précédents.
- Les ensembles de mai et tous les registres d’exclusions restent inchangés. Les étiquettes complètes sont invariantes aux coupures à signe fixe ; le remplacement a/o peut modifier leur chaîne, même si aucune correspondance complète d’avril n’apparaît ici.
- Les huit variantes gardant le signe natif reproduisent les fichiers de phase 33 à l’octet. Les 2 640 paires, 240 ensembles de page, 80 registres de soutien et 20 comparaisons d’étiquettes complètes de cette phase sont reproduits exactement.

Une vérification distincte du calcul reprend le parseur indépendant de phase 33 : **12 060 enregistrements locus/corpus/mode/version**, 432 ensembles de page, les 4 752 paires, 144 registres de soutien et 36 comparaisons d’étiquettes complètes sont contrôlés. Seuls les deux points prescrits et, dans huit des seize fichiers, un caractère a/o changent. Les autres lignes, lettres, séparateurs, mises en page et fins de ligne sont préservés.

La reproduction dans un dossier neuf retrouve les **24 fichiers de variantes et de résultats à l’octet**. Les 4 679 entrées des inventaires antérieurs, phases 20–33 et atlas, sont conservées. Ces vérifications portent sur le traitement et l’intégrité des données ; elles n’apportent pas une validation paléographique ou sémantique indépendante.

## Limites et conséquence pour la suite

La phase couvre une seule variante de signe et deux frontières précises. Elle n’effectue aucune substitution globale a/o, ne teste pas toutes les incertitudes, ne change aucun autre découpage et ne choisit pas une lecture parce qu’elle produit davantage de ressemblances. Les quatre extraits GC disponibles restent des extraits, sans invention d’un corpus complet ni conversion conjecturale en EVA.

Aucune nouvelle image n’est lue et aucun nouveau lecteur n’est sollicité. Les lectures IA séparées de phase 32 restent limitées à leur dispositif ; elles ne deviennent pas une expertise humaine. Les observations spatiales antérieures ne sont pas réexécutées. Aucun mot clair attendu, langue, clé ou traduction n’est introduit.

Les huit hypothèses doivent rester visibles dans les analyses suivantes. Pour départager le signe ou les coupures, il faudra un argument graphique indépendant du rapprochement recherché ; pour attribuer un sens, il faudra en plus une justification sémantique extérieure. **Cette phase établit une dépendance aux choix de transcription, sans établir de traduction.**

Les phases antérieures sont préservées. Résultats et livraison locaux ; aucun push, publication ou message externe.
