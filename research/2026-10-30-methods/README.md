# Recherche de méthodes après la phase 19

État au 30 octobre 2026. **Aucune langue, clé ou traduction du Voynich validée.**
Ce dossier est une recherche de sources et un audit ciblé, pas une phase 20
exécutée. La [phase 19](../../voynich_phase19/RAPPORT.md) reste inchangée.

## Travail effectivement réalisé

Quatre requêtes GitHub archivées ont renvoyé **82 dépôts distincts** sur leurs
premières pages. C'est un inventaire de découverte, pas 82 études vérifiées,
ni une recherche exhaustive de GitHub. La requête générale `voynich` et des
recherches web supplémentaires ont aussi fourni des pistes ; elles ne sont
pas comprises dans ce décompte reproductible.

Le fichier [github-search.json](https://github.com/alxbouchard/voynich-research/blob/7542c393ad441383c0d9957a1eee999682ba1f03/research/2026-10-30-methods/github-search.json) conserve les requêtes et
les résultats. Les empreintes des fichiers récupérés figurent dans
[retrieved-file-hashes.json](retrieved-file-hashes.json). Les textes externes
consultés restent dans `tmp/`, non publié ; les liens ci-dessous donnent les
sources. Aucun solveur ou générateur externe n'a été exécuté dans cet audit.

## Méthodes et conditions d'utilisation

| Source primaire | Ce qui a été consulté | Conséquence pour notre travail |
| --- | --- | --- |
| [Kambhatla, Born et Sarkar, EACL 2023](https://aclanthology.org/2023.findings-eacl.160/), [dépôt](https://github.com/protonish/decipher_symbol_recurrence/tree/3525d314984ec107206acfff358d108c2e74901c) | Résumé de l'article ; arbre Git complet, branche et README. Le dépôt ne contient qu'un README annonçant le code et les données. | Les résultats publiés concernent la substitution, notamment homophonique. Aucune exécution du modèle ici. Le dépôt cité ne permet pas actuellement une réplication directe. |
| [Luo et al., TACL 2021](https://aclanthology.org/2021.tacl-1.5/) | PDF : modèle et contraintes, pp. 71–74 ; expériences et interprétation, pp. 75–78. Page 71 rendue et inspectée. [Dépôt diffusé](https://github.com/j-luo93/DecipherUnsegmented/tree/3cdd0f42572a6af5f4c386a09f322d8fbf3b8347) : README et arbre. | Segmentation et appariement de mots apparentés sont appris ensemble, sous des contraintes phonologiques et d'alignement. Le modèle suppose une écriture alphabétique côté inconnu. Les scores de candidats, parfois parmi dix propositions, ne sont pas un taux de traduction du texte. |
| [Code amont xib de Luo](https://github.com/j-luo93/xib/tree/db3c8a3def0ff47bf3bb2bccf9496fb507bbde07) | Arbre ; configuration de compilation ; début du modèle de déchiffrement. | Le petit dépôt diffusé ne comprend pas tout l'entraînement ; l'amont contient des modules supplémentaires. Compatibilité, données, dépendances et correspondance exacte avec les expériences restent à vérifier. Rien n'a été installé ou lancé. |
| [Lasry, HistoCrypt 2024](https://doi.org/10.58009/aere-perennius0106) | Notice universitaire et extrait indexé de la section 4 du PDF. Téléchargements du texte intégral en échec. | La méthode apprend des statistiques sur des séquences de lettres et syllabes, avec hypothèses sur la décomposition, les homophones et la langue. C'est une piste d'extension, pas une méthode intégralement reproduite dans nos phases 5–6. |
| [CrypTool Transcriber & Solver](https://github.com/CrypToolProject/CTTS/tree/d8b7d77b4e12e7a22d3980f8b5fb4e44c773287b) | Arbre et passages de documentation sur la cryptanalyse. | Le README décrit un solveur homophonique et une révision interactive des clés. Sa disponibilité ne prouve pas qu'il implémente le solveur syllabique de l'article de 2024. |
| [Rozanova et Temerev : voynich-units](https://github.com/lrozanova/voynich-units/tree/956a7c4fc39981f4d116fa3f4edfccce6d065571) | README et arbre de reproduction. | Code, transcriptions et contrôles sont présents. Les mesures d'images archivées et leur recalcul depuis les scans sont deux niveaux distincts. Les tests connexes de notre phase 7 ne constituent pas une réplication complète de ce travail. |
| [Gaskell et Bowern, 2022 : données et code](https://github.com/danielgaskell/voynich/tree/d076a7d081f35098fa405928239595afd2e75927) | README, licence et inventaire des archives. | Les textes sans message produits par 42 volontaires offrent des témoins d'un autre type. Ils sont courts et ne peuvent pas être présentés comme des manuscrits de taille comparable. Leur analyse n'a pas été refaite ici. |
| [Alexander Boxer : Voynich Attack](https://github.com/alexanderboxer/voynich-attack/tree/255bd632e45459230eaf2a994e0557ed6c682869) | README et révision de la branche. | L'auteur décrit une transcription indépendante et des corpus historiques. La transcription peut servir à étudier la robustesse aux unités graphiques ; son exactitude n'est pas validée par la seule documentation. |
| [Zhang et Sheng, prépublication du 25 octobre 2026](https://arxiv.org/html/2610.34499v1) | Résumé, introduction, table 15 et annexe F consultés. | L'annexe F annonce une publication ultérieure du code. Les exclusions revendiquées restent celles des modèles testés par les auteurs. Aucune réplication complète ici, ni preuve universelle d'absence de message. |
| [Layfield et Davis, Singulion Structure, 2026](https://doi.org/10.4000/16k0a) | Résumé diffusé par les auteurs ; annonce de l'éditeur. Le site de l'article est bloqué par une vérification Anubis. | Piste sur l'ordre matériel des feuillets ; aucune lecture linguistique n'en découle. Ne pas reprendre une date de publication précise ni une reconstruction comme acquise à partir d'un article de presse. Texte intégral encore à examiner. |
| [thisisntjon/voynich](https://github.com/thisisntjon/voynich/tree/713fa1003dd56e9526e8596f57128e60e18c02d6) | Arbre et document DEAD-ENDS, dont les retraits et limites de calibration. | Registre utile de pistes et d'échecs à vérifier. Les conclusions de cette équipe, certaines contestées dans son propre registre, ne sont pas des exclusions reproduites par notre projet. |

## Audit ciblé d'un test public de générateurs

Piste signalée par [une analyse méthodologique externe](https://beyond-any-doubt.org/posts/voynich-harness/), puis vérifiée contre les sources primaires :
[prépublication de Yang Ou](https://doi.org/10.21203/rs.3.rs-9755825/v1),
[code](https://github.com/yangou2012/voynich_stt/blob/6d061eb959b1053b35d12a689aa764a8d22930f4/src/04_stt_battery.py#L350)
et [résultats archivés](https://github.com/yangou2012/voynich_stt/blob/6d061eb959b1053b35d12a689aa764a8d22930f4/results/stt_battery_results.json).

La section 3.2.0.8 annonce un écart inférieur à cinq points de pourcentage
entre les précisions de classification. Le code accepte seulement selon
`baseline - synthetic < 0.05`, même quand le texte généré dépasse largement
la référence. Sur les moyennes archivées, le modèle L8b a un écart de
**−0,316175**, soit 31,62 points ; il passe ce test unilatéral mais échoue
au critère bilatéral. En conservant les sept autres décisions publiées,
son total devient **6/8 au lieu de 7/8**. Cinq décisions M8 changent parmi
les dix-huit modèles.

Le [recalcul](ou-m8-audit.json) vérifie les nombres archivés, sans relancer
les générateurs ni les classifieurs. Il ne reconstitue pas non plus la règle
de majorité par exécution annoncée dans l'article : le code statue sur les
moyennes. Ce contrôle ciblé n'est pas une réévaluation complète de l'étude.
La conséquence pratique est de ne pas reprendre sa batterie comme une
preuve prête à l'emploi de présence ou d'absence de sens.

Pour reproduire, récupérer le JSON à la révision indiquée, puis :

```sh
python3 research/2026-10-30-methods/audit_ou_m8.py CHEMIN_DU_JSON
```

Le script refuse un fichier dont l'empreinte ne correspond pas à la source
consultée. Aucune donnée du manuscrit n'est envoyée à un service extérieur.

## Direction retenue pour la suite

La question suivante est la **récupération de correspondances stables lorsque
les unités et les espaces ne sont plus supposés être des lettres et mots**.
La phase 4 avait déjà supprimé les espaces et testé des substitutions
homophoniques avec un score de quatre caractères, en EVA et en signes composés.
La phase 13 avait déjà testé EVA et six groupes graphiques composés ; les
répéter ne constituerait donc pas une nouvelle piste. Une segmentation
conjointe, une transcription indépendante et une calibration sur des systèmes
syllabiques connus apporteraient un test différent.

Avant tout essai interprété sur le manuscrit, il faut vérifier que le modèle
retrouve un texte et ses limites de mots sur des contrôles réservés, puis
mesurer ce qu'il produit sur les témoins sans message de phase 19. Si les
contrôles échouent, le résultat sur le Voynich restera non concluant. La langue
ne sera pas choisie sur la seule facilité à fabriquer des mots plausibles.

Le choix exact des corpus, de la famille de codage et du budget reste à
arrêter et à figer avant les prochains calculs. Ce dossier n'ajoute aucune
lecture ni valeur phonétique au manuscrit.

Un [diagnostic préparatoire de phase 20](../../voynich_phase20/README.md)
exécute ensuite le programme de Hauer, Hayward et Kondrak (COLING 2014)
sur son exemple public et vérifie une alternative au découpage glouton.
Il est distinct de l'audit ci-dessus : aucun texte du manuscrit n'y est ajusté.
