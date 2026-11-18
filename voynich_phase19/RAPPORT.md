# Phase 19 — les générateurs sans message reproduisent-ils le signal des finales ?

30 octobre 2026. Aucune langue, clé ou traduction du Voynich validée.

**Oui : au moins un texte produit sans message intentionnel reproduit le signal en fin de mot, selon le critère fixé avant calcul.** Ce signal n’est donc pas spécifique d’un message dans ce dispositif. Cela ne prouve pas que le Voynich est dépourvu de sens.

Parmi les six nouveaux textes de Markov, **4/6** satisfont le critère.
L’échantillon publié Timm–Schinner **le satisfait également**.
Tous les tirages et échecs figurent ci-dessous ; aucune graine n’a été choisie
après consultation d’un score.

[Signal observé et témoins](https://github.com/alxbouchard/voynich-research/blob/7542c393ad441383c0d9957a1eee999682ba1f03/voynich_phase19/results/message_free_comparison.png)

## Question héritée de la phase 18

En phase 18, une seconde table de substitution réservée au dernier caractère
du mot améliorait le score hors ajustement. Avec le modèle latin, les gains
ZL/A et ZL/B dépassaient leurs mélanges. Cela justifiait une vérification de
spécificité, pas une identification du latin ni un déchiffrement.

La phase 19 conserve uniquement cette hypothèse : une table unique contre
une table ordinaire et une table finale, espaces fixes, avec le même solveur,
modèle de langue, budget et graine d’optimisation. Le [protocole](PROTOCOL.json)
et le code ont été figés localement dans `5afafb7`, avant génération et
ajustement de phase 19. Ce n’est pas une préinscription externe : le choix
de la finale et du modèle latin vient des résultats déjà connus de phase 18.

## Corpus et critère fixé

Deux observations ZL/A et ZL/B reprennent les feuillets réservés de phase 18,
avec les deux faces d’un même feuillet dans le même ensemble. Ces pages ont
déjà été vues dans le projet. Elles ne constituent pas un nouveau test aveugle.
Le plafond reste de 24 000 lettres d’apprentissage en lignes complètes.

Six textes nouveaux sont produits par un modèle de Markov d’ordre 2, trois
tirages par groupe A/B. Il apprend uniquement les transitions des mots
d’apprentissage retenus pour le score, selon le rôle du prochain signe
(initial, intérieur, final, singleton). Le repli vers les contextes plus
courts utilise un pseudo-compte de 1. Chaque mot est ensuite généré signe
après signe, indépendamment des autres mots, sans texte clair ni clé de
chiffrement. Les caractères d’apprentissage et de test sont régénérés avec
deux graines distinctes. Les lettres du test réel n’ajustent pas le générateur,
mais **ses longueurs et sa disposition sont connues et conservées**.

Un septième témoin est l’échantillon Timm–Schinner publié et déjà archivé.
La première ligne d’amorce issue du Voynich avait été retirée en phase 6.
Le générateur d’origine n’a pas été réexécuté. Ce texte, redisposé sur un
gabarit artificiel, est séparé chronologiquement par pages artificielles
entières ; ses volumes et sa partition diffèrent des observations ZL.

Chaque corpus reçoit dix-neuf mélanges de lettres par feuillet/groupe de
page et rôle dans le mot. Les clés sont réapprises sur chaque mélange.
Contrairement à la phase 18, les segments courts exclus du score restent
fixes : les fréquences des caractères **effectivement notés** sont donc
exactement préservées. Apprentissage et test sont mélangés séparément.

Le critère est identique pour chaque corpus : gain positif, supérieur aux
dix-neuf gains mélangés, et couverture des signes réservés par les signes
d’apprentissage ≥99,5 %. Le gain se mesure en bits par fenêtre de quatre
caractères, espaces compris. Les décomptes sont descriptifs ; aucune p-valeur,
équivalence statistique ou correction pour comparaisons multiples n’est
revendiquée. Le rapport d’amplitude n’est pas un seuil sélectionné après coup.

## Résultats complets

| Corpus | Gain | Étendue des mélanges | Gain − moyenne des mélanges | Mélanges ≥ observé | Couverture (%) | Critère atteint | Gain / ZL associé |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Voynich ZL / A | 1,0038 | 0,1269 à 0,6767 | 0,6054 | 0/19 | 100,00 | Oui | — |
| Généré / A / tirage 1 | 1,3583 | 0,0266 à 0,4044 | 1,1070 | 0/19 | 99,98 | Oui | 1,35 |
| Généré / A / tirage 2 | 0,7003 | 0,0067 à 0,2694 | 0,5215 | 0/19 | 100,00 | Oui | 0,70 |
| Généré / A / tirage 3 | -0,0488 | 0,0116 à 0,4151 | -0,2681 | 19/19 | 99,96 | Non | -0,05 |
| Voynich ZL / B | 1,1996 | 0,1388 à 0,4246 | 0,9648 | 0/19 | 99,99 | Oui | — |
| Généré / B / tirage 1 | 0,3095 | 0,2709 à 0,4674 | -0,0715 | 18/19 | 100,00 | Non | 0,26 |
| Généré / B / tirage 2 | 1,2248 | 0,3011 à 0,5146 | 0,8468 | 0/19 | 100,00 | Oui | 1,02 |
| Généré / B / tirage 3 | 1,1779 | 0,2804 à 0,5804 | 0,7822 | 0/19 | 100,00 | Oui | 0,98 |
| Timm–Schinner (échantillon) | 0,9682 | 0,1204 à 0,4457 | 0,6400 | 0/19 | 100,00 | Oui | — |

Le signe et l’amplitude sont à distinguer : un texte généré peut avoir un
gain différent de celui du manuscrit tout en passant le même critère de
signal. Le rapport d’amplitude compare chaque Markov au groupe ZL qui lui
fournit ses statistiques et son gabarit. Aucune telle correspondance stricte
n’est imposée à l’échantillon Timm.

La variation entre tirages combine les différences des textes générés et
la convergence d’un solveur heuristique à budget fixe. Un échec n’établit
pas l’optimum global. Avec trois tirages par gabarit, ces décomptes ne sont
pas une estimation générale d’un taux de faux positifs.

## Vérification

- Quatre contrôles latins chiffrés, huit ajustements, retrouvent les clés
  et scores de phase 18 : 99,9930 % des lettres réservées et 100 % des finales.
  Ce sont des réexécutions des mêmes contrôles, pas quatre nouvelles clés.
- **368 ajustements** vérifiés : huit de calibration et 360 d’étude.
- **6 466 992 prédictions** réservées recalculées par un second
  décodage et un second calcul de score ; ce total compte les répétitions.
- Les six générations, soit **240 789 caractères**, sont reconstruites
  par un second code à partir des statistiques et graines archivées.
- Les comptes de transitions sont reconstruits à partir des seules pages
  d’apprentissage ; changer les lettres réservées à longueur constante
  n’affecte pas les sorties du générateur dans le test ciblé.
- **342 ensembles mélangés** contrôlés ; écart des fréquences par
  rôle sur les caractères notés : **zéro**. Segments exclus, longueurs et
  barrières sont conservés.
- Les **10 823 mots** de l’échantillon archivé correspondent exactement
  au fichier publié après retrait de sa seule première ligne de texte.
- Les observations ZL non mélangées reproduisent les clés et scores de phase 18.
- Six tests ciblés réussis ; toutes les sorties portent `NOT_TRANSLATION`.

Ce contrôle est interne au projet, avec les mêmes sources et modèle de
langue. Il ne remplace ni une réplication indépendante ni une lecture
paléographique ou linguistique.

## Ce que cela change pour le déchiffrement

**Oui : au moins un texte produit sans message intentionnel reproduit le signal en fin de mot, selon le critère fixé avant calcul.** Ce signal n’est donc pas spécifique d’un message dans ce dispositif. Cela ne prouve pas que le Voynich est dépourvu de sens.

Un générateur fondé sur le Voynich hérite nécessairement d’une partie de
sa structure, et peut reproduire fortuitement des mots de l’apprentissage.
Les trois tirages par gabarit partagent leurs statistiques : ce ne sont pas
des manuscrits indépendants. L’échantillon Timm conserve aussi l’influence
de ses paramètres et de son amorce. Aucun de ces modèles n’est établi comme
procédé historique de rédaction du manuscrit.

Cette expérience teste une mesure, pas l’existence générale d’un sens.
Le même résultat ne pourrait donc pas être utilisé pour déclarer le texte
« traduit », « latin », « faux » ou « dénué de message ». Une piste de
déchiffrement devra apporter des prédictions qui résistent à ces témoins
structurés, une clé stable, des lectures longues et une confirmation externe.

## Suite

Les tableaux, textes générés, clés, sorties complètes, graines, versions et
empreintes restent conservés. L’étape suivante devra rechercher un critère
qui distingue des mécanismes connus porteurs d’un message de générateurs
sans message, sur des corpus et partitions qui n’ont pas servi à le choisir.
La mesure des finales seule ne remplit pas ce rôle si des témoins structurés
la reproduisent. Aucun calcul de phase 20 n’est exécuté ici.

## Sources et reproduction

Les données Voynich et les modèles César/Pline viennent des archives du projet,
sans acquisition d’un nouveau corpus. Le modèle de Markov est développé ici.
Pour Timm–Schinner : [description officielle du générateur](https://github.com/TorstenTimm/SelfCitationTextgenerator#self-citation-text-generator),
[échantillon](https://github.com/TorstenTimm/SelfCitationTextgenerator/blob/master/executable/generate/generated_text.txt),
[article référencé](https://doi.org/10.1080/01611194.2019.1596999).
L’analyse porte sur l’échantillon archivé, pas sur une réplication complète
de cet article. Les droits et la licence MIT sont conservés.

[Notice de reproduction](README.md) · [Résultats JSON](results/summary.json)
· [Vérification](results/verification.json) · [Attributions](../NOTICE.md)
