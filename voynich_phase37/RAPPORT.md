# Phase 37 — Une règle partielle peut être exacte sur des clés stables et trompeuse sur des clés mélangées

17 novembre 2026. **Aucun déchiffrement du Voynich obtenu. Aucune traduction validée.**

La correction du défaut de phase 36 fonctionne sur les douze nouveaux contrôles à clé stable. Elle échoue cependant au contrôle de fiabilité : un texte à clés mélangées est accepté et produit 18 mots normalisés erronés. Le seuil complet fixé avant les résultats échoue. Aucune inférence n'est exécutée sur le manuscrit avec cette méthode.

## Ce qui a été testé

La phase 36 confondait parfois deux mots différents partageant une même fin. Une telle rencontre pouvait invalider toute une règle pourtant correcte. La phase 37 demande plusieurs concordances : au moins trois fins distinctes et 80 % d'accord. Un passage séparé doit retrouver la même correspondance. Des sources multiples répétées pour les mêmes fins provoquent également une abstention.

La règle porte uniquement sur le premier signe du premier mot de chaque ligne. Elle ramène ce signe à un alphabet **encore chiffré**. Elle ne restitue pas une langue, des sons ou le sens des mots.

Le protocole, les sources et les programmes ont été figés avant les nouvelles générations au commit local `10ea73b13c65ad95cc11a6d96aedf9a469613c3d`. Les anciens contrôles ont servi ouvertement au développement ; leurs résultats ne sont pas comptés comme validation nouvelle.

Les nouveaux essais utilisent six triplets de passages de Doyle, Cervantes et Verne. Ils ne recouvrent pas les plages de phase 36. Ce sont de nouveaux passages d'œuvres déjà utilisées, pas de nouveaux auteurs. Chaque triplet comprend 8 000 mots d'apprentissage, 3 000 mots de vérification et 4 000 mots de transfert, avec des intervalles de 200 mots entre les étapes.

Deux mises en lignes et sept familles donnent 84 cas. Les mêmes passages sont réutilisés entre familles et mises en lignes : ces 84 cas ne sont donc pas 84 textes indépendants. Les clés sont nouvelles et absentes des arguments du solveur. Le même opérateur possède cependant le générateur et les réponses ; il ne s'agit pas d'un aveuglement humain ou d'une isolation informatique.

## Résultats nouveaux

Une réussite exige une règle partielle d'au moins trois correspondances, au moins 100 premiers mots produits, une couverture d'au moins 25 %, et aucune erreur. Pour les familles incompatibles avec une clé stable, le protocole exige une abstention complète.

| Famille | Cas | Cas autorisés | Réussites exactes | Mots produits erronés |
|---|---:|---:|---:|---:|
| Substitution spéciale stable en début de ligne | 12 | 12 | 12 | 0 |
| Identité : aucune substitution spéciale | 12 | 12 | 12 | 0 |
| Clé remplacée entre apprentissage et vérification | 12 | 0 | 0 | 0 |
| Ajout d'un préfixe | 12 | 0 | 0 | 0 |
| Groupes générés sans passage cible | 12 | 12 | 12 | 0 |
| Deux clés mélangées dans chaque passage | 12 | **1** | 0 | **18** |
| Initiales remplacées aléatoirement | 12 | 0 | 0 | 0 |

Les douze contrôles positifs retrouvent 85 correspondances partielles au total et normalisent exactement 3 273 premiers mots sur 6 163. La couverture par cas varie de 38,1 % à 66,2 %. Les autres premiers mots restent inconnus ; aucune clé complète n'est revendiquée. Chaque auteur compte quatre réussites sur quatre.

Sur **les mêmes nouveaux textes**, le programme de phase 36 ne réussit qu'un contrôle positif sur douze, contre douze pour la correction. Cette comparaison utilise les mêmes données et évite de confondre le changement de méthode avec l'augmentation de la taille des passages. L'ancien programme s'abstient sur tous les cas à clés mélangées.

