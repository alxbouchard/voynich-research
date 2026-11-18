# Peut-on restituer le nom du dessin en couvrant un mot dans la prose ?

À f89r2.22, le cinquième mot est `opcheor`. Si on le couvre, il reste `sheey … opcheol`. Une légende du panneau a exactement les mêmes cinq premières unités que le voisin de droite et en diffère seulement à la fin. Cette règle restitue bien `opcheor`. Elle a été imaginée en connaissant cette paire. Nous avons cherché où elle prendrait un nouveau risque, en inscrivant à l’avance des réponses pour toutes les places entre deux mots lisibles. [Protocole](PROTOCOLE.md) · [Annonces avant comparaison](PREDICTIONS.json.gz)

Les neuf panneaux hors des feuillets 89 et 100 fournissent **429 cases**, dont **396** avec un milieu vérifiable dans les deux transcriptions, blancs faibles joints ou séparés. Seulement trois de ces 396 milieux sont aussi une forme de légende du panneau. Les 33 milieux indéterminés restent au relevé. Même lorsque le mot réel n’est pas une légende, annoncer le nom d’un dessin compte comme une erreur. [Résultats par place, par liste et par règle](RESULTATS.json.gz)

| Règle pour choisir parmi les légendes de la page | Annonces vérifiables | Justes | Reprises de légende retrouvées |
|---|---:|---:|---:|
| Les deux voisins encadrent déjà le candidat sur un autre feuillet | 0 | 0 | 0/3 |
| Au moins un voisin est attesté du bon côté, meilleur candidat unique | 77 | 0 | 0/3 |
| Même forme qu’un voisin à un signe final près, avec au moins quatre signes communs | 1 | 0 | 0/3 |
| Choisir systématiquement la légende la plus fréquente dans la prose des autres feuillets | 303 | 2 | 2/3 |

La seule nouvelle place annoncée par ressemblance finale est le huitième groupe de f88r.27. Le voisin de droite est `oldal`, la légende du panneau est `oldar`, mais la place masquée porte **`aiin`**. Le choix par fréquence trouve réellement `okeody` à f102v1.21 et `cheor` à f102v2.39. Il les annonce aussi à de nombreuses positions erronées, sans utiliser les voisins. En réattribuant les paquets de légendes au sein de chaque cahier, 50,99 % des permutations atteignent au moins ses deux réussites. Le troisième milieu réellement partagé est `okeoly` à f99r.18. [Photographie du mot et de sa légende](../enumeration/photo/NOTE.md)

Les autres paquets du même cahier fournissent 3 bonnes propositions sur 556 pour la règle à un voisin et 0 sur 7 pour la variante finale. Les véritables paquets en fournissent respectivement 0 sur 77 et 0 sur 1. En donnant le même poids à chaque panneau, la règle de fréquence trouve une légende à 0,61 % des positions avec les vrais paquets, à 0,45 % avec ceux des panneaux concurrents. Les prédictions se chevauchent parfois et les lectures proviennent d’un même manuscrit. [Dénominateurs et permutations](RESULTATS.json.gz)

Sur l’ensemble des quinze panneaux, la paire qui a inspiré le test est l’unique succès des sept annonces vérifiables par variante finale. Le critère des deux voisins ne donne qu’une annonce vérifiable, à f89v2.10, et lit à tort `chody` à la place de `or`. Les dix reprises locales recensées dans l’[étude de la formule d’appellation](../lecture/RAPPORT.md) ont été relevées avec d’autres critères. Ici, il faut à la fois une légende de trois unités au moins et un voisin de chaque côté au même rang dans les quatre lectures.

## Une épreuve identique dans un herbier lisible

Dans les quarante extraits du *Macer*, les cinq rubriques de chaque lot font office de légendes. Les sept autres lots fournissent le vocabulaire d’apprentissage. Parmi 3 795 positions intérieures, 20 contiennent à l’identique l’un des cinq mots proposés. La règle des deux voisins n’annonce aucun nom. La règle à un voisin fait une annonce erronée et la variante finale en fait quatre, toutes erronées. Le choix par fréquence réussit une fois en 952 annonces, au cinquième mot de la notice de la rose. Les prévisions sont identiques, lettre par lettre après déchiffrement, quand on remplace tout l’alphabet latin par un alphabet secret. Cette substitution préserve les ressemblances graphiques. Le test ne découvre aucune valeur de lettre. [Extraits du Macer et édition utilisée](../../2026-11-18-noms-dans-les-notices/historique/README.md)

Cet herbier parle effectivement des plantes qu’annoncent ses rubriques. Le faible rendement observé dans les deux corpus ne décide donc pas si le Voynich décrit ses illustrations. Il chiffre le risque d’assigner à un trou précis le nom qu’offre la page. Pour reproduire, exécuter `python3 -B contexte.py` puis `python3 -B verifier.py` depuis ce dossier. [Préparation des contextes](contexte.py) · [Ouverture des mots, contrôles et permutations](verifier.py)
