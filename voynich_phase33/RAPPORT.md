# Phase 33 — Les conclusions résistent-elles aux deux découpages ?

**31 octobre 2026 — NOT_TRANSLATION. Phase exécutée.** Les formes communes aux étiquettes d’avril changent avec les coupures. Aucune ne reste commune sous les quatre combinaisons testées, dans ZL comme dans IT. La conclusion prudente est donc maintenue : ces ressemblances ne fournissent pas un indice de sens fiable. Cela ne prouve ni que les groupes doivent être joints, ni qu’ils doivent être séparés, ni qu’ils sont dépourvus de sens.

## Résultat principal : ce qui change

Les deux frontières non résolues en phase 32 sont testées séparément. La première concerne f71r.13, `otolchdy` ou `otol.chdy` ; la seconde f71r.17, `otaldar` ou `otal.dar`. Le point représente uniquement une séparation dans la translittération. Tous les autres signes, séparations, incertitudes et lieux de texte restent fixes au sein de chaque corpus.

| f71r.13 | f71r.17 | Formes communes aux étiquettes d’avril, ZL | Formes communes, IT |
|---|---|---|---|
| Joint | Joint | Aucune | Aucune |
| Joint | Séparé | `otal` | `otal` |
| Séparé | Joint | Aucune | `otol` |
| Séparé | Séparé | `otal` | `otal`, `otol` |

Cette table est identique dans les deux traitements prévus des signes incertains, strict et avec développement des alternatives littérales. Les étiquettes d’avril ne comportent aucune exclusion dans ces comparaisons. ZL d’origine correspond au premier cas ; IT d’origine au dernier. Les deux cas mixtes permettent de distinguer l’effet de chaque frontière.

Il serait donc incorrect de conserver une conclusion absolue telle que « les deux panneaux n’ont aucune forme commune », ou de présenter `otal` et `otol` comme des correspondances indépendantes du découpage. L’existence même d’une intersection varie. En revanche, il reste exact qu’aucun candidat d’étiquette n’est robuste aux **quatre choix testés**. Cette robustesse limitée n’est pas une mesure du sens ni une identification de la vraie segmentation.

## D’où viennent les correspondances ?

`otal` apparaît quand f71r.17 est découpé en `otal.dar`. Il rencontre `otal` à f70v1.16 dans les deux corpus, ainsi qu’à f70v1.11 dans ZL.

`otol` apparaît comme correspondance d’étiquette dans IT quand f71r.13 est découpé en `otol.chdy`. Il rencontre la lecture `otol` de f70v1.11 dans IT. ZL y lit `otal`, ce qui explique pourquoi la même coupure ne produit pas cette correspondance dans ZL. La différence de signe `a/o` a été conservée, pas résolue ou ajustée pour obtenir une intersection. La coupure supplémentaire de f70v1.16 (`okealar`/`okeal.ar`) reste également propre à chaque corpus.

Les [loci soutenant chaque correspondance](results/PAIR_SUPPORTS.json) conservent les lignes et les formes exactes, scénario par scénario. Les variantes sont des hypothèses de traitement des mêmes signes : elles ne deviennent pas de nouvelles lectures historiques.

## Ce qui reste stable, et à quel titre

| Observation | Résultat de phase 33 | Portée |
|---|---|---|
| Formes communes aux étiquettes d’avril | Variables, de zéro à une dans ZL et de zéro à deux dans IT | Dépendance au découpage démontrée dans ces fichiers |
| Candidat d’étiquette commun dans toutes les variantes d’avril | Aucun dans chaque corpus | Aucun candidat robuste à ces deux frontières seulement |
| Étiquette complète identique entre les deux panneaux d’avril, séparateurs retirés | Aucune, dans toutes les variantes et les deux corpus | Comparateur littéral de groupes entiers ; pas une hypothèse de mot unique |
| Formes communes de la paire de mai | Inchangées | Contrôle du traitement, puisque les deux passages de mai ne sont pas modifiés |
| Présence d’au moins une forme commune entre toutes les paires de pages, en incluant les textes circulaires | Toujours 66 paires sur 66 | Une intersection étendue ne suffit pas à localiser un mot de mois |
| Sens, langue, clé ou traduction | Aucun nouvel élément permettant de les établir | Le test ne mesure que la sensibilité des comparaisons à des séparateurs |