Les douze contrôles sans passage cible réussissent aussi. Ce résultat confirme qu'une récupération de correspondances ne permet pas, à elle seule, de distinguer un texte porteur d'un message.

## Le contre-exemple qui empêche l'application au manuscrit

Le cas `c10_mixed_key` emploie le second nouveau bloc de Verne, en lignes de huit mots. À chaque début de ligne, le générateur choisit la seconde clé avec une probabilité de 25 %. Les deux clés diffèrent pour tous les signes.

L'apprentissage et le passage de vérification autorisent les mêmes quatre correspondances. Les votes paraissent convaincants : six fins sur six, six sur sept, sept sur sept et six sur sept. Le détecteur de sources multiples répétées ne trouve pas les trois fins nécessaires à son veto.

Sur le passage de transfert, 127 premiers mots sont alors produits : **109 sont corrects et 18 sont faux**, soit 14,2 % d'erreurs parmi les sorties. En reconvertissant uniquement pour le diagnostic avec la vraie clé connue du contrôle, on observe notamment `et → at`, `entendre → antendre` et `ci → mi`. Ces exemples viennent du contrôle français normalisé ; ce ne sont jamais des lectures proposées du Voynich.

Le problème dépasse donc la collision isolée corrigée : une règle majoritaire peut être stable sur deux passages tout en restant fausse pour certaines occurrences. Les quatre paires sont marquées « invalides » par le protocole parce que ce cas sort du modèle de clé unique ; cela ne signifie pas que chacune produit toujours un résultat erroné.

Deux conditions du seuil échouent : absence totale d'erreurs et abstention sur toutes les clés mélangées. Les seuils ne sont pas modifiés après ce résultat.

## Vérifications et portée

Un programme distinct, qui n'importe ni le solveur ni le générateur, a reconstruit les plages, les clés et les **1 260 000 occurrences chiffrées**, puis contrôlé les décisions des deux programmes, 87 750 prédictions avec abstentions et 21 043 sorties effectives. Il retrouve les mêmes erreurs et la même décision d'arrêt.

Une réexécution dans un dossier temporaire produit **1 266 fichiers identiques octet pour octet**, dont les cas, les résultats des deux programmes, le diagnostic et le tableau CSV. Cette vérification logicielle est faite par le même opérateur ; elle ne constitue pas une expertise linguistique ou paléographique extérieure.

Les fichiers ZL et IT sont copiés et hachés pour contrôler leur intégrité. Aucun ajustement, aucune prédiction et aucune évaluation de cette méthode sur le manuscrit ne sont exécutés après l'échec du seuil.

Les unités graphiques, les espaces et la langue du Voynich restent indéterminés. La recherche de [Feaster (2022)](https://ceur-ws.org/Vol-3313/paper12.pdf) décrit des contraintes positionnelles qui dépassent les extrémités des lignes ; notre hypothèse limitée à la première unité n'en est pas une réplication et n'explique pas toute cette organisation. La [notice de Yale](https://beinecke.library.yale.edu/collections/highlights/voynich-manuscript), consultée le 17 novembre 2026, présente toujours le texte comme non déchiffré.

## Conséquence pour le déchiffrement

Cette expérience améliore un outil dans une famille connue et fournit un contre-exemple précis à sa fiabilité générale. Elle ne révèle aucun mot du manuscrit et ne mesure aucune « proximité » de sa traduction.

La prochaine difficulté à résoudre est de distinguer une correspondance constante d'un mélange de règles sans se fier seulement aux récurrences majoritaires. Une future méthode devra être mise au point sur les cas maintenant connus, puis évaluée sur d'autres contrôles réservés. Même un succès demanderait encore une justification indépendante des valeurs linguistiques et une lecture transférable à d'autres passages. Aucun indice clair/Voynich authentifié n'est acquis dans ce dossier.

Fichiers utiles : [protocole](PROTOCOL.json), [tableau des 168 évaluations](RESULTATS.csv), [résumé machine](results/SUMMARY.json), [diagnostic](results/DIAGNOSTIC_POSTHOC.json), [vérification](results/verification.json) et [réexécution](results/replay.json).
