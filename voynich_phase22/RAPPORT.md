# Phase 22 — correction prudente des fusions : aucun gain sur les nouveaux passages

**Sur douze nouveaux passages de transfert, la correction rétablit
0 séparations oubliées et ajoute 0
fausse(s) coupure(s). L'objectif strict « corriger dans les deux langues sans
ajouter de coupure erronée » n'est pas atteint sur cette série.
6/12 contrôles passent les deux seuils de lettres et d'espaces,
contre 6/12 avant correction. Aucun essai sur le Voynich.**

[Fusions et fausses coupures](https://github.com/alxbouchard/voynich-research/blob/7542c393ad441383c0d9957a1eee999682ba1f03/voynich_phase22/results/conservative_boundaries.png)

## Ce qui a été modifié

Le déchiffreur de phase 21 reste identique : initialisation sur les caractères,
puis affinage avec le modèle de mots connus et inconnus. La phase 22 intervient
**après fixation des lettres**. Chaque frontière déjà proposée est conservée.
Une coupure supplémentaire doit être soutenue par le contexte de trois lettres
à gauche et trois à droite, puis améliorer le score global de segmentation.
Les comparaisons avant/après utilisent donc exactement les mêmes clés.

Le classifieur est entraîné uniquement sur César et Inferno/Purgatorio, avec
repli vers des contextes plus courts et lissage de force 20. Il n'utilise aucune
frontière de Pline ou du Paradiso pour apprendre ses tables. Son résultat est
une fréquence contextuelle lissée, pas une probabilité calibrée de lecture juste.

Le score contraint est celui de phase 21, augmenté de la somme des log-rapports
`log(p / (1-p))` aux nouvelles coupures, avec poids 1. Les nouvelles coupures
doivent avoir `p ≥ 0,90`. La programmation dynamique est exacte dans cet espace
contraint ; elle ne recherche pas toutes les segmentations possibles. Elle
préfère moins d'ajouts en cas d'égalité et conserve le résultat initial si le
gain ne dépasse pas 1e-9. Ce score pondéré n'est pas une vraisemblance normalisée.
Les termes constants omis ne le sont qu'à lettres fixées : ce score ne sert
jamais à comparer des clés différentes.

Cette contrainte empêche toute nouvelle fusion, mais empêche également de
retirer une ancienne fausse coupure. Elle limite donc le progrès possible.

## Réglage sur les anciens passages, puis gel

Les 48 passages des phases 20 et 21 ont servi au développement, à lettres et
espaces connus. Parmi 24 configurations prédéfinies, seuil 0,90 et poids 1
corrigent six fusions (quatre latines, deux italiennes) sans nouvelle fausse
coupure. Cette mesure a servi à choisir le réglage ; elle n'est pas un test réservé.

Le commit **`9f96418`** fige ensuite
le protocole, le moteur, le générateur, le vérificateur et ces résultats avant
de sélectionner les nouveaux extraits ou de générer leurs clés. Aucun réglage
n'a été changé après les nouveaux résultats. Ce gel local n'est pas un
préenregistrement externe, et les œuvres étaient déjà connues de l'analyste.

Douze substitutions monoalphabétiques nouvelles sont cherchées sur environ
250, 500 ou 1 000 lettres sans espaces, puis transférées sans réajustement à
environ 500 autres lettres. Les extraits sont disjoints de ceux des phases 20
et 21 avec une marge de 50 mots ; les deux extraits de chaque contrôle sont
séparés de 50 mots. La langue est fournie au solveur. Les vérités et les passages
de transfert n'entrent pas dans la recherche de clé. Les graphies normalisées
de phase 10 et les deux œuvres de contrôle, Pline et le Paradiso, restent les mêmes.

## Résultats complets sur les passages de transfert

Le critère strict exige au moins une fusion corrigée dans chaque langue et
zéro fausse coupure ajoutée en tout. Le seuil général exige au moins 95 % de
lettres correctes et F1 des frontières au moins 0,90 dans **chacun** des douze
contrôles. Les arrondis du tableau ne modifient pas la décision.

| Contrôle | Lettres correctes | F1 avant | F1 après | Fusions corrigées | Fausses coupures ajoutées | Deux seuils |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| latin_250_1 | 100,00 % | 0,8837 | 0,8837 | 0 | 0 | Non |
| latin_500_1 | 99,80 % | 0,8541 | 0,8541 | 0 | 0 | Non |
| latin_1000_1 | 100,00 % | 0,8876 | 0,8876 | 0 | 0 | Non |
| latin_250_2 | 99,20 % | 0,7682 | 0,7682 | 0 | 0 | Non |
| latin_500_2 | 100,00 % | 0,8364 | 0,8364 | 0 | 0 | Non |
| latin_1000_2 | 100,00 % | 0,8166 | 0,8166 | 0 | 0 | Non |
| italian_250_1 | 98,60 % | 0,9317 | 0,9317 | 0 | 0 | Oui |
| italian_500_1 | 100,00 % | 0,9308 | 0,9308 | 0 | 0 | Oui |
| italian_1000_1 | 100,00 % | 0,9690 | 0,9690 | 0 | 0 | Oui |
| italian_250_2 | 98,80 % | 0,9590 | 0,9590 | 0 | 0 | Oui |
| italian_500_2 | 100,00 % | 0,9606 | 0,9606 | 0 | 0 | Oui |
| italian_1000_2 | 100,00 % | 0,9732 | 0,9732 | 0 | 0 | Oui |

| Langue | Frontières oubliées avant → après | Fausses coupures avant → après | Fusions corrigées | Fausses coupures ajoutées |
| --- | ---: | ---: | ---: | ---: |
| Latin | 93 → 93 | 66 → 66 | 0 | 0 |
| Italien | 33 → 33 | 37 → 37 | 0 | 0 |

Les frontières oubliées passent de **126 à 126**,
et les fausses coupures de **103 à 103**.
La moyenne des F1 par passage passe de **0,8976 à
0,8976** ; les F1 regroupés sont respectivement
0,9097 et 0,9097.
Il faut comparer les deux méthodes sur ces mêmes passages, pas directement
aux chiffres de phase 21 obtenus sur d'autres extraits.

Les six contrôles italiens passent les deux seuils et les six latins échouent,
avant comme après correction. Le passage de 5/12 en phase 21 à 6/12 ici ne
constitue donc pas un progrès de la méthode : les passages ont changé et
la correction ne modifie aucun résultat de transfert.

## Toutes les nouvelles coupures de transfert

Aucune nouvelle coupure proposée.

Le [fichier des décisions](results/aggregate.json) conserve aussi tous les
ajouts sur les passages d'ajustement et avec les lettres exactes.

## Résultats sur les nouveaux passages d'ajustement des clés

Ces passages sont nouveaux pour le réglage de la correction, mais servent à
chercher les clés : ils ne sont pas des passages de transfert. La correction
y rétablit **1 frontière** et ajoute **2
fausses coupures**. Ce résultat défavorable est conservé : zéro erreur sur
le développement ne garantissait pas zéro erreur sur de nouveaux textes.

- `latin_1000_1`, position 718 : `properantque` → `properant que` ; fausse coupure.
- `latin_1000_1`, position 790 : `maturantque` → `maturant que` ; fausse coupure.
- `latin_1000_2`, position 912 : `siorecorticem` → `siore corticem` ; séparation correcte.

Les positions comptent les lettres sans espaces. « Fausse coupure » signifie
ici un désaccord avec les espaces de la source normalisée ; ce critère ne
tranche pas à lui seul le statut linguistique des éléments séparés.

## Diagnostic explicatif ajouté après les résultats

Sur les 126 frontières oubliées en transfert,
**123** ont une fréquence contextuelle
inférieure au seuil figé. Les **3** restantes franchissent
ce filtre, mais leur ajout isolé dégrade encore le score de segmentation ;
le meilleur gain vaut -1,5188.
Le calcul exact contraint confirme qu'aucune combinaison admise n'améliore
le résultat. Le filtre est donc trop restrictif pour corriger ces omissions
dans le dispositif testé ; le modèle lexical résiste aussi aux rares ajouts admis.

Ce [diagnostic postérieur](results/posthoc_diagnostic.json) explique l'absence
d'action. Il n'était pas préenregistré et ne sert pas à retoucher le seuil.
Baisser simplement le seuil ne serait pas une correction validée : la grille
de développement et les deux fausses coupures nouvelles montrent déjà le
risque de réintroduire les erreurs que l'on cherche à éviter.

## Clés et diagnostic à lettres exactes

Les deux méthodes restituent **6008/6026
lettres (99,70 %)**. La correction des espaces ne peut pas
changer ce résultat. Toutes les correspondances observées pendant
l'ajustement sont exactes dans **11/12 contrôles**. Les erreurs de transfert
se répartissent en 4 occurrences de signes déjà observés et
14 occurrences de signes absents de l'ajustement. Une affectation
de clé à un signe absent ne constitue pas une correspondance identifiée.

En fournissant les lettres exactes après les recherches de clés, la correction
rétablit 0 séparations et ajoute
0 fausse(s) coupure(s). Le découpage corrigé atteint
F1 ≥0,90 dans 6/12 cas à lettres exactes. Ce diagnostic ne
compte pas comme réussite de déchiffrement à clé inconnue.

## Vérification

- Les 256 contextes du classifieur vérifiés par comptage indépendant concordent.
- 48 tests courts, incluant un modèle artificiel qui force des ajouts, comparent
  le C++, le programme Python et l'énumération de 6 144 partitions candidates
  avant filtrage des contraintes ; écart maximal 2.84e-14.
- Les 96 sorties sont reconstruites et notées par
  un code Python distinct ; 96 optima sont recalculés
  (48 de base et 48 contraints), avec écart maximal 4.09e-12.
- Les frontières initiales sont préservées partout ; les ajouts, les métriques,
  les 24 extraits source, les marges d'exclusion, les douze nouvelles clés et
  l'absence des vérités dans les commandes de recherche sont vérifiés.
- Le code et le protocole figés sont inchangés depuis le commit de gel.

Le premier lancement du vérificateur a chargé par erreur un module homonyme
de phase 21 et a échoué avant l'audit. Un lanceur explicite ajouté ensuite
permet d'exécuter le vérificateur figé sans en modifier les assertions ni
les résultats de l'expérience. Cette correction d'exécution, postérieure
aux résultats, est documentée dans [l'addendum](AUDIT_ADDENDUM.md).

[Vérification](results/verification.json) · [résultats complets](results/summary.json)
· [agrégats, clés et décisions](results/aggregate.json).
Ces vérifications sont internes, avec les mêmes corpus et modèles, et ne
remplacent pas une réplication extérieure.

## Portée

Ce test mesure une correction précise sur deux œuvres, en langue connue et
sous substitution monoalphabétique. Il ne valide ni une langue, ni un procédé
de codage, ni une traduction du manuscrit. Même un bon score de lettres ne
suffit pas à certifier les mots. Les témoins sans message de phase 19 restent
nécessaires avant toute interprétation du Voynich.

Les paramètres sont conservés tels quels. Si ces erreurs guident une nouvelle
correction, ces passages devront devenir du développement et la nouvelle
méthode devra être évaluée sur d'autres données réservées.

La correction de phase 22 n'est pas retenue comme amélioration : elle ne
corrige aucune fusion en transfert et introduit deux erreurs sur les passages
d'ajustement. La prochaine piste serait de mieux distinguer un mot inconnu
entier de deux mots fusionnés, avec possibilité d'abstention, puis de mesurer
à nouveau le compromis sur de nouveaux passages. Elle reste à tester.

[Méthode et reproduction](README.md) · [protocole figé](PROTOCOL.json)
· [attribution](NOTICE.md).