Pour mai, ZL conserve `char` et `otaiin` en mode strict, puis ajoute `ar` dans le traitement des alternatives. IT conserve les trois formes. Leur sens n’est pas démontré par cette stabilité. La liste des autres pages où une forme apparaît peut changer si f71r gagne ou perd cette forme ; elle est distincte de l’intersection propre à la paire de mai.

Dans le périmètre de toute la page, les correspondances d’avril sont plus nombreuses et partiellement stables : **3–4 formes dans ZL strict, 8 dans ZL avec alternatives, 9–10 dans IT**. Elles viennent aussi d’autres lieux du texte. Elles ne rétablissent pas un alignement avec une annotation de mois. Le passage à un périmètre plus large ne constitue donc pas une confirmation sémantique.

Les 66 comparaisons d’étiquettes entre panneaux donnent elles aussi des totaux sensibles aux coupures : **32–35 paires non vides en ZL strict**, **36–39 en ZL avec alternatives**, et **39–43 en IT**. Les paires partagent des pages et des tokens : ces nombres ne sont pas des essais indépendants et aucune valeur p n’est calculée.

## Méthode et contrôles

Le protocole, les entrées et le code de calcul ont été gelés au commit `585b1069967bca064f33b4986f96a7b245b5d895`, avant de produire les variantes. La question et les données étaient déjà connues : il s’agit d’une analyse exploratoire de sensibilité, pas d’une validation sur des pages aveugles.

Quatre combinaisons sont calculées dans chacun des deux corpus, avec les deux traitements d’incertitude et les deux périmètres de phase 31. Les 66 paires de panneaux sont toutes conservées. Avec les résultats d’origine, cela donne **2 640 enregistrements dépendants**, dont 528 reproduisent la phase 31. Il ne s’agit ni de 2 640 nouveaux passages ni de nouveaux essais de déchiffrement.

Le parseur de phase 31 est repris à l’octet. Huit fichiers de variantes sont produits sans modifier les sources : le [registre des interventions](results/EDIT_LEDGER.json) enregistre les seize affectations de frontière, les lignes avant/après et leurs empreintes. Certaines affectations retrouvent l’original, ce qui constitue un contrôle : ZL avec les deux groupes joints et IT avec les deux groupes séparés sont identiques à leurs fichiers de départ.

Les vérifications ont confirmé :

- les 528 comparaisons et 48 ensembles de page d’origine reproduits exactement ;
- seuls les points prescrits changent, avec toutes les lettres et toutes les lignes non ciblées conservées ;
- les exclusions de tokens incertains restent identiques ;
- les 55 paires sans f71r conservent leurs ensembles de formes communes dans chaque configuration, soit 1 760 comparaisons de contrôle ;
- les comparaisons d’étiquettes complètes restent invariantes à ces points retirés ou ajoutés.

Une autre implémentation relit 6 700 enregistrements locus/corpus/mode/scénario, vérifie les 240 ensembles de page, les 2 640 comparaisons et leurs justifications. Une reproduction dans un dossier neuf retrouve les seize fichiers de variantes et de résultats à l’octet. Ce sont des preuves de traitement logiciel, pas des validations linguistiques ou humaines.

## Limites et conséquence pratique

Le test couvre les deux frontières désignées. Il ne parcourt pas toutes les coupures possibles, les variantes de signes, les autres transcriptions ou tous les mécanismes de codage. Les quatre extraits GC disponibles en phase 32 ne sont pas transformés en corpus complet ni convertis conjecturalement en EVA. Aucune nouvelle lecture d’image ou expertise humaine n’a été obtenue ici.

L’audit spatial de phase 31 et les observations incertaines de phase 32 ne sont pas réexécutés. Modifier un point dans les fichiers ne déplace pas l’écriture sur la page et n’ajoute aucun témoin sémantique. La phase 33 ne doit pas être présentée comme une nouvelle confirmation de ces observations visuelles.

Pour la suite, les quatre variantes doivent rester explicites dans les analyses. Une correspondance qui n’existe qu’après une coupure incertaine ne peut servir seule à sélectionner cette coupure : ce serait choisir le découpage parce qu’il produit le rapprochement souhaité.

**Les correspondances brutes changent ; aucune traduction n’est établie dans l’un ou l’autre découpage.** Les phases précédentes et leurs résultats sont préservés. Aucun push, publication, déploiement ou message externe.
