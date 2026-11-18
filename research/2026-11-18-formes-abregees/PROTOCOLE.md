# Une forme longue peut-elle être retrouvée sans connaître les lettres ?

Protocole du 18 novembre 2026, à enregistrer dans Git avant l'ouverture du lot de contrôle. La première épreuve porte sur un manuscrit lisible. Elle conditionne l'emploi de la règle sur le Voynich.

## Témoin et séparation des passages

Nous choisissons un seul témoin de *Piers Plowman*, Huntington Library, HM 128, dans son [édition électronique](https://piers.chass.ncsu.edu/texts/Hm/intro). Le [XML Hm](https://piers.chass.ncsu.edu/texts/xml/HmWhole.xml) distingue des lettres développées par les éditeurs. Le fragment Hm2 appartient à un autre témoin. Dans Hm, le prologue et les passus 1 à 9 servent à chercher les correspondances. Les passus 10 à 12 séparent les lots. Les passus 13 à 20 forment le lot réservé. Les frontières de vers sont conservées.

Une précédente étude du projet a utilisé cette édition pour vérifier une règle différente, celle du trait nasal. Une partie de ces pages a donc déjà servi au projet. La nouvelle mesure repose sur une règle fixée avant le calcul et sur une séparation des entrées du programme. Elle n'établit pas que l'opérateur ignore la langue ou n'a jamais vu ces pages.

L'extracteur sépare pour chaque mot la suite des lettres visibles et celle qui inclut les développements marqués par les éditeurs. Il applique la même substitution bijective aux lettres des deux suites. Le prédicteur reçoit uniquement les formes visibles anonymisées, le numéro du vers et le passus. Ni les lettres rétablies, ni le statut abrégé du mot, ni la place des lettres manquantes ne lui sont fournis, même sur le lot d'apprentissage. Une lettre visible reste un signe. La position des mots et des vers est fournie. Le détail des conventions de l'édition et des exclusions sera documenté avec les résultats.

## Règle et prédiction

On examine chaque mot intérieur X comprenant au moins deux signes, avec un voisin L à gauche et un voisin R à droite sur le même vers. Dans les vers d'apprentissage, il faut trouver à la fois L X R et L Y R. Y s'obtient en insérant dans X une seule suite contiguë de un à trois signes, à n'importe quel emplacement. Les voisins doivent être strictement identiques. Sur le lot réservé, en présence de L X R, la règle annonce le Y entier s'il existe un seul Y distinct. Elle s'abstient dans tous les autres cas. Les égalités sont des égalités de mots complets.

Le fichier des annonces est engagé dans Git ou par son empreinte inscrite dans Git avant d'ouvrir le corrigé. Aucune proposition nouvelle ne s'ajoute ensuite. La mesure principale compte séparément les développements exacts, les fausses expansions sur une graphie déjà complète et les expansions erronées d'une véritable abréviation. Le rapport donne les abstentions, le nombre réel d'abréviations à ces positions, les résultats par passus et la couverture. Une forme visible identique à sa forme éditoriale constitue une réponse exacte pour le témoin d'identité.

## Deux comparaisons et un texte sans message

Aux mêmes emplacements annoncés, la première réponse témoin conserve X. La seconde donne le développement admissible le plus fréquent parmi les mots visibles de l'apprentissage, sans consulter les mots voisins. Le comptage porte sur les occurrences. L'ordre des signes anonymes départage les ex æquo. Ainsi, la méthode doit apporter quelque chose de plus que la préférence pour une forme fréquente.

Un second texte est produit sans vocabulaire historique ni phrase cible, avec la graine 20261118, 16 signes et 96 mots de deux à sept signes. Mille vers initiaux contiennent huit mots chacun. Quatre mille autres sont obtenus en copiant un vers antérieur puis en modifiant un seul mot par insertion ou suppression de un à trois signes, en conservant au moins deux signes. Mille nouveaux vers du même processus servent de réserve. Chaque mot produit y est complet par construction. Toute annonce de développement constitue donc une fausse alerte. Cette simulation mesure la propension de la règle à confondre ressemblance et abréviation dans ce seul scénario.

## Décision fixée avant le score

Pour avancer vers le Voynich, il faut remplir **toutes** les conditions suivantes.

- Au moins 20 annonces sur le lot réservé, réparties dans au moins trois passus et sur au moins cinq formes courtes distinctes.
- Au moins 80 % de mots entiers exacts parmi les annonces.
- Strictement plus de succès que chacune des deux réponses témoins, aux mêmes emplacements.
- Au plus 1 % de fausses expansions sur toutes les positions intérieures admissibles du texte sans message.

Ces seuils constituent une décision pratique pour cette expérience. Le score conserve ses dénominateurs et les erreurs même si la règle s'abstient presque partout. Si un seuil manque, le test s'arrête au manuscrit connu. Un échec ne serait une mesure ni de toutes les méthodes d'abréviation ni de la nature du Voynich. Toute modification de la règle après le score demanderait une autre réserve.
